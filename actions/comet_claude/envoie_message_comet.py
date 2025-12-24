import pyautogui
import time
from outils.recherche_image import cliquer_image
from outils.affichage_rouge import afficher_texte_action
from outils.logger import log, log_hotkey, log_key, log_wait
from outils.screen_regions import REGION_LEFT
from config import DELAY, DELAY_BEFORE_PASTE_COMET, DELAY_AFTER_PASTE_COMET, DELAY_IMAGE_SEARCH_LOOP

IMAGE_MESSAGE = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\message_comet.png"

def execute():
    log("Recherche bouton message Comet...")
    while True:
        if cliquer_image(IMAGE_MESSAGE, region=REGION_LEFT):
            log("Bouton message Comet trouve")
            log_wait(DELAY_BEFORE_PASTE_COMET, "avant CTRL+V")
            time.sleep(DELAY_BEFORE_PASTE_COMET)
            afficher_texte_action("CTRL+V")
            log_hotkey(['ctrl', 'v'], "coller message")
            pyautogui.hotkey('ctrl', 'v')
            log_wait(DELAY_AFTER_PASTE_COMET, "apres CTRL+V")
            time.sleep(DELAY_AFTER_PASTE_COMET)
            log_wait(DELAY, "avant ENTREE")
            time.sleep(DELAY)
            afficher_texte_action("ENTREE")
            log_key('enter', "envoyer message Comet")
            pyautogui.press('enter')
            log("Message Comet envoye")
            return True
        time.sleep(DELAY_IMAGE_SEARCH_LOOP)
