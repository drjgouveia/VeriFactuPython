"""NifValidation - Validación en línea de NIF con la AEAT."""

from typing import Optional, List

from verifactu.config.settings import Settings


class NifValidation:
    """Valida el NIF y el nombre de un contribuyente mediante el
    servicio web de la AEAT (VNifV2) o mediante el API REST."""

    def __init__(self, nif: Optional[str], name: Optional[str]):
        self._nif = nif
        self._name = name

    def get_errors(self) -> List[str]:
        """Devuelve los errores de la validación del NIF."""
        if Settings.current.skip_nif_aeat_validation:
            return []

        from verifactu.business.validation.nif.tax_id.tax_id_es import TaxIdEs, TaxIdEsException

        errors = []
        try:
            tax_id = TaxIdEs(self._nif)
            if not tax_id.is_dc_ok:
                errors.append(f"El NIF '{self._nif}' no es válido.")
        except TaxIdEsException:
            errors.append(f"El NIF '{self._nif}' no tiene un formato válido.")
        except Exception:
            errors.append(f"El NIF '{self._nif}' no es válido.")
        return errors
