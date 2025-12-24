# Configuration des delais (en secondes)

# =============================================================================
# DELAIS COMMUNS (utilises dans COMET/CLAUDE et ORCH/DEV)
# =============================================================================

# Delai general entre les etapes principales de la boucle
DELAY = 1

# Delai entre chaque tentative de recherche d'image (polling)
DELAY_IMAGE_SEARCH_LOOP = 1

# Duree d'appui sur les touches (en secondes)
DELAY_KEY_PRESS = 0.5

# Delai de polling quand le processus est en pause
DELAY_PAUSE_POLLING = 0.2

# Delai avant d'effectuer CTRL+V apres avoir clique sur le champ message
DELAY_BEFORE_PASTE = 2

# Delai apres CTRL+V pour laisser le texte se coller
DELAY_AFTER_PASTE = 2

# Delai avant de cliquer sur un bouton copier (apres affichage rectangle)
DELAY_BEFORE_CLICK_COPY = 1

# Delai avant de copier la reponse dans le presse-papier
DELAY_BEFORE_COPY_RESPONSE = 2

# =============================================================================
# MODE COMET/CLAUDE - Delais specifiques
# =============================================================================

# Delai avant de lancer la boucle principale apres l'initialisation
DELAY_BEFORE_MAIN = DELAY

# Delai entre chaque appui Page Down lors du scroll
DELAY_PAGE_DOWN = 2

# Nombre de scrolls Page Down
SCROLL_PAGE_DOWN_COUNT = 5

# Timeout maximum pour attendre la reponse de Comet (en secondes)
TIMEOUT_ATTENTE_COMET = 600

# Multiplicateur pour le delai d'attente reponse Claude
DELAY_MULTIPLIER_ATTENTE_CLAUDE = 20

# =============================================================================
# MODE ORCH/DEV (CLAUDE/CLAUDE) - Delais specifiques
# =============================================================================

# Timeout maximum pour attendre la reponse de Claude (Orch ou Dev)
TIMEOUT_ATTENTE_CLAUDE = 300

# Commande pour initialiser l'orchestrateur
STARTORCH_COMMAND = "/startorch"

# =============================================================================
# ALIASES POUR RETROCOMPATIBILITE
# =============================================================================

# Comet utilise les memes delais que les communs
DELAY_BEFORE_PASTE_COMET = DELAY_BEFORE_PASTE
DELAY_AFTER_PASTE_COMET = DELAY_AFTER_PASTE
DELAY_BEFORE_CLICK_COMET = DELAY_BEFORE_CLICK_COPY

# Claude utilise les memes delais que les communs
DELAY_BEFORE_PASTE_CLAUDE = DELAY_BEFORE_PASTE
DELAY_AFTER_PASTE_CLAUDE = DELAY_AFTER_PASTE
