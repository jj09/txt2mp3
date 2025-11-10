import edge_tts
import asyncio
from pathlib import Path

## Full Voice List from edge_tts

#| Language + Voice Name        | Gender    | Style / Accent            |
#|------------------------------|-----------|---------------------------|
#| **English (US)** ----------------------------------------------------|
#| `en-US-AvaNeural`            | Female    | Warm, clear, modern       |
#| `en-US-EmmaNeural`           | Female    | Bright, energetic         |
#| `en-US-JennyNeural`          | Female    | Friendly, upbeat          |
#| `en-US-MichelleNeural`       | Female    | Calm, professional        |
#| `en-US-SaraNeural`           | Female    | Soft, natural             |
#| `en-US-GuyNeural`            | Male      | Confident, deep           |
#| `en-US-BrandonNeural`        | Male      | Strong, authoritative     |
#| `en-US-ChristopherNeural`    | Male      | Warm, mature              |
#| `en-US-JacobNeural`          | Male      | Clear, friendly           |
#| `en-US-RyanNeural`           | Male      | Casual, youthful          |
#|----------------------------------------------------------------------|
#| **English (UK)** ----------------------------------------------------|
#| `en-GB-SoniaNeural`          | Female    | British, clear, engaging  |
#| `en-GB-LibbyNeural`          | Female    | Soft, elegant             |
#| `en-GB-MaisieNeural`         | Female    | Young, lively             |
#| `en-GB-RyanNeural`           | Male      | Confident British         |
#| `en-GB-ThomasNeural`         | Male      | Deep, authoritative       |

# === CONFIG: CHANGE THESE ===
INPUT_DIR   = "files"
OUTPUT_DIR  = "output"
VOICE       = "en-GB-RyanNeural"     # Best for Simon Wardley
# =============================

async def convert_file(txt_file: Path):
    # Read text
    text = txt_file.read_text(encoding="utf-8").strip()
    if not text:
        print(f"Skipped (empty): {txt_file.name}")
        return

    # Output MP3 = same name, .mp3
    mp3_file = txt_file.with_suffix(".mp3")
    
    print(f"Converting: {txt_file.name} → {mp3_file.name}")
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(str(mp3_file))
    print(f"Done: {mp3_file.name}")


async def main():
    # Find all .txt files in current directory
    txt_files = sorted(Path(INPUT_DIR).glob("*.txt"))
    
    if not txt_files:
        print(f"No .txt files found in '{INPUT_DIR}' folder.")
        print("Put your .txt files in '{INPUT_DIR}' and run again.")
        return

    print(f"Found {len(txt_files)} .txt file(s). Starting conversion...\n")
    await asyncio.gather(*(convert_file(f) for f in txt_files))
    print(f"\nAll done! MP3s are in {OUTPUT_DIR} folder.")

asyncio.run(main())