import json
import queue
import sounddevice as sd
from config import VOSK_MODEL_PATH
from vosk import Model, KaldiRecognizer
from pathlib import Path


class JarvisListener:

    def __init__(self):
        self.sample_rate = 16000
        self.audio_queue = queue.Queue()

        model_path = (
            Path(__file__).resolve().parent.parent
            / "models"
            / "vosk-model"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"Vosk model not found: {model_path}"
            )

        print("Loading JARVIS speech model...")

        self.model = Model(str(model_path))

        self.recognizer = KaldiRecognizer(
            self.model,
            self.sample_rate
        )

        print("JARVIS listening engine ready.")

    def audio_callback(self, indata, frames, time, status):
        if status:
            print("Audio status:", status)

        self.audio_queue.put(bytes(indata))

    def listen(self):
        print("\nListening... Speak now.")

        self.recognizer.Reset()

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self.audio_callback
        ):

            while True:
                data = self.audio_queue.get()

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(
                        self.recognizer.Result()
                    )

                    text = result.get("text", "").strip()

                    if text:
                        print("YOU:", text)
                        return text
