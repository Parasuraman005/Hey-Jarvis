import sounddevice as sd
import numpy as np

print("Available microphones:")
print(sd.query_devices())

print("\nRecording for 5 seconds... Speak now!")

audio = sd.rec(
    int(5 * 16000),
    samplerate=16000,
    channels=1,
    dtype="int16"
)

sd.wait()

volume = np.max(np.abs(audio))

print("Recording completed.")
print("Maximum microphone volume:", volume)

if volume > 500:
    print("SUCCESS: Microphone is receiving audio.")
else:
    print("WARNING: No or very low microphone input detected.")
