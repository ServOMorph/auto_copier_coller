import time
import pyautogui
from outils.affichage_rouge import afficher_rectangle
from outils.logger import log, log_image_found
from outils.screen_regions import REGION_RIGHT
from config import DELAY_IMAGE_SEARCH_LOOP, TIMEOUT_ATTENTE_CLAUDE

IMAGE_FIN_CONV = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\fin_conv_claude.png"
CONFIDENCE = 0.8


def execute():
    log("Attente reponse Claude...")
    start_time = time.time()
    iteration = 0
    while True:
        iteration += 1
        elapsed = time.time() - start_time

        if elapsed > TIMEOUT_ATTENTE_CLAUDE:
            log(f"Timeout atteint ({TIMEOUT_ATTENTE_CLAUDE}s)")
            return False

        try:
            location = pyautogui.locateOnScreen(
                IMAGE_FIN_CONV,
                region=REGION_RIGHT,
                confidence=CONFIDENCE
            )
            if location:
                log_image_found("fin_conv_claude", location)
                log("Affichage rectangle...")
                afficher_rectangle(
                    location.left,
                    location.top,
                    location.width,
                    location.height
                )
                log("Fin attente reponse Claude")
                return True
            else:
                if iteration % 10 == 0:
                    log(f"Iteration {iteration}: image non trouvee...")
        except pyautogui.ImageNotFoundException:
            if iteration % 10 == 0:
                log(f"Iteration {iteration}: image non trouvee...")
        time.sleep(DELAY_IMAGE_SEARCH_LOOP)

if __name__ == "__main__":
    execute()
