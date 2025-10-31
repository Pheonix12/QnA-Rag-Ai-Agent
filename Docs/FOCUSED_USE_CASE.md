# Document Q&A System - Focused Use Case

## Project Vision

**A Streamlit web application where users can:**
1. Upload documents (PDF, Excel, Word, Text, JSON, CSV, etc.)
2. Documents are automatically embedded and stored in ChromaDB
3. Ask questions about the uploaded documents
4. Get answers with source citations

## User Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     Streamlit Web Interface                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ↓                           ↓
      ┌──────────────────┐        ┌──────────────────┐
      │  Upload Section  │        │   Chat Section   │
      │                  │        │                  │
      │  📁 Drag & Drop  │        │  💬 Ask Question │
      │  📄 File List    │        │  🤖 Get Answer   │
      │  ✅ Status       │        │  📚 View Sources │
      └──────────────────┘        └──────────────────┘
                │                           │
                └─────────────┬─────────────┘
                              ↓
                    ┌──────────────────┐
                    │   RAG Engine     │
                    │                  │
                    │  • Embed Docs    │
                    │  • Store in DB   │
                    │  • Retrieve      │
                    │  • Generate      │
                    └──────────────────┘
                              │
                              ↓
                    ┌──────────────────┐
                    │   ChromaDB       │
                    │                  │
                    │  Vector Storage  │
                    └──────────────────┘
```

## Features

### 1. Multi-Format File Upload
- **Supported Formats:**
  - PDF (`.pdf`)
  - Word Documents (`.docx`, `.doc`)
  - Excel Spreadsheets (`.xlsx`, `.xls`, `.csv`)
  - Text Files (`.txt`, `.md`)
  - JSON Files (`.json`)
  - Presentations (`.pptx`) - Future

### 2. Automatic Processing
- **On Upload:**
  1. Validate file type
  2. Extract text content
  3. Chunk into manageable pieces
  4. Generate embeddings
  5. Store in ChromaDB
  6. Show success/error status

### 3. Intelligent Q&A
- **Features:**
  - Natural language questions
  - Context-aware answers
  - Source citations (which document + page/section)
  - Conversation history
  - Follow-up questions

### 4. Document Management
- **User Can:**
  - View uploaded documents
  - See document metadata (size, pages, upload time)
  - Delete specific documents
  - Clear entire collection
  - Create multiple collections (workspaces)

## Streamlit Interface Design

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  📚 Document Q&A System                               [Settings] │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Sidebar                          Main Area                      │
│  ┌──────────────────┐  ┌──────────────────────────────────────┐ │
│  │                  │  │                                      │ │
│  │ 📤 Upload Files  │  │  Chat Interface                      │ │
│  │                  │  │                                      │ │
│  │ [Drop files here]│  │  You: What is the summary?           │ │
│  │                  │  │  🤖: Based on the documents...       │ │
│  │ ────────────────│  │                                      │ │
│  │                  │  │  Sources: report.pdf (page 3)        │ │
│  │ 📁 My Documents  │  │                                      │ │
│  │                  │  │  ─────────────────────────────────  │ │
│  │ ✓ report.pdf     │  │                                      │ │
│  │   (5 pages)      │  │  You: [Type question...]             │ │
│  │                  │  │                             [Send →] │ │
│  │ ✓ data.xlsx      │  │                                      │ │
│  │   (200 rows)     │  │                                      │ │
│  │                  │  │                                      │ │
│  │ ✓ notes.txt      │  │                                      │ │
│  │   (1.2 KB)       │  │                                      │ │
│  │                  │  └──────────────────────────────────────┘ │
│  │ [Clear All]      │                                           │
│  └──────────────────┘                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Screens

#### 1. Welcome Screen (No Documents)
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📚 Welcome to Document Q&A System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Get started by uploading your documents!

Supported formats:
  📄 PDF, Word, Excel, CSV, Text, JSON

Upload files using the sidebar →

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 2. Upload in Progress
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Processing: annual_report.pdf
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   [████████████░░░░░░░░] 60%

   Extracting text from PDF...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 3. Chat Interface
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You: What are the key financial metrics?

🤖 Assistant:
Based on the uploaded documents, here are the key
financial metrics:

1. Revenue: $2.5M (annual_report.pdf, page 5)
2. Profit Margin: 15% (financials.xlsx, Sheet1)
3. Growth Rate: 23% YoY (quarterly.pdf, page 2)

Sources:
  📄 annual_report.pdf (pages 5, 7)
  📊 financials.xlsx (Sheet1, rows 45-50)
  📄 quarterly.pdf (page 2)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Implementation Plan

### Phase 1: Basic File Upload & Q&A (Week 1)

**Goal:** Upload PDF/TXT, ask questions

**Files to Create:**
1. `src/interfaces/streamlit_app.py` - Main Streamlit app
2. `src/data/loaders/pdf_loader.py` - PDF support
3. `src/data/loaders/text_loader.py` - TXT support
4. `src/utils/file_handler.py` - File upload handling

**Features:**
- File upload widget
- PDF and TXT processing
- Basic chat interface
- ChromaDB storage

### Phase 2: Multi-Format Support (Week 2)

**Goal:** Support all major formats

**Files to Create:**
1. `src/data/loaders/docx_loader.py` - Word documents
2. `src/data/loaders/excel_loader.py` - Excel files
3. `src/data/loaders/json_loader.py` - JSON files
4. `src/data/loaders/csv_loader.py` - CSV files (already have)

**Features:**
- All format support
- Better error handling
- File type detection

### Phase 3: Enhanced UI (Week 3)

**Goal:** Better UX and features

**Features:**
- Document preview
- Source citations with highlighting
- Conversation history
- Export Q&A as PDF
- Multiple collections/workspaces

### Phase 4: Advanced Features (Week 4)

**Goal:** Production-ready

**Features:**
- User authentication
- Share collections
- API access
- Batch upload
- Advanced search filters

## File Structure for This Use Case

```
ai-agent-llm/
├── app.py                          # Main Streamlit entry point
├── config/
│   ├── settings.py
│   └── prompts/
│       └── document_qa.txt         # Q&A prompt template
├── src/
│   ├── core/
│   │   ├── rag_engine.py
│   │   ├── embeddings.py
│   │   └── document_processor.py   # NEW: Handles all file types
│   ├── data/
│   │   ├── loaders/
│   │   │   ├── base.py
│   │   │   ├── pdf_loader.py       # NEW
│   │   │   ├── docx_loader.py      # NEW
│   │   │   ├── excel_loader.py     # NEW
│   │   │   ├── text_loader.py      # NEW
│   │   │   ├── json_loader.py      # NEW
│   │   │   └── csv_loader.py       # Already have
│   │   └── vectorstore.py
│   ├── interfaces/
│   │   ├── streamlit_app.py        # NEW: Main UI
│   │   └── components/             # NEW: UI components
│   │       ├── upload_section.py
│   │       ├── chat_section.py
│   │       └── document_list.py
│   └── utils/
│       ├── file_handler.py         # NEW: File management
│       └── session_manager.py      # NEW: Streamlit session state
├── data/
│   ├── uploads/                    # Temporary file storage
│   └── vectorstore/                # ChromaDB persistence
└── tests/
    └── test_file_upload.py
```

## Tech Stack

### Core
- **Python 3.10+**
- **LangChain** - RAG orchestration
- **ChromaDB** - Vector storage
- **Ollama** - Local LLM (llama3.2)

### File Processing
- **PyPDF2** / **pdfplumber** - PDF extraction
- **python-docx** - Word documents
- **openpyxl** / **pandas** - Excel files
- **json** - JSON parsing

### Frontend
- **Streamlit** - Web interface
- **streamlit-extras** - Enhanced components

### Optional Enhancements
- **pytesseract** - OCR for scanned PDFs
- **python-magic** - File type detection
- **pillow** - Image handling

## User Scenarios

### Scenario 1: Research Assistant
```
User uploads:
  - 10 research papers (PDF)
  - Literature review notes (DOCX)
  - Citation database (CSV)

Questions:
  - "What are the common methodologies used?"
  - "Which papers discuss climate change?"
  - "Summarize the key findings"
```

### Scenario 2: Business Analyst
```
User uploads:
  - Annual reports (PDF)
  - Financial data (XLSX)
  - Meeting notes (TXT)
  - Market data (JSON)

Questions:
  - "What was Q3 revenue?"
  - "Compare performance vs last year"
  - "What are the risk factors mentioned?"
```

### Scenario 3: Student Study Aid
```
User uploads:
  - Textbook chapters (PDF)
  - Lecture notes (DOCX)
  - Study guides (TXT)

Questions:
  - "Explain concept X"
  - "What are the key formulas?"
  - "Create a summary for exam prep"
```

### Scenario 4: Legal Document Review
```
User uploads:
  - Contracts (PDF)
  - Case law (DOCX)
  - Compliance docs (PDF)

Questions:
  - "What are the termination clauses?"
  - "Find confidentiality agreements"
  - "Compare contract terms across documents"
```

## Key Features Summary

### ✅ Must Have (Phase 1)
- [ ] Upload PDF and TXT files
- [ ] Extract and embed content
- [ ] Store in ChromaDB
- [ ] Ask questions via chat
- [ ] Show basic sources

### ✅ Should Have (Phase 2-3)
- [ ] Support Word, Excel, JSON, CSV
- [ ] Document management (view, delete)
- [ ] Better source citations
- [ ] Conversation history
- [ ] Multiple collections

### ✅ Nice to Have (Phase 4+)
- [ ] User authentication
- [ ] Share collections
- [ ] Export conversations
- [ ] OCR for scanned docs
- [ ] Batch processing
- [ ] Advanced filters

## Getting Started

### Quick Setup
```bash
# 1. Install dependencies
pip install streamlit streamlit-extras pypdf2 python-docx openpyxl

# 2. Run Streamlit app
streamlit run app.py

# 3. Open browser (usually http://localhost:8501)

# 4. Upload documents and start asking questions!
```

### First Time User Experience
1. User sees welcome screen
2. Drags and drops a PDF file
3. App shows progress: "Processing document..."
4. Success message: "✓ Document ready! Ask a question below."
5. User types: "What is this document about?"
6. App retrieves relevant chunks and generates answer
7. Shows answer with source citations

## Success Metrics

1. **Functionality**
   - ✅ Can upload 5+ file formats
   - ✅ Processing time < 10 seconds per document
   - ✅ Query response time < 5 seconds
   - ✅ Accurate source citations

2. **Usability**
   - ✅ Intuitive UI (no tutorial needed)
   - ✅ Clear error messages
   - ✅ Mobile-friendly layout

3. **Reliability**
   - ✅ Handles large files (100+ pages)
   - ✅ Graceful error handling
   - ✅ Session persistence

## Next Steps

Ready to build? Follow:
1. `STREAMLIT_IMPLEMENTATION.md` - Detailed Streamlit guide
2. `QUICK_START_STREAMLIT.md` - Day-by-day build plan
