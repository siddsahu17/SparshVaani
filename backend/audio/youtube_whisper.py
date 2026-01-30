import os
import whisper
from .youtube_audio_downloader import download_youtube_audio

# Define output file path
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "whisper_output.txt")

def transcribe_with_whisper(youtube_url: str):
    """
    Downloads audio from YouTube and transcribes it using OpenAI Whisper (offline).
    """
    try:
        # Step 1: Download Audio
        wav_path = download_youtube_audio(youtube_url)
        
        print("Loading Whisper model (base)...")
        # Step 2: Load Model
        model = whisper.load_model("base")
        
        print(f"Transcribing with Whisper: {wav_path}")
        
        # Step 3: Transcribe
        result = model.transcribe(wav_path)
        text = result["text"]
        language = result.get("language", "unknown")
        
        # Step 4: Save Output
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"[Detected Language: {language}]\n\n")
            f.write(text)
            
        print(f"Transcription saved to: {OUTPUT_FILE}")
        print(f"Detected Language: {language}")
        print("-" * 50)
        print(text)
        print("-" * 50)
        
        return text

    except Exception as e:
        error_msg = f"Error in Whisper module: {e}"
        print(error_msg)
        return error_msg
