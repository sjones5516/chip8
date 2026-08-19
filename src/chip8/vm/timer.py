from threading import Event, Lock, Thread
import time


class Timer:
    """Counts down until it reaches 0."""

    def __init__(self, starting_value=0, hz=60):
        self._value = starting_value
        self._hz = hz
        self._cycle_time = 1 / self._hz
        self._value_lock = Lock()
        self.stop_signal = Event()
        self._thread = None

    @property
    def value(self) -> int:
        with self._value_lock:
            return self._value

    @value.setter
    def value(self, value: int):
        with self._value_lock:
            self._value = value

    def _decrement_once(self):
        with self._value_lock:
            if self._value > 0:
                self._value -= 1

    def worker(self):
        while not self.stop_signal.is_set():
            time.sleep(self._cycle_time)
            self._decrement_once()

    def start(self):
        if self._thread is not None and self._thread.is_alive():
            return

        self.stop_signal.clear()
        self._thread = Thread(target=self.worker, daemon=True)
        self._thread.start()

    def stop(self):
        self.stop_signal.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=max(0.1, (2 / self._hz) + 0.1))
        self._thread = None
