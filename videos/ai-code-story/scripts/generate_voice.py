"""Generate every Mandarin narration take with one offline Kokoro model load."""

import json
from pathlib import Path

import soundfile as sf
from kokoro_onnx import Kokoro


root = Path(__file__).resolve().parents[1]
plan = json.loads((root / "shot-plan.json").read_text(encoding="utf-8"))
cache = Path.home() / ".cache" / "hyperframes" / "tts"
model = cache / "models" / "kokoro-v1.0.onnx"
voices = cache / "voices" / "voices-v1.0.bin"
if not model.exists() or not voices.exists():
    raise SystemExit("Local Kokoro model or voices file is missing")

engine = Kokoro(str(model), str(voices))
out = root / "assets" / "voice"
out.mkdir(parents=True, exist_ok=True)
entries = []
for number, shot in enumerate(plan, 1):
    shot_id = f"shot{number:02d}"
    samples, sample_rate = engine.create(
        shot["voice"], voice="zf_xiaobei", speed=1.08, lang="cmn"
    )
    path = out / f"{shot_id}.wav"
    sf.write(str(path), samples, sample_rate)
    duration = len(samples) / sample_rate
    entries.append(
        {"id": shot_id, "path": str(path.relative_to(root)).replace("\\", "/"), "duration_s": round(duration, 3)}
    )
    print(f"{shot_id} {duration:.2f}s {shot['voice'][:16]}", flush=True)

meta = {"provider": "kokoro-onnx", "voice": "zf_xiaobei", "lang": "zh", "speed": 1.08, "voices": entries}
(root / "audio_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"total voice duration {sum(item['duration_s'] for item in entries):.2f}s", flush=True)
