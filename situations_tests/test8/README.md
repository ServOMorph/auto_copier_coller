# Idle Game - Test 8

## Description
Jeu idle (clicker) en HTML/CSS/JS standalone.

## Fichier principal
- `idle_game.html`

## Progression des étapes

| Étape | Description | Statut |
|-------|-------------|--------|
| 1 | Structure HTML de base | OK |
| 2 | Style CSS (thème sombre, layout centré) | OK |
| 3 | Compteur de points + bouton clic | OK |
| 4 | Générateurs automatiques (+1/sec) | OK |
| 5 | Multiplicateur de clic (x2) | OK |
| 6 | Sauvegarde localStorage | OK |
| 7 | Améliorations UI/UX | OK |
| 8 | Fonctionnalités bonus (assets) | OK |
| 9 | Système de prestige | OK |

## Étape 9 terminée : Système de prestige

Implémenté :
- Seuil : prestige disponible à partir de 1000 points (maxPoints)
- Formule : `P = floor(sqrt(maxPoints / 1000))`
- Bonus : +10% production globale par point de prestige
- Reset : points, générateurs, upgrades remis à zéro
- Conservé : prestigePoints, totalPrestiges, maxPoints
- UI dorée distincte, bouton caché si maxPoints < 1000
- Sauvegarde localStorage étendue

## État actuel

**Jeu fonctionnel.** Toutes les étapes (1-9) complétées.

## Prochaines étapes possibles

| Étape | Description |
|-------|-------------|
| 10 | Polish UI (animations, feedbacks visuels) |
| 11 | Équilibrage gameplay (coûts, formules) |
| 12 | Sons et effets audio |
| 13 | Nouveaux upgrades/générateurs |
| 14 | Achievements/succès |

## Étape 6 terminée : Sauvegarde localStorage

Implémenté :
- `saveGame()` : sauvegarde points, generators, multiplierLevel, clickMultiplier
- `loadGame()` : restaure les données au démarrage
- Sauvegarde auto toutes les 5 secondes
- Sauvegarde au beforeunload (fermeture page)

## État actuel du jeu
- Points : clic manuel + générateurs automatiques
- Générateurs : coût 10 pts, +1 pt/sec chacun
- Multiplicateur : coût 50 pts, x2 par niveau

## Étape 8 terminée : Assets images

Assets intégrés :
- `logo.png` : logo "Pixel Forge" en header (max-width: 200px)
- `background.png` : image de fond avec overlay sombre
- `icon-click.png` : icone bouton clic (32x32px)
- `icon-multiplier.png` : icone multiplicateur (24x24px)

Note : `icon-generator.png` manquant (renommé en icon-click car le visuel correspondait au clic)

Design appliqué :
- Thème vert cohérent avec les assets
- Effets glow sur les boutons et textes
- Background avec overlay pour lisibilité
- Transitions fluides sur hover/active
