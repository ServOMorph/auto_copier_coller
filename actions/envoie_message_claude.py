import pyautogui
import time
from outils.recherche_image import cliquer_image
from config import DELAY

IMAGE_MESSAGE = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\message_claudecode.png"
RIGHT_SCREEN_REGION = (960, 0, 960, 1080)

def execute():
    print("Recherche bouton message Claude...")
    while True:
        if cliquer_image(IMAGE_MESSAGE, region=RIGHT_SCREEN_REGION):
            print("  Bouton message trouve, envoi du message...")
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            time.sleep(DELAY)
            pyautogui.press('enter')
            print("  Message envoye")
            return True
        time.sleep(0.5)
