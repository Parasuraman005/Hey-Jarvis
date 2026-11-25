import pyttsx3


class JarvisSpeaker:

    def __init__(self):
        self.engine = pyttsx3.init("sapi5")

        self.engine.setProperty("rate", 175)
        self.engine.setProperty("volume", 1.0)

        voices = self.engine.getProperty("voices")

        if voices:
            self.engine.setProperty("voice", voices[0].id)

    def speak(self, text):
        print(f"\nJARVIS: {text}")

        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == "__main__":
    jarvis = JarvisSpeaker()
    jarvis.speak("Hello! I am Jarvis. My voice system is online.")
