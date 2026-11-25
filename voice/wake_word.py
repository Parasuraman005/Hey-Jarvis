import json
import queue
import threading
from pathlib import Path

import sounddevice as sd
from vosk import Model, KaldiRecognizer

from config import VOSK_MODEL_PATH


# ==========================================
# CONFIGURATION
# ==========================================

SAMPLE_RATE = 16000
BLOCK_SIZE = 8000

WAKE_WORDS = ["jarvis", "hey jarvis"]

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = Path(VOSK_MODEL_PATH)

if not MODEL_PATH.is_absolute():
    MODEL_PATH = BASE_DIR / MODEL_PATH


# ==========================================
# AUDIO QUEUE
# ==========================================

audio_queue = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    """Receive microphone audio."""

    if status:
        print("[AUDIO]", status)

    audio_queue.put(bytes(indata))


def clear_audio_queue():
    """Remove old microphone audio."""

    while True:
        try:
            audio_queue.get_nowait()
        except queue.Empty:
            break


# ==========================================
# WAKE WORD DETECTOR
# ==========================================

class WakeWordDetector:

    def __init__(self):

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Vosk model not found: {MODEL_PATH}"
            )

        print("[JARVIS] Loading offline voice model...")

        self.model = Model(str(MODEL_PATH))

        self.grammar = json.dumps(WAKE_WORDS)

        self.recognizer = self.create_recognizer()

        print("[JARVIS] Wake word engine initialized.")

    def create_recognizer(self):
        """Create a fresh recognizer using the loaded model."""

        return KaldiRecognizer(
            self.model,
            SAMPLE_RATE,
            self.grammar
        )

    def listen(self, stop_event=None):
        """
        Listen for the wake word.

        Returns:
            True  - Wake word detected.
            False - Stop requested or microphone error.
        """

        if stop_event is None:
            stop_event = threading.Event()

        self.recognizer = self.create_recognizer()

        clear_audio_queue()

        print("\n[JARVIS] Waiting for wake word...")
        print('[JARVIS] Say "Hey JARVIS" to activate.')

        try:
            with sd.RawInputStream(
                samplerate=SAMPLE_RATE,
                blocksize=BLOCK_SIZE,
                dtype="int16",
                channels=1,
                callback=audio_callback
            ):

                while not stop_event.is_set():

                    try:
                        audio_data = audio_queue.get(timeout=0.2)

                    except queue.Empty:
                        continue

                    if self.recognizer.AcceptWaveform(audio_data):

                        result = json.loads(
                            self.recognizer.Result()
                        )

                        recognized_text = result.get(
                            "text", ""
                        ).lower().strip()

                        if recognized_text:

                            print("[VOICE]", recognized_text)

                            words = recognized_text.split()

                            if "jarvis" in words:

                                print(
                                    "\n[JARVIS] Wake word detected!"
                                )

                                return True

            print("[JARVIS] Wake detection stopped.")
            return False

        except Exception as error:

            print(f"[JARVIS] Microphone error: {error}")
            return False


# ==========================================
# REUSABLE DETECTOR
# ==========================================

_detector = None
_detector_lock = threading.Lock()


def get_detector():
    """Load the Vosk model only once."""

    global _detector

    with _detector_lock:

        if _detector is None:
            _detector = WakeWordDetector()

        return _detector


# ==========================================
# MAIN WAKE WORD FUNCTION
# ==========================================

def wait_for_wake_word(stop_event=None):
    """
    Wait until Hey JARVIS is detected.

    Returns:
        True  - Wake word detected.
        False - Stop requested or an error occurred.
    """

    if stop_event is None:
        stop_event = threading.Event()

    if stop_event.is_set():
        return False

    try:
        detector = get_detector()

        return detector.listen(stop_event)

    except Exception as error:

        print(f"[JARVIS WAKE ERROR] {error}")
        return False


# ==========================================
# DIRECT TEST
# ==========================================

if __name__ == "__main__":

    print("=" * 40)
    print("       JARVIS WAKE ENGINE")
    print("=" * 40)

    stop_event = threading.Event()

    try:

        while not stop_event.is_set():

            activated = wait_for_wake_word(stop_event)

            if activated:
                print("[JARVIS] ACTIVATED SUCCESSFULLY!")
                break

    except KeyboardInterrupt:

        print("\n[JARVIS] Wake detection stopped.")
        stop_event.set()