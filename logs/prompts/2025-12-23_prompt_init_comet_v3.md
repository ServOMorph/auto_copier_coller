# Log de modification - prompt_init_comet.md v3

**Date** : 2025-12-23

## Problèmes identifiés

- Pas de traçabilité de l'avancement dans test8/
- Risque de refaire des étapes déjà complétées en cas de reprise
- Le prompt indiquait de commencer à l'étape 1 alors que les étapes 1-5 sont terminées

## Modifications appliquées

### Ajout section "Fichier README obligatoire"

**Avant** : Aucune mention de README

**Après** :
```markdown
## Fichier README obligatoire

- Un fichier `README.md` doit exister dans `test8/` pour tracer l'avancement.
- **Avant de commencer**, W1 doit lire ce README pour connaître l'état actuel.
- **Après chaque étape validée**, W1 doit mettre à jour le README avec :
  - L'étape complétée
  - Un résumé des modifications
  - L'étape suivante à faire
- Cela évite de refaire des étapes déjà terminées en cas de reprise.
```

### Ajout section "État actuel du projet"

**Avant** : Aucune

**Après** :
```markdown
## État actuel du projet

Les étapes suivantes sont **déjà complétées** :
- Étape 1 : Structure HTML de base + affichage compteur
- Étape 2 : Bouton de clic manuel +1 point
- Étape 3 : Générateur automatique (coût 10, +1/sec)
- Étape 4 : Affichage générateurs et pts/sec
- Étape 5 : Upgrade multiplicateur x2 (coût 50)
```

### Modification section "Démarrage"

**Avant** :
```markdown
- Tu commences à l'**Étape 1** en envoyant à W1 un message V5...
```

**Après** :
```markdown
- Tu commences à l'**Étape 6** (sauvegarde localStorage).
- **Première action** : demander à W1 de créer/mettre à jour le README.md dans test8/ avec l'état actuel.
```

## Résultat attendu

- Comet reprend à l'étape 6 sans refaire les étapes précédentes
- Un README.md est créé/maintenu dans test8/ pour tracer l'avancement
- En cas de nouvelle reprise, W1 consulte le README avant d'agir

## Checklist de tests

- [ ] Comet démarre bien à l'étape 6
- [ ] Comet demande la création du README en premier
- [ ] W1 met à jour le README après chaque étape
- [ ] Les étapes 1-5 ne sont pas refaites
