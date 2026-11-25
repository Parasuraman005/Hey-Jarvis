
import requests

from config import (
    AI_BACKEND,
    FASTAPI_URL,
    OLLAMA_URL,
    OLLAMA_MODEL,
    AI_TIMEOUT,
    MAX_HISTORY
)


class JARVISBrain:

    def __init__(self):

        self.history = []

    def build_prompt(self, question):

        conversation = ""

        for item in self.history[-MAX_HISTORY:]:
            conversation += (
                f"User: {item['user']}\n"
                f"JARVIS: {item['assistant']}\n"
            )

        return (
            "You are JARVIS, a helpful local desktop AI assistant. "
            "Answer clearly, naturally and concisely. "
            "Do not claim to have performed actions you have not performed.\n\n"
            f"{conversation}"
            f"User: {question}\n"
            "JARVIS:"
        )

    def ask_fastapi(self, prompt):

        response = requests.post(
            FASTAPI_URL,
            json={"question": prompt},
            timeout=AI_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, str):
            return data

        if isinstance(data, dict):

            for key in ("response", "answer", "reply", "result"):
                if isinstance(data.get(key), str):
                    return data[key]

        raise ValueError(
            "Unexpected FastAPI response format: "
            + str(data)
        )

    def ask_ollama(self, prompt):

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=AI_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "")

    def think(self, question):

        try:

            prompt = self.build_prompt(question)

            if AI_BACKEND.lower() == "fastapi":
                answer = self.ask_fastapi(prompt)

            elif AI_BACKEND.lower() == "ollama":
                answer = self.ask_ollama(prompt)

            else:
                raise ValueError("Unknown AI backend.")

            answer = answer.strip()

            if not answer:
                return "I could not generate a response."

            self.history.append({
                "user": question,
                "assistant": answer
            })

            self.history = self.history[-MAX_HISTORY:]

            return answer

        except requests.exceptions.ConnectionError:
            return (
                "I cannot connect to my local AI server. "
                "Please check whether the server is running."
            )

        except requests.exceptions.Timeout:
            return "My AI server is taking too long to respond."

        except Exception as error:
            print(f"[BRAIN ERROR] {error}")
            return "Sorry, I encountered an AI processing error."
