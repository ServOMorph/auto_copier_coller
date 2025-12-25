import time
import threading
import config
from config import DELAY_PAUSE_POLLING
from outils.stop_watcher import StopWatcher


class ProcessController:
    def __init__(self):
        self.paused = False
        self.running = False
        self.current_step = 0
        self.cycle_count = 0
        self.start_time = None
        self.thread = None
        self.stop_watcher = None
        self.gui_callback = None
        self.step_names = [
            "Envoi message Comet",
            "Attente reponse Comet",
            "Envoi message Claude",
            "Attente reponse Claude"
        ]

    def start(self, target_func, gui_callback):
        if self.running:
            return
        config.stop_requested = False
        self.running = True
        self.paused = False
        self.current_step = 0
        self.cycle_count = 0
        self.start_time = time.time()
        self.gui_callback = gui_callback
        self.stop_watcher = StopWatcher(self._on_stop_image_detected)
        self.stop_watcher.start()
        self.thread = threading.Thread(
            target=target_func,
            args=(self, gui_callback),
            daemon=True
        )
        self.thread.start()

    def _on_stop_image_detected(self):
        self.stop()
        if self.gui_callback:
            self.gui_callback("stop_image", "3 coeurs verts detectes", -1)

    def stop(self):
        config.stop_requested = True
        self.running = False
        self.paused = False
        if self.stop_watcher:
            self.stop_watcher.stop()
            self.stop_watcher = None
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def toggle_pause(self):
        if self.paused:
            self.resume()
        else:
            self.pause()
        return self.paused

    def wait_if_paused(self):
        while self.paused and self.running:
            time.sleep(DELAY_PAUSE_POLLING)
        return self.running

    def get_elapsed_time(self):
        if self.start_time is None:
            return "00:00:00"
        elapsed = int(time.time() - self.start_time)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def get_current_step_name(self):
        if 0 <= self.current_step < len(self.step_names):
            return self.step_names[self.current_step]
        return "Initialisation"
