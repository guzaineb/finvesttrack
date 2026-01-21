# Suivi du Backlog FinvestTrack

## Sprint 0: Setup & Architecture (CRITIQUE)
- [x] US-001: Setup projet Django avec DRF 
- [x] US-002: Architecture SOLID 

## Sprint 1: Gestion des Utilisateurs (HAUTE)
- [x] US-003: Création de compte 
- [x] US-004: Authentification JWT

## Sprint 2: Gestion des Actifs (HAUTE)
- [x] US-005: Ajouter un actif 
- [x] US-006: Lister les actifs
- [x] US-007: Détail d'un actif 

## Sprint 3: Calculs & Analytics (MOYENNE)
- [ ] US-008: Valeur totale 
- [ ] US-009: Performance globale 

## Rétrospective
### Ce qui a bien fonctionné:
- Application réussie des patterns Factory et Strategy
- Séparation claire des responsabilités
- Tests unitaires couvrant les services métier

### Difficultés rencontrées:
- Configuration initiale de JWT avec DRF
- Gestion des dépendances circulaires

### Améliorations possibles:
- Ajouter plus de tests d'intégration
- Implémenter le caching pour les calculs