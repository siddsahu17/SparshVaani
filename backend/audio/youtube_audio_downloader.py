import os
import yt_dlp
import subprocess
from pathlib import Path

# Define the output directory for audio files
# Since this file is now in 'backend/audio', the audio dir is the same as the file's dir
AUDIO_DIR = Path(__file__).parent

def download_youtube_audio(youtube_url: str) -> str:
    """
    Downloads audio from a YouTube URL usage yt-dlp and converts it to WAV (16kHz, mono).
    
    Args:
        youtube_url (str): The URL of the YouTube video.
        
    Returns:
        str: The absolute path to the converted WAV file.
        
    Raises:
        RuntimeError: If download or conversion fails.
    """
    try:
        print(f"Downloading audio from: {youtube_url}")
        
        # Configure yt-dlp to download best audio and convert to wav
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(AUDIO_DIR / '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info)
            # yt-dlp changes extension after post-processing
            base_filename = os.path.splitext(filename)[0]
            wav_filename = f"{base_filename}.wav"
            
            # Ensure the file exists
            if not os.path.exists(wav_filename):
                 pass

        # Post-processing to ensure 16kHz mono (Standard for most speech rec models)
        final_wav_path = str(AUDIO_DIR / f"{os.path.splitext(os.path.basename(wav_filename))[0]}_16k.wav")
        
        print(f"Converting to 16kHz mono: {final_wav_path}")
        
        # explicit ffmpeg call to ensure format valid for Vosk/Whisper/etc
        command = [
            'ffmpeg', '-y', 
            '-i', wav_filename, 
            '-ar', '16000', 
            '-ac', '1', 
            final_wav_path
        ]
        
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Clean up original download
        if os.path.exists(wav_filename):
             os.remove(wav_filename)
             
        return final_wav_path

    except Exception as e:
        raise RuntimeError(f"Failed to download/process YouTube audio: {e}")
