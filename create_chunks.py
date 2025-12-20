import whisper
import json
import os
from pathlib import Path

# load the model (change to "large-v2" if you want highest accuracy)
model = whisper.load_model("medium")

audios_dir = Path("audios")
jsons_dir = Path("jsons")
jsons_dir.mkdir(parents=True, exist_ok=True)

for audio_file in audios_dir.iterdir():
    if "_" not in audio_file.name:
        continue

    number, rest = audio_file.stem.split("_", 1)   # split once only
    title = rest                                   # full title without extension

    print(number, title)

    # transcribe (translate Hindi → English since task="translate")
    result = model.transcribe(
        str(audio_file),
        language="hi",
        task="translate",
        word_timestamps=False
    )

    # build chunks
    chunks = [
        {
            "number": number,
            "title": title,
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"],
        }
        for seg in result["segments"]
    ]

    chunks_with_metadata = {"chunks": chunks, "text": result["text"]}

    out_file = jsons_dir / f"{number}_{title}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(chunks_with_metadata, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {out_file}")