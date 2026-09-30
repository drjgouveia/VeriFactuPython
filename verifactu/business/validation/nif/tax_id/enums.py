"""Enums for Spanish tax ID validation."""

from enum import Enum


class TaxIdEsDCNif(Enum):
    """Dígito de control de un NIF de persona jurídica."""
    J = 0
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7
    H = 8
    I = 9


class TaxIdEsDCDniNie(Enum):
    """Dígito de control de un DNI o NIE."""
    T = 0
    R = 1
    W = 2
    A = 3
    G = 4
    M = 5
    Y = 6
    F = 7
    P = 8
    D = 9
    X = 10
    B = 11
    N = 12
    J = 13
    Z = 14
    S = 15
    Q = 16
    V = 17
    H = 18
    L = 19
    C = 20
    K = 21
    E = 22


class TaxIdEsTypes(Enum):
    """Tipo de número de identificación fiscal."""
    DNI = "DNI"
    NIF = "NIF"
    NIE = "NIE"


class TaxIdEsError(Enum):
    """Último error en la validación del número de identificación fiscal."""
    NoError = "NoError"
    InvalidString = "InvalidString"
    InvalidFirstChar = "InvalidFirstChar"
    InvalidLength = "InvalidLength"
    InvalidControlNumber = "InvalidControlNumber"


class TaxIdEsPersonTypeCode(Enum):
    """Tipo de persona. Física o jurídica."""
    LegalEntity = "LegalEntity"
    Individual = "Individual"
