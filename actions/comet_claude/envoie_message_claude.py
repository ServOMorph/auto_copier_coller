import pyautogui
import time
from outils.recherche_image import cliquer_image
from outils.affichage_rouge import afficher_texte_action
from outils.logger import log, log_hotkey, log_key, log_wait
from outils.screen_regions import REGION_RIGHT
from config import DELAY, DELAY_BEFORE_PASTE_CLAUDE, DELAY_AFTER_PASTE_CLAUDE, DELAY_IMAGE_SEARCH_LOOP

IMAGE_MESSAGE = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\assets\images\message_claudecode.png"

def execute():
    log("Recherche bouton message Claude...")
    while True:
        if cliquer_image(IMAGE_MESSAGE, region=REGION_RIGHT):
            log("Bouton message Claude trouve")
            log_wait(DELAY_BEFORE_PASTE_CLAUDE, "avant CTRL+V")
            time.sleep(DELAY_BEFORE_PASTE_CLAUDE)
            afficher_texte_action("CTRL+V")
            log_hotkey(['ctrl', 'v'], "coller message")
            pyautogui.hotkey('ctrl', 'v')
            log_wait(DELAY_AFTER_PASTE_CLAUDE, "apres CTRL+V")
            time.sleep(DELAY_AFTER_PASTE_CLAUDE)
            log_wait(DELAY, "avant ENTREE")
            time.sleep(DELAY)
            afficher_texte_action("ENTREE")
            log_key('enter', "envoyer message Claude")
            pyautogui.press('enter')
            log("Message Claude envoye")
            return True
        time.sleep(DELAY_IMAGE_SEARCH_LOOP)
