"""ValidatorRegistroFactura - Validaciones del bloque RegistroFactura (3.1.2)."""

from typing import List


class ValidatorRegistroFactura:
    """Valida los datos de RegistroFactura."""

    @staticmethod
    def get_errors(registro) -> List[str]:
        """Ejecuta las validaciones y devuelve una lista con los errores."""
        result = []

        from verifactu.xml.factu.alta.registro_alta import RegistroAlta
        from verifactu.xml.factu.anulacion.registro_anulacion import RegistroAnulacion
        from verifactu.business.validation.validators.alta.validator_registro_alta import (
            ValidatorRegistroAlta)
        from verifactu.business.validation.validators.anulacion.validator_registro_anulacion import (
            ValidatorRegistroAnulacion)

        if isinstance(registro, RegistroAlta):
            result.extend(ValidatorRegistroAlta.get_errors(registro))
        elif isinstance(registro, RegistroAnulacion):
            result.extend(ValidatorRegistroAnulacion.get_errors(registro))
        else:
            result.append(
                f"[0.0.1-0.1] Error en el bloque RegistroFactura.Registro: Se ha"
                f" encontrado un elemento de la clase {type(registro).__name__} en la"
                f" colección RegistroFactura. Esta colección sólo admite elementos del"
                f" tipo RegistroAlta o RegistroAnulacion.")

        return result
