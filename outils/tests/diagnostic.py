import sys
sys.path.insert(0, r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller")

import pyautogui
from PIL import Image
import os

IMAGE_PATH = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\message_comet.png"
LEFT_SCREEN_REGION = (0, 0, 960, 1080)
OUTPUT_DIR = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\outils\tests"

print("=== DIAGNOSTIC ===\n")

print("1. Verification de l'image source:")
if os.path.exists(IMAGE_PATH):
    img = Image.open(IMAGE_PATH)
    print(f"   Fichier: OK")
    print(f"   Taille: {img.size[0]}x{img.size[1]} px")
    print(f"   Format: {img.format}")
    print(f"   Mode: {img.mode}")
else:
    print(f"   ERREUR: Fichier non trouve!")

print("\n2. Information ecran:")
screen_size = pyautogui.size()
print(f"   Resolution detectee: {screen_size.width}x{screen_size.height}")

print("\n3. Capture de la region gauche:")
screenshot_path = os.path.join(OUTPUT_DIR, "screenshot_region.png")
screenshot = pyautogui.screenshot(region=LEFT_SCREEN_REGION)
screenshot.save(screenshot_path)
print(f"   Screenshot sauvegarde: {screenshot_path}")
print(f"   Taille: {screenshot.size[0]}x{screenshot.size[1]} px")

print("\n4. Test de detection avec differentes confiances:")
for conf in [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]:
    try:
        location = pyautogui.locateOnScreen(IMAGE_PATH, region=LEFT_SCREEN_REGION, confidence=conf)
        if location:
            print(f"   Confidence {conf}: TROUVE a {location}")
            break
        else:
            print(f"   Confidence {conf}: non trouve")
    except pyautogui.ImageNotFoundException:
        print(f"   Confidence {conf}: non trouve")
    except Exception as e:
        print(f"   Confidence {conf}: erreur - {e}")

print("\n5. Test sans region (ecran complet):")
try:
    location = pyautogui.locateOnScreen(IMAGE_PATH, confidence=0.5)
    if location:
        print(f"   TROUVE a {location}")
    else:
        print("   Non trouve")
except pyautogui.ImageNotFoundException:
    print("   Non trouve")
except Exception as e:
    print(f"   Erreur: {e}")

print("\n=== FIN DIAGNOSTIC ===")
print(f"\nComparez visuellement:")
print(f"  - Image recherchee: {IMAGE_PATH}")
print(f"  - Screenshot region: {screenshot_path}")
