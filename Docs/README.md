# Document Q&A System

A Streamlit-based web application where users can upload documents (PDF, Word, Excel, CSV, Text, JSON) and ask questions about them using AI-powered Retrieval-Augmented Generation (RAG).

> **Note:** This README describes the full technical architecture. For a quick start guide, see [STREAMLIT_QUICK_START.md](STREAMLIT_QUICK_START.md).

## Quick Links
- **New to this project?** → [START_HERE.md](START_HERE.md)
- **Ready to build?** → [STREAMLIT_QUICK_START.md](STREAMLIT_QUICK_START.md)
- **See the use case?** → [FOCUSED_USE_CASE.md](FOCUSED_USE_CASE.md)

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   CLI Tool   │  │   REST API   │  │   Web UI     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Application Core Layer                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │            Query Processing & Orchestration              │   │
│  │  • Intent Detection  • Query Routing  • Response Gen    │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      RAG Engine Layer                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Retrieval     │  │   Augmentation  │  │   Generation    │ │
│  │   • Vector DB   │  │   • Context     │  │   • LLM         │ │
│  │   • Semantic    │  │   • Prompt      │  │   • Templates   │ │
│  │   • Hybrid      │  │   • Reranking   │  │   • Streaming   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Data Management Layer                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  Document Processing                     │   │
│  │  • Loaders  • Chunking  • Metadata  • Embeddings       │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Data Sources                          │   │
│  │  • CSV  • PDF  • JSON  • Web  • Databases  • APIs      │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Vector DB  │  │  Cache      │  │  Monitoring │             │
│  │  (Chroma/   │  │  (Redis)    │  │  (Logging)  │             │
│  │   Pinecone) │  │             │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

## Proposed Project Structure

```
ai-agent-llm/
├── README.md
├── requirements.txt
├── setup.py
├── .env.example
├── config/
│   ├── __init__.py
│   ├── settings.py              # Global configuration
│   ├── models.yaml              # LLM model configurations
│   ├── data_sources.yaml        # Data source definitions
│   └── prompts/
│       ├── default.txt
│       ├── technical.txt
│       └── conversational.txt
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── rag_engine.py       # Main RAG orchestration
│   │   ├── retriever.py        # Retrieval strategies
│   │   ├── generator.py        # LLM generation
│   │   └── embeddings.py       # Embedding management
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loaders/
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # Base loader interface
│   │   │   ├── csv_loader.py
│   │   │   ├── pdf_loader.py
│   │   │   ├── json_loader.py
│   │   │   ├── web_loader.py
│   │   │   └── database_loader.py
│   │   ├── processors/
│   │   │   ├── __init__.py
│   │   │   ├── chunker.py      # Text chunking strategies
│   │   │   ├── cleaner.py      # Data cleaning
│   │   │   └── metadata.py     # Metadata extraction
│   │   └── vectorstore.py      # Vector database interface
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── cli.py              # Command-line interface
│   │   ├── api.py              # REST API (FastAPI)
│   │   └── websocket.py        # WebSocket for streaming
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py           # Logging utilities
│   │   ├── cache.py            # Caching layer
│   │   └── monitoring.py       # Performance monitoring
│   └── agents/
│       ├── __init__.py
│       ├── base_agent.py       # Base agent class
│       ├── qa_agent.py         # Q&A specialized agent
│       ├── search_agent.py     # Search specialized agent
│       └── chat_agent.py       # Conversational agent
├── data/
│   ├── raw/                    # Raw data files
│   ├── processed/              # Processed documents
│   └── vectorstore/            # Vector DB persistence
├── tests/
│   ├── __init__.py
│   ├── test_loaders.py
│   ├── test_retrieval.py
│   └── test_generation.py
├── scripts/
│   ├── ingest_data.py          # Data ingestion script
│   ├── update_vectorstore.py   # Update vector DB
│   └── benchmark.py            # Performance benchmarking
├── examples/
│   ├── restaurant_qa.py        # Original use case
│   ├── document_qa.py          # Document Q&A
│   ├── code_assistant.py       # Code Q&A
│   └── customer_support.py     # Support chatbot
└── docs/
    ├── architecture.md
    ├── configuration.md
    ├── api_reference.md
    └── deployment.md
```

## Key Components

### 1. Data Management Layer

**Purpose**: Handle diverse data sources and prepare documents for retrieval

**Components**:
- **Loaders**: Pluggable loaders for different data types
  - CSV, JSON, XML
  - PDF, DOCX, TXT
  - Web scraping (HTML, Markdown)
  - Databases (SQL, MongoDB)
  - APIs (REST, GraphQL)

- **Processors**: Transform and enhance documents
  - Intelligent chunking (semantic, fixed-size, recursive)
  - Metadata extraction (dates, authors, categories)
  - Data cleaning and normalization

### 2. RAG Engine Layer

**Purpose**: Core retrieval-augmented generation logic

**Components**:
- **Retriever**: Multiple retrieval strategies
  - Vector similarity search (semantic)
  - Keyword search (BM25)
  - Hybrid search (combining semantic + keyword)
  - Re-ranking for improved relevance

- **Augmentation**: Context enhancement
  - Prompt engineering and templates
  - Context window management
  - Citation and source tracking

- **Generator**: LLM integration
  - Multiple model support (Ollama, OpenAI, Anthropic)
  - Streaming responses
  - Temperature and parameter control

### 3. Application Core Layer

**Purpose**: Business logic and orchestration

**Components**:
- **Query Processing**: Intent detection and routing
- **Session Management**: Conversation history
- **Agent System**: Specialized agents for different tasks
- **Response Formatting**: Output customization

### 4. Interface Layer

**Purpose**: User-facing interfaces

**Components**:
- **CLI**: Interactive command-line tool
- **REST API**: HTTP endpoints for integration
- **WebSocket**: Real-time streaming responses
- **Web UI**: Optional web interface (React/Streamlit)

### 5. Infrastructure Layer

**Purpose**: Supporting services and utilities

**Components**:
- **Vector Database**: Chroma, Pinecone, Weaviate, or Qdrant
- **Caching**: Redis for query caching
- **Logging**: Structured logging with log levels
- **Monitoring**: Performance metrics and tracing

## Key Features

### 1. Multi-Source Data Ingestion
```python
# Ingest from multiple sources
rag_app.ingest(
    sources=[
        {"type": "csv", "path": "reviews.csv"},
        {"type": "pdf", "path": "manual.pdf"},
        {"type": "web", "url": "https://docs.example.com"},
        {"type": "database", "connection": "postgresql://..."}
    ]
)
```

### 2. Configurable Retrieval Strategies
```yaml
retrieval:
  strategy: hybrid  # semantic, keyword, hybrid
  top_k: 5
  similarity_threshold: 0.7
  reranking: true
```

### 3. Multiple LLM Support
```yaml
models:
  default: ollama/llama3.2
  alternatives:
    - openai/gpt-4
    - anthropic/claude-3-sonnet
    - ollama/mistral
```

### 4. Specialized Agents
- **QA Agent**: Direct question-answering
- **Chat Agent**: Conversational interactions with memory
- **Search Agent**: Information retrieval and summarization
- **Code Agent**: Technical documentation and code assistance

### 5. Advanced Features
- **Conversation Memory**: Multi-turn dialogue support
- **Source Citations**: Track and display sources
- **Query Optimization**: Automatic query expansion and refinement
- **Multi-tenancy**: Support multiple knowledge bases
- **Access Control**: User authentication and permissions

## Use Cases

### 1. Customer Support Bot
```python
from src.agents import ChatAgent
from src.core import RAGEngine

# Initialize with support documentation
agent = ChatAgent(
    knowledge_base="customer_support",
    persona="helpful support representative"
)
response = agent.chat("How do I reset my password?")
```

### 2. Technical Documentation Assistant
```python
from src.agents import QAAgent

# Load technical docs
agent = QAAgent(
    sources=["api_docs/", "tutorials/", "examples/"],
    model="gpt-4",
    prompt_template="technical"
)
answer = agent.query("How do I authenticate API requests?")
```

### 3. Research Paper Analysis
```python
from src.data.loaders import PDFLoader
from src.agents import SearchAgent

# Index research papers
loader = PDFLoader()
agent = SearchAgent()
agent.ingest_documents(loader.load_directory("papers/"))
summary = agent.search("What are the latest advances in RAG?")
```

### 4. Internal Knowledge Base
```python
# Company wiki, documentation, policies
rag_app.ingest_sources({
    "confluence": {"url": "...", "auth": "..."},
    "sharepoint": {"url": "...", "auth": "..."},
    "gdrive": {"folder_id": "...", "auth": "..."}
})
```

## Configuration

### Environment Variables (.env)
```bash
# LLM Configuration
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2
LLM_BASE_URL=http://localhost:11434

# Embedding Model
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=mxbai-embed-large

# Vector Database
VECTOR_DB=chroma
VECTOR_DB_PATH=./data/vectorstore

# API Keys (if using cloud services)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
PINECONE_API_KEY=

# Application Settings
LOG_LEVEL=INFO
CACHE_ENABLED=true
MAX_CONTEXT_LENGTH=4096
```

### Data Source Configuration (config/data_sources.yaml)
```yaml
data_sources:
  - name: main_knowledge_base
    type: csv
    path: ./data/raw/knowledge.csv
    enabled: true

  - name: documentation
    type: directory
    path: ./docs
    file_types: [.md, .txt, .pdf]
    recursive: true

  - name: web_content
    type: web
    urls:
      - https://example.com/docs
    depth: 2

  - name: database
    type: postgresql
    connection: ${DATABASE_URL}
    query: "SELECT * FROM knowledge_articles"
```

## Getting Started

### Installation
```bash
# Clone repository
git clone <repo-url>
cd ai-agent-llm

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your configuration
```

### Quick Start
```bash
# 1. Ingest your data
python scripts/ingest_data.py --source ./data/raw --config config/data_sources.yaml

# 2. Start CLI interface
python -m src.interfaces.cli

# Or start API server
python -m src.interfaces.api --host 0.0.0.0 --port 8000
```

### API Usage
```bash
# Start the API server
uvicorn src.interfaces.api:app --reload

# Query endpoint
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Your question here", "top_k": 5}'

# Ingest new documents
curl -X POST http://localhost:8000/api/v1/ingest \
  -F "file=@document.pdf" \
  -F "source_type=pdf"
```

## Development Roadmap

### Phase 1: Core Generalization (Current → v0.2)
- [ ] Refactor current code into modular structure
- [ ] Create base loader interface and CSV loader
- [ ] Add PDF and JSON loaders
- [ ] Implement configuration management
- [ ] Add basic REST API

### Phase 2: Enhanced RAG (v0.2 → v0.5)
- [ ] Hybrid search (semantic + keyword)
- [ ] Query optimization and expansion
- [ ] Re-ranking for better relevance
- [ ] Multiple vector database support
- [ ] Conversation memory and context
- [ ] Source citation tracking

### Phase 3: Advanced Features (v0.5 → v1.0)
- [ ] Agent system with specialized agents
- [ ] Multi-tenancy support
- [ ] Authentication and authorization
- [ ] Caching layer (Redis)
- [ ] Performance monitoring
- [ ] Web UI (Streamlit/React)

### Phase 4: Enterprise Features (v1.0+)
- [ ] Distributed processing
- [ ] Advanced analytics
- [ ] A/B testing for prompts
- [ ] Fine-tuning support
- [ ] Kubernetes deployment
- [ ] Multi-language support

## Performance Considerations

### Scalability
- **Vector DB Selection**: Choose based on scale
  - Chroma: Small to medium (< 1M documents)
  - Pinecone/Weaviate: Large scale (> 1M documents)
  - Qdrant: On-premise large scale

- **Caching**: Implement query result caching for common queries
- **Async Processing**: Use async/await for I/O operations
- **Batch Processing**: Process documents in batches for ingestion

### Optimization Tips
- Use smaller embedding models for faster retrieval
- Implement query caching for frequently asked questions
- Optimize chunk sizes based on your data type
- Use hybrid search for better accuracy
- Implement pagination for large result sets

## Testing Strategy

```bash
# Run all tests
pytest tests/

# Test specific component
pytest tests/test_loaders.py

# Test with coverage
pytest --cov=src tests/
```

## Deployment Options

### Local Deployment
```bash
# Using Docker
docker-compose up -d
```

### Cloud Deployment
- **AWS**: ECS/EKS with RDS + S3
- **GCP**: Cloud Run + Cloud SQL + GCS
- **Azure**: Container Apps + Cosmos DB + Blob Storage

### Serverless Options
- API Gateway + Lambda + DynamoDB (AWS)
- Cloud Functions + Firestore (GCP)

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for guidelines.

## License

[Your License Here]

## References

- [LangChain Documentation](https://python.langchain.com/)
- [Chroma Vector Database](https://docs.trychroma.com/)
- [RAG Best Practices](https://www.anthropic.com/index/retrieval-augmented-generation)
