
from voice.wake_word import wait_for_wake_word
from voice.speech_to_text import SpeechToText
from voice.text_to_speech import TextToSpeech

from core.brain import JARVISBrain
from core.command_handler import CommandHandler

from memory.memory_manager import MemoryManager

from vosk import Model
model = Model("models/vosk-model")

from config import VOSK_MODEL_PATH
model = Model(str(VOSK_MODEL_PATH))
def main():

    print("=" * 50)
    print("                 J.A.R.V.I.S")
    print("          VOICE ASSISTANT SYSTEM")
    print("=" * 50)

    speaker = None

    try:

        print("\n[JARVIS] Initializing...")

        speaker = TextToSpeech()
        stt = SpeechToText()
        brain = JARVISBrain()
        memory = MemoryManager()

        handler = CommandHandler(brain, speaker)

        speaker.speak("JARVIS is online.")

        while True:

            print("\n[JARVIS] Waiting for Hey JARVIS...")

            if not wait_for_wake_word():
                continue

            print("[WAKE] Hey JARVIS detected.")

            speaker.speak("Yes, I'm listening.")

            command = stt.listen()

            if not command:
                speaker.speak("I didn't hear anything. Try again.")
                continue

            print(f"[COMMAND] {command}")

            result = handler.process(command)

            if result == "EXIT":
                break

            # Save the latest interaction
            if brain.history:
                latest = brain.history[-1]

                if latest["user"] == command:
                    memory.add_conversation(
                        latest["user"],
                        latest["assistant"]
                    )

            print("[STATUS] Interaction completed.")

    except KeyboardInterrupt:
        print("\n[JARVIS] Stopping...")

    except Exception as error:
        print(f"\n[JARVIS ERROR] {error}")

    finally:

        if speaker:
            speaker.stop()

        print("[JARVIS] Goodbye!")


if __name__ == "__main__":
    main()
