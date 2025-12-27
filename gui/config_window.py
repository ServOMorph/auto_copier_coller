import tkinter as tk
from tkinter import ttk
from .theme import THEME
import config

CONFIG_ITEMS = [
    ("DELAIS COMMUNS", None),
    ("DELAY", "Delai general entre etapes", "float"),
    ("DELAY_IMAGE_SEARCH_LOOP", "Delai recherche image", "float"),
    ("DELAY_KEY_PRESS", "Duree appui touche", "float"),
    ("DELAY_PAUSE_POLLING", "Delai polling pause", "float"),
    ("DELAY_BEFORE_PASTE", "Delai avant CTRL+V", "float"),
    ("DELAY_AFTER_PASTE", "Delai apres CTRL+V", "float"),
    ("DELAY_BEFORE_CLICK_COPY", "Delai avant clic copier", "float"),
    ("DELAY_BEFORE_COPY_RESPONSE", "Delai avant copie reponse", "float"),

    ("MODE COMET/CLAUDE", None),
    ("DELAY_PAGE_DOWN", "Delai entre Page Down", "float"),
    ("SCROLL_PAGE_DOWN_COUNT", "Nombre de scrolls", "int"),
    ("TIMEOUT_ATTENTE_COMET", "Timeout Comet (s)", "int"),

    ("MODE ORCH/DEV", None),
    ("TIMEOUT_ATTENTE_CLAUDE", "Timeout Claude (s)", "int"),
    ("STARTORCH_COMMAND", "Commande Orch", "str"),
    ("STARTDEV_COMMAND", "Commande Dev", "str"),

    ("MODE CLAUDE SOLO", None),
    ("DELAY_CLAUDE_SOLO_END", "Delai fin workflow", "float"),
]


class ConfigWindow(tk.Toplevel):
    def __init__(self, parent, on_save_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.on_save_callback = on_save_callback
        self.entries = {}
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.title("Configuration")
        self.configure(bg=THEME["bg_primary"])
        self.transient(self.parent)
        self.grab_set()

        width = 420
        height = 620
        x = self.parent.winfo_x() + 50
        y = self.parent.winfo_y() - 100
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(400, 550)

    def create_widgets(self):
        main_frame = tk.Frame(self, bg=THEME["bg_primary"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(main_frame, bg=THEME["bg_primary"], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg=THEME["bg_primary"])

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        for item in CONFIG_ITEMS:
            if item[1] is None:
                self.create_section_header(item[0])
            else:
                self.create_config_row(item[0], item[1], item[2])

        btn_frame = tk.Frame(self, bg=THEME["bg_primary"])
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        save_btn = tk.Button(
            btn_frame,
            text="APPLIQUER",
            command=self.apply_config,
            font=(THEME["font_family"], THEME["font_size_xs"], "bold"),
            bg=THEME["accent_secondary"],
            fg=THEME["bg_primary"],
            activebackground=THEME["accent_primary"],
            relief="flat",
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        reset_btn = tk.Button(
            btn_frame,
            text="RESET",
            command=self.reset_config,
            font=(THEME["font_family"], THEME["font_size_xs"], "bold"),
            bg=THEME["bg_tertiary"],
            fg=THEME["text_secondary"],
            activebackground=THEME["accent_primary"],
            relief="flat",
            cursor="hand2"
        )
        reset_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 5))

        quit_btn = tk.Button(
            btn_frame,
            text="QUITTER",
            command=self.destroy,
            font=(THEME["font_family"], THEME["font_size_xs"], "bold"),
            bg=THEME["alert_color"],
            fg=THEME["text_primary"],
            activebackground=THEME["accent_primary"],
            relief="flat",
            cursor="hand2"
        )
        quit_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

    def create_section_header(self, title):
        header = tk.Label(
            self.scroll_frame,
            text=title,
            font=(THEME["font_family"], THEME["font_size_xs"], "bold"),
            fg=THEME["accent_secondary"],
            bg=THEME["bg_primary"],
            anchor="w",
            pady=8
        )
        header.pack(fill=tk.X)

    def create_config_row(self, key, label, value_type):
        row = tk.Frame(self.scroll_frame, bg=THEME["bg_secondary"], pady=3, padx=5)
        row.pack(fill=tk.X, pady=1)

        lbl = tk.Label(
            row,
            text=label,
            font=(THEME["font_family"], THEME["font_size_xs"]),
            fg=THEME["text_secondary"],
            bg=THEME["bg_secondary"],
            anchor="w",
            width=22
        )
        lbl.pack(side=tk.LEFT)

        current_value = getattr(config, key, "")

        entry = tk.Entry(
            row,
            font=(THEME["font_family"], THEME["font_size_xs"]),
            bg=THEME["bg_tertiary"],
            fg=THEME["text_primary"],
            insertbackground=THEME["text_primary"],
            relief="flat",
            width=12
        )
        entry.insert(0, str(current_value))
        entry.pack(side=tk.RIGHT, padx=(5, 0))

        self.entries[key] = (entry, value_type)

    def apply_config(self):
        for key, (entry, value_type) in self.entries.items():
            try:
                value = entry.get().strip()
                if value_type == "float":
                    setattr(config, key, float(value))
                elif value_type == "int":
                    setattr(config, key, int(value))
                else:
                    setattr(config, key, value)
            except ValueError:
                pass

        self.update_aliases()

        if self.on_save_callback:
            self.on_save_callback()

        self.destroy()

    def update_aliases(self):
        config.DELAY_BEFORE_MAIN = config.DELAY
        config.DELAY_BEFORE_PASTE_COMET = config.DELAY_BEFORE_PASTE
        config.DELAY_AFTER_PASTE_COMET = config.DELAY_AFTER_PASTE
        config.DELAY_BEFORE_CLICK_COMET = config.DELAY_BEFORE_CLICK_COPY
        config.DELAY_BEFORE_PASTE_CLAUDE = config.DELAY_BEFORE_PASTE
        config.DELAY_AFTER_PASTE_CLAUDE = config.DELAY_AFTER_PASTE

    def reset_config(self):
        defaults = {
            "DELAY": 1,
            "DELAY_IMAGE_SEARCH_LOOP": 1,
            "DELAY_KEY_PRESS": 0.5,
            "DELAY_PAUSE_POLLING": 0.2,
            "DELAY_BEFORE_PASTE": 2,
            "DELAY_AFTER_PASTE": 2,
            "DELAY_BEFORE_CLICK_COPY": 1,
            "DELAY_BEFORE_COPY_RESPONSE": 2,
            "DELAY_PAGE_DOWN": 2,
            "SCROLL_PAGE_DOWN_COUNT": 5,
            "TIMEOUT_ATTENTE_COMET": 600,
            "TIMEOUT_ATTENTE_CLAUDE": 300,
            "STARTORCH_COMMAND": "/startorch",
            "STARTDEV_COMMAND": "/startdev",
            "DELAY_CLAUDE_SOLO_END": 2,
        }

        for key, (entry, value_type) in self.entries.items():
            if key in defaults:
                entry.delete(0, tk.END)
                entry.insert(0, str(defaults[key]))


def open_config(parent, on_save_callback=None):
    ConfigWindow(parent, on_save_callback)
