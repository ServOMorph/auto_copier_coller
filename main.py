from actions import envoie_message_comet, attendre_reponse_comet

def main():
    envoie_message_comet.execute()
    attendre_reponse_comet.execute()

if __name__ == "__main__":
    main()
