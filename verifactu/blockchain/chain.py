"""Chain - Base class for blockchain chains."""

import csv
import os
from threading import Lock
from typing import Optional, Dict, Type

from verifactu.config.settings import Settings


class Chain:
    """Base class for blockchain chains."""

    _instances: Dict[str, 'Chain'] = {}
    _locker = Lock()
    _csv_separator = ","

    def __init__(self, seller_id: str):
        self.seller_id = seller_id
        self.current_id: int = 0
        self.current_time_stamp = None
        self.current: Optional[dict] = None
        self.previous: Optional[dict] = None
        self.chain_path: str = ""

    @property
    def locker(self) -> Lock:
        return Chain._locker

    @classmethod
    def get_instance(cls, seller_id: str, chain_class: Type['Chain']) -> 'Chain':
        """Get or create a chain instance for a seller."""
        key = f"{chain_class.__name__}:{seller_id}"
        with Chain._locker:
            if key not in Chain._instances:
                instance = chain_class(seller_id)
                instance.chain_path = instance._get_chain_dir(seller_id)
                instance.read_var()
                Chain._instances[key] = instance
            return Chain._instances[key]

    @classmethod
    def exit_all(cls):
        """Exit all chains."""
        with Chain._locker:
            cls._instances.clear()

    def _get_chain_dir(self, seller_id: str) -> str:
        """Get the directory for the chain."""
        return os.path.join(Settings.current.blockchain_path, seller_id)

    def read_var(self):
        """Read the chain variable file."""
        var_file = os.path.join(self.chain_path, "var.txt")
        if not os.path.exists(var_file):
            return

        with open(var_file, 'r') as f:
            reader = csv.reader(f, delimiter=self._csv_separator)
            for row in reader:
                if len(row) >= 6:
                    self.current_id = int(row[0])
                    self.current_time_stamp = row[1]
                    self.current = {
                        'huella': row[2],
                        'id_factura': {
                            'fecha_expedicion': row[3],
                            'id_emisor': row[4],
                            'num_serie': row[5],
                        }
                    }

    def write(self, lines: list = None):
        """Write the chain data to disk."""
        os.makedirs(self.chain_path, exist_ok=True)
        data_file = os.path.join(self.chain_path, "data.csv")
        var_file = os.path.join(self.chain_path, "var.txt")

        if lines:
            with open(data_file, 'a', newline='') as f:
                writer = csv.writer(f, delimiter=self._csv_separator)
                for line in lines:
                    writer.writerow(line.split(self._csv_separator))
        else:
            with open(data_file, 'a', newline='') as f:
                writer = csv.writer(f, delimiter=self._csv_separator)
                writer.writerow(self._get_var_file_line().split(self._csv_separator))

        with open(var_file, 'w') as f:
            f.write(self._get_var_file_line())

    def _get_var_file_line(self) -> str:
        """Get the variable file line."""
        current = self.current or {}
        id_factura = current.get('id_factura', {})
        return (f"{self.current_id}{self._csv_separator}"
                f"{self.current_time_stamp}{self._csv_separator}"
                f"{current.get('huella', '')}{self._csv_separator}"
                f"{id_factura.get('fecha_expedicion', '')}{self._csv_separator}"
                f"{id_factura.get('id_emisor', '')}{self._csv_separator}"
                f"{id_factura.get('num_serie', '')}")

    def save_current(self):
        """Save the current record."""
        pass

    def restore_previous(self):
        """Restore the previous record."""
        pass

    def restore_previous_data(self, data_file: str, previous_file: str):
        """Restore previous data from files."""
        pass