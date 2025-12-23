# Commande /analyse_conv

Analyse croisée des logs de sessions et modifications du prompt.

## Instructions

1. **Lire les logs de sessions** dans `logs/sessions/`
2. **Lire les logs de modifications du prompt** dans `logs/prompts/`
3. **Corréler par date** les échanges avec les modifications
4. **Identifier** :
   - Les problèmes récurrents dans les échanges
   - Les modifications apportées en réponse
   - L'efficacité des changements (problème résolu ou persistant)
   - Les patterns non encore traités

5. **Produire une proposition de modification** de `prompt_init_comet.md` basée sur l'analyse

6. **Afficher le signal de validation** :
```
# 💚💚💚
```
Puis attendre la validation utilisateur avant d'appliquer les modifications.

## Format de sortie

```markdown
## Analyse des logs

### Corrélations identifiées
| Session | Problème | Modification prompt | Statut |
|---------|----------|---------------------|--------|
| ... | ... | ... | Résolu/Persistant |

### Problèmes non traités
- ...

### Proposition de modification

[Détail des modifications proposées pour prompt_init_comet.md]

# 💚💚💚

Validation requise avant application.
```

## Chemins

- Sessions : `C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\logs\sessions\`
- Prompts : `C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\logs\prompts\`
- Fichier cible : `C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\prompt_init_comet.md`
