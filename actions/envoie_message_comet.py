import pyautogui
import time
from outils.recherche_image import cliquer_image
from outils.affichage_rouge import afficher_texte_action
from config import DELAY

IMAGE_MESSAGE = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\message_comet.png"
LEFT_SCREEN_REGION = (0, 0, 960, 1080)

def execute():
    print("Recherche bouton message...")
    while True:
        if cliquer_image(IMAGE_MESSAGE, region=LEFT_SCREEN_REGION):
            print("  Bouton message trouve, envoi du message...")
            time.sleep(0.2)
            afficher_texte_action("CTRL+V")
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            time.sleep(DELAY)
            afficher_texte_action("ENTREE")
            pyautogui.press('enter')
            print("  Message envoye")
            return True
        time.sleep(0.5)
