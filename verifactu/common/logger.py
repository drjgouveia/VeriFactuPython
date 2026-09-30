"""Logger for VeriFactu."""

import logging


class Logger:
    """Simple logger wrapper."""

    def __init__(self):
        self._logger = logging.getLogger("verifactu")

    def log(self, msg: str):
        """Log a message."""
        self._logger.info(msg)