import tkinter as tk
from tkinter import ttk
import re
from .theme import THEME


class MarkdownViewer(tk.Toplevel):
    def __init__(self, parent, title: str, content: str):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=THEME["bg_primary"])
        self.geometry("800x600")
        self.minsize(600, 400)

        self.create_widgets(content)

    def create_widgets(self, content: str):
        header = tk.Frame(self, bg=THEME["accent_primary"], height=30)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="VISUALISEUR ECHANGES",
            font=(THEME["font_family"], THEME["font_size_sm"], "bold"),
            fg=THEME["text_primary"],
            bg=THEME["accent_primary"]
        ).pack(expand=True)

        container = tk.Frame(self, bg=THEME["bg_primary"])
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text = tk.Text(
            container,
            wrap=tk.WORD,
            bg=THEME["bg_secondary"],
            fg=THEME["text_primary"],
            font=(THEME["font_family"], THEME["font_size_base"]),
            padx=15,
            pady=15,
            yscrollcommand=scrollbar.set,
            relief="flat",
            cursor="arrow"
        )
        self.text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text.yview)

        self._configure_tags()
        self._render_markdown(content)
        self.text.config(state=tk.DISABLED)

        btn_frame = tk.Frame(self, bg=THEME["bg_primary"])
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Button(
            btn_frame,
            text="FERMER",
            command=self.destroy,
            font=(THEME["font_family"], THEME["font_size_xs"], "bold"),
            bg=THEME["bg_tertiary"],
            fg=THEME["text_primary"],
            activebackground=THEME["accent_primary"],
            relief="flat",
            cursor="hand2"
        ).pack(side=tk.RIGHT)

    def _configure_tags(self):
        self.text.tag_configure("h1", font=(THEME["font_family"], 20, "bold"), foreground=THEME["accent_secondary"])
        self.text.tag_configure("h2", font=(THEME["font_family"], 16, "bold"), foreground=THEME["text_accent"])
        self.text.tag_configure("h3", font=(THEME["font_family"], 14, "bold"), foreground=THEME["text_primary"])
        self.text.tag_configure("bold", font=(THEME["font_family"], THEME["font_size_base"], "bold"))
        self.text.tag_configure("code", font=("Consolas", THEME["font_size_sm"]), background=THEME["bg_tertiary"], foreground="#98c379")
        self.text.tag_configure("comet", foreground="#ff9500", font=(THEME["font_family"], THEME["font_size_base"], "bold"))
        self.text.tag_configure("claude", foreground="#8b5cf6", font=(THEME["font_family"], THEME["font_size_base"], "bold"))
        self.text.tag_configure("chatgpt", foreground="#10a37f", font=(THEME["font_family"], THEME["font_size_base"], "bold"))
        self.text.tag_configure("separator", foreground=THEME["text_muted"])

    def _render_markdown(self, content: str):
        lines = content.split("\n")
        in_code_block = False

        for line in lines:
            if line.startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                self.text.insert(tk.END, line + "\n", "code")
                continue

            if line.startswith("# "):
                self.text.insert(tk.END, line[2:] + "\n\n", "h1")
            elif line.startswith("## "):
                text = line[3:]
                if "COMET" in text.upper():
                    self.text.insert(tk.END, text + "\n\n", "comet")
                elif "CLAUDE" in text.upper():
                    self.text.insert(tk.END, text + "\n\n", "claude")
                elif "CHATGPT" in text.upper():
                    self.text.insert(tk.END, text + "\n\n", "chatgpt")
                else:
                    self.text.insert(tk.END, text + "\n\n", "h2")
            elif line.startswith("### "):
                self.text.insert(tk.END, line[4:] + "\n\n", "h3")
            elif line.startswith("---"):
                self.text.insert(tk.END, "-" * 60 + "\n\n", "separator")
            elif line.startswith("**") and "**:" in line:
                parts = line.split("**")
                if len(parts) >= 2:
                    self.text.insert(tk.END, parts[1], "bold")
                    self.text.insert(tk.END, "".join(parts[2:]) + "\n")
            else:
                self.text.insert(tk.END, line + "\n")
