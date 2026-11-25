
import json
import queue
import time

import sounddevice as sd
from vosk import Model, KaldiRecognizer

from config import SAMPLE_RATE, MAX_LISTEN_SECONDS, VOSK_MODEL_PATH


class SpeechToText:

    def __init__(self):
        print("[STT] Loading Vosk model...")

        self.model = Model(str(VOSK_MODEL_PATH))
        self.audio_queue = queue.Queue()

        print("[STT] Speech recognition ready.")

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print("[AUDIO]", status)

        self.audio_queue.put(bytes(indata))

    def clear_queue(self):
        while True:
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break

    def listen(self):

        self.clear_queue()

        recognizer = KaldiRecognizer(
            self.model,
            SAMPLE_RATE
        )

        print("\n[JARVIS] Listening...")
        start_time = time.monotonic()
        last_speech_time = None
        silence_limit = 1.5
        recognized_text = ""

        try:
            with sd.RawInputStream(
                samplerate=SAMPLE_RATE,
                blocksize=4000,
                dtype="int16",
                channels=1,
                callback=self.audio_callback
            ):

                while time.monotonic() - start_time < MAX_LISTEN_SECONDS:

                    try:
                        audio = self.audio_queue.get(timeout=0.5)
                    except queue.Empty:
                        continue

                    if recognizer.AcceptWaveform(audio):
                        result = json.loads(recognizer.Result())
                        text = result.get("text", "").strip()

                        if text:
                            recognized_text = (
                                recognized_text + " " + text
                            ).strip()

                            last_speech_time = time.monotonic()

                    else:
                        partial = json.loads(
                            recognizer.PartialResult()
                        ).get("partial", "").strip()

                        if partial and last_speech_time is None:
                            last_speech_time = time.monotonic()

                    if (
                        last_speech_time is not None
                        and time.monotonic() - last_speech_time
                        >= silence_limit
                    ):
                        break

            final_result = json.loads(recognizer.FinalResult())
            final_text = final_result.get("text", "").strip()

            if final_text:
                recognized_text = (
                    recognized_text + " " + final_text
                ).strip()

            if recognized_text:
                print(f"[USER] {recognized_text}")
                return recognized_text

            print("[STT] No speech recognized.")
            return None

        except Exception as error:
            print(f"[STT ERROR] {error}")
            return None
