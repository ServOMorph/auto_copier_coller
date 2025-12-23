import time
import tkinter as tk
import pyautogui

IMAGE_FIN_CONV = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\images\fin_conv_claude.png"
RIGHT_SCREEN_REGION = (960, 0, 960, 1080)
CONFIDENCE = 0.8

def draw_red_rectangle(location, duration=3):
    x, y, w, h = location.left, location.top, location.width, location.height
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.attributes('-transparentcolor', 'white')
    root.geometry(f"{w + 10}x{h + 10}+{x - 5}+{y - 5}")
    canvas = tk.Canvas(root, width=w + 10, height=h + 10, bg='white', highlightthickness=0)
    canvas.pack()
    canvas.create_rectangle(3, 3, w + 7, h + 7, outline='red', width=4)
    root.after(int(duration * 1000), root.destroy)
    root.mainloop()

def execute():
    print("Attente reponse Claude...")
    iteration = 0
    while True:
        iteration += 1
        try:
            location = pyautogui.locateOnScreen(
                IMAGE_FIN_CONV,
                region=RIGHT_SCREEN_REGION,
                confidence=CONFIDENCE
            )
            if location:
                print(f"  Fin de conversation trouvee: {location}")
                draw_red_rectangle(location)
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
