# Architecture & Modularity Guide

> **📖 Context:** This guide explains the modular design of the Document Q&A system and shows how to extend it with new features.

**Yes, this is a fully modular architecture!** You can add new components without modifying existing code.

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [Quick Reference Checklists](#quick-reference-checklists)
3. [Detailed Examples](#detailed-examples)
4. [Design Patterns](#design-patterns)
5. [Testing Modularity](#testing-modularity)

---

# Core Principles

## Plugin Architecture

The system uses **abstract base classes** and **factory patterns** for plug-and-play modules.

```
┌─────────────────────────────────────────────────────────────┐
│         Add New Module = Create One File                    │
│                                                              │
│  No need to modify existing code!                          │
│  Just inherit from base class and register                 │
└─────────────────────────────────────────────────────────────┘
```

---

# Quick Reference Checklists

## ☐ Adding a New Data Loader (e.g., Excel)

### Step 1: Create loader file (15 min)
```bash
touch src/data/loaders/excel_loader.py
```

### Step 2: Inherit from BaseLoader
```python
from .base import BaseLoader

class ExcelLoader(BaseLoader):
    def validate_source(self) -> bool:
        # Check file exists
        pass

    def load(self) -> List[Document]:
        # Load Excel and return Documents
        pass
```

### Step 3: Register (1 line!)
```python
# In src/data/loaders/__init__.py
from .excel_loader import ExcelLoader

LOADERS = {
    'excel': ExcelLoader,  # ← Add this line
}
```

### Step 4: Use it immediately!
```python
loader = ExcelLoader("data.xlsx")
engine.ingest(loader)
```

**✅ Done! No other code changes needed.**

---

## ☐ Adding a New LLM Provider (e.g., OpenAI)

### Step 1: Add import
```python
# In src/core/generator.py
from langchain_openai import ChatOpenAI  # ← Add this
```

### Step 2: Add elif clause
```python
def _initialize_llm(self):
    if settings.llm_provider == "ollama":
        return OllamaLLM(...)
    elif settings.llm_provider == "openai":  # ← Add this
        return ChatOpenAI(...)
```

### Step 3: Update .env
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
OPENAI_API_KEY=sk-...
```

**✅ Done! Entire system now uses OpenAI.**

---

## ☐ Adding a New Agent (e.g., Legal Agent)

### Step 1: Create agent file
```bash
touch src/agents/legal_agent.py
```

### Step 2: Inherit from BaseAgent
```python
from .base_agent import BaseAgent

class LegalAgent(BaseAgent):
    def __init__(self):
        super().__init__(collection_name="legal_docs")
        self.prompt_template = "You are a legal expert..."
```

### Step 3: Use it!
```python
from src.agents import LegalAgent

agent = LegalAgent()
answer = agent.query("Explain this clause")
```

**✅ Done! No modifications to existing agents.**

---

## ☐ Adding a New CLI Command

### Step 1: Add command handler in cli.py
```python
class CLI:
    def run(self):
        if user_input == 'stats':  # ← New command
            self.show_stats()

    def show_stats(self):  # ← New method
        print("Collection stats...")
```

**✅ Done! Command available immediately.**

---

## ☐ Adding a New API Endpoint

### Step 1: Add endpoint in api.py
```python
@app.get("/api/v1/stats")  # ← New endpoint
def get_stats():
    return {"collections": 5, "docs": 1000}
```

**✅ Done! Endpoint live immediately.**

---

# Detailed Examples

## 1. Adding New Data Loaders (Most Common)

### How It Works

```python
# Base interface (already exists)
class BaseLoader(ABC):
    @abstractmethod
    def load(self) -> List[Document]:
        pass
```

### Example: Add Excel Loader (New Module)

**Complete Implementation:**

```python
# src/data/loaders/excel_loader.py
import pandas as pd
from typing import List
from langchain.schema import Document
from .base import BaseLoader

class ExcelLoader(BaseLoader):
    """Load documents from Excel files."""

    def __init__(self, file_path: str, sheet_name: str = 0, content_column: str = "content"):
        super().__init__(file_path)
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.content_column = content_column

    def validate_source(self) -> bool:
        return Path(file_path).exists()

    def load(self) -> List[Document]:
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        documents = []

        for idx, row in df.iterrows():
            content = str(row[self.content_column])
            metadata = {"source": self.file_path, "row": idx}
            documents.append(self._create_document(content, metadata))

        return documents
```

### ✅ What You Didn't Need to Modify:
- RAG Engine
- Vector Store
- CLI
- API
- Any existing loaders

**Zero existing code changes!**

---

## 2. Adding New Embedding Models

### Example: Add OpenAI Embeddings

**Update `src/core/embeddings.py`:**

```python
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings  # New import
from config.settings import settings

class EmbeddingManager:
    def _initialize_embeddings(self):
        if settings.embedding_provider == "ollama":
            return OllamaEmbeddings(
                model=settings.embedding_model,
                base_url=settings.llm_base_url
            )
        elif settings.embedding_provider == "openai":  # ← Add this
            return OpenAIEmbeddings(
                model=settings.embedding_model,
                openai_api_key=settings.openai_api_key
            )
        else:
            raise ValueError(f"Unsupported: {settings.embedding_provider}")
```

**Update `.env`:**
```env
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
OPENAI_API_KEY=sk-...
```

**Done!** Everything else automatically uses the new embeddings.

---

## 3. Adding New LLM Providers

### Example: Add Anthropic Claude

**Update `src/core/generator.py`:**

```python
from langchain_ollama import OllamaLLM
from langchain_anthropic import ChatAnthropic  # New import
from config.settings import settings

class Generator:
    def _initialize_llm(self):
        if settings.llm_provider == "ollama":
            return OllamaLLM(
                model=self.model,
                base_url=settings.llm_base_url
            )
        elif settings.llm_provider == "anthropic":  # ← Add this
            return ChatAnthropic(
                model=self.model,
                api_key=settings.anthropic_api_key,
                temperature=self.temperature
            )
        else:
            raise ValueError(f"Unsupported: {settings.llm_provider}")
```

**Update `.env`:**
```env
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_API_KEY=sk-ant-...
```

**Done!** Entire system now uses Claude.

---

## 4. Adding New Retrieval Strategies

### Example: Add Hybrid Search (Semantic + Keyword)

**Create `src/core/hybrid_retriever.py`:**

```python
from typing import List
from langchain.schema import Document
from src.data.vectorstore import VectorStoreManager

class HybridRetriever:
    """Combine semantic and keyword search."""

    def __init__(self, collection_name: str = "default", k: int = 5):
        self.vectorstore_manager = VectorStoreManager(collection_name)
        self.k = k

    def retrieve(self, query: str, k: int = None) -> List[Document]:
        k = k or self.k

        # Semantic search
        semantic_docs = self.vectorstore_manager.search(query, k=k)

        # Keyword search (BM25)
        # ... implement keyword search logic

        # Combine and re-rank
        combined = self._merge_results(semantic_docs, keyword_docs)
        return combined[:k]

    def _merge_results(self, semantic, keyword):
        # Implement merging logic
        pass
```

**Use in RAG Engine:**

```python
from src.core.hybrid_retriever import HybridRetriever

engine = RAGEngine()
engine.retriever = HybridRetriever(collection_name="docs", k=5)
# Now uses hybrid search!
```

---

# Design Patterns

## Key Principle: Interface, Not Implementation

```python
# Interface (abstract)
class BaseLoader(ABC):
    @abstractmethod
    def load(self): pass

# Implementation 1
class CSVLoader(BaseLoader):
    def load(self): ...  # CSV-specific

# Implementation 2
class PDFLoader(BaseLoader):
    def load(self): ...  # PDF-specific

# RAG Engine doesn't care which!
engine.ingest(loader)  # ← Works with ANY loader!
```

**The RAG engine works with the interface, not specific implementations.**

---

## What Makes This Modular?

### ✅ 1. Abstract Base Classes
Every extensible component has a base class:
- `BaseLoader` for data loaders
- `BaseAgent` for agents
- Common interface = easy to extend

### ✅ 2. Factory Pattern
```python
loader = get_loader('csv')  # Returns CSVLoader
loader = get_loader('pdf')  # Returns PDFLoader
```
Create objects without knowing the exact class.

### ✅ 3. Dependency Injection
```python
# Can swap components
engine = RAGEngine(
    retriever=HybridRetriever(),  # Custom retriever
    generator=ClaudeGenerator()   # Custom generator
)
```

### ✅ 4. Configuration-Driven
```env
# Change behavior without code changes
LLM_PROVIDER=openai  # Was: ollama
VECTOR_DB=pinecone   # Was: chroma
```

### ✅ 5. Single Responsibility
Each module does ONE thing:
- Loaders: Load data
- Chunker: Chunk text
- Retriever: Retrieve docs
- Generator: Generate text
- Easy to add/modify/test independently

---

## Real-World Example: Adding 3 New Data Sources

**Scenario:** Add support for Excel, XML, and databases

### Traditional Approach (Non-Modular):
```
1. Modify core engine ❌
2. Update existing loaders ❌
3. Change CLI ❌
4. Update API ❌
5. Modify tests ❌
Total: Modify 10+ files, risk breaking existing code
```

### Modular Approach (This Architecture):
```
1. Create excel_loader.py ✅
2. Create xml_loader.py ✅
3. Create db_loader.py ✅
4. Add 3 lines to __init__.py ✅
Total: 3 new files, 3 lines changed, zero risk
```

---

## Module Compatibility Matrix

| Module Type | Works With All | Config Only | Code Change |
|-------------|----------------|-------------|-------------|
| Data Loader | ✅ | ❌ | New file |
| LLM Provider | ✅ | ✅ | 1 elif |
| Embedding Model | ✅ | ✅ | 1 elif |
| Vector DB | ✅ | ✅ | 1 elif |
| Agent | ✅ | ❌ | New file |
| Prompt | ✅ | ✅ | New text file |
| CLI Command | ✅ | ❌ | New method |
| API Endpoint | ✅ | ❌ | New function |

**Legend:**
- ✅ Works With All: Module works with all other modules
- ✅ Config Only: Can switch via .env, no code change
- New file: Create one new file, no existing code changes

---

# Testing Modularity

## The "One File" Test

**Rule:** Adding a feature should require creating/modifying **as few files as possible**.

### Examples:

**Add Excel Support:**
- Create: `excel_loader.py` (1 file)
- Modify: `__init__.py` (1 line)
- **Total: 1 new file, 1 line changed** ✅

**Switch to OpenAI:**
- Modify: `.env` (2 lines)
- **Total: 0 new files, 2 lines changed** ✅

**Add Legal Agent:**
- Create: `legal_agent.py` (1 file)
- **Total: 1 new file, 0 lines changed** ✅

**Add API Endpoint:**
- Modify: `api.py` (1 function)
- **Total: 0 new files, 5 lines changed** ✅

---

## Anti-Patterns to Avoid (Not Modular)

### ❌ Don't: Hardcode in RAG Engine
```python
# BAD - Hardcoded!
class RAGEngine:
    def __init__(self):
        if self.use_csv:
            loader = CSVLoader()
        elif self.use_pdf:
            loader = PDFLoader()
```

### ✅ Do: Accept Interface
```python
# GOOD - Modular!
class RAGEngine:
    def ingest(self, loader: BaseLoader):
        docs = loader.load()  # Works with ANY loader!
```

### ❌ Don't: Direct Imports in Core
```python
# BAD - Tight coupling!
from src.data.loaders.csv_loader import CSVLoader

class RAGEngine:
    def __init__(self):
        self.loader = CSVLoader()  # Fixed to CSV!
```

### ✅ Do: Factory Pattern
```python
# GOOD - Loose coupling!
from src.data.loaders import get_loader

loader = get_loader('csv')  # Can be any type!
engine.ingest(loader)
```

---

## Quick Decision Tree: Where to Add?

```
What are you adding?
│
├─ New data format (Excel, XML, etc.)?
│  └─ Create: src/data/loaders/X_loader.py
│
├─ New LLM provider (OpenAI, Anthropic)?
│  └─ Modify: src/core/generator.py (add elif)
│
├─ New embedding model?
│  └─ Modify: src/core/embeddings.py (add elif)
│
├─ New vector database?
│  └─ Modify: src/data/vectorstore.py (add elif)
│
├─ New retrieval strategy?
│  └─ Create: src/core/X_retriever.py
│
├─ New agent type?
│  └─ Create: src/agents/X_agent.py
│
├─ New CLI command?
│  └─ Modify: src/interfaces/cli.py (add method)
│
├─ New API endpoint?
│  └─ Modify: src/interfaces/api.py (add function)
│
└─ New prompt template?
   └─ Create: config/prompts/X.txt
```

---

# Summary: Modularity Guarantee

## ✅ This Architecture Guarantees:

1. **Add new data source** → 1 new file, 1 line registration
2. **Switch LLM/embeddings/vector DB** → Change .env only
3. **Add new agent** → 1 new file, 0 changes to existing code
4. **Add new endpoint** → 1 function, 0 changes to core
5. **Change prompts** → Edit text file, 0 code changes

## ✅ You Will NEVER Need To:

- ❌ Modify RAG engine core for new data sources
- ❌ Change existing loaders to add new ones
- ❌ Update CLI to add new data formats
- ❌ Modify vector store for new retrieval strategies
- ❌ Touch configuration system for new modules

## ✅ "Plug and Play" Means:

```python
# Day 1: Use CSV
loader = CSVLoader("data.csv")
engine.ingest(loader)

# Day 2: Add Excel support (15 min work)
# Create excel_loader.py

# Day 2: Use Excel (same code!)
loader = ExcelLoader("data.xlsx")
engine.ingest(loader)  # ← Same line!
```

**The interface stays the same, implementations are swappable.**

---

## Quick Reference Table: Adding Common Modules

| Want to Add | Create File | Inherit From | Register In |
|-------------|-------------|--------------|-------------|
| Data loader | `src/data/loaders/X_loader.py` | `BaseLoader` | `loaders/__init__.py` |
| Agent | `src/agents/X_agent.py` | `BaseAgent` | N/A (import directly) |
| CLI command | N/A | N/A | `cli.py` (add method) |
| API endpoint | N/A | N/A | `api.py` (add function) |
| LLM provider | N/A | N/A | `generator.py` (add elif) |
| Vector DB | N/A | N/A | `vectorstore.py` (add elif) |
| Prompt template | `config/prompts/X.txt` | N/A | N/A (just load file) |

**Average time to add module: 15-30 minutes**

---

## Next Steps

1. **Understand the pattern** → Read this guide
2. **Follow the guide** → Build from `STREAMLIT_QUICK_START.md`
3. **Test modularity** → Add your first custom loader
4. **Extend freely** → Add any module you need!

**Yes, this is truly modular!** Each component is independent, testable, and swappable. 🎉

---

## 💡 Pro Tips

1. **New to modularity?** Start by adding a simple data loader
2. **Want to experiment?** Try swapping LLM providers via .env
3. **Building features?** Always inherit from base classes
4. **Stuck?** Check if you're modifying existing code (you probably shouldn't be!)
5. **Testing?** Each module should work independently

---

**This is true modular architecture!** 🎉
