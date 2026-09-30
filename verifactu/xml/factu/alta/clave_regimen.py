"""Enum: ClaveRegimen - Tax regime codes."""

from enum import Enum


class ClaveRegimen(Enum):
    """Clave que identifica el tipo de régimen del IVA o IGIC."""
    RegimenGeneral = "01"
    Exportacion = "02"
    Rebu = "03"
    OroInversion = "04"
    AgenciasViajes = "05"
    GrupoEntidades = "06"
    Recc = "07"
    IpsiIgic = "08"
    MediadoresAgenciasViaje = "09"
    CobroTerceros = "10"
    ArrendamientoLocalNecocio = "11"
    ArrendamientoLocalNecocioNoRetencion = "12"
    ObraPteDevengoAdmonPublica = "14"
    TractoSucesivoPteDevengo = "15"
    IossRegEspMin = "17"
    RecEquivPeqEmp = "18"
    RegimenEspecialAgriculturaArt25Ley19 = "19"
    RegimenSimplificado = "20"
    RegimenSimplificadoIpsi = "21"