import os
import re
import sys

PATTERNS = {
    "anthropic": r"sk-ant-[A-Za-z0-9_-]{20,}",
    "github": r"ghp_[A-Za-z0-9]{36}",
    "aws": r"AKIA[0-9A-Z]{16}",
}

DOSSIERS_IGNORES = {".git", ".venv", "__pycache__", "node_modules"}
FICHIERS_IGNORES = {".env"}  # ignoré par Git, il contient légitimement la vraie clé


def scan_file(chemin):
    alertes = 0
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            for numero, ligne in enumerate(f, start=1):
                for nom, motif in PATTERNS.items():
                    if re.search(motif, ligne):
                        print(f"{chemin} ligne {numero} : règle {nom}")
                        alertes += 1
    except (UnicodeDecodeError, OSError):
        pass  # fichier binaire ou illisible : on l'ignore
    return alertes


def scan_directory(chemin_racine="."):
    """Parcourt un dossier et ses sous-dossiers, renvoie le nombre de secrets trouvés."""
    total = 0
    for dossier, sous_dossiers, fichiers in os.walk(chemin_racine):
        # On retire les dossiers à ignorer : os.walk n'y descendra pas
        sous_dossiers[:] = [d for d in sous_dossiers if d not in DOSSIERS_IGNORES]
        for nom in fichiers:
            if nom in FICHIERS_IGNORES:
                continue
            total += scan_file(os.path.join(dossier, nom))
    return total


if __name__ == "__main__":
    nb = scan_directory(".")
    if nb > 0:
        print(f"{nb} secret(s) détecté(s). Commit bloqué.")
        sys.exit(1)
    print("Aucun secret détecté.")
    sys.exit(0)