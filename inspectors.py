"""Inspection hors-ligne des métadonnées et documents."""
from pathlib import Path

def image_info(path: str) -> dict:
    from PIL import Image, ExifTags
    p = Path(path)
    with Image.open(p) as im:
        data = {"Fichier": str(p), "Format": im.format, "Dimensions": f"{im.width} x {im.height}", "Mode": im.mode}
        try:
            exif = im.getexif()
            data["EXIF"] = {ExifTags.TAGS.get(k, str(k)): str(v)[:500] for k, v in exif.items()}
        except Exception:
            data["EXIF"] = "Aucune donnée EXIF lisible"
    return data

def document_info(path: str) -> dict:
    p = Path(path)
    ext = p.suffix.lower()
    result = {"Fichier": str(p), "Taille (octets)": p.stat().st_size}
    if ext == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(str(p))
        result["Pages"] = len(reader.pages)
        result["Métadonnées"] = {k: str(v) for k, v in (reader.metadata or {}).items()}
        result["Texte"] = "\n".join(page.extract_text() or "" for page in reader.pages)[:20000]
    elif ext == ".docx":
        from docx import Document
        doc = Document(str(p))
        result["Métadonnées"] = {"Auteur": doc.core_properties.author, "Titre": doc.core_properties.title}
        result["Texte"] = "\n".join(x.text for x in doc.paragraphs)[:20000]
    elif ext in (".txt", ".md", ".csv", ".log"):
        result["Texte"] = p.read_text(encoding="utf-8", errors="replace")[:20000]
    else:
        raise ValueError("Format non pris en charge. Formats : PDF, DOCX, TXT, MD, CSV, LOG.")
    return result

def audio_info(path: str) -> dict:
    from mutagen import File as MutagenFile
    audio = MutagenFile(path)
    if audio is None:
        raise ValueError("Format audio non reconnu par Mutagen")
    return {"Fichier": str(path), "Durée (s)": round(audio.info.length, 2) if audio.info else "inconnue", "Tags": {str(k): str(v)[:500] for k, v in (audio.tags or {}).items()}}
