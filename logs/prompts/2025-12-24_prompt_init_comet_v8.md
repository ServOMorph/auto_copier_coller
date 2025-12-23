# Log modification prompt_init_comet.md - v8

**Date** : 2025-12-24

## Problèmes identifiés

1. Section "Recherche web" redondante avec les règles de concision déjà établies
2. Gameplay limité aux mécaniques de base (clic, générateurs, prestige)
3. Manque d'éléments interactifs dynamiques pour maintenir l'engagement

## Modifications appliquées

### Suppression

**Avant** :
```markdown
## Recherche web

**DÉSACTIVÉE.** Ne fais jamais de recherche web sauf si W1 demande explicitement une information technique introuvable dans le contexte.
```

**Après** : Section supprimée (règles déjà couvertes dans "Règles de concision")

### Ajout étape 10 : Éléments cliquables bonus

**Avant** :
```markdown
| Étape | Description |
|-------|-------------|
| 10 | Polish UI (animations, feedbacks) |
```

**Après** :
```markdown
| Étape | Description |
|-------|-------------|
| 10 | **Éléments cliquables bonus** (style Cookie Clicker / Paperclips) |
| 11 | Polish UI (animations, feedbacks) |
```

### Nouvelle section ajoutée

Proposition détaillée pour les éléments cliquables avec :
- Concept général
- 4 types d'éléments (étoile dorée, pièce bonus, cristal prestige, éclair)
- Spécifications techniques d'implémentation

## Résultat attendu

- Prompt plus concis sans redondance
- Nouvelle mécanique de gameplay engageante
- Comet guidé pour implémenter les éléments cliquables en étape 10

## Checklist de tests

- [ ] Comet comprend la nouvelle étape 10
- [ ] Comet n'effectue pas de recherches web
- [ ] Les éléments cliquables sont implémentés correctement
- [ ] Timing d'apparition/disparition fonctionnel
- [ ] Bonus appliqués correctement au clic
