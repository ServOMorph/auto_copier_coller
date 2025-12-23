import time
import keyboard
import pyperclip
from actions import envoie_message_comet, attendre_reponse_comet, envoie_message_claude, attendre_reponse_claude
from config import DELAY

PROMPT_INIT_PATH = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\prompt_init_comet.md"

def main():
    envoie_message_comet.execute()
    time.sleep(DELAY)
    attendre_reponse_comet.execute()
    time.sleep(DELAY)
    envoie_message_claude.execute()
    time.sleep(DELAY * 10)
    attendre_reponse_claude.execute()
    time.sleep(DELAY)

if __name__ == "__main__":
    """with open(PROMPT_INIT_PATH, "r", encoding="utf-8") as f:
        pyperclip.copy(f.read())
    print("Prompt init copie dans le presse-papier")
    print("Appuyez sur ESC pour arreter la boucle")"""
    while True:
        if keyboard.is_pressed('esc'):
            print("Arret demande")
            break
        main()
        time.sleep(DELAY)
