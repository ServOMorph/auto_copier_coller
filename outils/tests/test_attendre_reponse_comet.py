import sys
import time
import threading
sys.path.insert(0, r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller")

import pyautogui
import tkinter as tk


def afficher_rectangle_rouge(x, y, width, height, duree=3):
    """Affiche un rectangle rouge autour d'une zone de l'ecran."""
    def show():
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes('-topmost', True)
        root.attributes('-transparentcolor', 'white')
        root.geometry(f"{width + 6}x{height + 6}+{x - 3}+{y - 3}")

        canvas = tk.Canvas(root, width=width + 6, height=height + 6,
                          bg='white', highlightthickness=0)
        canvas.pack()
        canvas.create_rectangle(3, 3, width + 3, height + 3,
                               outline='red', width=3)

        root.after(int(duree * 1000), root.destroy)
        root.mainloop()

    thread = threading.Thread(target=show)
    thread.start()
    return thread

IMAGE_ZONE = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\assets\images\zone_copier_comet.png"
IMAGE_COPIER = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\assets\images\copier_comet.png"
LEFT_SCREEN_REGION = (0, 0, 960, 1080)
LEFT_SCREEN_CENTER = (480, 540)
TIMEOUT = 60
CONFIDENCE = 0.6

def test_detection_zone():
    """Teste la detection de la zone sans effectuer d'actions."""
    print("Test detection zone")
    print(f"Image: {IMAGE_ZONE}")
    print(f"Region: {LEFT_SCREEN_REGION}")
    print(f"Confidence: {CONFIDENCE}")
    print("-" * 50)

    try:
        location = pyautogui.locateOnScreen(
            IMAGE_ZONE,
            region=LEFT_SCREEN_REGION,
            confidence=CONFIDENCE
        )
        if location:
            print(f"Zone TROUVEE: {location}")
            print("  Affichage rectangle rouge...")
            afficher_rectangle_rouge(location.left, location.top,
                                    location.width, location.height)
            return location
        else:
            print("Zone non trouvee")
            return None
    except pyautogui.ImageNotFoundException:
        print("Zone non trouvee (exception)")
        return None
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def test_detection_bouton(zone_location):
    """Teste la detection du bouton copier dans une zone."""
    print("\nTest detection bouton copier")
    print(f"Image: {IMAGE_COPIER}")
    print(f"Zone: {zone_location}")
    print("-" * 50)

    sub_region = (
        zone_location.left,
        zone_location.top,
        zone_location.width,
        zone_location.height
    )

    try:
        location = pyautogui.locateOnScreen(
            IMAGE_COPIER,
            region=sub_region,
            confidence=CONFIDENCE
        )
        if location:
            center = pyautogui.center(location)
            print(f"Bouton TROUVE: {location}")
            print(f"Centre: {center}")
            print("  Affichage rectangle rouge...")
            afficher_rectangle_rouge(location.left, location.top,
                                    location.width, location.height)
            print("  Attente 3 secondes...")
            time.sleep(3)
            print(f"  Clic sur le bouton copier ({center})...")
            pyautogui.click(center)
            print("  Clic effectue!")
            return location
        else:
            print("Bouton non trouve")
            return None
    except pyautogui.ImageNotFoundException:
        print("Bouton non trouve (exception)")
        return None
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def test_execute_avec_timeout():
    """Teste la fonction execute avec un timeout."""
    print("\nTest execute avec timeout")
    print(f"Timeout: {TIMEOUT}s")
    print("-" * 50)

    start_time = time.time()
    iteration = 0

    while True:
        iteration += 1
        elapsed = time.time() - start_time

        if elapsed > TIMEOUT:
            print(f"\nTimeout atteint ({TIMEOUT}s)")
            return False

        try:
            zone_location = pyautogui.locateOnScreen(
                IMAGE_ZONE,
                region=LEFT_SCREEN_REGION,
                confidence=CONFIDENCE
            )
            if zone_location:
                print(f"\n[{elapsed:.1f}s] Zone TROUVEE: {zone_location}")
                afficher_rectangle_rouge(zone_location.left, zone_location.top,
                                        zone_location.width, zone_location.height, duree=2)

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
                        print(f"  Bouton copier TROUVE!")
                        print(f"  Position: {copier_location}")
                        print(f"  Centre: {center}")
                        afficher_rectangle_rouge(copier_location.left, copier_location.top,
                                                copier_location.width, copier_location.height, duree=2)
                        print("  Clic en cours...")
                        time.sleep(2)
                        pyautogui.click(center)
                        print("  Clic effectue!")
                        return True
                    else:
                        print(f"[{elapsed:.1f}s] Iter {iteration}: bouton non trouve, scroll...")
                        pyautogui.click(LEFT_SCREEN_CENTER[0], LEFT_SCREEN_CENTER[1])
                        pyautogui.press('pagedown')
                except pyautogui.ImageNotFoundException:
                    print(f"[{elapsed:.1f}s] Iter {iteration}: bouton non trouve, scroll...")
                    pyautogui.click(LEFT_SCREEN_CENTER[0], LEFT_SCREEN_CENTER[1])
                    pyautogui.press('pagedown')
            else:
                if iteration % 10 == 0:
                    print(f"[{elapsed:.1f}s] Iter {iteration}: zone non trouvee, scroll...")
                pyautogui.click(LEFT_SCREEN_CENTER[0], LEFT_SCREEN_CENTER[1])
                pyautogui.press('pagedown')
        except pyautogui.ImageNotFoundException:
            if iteration % 10 == 0:
                print(f"[{elapsed:.1f}s] Iter {iteration}: zone non trouvee, scroll...")
            pyautogui.click(LEFT_SCREEN_CENTER[0], LEFT_SCREEN_CENTER[1])
            pyautogui.press('pagedown')

        time.sleep(0.5)

if __name__ == "__main__":
    print("=" * 50)
    print("TEST ATTENDRE REPONSE COMET")
    print("=" * 50)

    print("\n1. Test detection zone (instantane)")
    zone = test_detection_zone()

    if zone:
        print("\n2. Test detection bouton")
        test_detection_bouton(zone)

    print("\n3. Test execute avec timeout")
    choix = input("Lancer le test execute avec scroll? (o/n): ")
    if choix.lower() == 'o':
        result = test_execute_avec_timeout()
        print(f"\nResultat: {'Succes' if result else 'Echec/Timeout'}")

    print("\nTests termines")
