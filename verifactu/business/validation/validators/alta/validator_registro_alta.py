"""ValidatorRegistroAlta - Validaciones del bloque RegistroAlta."""

import re
from typing import List, Optional

from verifactu.xml.factu.alta.registro_alta import RegistroAlta
from verifactu.xml.factu.alta.tipo_factura import TipoFactura


def _from_xml_date(value: str):
    from verifactu.xml.xml_parser import to_date
    return to_date(value)


class ValidatorRegistroAlta:
    """Valida los datos de RegistroAlta."""

    # ---------------- Validaciones de campos obligatorios ----------------

    @staticmethod
    def _get_campo_obligatorio_errors(ra: RegistroAlta) -> List[str]:
        result = []
        registro = ra
        if not registro.id_version:
            result.append(f"Error en el bloque RegistroAlta ({registro}):"
                          " El campo IDVersion es obligatorio")
        if registro.id_factura_alta is None or not registro.id_factura_alta.id_emisor_factura:
            result.append(f"Error en el bloque RegistroAlta ({registro}):"
                          " El campo IDFactura.IDEmisorFactura es obligatorio")
        if registro.id_factura_alta is None or not registro.id_factura_alta.num_serie_factura:
            result.append(f"Error en el bloque RegistroAlta ({registro}):"
                          " El campo IDFactura.NumSerieFactura es obligatorio")
        if registro.id_factura_alta is None or not registro.id_factura_alta.fecha_expedicion_factura:
            result.append(f"Error en el bloque RegistroAlta ({registro}):"
                          " El campo IDFactura.FechaExpedicionFactura es obligatorio")
        if not registro.nombre_razon_emisor:
            result.append(f"Error en el bloque RegistroAlta ({registro}):"
                          " El campo NombreRazonEmisor es obligatorio")

        for rectificada in (registro.facturas_rectificadas or []):
            if not rectificada.id_emisor_factura:
                result.append(
                    f"Error en el bloque RegistroAlta.FacturasRectificadas ({rectificada}):"
                    " El campo IDEmisorFactura es obligatorio")
            if not rectificada.num_serie_factura:
                result.append(
                    f"Error en el bloque RegistroAlta.FacturasRectificadas ({rectificada}):"
                    " El campo NumSerieFactura es obligatorio")
            if not rectificada.fecha_expedicion_factura:
                result.append(
                    f"Error en el bloque RegistroAlta.FacturasRectificadas ({rectificada}):"
                    " El campo FechaExpedicionFactura es obligatorio")

        for sustituida in (registro.facturas_sustituidas or []):
            if not sustituida.id_emisor_factura:
                result.append(
                    f"Error en el bloque RegistroAlta.FacturasSustituidas ({sustituida}):"
                    " El campo IDEmisorFactura es obligatorio")
            if not sustituida.num_serie_factura:
                result.append(
                    f"Error en el bloque RegistroAlta.FacturasSustituidas ({sustituida}):"
                    " El campo NumSerieFactura es obligatorio")
            if not sustituida.fecha_expedicion_factura:
                result.append(
                    f"Error en el bloque RegistroAlta.FacturasSustituidas ({sustituida}):"
                    " El campo FechaExpedicionFactura es obligatorio")

        if not registro.descripcion_operacion:
            result.append(f"Error en el bloque RegistroAlta ({registro}):"
                          " El campo DescripcionOperacion es obligatorio")

        # Tercero
        if registro.tercero is not None:
            if not registro.tercero.nombre_razon:
                result.append(f"Error en el bloque RegistroAlta ({registro}):"
                              " El campo Tercero.NombreRazon es obligatorio")
            if registro.tercero.id_otro is None and not registro.tercero.nif:
                result.append(f"Error en el bloque RegistroAlta ({registro}):"
                              " El campo Tercero.NIF es obligatorio")
            if registro.tercero.id_otro is not None and not registro.tercero.id_otro.id:
                result.append(f"Error en el bloque RegistroAlta ({registro}):"
                              " El campo Tercero.IDOtro.ID es obligatorio")

        return result

    # ---------------- Validación de IDFactura ----------------

    @staticmethod
    def _get_id_factura_errors(ra: RegistroAlta) -> List[str]:
        result = []
        registro = ra
        idf = registro.id_factura_alta
        if idf is None:
            return result

        fecha = idf.fecha_expedicion_factura
        if fecha and not re.match(r"^\d{2}-\d{2}-\d{4}$", fecha):
            result.append(
                f"Error en el bloque RegistroAlta ({registro}):"
                " La propiedad IDFactura.FechaExpedicion tiene que tener un valor"
                " con formato dd-mm-yyyy.")

        return result

    # ---------------- CuotaTotal ----------------

    @staticmethod
    def _get_cuota_total_errors(ra: RegistroAlta) -> List[str]:
        from decimal import Decimal

        result = []
        registro = ra

        # 16. CuotaTotal: Ʃ (CuotaRepercutida + CuotaRecargoEquivalencia)
        # +/- 10,00 euros.
        if registro.num_registro_acuerdo_facturacion or \
                registro.factura_sin_identif_destinatario_art61d == "S":
            return result

        if registro.desglose:
            total = Decimal("0")
            for detalle in registro.desglose:
                if detalle.cuota_repercutida:
                    total += Decimal(detalle.cuota_repercutida.replace(",", "."))
                if detalle.cuota_recargo_equivalencia:
                    total += Decimal(detalle.cuota_recargo_equivalencia.replace(",", "."))

            cuota_total = Decimal(
                registro.cuota_total.replace(",", ".")) if registro.cuota_total \
                else Decimal("0")

            if abs(cuota_total - total) > Decimal("10"):
                result.append(
                    f"[3.1.3-16.0] Error en el bloque RegistroAlta ({registro}):"
                    " Ʃ (CuotaRepercutida + CuotaRecargoEquivalencia) debe ser"
                    " igual a CuotaTotal +/- 10,00 euros.")
        return result

    # ---------------- ImporteTotal ----------------

    @staticmethod
    def _get_importe_total_errors(ra: RegistroAlta) -> List[str]:
        from decimal import Decimal
        from verifactu.xml.factu.alta.clave_regimen import ClaveRegimen

        result = []
        registro = ra
        if registro.desglose:
            # 17. ImporteTotal: Ʃ (BaseImponibleOimporteNoSujeto +
            # CuotaRepercutida + CuotaRecargoEquivalencia) +/- 10,00 euros.
            # No aplicable cuando ClaveRegimen sea 03, 05, 06, 08 o 09.
            claves_excluidas = (ClaveRegimen.Rebu, ClaveRegimen.AgenciasViajes,
                                ClaveRegimen.GrupoEntidades, ClaveRegimen.IpsiIgic,
                                ClaveRegimen.MediadoresAgenciasViaje)

            if registro.num_registro_acuerdo_facturacion or \
                    registro.factura_sin_identif_destinatario_art61d == "S":
                return result

            total = Decimal("0")
            for detalle in registro.desglose:
                if detalle.clave_regimen in claves_excluidas:
                    return result
                if detalle.base_imponible_o_importe_no_sujeto:
                    total += Decimal(
                        detalle.base_imponible_o_importe_no_sujeto.replace(",", "."))
                if detalle.cuota_repercutida:
                    total += Decimal(detalle.cuota_repercutida.replace(",", "."))
                if detalle.cuota_recargo_equivalencia:
                    total += Decimal(
                        detalle.cuota_recargo_equivalencia.replace(",", "."))

            importe_total = Decimal(
                registro.importe_total.replace(",", ".")) if registro.importe_total \
                else Decimal("0")

            if abs(importe_total - total) > Decimal("10"):
                result.append(
                    f"[3.1.3-17.0] Error en el bloque RegistroAlta ({registro}):"
                    " Ʃ (BaseImponibleOimporteNoSujeto + CuotaRepercutida +"
                    " CuotaRecargoEquivalencia) debe ser igual a ImporteTotal"
                    " +/- 10,00 euros.")
        return result

    # ---------------- FechaOperacion ----------------

    @staticmethod
    def _get_fecha_operacion_errors(ra: RegistroAlta) -> List[str]:
        result = []
        registro = ra
        fecha_operacion = registro.fecha_operacion
        if fecha_operacion:
            if not re.match(r"^\d{2}-\d{2}-\d{4}$", fecha_operacion):
                result.append(
                    f"Error en el bloque RegistroAlta ({registro}):"
                    " La propiedad FechaOperacion tiene que tener un valor"
                    " con formato dd-mm-yyyy.")
            else:
                fecha_expedicion = _from_xml_date(
                    registro.id_factura_alta.fecha_expedicion_factura)
                fecha_operacion_dt = _from_xml_date(fecha_operacion)
                if fecha_operacion_dt > fecha_expedicion:
                    result.append(
                        f"Error en el bloque RegistroAlta ({registro}):"
                        " La FechaOperacion no puede ser posterior a la fecha"
                        " de expedición.")
        return result

    # ---------------- Huella ----------------

    @staticmethod
    def _get_huella_errors(ra: RegistroAlta) -> List[str]:
        result = []
        registro = ra
        encadenamiento = registro.encadenamiento
        if encadenamiento is not None and encadenamiento.registro_anterior is not None:
            huella = encadenamiento.registro_anterior.huella
            if huella is not None and len(huella) != 64:
                result.append(
                    f"Error en el bloque RegistroAlta ({registro}):"
                    " La Huella del registro anterior debe tener una longitud"
                    " de 64 caracteres.")
        return result

    # ---------------- TipoFactura / TipoRectificativa ----------------

    @staticmethod
    def _get_tipo_rectificativa_errors(ra: RegistroAlta) -> List[str]:
        result = []
        registro = ra
        is_rectificativa = registro.tipo_factura in (
            TipoFactura.R1, TipoFactura.R2, TipoFactura.R3, TipoFactura.R4, TipoFactura.R5)

        if is_rectificativa:
            if registro.tipo_rectificativa is None or not registro.tipo_rectificativa_specified:
                result.append(
                    f"Error en el bloque RegistroAlta ({registro}):"
                    " El campo TipoRectificativa es obligatorio para facturas"
                    " rectificativas.")
        else:
            if registro.tipo_rectificativa_specified and registro.tipo_rectificativa is not None:
                result.append(
                    f"Error en el bloque RegistroAlta ({registro}):"
                    " El campo TipoRectificativa sólo puede informarse en facturas"
                    " rectificativas.")
        return result

    # ---------------- Método principal ----------------

    @classmethod
    def get_errors(cls, registro_alta: RegistroAlta) -> List[str]:
        """Ejecuta las validaciones y devuelve una lista con los errores."""
        result = []

        if not isinstance(registro_alta, RegistroAlta):
            return result

        result.extend(cls._get_campo_obligatorio_errors(registro_alta))
        result.extend(cls._get_id_factura_errors(registro_alta))
        result.extend(cls._get_tipo_rectificativa_errors(registro_alta))
        result.extend(cls._get_fecha_operacion_errors(registro_alta))
        result.extend(cls._get_cuota_total_errors(registro_alta))
        result.extend(cls._get_importe_total_errors(registro_alta))
        result.extend(cls._get_huella_errors(registro_alta))

        # 15. Agrupación Desglose
        from verifactu.business.validation.validators.alta.detalle.validator_registro_alta_detalle_desglose import (
            ValidatorRegistroAltaDetalleDesglose)
        for detalle in (registro_alta.desglose or []):
            result.extend(ValidatorRegistroAltaDetalleDesglose.get_errors(detalle))

        return result
