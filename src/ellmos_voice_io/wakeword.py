"""Optional local wake-word listener with an explicit keyboard fallback."""

from __future__ import annotations

import threading
from collections.abc import Callable
from importlib.util import find_spec


class WakeWordListener:
    """Run openWakeWord locally; callers own microphone permission and lifecycle."""

    def __init__(self, threshold: float = 0.5):
        if not 0 < threshold <= 1:
            raise ValueError("threshold must be in (0, 1]")
        self.threshold = threshold

    def available(self) -> tuple[bool, str]:
        if all(find_spec(package) is not None for package in ("numpy", "pyaudio", "openwakeword")):
            return True, "openwakeword"
        return False, "Install the wakeword extra to access microphone-based wake words."

    def listen(self, on_wake: Callable[[], None], stop_event: threading.Event | None = None) -> None:
        available, detail = self.available()
        if not available:
            raise RuntimeError(detail)
        import numpy as np
        import pyaudio
        from openwakeword.model import Model

        event = stop_event or threading.Event()
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16_000, input=True, frames_per_buffer=1_280)
        try:
            model = Model()
            while not event.is_set():
                samples = np.frombuffer(stream.read(1_280, exception_on_overflow=False), dtype=np.int16)
                model.predict(samples)
                if any(values[-1] >= self.threshold for values in model.prediction_buffer.values()):
                    on_wake()
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
