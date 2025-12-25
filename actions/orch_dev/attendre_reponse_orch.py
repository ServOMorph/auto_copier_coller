import time
import pyautogui
import config
from outils.affichage_rouge import afficher_rectangle
from outils.logger import log, log_image_found
from outils.screen_regions import REGION_LEFT
from config import DELAY_IMAGE_SEARCH_LOOP, TIMEOUT_ATTENTE_CLAUDE

IMAGE_FIN_CONV = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\assets\images\fin_conv_claude.png"
CONFIDENCE = 0.8


def execute():
    log("=== ATTENTE REPONSE ORCH (gauche) ===")
    start_time = time.time()
    iteration = 0
    while True:
        if config.stop_requested:
            log("Arret demande par l'utilisateur")
            return False

        iteration += 1
        elapsed = time.time() - start_time

        if elapsed > TIMEOUT_ATTENTE_CLAUDE:
            log(f"TIMEOUT atteint ({TIMEOUT_ATTENTE_CLAUDE}s)")
            return False

        try:
            location = pyautogui.locateOnScreen(
                IMAGE_FIN_CONV,
                region=REGION_LEFT,
                confidence=CONFIDENCE
            )
            if location:
                log_image_found("fin_conv_orch", location)
                afficher_rectangle(
                    location.left,
                    location.top,
                    location.width,
                    location.height
                )
                log("Fin reponse Orch detectee")
                log("=== FIN ATTENTE REPONSE ORCH ===")
                return True
            else:
                if iteration % 10 == 0:
                    log(f"Iteration {iteration}: recherche fin_conv_orch...")
        except pyautogui.ImageNotFoundException:
            if iteration % 10 == 0:
                log(f"Iteration {iteration}: image non trouvee...")
        time.sleep(DELAY_IMAGE_SEARCH_LOOP)


if __name__ == "__main__":
    execute()
