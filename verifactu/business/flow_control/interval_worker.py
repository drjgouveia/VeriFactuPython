"""IntervalWorker - Worker for periodic tasks."""

import threading
import time
from typing import Optional, Callable


class IntervalWorker:
    """Worker that executes a function at regular intervals."""
    
    def __init__(self, interval: float, function: Callable, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self._timer = None
        self._stop_event = threading.Event()
    
    def start(self):
        self._timer = threading.Timer(self.interval, self._run)
        self._timer.start()
    
    def _run(self):
        if not self._stop_event.is_set():
            self.function(*self.args, **self.kwargs)
            self.start()
    
    def stop(self):
        self._stop_event.set()
        if self._timer:
            self._timer.cancel()