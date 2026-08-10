"""Optional local wake-word listener with an explicit keyboard fallback."""

from __future__ import annotations

import threading
from collections.abc import Callable
from importlib.util import find_spec


class WakeWordListener:
    """Run openWakeWord locally; callers own microphone permission and lifecycle.

    The listener deliberately keeps a small, explicit lifecycle contract:

    * a callback is invoked once for every audio chunk whose latest prediction
      reaches ``threshold``; repeated qualifying chunks therefore produce
      repeated callbacks and any debouncing belongs to the caller;
    * ``stop_event`` is checked before opening the microphone and before every
      read, so a pre-cancelled listener does not touch audio hardware;
    * callback, model, stream, and read exceptions propagate after the stream
      and ``PyAudio`` instance have been cleaned up.
    """

    def __init__(self, threshold: float = 0.5):
        if not 0 < threshold <= 1:
            raise ValueError("threshold must be in (0, 1]")
        self.threshold = threshold

    def available(self) -> tuple[bool, str]:
        if all(find_spec(package) is not None for package in ("numpy", "pyaudio", "openwakeword")):
            return True, "openwakeword"
        return False, "Install the wakeword extra to access microphone-based wake words."

    def listen(self, on_wake: Callable[[], None], stop_event: threading.Event | None = None) -> None:
        event = stop_event or threading.Event()
        if event.is_set():
            return

        available, detail = self.available()
        if not available:
            raise RuntimeError(detail)
        import numpy as np
        import pyaudio
        from openwakeword.model import Model

        if event.is_set():
            return

        audio = pyaudio.PyAudio()
        stream = None
        try:
            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16_000, input=True, frames_per_buffer=1_280)
            model = Model()
            while not event.is_set():
                samples = np.frombuffer(stream.read(1_280, exception_on_overflow=False), dtype=np.int16)
                model.predict(samples)
                if any(values[-1] >= self.threshold for values in model.prediction_buffer.values()):
                    on_wake()
        finally:
            try:
                if stream is not None:
                    try:
                        stream.stop_stream()
                    finally:
                        stream.close()
            finally:
                audio.terminate()
