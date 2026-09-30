"""VeriFactuEndPointPrefixes - API endpoint prefixes."""

from dataclasses import dataclass


@dataclass
class VeriFactuEndPointPrefixes:
    """API endpoint prefixes for VeriFactu."""
    Test: str = "https://prewww2.aeat.es/wlpl/TIKE-CONT/Alta"
    TestReq: str = "https://prewww2.aeat.es/wlpl/TIKE-CONT/Req"
    TestValidate: str = "https://prewww2.aeat.es/wlpl/TIKE-CONT/ValidarQR"
    Production: str = "https://www2.agenciatributaria.gob.es/wlpl/TIKE-CONT/Alta"
    ProductionReq: str = "https://www2.agenciatributaria.gob.es/wlpl/TIKE-CONT/Req"
    ProductionValidate: str = "https://www2.agenciatributaria.gob.es/wlpl/TIKE-CONT/ValidarQR"