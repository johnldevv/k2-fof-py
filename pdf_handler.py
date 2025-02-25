import streamlit as st
import os
from PyPDF2 import PdfReader
from rag_handler import RAGHandler

# Create documents directory if it doesn't exist
UPLOAD_FOLDER = "documents/pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_rag_handler():
    """Initialize RAG handler if not already in session state"""
    if 'rag_handler' not in st.session_state:
        try:
            st.session_state['rag_handler'] = RAGHandler()
            st.success("RAG handler initialized successfully!")
        except Exception as e:
            st.error(f"Error initializing RAG handler: {str(e)}")

def save_uploaded_pdf(uploaded_file):
    """Save the uploaded PDF file and return its path"""
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def load_saved_pdfs():
    """Load list of previously saved PDFs"""
    if os.path.exists(UPLOAD_FOLDER):
        return [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
    return []

def process_pdf_content(file_path, filename):
    """Extract and process PDF content"""
    with open(file_path, "rb") as f:
        pdf_reader = PdfReader(f)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Process the text with RAG handler
        st.session_state['rag_handler'].process_pdf(text, filename)
        return text

def pdf_upload_section():
    st.markdown("### Saved Documents")
    
    # Display saved PDFs
    saved_pdfs = load_saved_pdfs()
    if saved_pdfs:
        for pdf in saved_pdfs:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(pdf)
            with col2:
                if st.button("Load", key=pdf):
                    file_path = os.path.join(UPLOAD_FOLDER, pdf)
                    with open(file_path, "rb") as f:
                        pdf_reader = PdfReader(f)
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text()
                        st.session_state['pdf_content'] = text
                        
                        # Process the PDF with RAG handler
                        if 'rag_handler' in st.session_state:
                            st.session_state['rag_handler'].process_pdf(text, pdf)
    
    # Show processing status if available
    if 'current_file' in st.session_state:
        st.markdown("---")
        st.markdown("### Document Statistics")
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("📝 **Document Length:**")
            st.markdown("🔢 **Chunks Created:**")
            st.markdown("📊 **Avg. Chunk Size:**")
        with col2:
            st.markdown(f"{st.session_state['text_length']:,}")
            st.markdown(f"{st.session_state['chunk_count']}")
            st.markdown(f"{st.session_state['avg_chunk_size']:,}")
        
        if st.session_state.get('embedding_success', False):
            st.success("✅ Document embedded")
    
    # Upload new PDF section at the bottom
    st.markdown("---")
    st.markdown("### Upload New Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
    if uploaded_file is not None:
        file_path = save_uploaded_pdf(uploaded_file)
        st.success(f"File saved: {uploaded_file.name}") 