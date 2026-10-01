import re

PATTERNS = {
    "anthropic": r"sk-ant-[A-Za-z0-9_-]{20,}",
    "github": r"ghp_[A-Za-z0-9]{36}",
    "aws": r"AKIA[0-9A-Z]{16}",
}


def scan_file(chemin):
    alertes = 0
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            for numero , ligne in enumerate(f, start=1):
                for nom, motif in PATTERNS.items():
                    if re.search(motif, ligne):
                        print(f"{chemin} ligne {numero} : règle {nom}")
                        alertes += 1
    except UnicodeDecodeError:
        pass  # fichier binaire (image, etc.) : on l'ignore
    return alertes


total = scan_file(r"C:\Users\antho\Projets\test-gitleaks\config.py")
print("Total :", total)
