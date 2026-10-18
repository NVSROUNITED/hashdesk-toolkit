"""Fonctions de hashage et conversions d'encodage."""
from __future__ import annotations
import hashlib
import re
from pathlib import Path

PATTERNS = [
    ("MD5 (possible)", re.compile(r"^[a-fA-F0-9]{32}$")),
    ("SHA-1 (possible)", re.compile(r"^[a-fA-F0-9]{40}$")),
    ("SHA-224 (possible)", re.compile(r"^[a-fA-F0-9]{56}$")),
    ("SHA-256 (possible)", re.compile(r"^[a-fA-F0-9]{64}$")),
    ("SHA-384 (possible)", re.compile(r"^[a-fA-F0-9]{96}$")),
    ("SHA-512 (possible)", re.compile(r"^[a-fA-F0-9]{128}$")),
]

def identify(value: str) -> list[str]:
    value = value.strip()
    found = [name for name, pattern in PATTERNS if pattern.fullmatch(value)]
    return found or ["Format non reconnu parmi les formats courants (résultat indicatif)."]

def hash_file(path: str, algorithm: str = "sha256") -> str:
    if algorithm not in hashlib.algorithms_available:
        raise ValueError(f"Algorithme indisponible : {algorithm}")
    digest = hashlib.new(algorithm)
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def hash_text(text: str, algorithm: str = "sha256") -> str:
    return hashlib.new(algorithm, text.encode("utf-8")).hexdigest()

def convert(text: str, mode: str) -> str:
    import base64
    if mode == "1":
        return base64.b64encode(text.encode()).decode()
    if mode == "2":
        return base64.b64decode(text, validate=True).decode("utf-8")
    if mode == "3":
        return text.encode().hex()
    if mode == "4":
        return bytes.fromhex(text).decode("utf-8")
    if mode == "5":
        from urllib.parse import quote
        return quote(text, safe="")
    if mode == "6":
        from urllib.parse import unquote
        return unquote(text)
    raise ValueError("Choix de conversion invalide")
