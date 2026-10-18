"""Stéganographie LSB simple pour fichiers personnels : PNG et WAV PCM."""
from pathlib import Path

MAGIC = b"HDSK1"

def _bits(data: bytes):
    for byte in data:
        for shift in range(7, -1, -1):
            yield (byte >> shift) & 1

def _bytes(bits):
    out = bytearray()
    for i in range(0, len(bits) - 7, 8):
        value = 0
        for bit in bits[i:i + 8]:
            value = (value << 1) | int(bit)
        out.append(value)
    return bytes(out)

def _payload(message: str) -> bytes:
    raw = message.encode("utf-8")
    return MAGIC + len(raw).to_bytes(4, "big") + raw

def _extract(data: bytes) -> str:
    if not data.startswith(MAGIC) or len(data) < 9:
        raise ValueError("Aucun message HashDesk détecté")
    size = int.from_bytes(data[5:9], "big")
    if size > len(data) - 9:
        raise ValueError("Message intégré incomplet ou fichier altéré")
    return data[9:9 + size].decode("utf-8")

def hide_image(source: str, output: str, message: str) -> None:
    from PIL import Image
    import numpy as np
    with Image.open(source) as im:
        if im.format != "PNG":
            raise ValueError("Utilisez un PNG en entrée pour éviter la perte par compression")
        arr = np.array(im.convert("RGB"))
        payload = _payload(message)
        bits = list(_bits(payload))
        flat = arr.reshape(-1)
        if len(bits) > flat.size:
            raise ValueError(f"Message trop long : capacité d'environ {flat.size // 8 - 9} octets")
        flat[:len(bits)] = (flat[:len(bits)] & 0xFE) | bits
        Image.fromarray(arr).save(output, format="PNG")

def reveal_image(path: str) -> str:
    from PIL import Image
    import numpy as np
    with Image.open(path) as im:
        flat = np.array(im.convert("RGB")).reshape(-1)
    # Lire l'en-tête puis uniquement le nombre de bits indiqué.
    header = _bytes((flat[:72] & 1).tolist())
    if not header.startswith(MAGIC):
        raise ValueError("Aucun message HashDesk détecté")
    size = int.from_bytes(header[5:9], "big")
    end = (9 + size) * 8
    return _extract(_bytes((flat[:end] & 1).tolist()))

def hide_wav(source: str, output: str, message: str) -> None:
    import wave
    with wave.open(source, "rb") as w:
        if w.getsampwidth() != 2 or w.getcomptype() != "NONE":
            raise ValueError("Seuls les WAV PCM 16 bits non compressés sont pris en charge")
        params, frames = w.getparams(), bytearray(w.readframes(w.getnframes()))
    payload = _payload(message)
    bits = list(_bits(payload))
    if len(bits) > len(frames):
        raise ValueError("Message trop long pour ce fichier WAV")
    for i, bit in enumerate(bits):
        frames[i] = (frames[i] & 0xFE) | bit
    with wave.open(output, "wb") as w:
        w.setparams(params)
        w.writeframes(frames)

def reveal_wav(path: str) -> str:
    import wave
    with wave.open(path, "rb") as w:
        frames = w.readframes(w.getnframes())
    header = _bytes([x & 1 for x in frames[:72]])
    if not header.startswith(MAGIC):
        raise ValueError("Aucun message HashDesk détecté")
    size = int.from_bytes(header[5:9], "big")
    return _extract(_bytes([x & 1 for x in frames[:(9 + size) * 8]]))
