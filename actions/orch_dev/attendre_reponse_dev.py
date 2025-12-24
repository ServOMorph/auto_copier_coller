import time
import pyautogui
import pyperclip
from outils.affichage_rouge import afficher_rectangle, afficher_croix, afficher_texte_action
from outils.logger import log, log_image_found, log_click, log_wait, log_action
from outils.screen_regions import REGION_RIGHT
from config import (
    DELAY_IMAGE_SEARCH_LOOP,
    TIMEOUT_ATTENTE_CLAUDE,
    DELAY_BEFORE_CLICK_COPY,
    DELAY_BEFORE_COPY_RESPONSE
)

IMAGE_FIN_CONV = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\fin_conv_claude.png"
IMAGE_COPIER = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\copier_claude.png"
CONFIDENCE = 0.8
CONFIDENCE_COPIER = 0.6


def execute():
    log("=== ATTENTE REPONSE DEV (droite) ===")
    start_time = time.time()
    iteration = 0
    while True:
        iteration += 1
        elapsed = time.time() - start_time

        if elapsed > TIMEOUT_ATTENTE_CLAUDE:
            log(f"TIMEOUT atteint ({TIMEOUT_ATTENTE_CLAUDE}s)")
            return False

        try:
            location = pyautogui.locateOnScreen(
                IMAGE_FIN_CONV,
                region=REGION_RIGHT,
                confidence=CONFIDENCE
            )
            if location:
                log_image_found("fin_conv_dev", location)
                afficher_rectangle(
                    location.left,
                    location.top,
                    location.width,
                    location.height
                )
                log("Fin reponse Dev detectee")
                log_action("COPIE_REPONSE", "demarrage copie reponse Dev")
                if _copier_reponse():
                    log("=== FIN ATTENTE REPONSE DEV ===")
                    return True
                else:
                    log("Echec copie, nouvelle tentative...")
            else:
                if iteration % 10 == 0:
                    log(f"Iteration {iteration}: recherche fin_conv_dev...")
        except pyautogui.ImageNotFoundException:
            if iteration % 10 == 0:
                log(f"Iteration {iteration}: image non trouvee...")
        time.sleep(DELAY_IMAGE_SEARCH_LOOP)


def _copier_reponse():
    log("Recherche bouton copier...")
    try:
        copier_location = pyautogui.locateOnScreen(
            IMAGE_COPIER,
            region=REGION_RIGHT,
            confidence=CONFIDENCE_COPIER
        )
        if copier_location:
            center = pyautogui.center(copier_location)
            log_image_found("copier_claude", copier_location)
            afficher_rectangle(
                copier_location.left,
                copier_location.top,
                copier_location.width,
                copier_location.height
            )

            afficher_texte_action("COPIE REPONSE")
            log_wait(DELAY_BEFORE_COPY_RESPONSE, "avant copie reponse")
            time.sleep(DELAY_BEFORE_COPY_RESPONSE)

            log_wait(DELAY_BEFORE_CLICK_COPY, "avant clic bouton copier")
            time.sleep(DELAY_BEFORE_CLICK_COPY)

            clipboard_before = pyperclip.paste()
            log_click(center.x, center.y, "bouton copier Dev")
            pyautogui.click(center)
            afficher_croix(center.x, center.y)

            time.sleep(0.5)
            clipboard_after = pyperclip.paste()

            if clipboard_after != clipboard_before:
                log(f"Reponse copiee dans presse-papier: {len(clipboard_after)} caracteres")
                return True
            else:
                log("ERREUR: Presse-papier non modifie, second clic...")
                pyautogui.click(center)
                time.sleep(0.5)
                if pyperclip.paste() != clipboard_before:
                    log("Second clic reussi")
                    return True
                return False
    except pyautogui.ImageNotFoundException:
        log("Bouton copier non trouve")
    return False


if __name__ == "__main__":
    execute()
