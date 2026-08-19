from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional


class Opcode(Enum):
    OP_00E0 = 0x00E0
    """Clears the screen"""
    OP_00EE = 0x00EE
    """Returns from a subroutine"""
    OP_1NNN = 0x1000
    """Jumps to address NNN"""
    OP_2NNN = 0x2000
    """Calls the subroutine at address NNN"""
    OP_3XNN = 0x3000
    """Skips the next instruction if VX eq NN"""
    OP_4XNN = 0x4000
    """Skips the next instruction if VX neq NN"""
    OP_5XY0 = 0x5000
    """Skips the next instruction if VX eq VY"""
    OP_6XNN = 0x6000
    """Sets VX to NN"""
    OP_7XNN = 0x7000
    """Adds NN to VX"""
    OP_8XY0 = 0x8000
    """Sets VX to the value of VY"""
    OP_8XY1 = 0x8001
    """Sets VX to VX OR VY"""
    OP_8XY2 = 0x8002
    """Sets VX to VX AND VY"""
    OP_8XY3 = 0x8003
    """Sets VX to VX XOR VY"""
    OP_8XY4 = 0x8004
    """Adds VY to VX and sets VF to the carry flag"""
    OP_8XY5 = 0x8005
    """Subtracts VY from VX and sets VF to the inverse borrow flag"""
    OP_8XY6 = 0x8006
    """Shifts VX right by one and stores its least significant bit in VF"""
    OP_8XY7 = 0x8007
    """Sets VX to VY minus VX and sets VF to the inverse borrow flag"""
    OP_8XYE = 0x800E
    """Shifts VX left by one and stores its most significant bit in VF"""
    OP_9XY0 = 0x9000
    """Skips the next instruction if VX is not equal to VY"""
    OP_ANNN = 0xA000
    """Sets I to address NNN"""
    OP_BNNN = 0xB000
    """Jumps to address NNN plus V0"""
    OP_CXNN = 0xC000
    """Sets VX to a random byte AND NN"""
    OP_DXYN = 0xD000
    """Draws an N-byte sprite at coordinates VX, VY and sets VF on collision"""
    OP_EX9E = 0xE09E
    """Skips the next instruction if the key VX is pressed"""
    OP_EXA1 = 0xE0A1
    """Skips the next instruction if the key VX is not pressed"""
    OP_FX07 = 0xF007
    """Sets VX to the current delay timer value"""
    OP_FX0A = 0xF00A
    """Waits for a key press and stores its value in VX"""
    OP_FX15 = 0xF015
    """Sets the delay timer to VX"""
    OP_FX18 = 0xF018
    """Sets the sound timer to VX"""
    OP_FX1E = 0xF01E
    """Adds VX to I"""
    OP_FX29 = 0xF029
    """Sets I to the location of the sprite for digit VX"""
    OP_FX33 = 0xF033
    """Stores the binary-coded decimal representation of VX at I, I plus 1, and I plus 2"""
    OP_FX55 = 0xF055
    """Stores registers V0 through VX in memory starting at I"""
    OP_FX65 = 0xF065
    """Loads registers V0 through VX from memory starting at I"""


@dataclass
class Instruction:
    """Represents an 2B instruction, including opcode and optional fields"""

    opcode: Opcode
    NNN: int
    """Always 12 least significant bits. Address"""
    NN: int
    """Always 8 least significant bits. 8-bit constant"""
    N: int
    """Always 4 least significant bits. 4-bit constant"""
    X: int
    """Always the 2nd least significant nibble. First register identifier"""
    Y: int
    """Always the 3rd least significant nibble. Second register identifier"""

    @staticmethod
    def _extract_opcode(data: int) -> Opcode:
        for opcode in Opcode:
            opcode_name = opcode.name[3:]
            if opcode_name in {"00E0", "00EE"}:
                mask = 0xFFFF
            elif opcode_name[0] in {"1", "2", "3", "4", "6", "7", "A", "B", "C", "D"}:
                mask = 0xF000
            elif opcode_name[0] in {"5", "8", "9"}:
                mask = 0xF00F
            else:
                mask = 0xF0FF

            if data & mask == opcode.value:
                return opcode

        raise ValueError(f"Unknown opcode: 0x{data:04X}")

    def __init__(self, value: bytes):
        data_size = len(value)
        if data_size != 2:
            raise ValueError(
                f"Cannot parse {value} as opcode. Expected 2B, got {data_size}"
            )
        data = int.from_bytes(value, "big")
        self.opcode = self._extract_opcode(data)
        self.NNN = data & 0xFFF
        self.NN = data & 0xFF
        self.N = data & 0xF
        self.X = (data >> 8) & 0xF
        self.Y = (data >> 4) & 0xF
