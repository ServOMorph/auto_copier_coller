import time
import pyautogui
import pyperclip
import tkinter as tk
from config import DELAY

IMAGE_INIT = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\init_message_comet.png"
PROMPT_FILE = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\prompt_init_comet.md"
LEFT_SCREEN_REGION = (0, 0, 960, 1080)
CONFIDENCE = 0.6
TIMEOUT = 300


def _afficher_rectangle_rouge(x, y, width, height, duree=None):
    if duree is None:
        duree = DELAY
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.attributes('-transparentcolor', 'white')
    root.overrideredirect(True)
    root.geometry(f"{width + 6}x{height + 6}+{x - 3}+{y - 3}")
    canvas = tk.Canvas(root, width=width + 6, height=height + 6, bg='white', highlightthickness=0)
    canvas.pack()
    canvas.create_rectangle(3, 3, width + 3, height + 3, outline='red', width=3)
    root.after(int(duree * 1000), root.destroy)
    root.mainloop()


def _afficher_croix_rouge(x, y, duree=None):
    if duree is None:
        duree = DELAY
    taille = 30
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.attributes('-transparentcolor', 'white')
    root.overrideredirect(True)
    root.geometry(f"{taille}x{taille}+{x - taille // 2}+{y - taille // 2}")
    canvas = tk.Canvas(root, width=taille, height=taille, bg='white', highlightthickness=0)
    canvas.pack()
    canvas.create_line(0, 0, taille, taille, fill='red', width=4)
    canvas.create_line(taille, 0, 0, taille, fill='red', width=4)
    root.after(int(duree * 1000), root.destroy)
    root.mainloop()


def execute():
    print("Recherche image init_message_comet.png...")
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time

        if elapsed > TIMEOUT:
            print(f"  Timeout atteint ({TIMEOUT}s)")
            return False

        try:
            location = pyautogui.locateOnScreen(
                IMAGE_INIT,
                region=LEFT_SCREEN_REGION,
                confidence=CONFIDENCE
            )

            if location:
                print(f"  [{elapsed:.1f}s] Image trouvee: {location}")

                print(f"  Affichage rectangle rouge et attente {DELAY}s...")
                _afficher_rectangle_rouge(
                    location.left,
                    location.top,
                    location.width,
                    location.height
                )

                location = pyautogui.locateOnScreen(
                    IMAGE_INIT,
                    region=LEFT_SCREEN_REGION,
                    confidence=CONFIDENCE
                )

                if location:
                    center = pyautogui.center(location)
                    print(f"  Affichage croix rouge et attente {DELAY}s avant clic...")
                    _afficher_croix_rouge(center.x, center.y)

                    print(f"  Clic sur {center}")
                    pyautogui.click(center)
                    time.sleep(DELAY)

                    print(f"  Copie du fichier prompt_init_comet.md...")
                    with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
                        contenu = f.read()
                    pyperclip.copy(contenu)
                    time.sleep(DELAY)

                    print(f"  Colle le contenu (Ctrl+V)...")
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(DELAY)

                    print(f"  Appui sur Entree...")
                    pyautogui.press('enter')

                    print("  Lancement termine avec succes")
                    return True
                else:
                    print("  Image disparue apres attente, nouvelle recherche...")

        except pyautogui.ImageNotFoundException:
            pass

        time.sleep(0.5)


if __name__ == "__main__":
    execute()
