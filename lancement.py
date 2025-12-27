import pyperclip
from pathlib import Path
import config


def execute():
    prompt_path = Path(config.PROMPT_PATH)

    contenu = prompt_path.read_text(encoding="utf-8")
    pyperclip.copy(contenu)

    print(f"Prompt copie: {prompt_path.name}")


if __name__ == "__main__":
    execute()
