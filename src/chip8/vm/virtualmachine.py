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
    PROGRAM_START = 0x200
    AVAILABLE_ROM_LOCATIONS = MEMORY_LOCATIONS - PROGRAM_START

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

    def _can_fit_into_memory(self, data_size: int) -> bool:
        return data_size <= self.AVAILABLE_ROM_LOCATIONS

    def load_rom(self, rom: bytes):
        rom_array = bytearray(rom)
        rom_size = len(rom_array)
        if not self._can_fit_into_memory(rom_size):
            raise MemoryError(
                f"Cannot fit ROM into VM memory. Got {rom_size} bytes, max is {self.AVAILABLE_ROM_LOCATIONS}"
            )

        self._memory[self.PROGRAM_START : self.PROGRAM_START + rom_size] = rom_array
