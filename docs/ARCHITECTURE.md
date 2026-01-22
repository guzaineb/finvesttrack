
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
  - `asset_factory.py`: Création d'objets

### 3. Couche API (Views/Serializers)
- **Responsabilité**: Gestion des requêtes HTTP
- **Exemple**: `AssetViewSet`, `PortfolioSummaryView`
- **Principe**: Thin Controllers (logique métier déléguée aux services)

### 4. Couche Infrastructure (Configuration)
- **Responsabilité**: Configuration, URLs, middleware
- **Exemple**: `settings.py`, `urls.py`

