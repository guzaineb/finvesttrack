# Architecture du Projet FinvesTrack

## Vue d'ensemble
L'architecture suit une approche modulaire avec séparation claire des responsabilités, basée sur les principes SOLID.

## Structure des Modules

### 1. Couche Modèles (Models)
**Responsabilité** : Représentation des données et logique métier basique  
**Exemple** : `Asset`, `Portfolio`, `User`  
**Principe** : Single Responsibility  
**Emplacement** : `apps/portfolio/models.py`

### 2. Couche Services (Services)
**Responsabilité** : Logique métier complexe  
**Sous-modules** :
- `interfaces.py` : Contrats abstraits
- `repositories.py` : Accès aux données (Repository Pattern)
- `calculators.py` : Algorithmes de calcul financier
- `portfolio_service.py` : Orchestration métier
- `asset_factory.py` : Création d'objets (Factory Pattern)

**Design Patterns** : Strategy, Repository, Factory  
**Emplacement** : `apps/portfolio/services/`

### 3. Couche API (Views/Serializers)
**Responsabilité** : Gestion des requêtes HTTP  
**Exemple de vues** :
- `AssetViewSet` : CRUD complet des actifs
- `PortfolioSummaryView` : Résumé consolidé
- `PortfolioPerformanceView` : Calculs de performance

**Principe** : Thin Controllers (logique déléguée aux services)  
**Emplacement** : `apps/portfolio/views.py`, `apps/portfolio/serializers.py`

### 4. Couche Infrastructure
**Responsabilité** : Configuration globale  
**Composants** :
- `settings.py` : Configuration Django
- `urls.py` : Routes API
- Middleware d'authentification

**Emplacement** : `config/`

### 5. Couche Tests
**Structure des tests** :

**Types de tests** :
- **Unitaires** : Models, Services, Calculs
- **Intégration** : Vues API, Repositories
- **Outils** : pytest, pytest-django, coverage

**Emplacement** : `apps/portfolio/tests/`, `tests/`