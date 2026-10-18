from __future__ import annotations
import json
from pathlib import Path
from . import hashes, inspectors, stego

def show(value):
    print(json.dumps(value, ensure_ascii=False, indent=2, default=str))

def ask_path(prompt="Chemin du fichier : "):
    return input(prompt).strip().strip('"').strip("'")

def run():
    while True:
        print("\n=== HashDesk — boîte à outils locale ===")
        print("1. Identifier un hash (indicatif)   2. Calculer le hash d’un fichier")
        print("3. Convertir texte/Base64/Hex/URL   4. Lire les métadonnées d’une image")
        print("5. Analyser PDF/DOCX/TXT             6. Lire les tags audio")
        print("7. Cacher un message dans PNG         8. Extraire un message d’un PNG")
        print("9. Cacher un message dans WAV         10. Extraire un message d’un WAV")
        print("0. Quitter")
        choice = input("Choix : ").strip()
        try:
            if choice == "0":
                return
            elif choice == "1":
                print("Résultat indicatif :", ", ".join(hashes.identify(input("Hash : "))))
            elif choice == "2":
                path = ask_path(); alg = input("Algorithme (sha256 par défaut) : ").strip() or "sha256"
                print(f"{alg}: {hashes.hash_file(path, alg)}")
            elif choice == "3":
                print("1 Base64 encoder | 2 Base64 décoder | 3 Hex encoder | 4 Hex décoder | 5 URL encoder | 6 URL décoder")
                mode = input("Mode : ").strip(); print(hashes.convert(input("Texte : "), mode))
            elif choice == "4":
                show(inspectors.image_info(ask_path()))
            elif choice == "5":
                show(inspectors.document_info(ask_path()))
            elif choice == "6":
                show(inspectors.audio_info(ask_path()))
            elif choice in ("7", "9"):
                source = ask_path("Fichier source (PNG ou WAV) : ")
                output = ask_path("Fichier de sortie : ")
                message = input("Message à cacher : ")
                (stego.hide_image if choice == "7" else stego.hide_wav)(source, output, message)
                print("Message intégré dans", output)
            elif choice in ("8", "10"):
                path = ask_path()
                print((stego.reveal_image if choice == "8" else stego.reveal_wav)(path))
            else:
                print("Choix invalide")
        except Exception as exc:
            print(f"Erreur : {exc}")

def main():
    run()
