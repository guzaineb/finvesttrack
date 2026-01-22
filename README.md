# FinvestTrack - Suivi de Portefeuille d'Investissement

## 📋 Description
Application de suivi de portefeuille d'investissement avec Django REST Framework, conçue pour les investisseurs individuels et les professionnels.

## 🏗️ Stack Technique
| Composant | Technologie |
|-----------|-------------|
| **Backend** | Python 3.10+, Django 4.2+ |
| **API** | Django REST Framework |
| **Base de données** | SQLite  |
| **Authentification** | JWT via djangorestframework-simplejwt |
| **Tests** | pytest + pytest-django |
| **Documentation** | drf-spectacular (Swagger) |
|

## 🚀 Fonctionnalités principales
- ✅ **Gestion de portefeuille** - Suivi des actifs et performances
- ✅ **Authentification sécurisée** - JWT pour une connexion sécurisée
- ✅ **Documentation interactive** - Swagger
- ✅ **Tests complets** - Couverture de code et tests automatisés
- ✅ **Architecture modulaire** - Séparation des responsabilités

## 📥 Installation & Démarrage

### 1. Cloner le projet
```bash
# Cloner le dépôt via HTTPS
git clone https://github.com/guzaineb/finvesttrack.git
cd finvesttrack

# Ou via SSH
git clone git@github.com:guzaineb/finvesttrack.git
cd finvesttrack


# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Windows:
venv\Scripts\activate
# Sur Mac/Linux:
source venv/bin/activate

# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur (optionnel)
python manage.py createsuperuser

# Démarrer le serveur
python manage.py runserver

Swagger UI : http://localhost:8000/api/docs/

# Tous les tests avec couverture
pytest --cov=. --cov-report=term-missing --cov-report=html

# Tests avec verbosité
pytest -v

# Tests d'un module spécifique
pytest apps/portfolio/tests/    # Tests du module portfolio
pytest apps/users/tests/        # Tests d'authentification

# Tests avec rapport HTML
pytest --cov=. --cov-report=html
