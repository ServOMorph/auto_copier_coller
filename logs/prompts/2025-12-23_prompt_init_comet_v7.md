# Log modification prompt_init_comet.md - v7

**Date** : 2025-12-23

## Problèmes identifiés

| Problème | Sessions concernées | Impact |
|----------|---------------------|--------|
| Références web `[n]` persistantes | 21:37, 21:51, 22:18, 22:24, 22:34, 22:55 | 60% des sessions polluées |
| Recherche web Larousse inutile | 22:18, 22:24 | Tokens gaspillés sur `larousse.fr/test` |
| Règles v2/v4 insuffisantes | Analyse croisée | "INTERDIT" ignoré par Comet |

## Modifications appliquées

### 1. Nouvelle section "RÈGLE ABSOLUE" (lignes 4-11)

**Avant** : Aucune section en tête de prompt

**Après** :
```markdown
## RÈGLE ABSOLUE

**Tu ne dois JAMAIS inclure** :
- Des références numérotées `[1]`, `[2]`, etc.
- Des URLs ou liens hypertextes
- Des résultats de recherche web

Ces éléments polluent les échanges et gaspillent des tokens. Si tu violes cette règle, l'échange est considéré comme échoué.
```

### 2. Renforcement "Règles de concision (STRICT)" (lignes 86-95)

**Avant** :
```markdown
- **INTERDIT** : Les références web `[1]`, `[2]`, etc. dans TOUS les messages.
- **INTERDIT** : Les URLs ou liens dans les messages V5.
- **Pas de paraphrase** : Ne répète jamais ce que W1 vient de confirmer.
- **Enchaînement direct** : Après confirmation de W1, envoie immédiatement le message V5.
```

**Après** :
```markdown
**CRITIQUE - VIOLATION = ÉCHEC** :
- **ZÉRO référence web** : Aucun `[1]`, `[2]`, URL, ou lien hypertexte dans les messages.
- **ZÉRO recherche web** pour les validations d'étapes.

**Format obligatoire** :
- Après confirmation W1 : `✓ Étape N validée.` + message V5. **Rien d'autre.**
- Pas de paraphrase de ce que W1 vient de dire.
- Pas d'explications ("Pour rester conforme...", "Si tu valides...").
```

### 3. Simplification "Recherche web" (lignes 97-99)

**Avant** :
```markdown
- **DÉSACTIVÉE par défaut** pour les validations et transitions d'étapes.
- **ACTIVÉE uniquement** si l'instruction technique nécessite des informations externes (ex: syntaxe API inconnue).
- **Jamais** dans les messages de validation `✓ Étape N validée.`
```

**Après** :
```markdown
**DÉSACTIVÉE.** Ne fais jamais de recherche web sauf si W1 demande explicitement une information technique introuvable dans le contexte.
```

## Résultat attendu

| Avant | Après |
|-------|-------|
| Références `[n]` dans 60% sessions | Zéro référence |
| "INTERDIT" insuffisant | "VIOLATION = ÉCHEC" |
| Recherche web conditionnelle floue | Recherche web désactivée par défaut |

## Checklist de tests

- [ ] Vérifier absence totale de `[1]`, `[2]`, etc. dans les messages Comet
- [ ] Vérifier absence de recherches web sur validations simples
- [ ] Vérifier format strict `✓ Étape N validée.` + V5 sans texte additionnel
- [ ] Mesurer réduction tokens par échange vs sessions précédentes
