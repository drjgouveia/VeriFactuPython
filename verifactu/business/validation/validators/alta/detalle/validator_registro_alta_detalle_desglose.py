"""ValidatorRegistroAltaDetalleDesglose - Validaciones del bloque Desglose."""

from decimal import Decimal

from typing import List


class ValidatorRegistroAltaDetalleDesglose:
    """Valida los datos de DetalleDesglose."""

    @classmethod
    def get_errors(cls, detalle) -> List[str]:
        """Ejecuta las validaciones y devuelve una lista con los errores."""
        result = []

        if detalle is None:
            return result

        from decimal import Decimal
        from verifactu.xml.factu.impuesto import Impuesto
        from verifactu.xml.factu.alta.calificacion_operacion import CalificacionOperacion
        from verifactu.xml.factu.alta.causa_exencion import CausaExencion

        # Operaciones exentas no pueden tener tipo ni cuota
        if detalle.operacion_exenta is not None and \
                detalle.operacion_exenta != CausaExencion.NA:
            if detalle.tipo_impositivo or detalle.cuota_repercutida:
                result.append(
                    f"Error en el bloque RegistroAlta.DetalleDesglose ({detalle}):"
                    " Operación exenta no puede tener TipoImpositivo ni"
                    " CuotaRepercutida informados.")

        # CalificacionOperacion N1/N2 con impuesto IVA no puede tener cuota
        is_n = detalle.calificacion_operacion in (
            CalificacionOperacion.N1, CalificacionOperacion.N2)
        if is_n and detalle.impuesto == Impuesto.IVA:
            if detalle.tipo_impositivo or detalle.cuota_repercutida:
                result.append(
                    f"Error en el bloque RegistroAlta.DetalleDesglose ({detalle}):"
                    " El valor del campo CalificacionOperacion está informado como N1"
                    " o N2 y el impuesto es IVA. No se puede informar de los campos"
                    " TipoImpositivo, CuotaRepercutida, TipoRecargoEquivalencia y"
                    " CuotaRecargoEquivalencia.")

        # Coherencia base x tipo = cuota (tolerancia de redondeo)
        if detalle.tipo_impositivo and detalle.base_imponible_o_importe_no_sujeto \
                and detalle.cuota_repercutida:
            base = Decimal(detalle.base_imponible_o_importe_no_sujeto.replace(",", "."))
            rate = Decimal(detalle.tipo_impositivo.replace(",", "."))
            cuota = Decimal(detalle.cuota_repercutida.replace(",", "."))
            expected = cls._round(base * rate / Decimal("100"))
            if abs(expected - cuota) > Decimal("0.01"):
                result.append(
                    f"Error en el bloque RegistroAlta.DetalleDesglose ({detalle}):"
                    " La CuotaRepercutida no se corresponde con la BaseImponible"
                    " aplicando el TipoImpositivo.")

        return result

    @staticmethod
    def _round(value: Decimal) -> Decimal:
        from decimal import ROUND_HALF_UP
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
