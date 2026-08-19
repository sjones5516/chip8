from threading import Lock

import numpy as np


class Screen:
    """Threadsafe monochrome display for VM"""

    def __init__(self, width: int, height: int) -> None:
        self._screen = np.zeros((height, width), dtype=bool)
        self._lock = Lock()

    @property
    def screen(self):
        with self._lock:
            return self._screen

    @screen.setter
    def screen(self, value):
        with self._lock:
            self._screen = value
