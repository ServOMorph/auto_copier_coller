import tkinter as tk
from tkinter import ttk
from .theme import THEME
from .viewer_md import MarkdownViewer
from outils.logger_echanges import LoggerEchanges


class HistoriqueWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Historique des echanges")
        self.configure(bg=THEME["bg_primary"])
        self.geometry("500x400")
        self.minsize(400, 300)

        self.create_widgets()
        self.load_sessions()

    def create_widgets(self):
        header = tk.Frame(self, bg=THEME["accent_primary"], height=30)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="HISTORIQUE ECHANGES IA",
            font=(THEME["font_family"], THEME["font_size_sm"], "bold"),
            fg=THEME["text_primary"],
            bg=THEME["accent_primary"]
        ).pack(expand=True)

        list_frame = tk.Frame(self, bg=THEME["bg_primary"])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_frame,
            bg=THEME["bg_secondary"],
            fg=THEME["text_primary"],
            font=(THEME["font_family"], THEME["font_size_sm"]),
            selectbackground=THEME["accent_secondary"],
            selectforeground=THEME["bg_primary"],
            activestyle="none",
            relief="flat",
            yscrollcommand=scrollbar.set
        )
        self.listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.bind("<Double-1>", self.on_select)
        self.listbox.bind("<Return>", self.on_select)

        btn_frame = tk.Frame(self, bg=THEME["bg_primary"])
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Button(
            btn_frame,
            text="OUVRIR",
            command=self.open_selected,
            font=(THEME["font_family"], THEME["font_size_xs"], "bold"),
            bg=THEME["accent_secondary"],
            fg=THEME["bg_primary"],
            activebackground=THEME["accent_primary"],
            relief="flat",
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 5))

        tk.Button(
            btn_frame,
            text="RAFRAICHIR",
            command=self.load_sessions,
            font=(THEME["font_family"], THEME["font_size_xs"], "bold"),
            bg=THEME["bg_tertiary"],
            fg=THEME["text_primary"],
            activebackground=THEME["accent_primary"],
            relief="flat",
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 5))

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

        self.info_label = tk.Label(
            self,
            text="Double-cliquez pour ouvrir une session",
            font=(THEME["font_family"], THEME["font_size_xs"]),
            fg=THEME["text_muted"],
            bg=THEME["bg_primary"]
        )
        self.info_label.pack(pady=(0, 5))

    def load_sessions(self):
        self.listbox.delete(0, tk.END)
        self.sessions = LoggerEchanges.get_all_sessions()

        if not self.sessions:
            self.listbox.insert(tk.END, "Aucune session enregistree")
            self.info_label.config(text="Demarrez une session pour enregistrer des echanges")
            return

        for session in self.sessions:
            size_kb = session["size"] / 1024
            display = f"{session['date']} - {session['filename']} ({size_kb:.1f} KB)"
            self.listbox.insert(tk.END, display)

        self.info_label.config(text=f"{len(self.sessions)} session(s) trouvee(s)")

    def on_select(self, event=None):
        self.open_selected()

    def open_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            return

        idx = selection[0]
        if not self.sessions or idx >= len(self.sessions):
            return

        session = self.sessions[idx]
        content = LoggerEchanges.read_session(session["path"])
        MarkdownViewer(self, session["filename"], content)


def open_historique(parent):
    HistoriqueWindow(parent)
