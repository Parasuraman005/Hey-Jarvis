
import threading
import queue


class AssistantBridge:

    def __init__(self, assistant_runner):

        self.assistant_runner = assistant_runner

        self.events = queue.Queue()

        self.running = False
        self.thread = None

    def emit(self, event, data=None):

        self.events.put({
            "event": event,
            "data": data
        })

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self.thread.start()

    def _run(self):

        try:
            self.emit("status", "standby")

            self.assistant_runner(self.emit)

        except Exception as error:

            self.emit("error", str(error))

        finally:

            self.running = False
            self.emit("status", "stopped")

    def stop(self):

        self.running = False

        # The actual voice engine must also receive
        # a stop signal to release microphone resources.
