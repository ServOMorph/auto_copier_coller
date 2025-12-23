import time
import pyautogui
from config import DELAY
from outils.affichage_rouge import afficher_rectangle, afficher_croix, afficher_texte_action

IMAGE_ZONE = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\zone_copier_comet.png"
IMAGE_ZONE_2 = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\zone_copier_comet_2.png"
IMAGE_COPIER = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\copier_comet.png"
LEFT_SCREEN_REGION = (0, 0, 960, 1080)
LEFT_SCREEN_CENTER = (480, 540)
CONFIDENCE = 0.6
TIMEOUT = 300


def execute():
    print("Attente reponse comet...")
    start_time = time.time()
    iteration = 0

    while True:
        iteration += 1
        elapsed = time.time() - start_time

        if elapsed > TIMEOUT:
            print(f"  Timeout atteint ({TIMEOUT}s)")
            return False

        try:
            zone_location = None
            for zone_image in [IMAGE_ZONE, IMAGE_ZONE_2]:
                zone_location = pyautogui.locateOnScreen(
                    zone_image,
                    region=LEFT_SCREEN_REGION,
                    confidence=CONFIDENCE
                )
                if zone_location:
                    break
            if zone_location:
                zone_region = (zone_location.left, zone_location.top, zone_location.width, zone_location.height)
                copier_location = pyautogui.locateOnScreen(
                    IMAGE_COPIER,
                    region=zone_region,
                    confidence=CONFIDENCE
                )
                if copier_location:
                    center = pyautogui.center(copier_location)
                    print(f"  [{elapsed:.1f}s] Bouton copier trouve: {copier_location}")
                    print(f"  Centre: {center}")
                    print(f"  Affichage rectangle rouge et attente {DELAY}s...")
                    afficher_rectangle(
                        copier_location.left,
                        copier_location.top,
                        copier_location.width,
                        copier_location.height
                    )
                    copier_location_2 = pyautogui.locateOnScreen(
                        IMAGE_COPIER,
                        region=zone_region,
                        confidence=CONFIDENCE
                    )
                    if copier_location_2:
                        center = pyautogui.center(copier_location_2)
                        print(f"  Affichage croix rouge et attente {DELAY}s avant clic...")
                        afficher_croix(center.x, center.y)
                        print(f"  Clic sur {center}")
                        pyautogui.click(center)
                        return True
                    else:
                        print("  Bouton disparu apres attente, nouvelle recherche...")
                else:
                    _scroll_page(iteration, elapsed)
            else:
                _scroll_page(iteration, elapsed)
        except pyautogui.ImageNotFoundException:
            _scroll_page(iteration, elapsed)

        time.sleep(0.5)


def _scroll_page(iteration, elapsed):
    if iteration % 10 == 0:
        print(f"  [{elapsed:.1f}s] Iter {iteration}: bouton non trouve, scroll...")
    pyautogui.click(LEFT_SCREEN_CENTER[0], LEFT_SCREEN_CENTER[1])
    afficher_texte_action("PAGEDOWN", duree=0.3)
    pyautogui.press('pagedown')
