# Log de modification - prompt_init_comet.md v4

**Date** : 2025-12-23

## Problèmes identifiés

| Problème | Source | Impact |
|----------|--------|--------|
| Références web `[1]`-`[10]` persistantes | Sessions 21:37 et 21:51 | Bruit dans les échanges, tokens gaspillés |
| Règle v2 insuffisante | Analyse croisée | Comet ignore partiellement l'interdiction |
| Recherche web sur validations simples | Session 21:51 | Latence inutile |

## Modifications appliquées

### 1. Section "Règles de concision" renforcée

**Avant** :
```markdown
## Règles de concision

- **Pas de paraphrase** : Ne répète jamais ce que W1 vient de confirmer.
- **Enchaînement direct** : Après confirmation de W1, envoie immédiatement le message V5 de l'étape suivante.
- **Pas de références web** dans les messages inter-agents (supprime les `[1]`, `[2]`, etc.).
```

**Après** :
```markdown
## Règles de concision (STRICT)

- **INTERDIT** : Les références web `[1]`, `[2]`, etc. dans TOUS les messages.
- **INTERDIT** : Les URLs ou liens dans les messages V5.
- **Pas de paraphrase** : Ne répète jamais ce que W1 vient de confirmer.
- **Enchaînement direct** : Après confirmation de W1, envoie immédiatement le message V5.
```

### 2. Nouvelle section "Recherche web" explicite

**Avant** : Ligne unique dans les règles d'orchestration

**Après** :
```markdown
## Recherche web

- **DÉSACTIVÉE par défaut** pour les validations et transitions d'étapes.
- **ACTIVÉE uniquement** si l'instruction technique nécessite des informations externes (ex: syntaxe API inconnue).
- **Jamais** dans les messages de validation `✓ Étape N validée.`
```

### 3. Nouvelle section "Format de transition strict"

**Ajout** :
```markdown
## Format de transition strict

Le SEUL format accepté après confirmation de W1 :
✓ Étape N validée.

M<n>|O1>W1|TASK|TID|PRI|STATE|ERR|DEPTH|CTX|BUDGET|step=N+1; dir=...; file=...; [instruction courte]

**Aucun autre texte n'est autorisé.**
```

## Résultat attendu

| Avant | Après |
|-------|-------|
| Références `[n]` sporadiques | Zéro référence web |
| Recherche web systématique | Recherche conditionnelle |
| Format de transition variable | Format unique imposé |

## Checklist de tests

- [ ] Vérifier absence totale de `[1]`, `[2]`, etc. dans les messages Comet
- [ ] Vérifier que Comet ne lance pas de recherche web sur les validations
- [ ] Vérifier que le format de transition est respecté strictement
- [ ] Mesurer la réduction de tokens par échange
