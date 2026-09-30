"""TaxIdEs - Validación de números de identificación fiscal españoles.

Port of ``VeriFactu.Business.Validation.NIF.TaxId.TaxIdEs`` (C#).
Valida NIF, DNI y NIE de acuerdo con el Real Decreto 1065/2007, de 27 de julio.
"""

import re

from verifactu.business.validation.nif.tax_id.enums import (
    TaxIdEsDCDniNie,
    TaxIdEsDCNif,
    TaxIdEsError,
    TaxIdEsPersonTypeCode,
    TaxIdEsTypes,
)
from verifactu.business.validation.nif.tax_id.tax_id_es_exception import TaxIdEsException

# Regular expressions related to TaxIdentificationNumber
PatternTaxIdentification = r"(\b[A-HJ-NP-SU-Z0-9]{1}[0-9]{7}[A-NP-TV-Z0-9]{1}\b)"
PatternTaxIdNieIndividual = r"(\b[XYZ]{1}[0-9]{7}[A-HJ-NP-Z]{1}\b)"
PatternTaxIdDniIndividual = r"(\b[0-9]{1}[0-9]{7}[A-HJ-NP-Z]{1}\b)"
PatternTaxIdNifIndividual = r"(\b[KLM]{1}[0-9]{7}[A-HJ-NP-Z]{1}\b)"
PatternTaxIdNifLegalEntity = r"(\b[A-HJ-NP-SUVW]{1}[0-9]{8}\b)"
PatternTaxIdNifLegalEntityNRyCL = r"(\b[BSNPQRW]{1}[0-9]{7}[A-NP-Z]{1}\b)"

# Tipos de organizaciones asociados a la primera letra del NIF de persona jurídica.
LegalEntities = {
    "A": "Sociedades anónimas",
    "B": "Sociedades de responsabilidad limitada",
    "C": "Sociedades colectivas",
    "D": "Sociedades comanditarias",
    "E": "Comunidades de bienes y herencias yacentes",
    "F": "Sociedades cooperativas",
    "G": "Asociaciones",
    "H": "Comunidades de propietarios en régimen de propiedad horizontal",
    "J": "Sociedades civiles, con o sin personalidad jurídica",
    "N": "Entidades extranjeras",
    "P": "Corporaciones Locales",
    "Q": "Organismos públicos",
    "R": "Congregaciones e instituciones religiosas",
    "S": "Órganos de la Administración del Estado y de las Comunidades Autónomas",
    "U": "Uniones Temporales de Empresas",
    "V": "Otros tipos no definidos en el resto de claves",
    "W": "Establecimientos permanentes de entidades no residentes en España",
}

# Tipos de personas físicas definidos por la letra del NIF o NIE.
Individuals = {
    "K": "Españoles menores de 14 años que carezcan de DNI.",
    "L": "Españoles mayores de 14 años residentes en el extranjero y que no tengan DNI.",
    "M": "Extranjeros sin NIE, de forma transitoria o definitiva.",
    "X": "Extranjeros residentes en España identificados con NIE asignado hasta el 15 de julio de 2008.",
    "Y": "Extranjeros residentes en España identificados con NIE asignado desde el 16 de julio de 2008.",
    "Z": "Letra reservada para Extranjeros identificados por la Policía, para cuando se agoten los 'NIE Y'",
}


class TaxIdEs:
    """Valida y obtiene información de números de identificación fiscal españoles."""

    def __init__(self, taxcode: str = None):
        self.person_type = None
        self.person_type_den = ""
        self.tax_identification_type = None
        self.last_error = TaxIdEsError.NoError
        self.dc_str = ""
        self.dc_num = 0
        self.is_dc_num = False
        self.is_dc_ok = False

        self._tax_code = None
        self._str_first = ""

        self._rgx_tax_identification = re.compile(PatternTaxIdentification)
        self._rgx_tax_id_nie_individual = re.compile(PatternTaxIdNieIndividual)
        self._rgx_tax_id_dni_individual = re.compile(PatternTaxIdDniIndividual)
        self._rgx_tax_id_nif_individual = re.compile(PatternTaxIdNifIndividual)
        self._rgx_tax_id_nif_legal_entity = re.compile(PatternTaxIdNifLegalEntity)
        self._rgx_tax_id_nif_legal_entity_nr_cl = re.compile(PatternTaxIdNifLegalEntityNRyCL)

        if taxcode is not None:
            self.tax_code = taxcode

    @property
    def tax_code(self):
        return self._tax_code

    @tax_code.setter
    def tax_code(self, value):
        if value is None:
            self._tax_code = None
            self.last_error = TaxIdEsError.InvalidString
            return

        self._tax_code = value.upper()

        if not self._rgx_tax_identification.search(self._tax_code):
            self._tax_code = None
            self.last_error = TaxIdEsError.InvalidString
            return
        self.dc_str = self._tax_code[-1:]
        try:
            self.dc_num = int(self.dc_str)
            self.is_dc_num = True
            self.dc_str = ""
        except ValueError:
            self.is_dc_num = False
            self.dc_num = 0

        self._str_first = self._tax_code[0]

        if self._str_first.isdigit():
            self.person_type = TaxIdEsPersonTypeCode.Individual
            self.person_type_den = ("Españoles con documento nacional de identidad"
                                    " (DNI) asignado por el Ministerio del Interior")
            self.tax_identification_type = TaxIdEsTypes.DNI
        elif self._str_first in Individuals:
            self.person_type = TaxIdEsPersonTypeCode.Individual
            self.person_type_den = Individuals[self._str_first]
            if self._str_first in ("K", "L", "M"):
                self.tax_identification_type = TaxIdEsTypes.NIF
            else:
                self.tax_identification_type = TaxIdEsTypes.NIE
        elif self._str_first in LegalEntities:
            self.person_type = TaxIdEsPersonTypeCode.LegalEntity
            self.person_type_den = LegalEntities[self._str_first]
            self.tax_identification_type = TaxIdEsTypes.NIF
        else:
            self.last_error = TaxIdEsError.InvalidFirstChar

        if self._tax_code is None:
            return

        if self.tax_identification_type == TaxIdEsTypes.DNI:
            if not self._rgx_tax_id_dni_individual.search(self._tax_code):
                raise TaxIdEsException(
                    f"TaxIdEs.DNI don't match the pattern: {PatternTaxIdDniIndividual}")
        elif self.tax_identification_type == TaxIdEsTypes.NIE:
            if not self._rgx_tax_id_nie_individual.search(self._tax_code):
                raise TaxIdEsException(
                    f"TaxIdEs.DNI don't match the pattern: {PatternTaxIdNieIndividual}")
        elif self.tax_identification_type == TaxIdEsTypes.NIF:
            if self.person_type == TaxIdEsPersonTypeCode.Individual:
                if not self._rgx_tax_id_nif_individual.search(self._tax_code):
                    raise TaxIdEsException(
                        f"TaxIdEs.DNI don't match the pattern: {PatternTaxIdNifIndividual}")
            elif self.person_type == TaxIdEsPersonTypeCode.LegalEntity:
                if (not self._rgx_tax_id_nif_legal_entity.search(self._tax_code)
                        and not self._rgx_tax_id_nif_legal_entity_nr_cl.search(self._tax_code)):
                    raise TaxIdEsException(
                        f"TaxIdEs.DNI don't match the pattern: {PatternTaxIdNifLegalEntity}")
            else:
                raise TaxIdEsException("Unknown TaxIdEsPersonTypeCode.")
        else:
            raise TaxIdEsException("Unknown TaxIdentificationType.")

        if self.tax_identification_type == TaxIdEsTypes.NIF:
            dc = self._get_dc_nif()
            if self.is_dc_num:
                self.is_dc_ok = dc.value == self.dc_num
            else:
                try:
                    self.is_dc_ok = dc.value == TaxIdEsDCNif[self.dc_str].value
                except KeyError:
                    raise TaxIdEsException(f"Dígito de control inválido: {self.dc_str}")
        else:
            dc = self._get_dc_dni_nie()
            if self.is_dc_num:
                self.is_dc_ok = dc.value == self.dc_num
            else:
                try:
                    self.is_dc_ok = dc.value == TaxIdEsDCDniNie[self.dc_str].value
                except KeyError:
                    raise TaxIdEsException(f"Dígito de control inválido: {self.dc_str}")

    def _get_dc_nif(self) -> TaxIdEsDCNif:
        """Calcula el dígito de control de un NIF de persona jurídica."""
        num_cif = self._tax_code[1:8]
        # Suma A: número de las posiciones pares
        sum_a = sum(int(num_cif[pos]) for pos in range(1, len(num_cif), 2))
        # Suma B: número de las posiciones impares x 2 (suma de decenas y unidades)
        sum_b = 0
        for pos in range(0, len(num_cif), 2):
            dig_i = 2 * int(num_cif[pos])
            dig_iu = dig_i % 10
            dig_id = (dig_i - dig_iu) // 10
            sum_b += dig_iu + dig_id
        sum_c = sum_a + sum_b
        dig_e = sum_c % 10
        dig_d = 0 if dig_e == 0 else 10 - dig_e
        return TaxIdEsDCNif(dig_d)

    def _get_dc_dni_nie(self) -> TaxIdEsDCDniNie:
        """Calcula el dígito de control de un DNI o NIE."""
        if self._tax_code[0] > "9":  # Si es una letra entonces se trata de un NIE
            n_cif = ((ord(self._tax_code[0]) - ord("X")) * 10 ** 7
                     + int(self._tax_code[1:8]))
        else:
            n_cif = int(self._tax_code[0:8])
        return TaxIdEsDCDniNie(n_cif % 23)

    def get_ccaa(self) -> str:
        """Devuelve el nombre de la provincia representada por los dos
        primeros dígitos de un NIF de persona jurídica (no significativo ya)."""
        return ""
