import pyautogui

def trouver_image(image_path, region=None, confidence=0.8):
    try:
        location = pyautogui.locateOnScreen(image_path, region=region, confidence=confidence)
        if location:
            return pyautogui.center(location)
    except pyautogui.ImageNotFoundException:
        pass
    return None

def cliquer_image(image_path, region=None, confidence=0.8):
    center = trouver_image(image_path, region, confidence)
    if center:
        pyautogui.click(center)
        return True
    return False
