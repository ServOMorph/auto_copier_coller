# Modifications prompt_init_comet.md
**Date** : 2025-12-23
**Version** : v2
**Fichier modifié** : `prompt_init_comet.md`

---

## Problèmes identifiés

| Problème | Impact |
|----------|--------|
| Redites de validation | Comet paraphrase ce que Claude confirme |
| Références web `[1]`, `[2]` | Bruit inutile dans les échanges inter-agents |
| Explications superflues | "Pour rester conforme au plan...", "Quand tu es prêt..." |
| Double validation | Comet valide puis re-demande confirmation |
| Recherche web systématique | Ralentit les validations simples |

---

## Modifications appliquées

### 1. Nouvelle section "Règles de concision"

```markdown
## Règles de concision

- **Pas de paraphrase** : Ne répète jamais ce que W1 vient de confirmer.
- **Enchaînement direct** : Après confirmation de W1, envoie immédiatement le message V5 de l'étape suivante.
- **Pas de références web** dans les messages inter-agents (supprime les `[1]`, `[2]`, etc.).
- **Format de transition attendu** :
  ✓ Étape N validée.
  M<n>|O1>W1|TASK|TID|PRI|STATE|ERR|DEPTH|CTX|BUDGET|step=N+1; dir=...; file=...; [instruction]
```

### 2. Recherche web conditionnelle

**Avant** :
> Tu **dois effectuer des recherches web** avant chaque réponse pour t'assurer d'utiliser les meilleures pratiques et informations actuelles.

**Après** :
> Recherches web uniquement pour les étapes techniques complexes, pas pour les validations.

### 3. Suppression des références web

Toutes les références `[1]` à `[10]` supprimées du fichier (intro, agents, contexte, plan).

---

## Résultat attendu

| Avant | Après |
|-------|-------|
| 3-4 messages par étape | 2 messages par étape |
| Paraphrases systématiques | Validation concise + instruction directe |
| Références web dans les réponses | Réponses propres |

---

## A tester

- [ ] Vérifier que Comet applique bien le format `✓ Étape N validée.`
- [ ] Vérifier l'absence de références `[n]` dans les réponses
- [ ] Mesurer le nombre de tokens économisés par étape
- [ ] Vérifier que les recherches web se font uniquement sur étapes complexes
