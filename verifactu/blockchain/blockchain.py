"""Blockchain - Cadena de registros de facturación."""

import csv
import os
from datetime import datetime
from threading import Lock
from typing import List, Optional

from verifactu.config.settings import Settings
from verifactu.xml.factu.registro import Registro
from verifactu.xml.factu.id_factura import IDFactura
from verifactu.xml.factu.encadenamiento import Encadenamiento
from verifactu.xml.factu.registro_anterior import RegistroAnterior
from verifactu.xml.xml_parser import get_xml_date_time_iso8601, to_date

_CsvSeparator = ";"


class Blockchain:
    """Representa una cadena de registros de facturación."""

    _instances = {}
    _class_locker = Lock()
    _initialized = False

    def __init__(self, seller_id: str):
        self.seller_id = seller_id
        self.current_id = 0
        self.current_time_stamp: Optional[datetime] = None
        self.current: Optional[Registro] = None
        self.previous: Optional[Registro] = None
        self.previous_time_stamp: Optional[datetime] = None
        self.chain_path = os.path.join(Settings.current.blockchain_path, seller_id)
        self._locker = Lock()

    @property
    def locker(self) -> Lock:
        return self._locker

    # ---------------- Gestión de instancias ----------------

    @classmethod
    def get(cls, seller_id: str) -> "Blockchain":
        """Devuelve la instancia correspondiente a la cadena de bloques
        de un emisor de facturas."""
        with cls._class_locker:
            if seller_id not in cls._instances:
                instance = cls(seller_id)
                instance.read_var()
                cls._instances[seller_id] = instance
            return cls._instances[seller_id]

    @classmethod
    def load_blockchains_from_disk(cls):
        """Carga todas las cadenas de bloques."""
        blockchain_path = Settings.current.blockchain_path
        if not blockchain_path or not os.path.exists(blockchain_path):
            raise ValueError(
                f"Revise el archivo de configuración {Settings.file_name},"
                " el valor de BlockchainPath debe ser el de un directorio válido.")

        for dir_name in os.listdir(blockchain_path):
            dir_path = os.path.join(blockchain_path, dir_name)
            if os.path.isdir(dir_path):
                blockchain = cls(dir_name)
                blockchain.read_var()
                cls._instances[dir_name] = blockchain

    # ---------------- Encadenamiento ----------------

    def get_encadenamiento(self) -> Encadenamiento:
        """Devuelve un encadenamiento con el último elemento de la cadena."""
        if self.current is None or not self.current.huella:
            encadenamiento = Encadenamiento()
            encadenamiento.primer_registro = "S"
            return encadenamiento

        encadenamiento = Encadenamiento()
        encadenamiento.registro_anterior = RegistroAnterior()
        encadenamiento.registro_anterior.huella = self.current.huella
        encadenamiento.registro_anterior.fecha_expedicion_factura = \
            self.current.id_factura.fecha_expedicion
        encadenamiento.registro_anterior.id_emisor_factura = \
            self.current.id_factura.id_emisor
        encadenamiento.registro_anterior.num_serie_factura = \
            self.current.id_factura.num_serie
        return encadenamiento

    def insert(self, registro: Registro) -> str:
        """Inserta un eslabón en la cadena."""
        # Guardo previo
        self.save_current()

        # Actualizo los datos de encadenamiento con el registro anterior
        registro.encadenamiento = self.get_encadenamiento()

        # Establezco el momento de generación.
        self.current_time_stamp = datetime.now()
        registro.fecha_hora_huso_gen_registro = \
            get_xml_date_time_iso8601(self.current_time_stamp)

        # Calculo la huella con los datos del encadenamiento ya actualizados
        registro.huella = registro.get_hash_output()

        # Establezco el elemento insertado como el último de la cadena
        self.current = registro
        self.current_id += 1

        # Asigno el identificador del eslabón
        registro.blockchain_link_id = self.current_id
        registro.set_extern_key()

        return self.get_control_file_line()

    # ---------------- Archivos de control ----------------

    def get_var_file_line(self) -> str:
        """Devuelve un texto con los datos necesarios para restaurar."""
        return (_CsvSeparator.join([
            str(self.current_id),
            str(self.current_time_stamp),
            str(self.current.huella),
            str(self.current.id_factura.fecha_expedicion),
            str(self.current.id_factura.id_emisor),
            str(self.current.id_factura.num_serie),
        ]))

    def get_control_file_line(self) -> str:
        """Devuelve un texto para el archivo csv de control."""
        return (_CsvSeparator.join([
            str(self.current_id),
            str(self.current_time_stamp),
            str(self.current.huella),
            str(self.current.id_factura.fecha_expedicion),
            str(self.current.id_factura.id_emisor),
            str(self.current.id_factura.num_serie),
            f"[{self.current.get_hash_text_input()}]",
        ]))

    def read_var(self):
        """Restaura el estado de la cadena desde el archivo de variables."""
        var_file = os.path.join(self.chain_path, "var.dat")
        if not os.path.exists(var_file):
            return
        with open(var_file, "r", encoding="utf-8") as f:
            line = f.readline().rstrip("\n")
        if not line:
            return
        values = line.split(_CsvSeparator)
        self.restore_current(values)

    def restore_current(self, values: List[str]):
        """Restaura el último registro de la cadena."""
        self.current_id = int(values[0])
        try:
            self.current_time_stamp = datetime.fromisoformat(values[1])
        except ValueError:
            self.current_time_stamp = None
        self.current = Registro()
        self.current.huella = values[2]
        self.current.id_factura = IDFactura()
        self.current.id_factura.fecha_expedicion = values[3]
        self.current.id_factura.id_emisor = values[4]
        self.current.id_factura.num_serie = values[5]

    def save_current(self):
        """Guarda el estado previo para permitir una reversión."""
        self.previous = self.current
        self.previous_time_stamp = self.current_time_stamp
        self.previous_id = self.current_id

    def restore_previous(self):
        """Restaura el estado previo."""
        if self.previous is None and self.current_id > 1:
            raise ValueError("No se puede eliminar el último elemento ya que"
                             " no existe información del elemento previo.")
        self.current = self.previous
        self.current_time_stamp = self.previous_time_stamp
        self.current_id = self.previous_id

    def write_var(self):
        """Escribe el archivo de variables."""
        os.makedirs(self.chain_path, exist_ok=True)
        var_file = os.path.join(self.chain_path, "var.dat")
        with open(var_file, "w", encoding="utf-8") as f:
            f.write(self.get_var_file_line())

    def write(self, csv_lines: Optional[List[str]] = None):
        """Escribe los datos de la cadena en el archivo csv de control."""
        os.makedirs(self.chain_path, exist_ok=True)

        if self.current_time_stamp is None:
            return

        # El archivo csv se organiza por mes de generación
        csv_file = os.path.join(
            self.chain_path, f"{self.current_time_stamp:%Y%m}.csv")

        lines = csv_lines if csv_lines is not None else [self.get_control_file_line()]
        with open(csv_file, "a", encoding="utf-8", newline="") as f:
            for line in lines:
                f.write(line + "\n")

        self.write_var()

    def get_delete_disabled(self) -> bool:
        """True si está desactivada la eliminación en la cadena."""
        return Settings.current.disable_blockchain_delete

    def restore_previous_data(self, data_file_name: str, previous_file_name: str):
        """Restaura los archivos de datos previos."""
        data_file = os.path.join(self.chain_path, data_file_name)
        previous_file = os.path.join(self.chain_path, previous_file_name)
        if os.path.exists(previous_file):
            if os.path.exists(data_file):
                os.replace(previous_file, data_file)

    # ---------------- Operaciones públicas ----------------

    def add(self, registro: Registro):
        """Añade un elemento a la cadena de bloques."""
        add_exception = None
        with self.locker:
            try:
                self.insert(registro)
                self.write()
            except Exception as ex:
                add_exception = ex

        if add_exception is not None:
            raise RuntimeError(
                f"Error añadiendo eslabón de la cadena: {add_exception}.")

    def add_if_not_exists(self, registro: Registro) -> bool:
        """Añade un registro a la cadena únicamente si no se encuentra ya
        incluido en el archivo de control correspondiente a su período."""
        if registro is None:
            raise ValueError("registro no puede ser nulo.")
        if not registro.fecha_hora_huso_gen_registro:
            raise ValueError("El registro no contiene FechaHoraHusoGenRegistro.")
        if not registro.huella:
            raise ValueError("El registro no contiene Huella.")

        with self.locker:
            created = to_date(registro.fecha_hora_huso_gen_registro[:10])
            csv_file = os.path.join(self.chain_path, f"{created:%Y%m}.csv")

            if os.path.exists(csv_file):
                with open(csv_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.rstrip("\n")
                        if not line.strip():
                            continue
                        values = line.split(_CsvSeparator)
                        if len(values) < 3:
                            continue
                        if int(values[0]) == registro.blockchain_link_id \
                                and values[2] == registro.huella:
                            return False

            self.insert(registro)
            self.write()
            return True

    def add_list(self, registros: List[Registro]):
        """Añade una lista de elementos a la cadena de bloques."""
        add_exception = None
        with self.locker:
            try:
                csv_lines = []
                for registro in registros:
                    csv_lines.append(self.insert(registro))
                self.write(csv_lines)
            except Exception as ex:
                add_exception = ex

        if add_exception is not None:
            raise RuntimeError(
                f"Error añadiendo eslabones de la cadena: {add_exception}.")

    def delete(self, registro: Registro):
        """Elimina el último elemento añadido a la cadena."""
        if self.get_delete_disabled():
            raise ValueError(
                f"Se ha intentado borrar el registro {registro.huella} y en la"
                " configuración está establecido DisableClearPost = true.")

        restore_exception = None
        with self.locker:
            try:
                if registro.huella != (self.current.huella if self.current else None):
                    raise ValueError(
                        f"Se ha intentado borrar el registro {registro.huella} que"
                        f" no coincide con el último {self.current.huella}")

                self.restore_previous()
                self.write_var()
            except Exception as ex:
                restore_exception = ex

        if restore_exception is not None:
            raise RuntimeError(
                f"Error al restaurar datos borrando último eslabón de la cadena:"
                f" {restore_exception}.")

    def __str__(self) -> str:
        current_id_factura = self.current.id_factura if self.current else None
        return (f"{self.seller_id} ({self.current_id},"
                f" {current_id_factura.num_serie if current_id_factura else ''},"
                f" {current_id_factura.fecha_expedicion if current_id_factura else ''},"
                f" {self.current.huella if self.current else ''})")
