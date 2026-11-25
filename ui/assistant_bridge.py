
import threading
import queue


class AssistantBridge:

    def __init__(self, assistant_runner):
        self.assistant_runner = assistant_runner

        self.events = queue.Queue()
        self.running = False
        self.thread = None

        self.stop_event = threading.Event()
        self.speaker = None

        self._lock = threading.Lock()

    def emit(self, event, data=None):
        # Keep the TTS object inside the bridge.
        # Do not send it to the dashboard event queue.
        if event == "tts_ready":
            with self._lock:
                self.speaker = data
            return

        self.events.put({
            "event": event,
            "data": data
        })

    def start(self):
        with self._lock:
            if self.running:
                return

            self.stop_event.clear()
            self.speaker = None
            self.running = True

            self.thread = threading.Thread(
                target=self._run,
                daemon=True
            )
            self.thread.start()

    def _run(self):
        try:
            self.emit("status", "initializing")

            self.assistant_runner(
                self.emit,
                self.stop_event
            )

        except Exception as error:
            self.emit("error", str(error))

        finally:
            with self._lock:
                self.running = False
                self.speaker = None

            self.emit("status", "stopped")

    def stop(self):
        self.stop_event.set()

    def set_muted(self, muted):
        with self._lock:
            speaker = self.speaker

        if speaker is not None:
            speaker.set_mute(muted)

    def is_running(self):
        with self._lock:
            return self.running

    def get_event(self):
        try:
            return self.events.get_nowait()
        except queue.Empty:
            return None
