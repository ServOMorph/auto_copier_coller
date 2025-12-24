import pyperclip
from config import STARTORCH_COMMAND, STARTDEV_COMMAND
from outils.logger import log
from . import envoie_message_orch, envoie_message_dev, attendre_reponse_orch, attendre_reponse_dev


def init_orch():
    log("Initialisation Orch avec /startorch...")
    pyperclip.copy(STARTORCH_COMMAND)
    envoie_message_orch.execute()
    attendre_reponse_orch.execute()
    log("Orch initialise")


def init_dev():
    log("Initialisation Dev avec /startdev...")
    pyperclip.copy(STARTDEV_COMMAND)
    envoie_message_dev.execute()
    attendre_reponse_dev.execute()
    log("Dev initialise")


def execute():
    init_orch()
    init_dev()
    log("Initialisation Orch/Dev terminee")
