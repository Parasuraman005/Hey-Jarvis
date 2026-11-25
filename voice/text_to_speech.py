
import pyttsx3
import threading

from config import TTS_RATE, TTS_VOLUME


class TextToSpeech:

    def __init__(self):

        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", TTS_RATE)
        self.engine.setProperty("volume", TTS_VOLUME)

        self.muted = False
        self.lock = threading.RLock()

        self.engine.setProperty("voice", self.get_voice())

        print("[TTS] Voice engine initialized.")

    def get_voice(self):

        voices = self.engine.getProperty("voices")

        if not voices:
            return None

        for voice in voices:
            if "english" in voice.name.lower():
                return voice.id

        return voices[0].id

    def speak(self, text):

        if not text or self.muted:
            return

        print(f"\n[JARVIS] {text}")

        try:
            with self.lock:
                if not self.muted:
                    self.engine.say(text)
                    self.engine.runAndWait()

        except Exception as error:
            print(f"[TTS ERROR] {error}")

    def set_mute(self, muted):
        """Enable or disable voice output."""

        self.muted = bool(muted)

        if self.muted:
            self.stop()

        print(
            "[TTS] Muted." if self.muted else "[TTS] Unmuted."
        )

    def stop(self):

        try:
            with self.lock:
                self.engine.stop()

        except Exception as error:
            print(f"[TTS STOP ERROR] {error}")
