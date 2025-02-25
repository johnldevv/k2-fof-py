import streamlit as st
import os
from PyPDF2 import PdfReader
from datetime import datetime

# Create documents directory if it doesn't exist
UPLOAD_FOLDER = "documents/pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_uploaded_pdf(uploaded_file):
    """Save the uploaded PDF file and return its path"""
    # Create a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    # Save the file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def load_saved_pdfs():
    """Load list of previously saved PDFs"""
    if os.path.exists(UPLOAD_FOLDER):
        return [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
    return []

# Add this to your Streamlit UI
def pdf_upload_section():
    st.subheader("PDF Documents")
    
    # Upload new PDF
    uploaded_file = st.file_uploader("Upload a PDF document", type=['pdf'])
    if uploaded_file is not None:
        file_path = save_uploaded_pdf(uploaded_file)
        st.success(f"File saved successfully: {uploaded_file.name}")
    
    # Display saved PDFs
    saved_pdfs = load_saved_pdfs()
    if saved_pdfs:
        st.subheader("Saved Documents")
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
                        st.success("PDF content loaded!") 