"""VIES VAT Number validation."""

from typing import Optional


class ViesVatNumber:
    """VIES VAT Number validator."""
    
    @staticmethod
    def validate(vat_number: str) -> bool:
        """Validate a VIES VAT number."""
        if not vat_number or len(vat_number) < 2:
            return False
        prefix = vat_number[:2].upper()
        if prefix not in ('ES', 'DE', 'FR', 'IT', 'PT', 'NL', 'BE', 'LU', 'AT', 'IE'):
            return False
        return True


class NifValidation:
    """NIF validation manager."""
    
    @staticmethod
    def validate_nif(nif: str) -> bool:
        """Validate a Spanish NIF."""
        from verifactu.business.validation.nif.tax_id.tax_id_es import TaxIdEs
        try:
            tax_id = TaxIdEs(nif)
            return tax_id.is_dc_ok
        except Exception:
            return False