# 📚 Bibliothèque Intelligente avec Chatbot IA
**Projet Semestriel Python — iTeam University 2025–2026**

Application Django de gestion de bibliothèque avec chatbot IA (Anthropic Claude ou Google Gemini).

---

## 🚀 Installation et lancement

### 1. Prérequis
- Python 3.10 ou supérieur

### 2. Cloner / décompresser le projet
```bash
cd bibliotheque
```

### 3. Créer un environnement virtuel (recommandé)
```bash
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows
```

### 4. Installer Django
```bash
pip install -r requirements.txt
```

### 5. Configurer la clé API IA
Ouvrez `bibliotheque/settings.py` et renseignez votre clé :

**Option A — Anthropic Claude (recommandé par le projet)**
```python
ANTHROPIC_API_KEY = 'sk-ant-...'  # Votre vraie clé
AI_PROVIDER = 'anthropic'
```

**Option B — Google Gemini (gratuit sur ai.google.dev)**
```python
GEMINI_API_KEY = 'AIza...'        # Votre vraie clé
AI_PROVIDER = 'gemini'
```

### 6. Créer la base de données
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. (Optionnel) Peupler avec des données d'exemple
```bash
python seed_data.py
```

### 8. Créer un compte administrateur
```bash
python manage.py createsuperuser
```

### 9. Lancer le serveur
```bash
python manage.py runserver
```

Ouvrir : **http://127.0.0.1:8000**

---

## 📁 Structure du projet

```
bibliotheque/
├── bibliotheque/          # Configuration Django
│   ├── settings.py        # ⚙️  Config + clés API
│   └── urls.py
├── livres/                # App CRUD livres
│   ├── models.py          # Modèle Livre
│   ├── views.py           # Vues CRUD
│   ├── forms.py           # Formulaires
│   ├── urls.py
│   └── templates/livres/
│       ├── liste.html
│       ├── detail.html
│       ├── formulaire.html
│       └── confirmer_suppression.html
├── chatbot/               # App Chatbot IA
│   ├── views.py
│   ├── services.py        # 🤖 Logique IA (Anthropic / Gemini)
│   ├── urls.py
│   └── templates/chatbot/
│       └── chatbot.html
├── templates/
│   └── base.html          # Template de base (navigation, style)
├── manage.py
├── seed_data.py           # Données d'exemple
└── requirements.txt
```

---

## 🎯 Fonctionnalités

### CRUD Livres
- ✅ Ajouter un livre (titre, auteur, catégorie, année, quantité, statut)
- ✅ Afficher tous les livres avec statistiques
- ✅ Modifier un livre
- ✅ Supprimer un livre
- ✅ Recherche par titre, auteur ou ID
- ✅ Filtrage par catégorie et statut

### Chatbot IA
- ✅ Vérifier l'existence d'un livre par ID
- ✅ Vérifier la disponibilité d'un livre
- ✅ Recommandations personnalisées
- ✅ Recherche par auteur
- ✅ Le chatbot consulte la vraie base de données

---

## 🔧 Technologies utilisées

| Composant | Technologie |
|-----------|-------------|
| Backend | Django 4.2 |
| Base de données | SQLite (sqlite3) |
| Interface | Django Templates + CSS personnalisé |
| API IA | Anthropic Claude / Google Gemini |
| Authentification | Django Admin |

---

## 👨‍💻 Interface Admin

Accessible sur : **http://127.0.0.1:8000/admin/**

Permet de gérer les livres directement depuis l'interface d'administration Django.
