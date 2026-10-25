"""Check that all narration takes exist, have signal, and fit the brief."""

import json
import wave
from pathlib import Path

import numpy as np


root = Path(__file__).resolve().parents[1]
meta = json.loads((root / "audio_meta.json").read_text(encoding="utf-8"))
assert len(meta["voices"]) == 22
total = 0.0
rms_values = []
for item in meta["voices"]:
    path = root / item["path"]
    assert path.is_file() and path.stat().st_size > 10_000, path
    with wave.open(str(path), "rb") as stream:
        samples = np.frombuffer(stream.readframes(stream.getnframes()), dtype="<i2")
        actual = len(samples) / stream.getframerate()
    assert abs(actual - item["duration_s"]) < 0.02, item["id"]
    rms = float(np.sqrt(np.mean(samples.astype(np.float32) ** 2)) / 32768)
    assert rms > .005, (item["id"], rms)
    rms_values.append(rms)
    total += actual + .45

assert total < 300, total
print(f"22 takes; timeline {total:.2f}s; RMS {min(rms_values):.3f}–{max(rms_values):.3f}")
