# File Dependency Map

> **⚠️ For Document Q&A System:** This is a comprehensive dependency map. For the focused Document Q&A implementation, see **[STREAMLIT_QUICK_START.md](STREAMLIT_QUICK_START.md)** which uses a subset of these files.

This shows which files depend on which others. Always implement files from top to bottom (no dependencies → has dependencies).

## Visual Dependency Tree

```
Level 0 (No Dependencies - Start Here)
├── .env.example
└── requirements.txt

Level 1 (Depends only on Level 0)
├── config/
│   └── settings.py  [depends: .env]

Level 2 (Depends on Level 0-1)
├── src/data/loaders/
│   └── base.py  [depends: langchain]
└── src/utils/
    └── logger.py  [depends: config/settings.py]

Level 3 (Depends on Level 0-2)
├── src/data/loaders/
│   ├── csv_loader.py  [depends: base.py, pandas]
│   ├── json_loader.py  [depends: base.py]
│   ├── pdf_loader.py  [depends: base.py, pypdf]
│   └── text_loader.py  [depends: base.py]
├── src/data/processors/
│   └── chunker.py  [depends: config/settings.py, langchain]
└── src/core/
    └── embeddings.py  [depends: config/settings.py, langchain_ollama]

Level 4 (Depends on Level 0-3)
└── src/data/
    └── vectorstore.py  [depends: embeddings.py, config/settings.py, langchain_chroma]

Level 5 (Depends on Level 0-4)
├── src/core/
│   ├── retriever.py  [depends: vectorstore.py]
│   └── generator.py  [depends: config/settings.py, langchain_ollama]

Level 6 (Depends on Level 0-5)
└── src/core/
    └── rag_engine.py  [depends: retriever.py, generator.py, chunker.py, vectorstore.py, base.py]

Level 7 (Depends on Level 0-6)
├── src/interfaces/
│   ├── cli.py  [depends: rag_engine.py, logger.py]
│   └── api.py  [depends: rag_engine.py, fastapi]
├── src/agents/
│   ├── base_agent.py  [depends: rag_engine.py]
│   ├── qa_agent.py  [depends: base_agent.py]
│   └── chat_agent.py  [depends: base_agent.py]
├── scripts/
│   └── ingest_data.py  [depends: rag_engine.py, csv_loader.py, logger.py]
└── examples/
    └── restaurant_qa.py  [depends: rag_engine.py, csv_loader.py]
```

## Dependency Graph (Detailed)

### Configuration Layer
```
.env.example
    ↓
.env
    ↓
config/settings.py ──┐
                     │
                     ├→ Used by: embeddings.py
                     ├→ Used by: chunker.py
                     ├→ Used by: generator.py
                     ├→ Used by: logger.py
                     └→ Used by: vectorstore.py
```

### Data Layer
```
base.py (Abstract Loader)
    ↓
    ├→ csv_loader.py ──┐
    ├→ pdf_loader.py   │
    ├→ json_loader.py  ├→ Used by: rag_engine.py, ingest_data.py
    ├→ text_loader.py  │
    └→ web_loader.py ──┘

chunker.py ──→ Used by: rag_engine.py

embeddings.py
    ↓
vectorstore.py
    ↓
    ├→ Used by: retriever.py
    └→ Used by: rag_engine.py
```

### Core Layer
```
embeddings.py ──→ vectorstore.py
                        ↓
                  retriever.py ──┐
                                 │
generator.py ─────────────────────┤
                                  │
                                  ↓
                            rag_engine.py
                                  ↓
                    ┌─────────────┼─────────────┐
                    ↓             ↓             ↓
                cli.py        api.py      agents/
```

### Interface Layer
```
rag_engine.py
    ↓
    ├→ cli.py ──→ Run: python src/interfaces/cli.py
    ├→ api.py ──→ Run: uvicorn src.interfaces.api:app
    └→ websocket.py
```

### Script Layer
```
rag_engine.py + csv_loader.py + logger.py
    ↓
ingest_data.py ──→ Run: python scripts/ingest_data.py
```

### Example Layer
```
rag_engine.py + csv_loader.py
    ↓
    ├→ restaurant_qa.py
    ├→ document_qa.py
    └→ code_assistant.py
```

## Implementation Order (Must Follow This Order)

### Phase 1: Foundation
```
Order │ File                              │ Can Test Independently?
──────┼──────────────────────────────────┼────────────────────────
1     │ .env.example                      │ Yes (just view)
2     │ config/settings.py                │ Yes (import and print)
3     │ src/data/loaders/base.py          │ Yes (import)
4     │ src/data/loaders/csv_loader.py    │ Yes (load CSV)
5     │ src/data/processors/chunker.py    │ Yes (chunk text)
6     │ src/core/embeddings.py            │ Yes (embed text)
7     │ src/data/vectorstore.py           │ Yes (add/search)
8     │ src/core/retriever.py             │ Yes (retrieve)
9     │ src/core/generator.py             │ Yes (generate)
10    │ src/core/rag_engine.py            │ Yes (query)
11    │ src/utils/logger.py               │ Yes (log message)
12    │ src/interfaces/cli.py             │ Yes (run CLI)
13    │ scripts/ingest_data.py            │ Yes (ingest data)
14    │ examples/restaurant_qa.py         │ Yes (full example)
```

### Phase 2: Additional Loaders
```
Order │ File                              │ Depends On
──────┼──────────────────────────────────┼────────────────────────
15    │ src/data/loaders/json_loader.py   │ base.py
16    │ src/data/loaders/pdf_loader.py    │ base.py
17    │ src/data/loaders/text_loader.py   │ base.py
18    │ src/data/loaders/web_loader.py    │ base.py
19    │ src/data/loaders/__init__.py      │ All loaders
```

### Phase 3: API Layer
```
Order │ File                              │ Depends On
──────┼──────────────────────────────────┼────────────────────────
20    │ src/interfaces/api.py             │ rag_engine.py
21    │ src/interfaces/websocket.py       │ api.py
```

### Phase 4: Advanced Features
```
Order │ File                              │ Depends On
──────┼──────────────────────────────────┼────────────────────────
22    │ src/utils/cache.py                │ None
23    │ src/agents/base_agent.py          │ rag_engine.py
24    │ src/agents/qa_agent.py            │ base_agent.py
25    │ src/agents/chat_agent.py          │ base_agent.py
26    │ config/prompts/default.txt        │ None
27    │ config/prompts/technical.txt      │ None
```

## Critical Dependency Notes

### ⚠️ Cannot Build Before Dependencies
- **csv_loader.py** needs **base.py** ← Must create base first
- **vectorstore.py** needs **embeddings.py** ← Must create embeddings first
- **rag_engine.py** needs **retriever.py + generator.py** ← Must create both first
- **cli.py** needs **rag_engine.py** ← Must create RAG engine first

### ✅ Can Build Independently (Parallel Development)
- All loaders (csv, pdf, json, text) can be built in parallel (after base.py)
- retriever.py and generator.py can be built in parallel
- Different agents can be built in parallel (after base_agent.py)

### 🔄 Circular Dependency Warnings (Avoid These)
- **DON'T** import rag_engine in base_loader
- **DON'T** import vectorstore in embeddings
- **DON'T** import retriever in generator

## Testing Dependencies

Each file needs these imports to test:

### Level 1-2 (Foundation)
```python
# config/settings.py
from pydantic_settings import BaseSettings

# src/data/loaders/base.py
from abc import ABC, abstractmethod
from langchain.schema import Document
```

### Level 3 (Loaders & Processors)
```python
# csv_loader.py
from src.data.loaders.base import BaseLoader
import pandas as pd

# chunker.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import settings
```

### Level 4 (Embeddings & Vector Store)
```python
# embeddings.py
from langchain_ollama import OllamaEmbeddings
from config.settings import settings

# vectorstore.py
from langchain_chroma import Chroma
from src.core.embeddings import EmbeddingManager
```

### Level 5 (Core Components)
```python
# retriever.py
from src.data.vectorstore import VectorStoreManager

# generator.py
from langchain_ollama import OllamaLLM
```

### Level 6 (RAG Engine)
```python
# rag_engine.py
from src.core.retriever import Retriever
from src.core.generator import Generator
from src.data.processors.chunker import DocumentChunker
```

### Level 7 (Interfaces & Scripts)
```python
# cli.py
from src.core.rag_engine import RAGEngine

# ingest_data.py
from src.core.rag_engine import RAGEngine
from src.data.loaders.csv_loader import CSVLoader
```

## Quick Reference: "What Can I Build Now?"

### After Completing File #1-2 (settings.py)
✅ Can test: Configuration loading
❌ Cannot build: Anything else

### After Completing File #1-4 (base.py, csv_loader.py)
✅ Can test: CSV loading
✅ Can build: json_loader, pdf_loader, text_loader (in parallel)
❌ Cannot build: Anything using vector store

### After Completing File #1-7 (vectorstore.py)
✅ Can test: Document storage and search
✅ Can build: retriever.py, generator.py (in parallel)
❌ Cannot build: RAG engine yet

### After Completing File #1-10 (rag_engine.py)
✅ Can test: Full RAG queries
✅ Can build: CLI, API, scripts, examples, agents (in parallel)
❌ Nothing blocked anymore!

## Development Workflow Example

### Day 1 Path:
```
1. Create .env.example (15 min)
   ├─ Test: View file
   └─ Status: ✓ Ready for next

2. Create config/settings.py (30 min)
   ├─ Test: python -c "from config.settings import settings; print(settings.llm_model)"
   └─ Status: ✓ Ready for next

3. Create src/data/loaders/base.py (45 min)
   ├─ Test: python -c "from src.data.loaders.base import BaseLoader"
   └─ Status: ✓ Ready for next

4. Create src/data/loaders/csv_loader.py (30 min)
   ├─ Test: Load realistic_restaurant_reviews.csv
   └─ Status: ✓ Ready for next

✓ Day 1 Complete: Can load data from CSV
```

### Day 2 Path:
```
5. Create src/data/processors/chunker.py (1 hour)
   ├─ Test: Chunk sample text
   └─ Status: ✓ Ready for next

6. Create src/core/embeddings.py (30 min)
   ├─ Test: Embed sample text
   └─ Status: ✓ Ready for next

7. Create src/data/vectorstore.py (1.5 hours)
   ├─ Test: Add docs and search
   └─ Status: ✓ Ready for next

✓ Day 2 Complete: Can store and retrieve vectors
```

### Day 3 Path:
```
8-9. Create retriever.py + generator.py (2 hours - parallel!)
   ├─ Test both independently
   └─ Status: ✓ Ready for next

10. Create src/core/rag_engine.py (2 hours)
   ├─ Test: End-to-end query
   └─ Status: ✓ Ready for next

✓ Day 3 Complete: Full RAG pipeline works!
```

## Summary: Critical Path

**Absolute Minimum to Have Working System:**

```
.env → settings.py → base.py → csv_loader.py → embeddings.py →
vectorstore.py → (retriever.py + generator.py) → rag_engine.py → cli.py
```

**Total files: 9**
**Total time: ~2-3 days**
**Result: Working RAG system**

Everything else is an enhancement!
