# FinvestTrack - Suivi de Portefeuille d'Investissement

## Description
Application de suivi de portefeuille d'investissement avec Django REST Framework.

## Stack Technique
- **Backend**: Python 3.10+, Django 4.2+
- **API**: Django REST Framework
- **Base de données**: SQLite 
- **Authentification**: JWT(djangorestframework-simplejwt)
- **Tests**: pytest + pytest-django
- **Documentation**: drf-spectacular (Swagger)


## Installation
1. Cloner le projet
2. Créer un environnement virtuel: `python -m venv venv`
3. Activer l'environnement
4. Installer les dépendances: `pip install -r requirements.txt`
5. Configurer les variables d'environnement: `cp .env.example .env`
6. Appliquer les migrations: `python manage.py migrate`
7. Lancer le serveur: `python manage.py runserver`

## API Documentation
Accédez à la documentation Swagger: `http://localhost:8000/api/docs/`