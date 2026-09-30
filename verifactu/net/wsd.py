"""Wsd - Gestión de las operaciones con los servicios web de la AEAT."""

import os
from datetime import datetime
from typing import Optional, Dict

from verifactu.config.settings import Settings

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class Certificate:
    """Representación simplificada de un certificado X509."""

    def __init__(self, cert_path: str, password: str = None):
        self.cert_path = cert_path
        self.password = password
        self._not_after = None
        self._load()

    def _load(self):
        try:
            from cryptography import x509
            from cryptography.hazmat.primitives.serialization import pkcs12
            with open(self.cert_path, "rb") as f:
                data = f.read()
            if self.password:
                key, cert, additional = pkcs12.load_key_and_certificates(
                    data, self.password.encode())
            else:
                key, cert, additional = pkcs12.load_key_and_certificates(data, None)
            self._cert_obj = cert
            self._key_obj = key
            self._not_after = cert.not_valid_after_utc
            self.subject = cert.subject.rfc4514_string()
        except ImportError:
            self._cert_obj = None
            self._key_obj = None
            self._not_after = None

    @property
    def not_after(self):
        return self._not_after


class Wsd:
    """Gestiona las operaciones con los servicios web de la AEAT."""

    certificate: Optional[Certificate] = None
    http_clients: Dict[str, object] = {}

    @classmethod
    def get_checked_certificate(cls) -> Certificate:
        """Obtiene el certificado configurado y verifica la validez."""
        certificate = cls.get_certificate()
        if certificate is None:
            raise ValueError(
                "Certificate is null. Maybe serial number in configuration was wrong.")
        cls.check_certificate(certificate)
        return certificate

    @classmethod
    def check_certificate(cls, certificate: Certificate):
        """Verifica la validez del certificado."""
        if certificate.not_after is not None and certificate.not_after < datetime.now(
                certificate.not_after.tzinfo):
            raise ValueError(
                f"Certificate is out of date. NotAfter: {certificate.not_after}.")

    @classmethod
    def get_certificate(cls) -> Optional[Certificate]:
        """Devuelve el certificado de la configuración.

        Jerarquía: 1. valor establecido; 2. fichero; 3. huella digital;
        4. número de serie (últimos dos solo disponibles en Windows).
        """
        if cls.certificate is not None:
            return cls.certificate
        cert = cls.get_certificate_by_file()
        if cert is not None:
            return cert
        return None

    @classmethod
    def get_certificate_by_file(cls) -> Optional[Certificate]:
        """Devuelve el certificado establecido en la configuración por ruta de fichero."""
        path = Settings.current.certificate_path
        if path and os.path.exists(path):
            return Certificate(path, Settings.current.certificate_password or None)
        return None

    @classmethod
    def call(cls, url: str, action: str, xml_document: bytes,
             certificate: Certificate = None) -> str:
        """Llama al web service de la AEAT para el VeriFactu seleccionado."""
        if not HAS_REQUESTS:
            raise ImportError("El paquete 'requests' es necesario para las comunicaciones.")

        cert = certificate or cls.get_checked_certificate()

        cert_obj = getattr(cert, "_cert_obj", None)
        key_obj = getattr(cert, "_key_obj", None)
        client_cert = None
        if cert_obj is not None and key_obj is not None:
            # requests necesita archivos PEM; usamos archivos temporales
            import tempfile
            tmp_dir = tempfile.gettempdir()
            cert_pem = os.path.join(tmp_dir, "verifactu_cert.pem")
            key_pem = os.path.join(tmp_dir, "verifactu_key.pem")
            try:
                from cryptography.hazmat.primitives import serialization
                with open(cert_pem, "wb") as f:
                    f.write(cert_obj.public_bytes(serialization.Encoding.PEM))
                if cert.password:
                    with open(key_pem, "wb") as f:
                        f.write(key_obj.private_bytes(
                            serialization.Encoding.PEM,
                            serialization.PrivateFormat.PKCS8,
                            serialization.BestAvailableEncryption(cert.password.encode())))
                else:
                    with open(key_pem, "wb") as f:
                        f.write(key_obj.private_bytes(
                            serialization.Encoding.PEM,
                            serialization.PrivateFormat.PKCS8,
                            serialization.NoEncryption()))
                client_cert = (cert_pem, key_pem)
            except Exception:
                client_cert = None

        response = requests.post(
            url,
            data=xml_document,
            headers={
                "Content-Type": "text/xml;charset=\"utf-8\"",
                "Accept": "text/xml",
                "SOAPAction": action,
            },
            cert=client_cert,
            timeout=100,
        )
        response.raise_for_status()
        return response.text
