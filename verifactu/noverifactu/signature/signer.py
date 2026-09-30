"""Signer - Firma XAdES de registros (modo NO VERI*FACTU)."""

from typing import Optional


class Signer:
    """Firma electrónica XAdES-EPES de registros de facturación.

    Requiere el paquete ``cryptography`` y ``xmlsec`` para la firma
    XML digital. En el modo NO VERI*FACTU los registros se almacenan
    firmados localmente.
    """

    def __init__(self, certificate: Optional[object] = None):
        self.certificate = certificate

    def sign(self, registro) -> bytes:
        """Firma el xml del registro y devuelve los bytes firmados."""
        raise NotImplementedError(
            "La firma XAdES (modo NO VERI*FACTU) requiere los paquetes"
            " 'cryptography' y 'xmlsec'. Instale con:"
            " pip install cryptography xmlsec")


class SignatureVerifier:
    """Verificación de firmas XAdES."""

    @staticmethod
    def verify(xml: bytes) -> bool:
        """Verifica la firma XAdES de un documento xml."""
        raise NotImplementedError(
            "La verificación XAdES requiere los paquetes"
            " 'cryptography' y 'xmlsec'. Instale con:"
            " pip install cryptography xmlsec")
