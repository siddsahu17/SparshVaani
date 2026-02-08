# SparshVaani: AI-Powered Study Companion for the Visually Impaired 🌟

**SparshVaani** is an advanced multi-agent system designed to make educational content accessible. It takes YouTube video URLs as input and generates comprehensive study materials, including summaries, structured notes, Q&A, and Braille-ready PDFs.

The project is built with **Python**, **Streamlit**, and **FastAPI**, leveraging **LLMs (Large Language Models)** for intelligent processing. It supports both cloud-based (OpenAI) and privacy-focused local execution (Ollama).

---

## 🚀 Key Features

*   **Multi-Agent Architecture**: A coordinated workflow of specialized agents:
    *   **Language Detective**: Identifies the video's language.
    *   **Transcriber**: Converts audio to text using Google Speech Recognition, OpenAI Whisper, or Vosk.
    *   **Context Analyzer**: Determines the topic and educational intent.
    *   **Summarizer**: Creates concise executive summaries.
    *   **Note Taker**: Generates structured, bullet-point study notes.
    *   **Examiner (Q&A)**: Creates practice questions and answers.
    *   **Braille Converter**: Translates text into Grade 1 Braille (Unicode).
*   **LLM Agnosticism**:
    *   **OpenAI**: Uses GPT-4o / GPT-3.5 for high-quality cloud processing.
    *   **Ollama**: Supports local models (e.g., Mistral, Llama 3) for offline/private use.
*   **PDF Generation**: Exports all generated content into a formatted PDF, including Braille sections.
*   **Comparison Tool**: Side-by-side comparison of OpenAI vs. Local LLM performance.

---

## 🛠️ Tech Stack

*   **Language**: Python 3.10+
*   **Frontend**: Streamlit
*   **Backend**: Python (Modular Agents)
*   **LLM Providers**: OpenAI API, Ollama (Local)
*   **Audio Processing**: `SpeechRecognition`, `openai-whisper`, `vosk`, `pydub`, `ffmpeg`
*   **PDF**: `reportlab`

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/siddsahu17/SparshVaani.git
cd SparshVaani
```

### 2. Set Up Virtual Environment
It is recommended to use a virtual environment.
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Install External Tools
*   **FFmpeg**: Required for audio processing. Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your system PATH.
*   **Ollama**: Required for local LLM inference. Download from [ollama.com](https://ollama.com/).
    *   Pull a model: `ollama pull mistral`

### 5. Environment Configuration
Create a `.env` file in the `backend/` directory:
```bash
# backend/.env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🖥️ Usage

Run the Streamlit applications from the project root.

### 1. Main Study Agent (OpenAI default)
The primary interface for generating study materials.
```bash
streamlit run backend/streamlit/agent.py
```

### 2. Local Agent (Ollama)
Run the workflow entirely locally using Ollama.
```bash
streamlit run backend/streamlit/ollama_agent.py
```

### 3. LLM Comparison Tool
Compare result quality and latency between OpenAI and Ollama.
```bash
streamlit run backend/streamlit/compare_llms.py
```

---

## 📂 Project Structure

```
SparshVaani/
├── backend/
│   ├── agents/                 # Logic for individual agents (summary, notes, etc.)
│   ├── audio/                  # Audio transcription modules (Google, Whisper, Vosk)
│   ├── LLM/                    # LLM Provider abstractions (OpenAI, Ollama)
│   ├── streamlit/              # UI Applications
│   │   ├── agent.py            # Main App
│   │   ├── ollama_agent.py     # Local App
│   │   └── compare_llms.py     # Comparison App
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # API Keys (ignored by git)
├── frontend/                   # (Optional) React/Vite frontend components
└── README.md                   # Project Documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📄 License

This project is open-source.
