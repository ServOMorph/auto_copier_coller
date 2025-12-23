import time
import keyboard
from actions import envoie_message_comet, attendre_reponse_comet, envoie_message_claude, attendre_reponse_claude
from config import DELAY

def main():
    envoie_message_comet.execute()
    time.sleep(DELAY)
    attendre_reponse_comet.execute()
    envoie_message_claude.execute()
    time.sleep(DELAY * 5)
    attendre_reponse_claude.execute()
    time.sleep(DELAY)

if __name__ == "__main__":
    print("Appuyez sur ESC pour arreter la boucle")
    while True:
        if keyboard.is_pressed('esc'):
            print("Arret demande")
            break
        main()
        time.sleep(DELAY)
