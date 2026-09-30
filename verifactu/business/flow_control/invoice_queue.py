"""InvoiceQueue - Cola de procesamiento con control de flujo.

La AEAT establece en sus especificaciones que la aplicación debe
disponer de un control de flujo que respete los tiempos de espera
entre envíos. La cola realiza envíos cuando alcanza 1.000 registros
pendientes o cuando transcurre el tiempo de espera indicado en la
respuesta de la AEAT.
"""

import os
import threading
from datetime import datetime, timedelta
from typing import List, Optional

from verifactu.config.settings import Settings
from verifactu.common.utils import Utils


class InvoiceQueue:
    """Cola de envío de registros de facturación con control de flujo."""

    _instance: Optional["InvoiceQueue"] = None
    _lock = threading.Lock()

    def __init__(self):
        self._queue: List = []
        self._queue_lock = threading.Lock()
        self._worker: Optional[threading.Thread] = None
        self._exit_event = threading.Event()
        self.current_wait_seconds = 0
        self.last_process_moment: Optional[datetime] = None
        self.max_batch = 1000

    @classmethod
    def active_invoice_queue(cls) -> "InvoiceQueue":
        """Cola activa (equivalente a InvoiceQueue.ActiveInvoiceQueue)."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
                cls._instance.start()
            return cls._instance

    @classmethod
    def exit(cls):
        """Finaliza la cola asegurando que no queda nada pendiente."""
        with cls._lock:
            if cls._instance is not None:
                cls._instance.stop()
                cls._instance = None

    # ---------------- Gestión de la cola ----------------

    def add(self, invoice_action):
        """Añade un documento a la cola de procesamiento."""
        with self._queue_lock:
            self._queue.append(invoice_action)
            count = len(self._queue)

        if count >= self.max_batch:
            self.process_batch()

    @property
    def count(self) -> int:
        with self._queue_lock:
            return len(self._queue)

    def start(self):
        """Inicia el hilo de control de flujo."""
        self._exit_event.clear()
        self._worker = threading.Thread(target=self._run, daemon=True)
        self._worker.start()

    def stop(self):
        """Detiene el hilo de control de flujo."""
        self._exit_event.set()

    def _run(self):
        """Bucle del control de flujo."""
        while not self._exit_event.is_set():
            wait = self._wait_seconds()
            if self._exit_event.wait(timeout=max(wait, 0.1)):
                break
            if self.count > 0:
                self.process_batch()
            else:
                # Sin elementos pendientes esperamos de nuevo
                self.current_wait_seconds = 0

    def _wait_seconds(self) -> float:
        """Segundos restantes hasta la próxima ejecución."""
        if self.last_process_moment is None or self.current_wait_seconds <= 0:
            return 0.1
        next_moment = self.last_process_moment + timedelta(
            seconds=self.current_wait_seconds)
        remaining = (next_moment - datetime.now()).total_seconds()
        return max(remaining, 0.0)

    def process_batch(self):
        """Procesa un lote: contabiliza y envía los documentos pendientes."""
        batch: List = []
        with self._queue_lock:
            take = min(len(self._queue), self.max_batch)
            batch = self._queue[:take]
            self._queue = self._queue[take:]

        if not batch:
            return

        seller_id = batch[0].invoice.seller_id if batch else None
        Utils.log(
            f"Enviando datos a la AEAT {seller_id} de {len(batch)} elementos")

        errors = []
        for action in batch:
            try:
                action.save()
            except Exception as ex:
                errors.append((action, ex))

        # Establece el momento de la próxima ejecución en función de la
        # respuesta de la AEAT (TiempoEsperaEnvio).
        self.last_process_moment = datetime.now()
        wait = self._extract_wait_seconds(batch)
        if wait > 0:
            self.current_wait_seconds = wait

        for action, ex in errors:
            Utils.log(f"Error enviando {action}: {ex}")

    @staticmethod
    def _extract_wait_seconds(batch) -> int:
        """Extrae TiempoEsperaEnvio de la respuesta de la AEAT."""
        for action in batch:
            respuesta = getattr(action, "respuestas_reg_factu_sistema_facturacion", None)
            if respuesta is not None and getattr(respuesta, "tiempo_espera_envio", 0):
                return int(respuesta.tiempo_espera_envio)
        return 0

    def __len__(self) -> int:
        return self.count
