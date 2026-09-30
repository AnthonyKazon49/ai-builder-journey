# ai-builder-journey/hello_claude.py
"""Premier appel à l'API Claude : preuve que le poste de travail est prêt."""

import os
import sys

import anthropic
from dotenv import load_dotenv

# 1. Charger les variables du fichier .env dans l'environnement
load_dotenv()

# 2. Vérifier que la clé est présente, sans jamais l'afficher
if not os.getenv("ANTHROPIC_API_KEY"):
    sys.exit("Erreur : ANTHROPIC_API_KEY introuvable. Vérifie ton fichier .env.")

# 3. Créer le client (il lit la clé tout seul dans l'environnement)
client = anthropic.Anthropic()

# 4. Envoyer la question
try:
    reponse = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": "Dis bonjour à Anthony, qui démarre aujourd'hui son parcours d'AI Builder, en deux phrases.",
            }
        ],
    )
except anthropic.AuthenticationError:
    sys.exit("Erreur : clé refusée. Elle est peut-être mal copiée, révoquée ou expirée.")
except anthropic.APIError as erreur:
    sys.exit(f"Erreur de l'API : {erreur}")

# 5. Extraire et afficher le texte de la réponse
print(reponse.content[0].text)

# 6. Afficher la consommation : ton premier réflexe de chiffrage client
print(f"\nTokens envoyés : {reponse.usage.input_tokens} | Tokens reçus : {reponse.usage.output_tokens}")
