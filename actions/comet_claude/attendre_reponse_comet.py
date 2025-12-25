import time
import pyautogui
import pyperclip
import config
from config import DELAY, TIMEOUT_ATTENTE_COMET, DELAY_IMAGE_SEARCH_LOOP, DELAY_PAGE_DOWN, DELAY_KEY_PRESS, SCROLL_PAGE_DOWN_COUNT, DELAY_BEFORE_CLICK_COMET
from outils.affichage_rouge import afficher_rectangle, afficher_croix
from outils.logger import log, log_click, log_image_found, log_key, log_wait
from outils.screen_regions import REGION_LEFT

IMAGE_ZONE = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\assets\images\zone_copier_comet.png"
IMAGE_ZONE_2 = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\assets\images\zone_copier_comet_2.png"
IMAGE_COPIER = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\assets\images\copier_comet.png"
CONFIDENCE = 0.6


def execute():
    log("Attente reponse Comet...")
    start_time = time.time()
    iteration = 0
    page_down_done = False

    while True:
        if config.stop_requested:
            log("Arret demande par l'utilisateur")
            return False

        iteration += 1
        elapsed = time.time() - start_time

        if elapsed > TIMEOUT_ATTENTE_COMET:
            log(f"Timeout atteint ({TIMEOUT_ATTENTE_COMET}s)")
            return False

        if not page_down_done and iteration == 10:
            log(f"Debut scroll Page Down x{SCROLL_PAGE_DOWN_COUNT}")
            for i in range(SCROLL_PAGE_DOWN_COUNT):
                log_key('pagedown', f"scroll {i+1}/{SCROLL_PAGE_DOWN_COUNT}")
                pyautogui.keyDown('pagedown')
                time.sleep(DELAY_KEY_PRESS)
                pyautogui.keyUp('pagedown')
                log_wait(DELAY_PAGE_DOWN, "entre Page Down")
                time.sleep(DELAY_PAGE_DOWN)
            log("Fin scroll Page Down")
            page_down_done = True

        try:
            zone_location = None
            for zone_image in [IMAGE_ZONE, IMAGE_ZONE_2]:
                zone_location = pyautogui.locateOnScreen(
                    zone_image,
                    region=REGION_LEFT,
                    confidence=CONFIDENCE
                )
                if zone_location:
                    break
            if zone_location:
                log_image_found("zone_copier_comet", zone_location)
                zone_region = (zone_location.left, zone_location.top, zone_location.width, zone_location.height)
                copier_location = pyautogui.locateOnScreen(
                    IMAGE_COPIER,
                    region=zone_region,
                    confidence=CONFIDENCE
                )
                if copier_location:
                    center = pyautogui.center(copier_location)
                    log_image_found("copier_comet", copier_location)
                    log(f"Centre bouton: {center}")
                    afficher_rectangle(
                        copier_location.left,
                        copier_location.top,
                        copier_location.width,
                        copier_location.height
                    )
                    log_wait(DELAY_BEFORE_CLICK_COMET, "avant clic copier")
                    time.sleep(DELAY_BEFORE_CLICK_COMET)
                    log("Verification bouton toujours present...")
                    copier_location_2 = pyautogui.locateOnScreen(
                        IMAGE_COPIER,
                        region=zone_region,
                        confidence=CONFIDENCE
                    )
                    if copier_location_2:
                        center = pyautogui.center(copier_location_2)
                        clipboard_before = pyperclip.paste()
                        log_click(center.x, center.y, "bouton copier Comet")
                        pyautogui.click(center)
                        afficher_croix(center.x, center.y)
                        time.sleep(0.5)
                        clipboard_after = pyperclip.paste()
                        if clipboard_after != clipboard_before:
                            log(f"Presse-papier modifie: {len(clipboard_after)} caracteres")
                            log("Clic effectue sur bouton copier")
                            return True
                        else:
                            log("ERREUR: Presse-papier non modifie, nouveau clic...")
                            pyautogui.click(center)
                            time.sleep(0.5)
                    else:
                        log("Bouton disparu apres attente, nouvelle recherche...")
        except pyautogui.ImageNotFoundException:
            pass

        time.sleep(DELAY_IMAGE_SEARCH_LOOP)
