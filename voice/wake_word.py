
import json
import queue
from pathlib import Path
from config import VOSK_MODEL_PATH
import sounddevice as sd
from vosk import Model, KaldiRecognizer


# ==========================================
# CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "vosk-model"

SAMPLE_RATE = 16000
BLOCK_SIZE = 8000

WAKE_WORDS = ["jarvis", "hey jarvis"]


# ==========================================
# AUDIO QUEUE
# ==========================================

audio_queue = queue.Queue()


def audio_callback(indata, frames, time, status):
    """Receive microphone audio."""

    if status:
        print("[AUDIO]", status)

    audio_queue.put(bytes(indata))


# ==========================================
# WAKE WORD ENGINE
# ==========================================

class WakeWordDetector:

    def __init__(self):

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Vosk model not found: {MODEL_PATH}"
            )

        print("[JARVIS] Loading offline voice model...")

        self.model = Model(str(MODEL_PATH))

        grammar = json.dumps(WAKE_WORDS)

        self.recognizer = KaldiRecognizer(
            self.model,
            SAMPLE_RATE,
            grammar
        )

        print("[JARVIS] Wake word engine initialized.")


    def listen(self):
        """Continuously listen for the wake word."""

        print("\n[JARVIS] Waiting for wake word...")
        print('[JARVIS] Say "Hey JARVIS" to activate.')

        while True:

            audio_data = audio_queue.get()

            if self.recognizer.AcceptWaveform(audio_data):

                result = json.loads(
                    self.recognizer.Result()
                )

                recognized_text = result.get(
                    "text", ""
                ).lower().strip()

                if recognized_text:
                    print("[VOICE]", recognized_text)

                    if "jarvis" in recognized_text.split():

                        print("\n[JARVIS] Wake word detected!")

                        return True


# ==========================================
# START LISTENING
# ==========================================

def listen_for_wake_word():

    detector = WakeWordDetector()

    # Remove stale audio before starting
    while not audio_queue.empty():
        audio_queue.get_nowait()

    try:

        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            dtype="int16",
            channels=1,
            callback=audio_callback
        ):

            return detector.listen()

    except KeyboardInterrupt:
        print("\n[JARVIS] Wake detection stopped.")
        return False

    except Exception as error:
        print(f"[JARVIS] Microphone error: {error}")
        return False

def wait_for_wake_word():
    """
    Block until Hey JARVIS is detected.
    Return True when detected.
    """
    
# ==========================================
# DIRECT TEST
# ==========================================

if __name__ == "__main__":

    print("================================")
    print("       JARVIS WAKE ENGINE       ")
    print("================================")

    while True:

        activated = listen_for_wake_word()

        if activated:
            print("[JARVIS] ACTIVATED SUCCESSFULLY!")
            break
