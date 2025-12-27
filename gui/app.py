import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime
import threading
import json
from pathlib import Path
from .theme import THEME
from .process_controller import ProcessController
from .historique import open_historique
from .config_window import open_config
import config

PREFS_FILE = Path(__file__).parent.parent / "user_prefs.json"


class AutoCopierGUI(tk.Tk):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller or ProcessController()
        self.click_yes_active = False
        self.click_yes_thread = None
        self.mode_var = None
        self.load_prefs()
        self.setup_window()
        self.create_widgets()
        self.bind_events()
        self.update_timer_id = None

    def load_prefs(self):
        if PREFS_FILE.exists():
            try:
                prefs = json.loads(PREFS_FILE.read_text(encoding="utf-8"))
                config.PROMPT_PATH = prefs.get("prompt_path", config.PROMPT_PATH)
                cfg = prefs.get("config", {})
                for key, value in cfg.items():
                    if hasattr(config, key):
                        setattr(config, key, value)
                self._update_config_aliases()
            except Exception:
                pass

    def save_prefs(self):
        prefs = {
            "prompt_path": config.PROMPT_PATH,
            "config": {
                "DELAY": config.DELAY,
                "DELAY_IMAGE_SEARCH_LOOP": config.DELAY_IMAGE_SEARCH_LOOP,
                "DELAY_KEY_PRESS": config.DELAY_KEY_PRESS,
                "DELAY_PAUSE_POLLING": config.DELAY_PAUSE_POLLING,
                "DELAY_BEFORE_PASTE": config.DELAY_BEFORE_PASTE,
                "DELAY_AFTER_PASTE": config.DELAY_AFTER_PASTE,
                "DELAY_BEFORE_CLICK_COPY": config.DELAY_BEFORE_CLICK_COPY,
                "DELAY_BEFORE_COPY_RESPONSE": config.DELAY_BEFORE_COPY_RESPONSE,
                "DELAY_PAGE_DOWN": config.DELAY_PAGE_DOWN,
                "SCROLL_PAGE_DOWN_COUNT": config.SCROLL_PAGE_DOWN_COUNT,
                "TIMEOUT_ATTENTE_COMET": config.TIMEOUT_ATTENTE_COMET,
                "TIMEOUT_ATTENTE_CLAUDE": config.TIMEOUT_ATTENTE_CLAUDE,
                "STARTORCH_COMMAND": config.STARTORCH_COMMAND,
                "STARTDEV_COMMAND": config.STARTDEV_COMMAND,
                "DELAY_CLAUDE_SOLO_END": config.DELAY_CLAUDE_SOLO_END,
            }
        }
        PREFS_FILE.write_text(json.dumps(prefs, indent=2), encoding="utf-8")

    def _update_config_aliases(self):
        config.DELAY_BEFORE_MAIN = config.DELAY
        config.DELAY_BEFORE_PASTE_COMET = config.DELAY_BEFORE_PASTE
        config.DELAY_AFTER_PASTE_COMET = config.DELAY_AFTER_PASTE
        config.DELAY_BEFORE_CLICK_COMET = config.DELAY_BEFORE_CLICK_COPY
        config.DELAY_BEFORE_PASTE_CLAUDE = config.DELAY_BEFORE_PASTE
        config.DELAY_AFTER_PASTE_CLAUDE = config.DELAY_AFTER_PASTE

    def select_prompt_file(self):
        initial_dir = Path(config.PROMPT_PATH).parent
        initial_file = Path(config.PROMPT_PATH).name
        filepath = filedialog.askopenfilename(
            title="Selectionner le prompt init Comet",
            initialdir=initial_dir,
            initialfile=initial_file,
            filetypes=[("Markdown", "*.md"), ("Tous fichiers", "*.*")]
        )
        if filepath:
            config.PROMPT_PATH = filepath
            self.save_prefs()
            return True
        return False

    def setup_window(self):
        self.title("Auto Copier Coller")
        self.configure(bg=THEME["bg_primary"])
        self.position_center()
        self.minsize(200, 200)
        self.attributes("-topmost", False)

    def position_center(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = screen_width // 5
        window_height = screen_height // 3
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def create_widgets(self):
        self.create_header()
        self.create_mode_selector()
        self.create_status_section()
        self.create_control_section()
        self.create_click_yes_button()
        self.create_historique_button()
        self.create_info_section()
        self.create_footer()

    def create_header(self):
        self.header = tk.Frame(self, bg=THEME["accent_primary"], height=25)
        self.header.pack(fill=tk.X, side=tk.TOP)
        self.header.pack_propagate(False)

        self.header_label = tk.Label(
            self.header,
            text="AUTO COPIER",
            font=(THEME["font_family"], THEME["font_size_sm"], "bold"),
            fg=THEME["text_primary"],
            bg=THEME["accent_primary"]
        )
        self.header_label.pack(expand=True)

    def create_mode_selector(self):
        self.mode_frame = tk.Frame(self, bg=THEME["bg_secondary"], padx=5, pady=3)
        self.mode_frame.pack(fill=tk.X, padx=5, pady=(3, 2))

        self.mode_label = tk.Label(
            self.mode_frame,
            text="MODE:",
            font=(THEME["font_family"], THEME["font_size_xs"], "bold"),
            fg=THEME["text_secondary"],
            bg=THEME["bg_secondary"],
            anchor="w"
        )
        self.mode_label.pack(fill=tk.X)

        self.mode_var = tk.StringVar(value="comet_claude")

        self.mode_btn_frame = tk.Frame(self.mode_frame, bg=THEME["bg_secondary"])
        self.mode_btn_frame.pack(fill=tk.X, pady=(2, 0))

        self.mode_comet_btn = tk.Radiobutton(
            self.mode_btn_frame,
            text="Comet <-> Claude",
            variable=self.mode_var,
            value="comet_claude",
            font=(THEME["font_family"], THEME["font_size_xs"]),
            fg=THEME["text_primary"],
            bg=THEME["bg_secondary"],
            selectcolor=THEME["bg_tertiary"],
            activebackground=THEME["bg_secondary"],
            activeforeground=THEME["text_primary"],
            anchor="w",
            command=self.on_mode_change
        )
        self.mode_comet_btn.pack(fill=tk.X)

        self.mode_orch_btn = tk.Radiobutton(
            self.mode_btn_frame,
            text="Orch <-> Dev",
            variable=self.mode_var,
            value="orch_dev",
            font=(THEME["font_family"], THEME["font_size_xs"]),
            fg=THEME["text_primary"],
            bg=THEME["bg_secondary"],
            selectcolor=THEME["bg_tertiary"],
            activebackground=THEME["bg_secondary"],
            activeforeground=THEME["text_primary"],
            anchor="w",
            command=self.on_mode_change
        )
        self.mode_orch_btn.pack(fill=tk.X)

        self.mode_solo_btn = tk.Radiobutton(
            self.mode_btn_frame,
            text="Claude Solo",
            variable=self.mode_var,
            value="claude_solo",
            font=(THEME["font_family"], THEME["font_size_xs"]),
            fg=THEME["text_primary"],
            bg=THEME["bg_secondary"],
            selectcolor=THEME["bg_tertiary"],
            activebackground=THEME["bg_secondary"],
            activeforeground=THEME["text_primary"],
            anchor="w",
            command=self.on_mode_change
        )
        self.mode_solo_btn.pack(fill=tk.X)

    def on_mode_change(self):
        mode = self.mode_var.get()
        if mode == "comet_claude":
            self.header_label.config(text="COMET <-> CLAUDE")
        elif mode == "orch_dev":
            self.header_label.config(text="ORCH <-> DEV")
        else:
            self.header_label.config(text="CLAUDE SOLO")

    def get_current_mode(self):
        return self.mode_var.get()

    def create_status_section(self):
        self.status_frame = tk.Frame(self, bg=THEME["bg_secondary"], padx=5, pady=3)
        self.status_frame.pack(fill=tk.X, padx=5, pady=(3, 2))

        self.status_indicator = tk.Label(
            self.status_frame,
            text="ARRETE",
            font=(THEME["font_family"], THEME["font_size_xs"], "bold"),
            fg=THEME["text_muted"],
            bg=THEME["bg_secondary"],
            anchor="w"
        )
        self.status_indicator.pack(fill=tk.X)

        self.step_label = tk.Label(
            self.status_frame,
            text="-",
            font=(THEME["font_family"], THEME["font_size_xs"]),
            fg=THEME["text_secondary"],
            bg=THEME["bg_secondary"],
            anchor="w"
        )
        self.step_label.pack(fill=tk.X)

    def create_control_section(self):
        self.control_frame = tk.Frame(self, bg=THEME["bg_primary"])
        self.control_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)

        self.start_btn = tk.Button(
            self.control_frame,
            text="START",
            command=self.start_process,
            font=(THEME["font_family"], THEME["font_size_xs"], "bold"),
            bg=THEME["accent_secondary"],
            fg=THEME["bg_primary"],
            activebackground=THEME["accent_primary"],
            activeforeground=THEME["text_primary"],
            relief="flat",
            cursor="hand2"
        )
        self.start_btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 2))

        self.pause_btn = tk.Button(
            self.control_frame,
            text="PAUSE",
            command=self.toggle_pause,
            font=(THEME["font_family"], THEME["font_size_xs"], "bold"),
            bg=THEME["bg_tertiary"],
            fg=THEME["text_secondary"],
            activebackground=THEME["accent_primary"],
            activeforeground=THEME["text_primary"],
            relief="flat",
            cursor="hand2",
            state=tk.DISABLED
        )
        self.pause_btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(2, 0))

    def create_click_yes_button(self):
        self.click_yes_frame = tk.Frame(self, bg=THEME["bg_primary"])
        self.click_yes_frame.pack(fill=tk.X, padx=5, pady=(0, 3))

        self.click_yes_btn = tk.Button(
            self.click_yes_frame,
            text="CLICK YES: OFF",
            command=self.toggle_click_yes,
            font=(THEME["font_family"], THEME["font_size_xs"]),
            bg=THEME["bg_tertiary"],
            fg=THEME["text_secondary"],
            activebackground=THEME["accent_primary"],
            activeforeground=THEME["text_primary"],
            relief="flat",
            cursor="hand2"
        )
        self.click_yes_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.auto_stop_var = tk.BooleanVar(value=False)
        self.auto_stop_cb = tk.Checkbutton(
            self.click_yes_frame,
            text="Auto",
            variable=self.auto_stop_var,
            font=(THEME["font_family"], THEME["font_size_xs"]),
            fg=THEME["text_secondary"],
            bg=THEME["bg_primary"],
            selectcolor=THEME["bg_tertiary"],
            activebackground=THEME["bg_primary"],
            activeforeground=THEME["text_primary"]
        )
        self.auto_stop_cb.pack(side=tk.RIGHT, padx=(3, 0))

    def toggle_click_yes(self):
        if not self.click_yes_active:
            self.start_click_yes()
        else:
            self.stop_click_yes()

    def start_click_yes(self):
        import click_yes
        click_yes.stop_requested = False
        click_yes.auto_stop_on_input = self.auto_stop_var.get()
        self.click_yes_active = True
        self.click_yes_btn.config(
            text="CLICK YES: ON",
            bg=THEME["success_color"],
            fg=THEME["bg_primary"]
        )
        self.click_yes_thread = threading.Thread(target=self._run_click_yes, daemon=True)
        self.click_yes_thread.start()

    def _run_click_yes(self):
        import click_yes
        try:
            click_yes.main(poll_interval=0.5)
        except Exception:
            pass
        self.after(0, self._on_click_yes_stopped)

    def _on_click_yes_stopped(self):
        self.click_yes_active = False
        self.click_yes_btn.config(
            text="CLICK YES: OFF",
            bg=THEME["bg_tertiary"],
            fg=THEME["text_secondary"]
        )

    def stop_click_yes(self):
        import click_yes
        click_yes.stop_requested = True
        self.click_yes_active = False
        self.click_yes_btn.config(
            text="CLICK YES: OFF",
            bg=THEME["bg_tertiary"],
            fg=THEME["text_secondary"]
        )

    def create_historique_button(self):
        self.btn_row_frame = tk.Frame(self, bg=THEME["bg_primary"])
        self.btn_row_frame.pack(fill=tk.X, padx=5, pady=(0, 3))

        self.hist_btn = tk.Button(
            self.btn_row_frame,
            text="HISTORIQUE",
            command=lambda: open_historique(self),
            font=(THEME["font_family"], THEME["font_size_xs"]),
            bg=THEME["bg_tertiary"],
            fg=THEME["text_secondary"],
            activebackground=THEME["accent_primary"],
            activeforeground=THEME["text_primary"],
            relief="flat",
            cursor="hand2"
        )
        self.hist_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        self.config_btn = tk.Button(
            self.btn_row_frame,
            text="CONFIG",
            command=self.open_config_window,
            font=(THEME["font_family"], THEME["font_size_xs"]),
            bg=THEME["bg_tertiary"],
            fg=THEME["text_secondary"],
            activebackground=THEME["accent_primary"],
            activeforeground=THEME["text_primary"],
            relief="flat",
            cursor="hand2"
        )
        self.config_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

    def open_config_window(self):
        open_config(self, self.on_config_saved)

    def on_config_saved(self):
        self.save_prefs()

    def create_info_section(self):
        self.info_frame = tk.Frame(self, bg=THEME["bg_tertiary"], padx=5, pady=2)
        self.info_frame.pack(fill=tk.X, padx=5, pady=(0, 3))

        self.info_label = tk.Label(
            self.info_frame,
            text="C:0 | 00:00:00",
            font=(THEME["font_family"], THEME["font_size_xs"]),
            fg=THEME["text_secondary"],
            bg=THEME["bg_tertiary"]
        )
        self.info_label.pack()

    def create_footer(self):
        self.footer = tk.Label(
            self,
            text="@Je Geek Utile",
            font=(THEME["font_family"], 9),
            fg=THEME["text_accent"],
            bg=THEME["bg_tertiary"],
            pady=2
        )
        self.footer.pack(fill=tk.X, side=tk.BOTTOM)

    def bind_events(self):
        self.bind("<Escape>", self.on_escape)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_escape(self, event=None):
        self.stop_process()

    def on_close(self):
        self.stop_process()
        self.stop_click_yes()
        self.destroy()

    def start_process(self):
        mode = self.get_current_mode()
        if mode == "comet_claude":
            self._start_comet_claude()
        elif mode == "orch_dev":
            self._start_orch_dev()
        else:
            self._start_claude_solo()

    def _start_comet_claude(self):
        if not self.select_prompt_file():
            return

        from actions.comet_claude import envoie_message_comet, attendre_reponse_comet
        from actions.comet_claude import envoie_message_claude, attendre_reponse_claude
        from config import DELAY, DELAY_BEFORE_MAIN
        from outils.logger_echanges import logger
        import lancement
        import time
        import keyboard
        import pyperclip

        def startup_sequence(controller, gui_callback):
            gui_callback("step", "Lancement init...", -1)
            lancement.execute()
            time.sleep(DELAY_BEFORE_MAIN)
            main_loop(controller, gui_callback)

        def main_loop(controller, gui_callback):
            logger.start_session()

            steps = [
                (envoie_message_comet.execute, "Envoi message Comet", DELAY, "USER", "COMET"),
                (attendre_reponse_comet.execute, "Attente reponse Comet", DELAY, "COMET", "CLAUDE"),
                (envoie_message_claude.execute, "Envoi message Claude", DELAY, "COMET", "CLAUDE"),
                (attendre_reponse_claude.execute, "Attente reponse Claude", DELAY, "CLAUDE", "COMET"),
            ]

            while controller.running:
                if keyboard.is_pressed('esc'):
                    controller.running = False
                    break

                for i, (step_func, step_name, delay, src, dest) in enumerate(steps):
                    if not controller.running:
                        break

                    controller.current_step = i
                    gui_callback("step", step_name, i)

                    if not controller.wait_if_paused():
                        logger.end_session()
                        return

                    try:
                        clipboard_before = pyperclip.paste()
                        step_func()
                        clipboard_after = pyperclip.paste()
                        if clipboard_after != clipboard_before:
                            logger.log_message(src, dest, clipboard_after, step_name)
                    except Exception as e:
                        gui_callback("error", str(e), i)
                        logger.log_message("SYSTEM", "ERROR", str(e), "ERREUR")

                    time.sleep(delay)

                    if not controller.wait_if_paused():
                        logger.end_session()
                        return

                controller.cycle_count += 1
                gui_callback("cycle", "", controller.cycle_count)
                time.sleep(DELAY)

            logger.end_session()

        self.controller.start(startup_sequence, self.gui_callback)
        self.update_ui_started()
        self.start_timer_update()

    def _start_orch_dev(self):
        from actions.orch_dev import envoie_message_orch, envoie_message_dev
        from actions.orch_dev import attendre_reponse_orch, attendre_reponse_dev
        from config import DELAY, STARTORCH_COMMAND, DELAY_BEFORE_COPY_RESPONSE
        from outils.logger_echanges import logger
        from outils.logger import log, log_wait, log_action
        from outils.affichage_rouge import afficher_texte_action
        import time
        import keyboard
        import pyperclip

        def startup_sequence(controller, gui_callback):
            gui_callback("step", "Init Orch...", -1)
            log("=== INITIALISATION ORCH/DEV ===")
            log_action("COPY_COMMAND", f"copie commande {STARTORCH_COMMAND}")
            afficher_texte_action("COPY /startorch")
            log_wait(DELAY_BEFORE_COPY_RESPONSE, "avant copie commande")
            time.sleep(DELAY_BEFORE_COPY_RESPONSE)
            pyperclip.copy(STARTORCH_COMMAND)
            log(f"Commande copiee: {STARTORCH_COMMAND}")
            envoie_message_orch.execute()
            attendre_reponse_orch.execute()
            main_loop(controller, gui_callback)

        def main_loop(controller, gui_callback):
            logger.start_session()

            steps = [
                (envoie_message_dev.execute, "Envoi msg Dev", DELAY, "ORCH", "DEV"),
                (attendre_reponse_dev.execute, "Attente Dev", DELAY, "DEV", "ORCH"),
                (envoie_message_orch.execute, "Envoi msg Orch", DELAY, "DEV", "ORCH"),
                (attendre_reponse_orch.execute, "Attente Orch", DELAY, "ORCH", "DEV"),
            ]

            while controller.running:
                if keyboard.is_pressed('esc'):
                    controller.running = False
                    break

                for i, (step_func, step_name, delay, src, dest) in enumerate(steps):
                    if not controller.running:
                        break

                    controller.current_step = i
                    gui_callback("step", step_name, i)

                    if not controller.wait_if_paused():
                        logger.end_session()
                        return

                    try:
                        clipboard_before = pyperclip.paste()
                        step_func()
                        clipboard_after = pyperclip.paste()
                        if clipboard_after != clipboard_before:
                            logger.log_message(src, dest, clipboard_after, step_name)
                    except Exception as e:
                        gui_callback("error", str(e), i)
                        logger.log_message("SYSTEM", "ERROR", str(e), "ERREUR")

                    time.sleep(delay)

                    if not controller.wait_if_paused():
                        logger.end_session()
                        return

                controller.cycle_count += 1
                gui_callback("cycle", "", controller.cycle_count)
                time.sleep(DELAY)

            logger.end_session()

        self.controller.start(startup_sequence, self.gui_callback)
        self.update_ui_started()
        self.start_timer_update()

    def _start_claude_solo(self):
        from actions.claude_solo import boucle_claude_solo
        from config import DELAY
        from outils.logger import log
        import time
        import keyboard

        def main_loop(controller, gui_callback):
            log("=== DEMARRAGE CLAUDE SOLO ===")

            while controller.running:
                if keyboard.is_pressed('esc'):
                    controller.running = False
                    break

                gui_callback("step", "Attente fin conv", 0)

                if not controller.wait_if_paused():
                    return

                try:
                    result = boucle_claude_solo.execute()
                    if result:
                        controller.cycle_count += 1
                        gui_callback("cycle", "", controller.cycle_count)
                except Exception as e:
                    gui_callback("error", str(e), 0)
                    log(f"Erreur: {e}")

                time.sleep(DELAY)

                if not controller.wait_if_paused():
                    return

            log("=== FIN CLAUDE SOLO ===")

        self.controller.start(main_loop, self.gui_callback)
        self.update_ui_started()
        self.start_timer_update()

    def stop_process(self):
        self.controller.stop()
        self.update_ui_stopped()
        self.stop_timer_update()

    def toggle_pause(self):
        is_paused = self.controller.toggle_pause()
        if is_paused:
            self.pause_btn.config(
                text="PLAY",
                bg=THEME["success_color"],
                fg=THEME["bg_primary"]
            )
            self.status_indicator.config(
                text="PAUSE",
                fg=THEME["warning_color"]
            )
        else:
            self.pause_btn.config(
                text="PAUSE",
                bg=THEME["bg_tertiary"],
                fg=THEME["text_secondary"]
            )
            self.status_indicator.config(
                text="EN COURS",
                fg=THEME["success_color"]
            )

    def gui_callback(self, event_type, data, extra=None):
        self.after(0, lambda: self._handle_callback(event_type, data, extra))

    def _handle_callback(self, event_type, data, extra):
        if event_type == "step":
            step_num = extra + 1
            mode = self.get_current_mode()
            if mode == "claude_solo":
                self.step_label.config(text=data[:20])
            else:
                self.step_label.config(text=f"{step_num}/4: {data[:15]}")
        elif event_type == "cycle":
            pass
        elif event_type == "error":
            self.status_indicator.config(
                text="ERREUR",
                fg=THEME["alert_color"]
            )
        elif event_type == "stop_image":
            self.update_ui_stopped()
            self.stop_timer_update()
            self.status_indicator.config(
                text="STOP IMAGE",
                fg=THEME["alert_color"]
            )
            self.step_label.config(text="3 coeurs verts")

    def update_ui_started(self):
        self.start_btn.config(
            text="STOP",
            command=self.stop_process,
            bg=THEME["alert_color"]
        )
        self.pause_btn.config(state=tk.NORMAL, bg=THEME["accent_secondary"], fg=THEME["bg_primary"])
        self.status_indicator.config(text="EN COURS", fg=THEME["success_color"])
        self.mode_comet_btn.config(state=tk.DISABLED)
        self.mode_orch_btn.config(state=tk.DISABLED)
        self.mode_solo_btn.config(state=tk.DISABLED)
        self.iconify()

    def update_ui_stopped(self):
        self.start_btn.config(
            text="START",
            command=self.start_process,
            bg=THEME["accent_secondary"]
        )
        self.pause_btn.config(
            state=tk.DISABLED,
            text="PAUSE",
            bg=THEME["bg_tertiary"],
            fg=THEME["text_secondary"]
        )
        self.status_indicator.config(text="ARRETE", fg=THEME["text_muted"])
        self.step_label.config(text="-")
        self.mode_comet_btn.config(state=tk.NORMAL)
        self.mode_orch_btn.config(state=tk.NORMAL)
        self.mode_solo_btn.config(state=tk.NORMAL)

    def start_timer_update(self):
        self.update_info()

    def stop_timer_update(self):
        if self.update_timer_id:
            self.after_cancel(self.update_timer_id)
            self.update_timer_id = None

    def update_info(self):
        if self.controller.running:
            elapsed = self.controller.get_elapsed_time()
            cycles = self.controller.cycle_count
            self.info_label.config(text=f"C:{cycles} | {elapsed}")
            self.update_timer_id = self.after(1000, self.update_info)


def run_gui():
    controller = ProcessController()
    app = AutoCopierGUI(controller)
    app.mainloop()


if __name__ == "__main__":
    run_gui()
