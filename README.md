# ConvoLens AI

ConvoLens AI is a local-first AI meeting and video assistant that turns YouTube links or audio files into rich transcripts, smart summaries, key points, and improvement suggestions using AssemblyAI and a local LLM via LM Studio. [web:1076][web:1082]

---

## Features

- YouTube and local audio/video support: paste a YouTube URL or upload a file. [web:1076]
- Accurate transcription using AssemblyAI speech-to-text API. [web:1082]
- Local LLM analysis via LM Studio’s OpenAI-compatible `/v1` API (Phi‑3). [web:849][web:888]
- Smart summary, key points, and actionable improvement suggestions for the content.
- Clean Streamlit web UI that runs entirely on your laptop.

---

## Architecture

YouTube URL / Audio File
│
▼
AssemblyAI STT (API)
│
▼
Transcript
│
▼
LM Studio (local LLM, OpenAI-compatible)
│
▼
Smart Summary - Key Points - Improvements
│
▼
Streamlit Frontend

text

- STT: AssemblyAI for transcription from audio/video to text. [web:1082]
- LLM: Small local model (e.g. Phi‑3-mini ) served through LM Studio OpenAI-compatible server. [web:849][web:1014]
- Frontend: Streamlit app (`app.py`) providing a simple interface. [web:1076]

---

## Setup & Configuration

### 1. Clone the repository

git clone https://github.com/pavishnu152/ConvoLens-AI.git
cd ConvoLens-AI

text

### 2. Python environment and dependencies

python -m venv .venv
.venv\Scripts\activate # On Windows

pip install -r requirements.txt

text

### 3. AssemblyAI configuration

1. Create a free account at https://www.assemblyai.com and get your API key from the dashboard. [web:1082]
2. In the project root, create a `.env` file and add:

ASSEMBLYAI_API_KEY=YOUR_ASSEMBLYAI_KEY_HERE

text

### 4. LM Studio configuration (local LLM)

1. Install LM Studio from https://lmstudio.ai and open it. [web:1111]
2. Download a small text model, for example:
   - `Phi-3-mini-4k-instruct` (GGUF) [web:1014]
3. Load the chosen model in LM Studio.
4. Open the **Developer / Local Server** panel and start the **OpenAI-compatible API** server. Note the Base URL, for example:
   - `http://192.168.43.122:1234/v1` [web:849]
5. In your browser, open:

http://192.168.43.122:1234/v1/models

text

Find your model in the JSON and copy its `"microsoft/Phi-3-mini-4k-instruct-gguf

"` value exactly. [web:1112]

6. Add these lines to your `.env` (adjust for your IP and model id):

LMSTUDIO_BASE_URL=http://192.168.43.122:1234/v1
LMSTUDIO_API_KEY=lm-studio
LMSTUDIO_MODEL=microsoft/Phi-3-mini-4k-instruct-gguf

text

Use the exact model id you copied from `/v1/models`, not the example above. [web:1112]

---

## Run the App

With the virtual environment activated and `.env` configured:

python -m streamlit run app.py

text

Then open the URL shown in the terminal (usually `http://192.168.43.122:8501`) in your browser. [web:1059]

Usage:

1. Choose either **YouTube URL** or **Upload file**.
2. Paste a YouTube link or upload an audio/video file (start with 10–30 seconds).
3. Click **Analyze**.
4. View the transcript, smart summary, key points, and smart improvement suggestions in the UI.

---

## Screenshots and Demo (optional but recommended)

After you have the app running:

1. Take a screenshot of the main UI (showing input and generated summary) using `Win + Shift + S` on Windows and save it as `assets/convolens-ui.png`. [web:1048]
2. Add this to the README:

UI Screenshot
![ConvoLens UI](

text

3. Record a short screen capture demo (15–60 seconds) using a screen recorder (Xbox Game Bar or OBS), upload it to YouTube or Drive, and add a link:

Demo Video
Watch the demo

text

Commit and push the updated README and assets:

git add README.md assets/convolens-ui.png
git commit -m "Add UI screenshot and demo link"
git push

text

---

## Tech Stack

- Python
- Streamlit
- AssemblyAI (speech-to-text API) [web:1082]
- LM Studio (OpenAI-compatible local LLM server) [web:849]
- Local models: Phi‑3-mini / Qwen2.5‑3B Instruct (GGUF) [web:1014][web:1024]
- httpx, python-dotenv, and other utility libraries

---

## Why This Project

This project demonstrates:

- Designing and implementing an end‑to‑end AI application (data ingestion → transcription → LLM analysis → UI). [web:1076]
- Integrating cloud STT with a local LLM served through an OpenAI-compatible API. [web:849][web:888]
- Handling configuration via environment variables and local servers.
- Building a practical tool for meetings, lectures, and content creators who want fast summaries and feedback.

It is intended as a portfolio project for AI engineering roles and can be extended with features like transcript chunking, multi-language support, or cloud deployment in future versions.