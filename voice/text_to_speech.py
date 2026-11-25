
import pyttsx3

from config import TTS_RATE, TTS_VOLUME


class TextToSpeech:

    def __init__(self):

        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", TTS_RATE)
        self.engine.setProperty("volume", TTS_VOLUME)

        self.engine.setProperty("voice", self.get_voice())

        print("[TTS] Voice engine initialized.")

    def get_voice(self):

        voices = self.engine.getProperty("voices")

        if not voices:
            return None

        # Prefer an English voice
        for voice in voices:
            if "english" in voice.name.lower():
                return voice.id

        return voices[0].id

    def speak(self, text):

        if not text:
            return

        print(f"\n[JARVIS] {text}")

        try:
            self.engine.say(text)
            self.engine.runAndWait()

        except Exception as error:
            print(f"[TTS ERROR] {error}")

    def stop(self):
        self.engine.stop()
