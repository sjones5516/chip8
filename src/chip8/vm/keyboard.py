from threading import Lock
from typing import Literal

import numpy as np

type KEYBOARD_SIZE_TYPE = Literal[16]
KEYBOARD_SIZE = 16
type Keystate = np.ndarray[
    tuple[KEYBOARD_SIZE_TYPE, Literal[1]], np.dtype[np.bool_]
]


class Keyboard:
    """Threadsafe keyboard for VM"""

    def __init__(self) -> None:
        self._keyboard: Keystate = np.zeros((KEYBOARD_SIZE, 1), dtype=bool)
        self._lock = Lock()

    @property
    def keyboard(self) -> Keystate:
        with self._lock:
            return self._keyboard

    @keyboard.setter
    def keyboard(self, value: Keystate):
        with self._lock:
            self._keyboard = value
