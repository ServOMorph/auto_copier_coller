# Commande /pause

Met en pause le projet actuel en sauvegardant l'état d'avancement.

## Argument

`$ARGUMENTS` : numéro du test (ex: `8` pour test8). Si vide, utiliser le test mentionné dans le contexte récent.

## Instructions

1. **Identifier le projet** :
   - Dossier : `C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\situations_tests\test{$ARGUMENTS}\`
   - Fichier README : `README.md` dans ce dossier

2. **Lire le README actuel** du projet test

3. **Mettre à jour le README** avec :
   - Tableau des étapes : marquer les étapes complétées
   - Ajouter une section `## État de pause` avec :
     - Date de pause
     - Dernière étape complétée
     - Prochaine étape à faire
     - Notes éventuelles sur le contexte

4. **Lire** `C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\prompt_init_comet.md`

5. **Mettre à jour prompt_init_comet.md** :
   - Section `## État actuel du projet` : synchroniser avec les étapes complétées
   - Section `## Statut` : indiquer "**En pause.**" + dernière étape + prochaine étape

## Format de sortie

```
Projet test{N} mis en pause.

Dernière étape : {N} - {description}
Prochaine étape : {N+1} - {description}

Fichiers mis à jour :
- situations_tests/test{N}/README.md
- prompt_init_comet.md
```

## Chemins

- Tests : `C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\situations_tests\`
- Prompt Comet : `C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\prompt_init_comet.md`
