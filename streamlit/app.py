import streamlit as st
import sys
import os
from pathlib import Path

# Add backend to sys.path to allow imports
# Assuming structure:
# root/
#   streamlit/app.py
#   backend/audio/...
BACKEND_DIR = Path(__file__).parent.parent / "backend"
sys.path.append(str(BACKEND_DIR))

try:
    from audio import youtube_speech_recognition
    from audio import youtube_whisper
    from audio import youtube_vosk
    # from audio import youtube_audio_downloader # Not strictly needed if modules call it, but good for debugging if needed
except ImportError as e:
    st.error(f"Failed to import backend modules. Ensure directory structure is correct. Error: {e}")
    st.stop()

st.set_page_config(page_title="Vachak: YouTube Transcriber", layout="wide")

st.title("VIDEO TO AUDIO")
st.markdown("Enter a YouTube URL to transcribe it using multiple engines.")

youtube_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Transcribe All"):
    if not youtube_url:
        st.warning("Please enter a URL.")
    else:
        st.info("Processing... This may take a while depending on video length and hardware.")
        
        # Create tabs for results
        tab1, tab2, tab3 = st.tabs(["SpeechRecognition (Google)", "Whisper (Offline)", "Vosk (Offline)"])
        
        # We run them sequentially for now to avoid threading complexity with shared resources, 
        # though parallel execution is possible.
        
        # 1. Google
        with tab1:
            st.subheader("SpeechRecognition (Google Web Speech)")
            with st.spinner("Transcribing with Google..."):
                try:
                    text_google = youtube_speech_recognition.transcribe_with_speech_recognition(youtube_url)
                    st.text_area("Result", text_google, height=300)
                    st.success("Done!")
                except Exception as e:
                    st.error(f"Error: {e}")

        # 2. Whisper
        with tab2:
            st.subheader("OpenAI Whisper (Base Model)")
            with st.spinner("Transcribing with Whisper..."):
                try:
                    text_whisper = youtube_whisper.transcribe_with_whisper(youtube_url)
                    st.text_area("Result", text_whisper, height=300)
                    st.success("Done!")
                except Exception as e:
                    st.error(f"Error: {e}")

        # 3. Vosk
        with tab3:
            st.subheader("Vosk (Offline)")
            with st.spinner("Transcribing with Vosk..."):
                try:
                    text_vosk = youtube_vosk.transcribe_with_vosk(youtube_url)
                    st.text_area("Result", text_vosk, height=300)
                    st.success("Done!")
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.info("Ensure the Vosk model is present in `backend/modules/model/`.")

st.sidebar.markdown("### Instructions")
st.sidebar.info(
    """
    1. Paste a YouTube Link.
    2. Click 'Transcribe All'.
    3. View results in tabs.
    
    **Note:** 
    - Google API requires internet.
    - Whisper and Vosk run locally (offline).
    - Vosk requires a downloaded model in `backend/modules/model`.
    """
)
