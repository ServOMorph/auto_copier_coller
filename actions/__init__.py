from . import comet_claude
from . import orch_dev
from . import claude_solo

from .comet_claude import envoie_message_comet, attendre_reponse_comet
from .comet_claude import envoie_message_claude, attendre_reponse_claude
from .claude_solo import boucle_claude_solo
