# Quick Start: Document Q&A with Streamlit

Build a working document Q&A system in **3-5 days**!

## What You're Building

A Streamlit web app where users can:
1. ✅ Upload documents (PDF, Word, Excel, CSV, TXT, JSON)
2. ✅ Documents automatically embedded in ChromaDB
3. ✅ Ask questions via chat interface
4. ✅ Get answers with source citations

---

## Prerequisites

```bash
# Make sure you have:
- Python 3.10+
- Ollama installed with llama3.2 model
- Basic understanding of Python
```

---

## Day 1: Foundation (3-4 hours)

### Morning: Setup Core Components

#### Step 1: Create Directory Structure (5 min)
```bash
mkdir -p config/prompts
mkdir -p src/{core,data/loaders,data/processors,interfaces,utils}
mkdir -p data/{uploads,vectorstore}
mkdir -p tests
```

#### Step 2: Create `.env` File (5 min)
```bash
touch .env
```

Add this content:
```env
# LLM Configuration
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2
LLM_BASE_URL=http://localhost:11434

# Embedding Configuration
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=mxbai-embed-large

# Vector DB Configuration
VECTOR_DB=chroma
VECTOR_DB_PATH=./data/vectorstore

# Application Settings
LOG_LEVEL=INFO
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=5
```

#### Step 3: Install Dependencies (10 min)
```bash
# Create requirements.txt
cat > requirements.txt << 'EOF'
# Core RAG
langchain>=0.1.0
langchain-core>=0.1.0
langchain-ollama>=0.0.1
langchain-chroma>=0.1.0
chromadb>=0.4.0

# Streamlit
streamlit>=1.28.0
streamlit-extras>=0.3.0

# File Processing
pypdf2>=3.0.0
pdfplumber>=0.10.0
python-docx>=1.0.0
openpyxl>=3.1.0
pandas>=2.0.0

# Utilities
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
EOF

# Install
pip install -r requirements.txt
```

### Afternoon: Build Core Components

#### Step 4: Create Settings (30 min)

**File:** `config/__init__.py` (empty file)
```bash
touch config/__init__.py
```

**File:** `config/settings.py`
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM Configuration
    llm_provider: str = "ollama"
    llm_model: str = "llama3.2"
    llm_base_url: str = "http://localhost:11434"

    # Embedding Configuration
    embedding_provider: str = "ollama"
    embedding_model: str = "mxbai-embed-large"

    # Vector DB Configuration
    vector_db: str = "chroma"
    vector_db_path: str = "./data/vectorstore"

    # Application Settings
    log_level: str = "INFO"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 5

    class Config:
        env_file = ".env"

settings = Settings()
```

**Test:**
```bash
python -c "from config.settings import settings; print(settings.llm_model)"
# Should print: llama3.2
```

#### Step 5: Create Base Loader (45 min)

**File:** `src/__init__.py` (empty)
**File:** `src/data/__init__.py` (empty)
**File:** `src/data/loaders/__init__.py` (empty)

**File:** `src/data/loaders/base.py`
```python
from abc import ABC, abstractmethod
from typing import List
from langchain.schema import Document
from pathlib import Path

class BaseLoader(ABC):
    """Abstract base class for all data loaders."""

    def __init__(self, source: str):
        self.source = source

    @abstractmethod
    def load(self) -> List[Document]:
        """Load documents from source."""
        pass

    @abstractmethod
    def validate_source(self) -> bool:
        """Validate that source exists and is accessible."""
        pass

    def _create_document(self, content: str, metadata: dict) -> Document:
        """Helper to create Document objects."""
        return Document(page_content=content, metadata=metadata)
```

#### Step 6: Create Text Loader (30 min)

**File:** `src/data/loaders/text_loader.py`
```python
from pathlib import Path
from typing import List
from langchain.schema import Document
from .base import BaseLoader

class TextLoader(BaseLoader):
    """Load documents from text files (.txt, .md)."""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.file_path = Path(file_path)

    def validate_source(self) -> bool:
        return self.file_path.exists()

    def load(self) -> List[Document]:
        if not self.validate_source():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        content = self.file_path.read_text(encoding='utf-8')

        metadata = {
            "source": str(self.file_path),
            "file_name": self.file_path.name,
            "file_type": "text"
        }

        return [self._create_document(content, metadata)]
```

**Test:**
```bash
# Create test file
echo "This is a test document." > test.txt

# Test loader
python -c "
from src.data.loaders.text_loader import TextLoader
loader = TextLoader('test.txt')
docs = loader.load()
print(f'Loaded {len(docs)} document(s)')
print(f'Content: {docs[0].page_content}')
"
```

#### Step 7: Create PDF Loader (45 min)

**File:** `src/data/loaders/pdf_loader.py`
```python
from pathlib import Path
from typing import List
from langchain.schema import Document
from .base import BaseLoader
import pdfplumber

class PDFLoader(BaseLoader):
    """Load documents from PDF files."""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.file_path = Path(file_path)

    def validate_source(self) -> bool:
        return self.file_path.exists() and self.file_path.suffix.lower() == '.pdf'

    def load(self) -> List[Document]:
        if not self.validate_source():
            raise FileNotFoundError(f"PDF not found: {self.file_path}")

        documents = []

        with pdfplumber.open(self.file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()

                if text and text.strip():
                    metadata = {
                        "source": str(self.file_path),
                        "file_name": self.file_path.name,
                        "file_type": "pdf",
                        "page": page_num,
                        "total_pages": len(pdf.pages)
                    }

                    documents.append(self._create_document(text, metadata))

        return documents
```

---

## Day 2: Core RAG Components (3-4 hours)

### Step 8: Create Embeddings Manager (30 min)

**File:** `src/core/__init__.py` (empty)

**File:** `src/core/embeddings.py`
```python
from langchain_ollama import OllamaEmbeddings
from config.settings import settings

class EmbeddingManager:
    """Manage embedding model."""

    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=settings.embedding_model,
            base_url=settings.llm_base_url
        )

    def embed_documents(self, texts):
        return self.embeddings.embed_documents(texts)

    def embed_query(self, text):
        return self.embeddings.embed_query(text)
```

### Step 9: Create Vector Store Manager (1 hour)

**File:** `src/data/vectorstore.py`
```python
from typing import List
from langchain.schema import Document
from langchain_chroma import Chroma
from config.settings import settings
from src.core.embeddings import EmbeddingManager

class VectorStoreManager:
    """Manage vector database operations."""

    def __init__(self, collection_name: str = "default"):
        self.collection_name = collection_name
        self.embedding_manager = EmbeddingManager()
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embedding_manager.embeddings,
            persist_directory=settings.vector_db_path
        )

    def add_documents(self, documents: List[Document]):
        """Add documents to vector store."""
        return self.vectorstore.add_documents(documents)

    def search(self, query: str, k: int = None):
        """Search for similar documents."""
        k = k or settings.top_k
        return self.vectorstore.similarity_search(query, k=k)

    def delete_collection(self):
        """Delete the collection."""
        self.vectorstore.delete_collection()

    def get_retriever(self, k: int = None):
        """Get retriever for use in chains."""
        k = k or settings.top_k
        return self.vectorstore.as_retriever(search_kwargs={"k": k})
```

### Step 10: Create Document Chunker (30 min)

**File:** `src/data/processors/__init__.py` (empty)

**File:** `src/data/processors/chunker.py`
```python
from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import settings

class DocumentChunker:
    """Chunk documents into smaller pieces."""

    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks."""
        return self.splitter.split_documents(documents)
```

### Step 11: Create Generator (30 min)

**File:** `src/core/generator.py`
```python
from langchain_ollama import OllamaLLM
from config.settings import settings

class Generator:
    """Handle LLM generation."""

    def __init__(self, model: str = None):
        self.model = model or settings.llm_model
        self.llm = OllamaLLM(
            model=self.model,
            base_url=settings.llm_base_url
        )

    def generate(self, prompt: str) -> str:
        """Generate response."""
        return self.llm.invoke(prompt)
```

### Step 12: Create RAG Engine (1 hour)

**File:** `src/core/rag_engine.py`
```python
from typing import List, Dict
from src.data.loaders.base import BaseLoader
from src.data.processors.chunker import DocumentChunker
from src.data.vectorstore import VectorStoreManager
from src.core.generator import Generator

class RAGEngine:
    """Main RAG orchestration engine."""

    def __init__(self, collection_name: str = "default"):
        self.collection_name = collection_name
        self.vectorstore_manager = VectorStoreManager(collection_name)
        self.chunker = DocumentChunker()
        self.generator = Generator()

        self.prompt_template = """Based on the following context, answer the question.

Context:
{context}

Question: {question}

Answer:"""

    def ingest(self, loader: BaseLoader) -> int:
        """Ingest documents from a loader."""
        documents = loader.load()
        documents = self.chunker.chunk_documents(documents)
        self.vectorstore_manager.add_documents(documents)
        return len(documents)

    def query(self, question: str) -> Dict:
        """Query the RAG system."""
        # Retrieve relevant documents
        docs = self.vectorstore_manager.search(question)

        # Format context
        context = "\n\n".join([doc.page_content for doc in docs])

        # Generate response
        prompt = self.prompt_template.format(context=context, question=question)
        answer = self.generator.generate(prompt)

        return {
            "answer": answer,
            "sources": docs,
            "num_sources": len(docs)
        }
```

---

## Day 3: Additional Loaders & Integration (3-4 hours)

### Step 13: Create CSV Loader (30 min)

**File:** `src/data/loaders/csv_loader.py`
```python
import pandas as pd
from pathlib import Path
from typing import List
from langchain.schema import Document
from .base import BaseLoader

class CSVLoader(BaseLoader):
    """Load documents from CSV files."""

    def __init__(self, file_path: str, content_columns: List[str] = None):
        super().__init__(file_path)
        self.file_path = Path(file_path)
        self.content_columns = content_columns

    def validate_source(self) -> bool:
        return self.file_path.exists()

    def load(self) -> List[Document]:
        if not self.validate_source():
            raise FileNotFoundError(f"CSV not found: {self.file_path}")

        df = pd.read_csv(self.file_path)
        documents = []

        for idx, row in df.iterrows():
            # Combine all columns or specified columns
            if self.content_columns:
                content = "\n".join([f"{col}: {row[col]}" for col in self.content_columns if col in row])
            else:
                content = "\n".join([f"{col}: {val}" for col, val in row.items()])

            metadata = {
                "source": str(self.file_path),
                "file_name": self.file_path.name,
                "file_type": "csv",
                "row": idx
            }

            documents.append(self._create_document(content, metadata))

        return documents
```

### Step 14: Create Excel Loader (30 min)

**File:** `src/data/loaders/excel_loader.py`
```python
import pandas as pd
from pathlib import Path
from typing import List
from langchain.schema import Document
from .base import BaseLoader

class ExcelLoader(BaseLoader):
    """Load documents from Excel files."""

    def __init__(self, file_path: str, sheet_name: str = 0):
        super().__init__(file_path)
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name

    def validate_source(self) -> bool:
        return self.file_path.exists()

    def load(self) -> List[Document]:
        if not self.validate_source():
            raise FileNotFoundError(f"Excel file not found: {self.file_path}")

        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        documents = []

        for idx, row in df.iterrows():
            content = "\n".join([f"{col}: {val}" for col, val in row.items()])

            metadata = {
                "source": str(self.file_path),
                "file_name": self.file_path.name,
                "file_type": "excel",
                "sheet": str(self.sheet_name),
                "row": idx
            }

            documents.append(self._create_document(content, metadata))

        return documents
```

### Step 15: Create Word Document Loader (45 min)

**File:** `src/data/loaders/docx_loader.py`
```python
from pathlib import Path
from typing import List
from langchain.schema import Document
from .base import BaseLoader
from docx import Document as DocxDocument

class DOCXLoader(BaseLoader):
    """Load documents from Word files (.docx)."""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.file_path = Path(file_path)

    def validate_source(self) -> bool:
        return self.file_path.exists()

    def load(self) -> List[Document]:
        if not self.validate_source():
            raise FileNotFoundError(f"Word document not found: {self.file_path}")

        doc = DocxDocument(self.file_path)

        # Extract all paragraphs
        content = "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])

        metadata = {
            "source": str(self.file_path),
            "file_name": self.file_path.name,
            "file_type": "docx",
            "paragraphs": len(doc.paragraphs)
        }

        return [self._create_document(content, metadata)]
```

### Step 16: Create JSON Loader (30 min)

**File:** `src/data/loaders/json_loader.py`
```python
import json
from pathlib import Path
from typing import List
from langchain.schema import Document
from .base import BaseLoader

class JSONLoader(BaseLoader):
    """Load documents from JSON files."""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.file_path = Path(file_path)

    def validate_source(self) -> bool:
        return self.file_path.exists()

    def load(self) -> List[Document]:
        if not self.validate_source():
            raise FileNotFoundError(f"JSON not found: {self.file_path}")

        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Convert JSON to readable text
        content = json.dumps(data, indent=2)

        metadata = {
            "source": str(self.file_path),
            "file_name": self.file_path.name,
            "file_type": "json"
        }

        return [self._create_document(content, metadata)]
```

### Step 17: Create Loader Factory (15 min)

**Update:** `src/data/loaders/__init__.py`
```python
from .base import BaseLoader
from .text_loader import TextLoader
from .pdf_loader import PDFLoader
from .csv_loader import CSVLoader
from .excel_loader import ExcelLoader
from .docx_loader import DOCXLoader
from .json_loader import JSONLoader

LOADERS = {
    'text': TextLoader,
    'pdf': PDFLoader,
    'csv': CSVLoader,
    'excel': ExcelLoader,
    'docx': DOCXLoader,
    'json': JSONLoader,
}

def get_loader(file_type: str):
    """Get loader class by file type."""
    return LOADERS.get(file_type)
```

---

## Day 4: Streamlit Frontend (Already Created!)

The `app.py` file is already created! Just run it:

```bash
streamlit run app.py
```

---

## Day 5: Testing & Refinement

### Test the Complete System

#### Test 1: Upload Text File
```bash
# Create test file
echo "This is a test document about Python programming." > test.txt

# Run app
streamlit run app.py

# Upload test.txt
# Ask: "What is this document about?"
```

#### Test 2: Upload PDF
```bash
# Use any PDF file
# Upload via Streamlit
# Ask questions about it
```

#### Test 3: Multiple Files
```bash
# Upload multiple files of different types
# Ask cross-document questions
```

---

## Verification Checklist

After Day 5, verify:

- [ ] ✅ Can upload TXT files
- [ ] ✅ Can upload PDF files
- [ ] ✅ Can upload CSV files
- [ ] ✅ Can upload Excel files
- [ ] ✅ Can upload Word documents
- [ ] ✅ Can upload JSON files
- [ ] ✅ Documents are processed and embedded
- [ ] ✅ Can ask questions via chat
- [ ] ✅ Get relevant answers
- [ ] ✅ See source citations
- [ ] ✅ Can clear documents
- [ ] ✅ Can use different collections

---

## Quick Command Reference

```bash
# Run Streamlit app
streamlit run app.py

# Test imports
python -c "from src.core.rag_engine import RAGEngine; print('✓ RAG Engine OK')"

# Test loader
python -c "from src.data.loaders import get_loader; print('✓ Loaders OK')"

# Check vector store
python -c "from src.data.vectorstore import VectorStoreManager; print('✓ Vector Store OK')"
```

---

## Troubleshooting

### Error: "No module named 'src'"
```bash
# Make sure you're in the project root directory
# Create __init__.py files
touch src/__init__.py
touch src/core/__init__.py
touch src/data/__init__.py
```

### Error: "Ollama connection refused"
```bash
# Make sure Ollama is running
ollama serve

# In another terminal, pull the model
ollama pull llama3.2
ollama pull mxbai-embed-large
```

### Error: "ChromaDB permission denied"
```bash
# Create data directory
mkdir -p data/vectorstore
chmod -R 755 data/
```

---

## Next Steps

Once basic system works:
1. Add file preview
2. Add download Q&A as PDF
3. Add user authentication
4. Deploy to cloud (Streamlit Cloud)

**You now have a fully functional Document Q&A system!** 🎉
