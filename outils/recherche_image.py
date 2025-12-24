import os
import pyautogui
from outils.affichage_rouge import afficher_rectangle, afficher_croix
from outils.logger import log, log_click, log_image_found


def _get_image_name(image_path):
    return os.path.splitext(os.path.basename(image_path))[0]


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
        image_name = _get_image_name(image_path)
        log_image_found(image_name, location)
        center = pyautogui.center(location)
        log_click(center.x, center.y, image_name)
        pyautogui.click(center)
        afficher_rectangle(
            location.left,
            location.top,
            location.width,
            location.height
        )
        afficher_croix(center.x, center.y)
        return True
    return False
