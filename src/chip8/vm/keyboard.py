from threading import Lock
from typing import Literal

import numpy as np

type KEYBOARD_SIZE_TYPE = Literal[16]
KEYBOARD_SIZE = 16
type Keystate = np.ndarray[tuple[KEYBOARD_SIZE_TYPE, Literal[1]], np.dtype[np.bool_]]


class Keyboard:
    """Threadsafe keyboard for VM"""

    def __init__(self) -> None:
        self._keystate: Keystate = np.zeros((KEYBOARD_SIZE, 1), dtype=bool)
        self._lock = Lock()

    @property
    def keystate(self) -> Keystate:
        with self._lock:
            return self._keystate

    @keystate.setter
    def keystate(self, value: Keystate):
        with self._lock:
            self._keystate = value
