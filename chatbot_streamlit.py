import streamlit as st
import pandas as pd
from openai import OpenAI
import myapikeys
from text_speech_utils import *
from langdetect import detect
from pdf_handler import pdf_upload_section, init_rag_handler

client = OpenAI(api_key=myapikeys.OPENAI_KEY)
input_audio_filename = 'input.wav'
output_audio_filename = 'chatgpt_response.wav'
output_conversation_filename = 'ChatGPT_conversation.txt'

# Initialize app and RAG handler
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "system", "content": "You are a helpful assistant. Please respond in the same language the user speaks to you."}]

# Initialize RAG handler
init_rag_handler()

st.title("My personal voice assistant")

# Add the PDF section to the sidebar
with st.sidebar:
    pdf_upload_section()

# Replace slider with a button that can detect press and hold
col1, col2 = st.columns([1, 4])
with col1:
    if st.button('🎤', key='record_button'):
        with st.spinner("Recording... (5 seconds)"):
            record_audio(input_audio_filename, sec=5)
            
            # Get transcription
            transcription = transcribe_audio(input_audio_filename)
            if transcription:
                # Detect language
                try:
                    detected_lang = detect(transcription)
                    system_msg = f"You are a helpful assistant. Please respond in {detected_lang}."
                    st.session_state['messages'][0] = {"role": "system", "content": system_msg}
                except:
                    pass
                
                # Add user message to chat
                st.session_state['messages'].append({"role": "user", "content": transcription})
                st.write(f"Me: {transcription}")
                
                # Get AI response
                if 'rag_handler' in st.session_state:
                    response = st.session_state['rag_handler'].get_response(transcription)
                else:
                    response = "RAG system not initialized. Please upload a document first."
                
                # Add AI response to chat and speak it
                st.session_state['messages'].append({"role": "assistant", "content": response})
                st.write(f"Assistant: {response}")
                say(response)

st.download_button(label="Download conversation", 
                   data = pd.DataFrame(st.session_state['messages']).to_csv(index=False).encode('utf-8'), 
                   file_name=output_conversation_filename)
