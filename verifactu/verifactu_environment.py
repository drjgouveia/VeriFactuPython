"""VeriFactuEnvironment - Environment information."""

import platform
import os


class VeriFactuEnvironment:
    """Environment information for VeriFactu."""
    
    @staticmethod
    def get_path_and_lock() -> str:
        """Get the path and lock for the application."""
        return os.environ.get('VERIFACTU_PATH', '')
    
    @staticmethod
    def get_platform() -> str:
        """Get the current platform."""
        return platform.system()