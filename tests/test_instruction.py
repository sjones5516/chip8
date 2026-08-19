import pytest

from src.chip8.vm.instruction import Instruction, Opcode


@pytest.mark.parametrize("value", [b"", b"\x12", b"\x12\x34\x56"])
def test_instruction_rejects_values_that_are_not_two_bytes(value):
    with pytest.raises(ValueError, match="Expected 2B"):
        Instruction(value)


def test_instruction_extracts_optional_fields():
    instruction = Instruction(b"\x6a\xbc")

    assert instruction.NNN == 0xABC
    assert instruction.NN == 0xBC
    assert instruction.N == 0xC
    assert instruction.X == 0xA
    assert instruction.Y == 0xB


def test_instruction_extracts_opcode_type():
    instruction = Instruction(b"\x8a\xb4")

    assert instruction.opcode is Opcode.OP_8XY4


def _opcode_sample(opcode):
    name = opcode.name[3:]
    if name in {"00E0", "00EE"}:
        return opcode.value
    if name[0] in {"1", "2", "3", "4", "6", "7", "A", "B", "C", "D"}:
        return opcode.value | 0x0ABC
    if name[0] in {"5", "8", "9"}:
        return opcode.value | 0x0AB0
    return opcode.value | 0x0F00


@pytest.mark.parametrize("opcode", list(Opcode))
def test_instruction_extracts_every_opcode_type(opcode):
    instruction = Instruction(_opcode_sample(opcode).to_bytes(2, "big"))

    assert instruction.opcode is opcode
