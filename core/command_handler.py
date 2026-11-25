
class CommandHandler:

    def __init__(self, brain, speaker):
        self.brain = brain
        self.speaker = speaker

    def process(self, command):

        if not command:
            return

        normalized = command.lower().strip()

        # Exit command
        exit_commands = [
            "shutdown jarvis",
            "stop listening",
            "goodbye jarvis",
            "exit jarvis"
        ]

        if normalized in exit_commands:
            self.speaker.speak("Goodbye. Shutting down.")
            return "EXIT"

        # Basic assistant controls
        if normalized in ["hello jarvis", "hi jarvis"]:
            self.speaker.speak("Hello! How can I help you?")
            return "CONTINUE"

        if normalized in ["thank you", "thanks jarvis"]:
            self.speaker.speak("You're welcome.")
            return "CONTINUE"

        # Send other commands to AI
        print("[BRAIN] Processing command...")

        answer = self.brain.think(command)

        self.speaker.speak(answer)

        return "CONTINUE"
