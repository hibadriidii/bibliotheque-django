import json
import urllib.request
import urllib.error
from django.conf import settings
from livres.models import Livre


def get_library_context():
    """Génère le contexte de la bibliothèque pour le prompt IA."""
    livres = Livre.objects.all()
    if not livres.exists():
        return "La bibliothèque est actuellement vide."

    lines = ["=== CATALOGUE DE LA BIBLIOTHÈQUE ===\n"]
    for livre in livres:
        retour = f", retour prévu le {livre.date_retour_prevu.strftime('%d/%m/%Y')}" if livre.date_retour_prevu else ""
        lines.append(
            f"ID:{livre.id} | Titre: {livre.titre} | Auteur: {livre.auteur} | "
            f"Catégorie: {livre.categorie} | Année: {livre.annee_publication} | "
            f"Statut: {livre.get_statut_display_fr()} | Quantité: {livre.quantite_disponible}{retour}"
        )

    return "\n".join(lines)


def build_system_prompt():
    context = get_library_context()
    return f"""Tu es un assistant intelligent pour une bibliothèque. Tu dois répondre en français aux questions des utilisateurs sur les livres disponibles.

{context}

Règles importantes :
- Réponds TOUJOURS en français
- Consulte le catalogue ci-dessus pour répondre avec des données réelles
- Si un livre est emprunté, indique la date de retour prévue si disponible
- Propose des recommandations basées sur le catalogue existant
- Sois précis, amical et utile
- Si le livre n'existe pas dans le catalogue, dis-le clairement
- Pour les recommandations, base-toi sur la catégorie et le style des livres disponibles
"""


def call_anthropic(user_message):
    """Appel à l'API Anthropic Claude."""
    api_key = settings.ANTHROPIC_API_KEY
    if not api_key or api_key == 'your-anthropic-api-key-here':
        return None, "Clé API Anthropic non configurée. Veuillez définir ANTHROPIC_API_KEY dans settings.py."

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1024,
        "system": build_system_prompt(),
        "messages": [{"role": "user", "content": user_message}]
    }

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data['content'][0]['text'], None
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        return None, f"Erreur API Anthropic ({e.code}): {body}"
    except Exception as e:
        return None, f"Erreur de connexion: {str(e)}"


def call_gemini(user_message):
    """Appel à l'API Google Gemini."""
    api_key = settings.GEMINI_API_KEY
    if not api_key or api_key == 'your-gemini-api-key-here':
        return None, "Clé API Gemini non configurée. Veuillez définir GEMINI_API_KEY dans settings.py."

    system_prompt = build_system_prompt()
    full_message = f"{system_prompt}\n\nQuestion de l'utilisateur: {user_message}"

    payload = {
        "contents": [{"parts": [{"text": full_message}]}],
        "generationConfig": {"maxOutputTokens": 1024}
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data['candidates'][0]['content']['parts'][0]['text'], None
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        return None, f"Erreur API Gemini ({e.code}): {body}"
    except Exception as e:
        return None, f"Erreur de connexion: {str(e)}"


def get_chatbot_response(user_message):
    """Point d'entrée principal — choisit le provider selon les settings."""
    provider = getattr(settings, 'AI_PROVIDER', 'anthropic')

    if provider == 'gemini':
        response, error = call_gemini(user_message)
    else:
        response, error = call_anthropic(user_message)

    if error:
        return f"⚠️ {error}"
    return response
