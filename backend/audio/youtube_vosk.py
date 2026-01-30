import os
import wave
import json
from vosk import Model, KaldiRecognizer
from .youtube_audio_downloader import download_youtube_audio

# Define paths
# Current dir: backend/audio
AUDIO_DIR = os.path.dirname(__file__)
# Model dir: backend/modules/model -> ../modules/model
MODEL_DIR = os.path.join(AUDIO_DIR, "..", "modules", "model")
OUTPUT_FILE = os.path.join(AUDIO_DIR, "vosk_output.txt")

def transcribe_with_vosk(youtube_url: str):
    """
    Downloads audio from YouTube and transcribes it using Vosk (offline).
    Requires a Vosk model in 'backend/modules/model/'.
    """
    try:
        # Step 1: Check Model
        if not os.path.exists(MODEL_DIR) or not os.listdir(MODEL_DIR):
             raise FileNotFoundError(f"Vosk model not found in {MODEL_DIR}. Please download a model (e.g., vosk-model-small-en-us-0.15) and extract it there.")

        # Step 2: Download Audio
        wav_path = download_youtube_audio(youtube_url)
        
        print(f"Loading Vosk model from: {MODEL_DIR}")
        # Auto-detect model inside directory if it's a subdir
        model_path = MODEL_DIR
        # If the user extracted a folder inside 'model', use that
        subdirs = [d for d in os.listdir(MODEL_DIR) if os.path.isdir(os.path.join(MODEL_DIR, d))]
        if subdirs:
             model_path = os.path.join(MODEL_DIR, subdirs[0])
             
        model = Model(model_path)
        
        # Step 3: Open Audio
        wf = wave.open(wav_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            # Although downloader ensures 16k mono wav, double check
             print("Audio file must be WAV format mono PCM.")
        
        rec = KaldiRecognizer(model, wf.getframerate())
        
        print(f"Transcribing with Vosk: {wav_path}")
        
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                part = json.loads(rec.Result())
                results.append(part.get("text", ""))
        
        final_part = json.loads(rec.FinalResult())
        results.append(final_part.get("text", ""))
        
        full_text = " ".join([r for r in results if r])
        
        # Step 4: Save Output
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(full_text)
            
        print(f"Transcription saved to: {OUTPUT_FILE}")
        print("-" * 50)
        print(full_text)
        print("-" * 50)
        
        return full_text

    except Exception as e:
        error_msg = f"Error in Vosk module: {e}"
        print(error_msg)
        return error_msg
