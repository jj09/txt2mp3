# txt2mp3

Simple python script to convert txt files to mp3.

Created it to convert Wardley Maps book by Simon Wardley to mp3.

[Existing audiobook](https://learnwardleymapping.com/book/) uses pretty old voice models, and sounds very unnatural which makes it hard to listen.

## Prereq

python3

```
pip install edge_tts
pip install asyncio
```

## Usage

Put input `.txt` files in `files` directory.

```
python txt2mp3.py
```

Output `.mp3` files will be created in `output` directory.

