# Log modification prompt_init_comet.md

**Date** : 2024-12-24
**Version** : v1

## Problèmes identifiés

- Comet continuait à inclure des références web `[1]`, `[2]` et des URLs malgré les interdictions explicites
- Paradoxe : mentionner "websearch" dans les règles attire l'attention du modèle sur cette fonctionnalité
- Trop de règles négatives (JAMAIS, ZÉRO, INTERDIT) = confusion

## Modifications appliquées

### Avant (RÈGLE ABSOLUE)
```markdown
## RÈGLE ABSOLUE

**Tu ne dois JAMAIS inclure** :
- Des références numérotées `[1]`, `[2]`, etc.
- Des URLs ou liens hypertextes
- Des résultats de recherche web

Ces éléments polluent les échanges et gaspillent des tokens.
```

### Après (RÈGLE DE CONCISION)
```markdown
## RÈGLE DE CONCISION

Tes réponses doivent être **minimalistes** :
- Uniquement le format V5 requis
- Aucun contenu superflu
- Maximum 5 lignes par réponse (hors format V5)
```

### Avant (Règles de concision STRICT)
```markdown
## Règles de concision (STRICT)

**CRITIQUE - VIOLATION = ÉCHEC** :
- **ZÉRO référence web** : Aucun `[1]`, `[2]`, URL, ou lien hypertexte
- **ZÉRO recherche web** pour les validations d'étapes.

**Format obligatoire** :
- Après confirmation W1 : `✓ Étape N validée.` + message V5. **Rien d'autre.**
```

### Après (Format de réponse obligatoire)
```markdown
## Format de réponse obligatoire

Après confirmation W1 :
✓ Étape N validée.
[Message V5 suivant]

**Rien d'autre.** Pas de paraphrase, pas d'explications.
```

### Supprimé
- Section "Format de transition strict" (redondante)

## Résultat attendu

- Comet ne pense plus au websearch car non mentionné
- Réponses plus courtes et focalisées sur le format V5
- Moins de règles = moins de confusion

## Checklist de tests

- [ ] Envoyer un message à Comet et vérifier absence de `[1]`, `[2]`, URLs
- [ ] Vérifier que les réponses sont courtes (< 5 lignes hors V5)
- [ ] Vérifier respect du format `✓ Étape N validée.` + V5
