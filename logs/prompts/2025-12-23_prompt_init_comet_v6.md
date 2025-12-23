# Log modification prompt_init_comet.md - v6

**Date** : 2025-12-23
**Version** : 6

## Problèmes identifiés

- Projet marqué comme "terminé" alors qu'une nouvelle fonctionnalité (prestige) doit être ajoutée
- Plan de construction limité à 8 étapes, pas de système de prestige

## Modifications appliquées

### 1. Plan de construction (ligne 67)

**Avant** :
```
8. **Étape 8** : Demander des images à ChatGPT...
```

**Après** :
```
8. **Étape 8** : Demander des images à ChatGPT...
9. **Étape 9** : Système de prestige (reset contre bonus permanent de production).
```

### 2. État actuel du projet (lignes 101-112)

**Avant** :
```
Toutes les étapes sont **complétées** :
[...8 étapes ✅]
```

**Après** :
```
Étapes 1-8 **complétées**, étape 9 **en cours** :
[...8 étapes ✅]
- ⏳ Étape 9 : Système de prestige
```

### 3. Nouvelle section : Étape 9 (lignes 124-141)

Ajout des spécifications techniques :
- Seuil : maxPoints >= 1000
- Formule : P = floor(sqrt(maxPoints / 1000))
- Bonus : +10% production par point de prestige
- Variables localStorage : maxPoints, prestigePoints, totalPrestiges
- UI : bouton conditionnel + affichage multiplicateur

### 4. Statut (ligne 145)

**Avant** :
```
**Projet terminé.** Le jeu idle est fonctionnel avec tous les assets visuels intégrés.
```

**Après** :
```
**En cours.** Étape 9 (système de prestige) à implémenter.
```

## Résultat attendu

- Comet (O1) peut maintenant orchestrer l'étape 9
- W1 (ClaudeCode) reçoit les spécifications complètes du système de prestige
- La progression est tracée correctement

## Checklist de tests

- [ ] Comet comprend qu'il reste une étape à faire
- [ ] Comet envoie le bon message V5 pour l'étape 9
- [ ] W1 implémente les 3 variables (maxPoints, prestigePoints, totalPrestiges)
- [ ] W1 applique getPrestigeMultiplier() aux gains (clic + générateurs)
- [ ] W1 ajoute le bouton prestige conditionnel
- [ ] W1 étend le localStorage avec les nouvelles variables
- [ ] Fonctionnalité testée : prestige à 1000 points donne 1 point de prestige (+10%)
