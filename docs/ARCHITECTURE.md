
# Architecture du Projet FinvesTrack

## Vue d'ensemble
L'architecture suit une approche modulaire avec séparation claire des responsabilités. Le projet est organisé selon les principes SOLID et utilise plusieurs design patterns.

## Structure des Modules

### 1. Couche Modèles (Models)
- **Responsabilité**: Représentation des données et logique métier basique
- **Exemple**: `Asset`, `User`
- **Principe**: Single Responsibility (chaque modèle représente une entité métier)

### 2. Couche Services (Services)
- **Responsabilité**: Logique métier complexe
- **Sous-modules**:
  - `interfaces.py`: Contrats abstraits
  - `repositories.py`: Accès aux données
  - `calculators.py`: Algorithmes de calcul
  - `portfolio_service.py`: Orchestration métier
  - `asset_factory.py`: Création d'objets en utilisant Factory Pattern 
- **Design Patterns**: Strategy, Repository, Factory, Dependency Injection
- **Emplacement**: `portfolio/services/`
### 3. Couche API (Views/Serializers)
- **Responsabilité**: Gestion des requêtes HTTP
  - `AssetViewSet`: CRUD complet des actifs avec calcul de performance
  - `PortfolioSummaryView`: Résumé consolidé du portefeuille
  - `PortfolioPerformanceView`: Détails de performance avec ROI
- **Principe**: Thin Controllers (logique métier déléguée aux services)
 **Emplacement**: `portfolio/views.py`, `portfolio/serializers.py`

### 4. Couche Infrastructure (Configuration)
- **Responsabilité**: Configuration, URLs, middleware
- **Exemple**: `settings.py`, `urls.py`, authentification Django
- **Emplacement**: `config/`

### 5. Couche Tests
- **Structure**:
tests/
 ├── test_models.py
 ├── test_repository.py
 ├── test_services.py
 ├── test_factory.py
 ├── test_calculators.py
 ├── test_views.py
```


  - `test_calculators.py`: Tests unitaires des algorithmes de calcul
  - `test_repositories.py`: Tests des repositories
  - `test_services.py`: Tests des services métier
  - `test_views.py`: Tests d'intégration des endpoints API
- **Outils**: pytest, pytest-django, coverage
- **Emplacement**: `tests/`, `portfolio/tests/`
