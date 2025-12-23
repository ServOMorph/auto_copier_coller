import pyautogui
from outils.affichage_rouge import afficher_rectangle, afficher_croix


def trouver_image(image_path, region=None, confidence=0.8):
    try:
        location = pyautogui.locateOnScreen(image_path, region=region, confidence=confidence)
        if location:
            return location
    except pyautogui.ImageNotFoundException:
        pass
    return None


def cliquer_image(image_path, region=None, confidence=0.8):
    location = trouver_image(image_path, region, confidence)
    if location:
        afficher_rectangle(
            location.left,
            location.top,
            location.width,
            location.height
        )
        center = pyautogui.center(location)
        afficher_croix(center.x, center.y)
        pyautogui.click(center)
        return True
    return False
