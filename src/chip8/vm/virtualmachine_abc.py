from abc import ABC, abstractmethod

from .keyboard import Keystate


class VirtualMachineABC(ABC):
    @abstractmethod
    def load_rom(self, rom: bytes):
        """Loads a ROM into VM memory
        Raises:
            MemoryError: If the ROM cannot fit into system memory`
        """
        pass

    @abstractmethod
    def set_keystate(self, keystate: Keystate):
        """Sets the keystate of the VM"""
        pass
