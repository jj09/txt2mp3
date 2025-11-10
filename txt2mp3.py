import asyncio
import edge_tts
from pathlib import Path
import sys
from typing import Dict

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
VOICE       = "en-US-BrandonNeural"     # Best for Simon Wardley
INPUT_DIR   = "files"
OUTPUT_DIR  = "output" + f"({VOICE})"
# =============================

# ANSI escape codes
CLEAR_LINE = "\r\033[K"
MOVE_UP = "\033[A"

async def convert_file(txt_file: Path, status_dict: Dict[str, str], lock: asyncio.Lock, output_path: Path):
    filename = txt_file.name
    mp3_file = output_path / txt_file.with_suffix(".mp3").name

    # Set status
    async with lock:
        status_dict[filename] = "⏳PROCESSING"

    text = txt_file.read_text(encoding="utf-8").strip()
    if not text:
        async with lock:
            status_dict[filename] = "⚠️SKIPPED (empty)"
        return

    # Generate audio
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(str(mp3_file))

    # Mark complete
    async with lock:
        status_dict[filename] = "✅COMPLETE"

async def print_status(status_dict: Dict[str, str], lock: asyncio.Lock, input_path: Path, output_path: Path):
    lines = []
    dots = 0
    while True:
        async with lock:
            current = status_dict.copy()

        # Clear previous lines
        for _ in range(len(lines)):
            sys.stdout.write(MOVE_UP + CLEAR_LINE)
        sys.stdout.flush()

        # Build new output
        lines = []
        print("TXT 2 MP3 Conversion")
        print(f"Input  → {input_path}/")
        print(f"Output → {output_path}/")
        print("-" * 80)

        for filename, status in current.items():
            status_str = status = f"{status}{'.' * dots}" if status == "⏳PROCESSING" else status
            line = f"{filename:<60} {status_str}"
            lines.append(line)
            print(line)

        if not lines:
            print(f"No .txt files found in {INPUT_DIR} folder.")
            print("   Add files and rerun.")
        print("-" * 80)
        sys.stdout.flush()

        # update dots for processing animation
        dots = (dots+1) % 6

        await asyncio.sleep(1)

async def main():
    # Setup directories
    input_path = Path(INPUT_DIR)
    output_path = Path(OUTPUT_DIR)
    input_path.mkdir(exist_ok=True)
    output_path.mkdir(exist_ok=True)

    # Find .txt files
    txt_files = sorted(input_path.glob("*.txt"))
    if not txt_files:
        print(f"No .txt files in '{INPUT_DIR}/'")
        print(f"   Add files and run again.")
        return

    status_dict = {f.name: "☕️WAITING" for f in txt_files}
    lock = asyncio.Lock()

    # Start live printer
    printer_task = asyncio.create_task(print_status(status_dict, lock, input_path, output_path))

    # Convert all in parallel
    tasks = [convert_file(f, status_dict, lock, output_path) for f in txt_files]
    await asyncio.gather(*tasks)

    # Final update
    await asyncio.sleep(1)
    printer_task.cancel()

    print(f"\nAll done! MP3s saved in: {output_path}/")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user.")