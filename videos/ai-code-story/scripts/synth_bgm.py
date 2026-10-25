"""Make a quiet original electronic bed for the narration."""

import json
import math
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np


root = Path(__file__).resolve().parents[1]
shots = json.loads((root / "shot-plan.json").read_text(encoding="utf-8"))
metadata_path = root / "audio_meta.json"
if metadata_path.exists():
    voice_items = json.loads(metadata_path.read_text(encoding="utf-8")).get("voices", [])
    duration = sum(float(item["duration_s"]) + .45 for item in voice_items) + 5
else:
    duration = sum(max(6.4, len(x["voice"]) / 4.5 + 1.2) for x in shots) + 5
rate = 22050
length = math.ceil(duration * rate)
audio = np.zeros(length, dtype=np.float32)

# Four broad chords; the sparse pulses provide motion without competing with speech.
chords = [
    (110.00, 130.81, 164.81),
    (87.31, 130.81, 174.61),
    (130.81, 164.81, 196.00),
    (98.00, 146.83, 196.00),
]
block = 8.0
for start in np.arange(0, duration, block):
    left = int(start * rate)
    right = min(length, int((start + block) * rate))
    t = np.arange(right - left, dtype=np.float32) / rate
    chord = chords[int(start // block) % 4]
    fade_in = np.minimum(1, t / 1.7)
    fade_out = np.minimum(1, (right - left - np.arange(right - left)) / (rate * 1.4))
    env = np.minimum(fade_in, fade_out)
    pad = sum(np.sin(2 * np.pi * f * t) + .16 * np.sin(4 * np.pi * f * t) for f in chord)
    slow = .86 + .14 * np.sin(2 * np.pi * .18 * t)
    audio[left:right] += .024 * pad * env * slow

for start in np.arange(.35, duration, 1.6):
    left = int(start * rate)
    right = min(length, left + int(.32 * rate))
    t = np.arange(right - left, dtype=np.float32) / rate
    pulse = np.sin(2 * np.pi * 82 * t) * np.exp(-15 * t)
    audio[left:right] += .020 * pulse

fade = min(int(2.4 * rate), length // 2)
audio[:fade] *= np.linspace(0, 1, fade)
audio[-fade:] *= np.linspace(1, 0, fade)
audio = np.clip(audio, -.95, .95)

out = root / "assets" / "audio" / "original-bed.mp3"
out.parent.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory() as folder:
    wav_file = Path(folder) / "bed.wav"
    with wave.open(str(wav_file), "wb") as stream:
        stream.setnchannels(1)
        stream.setsampwidth(2)
        stream.setframerate(rate)
        stream.writeframes((audio * 32767).astype("<i2").tobytes())
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(wav_file), "-codec:a", "libmp3lame", "-b:a", "128k", str(out)], check=True)
print(out)
