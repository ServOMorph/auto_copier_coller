import time
import pyautogui
import pyperclip
import config
from outils.affichage_rouge import afficher_rectangle, afficher_texte_action
from outils.logger import log, log_click, log_image_found, log_key, log_wait
from outils.screen_regions import REGION_LEFT
from config import DELAY, DELAY_IMAGE_SEARCH_LOOP, DELAY_BEFORE_PASTE_CLAUDE, DELAY_AFTER_PASTE_CLAUDE, DELAY_CLAUDE_SOLO_END

IMAGE_FIN_CONV = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\assets\images\fin_conv_claude.png"
IMAGE_MESSAGE = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\assets\images\message_claudecode.png"
MESSAGE_AUTO = "Fais au mieux"
CONFIDENCE = 0.8


def execute():
    log("=== BOUCLE CLAUDE SOLO ===")
    log("Recherche fin conversation Claude (gauche)...")

    while True:
        if config.stop_requested:
            log("Arret demande par l'utilisateur")
            return False

        try:
            location = pyautogui.locateOnScreen(
                IMAGE_FIN_CONV,
                region=REGION_LEFT,
                confidence=CONFIDENCE
            )
            if location:
                log_image_found("fin_conv_claude", location)
                afficher_rectangle(
                    location.left,
                    location.top,
                    location.width,
                    location.height
                )
                log("Fin conversation Claude detectee")

                if envoyer_message_auto():
                    log("Message automatique envoye")
                    return True
                else:
                    log("Echec envoi message, nouvelle tentative...")
        except pyautogui.ImageNotFoundException:
            pass

        time.sleep(DELAY_IMAGE_SEARCH_LOOP)


def envoyer_message_auto():
    log("Recherche bouton message Claude (gauche)...")

    try:
        location = pyautogui.locateOnScreen(
            IMAGE_MESSAGE,
            region=REGION_LEFT,
            confidence=CONFIDENCE
        )
        if location:
            center = pyautogui.center(location)
            log_image_found("message_claudecode", location)
            afficher_rectangle(
                location.left,
                location.top,
                location.width,
                location.height
            )

            log_click(center.x, center.y, "bouton message Claude")
            pyautogui.click(center)

            log_wait(DELAY_BEFORE_PASTE_CLAUDE, "avant copie message")
            time.sleep(DELAY_BEFORE_PASTE_CLAUDE)

            afficher_texte_action(f"COPIE: {MESSAGE_AUTO}")
            log(f"Copie dans presse-papier: {MESSAGE_AUTO}")
            pyperclip.copy(MESSAGE_AUTO)

            afficher_texte_action("CTRL+V")
            log("Coller message")
            pyautogui.hotkey('ctrl', 'v')

            log_wait(DELAY_AFTER_PASTE_CLAUDE, "apres CTRL+V")
            time.sleep(DELAY_AFTER_PASTE_CLAUDE)

            log_wait(DELAY, "avant ENTREE")
            time.sleep(DELAY)

            afficher_texte_action("ENTREE")
            log_key('enter', "envoyer message Claude Solo")
            pyautogui.press('enter')

            log_wait(DELAY_CLAUDE_SOLO_END, "fin workflow Claude Solo")
            time.sleep(DELAY_CLAUDE_SOLO_END)

            return True
    except pyautogui.ImageNotFoundException:
        log("Bouton message non trouve")
    except Exception as e:
        log(f"Erreur: {e}")

    return False


if __name__ == "__main__":
    execute()
