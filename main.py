import time
import keyboard
import sys
from actions import envoie_message_comet, attendre_reponse_comet, envoie_message_claude, attendre_reponse_claude
import lancement
from config import DELAY
from outils.logger import log, log_wait, reset_timer

_cycle_count = 0

def main():
    global _cycle_count
    _cycle_count += 1
    reset_timer()
    log(f"========== CYCLE {_cycle_count} ==========")

    envoie_message_comet.execute()
    attendre_reponse_comet.execute()
    log_wait(DELAY, "entre Comet et Claude")
    time.sleep(DELAY)
    envoie_message_claude.execute()
    attendre_reponse_claude.execute()
    log_wait(DELAY, "fin de cycle")
    time.sleep(DELAY)
    log(f"========== FIN CYCLE {_cycle_count} ==========")


def run_console_mode():
    print("Appuyez sur ESC pour arreter la boucle")
    time.sleep(DELAY)
    while True:
        if keyboard.is_pressed('esc'):
            print("Arret demande")
            break
        main()
        time.sleep(DELAY)


def run_gui_mode():
    from gui.app import run_gui
    run_gui()


if __name__ == "__main__":
    if "--console" in sys.argv or "-c" in sys.argv:
        run_console_mode()
    else:
        run_gui_mode()
