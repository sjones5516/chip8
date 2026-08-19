import pytest

from src.chip8.vm.virtualmachine import VirtualMachine


def test_vm_initializes_expected_state():
    vm = VirtualMachine()

    assert len(vm._memory) == VirtualMachine.MEMORY_LOCATIONS
    assert vm._address_register == 0
    assert vm._data_register == [0] * VirtualMachine.NUM_DATA_REGISTER
    assert vm._stack == []
    assert vm._delay_timer.value == 0
    assert vm._sound_timer.value == 0
    assert len(vm._keystate) == VirtualMachine.NUM_KEYS
    assert vm._screen.screen.shape == (VirtualMachine.SCREEN_HEIGHT, VirtualMachine.SCREEN_WIDTH)


def test_load_rom_writes_bytes_to_memory_at_program_start():
    vm = VirtualMachine()
    rom = b"\x01\x02\x03\x04"

    vm.load_rom(rom)

    assert vm._memory[VirtualMachine.PROGRAM_START:VirtualMachine.PROGRAM_START + len(rom)] == rom


def test_load_rom_raises_when_rom_does_not_fit():
    vm = VirtualMachine()
    rom = b"\x00" * (VirtualMachine.AVAILABLE_ROM_LOCATIONS + 1)

    with pytest.raises(MemoryError):
        vm.load_rom(rom)
