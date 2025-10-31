"""
Document Q&A System - Streamlit Frontend
Upload documents and ask questions about them using RAG
"""

import streamlit as st
from pathlib import Path
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Document Q&A System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .uploaded-file {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .source-citation {
        background-color: #e8f4f8;
        padding: 8px;
        border-left: 3px solid #1f77b4;
        margin: 5px 0;
        font-size: 0.9rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = None

if 'collection_name' not in st.session_state:
    st.session_state.collection_name = "default"

# Import RAG components (will be created)
try:
    from src.core.rag_engine import RAGEngine
    from src.data.loaders import get_loader
    from src.utils.file_handler import FileHandler
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    st.error("⚠️ RAG components not found. Please complete Phase 1 setup first.")

# Helper functions
def initialize_rag_engine():
    """Initialize RAG engine if not already done."""
    if st.session_state.rag_engine is None and RAG_AVAILABLE:
        st.session_state.rag_engine = RAGEngine(
            collection_name=st.session_state.collection_name
        )

def get_file_type(filename):
    """Get file type from filename."""
    ext = Path(filename).suffix.lower()
    type_map = {
        '.pdf': 'pdf',
        '.docx': 'docx',
        '.doc': 'docx',
        '.xlsx': 'excel',
        '.xls': 'excel',
        '.csv': 'csv',
        '.txt': 'text',
        '.md': 'text',
        '.json': 'json'
    }
    return type_map.get(ext)

def process_uploaded_file(uploaded_file):
    """Process an uploaded file and add to vector store."""
    try:
        # Save file temporarily
        upload_dir = Path("data/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Get appropriate loader
        file_type = get_file_type(uploaded_file.name)

        if not file_type:
            return False, f"Unsupported file type: {uploaded_file.name}"

        # Load and ingest document
        loader = get_loader(file_type)(str(file_path))

        if not loader:
            return False, f"No loader available for {file_type}"

        num_docs = st.session_state.rag_engine.ingest(loader)

        # Add to uploaded files list
        st.session_state.uploaded_files.append({
            'name': uploaded_file.name,
            'size': uploaded_file.size,
            'type': file_type,
            'uploaded_at': datetime.now(),
            'chunks': num_docs
        })

        return True, f"✓ Processed {num_docs} chunks from {uploaded_file.name}"

    except Exception as e:
        return False, f"Error processing {uploaded_file.name}: {str(e)}"

# Main UI
def main():
    # Header
    st.markdown('<p class="main-header">📚 Document Q&A System</p>', unsafe_allow_html=True)

    # Initialize RAG engine
    if RAG_AVAILABLE:
        initialize_rag_engine()

    # Sidebar
    with st.sidebar:
        st.header("📤 Upload Documents")

        # Collection selector
        collection_name = st.text_input(
            "Collection Name",
            value=st.session_state.collection_name,
            help="Group related documents in collections"
        )

        if collection_name != st.session_state.collection_name:
            st.session_state.collection_name = collection_name
            st.session_state.rag_engine = None
            st.session_state.uploaded_files = []
            st.rerun()

        st.markdown("---")

        # File uploader
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['pdf', 'docx', 'doc', 'xlsx', 'xls', 'csv', 'txt', 'md', 'json'],
            accept_multiple_files=True,
            help="Upload PDF, Word, Excel, CSV, Text, or JSON files"
        )

        if uploaded_files and RAG_AVAILABLE:
            with st.spinner("Processing files..."):
                for uploaded_file in uploaded_files:
                    # Check if already uploaded
                    if uploaded_file.name not in [f['name'] for f in st.session_state.uploaded_files]:
                        success, message = process_uploaded_file(uploaded_file)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)

        st.markdown("---")

        # Document list
        st.header("📁 My Documents")

        if st.session_state.uploaded_files:
            for i, file_info in enumerate(st.session_state.uploaded_files):
                with st.expander(f"📄 {file_info['name']}"):
                    st.write(f"**Type:** {file_info['type']}")
                    st.write(f"**Size:** {file_info['size']:,} bytes")
                    st.write(f"**Chunks:** {file_info['chunks']}")
                    st.write(f"**Uploaded:** {file_info['uploaded_at'].strftime('%Y-%m-%d %H:%M')}")

            st.markdown("---")

            if st.button("🗑️ Clear All Documents", type="secondary"):
                if st.session_state.rag_engine:
                    st.session_state.rag_engine.retriever.vectorstore_manager.delete_collection()
                st.session_state.uploaded_files = []
                st.session_state.messages = []
                st.session_state.rag_engine = None
                st.success("✓ All documents cleared!")
                st.rerun()
        else:
            st.info("No documents uploaded yet")

        st.markdown("---")

        # Info
        with st.expander("ℹ️ Supported Formats"):
            st.markdown("""
            - **PDF** (.pdf)
            - **Word** (.docx, .doc)
            - **Excel** (.xlsx, .xls)
            - **CSV** (.csv)
            - **Text** (.txt, .md)
            - **JSON** (.json)
            """)

        with st.expander("💡 Tips"):
            st.markdown("""
            1. Upload multiple files at once
            2. Ask specific questions for better answers
            3. Check sources to verify information
            4. Use collections to organize documents
            """)

    # Main content area
    if not RAG_AVAILABLE:
        st.warning("""
        ### 🚧 Setup Required

        The RAG components are not yet set up. Please follow these steps:

        1. Complete Phase 1 from `QUICK_START.md`
        2. Create the necessary loaders
        3. Restart the Streamlit app

        See `FOCUSED_USE_CASE.md` for details.
        """)
        return

    if not st.session_state.uploaded_files:
        # Welcome screen
        st.markdown("""
        ### 👋 Welcome to Document Q&A System!

        Get started by uploading your documents using the sidebar.

        **How it works:**
        1. 📤 Upload your documents (PDF, Word, Excel, etc.)
        2. ⚡ Documents are automatically processed and embedded
        3. 💬 Ask questions about your documents
        4. 🎯 Get accurate answers with source citations

        **Example questions:**
        - "What is this document about?"
        - "Summarize the key points"
        - "What are the main findings?"
        - "Find information about [topic]"
        """)

        # Sample use cases
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            #### 🎓 Research
            Upload papers and notes to:
            - Find related studies
            - Compare methodologies
            - Summarize findings
            """)

        with col2:
            st.markdown("""
            #### 💼 Business
            Analyze reports and data:
            - Extract metrics
            - Find insights
            - Compare periods
            """)

        with col3:
            st.markdown("""
            #### 📖 Study
            Learn from materials:
            - Get explanations
            - Find examples
            - Create summaries
            """)

    else:
        # Chat interface
        st.markdown("### 💬 Ask Questions About Your Documents")

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

                # Show sources if available
                if "sources" in message and message["sources"]:
                    with st.expander("📚 View Sources"):
                        for source in message["sources"]:
                            st.markdown(f"""
                            <div class="source-citation">
                            📄 <strong>{source.metadata.get('source', 'Unknown')}</strong><br>
                            {source.page_content[:200]}...
                            </div>
                            """, unsafe_allow_html=True)

        # Chat input
        if prompt := st.chat_input("Ask a question about your documents..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        result = st.session_state.rag_engine.query(prompt)
                        response = result['answer']
                        sources = result.get('sources', [])

                        st.markdown(response)

                        # Show sources
                        if sources:
                            with st.expander("📚 View Sources"):
                                for source in sources:
                                    st.markdown(f"""
                                    <div class="source-citation">
                                    📄 <strong>{source.metadata.get('source', 'Unknown')}</strong><br>
                                    {source.page_content[:200]}...
                                    </div>
                                    """, unsafe_allow_html=True)

                        # Add assistant message
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "sources": sources
                        })

                    except Exception as e:
                        error_msg = f"Error generating response: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg
                        })

        # Clear chat button
        if st.session_state.messages:
            if st.button("🗑️ Clear Chat History"):
                st.session_state.messages = []
                st.rerun()

if __name__ == "__main__":
    main()
