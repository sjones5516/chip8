import time

from src.chip8.vm.timer import Timer


def test_timer_counts_down_to_zero_and_stops():
    timer = Timer(starting_value=2, hz=1000)

    timer.start()
    time.sleep(0.015)
    timer.stop()

    assert timer.value == 0


def test_timer_can_restart_multiple_times():
    timer = Timer(starting_value=2, hz=1000)

    for _ in range(3):
        timer.start()
        time.sleep(0.015)
        timer.stop()
        timer.value = 2

    assert timer.value == 2
