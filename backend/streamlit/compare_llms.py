import streamlit as st
import sys
import os
import time
from dotenv import load_dotenv

# Load .env
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Add parent directory to path to import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.agents.agent_orchestrator import run_agent_workflow

st.set_page_config(page_title="LLM Comparison: OpenAI vs Ollama", layout="wide")

st.title("🤖 LLM Comparison: OpenAI vs Ollama")
st.markdown("Run the same agent pipeline with two different LLM providers to compare accuracy, speed, and quality.")

# Sidebar Settings
st.sidebar.header("Settings")
youtube_url = st.sidebar.text_input("YouTube URL", "https://www.youtube.com/watch?v=example")
openai_model = st.sidebar.selectbox("OpenAI Model", ["gpt-4o", "gpt-3.5-turbo"], index=0)
ollama_model = st.sidebar.text_input("Ollama Model", "mistral")

if st.sidebar.button("Run Comparison"):
    if not youtube_url:
        st.error("Please enter a YouTube URL.")
    else:
        col1, col2 = st.columns(2)
        
        # --- OpenAI Run ---
        with col1:
            st.header("OpenAI")
            st.info(f"Running with {openai_model}...")
            start_time = time.time()
            
            try:
                results_openai = run_agent_workflow(youtube_url, provider_type="openai", provider_model=openai_model)
                end_time = time.time()
                st.success(f"Completed in {end_time - start_time:.2f}s")
                
                st.subheader("Language")
                st.write(results_openai.get("language", "N/A"))
                
                st.subheader("Context")
                st.json(results_openai.get("context", {}))
                
                st.subheader("Summary")
                st.write(results_openai.get("summary", "N/A"))
                
                st.subheader("Notes")
                notes = results_openai.get("notes", [])
                for note in notes:
                    st.write(f"- {note}")
                    
                st.subheader("Q&A")
                qa = results_openai.get("qa", [])
                for item in qa:
                    with st.expander(item.get("question", "Question")):
                        st.write(item.get("answer", "Answer"))

                st.subheader("PDF")
                st.write(results_openai.get("pdf_path", "N/A"))
                
            except Exception as e:
                st.error(f"Error: {e}")

        # --- Ollama Run ---
        with col2:
            st.header("Ollama (Local)")
            st.info(f"Running with {ollama_model}...")
            start_time = time.time()
            
            try:
                results_ollama = run_agent_workflow(youtube_url, provider_type="ollama", provider_model=ollama_model)
                end_time = time.time()
                st.success(f"Completed in {end_time - start_time:.2f}s")
                
                st.subheader("Language")
                st.write(results_ollama.get("language", "N/A"))
                
                st.subheader("Context")
                st.json(results_ollama.get("context", {}))
                
                st.subheader("Summary")
                st.write(results_ollama.get("summary", "N/A"))
                
                st.subheader("Notes")
                notes = results_ollama.get("notes", [])
                for note in notes:
                    st.write(f"- {note}")
                    
                st.subheader("Q&A")
                qa = results_ollama.get("qa", [])
                for item in qa:
                    with st.expander(item.get("question", "Question")):
                        st.write(item.get("answer", "Answer"))
                        
                st.subheader("PDF")
                st.write(results_ollama.get("pdf_path", "N/A"))
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.warning("Make sure Ollama is running (`ollama serve`) and the model is pulled (`ollama pull mistral`).")
