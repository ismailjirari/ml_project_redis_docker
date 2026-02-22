# 🧠 Sentence Embedding API

Une application complète de génération d'embeddings de phrases utilisant des modèles Sentence Transformers, avec une API FastAPI, un cache Redis et une interface React moderne.

---

## 📋 Table des matières

- [Aperçu du projet](#-aperçu-du-projet)
- [Architecture](#-architecture)
- [Fonctionnalités](#-fonctionnalités)
- [Prérequis](#-prérequis)
- [Installation et démarrage](#-installation-et-démarrage)
- [Utilisation de l'API](#-utilisation-de-lapi)
- [Interface Frontend](#-interface-frontend)
- [Cache Redis](#-cache-redis)
- [Structure du projet](#-structure-détaillée)
- [Déploiement avec Docker](#-déploiement-avec-docker)
- [Dépannage](#-dépannage)
- [Tutoriel vidéo](#-tutoriel-vidéo)

---

## 🎯 Aperçu du projet

Cette application permet de :

- Générer des embeddings (vecteurs) à partir de phrases
- Utiliser différents modèles Sentence Transformers
- Mettre en cache les résultats avec Redis pour des performances optimales
- Visualiser les embeddings générés via une interface React
- Interagir avec l'API RESTful FastAPI

---

## 🏗 Architecture

```
ml/
├── backend/                  # API FastAPI
│   ├── app/                  # Code source backend
│   │   ├── config.py         # Configuration
│   │   ├── database.py       # Gestion Redis
│   │   ├── ml_service.py     # Service d'embeddings
│   │   ├── models.py         # Modèles Pydantic
│   │   └── __init__.py
│   ├── models/               # Modèles téléchargés
│   │   └── all-MiniLM-L6-v2/
│   └── Dockerfile
├── frontend/                 # Interface React
│   ├── src/
│   │   ├── App.jsx           # Composant principal
│   │   └── App.css
│   └── Dockerfile
└── docker-compose.yml        # Orchestration des services
```

---

## ✨ Fonctionnalités

- **🔄 Multi-modèles** : Support de plusieurs modèles Sentence Transformers
- **⚡ Cache Redis** : Mise en cache des embeddings pour des réponses plus rapides
- **📊 Interface intuitive** : Frontend React pour visualiser les résultats
- **🔌 API RESTful** : Endpoints clairs et documentés
- **🐳 Docker** : Conteneurisation complète pour un déploiement facile
- **📈 Scalable** : Architecture modulaire et extensible

---

## 📦 Prérequis

- Docker et Docker Compose
- Node.js *(optionnel, pour développement sans Docker)*
- Python 3.11+ *(optionnel, pour développement sans Docker)*
- Redis *(optionnel, géré automatiquement dans Docker)*

---

## 🚀 Installation et démarrage

### Avec Docker (recommandé)

1. **Cloner le projet**

```bash
git clone <url-du-repo>
cd ml
```

2. **Télécharger un modèle** *(si non présent)*

```bash
# Placez vos modèles Sentence Transformers dans backend/models/
mkdir -p backend/models
# Téléchargez et décompressez le modèle dans ce dossier
```

3. **Lancer l'application**

```bash
docker-compose up --build
```

4. **Accéder à l'application**

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| API | http://localhost:8000 |
| Documentation API | http://localhost:8000/docs |

---

### Sans Docker (développement)

**Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

---

## 📡 Utilisation de l'API

### Endpoints disponibles

| Méthode | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Informations de l'API |
| `POST` | `/postageee/` | Créer un embedding |
| `GET` | `/gettage/` | Liste tous les embeddings |
| `GET` | `/models/` | Modèles disponibles |
| `GET` | `/redis-test` | Test connexion Redis |

### Exemples d'utilisation

```bash
# Créer un embedding
curl -X POST "http://localhost:8000/postageee/" \
  -H "Content-Type: application/json" \
  -d '{"phrase": "Hello world", "modelnumber": 1}'

# Récupérer tous les embeddings
curl "http://localhost:8000/gettage/"
```

---

## 💻 Interface Frontend

L'interface React propose :

- 📝 **Formulaire de création** : Entrez vos phrases et choisissez un modèle
- 📋 **Liste des embeddings** : Visualisez tous les embeddings générés
- 🔍 **Détails des vecteurs** : Aperçu et visualisation complète des embeddings
- 🔄 **Rafraîchissement** : Mise à jour en temps réel de la liste
- 📊 **Statut API** : Indicateur de connexion au backend

---

## 🔧 Cache Redis

Le système utilise Redis pour :

- **Mise en cache** : Les embeddings sont stockés avec une clé unique *(hash du texte + modèle)*
- **TTL** : Cache valide 1 heure *(configurable)*
- **Performance** : Évite de recalculer les mêmes embeddings
- **Clés** : Format `embedding:[hash]` et `phrase:[id]`

---

## 📁 Structure détaillée

### Backend (FastAPI)

| Fichier | Rôle |
|---|---|
| `main.py` | Point d'entrée, configuration CORS, routes principales |
| `app/config.py` | Configuration Redis, chemins des modèles |
| `app/database.py` | Gestion Redis et base de données en mémoire |
| `app/ml_service.py` | Service d'embeddings avec cache |
| `app/models.py` | Schémas Pydantic |

### Frontend (React + Vite)

`App.jsx` — Composant principal avec :
- Gestion d'état (`useState`, `useEffect`)
- Appels API `fetch`
- Rendu conditionnel
- Formatage des embeddings

---

## 🐳 Déploiement avec Docker

### `docker-compose.yml`

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - ./backend/models:/app/models
    environment:
      - REDIS_HOST=host.docker.internal  # Windows/Mac
      # - REDIS_HOST=172.17.0.1          # Linux
    networks:
      - ml-network

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend
    networks:
      - ml-network
```

### Configuration Redis

**Windows/Mac :**
```yaml
environment:
  - REDIS_HOST=host.docker.internal
extra_hosts:
  - "host.docker.internal:host-gateway"
```

**Linux :**
```yaml
environment:
  - REDIS_HOST=172.17.0.1
```

---

## 🔍 Dépannage

### Redis non accessible

- Vérifiez que Redis est installé localement
- Testez avec `/redis-test`
- Ajustez `REDIS_HOST` dans `docker-compose.yml`

### Modèles non chargés

- Vérifiez le dossier `backend/models/`
- Les modèles doivent être dans des sous-dossiers

### CORS errors

- Les origines autorisées sont configurées dans `main.py`
- Par défaut : `http://localhost:5173`

### Ports déjà utilisés

```bash
# Vérifier les ports utilisés
netstat -ano | findstr :8000   # Windows
lsof -i :8000                  # Mac/Linux
```

---

## 📹 Tutoriel vidéo

Regardez le tutoriel complet sur Google Drive :

🔗 [Dossier tutoriel vidéo](https://drive.google.com/drive/folders/1Gt88BQ_q6W4w9W9e6-JF-N-TXBfZbJcy)

Le tutoriel couvre :
- Installation et configuration
- Démonstration de l'application
- Explication du code
- Déploiement avec Docker

---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

---

## 📄 Licence

MIT

---

## 👨‍💻 Auteur

Créé avec ❤️ pour la communauté ML/DL

📧 **Support** : Pour toute question, consultez le tutoriel vidéo ou ouvrez une issue sur GitHub.
