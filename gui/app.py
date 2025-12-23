import tkinter as tk
from tkinter import ttk
from datetime import datetime
from .theme import THEME
from .process_controller import ProcessController
from .historique import open_historique


class AutoCopierGUI(tk.Tk):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller or ProcessController()
        self.setup_window()
        self.create_widgets()
        self.bind_events()
        self.update_timer_id = None

    def setup_window(self):
        self.title("Auto Copier Coller")
        self.configure(bg=THEME["bg_primary"])
        self.position_center()
        self.minsize(200, 150)
        self.attributes("-topmost", False)

    def position_center(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = screen_width // 8
        window_height = screen_height // 8
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def create_widgets(self):
        self.create_header()
        self.create_status_section()
        self.create_control_section()
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

    def create_historique_button(self):
        self.hist_btn = tk.Button(
            self,
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
        self.hist_btn.pack(fill=tk.X, padx=5, pady=(0, 3))

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
        self.destroy()

    def start_process(self):
        from actions import envoie_message_comet, attendre_reponse_comet
        from actions import envoie_message_claude, attendre_reponse_claude
        from config import DELAY, DELAY_BEFORE_MAIN, DELAY_MULTIPLIER_ATTENTE_CLAUDE
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
                (attendre_reponse_claude.execute, "Attente reponse Claude", DELAY * DELAY_MULTIPLIER_ATTENTE_CLAUDE, "CLAUDE", "COMET"),
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
            self.step_label.config(text=f"{step_num}/4: {data[:15]}")
        elif event_type == "cycle":
            pass
        elif event_type == "error":
            self.status_indicator.config(
                text="ERREUR",
                fg=THEME["alert_color"]
            )

    def update_ui_started(self):
        self.start_btn.config(
            text="STOP",
            command=self.stop_process,
            bg=THEME["alert_color"]
        )
        self.pause_btn.config(state=tk.NORMAL, bg=THEME["accent_secondary"], fg=THEME["bg_primary"])
        self.status_indicator.config(text="EN COURS", fg=THEME["success_color"])

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
