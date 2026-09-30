"""ValidatorCabecera - Validaciones del bloque Cabecera (3.1.1)."""

import re
from datetime import datetime
from typing import List


class ValidatorCabecera:
    """Valida los datos de Cabecera."""

    @staticmethod
    def get_errors(cabecera) -> List[str]:
        """Ejecuta las validaciones y devuelve una lista con los errores."""
        from verifactu.config.settings import Settings

        result = []

        # 1. ObligadoEmision
        if cabecera is None or cabecera.obligado_emision is None or \
                cabecera.obligado_emision.nif is None:
            result.append(
                "[3.1.1-1.0] Error en el bloque Cabecera: El NIF del bloque"
                " ObligadoEmision debe contener un valor")
        else:
            obligado = cabecera.obligado_emision
            # El interlocutor en ObligadoEmision sólo puede contener datos en NIF y NombreRazon
            if (getattr(obligado, "nombre_razon_representante", None) is not None
                    or getattr(obligado, "nif_representante", None) is not None
                    or getattr(obligado, "id_otro", None) is not None):
                result.append(
                    "[3.1.1-1.1] El campo 'ObligadoEmision' no puede contener"
                    " información en 'NombreRazonRepresentante' o 'NIFRepresentante'.")

            if not Settings.current.skip_nif_aeat_validation:
                from verifactu.business.validation.nif.nif_validation import NifValidation
                for error in NifValidation(obligado.nif, obligado.nombre_razon).get_errors():
                    result.append(f"[3.1.1-1.2] {error}")

        # 2. Representante
        if cabecera is not None and cabecera.representante is not None:
            representante = cabecera.representante
            if representante.nif is None:
                result.append(
                    "[3.1.1-2.0] Error en el bloque Cabecera: El valor del campo NIF"
                    " del bloque Representante no está identificado")

            if not Settings.current.skip_nif_aeat_validation:
                from verifactu.business.validation.nif.nif_validation import NifValidation
                for error in NifValidation(
                        representante.nif, representante.nombre_razon).get_errors():
                    result.append(f"[3.1.1-2.1] {error}")

            if (getattr(representante, "nombre_razon_representante", None) is not None
                    or getattr(representante, "nif_representante", None) is not None
                    or getattr(representante, "id_otro", None) is not None):
                result.append(
                    f"[3.1.1-2.2] Error en el bloque Representante ({representante}):"
                    " Los datos de interlocutor 'NombreRazonRepresentante' y"
                    " 'NIFRepresentante' no pueden contener valor.")

        # 3. FechaFinVeriFactu
        fecha_fin_veri_factu = None
        if cabecera is not None and cabecera.remision_voluntaria is not None:
            fecha_fin_veri_factu = getattr(
                cabecera.remision_voluntaria, "fecha_fin_veri_factu", None)

        if fecha_fin_veri_factu is not None:
            if not re.match(r"31-12-20\d{2}", fecha_fin_veri_factu):
                result.append(
                    "[3.1.1-3.0] Error en el bloque Cabecera: La fecha FechaFinVeriFactu"
                    " debe tener el formato 31-12-20XX.")
            else:
                try:
                    year = int(fecha_fin_veri_factu[6:10])
                    if year > datetime.now().year or year < datetime.now().year - 1:
                        result.append(
                            "[3.1.1-3.1] Error en el bloque Cabecera: El año de la fecha"
                            " FechaFinVeriFactu deberá ser igual al año de la fecha del"
                            " sistema de la AEAT, o al año anterior.")
                except (ValueError, IndexError):
                    result.append(
                        "[3.1.1-3.0] Error en el bloque Cabecera: La fecha"
                        " FechaFinVeriFactu debe tener el formato 31-12-20XX.")

        # 5. RefRequerimiento
        if cabecera is not None and cabecera.remision_requerimiento is not None:
            result.append(
                "[3.1.1-5.0] Error en el bloque Cabecera: RefRequerimiento: Sólo se"
                " permite contenido en sistemas que emiten facturas no verificables,"
                " la biblioteca Verifactu ha sido diseñada para funcionar únicamente"
                " como sistema verificable.")

        return result
