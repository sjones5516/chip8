from threading import Event

from .virtualmachine_abc import VirtualMachineABC
from .timer import Timer
from .screen import Screen


class VirtualMachine(VirtualMachineABC):
    MEMORY_LOCATIONS = 4096
    NUM_DATA_REGISTER = 16
    NUM_KEYS = 16
    SCREEN_WIDTH = 64
    SCREEN_HEIGHT = 32

    def __init__(self):
        super().__init__()

        self._memory = bytearray(self.MEMORY_LOCATIONS)
        self._data_register = [0] * self.NUM_DATA_REGISTER
        self._address_register = 0
        self._stack: list[int] = []
        self._delay_timer = Timer()
        self._sound_timer = Timer()
        self._keystate = [False] * self.NUM_KEYS
        self._screen = Screen(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self._sound_event = Event()
