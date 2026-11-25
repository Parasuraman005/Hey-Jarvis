
import json
import queue
import threading
import time

import sounddevice as sd
from vosk import Model, KaldiRecognizer

from config import SAMPLE_RATE, MAX_LISTEN_SECONDS, VOSK_MODEL_PATH


class SpeechToText:

    def __init__(self):

        print("[STT] Loading Vosk model...")

        self.model = Model(str(VOSK_MODEL_PATH))
        self.audio_queue = queue.Queue()

        self.silence_limit = 1.5
        self.block_size = 4000

        print("[STT] Speech recognition ready.")

    # ==========================================
    # AUDIO CALLBACK
    # ==========================================

    def audio_callback(self, indata, frames, time_info, status):

        if status:
            print("[AUDIO]", status)

        self.audio_queue.put(bytes(indata))

    # ==========================================
    # CLEAR AUDIO QUEUE
    # ==========================================

    def clear_queue(self):

        while True:

            try:
                self.audio_queue.get_nowait()

            except queue.Empty:
                break

    # ==========================================
    # SPEECH RECOGNITION
    # ==========================================

    def listen(self, stop_event=None):
        """
        Listen to the microphone and convert speech into text.

        stop_event:
            Optional threading.Event for dashboard stop control.

        Returns:
            Recognized text as a string.
            None if no speech is recognized or stop is requested.
        """

        if stop_event is None:
            stop_event = threading.Event()

        if stop_event.is_set():
            return None

        self.clear_queue()

        recognizer = KaldiRecognizer(
            self.model,
            SAMPLE_RATE
        )

        print("\n[JARVIS] Listening...")

        start_time = time.monotonic()
        last_speech_time = None
        recognized_text = ""

        try:

            with sd.RawInputStream(
                samplerate=SAMPLE_RATE,
                blocksize=self.block_size,
                dtype="int16",
                channels=1,
                callback=self.audio_callback
            ):

                while (
                    time.monotonic() - start_time < MAX_LISTEN_SECONDS
                    and not stop_event.is_set()
                ):

                    try:

                        audio = self.audio_queue.get(timeout=0.2)

                    except queue.Empty:
                        continue

                    # ----------------------------------
                    # FINAL RECOGNITION
                    # ----------------------------------

                    if recognizer.AcceptWaveform(audio):

                        result = json.loads(
                            recognizer.Result()
                        )

                        text = result.get("text", "").strip()

                        if text:

                            recognized_text = (
                                recognized_text + " " + text
                            ).strip()

                            last_speech_time = time.monotonic()

                    # ----------------------------------
                    # PARTIAL RECOGNITION
                    # ----------------------------------

                    else:

                        partial_result = json.loads(
                            recognizer.PartialResult()
                        )

                        partial = partial_result.get(
                            "partial", ""
                        ).strip()

                        if partial:
                            last_speech_time = time.monotonic()

                    # ----------------------------------
                    # SILENCE DETECTION
                    # ----------------------------------

                    if (
                        last_speech_time is not None
                        and time.monotonic() - last_speech_time
                        >= self.silence_limit
                    ):

                        print("[STT] Silence detected.")
                        break

            # --------------------------------------
            # STOP REQUEST
            # --------------------------------------

            if stop_event.is_set():

                print("[STT] Listening stopped.")
                return None

            # --------------------------------------
            # FINAL RESULT
            # --------------------------------------

            final_result = json.loads(
                recognizer.FinalResult()
            )

            final_text = final_result.get(
                "text", ""
            ).strip()

            if final_text:

                recognized_text = (
                    recognized_text + " " + final_text
                ).strip()

            # --------------------------------------
            # RETURN RESULT
            # --------------------------------------

            if recognized_text:

                print(f"[USER] {recognized_text}")

                return recognized_text

            print("[STT] No speech recognized.")

            return None

        except Exception as error:

            print(f"[STT ERROR] {error}")

            return None

        finally:

            self.clear_queue()
