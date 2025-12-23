import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from actions import attendre_reponse_claude
from actions import envoie_message_comet

def main():
    print("=== Test: attendre_reponse_claude puis envoie_message_comet ===")

    print("\n1. Attente reponse Claude...")
    result = attendre_reponse_claude.execute()

    if result:
        print("\n2. Reponse Claude detectee, envoi message Comet...")
        envoie_message_comet.execute()
        print("\n=== Test termine ===")
    else:
        print("\n=== Echec: reponse Claude non detectee ===")

if __name__ == "__main__":
    main()
