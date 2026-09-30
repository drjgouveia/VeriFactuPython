"""ValidatorRegistroAnulacion - Validaciones del bloque RegistroAnulacion."""

import re
from typing import List


class ValidatorRegistroAnulacion:
    """Valida los datos de RegistroAnulacion."""

    @staticmethod
    def get_errors(registro) -> List[str]:
        """Ejecuta las validaciones y devuelve una lista con los errores."""
        result = []

        if registro is None:
            return result

        from verifactu.xml.factu.anulacion.registro_anulacion import RegistroAnulacion
        ra = registro

        if not ra.id_version:
            result.append(f"Error en el bloque RegistroAnulacion ({ra}):"
                          " El campo IDVersion es obligatorio")

        idf = ra.id_factura_anulada
        if idf is None:
            result.append(f"Error en el bloque RegistroAnulacion ({ra}):"
                          " El bloque IDFacturaAnulada es obligatorio")
        else:
            if not idf.id_emisor_factura_anulada:
                result.append(f"Error en el bloque RegistroAnulacion ({ra}):"
                              " El campo IDFactura.IDEmisorFacturaAnulada es obligatorio")
            if not idf.num_serie_factura_anulada:
                result.append(f"Error en el bloque RegistroAnulacion ({ra}):"
                              " El campo IDFactura.NumSerieFacturaAnulada es obligatorio")
            if not idf.fecha_expedicion_factura_anulada:
                result.append(f"Error en el bloque RegistroAnulacion ({ra}):"
                              " El campo IDFactura.FechaExpedicionFacturaAnulada"
                              " es obligatorio")
            elif not re.match(r"^\d{2}-\d{2}-\d{4}$", idf.fecha_expedicion_factura_anulada):
                result.append(f"Error en el bloque RegistroAnulacion ({ra}):"
                              " La propiedad IDFactura.FechaExpedicionFacturaAnulada"
                              " tiene que tener un valor con formato dd-mm-yyyy.")

        if not ra.nombre_razon_emisor:
            result.append(f"Error en el bloque RegistroAnulacion ({ra}):"
                          " El campo NombreRazonEmisor es obligatorio")

        if not ra.fecha_hora_huso_gen_registro and not ra.ordered_fecha_hora_huso_gen_registro:
            result.append(f"Error en el bloque RegistroAnulacion ({ra}):"
                          " El campo FechaHoraHusoGenRegistro es obligatorio")

        if not ra.huella and not ra.ordered_huella:
            result.append(f"Error en el bloque RegistroAnulacion ({ra}):"
                          " El campo Huella es obligatorio")

        return result
