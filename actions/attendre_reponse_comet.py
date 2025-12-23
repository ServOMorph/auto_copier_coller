import time
import pyautogui

IMAGE_ZONE = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\zone_copier_comet.png"
IMAGE_COPIER = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\copier_comet.png"
LEFT_SCREEN_REGION = (0, 0, 960, 1080)
LEFT_SCREEN_CENTER = (480, 540)
CONFIDENCE = 0.6

def execute():
    print("Attente reponse comet...")
    iteration = 0
    while True:
        iteration += 1
        try:
            zone_location = pyautogui.locateOnScreen(
                IMAGE_ZONE,
                region=LEFT_SCREEN_REGION,
                confidence=CONFIDENCE
            )
            if zone_location:
                print(f"  Zone trouvee: {zone_location}")
                sub_region = (
                    zone_location.left,
                    zone_location.top,
                    zone_location.width,
                    zone_location.height
                )
                try:
                    copier_location = pyautogui.locateOnScreen(
                        IMAGE_COPIER,
                        region=sub_region,
                        confidence=CONFIDENCE
                    )
                    if copier_location:
                        center = pyautogui.center(copier_location)
                        print(f"  Bouton copier trouve, clic sur {center}")
                        time.sleep(2)
                        pyautogui.click(center)
                        return True
                    else:
                        print(f"  Iteration {iteration}: bouton non trouve dans zone, scroll...")
                        pyautogui.click(LEFT_SCREEN_CENTER[0], LEFT_SCREEN_CENTER[1])
                        pyautogui.press('pagedown')
                except pyautogui.ImageNotFoundException:
                    print(f"  Iteration {iteration}: bouton non trouve dans zone, scroll...")
                    pyautogui.click(LEFT_SCREEN_CENTER[0], LEFT_SCREEN_CENTER[1])
                    pyautogui.press('pagedown')
            else:
                if iteration % 10 == 0:
                    print(f"  Iteration {iteration}: zone non trouvee, scroll...")
                pyautogui.click(LEFT_SCREEN_CENTER[0], LEFT_SCREEN_CENTER[1])
                pyautogui.press('pagedown')
        except pyautogui.ImageNotFoundException:
            if iteration % 10 == 0:
                print(f"  Iteration {iteration}: zone non trouvee, scroll...")
            pyautogui.click(LEFT_SCREEN_CENTER[0], LEFT_SCREEN_CENTER[1])
            pyautogui.press('pagedown')
        time.sleep(0.5)
