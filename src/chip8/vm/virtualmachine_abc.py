from abc import ABC, abstractmethod


class VirtualMachineABC(ABC):
    @abstractmethod
    def load_rom(self, rom: bytes):
        """Loads a ROM into VM memory
        Raises:
            MemoryError: If the ROM cannot fit into system memory`
        """
        pass
