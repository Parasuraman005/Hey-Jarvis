
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="JARVIS AI API")

class AskRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "JARVIS API is running"}

@app.post("/ask")
def ask(request: AskRequest):
    try:
        from core.brain import ask_ollama

        answer = ask_ollama(request.message)

        return {"response": answer}

    except Exception as error:
        return {"error": str(error)}
