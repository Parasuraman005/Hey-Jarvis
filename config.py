
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Application
ASSISTANT_NAME = "JARVIS"
WAKE_WORD = "hey jarvis"

# Speech recognition
SAMPLE_RATE = 16000
MAX_LISTEN_SECONDS = 15
VOSK_MODEL_PATH = BASE_DIR / "models" / "vosk-model"

# AI configuration
AI_BACKEND = "ollama"

FASTAPI_URL = "http://127.0.0.1:8000/ask"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

OLLAMA_MODEL = "smollm2:1.7b"

AI_TIMEOUT = 120

# Text to speech
TTS_RATE = 175
TTS_VOLUME = 1.0

# Conversation
MAX_HISTORY = 10

# Memory
MEMORY_FILE = BASE_DIR / "assistant_memory.json"
