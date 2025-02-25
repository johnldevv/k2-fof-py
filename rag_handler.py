from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
import os
import myapikeys
import streamlit as st
import pyperclip

class RAGHandler:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.embeddings = OpenAIEmbeddings(openai_api_key=myapikeys.OPENAI_KEY)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.llm = ChatOpenAI(model_name=model_name, temperature=0, openai_api_key=myapikeys.OPENAI_KEY)
        self.vector_store = None
        
        # Updated prompt template
        template = """You are a helpful AI assistant that uses information from provided documents to answer questions.
        
        RULES:
        1. ONLY use information from the provided context
        2. If the context doesn't contain enough information for a complete answer, say "Based on the available documents, I can tell you that [partial information]. However, I don't have complete information about [missing aspects]."
        3. If the context has no relevant information at all, say "I cannot answer this based on the provided documents."
        4. Make your answers conversational and suitable for voice output
        5. Keep responses concise but informative
        
        Context from documents:
        {context}

        Question: {question}

        Answer (using ONLY the above context): """
        
        self.prompt = ChatPromptTemplate.from_template(template)

    def process_pdf(self, pdf_text, filename):
        """Process PDF content and store filename in metadata"""
        # Split the text into chunks
        splits = self.text_splitter.split_text(pdf_text)
        
        # Store processing details in session state
        st.session_state['current_file'] = filename
        st.session_state['text_length'] = len(pdf_text)
        st.session_state['chunk_count'] = len(splits)
        st.session_state['avg_chunk_size'] = len(pdf_text)//len(splits)
        
        # Process the chunks
        texts_with_metadata = [
            {"text": split, "metadata": {"source": filename, "chunk": i}} 
            for i, split in enumerate(splits)
        ]
        
        try:
            if self.vector_store is None:
                self.vector_store = FAISS.from_texts(
                    [t["text"] for t in texts_with_metadata],
                    self.embeddings,
                    metadatas=[t["metadata"] for t in texts_with_metadata]
                )
            else:
                self.vector_store.add_texts(
                    [t["text"] for t in texts_with_metadata],
                    metadatas=[t["metadata"] for t in texts_with_metadata]
                )
            st.session_state['embedding_success'] = True
        except Exception as e:
            st.session_state['embedding_success'] = False
            st.error(f"❌ Error during embedding: {str(e)}")

    def verify_embeddings(self, test_query="test"):
        """Verify that embeddings are working"""
        if self.vector_store is None:
            return "No documents loaded yet"
        
        try:
            # Try to retrieve documents
            docs = self.vector_store.similarity_search(test_query, k=1)
            return f"✅ Embeddings verified: Successfully retrieved {len(docs)} documents"
        except Exception as e:
            return f"❌ Embedding verification failed: {str(e)}"

    def get_response(self, question):
        """Get response using RAG"""
        if self.vector_store is None:
            return "No documents have been processed yet. Please upload a PDF first."
        
        # Get relevant documents
        docs = self.vector_store.similarity_search(question)
        
        # Display relevant chunks with unique keys
        st.markdown("#### Relevant Document Chunks:")
        for i, doc in enumerate(docs):
            with st.expander(f"Source: {doc.metadata['source']} (Chunk {doc.metadata['chunk']})"):
                st.text_area(
                    "Content",
                    value=doc.page_content,
                    key=f"text_{i}_{doc.metadata['source']}_{doc.metadata['chunk']}",
                    height=150
                )
        
        # Format prompt with context
        context = "\n\n".join([doc.page_content for doc in docs])
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Use the provided context to answer questions."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
        
        # Get response from OpenAI using LangChain's ChatOpenAI
        try:
            response = self.llm(messages)  # LangChain's ChatOpenAI uses direct calling
            return response.content
        except Exception as e:
            return f"Error getting response: {str(e)}"

    def get_stats(self):
        """Return statistics about the loaded documents"""
        if self.vector_store is None:
            return "📚 No documents loaded"
        
        try:
            # Get all documents and their metadata
            docs = self.vector_store.similarity_search("", k=1000)  # Get all docs
            
            # Count unique sources
            sources = set(doc.metadata['source'] for doc in docs)
            
            # Debug info
            st.write("📊 Vector Store Statistics:")
            st.write(f"- Total chunks: {len(docs)}")
            st.write(f"- Unique documents: {len(sources)}")
            st.write("\nLoaded documents:")
            for source in sources:
                st.write(f"- {source}")
            
            return f"📚 System ready with {len(docs)} chunks from {len(sources)} documents"
        except Exception as e:
            return f"❌ Error getting stats: {str(e)}" 