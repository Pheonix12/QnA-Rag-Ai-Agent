# Alternative Implementation Approaches

> **⚠️ For Document Q&A System:** For the recommended Streamlit-based Document Q&A implementation, see **[STREAMLIT_QUICK_START.md](STREAMLIT_QUICK_START.md)** (3-5 days, web UI, easier).

This guide provides two alternative approaches for building RAG systems:
1. **CLI-Based Approach** - Command-line interface (no web UI)
2. **General 5-Phase Approach** - Comprehensive RAG system with all features

---

## Which Approach Should You Use?

```
Want to build Document Q&A web app? → Use STREAMLIT_QUICK_START.md (Recommended)
Want command-line only? → Use Part 1 below (CLI Approach)
Want full-featured RAG platform? → Use Part 2 below (5-Phase Approach)
```

---

# PART 1: CLI-Based Implementation

> **Timeline:** 5 days | **Output:** Command-line RAG system | **UI:** Terminal only

This is a daily checklist for building a CLI-based RAG system. Simpler than the 5-phase approach, but no web interface.

## Overview

**What you'll build:**
- Command-line interface for querying
- Document ingestion via scripts
- Local vector storage
- Ollama-based LLM

**Not included:**
- Web UI (use Streamlit approach for this)
- REST API (use 5-phase approach for this)
- Advanced features (use 5-phase approach for this)

---

## Phase 1: Foundation (Week 1)

### DAY 1: Configuration & Data Loading

#### Morning Session (2-3 hours)

**Step 1: Create `.env.example`** (15 min)
```bash
touch .env.example
```

```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2
LLM_BASE_URL=http://localhost:11434

EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=mxbai-embed-large

VECTOR_DB=chroma
VECTOR_DB_PATH=./data/vectorstore

LOG_LEVEL=INFO
MAX_CONTEXT_LENGTH=4096
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=5
```

```bash
cp .env.example .env
```

---

**Step 2: Create `config/settings.py`** (30 min)

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
    max_context_length: int = 4096
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
```

---

**Step 3: Create `src/data/loaders/base.py`** (45 min)

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain.schema import Document

class BaseLoader(ABC):
    """Abstract base class for all data loaders."""

    def __init__(self, source: str, **kwargs):
        self.source = source
        self.kwargs = kwargs

    @abstractmethod
    def load(self) -> List[Document]:
        """Load documents from source."""
        pass

    @abstractmethod
    def validate_source(self) -> bool:
        """Validate that source exists and is accessible."""
        pass

    def _create_document(self, content: str, metadata: Dict[str, Any]) -> Document:
        """Helper to create Document objects."""
        return Document(page_content=content, metadata=metadata)
```

---

#### Afternoon Session (2-3 hours)

**Step 4: Create `src/data/loaders/csv_loader.py`** (30 min)

See the full implementation in the document for CSV loading with pandas.

**Step 5: Create `src/data/processors/chunker.py`** (1 hour)

Implement text chunking using LangChain's RecursiveCharacterTextSplitter.

---

### DAY 2: Vector Store & Core Components

**Step 6: Create `src/core/embeddings.py`** (30 min)
**Step 7: Create `src/data/vectorstore.py`** (1.5 hours)
**Step 8: Create `src/core/retriever.py`** (1 hour)
**Step 9: Create `src/core/generator.py`** (1 hour)

---

### DAY 3: RAG Engine

**Step 10: Create `src/core/rag_engine.py`** (2 hours)

Main orchestration that combines retriever + generator + chunker.

---

### DAY 4: CLI Interface

**Step 11: Create `src/utils/logger.py`** (30 min)
**Step 12: Create `src/interfaces/cli.py`** (2 hours)

Interactive command-line interface with commands:
- Query mode
- Exit/quit
- Error handling

---

### DAY 5: Scripts & Examples

**Step 13: Create `scripts/ingest_data.py`** (1 hour)
**Step 14: Create `examples/restaurant_qa.py`** (30 min)
**Step 15: Update `requirements.txt`** (15 min)

---

## Verification Checklist

After completing Phase 1, verify:

```bash
# 1. Settings load correctly
python -c "from config.settings import settings; print(settings.llm_model)"

# 2. CSV loader works
python -c "from src.data.loaders.csv_loader import CSVLoader; ..."

# 3. Vector store works
python -c "from src.data.vectorstore import VectorStoreManager; ..."

# 4. RAG engine works end-to-end
python examples/restaurant_qa.py
```

---

## What You've Achieved

✓ Clean, modular architecture
✓ Configuration management
✓ Pluggable data loaders
✓ Centralized vector store management
✓ Proper RAG orchestration
✓ Working CLI
✓ Data ingestion scripts
✓ Foundation for adding features

---

# PART 2: General 5-Phase Development Plan

> **Timeline:** 4-6 weeks | **Output:** Enterprise RAG platform | **Complexity:** High

This is a comprehensive plan for building a full-featured, production-ready RAG system with all components.

## Development Philosophy

**Incremental Development**: Build the foundation first, ensure it works, then add features layer by layer. Each phase produces a working application.

---

## Phase 0: Setup & Preparation (30 minutes)

```bash
# Create all directories
mkdir -p config/prompts
mkdir -p src/{core,data/loaders,data/processors,interfaces,utils,agents}
mkdir -p data/{raw,processed,vectorstore}
mkdir -p tests scripts examples docs
```

**File Order:**
1. `.env.example` - Environment template
2. `config/settings.py` - Global settings
3. `requirements.txt` - Dependencies

---

## Phase 1: Core Foundation (Week 1)

**Goal**: Extract and modularize code into clean foundation

### Day 1: Configuration & Settings

#### Files to Create:
1. `.env.example` (15 min)
2. `config/settings.py` (30 min)

### Day 2: Data Layer Foundation

#### Files to Create:
1. `src/data/loaders/base.py` (45 min) - Abstract base class
2. `src/data/loaders/csv_loader.py` (30 min) - CSV support
3. `src/data/processors/chunker.py` (1 hour) - Text chunking
4. `src/data/vectorstore.py` (1 hour) - Vector DB management

### Day 3: Core RAG Engine

#### Files to Create:
1. `src/core/embeddings.py` (30 min) - Embedding management
2. `src/core/retriever.py` (1 hour) - Document retrieval
3. `src/core/generator.py` (1 hour) - LLM generation
4. `src/core/rag_engine.py` (1.5 hours) - Main orchestration

### Day 4-5: Interface Layer

#### Files to Create:
1. `src/interfaces/cli.py` (1 hour) - CLI interface
2. `src/utils/logger.py` (30 min) - Logging
3. `scripts/ingest_data.py` (45 min) - Data ingestion

### Day 5: Integration & Testing

#### Files to Create:
1. `examples/restaurant_qa.py` (30 min) - Example use case
2. `tests/test_loaders.py` (1 hour) - Unit tests
3. Update `requirements.txt` (15 min)

---

## Phase 2: Additional Data Sources (Week 2)

**Goal**: Add support for more data types

### Priority Order:

1. **JSON Loader** (45 min) - Common and easy
2. **PDF Loader** (1.5 hours) - Very common for docs
   - Dependency: `pypdf` or `pdfplumber`
3. **Text Loader** (30 min) - .txt, .md files
4. **Web Loader** (2 hours) - Web scraping
   - Dependency: `beautifulsoup4`, `requests`
5. **Loader Factory** (15 min) - Easy access to all loaders

**Factory Pattern:**
```python
from .csv_loader import CSVLoader
from .pdf_loader import PDFLoader
from .json_loader import JSONLoader

LOADERS = {
    'csv': CSVLoader,
    'pdf': PDFLoader,
    'json': JSONLoader,
}

def get_loader(file_type: str):
    return LOADERS.get(file_type)
```

---

## Phase 3: REST API (Week 3)

**Goal**: Add HTTP API for remote access

### Files to Create:

1. **`src/interfaces/api.py`** (2 hours)
   - FastAPI application
   - Endpoints: POST /query, POST /ingest, GET /health
   - Pydantic models

2. **`src/interfaces/websocket.py`** (2 hours)
   - WebSocket for streaming
   - Real-time responses

---

## Phase 4: Advanced Features (Week 4)

**Goal**: Add production-ready features

### Priority Order:

1. **`src/utils/cache.py`** (1.5 hours)
   - Query result caching with TTL
   - Redis or in-memory

2. **`src/agents/base_agent.py`** (1 hour)
   - Base agent class with memory

3. **`src/agents/qa_agent.py`** (45 min)
   - Specialized Q&A agent

4. **`src/agents/chat_agent.py`** (1.5 hours)
   - Conversational agent with history

5. **`config/prompts/`** templates (30 min)
   - Reusable prompt templates

---

## Phase 5: Production Features (Week 5+)

1. **Monitoring** - Track latency, token usage, errors
2. **Authentication** - API keys, user sessions
3. **Multi-tenancy** - Multiple knowledge bases
4. **Docker** - Containerization
5. **CI/CD** - Automated deployment

---

## Quick Start Migration Path

### Minimal Path (2-3 days):

1. **Day 1 Morning:** Settings + Base Loader + CSV Loader
2. **Day 1 Afternoon:** VectorStore + Embeddings
3. **Day 2 Morning:** Retriever + Generator + RAG Engine
4. **Day 2 Afternoon:** New CLI using RAG Engine
5. **Day 3:** Ingest script + Testing

This gives you working refactored app with same functionality but better structure.

---

## Implementation Checklist

### Phase 1: Core Foundation ✓
- [ ] `.env.example`
- [ ] `config/settings.py`
- [ ] `src/data/loaders/base.py`
- [ ] `src/data/loaders/csv_loader.py`
- [ ] `src/data/processors/chunker.py`
- [ ] `src/data/vectorstore.py`
- [ ] `src/core/embeddings.py`
- [ ] `src/core/retriever.py`
- [ ] `src/core/generator.py`
- [ ] `src/core/rag_engine.py`
- [ ] `src/interfaces/cli.py`
- [ ] `src/utils/logger.py`
- [ ] `scripts/ingest_data.py`
- [ ] `examples/restaurant_qa.py`
- [ ] `tests/test_loaders.py`
- [ ] Update `requirements.txt`

### Phase 2: Additional Loaders ✓
- [ ] JSON, PDF, Text, Web loaders
- [ ] Loader factory pattern

### Phase 3: API ✓
- [ ] FastAPI REST API
- [ ] WebSocket streaming

### Phase 4: Advanced Features ✓
- [ ] Caching layer
- [ ] Agent framework
- [ ] Prompt templates

### Phase 5: Production ✓
- [ ] Monitoring & metrics
- [ ] Authentication
- [ ] Multi-tenancy
- [ ] Docker & CI/CD

---

## Development Tips

### 1. Test After Each File
Don't move to next file until current one works:
```bash
# Create → Implement → Test → Move on
python -c "from src.data.loaders.csv_loader import CSVLoader; print('Works!')"
pytest tests/test_loaders.py::test_csv_loader
```

### 2. Keep Current Code Working
- Don't delete `main.py` and `vector.py` yet
- Keep them until Phase 1 complete
- Use as reference
- Delete when `examples/restaurant_qa.py` works

### 3. Use Branches
```bash
git checkout -b phase-1-foundation
git commit -m "Phase 1: Core foundation complete"
git checkout -b phase-2-loaders
```

### 4. Document As You Go
Add docstrings to every class/function

### 5. Start Simple, Add Complexity
- Phase 1: Get it working
- Phase 2: More use cases
- Phase 3: Make it fast
- Phase 4: Make it robust
- Phase 5: Make it scalable

---

## Success Criteria

### Phase 1 Complete When:
- [ ] Can load CSV files with new loader
- [ ] Can create vector store
- [ ] Can query using RAGEngine
- [ ] CLI works with new architecture
- [ ] Original functionality preserved
- [ ] All tests pass

### Phase 2 Complete When:
- [ ] Can load PDF, JSON, TXT files
- [ ] Can ingest multiple file types
- [ ] Loaders are pluggable

### Phase 3 Complete When:
- [ ] API accepts queries via HTTP
- [ ] Can ingest via API
- [ ] WebSocket streams responses

### Phase 4 Complete When:
- [ ] Caching reduces latency
- [ ] Agents provide specialized functionality
- [ ] Conversation history works

### Phase 5 Complete When:
- [ ] Monitoring shows metrics
- [ ] Can deploy to production
- [ ] Multiple users can use simultaneously

---

## Estimated Timeline

| Phase | Time | Deliverable |
|-------|------|-------------|
| Phase 0 | 30 min | Project structure |
| Phase 1 | 5 days | Modular foundation |
| Phase 2 | 3 days | Multi-format support |
| Phase 3 | 3 days | REST API |
| Phase 4 | 5 days | Advanced features |
| Phase 5 | 2 weeks | Production-ready |
| **Total** | **~1 month** | Enterprise RAG system |

**Minimum Viable Product**: Phase 1 (1 week)
**Production Ready**: Phase 1-4 (2-3 weeks)
**Enterprise Grade**: All phases (4-6 weeks)

---

## Comparison: CLI vs 5-Phase vs Streamlit

| Feature | CLI Approach | 5-Phase Approach | Streamlit (Recommended) |
|---------|--------------|------------------|-------------------------|
| **Timeline** | 5 days | 4-6 weeks | 3-5 days |
| **Complexity** | Low | High | Medium |
| **User Interface** | Terminal only | API + Optional UI | Web UI built-in |
| **Data Loaders** | Basic (CSV, PDF) | All formats | Document-focused |
| **API** | No | Yes (Phase 3) | No (but easy to add) |
| **Agents** | No | Yes (Phase 4) | Can add later |
| **Best For** | Quick prototype | Enterprise platform | Document Q&A app |
| **Production Ready** | No | Yes (Phase 5) | Yes (with polish) |

---

## Next Steps

**Choose your path:**

1. **Want working system fast?** → Use [STREAMLIT_QUICK_START.md](STREAMLIT_QUICK_START.md)
2. **Want CLI only?** → Follow Part 1 above
3. **Want enterprise platform?** → Follow Part 2 above

**For most users:** We recommend **STREAMLIT_QUICK_START.md** - it's the perfect balance of features, usability, and development time.

---

## Questions Before Starting

1. **Do you need API immediately?** → 5-Phase approach
2. **Do you need web UI?** → Streamlit approach
3. **Just need command-line?** → CLI approach
4. **What data formats?** → All approaches support main formats
5. **Single or multi-user?** → 5-Phase for multi-user
6. **Local or cloud?** → Any approach works, 5-Phase best for cloud

---

**Still unsure?** Start with [START_HERE.md](START_HERE.md) for guidance!
