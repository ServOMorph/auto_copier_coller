import threading
import time
from outils.recherche_image import trouver_image
from outils.logger import log

STOP_IMAGE_PATH = r"C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\assets\images\3 coeurs verts.png"
WATCH_INTERVAL = 1.0


class StopWatcher:
    def __init__(self, on_stop_callback):
        self.on_stop_callback = on_stop_callback
        self.watching = False
        self.thread = None

    def start(self):
        if self.watching:
            return
        self.watching = True
        self.thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.thread.start()
        log("StopWatcher demarre - surveillance image 3 coeurs verts")

    def stop(self):
        self.watching = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
        log("StopWatcher arrete")

    def _watch_loop(self):
        while self.watching:
            location = trouver_image(STOP_IMAGE_PATH, confidence=0.8)
            if location:
                log("IMAGE 3 COEURS VERTS DETECTEE - ARRET DU PROCESSUS")
                self.watching = False
                if self.on_stop_callback:
                    self.on_stop_callback()
                break
            time.sleep(WATCH_INTERVAL)
