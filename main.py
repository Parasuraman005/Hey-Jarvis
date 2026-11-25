
import threading

from voice.wake_word import wait_for_wake_word
from voice.speech_to_text import SpeechToText
from voice.text_to_speech import TextToSpeech

from core.brain import JARVISBrain
from core.command_handler import CommandHandler

from memory.memory_manager import MemoryManager


def send_event(emit, event, data=None):
    if emit:
        emit(event, data)


def run_assistant(emit=None, stop_event=None):

    if stop_event is None:
        stop_event = threading.Event()

    speaker = None

    try:
        print("=" * 50)
        print("                 J.A.R.V.I.S")
        print("          VOICE ASSISTANT SYSTEM")
        print("=" * 50)

        send_event(emit, "status", "initializing")
        print("\n[JARVIS] Initializing...")

        # Initialize components
        speaker = TextToSpeech()
        send_event(emit, "tts_ready", speaker)

        stt = SpeechToText()
        brain = JARVISBrain()
        memory = MemoryManager()

        handler = CommandHandler(brain, speaker)

        if stop_event.is_set():
            return

        speaker.speak("JARVIS is online.")

        send_event(emit, "status", "waiting")

        # Main assistant loop
        while not stop_event.is_set():

            print("\n[JARVIS] Waiting for Hey JARVIS...")
            send_event(emit, "status", "waiting")

            activated = wait_for_wake_word(stop_event)

            if not activated or stop_event.is_set():
                break

            print("[WAKE] Hey JARVIS detected.")

            send_event(emit, "status", "listening")

            speaker.speak("Yes, I'm listening.")

            if stop_event.is_set():
                break

            command = stt.listen(stop_event)

            if stop_event.is_set():
                break

            if not command:
                speaker.speak("I didn't hear anything. Try again.")
                send_event(emit, "status", "waiting")
                continue

            print(f"[COMMAND] {command}")

            send_event(emit, "user_message", command)
            send_event(emit, "status", "thinking")

            result = handler.process(command)

            if result == "EXIT":
                send_event(emit, "status", "stopped")
                break

            # Save the latest conversation
            if brain.history:
                latest = brain.history[-1]

                if latest.get("user") == command:

                    assistant_response = latest.get("assistant", "")

                    memory.add_conversation(
                        latest["user"],
                        assistant_response
                    )

                    if assistant_response:
                        send_event(
                            emit,
                            "assistant_message",
                            assistant_response
                        )

            print("[STATUS] Interaction completed.")

            send_event(emit, "status", "waiting")

    except KeyboardInterrupt:
        print("\n[JARVIS] Stopping...")
        stop_event.set()

    except Exception as error:
        print(f"\n[JARVIS ERROR] {error}")
        send_event(emit, "error", str(error))

    finally:
        if speaker:
            speaker.stop()

        send_event(emit, "status", "stopped")
        print("[JARVIS] Goodbye!")


def main():

    stop_event = threading.Event()

    try:
        run_assistant(stop_event=stop_event)

    except KeyboardInterrupt:
        stop_event.set()


if __name__ == "__main__":
    main()
