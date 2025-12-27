# Workflow Orch <-> Dev

## Description

Communication automatisee entre deux instances Claude Code :
- **Orch** (Orchestrateur) : fenetre de gauche
- **Dev** (Developpeur) : fenetre de droite

## Disposition ecran

```
+---------------------------+---------------------------+
|                           |                           |
|      Claude Orch          |       Claude Dev          |
|       (gauche)            |        (droite)           |
|                           |                           |
|    REGION_LEFT            |     REGION_RIGHT          |
|    (0, 0, 960, 1080)      |    (960, 0, 960, 1080)    |
|                           |                           |
+---------------------------+---------------------------+
```

## Workflow

### Initialisation

1. Copier `/startorch` dans le presse-papier
2. Envoyer a Orch (fenetre gauche)
3. Copier `/startdev` dans le presse papier
4. Envoyer à Dev (fenetre droite)
5. Attendre reponse Orch

### Boucle principale

```
+------------------+
| Orch -> Dev      |
+--------+---------+
         |
         v
+------------------+
| Envoyer a Dev    |
| (droite)         |
+--------+---------+
         |
         v
+------------------+
| Attendre reponse |
+--------+---------+
         |
         v
+------------------+
| Dev -> Orch      |
+--------+---------+
         |
         v
+------------------+
| Envoyer a Orch   |
| (gauche)         |
+--------+---------+
         |
         v
+------------------+
| Attendre reponse |
+--------+---------+
         |
         +-------> Retour au debut de la boucle
```

## Actions utilisees

| Action | Region | Description |
|--------|--------|-------------|
| envoie_message_orch | REGION_LEFT | Colle et envoie message a Orch |
| attendre_reponse_orch | REGION_LEFT | Attend fin reponse + copie |
| envoie_message_dev | REGION_RIGHT | Colle et envoie message a Dev |
| attendre_reponse_dev | REGION_RIGHT | Attend fin reponse + copie |

## Configuration

Dans `config.py` :
- `STARTORCH_COMMAND = "/startorch"` : commande d'initialisation Orch
