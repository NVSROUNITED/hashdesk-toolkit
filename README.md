# HashDesk Toolkit

A **local** Python toolbox with a modular command-line menu. It is intended for inspection and learning with files you own or are authorized to analyze.

## Features

- Identify common hash formats by length (indicative only) and calculate hashes for files or text (SHA-256 by default).
- Encode/decode text as Base64, hexadecimal, or URL encoding.
- Read image dimensions and EXIF metadata.
- Extract text and metadata from PDF, DOCX, and text files.
- Display audio duration and tags supported by Mutagen.
- Hide/extract a UTF-8 message using LSB steganography in PNG and 16-bit PCM WAV files.

**Important:** A hash is not encrypted text. Hash functions are designed to be one-way: this project does not “decode” hashes and does not include password cracking or dictionary/brute-force features. Identification by length does not prove which algorithm was used. LSB steganography is educational and fragile (re-encoding may destroy the message); it does not provide encryption. Do not use it to protect sensitive data.

## Installation (Linux/macOS)

```bash
git clone https://github.com/YOUR-USERNAME/hashdesk-toolkit.git
cd hashdesk-toolkit
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[media]'
hashdesk
```

If the `hashdesk` command is unavailable, run `python -m hashdesk`. The `media` extra enables image, PDF, DOCX, and audio-tag features. Python 3.10 or later is required. The program does not upload files; all operations are performed locally.

## Windows (PowerShell)

```powershell
git clone https://github.com/YOUR-USERNAME/hashdesk-toolkit.git
cd hashdesk-toolkit
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -e ".[media]"
hashdesk
```

## Format limitations

- **Images:** Pillow can read supported image formats, but steganographic encoding requires a PNG input.
- **Documents:** PDF, DOCX, TXT, MD, CSV, and LOG. Scanned PDFs require OCR, which is not included.
- **Audio:** Metadata inspection uses Mutagen; steganography is limited to uncompressed 16-bit PCM WAV files.
- Be cautious when opening suspicious files on a sensitive machine. Metadata may contain private information such as GPS coordinates, device details, or author names.

## Contributing

Contributions are welcome, including automated tests, optional OCR, additional formats, and a graphical interface. Please open an issue before making major changes. Do not add features for credential cracking or unauthorized access.

## License

MIT — see `LICENSE`.
