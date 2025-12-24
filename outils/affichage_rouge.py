import tkinter as tk
import threading
from config import DELAY


def _afficher_rectangle_thread(x, y, width, height, duree):
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


def afficher_rectangle(x, y, width, height, duree=None):
    if duree is None:
        duree = DELAY
    thread = threading.Thread(target=_afficher_rectangle_thread, args=(x, y, width, height, duree), daemon=True)
    thread.start()


def _afficher_croix_thread(x, y, duree):
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


def afficher_croix(x, y, duree=None):
    if duree is None:
        duree = DELAY
    thread = threading.Thread(target=_afficher_croix_thread, args=(x, y, duree), daemon=True)
    thread.start()


def _afficher_texte_action_thread(texte, duree):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.attributes('-transparentcolor', 'white')
    root.overrideredirect(True)

    label = tk.Label(root, text=texte, font=('Arial', 24, 'bold'), fg='red', bg='white')
    label.pack(padx=10, pady=5)
    root.update_idletasks()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"+{x}+{y}")

    root.after(int(duree * 1000), root.destroy)
    root.mainloop()


def afficher_texte_action(texte, duree=None):
    if duree is None:
        duree = DELAY
    thread = threading.Thread(target=_afficher_texte_action_thread, args=(texte, duree), daemon=True)
    thread.start()
