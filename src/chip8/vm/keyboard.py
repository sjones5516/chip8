
from threading import Lock

import numpy as np


class Keyboard:
    """Threadsafe keyboard for VM"""

    def __init__(self, size: int) -> None:
        self._keyboard= np.zeros((size, 1), dtype=bool)
        self._lock = Lock()

    @property
    def keyboard(self):
        with self._lock:
            return self._keyboard

    @keyboard.setter
    def keyboard(self, value):
        with self._lock:
            self._keyboard = value
