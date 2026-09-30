"""ValidatorSistemaInformatico - Validaciones del bloque SistemaInformatico (0.0.2)."""

from typing import List


class ValidatorSistemaInformatico:
    """Valida los datos de SistemaInformatico."""

    @staticmethod
    def get_errors(sistema_informatico) -> List[str]:
        """Ejecuta las validaciones y devuelve una lista con los errores."""
        from verifactu.config.settings import Settings
        from verifactu.xml.factu.id_type import IDType

        result = []

        if sistema_informatico is None:
            result.append(
                "[0.0.2-0.1] Error en el bloque SistemaInformatico:"
                " El bloque no puede ser nulo.")
            return result

        si = sistema_informatico

        if getattr(si, "nombre_razon_representante", None) is not None \
                or getattr(si, "nif_representante", None) is not None:
            result.append(
                f"[0.0.2-0.2] Error en el bloque SistemaInformatico ({si}):"
                " Los datos de interlocutor 'NombreRazonRepresentante' y"
                " 'NIFRepresentante' no pueden contener valor.")

        if si.nif and getattr(si, "ido_otro", None) is not None:
            result.append(
                f"[0.0.2-0.3] Error en el bloque SistemaInformatico ({si}):"
                " Si se cumplimenta NIF, no deberá existir la agrupación IDOtro y viceversa")

        if not si.nif and getattr(si, "ido_otro", None) is None:
            result.append(
                f"[0.0.2-0.4] Error en el bloque SistemaInformatico ({si}):"
                " Es obligatorio que se cumplimente NIF o IDOtro.")

        if not si.id_sistema_informatico:
            result.append(
                f"[0.0.2-0.5] Error en el bloque SistemaInformatico ({si}):"
                " Falta informar campo obligatorio IdSistemaInformatico.")

        if si.id_sistema_informatico and len(si.id_sistema_informatico) > 2:
            result.append(
                f"[0.0.2-0.6] Error en el bloque SistemaInformatico ({si}):"
                " El campo obligatorio IdSistemaInformatico tiene una longitud"
                " máxima de 2 caracteres.")

        id_otro = getattr(si, "ido_otro", None)
        if id_otro is not None:
            if id_otro.id_type != IDType.NIF_IVA:
                result.append(
                    f"[0.0.2-0.7] Error en el bloque SistemaInformatico ({si}):"
                    " Es obligatorio que se cumplimente CodigoPais con IDOtro.IDType != '02'.")

            if Settings.current.skip_vies_vat_number_validation:
                is_valid_vies = True
            else:
                from verifactu.business.validation.vies.vies_vat_number import ViesVatNumber
                is_valid_vies = ViesVatNumber.validate(id_otro.id)

            if id_otro.id_type == IDType.NIF_IVA and not is_valid_vies:
                result.append(
                    f"[0.0.2-0.8] Error en el bloque SistemaInformatico ({si}):"
                    f" Es obligatorio que IDOtro.ID = '{id_otro.id}' esté identificado.")

        # Validaciones de campos obligatorios
        if not si.nombre_razon:
            result.append(
                f"[0.0.2-0.9] Error en el bloque SistemaInformatico ({si}):"
                " Falta informar campo obligatorio NombreRazon.")

        if not si.nombre_sistema_informatico:
            result.append(
                f"[0.0.2-0.10] Error en el bloque SistemaInformatico ({si}):"
                " Falta informar campo obligatorio NombreSistemaInformatico.")

        if not si.version:
            result.append(
                f"[0.0.2-0.11] Error en el bloque SistemaInformatico ({si}):"
                " Falta informar campo obligatorio Version.")

        if not si.numero_instalacion:
            result.append(
                f"[0.0.2-0.12] Error en el bloque SistemaInformatico ({si}):"
                " Falta informar campo obligatorio NumeroInstalacion.")

        if si.tipo_uso_posible_solo_verifactu not in ("S", "N"):
            result.append(
                f"[0.0.2-0.13] Error en el bloque SistemaInformatico ({si}):"
                " El campo TipoUsoPosibleSoloVerifactu debe tener el valor 'S' o 'N'.")

        if si.tipo_uso_posible_multi_ot not in ("S", "N"):
            result.append(
                f"[0.0.2-0.14] Error en el bloque SistemaInformatico ({si}):"
                " El campo TipoUsoPosibleMultiOT debe tener el valor 'S' o 'N'.")

        if si.tipo_uso_posible_solo_verifactu == "N" \
                and si.tipo_uso_posible_multi_ot == "N":
            result.append(
                f"[0.0.2-0.15] Error en el bloque SistemaInformatico ({si}):"
                " No puede existir un sistema informático con TipoUsoPosibleSoloVerifactu"
                " y TipoUsoPosibleMultiOT a la vez en 'N'.")

        return result
