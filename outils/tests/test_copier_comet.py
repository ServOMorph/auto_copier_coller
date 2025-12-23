import sys
import time
sys.path.insert(0, r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller")

import pyautogui

IMAGE_ZONE = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\zone_copier_comet.png"
IMAGE_COPIER = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\copier_comet.png"
LEFT_SCREEN_REGION = (0, 0, 960, 1080)
TIMEOUT = 30
CONFIDENCE = 0.6

if __name__ == "__main__":
    print(f"Etape 1: Recherche de la zone: {IMAGE_ZONE}")
    print(f"Region initiale: {LEFT_SCREEN_REGION}")
    print(f"Confidence: {CONFIDENCE}")
    print(f"Timeout: {TIMEOUT}s")
    print("-" * 50)

    start_time = time.time()
    iteration = 0

    while True:
        iteration += 1
        elapsed = time.time() - start_time

        if elapsed > TIMEOUT:
            print(f"\nTimeout atteint ({TIMEOUT}s)")
            break

        try:
            zone_location = pyautogui.locateOnScreen(
                IMAGE_ZONE,
                region=LEFT_SCREEN_REGION,
                confidence=CONFIDENCE
            )
            if zone_location:
                print(f"\n[{elapsed:.1f}s] Zone TROUVEE!")
                print(f"  Position: x={zone_location.left}, y={zone_location.top}")
                print(f"  Taille: {zone_location.width}x{zone_location.height}")

                sub_region = (
                    zone_location.left,
                    zone_location.top,
                    zone_location.width,
                    zone_location.height
                )
                print(f"\nEtape 2: Recherche du bouton copier dans la zone: {sub_region}")

                try:
                    copier_location = pyautogui.locateOnScreen(
                        IMAGE_COPIER,
                        region=sub_region,
                        confidence=CONFIDENCE
                    )
                    if copier_location:
                        center = pyautogui.center(copier_location)
                        print(f"  Bouton copier TROUVE!")
                        print(f"  Position: x={copier_location.left}, y={copier_location.top}")
                        print(f"  Centre: {center}")
                        print("  Clic en cours...")
                        pyautogui.click(center)
                        print("  Clic effectue!")
                        break
                    else:
                        print("  Bouton copier non trouve dans la zone")
                except pyautogui.ImageNotFoundException:
                    print("  Bouton copier non trouve dans la zone")
                except Exception as e:
                    print(f"  Erreur recherche bouton: {e}")
                break
            else:
                print(f"[{elapsed:.1f}s] Iteration {iteration}: zone non trouvee")
        except pyautogui.ImageNotFoundException:
            print(f"[{elapsed:.1f}s] Iteration {iteration}: zone non trouvee")
        except Exception as e:
            print(f"[{elapsed:.1f}s] Erreur: {e}")

        time.sleep(0.5)
