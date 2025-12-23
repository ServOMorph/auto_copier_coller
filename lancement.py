import pyperclip
from pathlib import Path


def execute():
    prompt_path = Path(r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\prompt_init_comet.md")

    contenu = prompt_path.read_text(encoding="utf-8")
    pyperclip.copy(contenu)

    print("Prompt copié dans le presse-papier.")


if __name__ == "__main__":
    execute()
