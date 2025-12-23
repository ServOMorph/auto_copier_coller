import time
import pyautogui
from outils.affichage_rouge import afficher_rectangle
from config import DELAY_PAGE_DOWN

IMAGE_FIN_CONV = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\fin_conv_claude.png"
RIGHT_SCREEN_REGION = (960, 0, 960, 1080)
CONFIDENCE = 0.8


def execute():
    print("Attente reponse Claude...")
    iteration = 0
    page_down_done = False
    while True:
        iteration += 1

        if not page_down_done and iteration == 10:
            print("  5s ecoulees - appui Page Down x3")
            for i in range(3):
                print(f"    Page Down {i+1}/3")
                pyautogui.press('pagedown')
                time.sleep(DELAY_PAGE_DOWN)
            page_down_done = True

        try:
            location = pyautogui.locateOnScreen(
                IMAGE_FIN_CONV,
                region=RIGHT_SCREEN_REGION,
                confidence=CONFIDENCE
            )
            if location:
                print(f"  Fin de conversation trouvee: {location}")
                afficher_rectangle(
                    location.left,
                    location.top,
                    location.width,
                    location.height
                )
                return True
            else:
                if iteration % 10 == 0:
                    print(f"  Iteration {iteration}: image non trouvee...")
        except pyautogui.ImageNotFoundException:
            if iteration % 10 == 0:
                print(f"  Iteration {iteration}: image non trouvee...")
        time.sleep(0.5)

if __name__ == "__main__":
    execute()
