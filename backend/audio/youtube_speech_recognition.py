import os
import speech_recognition as sr
from .youtube_audio_downloader import download_youtube_audio

# Define output file path
# Since this file is in 'backend/audio', output goes to same dir
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "speech_recognition_output.txt")

def transcribe_with_speech_recognition(youtube_url: str):
    """
    Downloads audio from YouTube and transcribes it using SpeechRecognition (Google Web Speech API).
    """
    try:
        # Step 1: Download Audio
        wav_path = download_youtube_audio(youtube_url)
        
        # Step 2: Initialize Recognizer
        recognizer = sr.Recognizer()
        
        print(f"Transcribing with SpeechRecognition: {wav_path}")
        
        # Step 3: Transcribe
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            try:
                # Google Web Speech API (default key)
                text = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                text = "[Error: Speech was unintelligible]"
            except sr.RequestError as e:
                text = f"[Error: Request failed; {e}]"
        
        # Step 4: Save Output
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(text)
            
        print(f"Transcription saved to: {OUTPUT_FILE}")
        print("-" * 50)
        print(text)
        print("-" * 50)
        
        return text

    except Exception as e:
        error_msg = f"Error in SpeechRecognition module: {e}"
        print(error_msg)
        return error_msg
