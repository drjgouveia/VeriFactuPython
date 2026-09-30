"""Espacios de nombre de VERI*FACTU."""

NamespacePrefix = "https://www2.agenciatributaria.gob.es/static_files/common/internet/dep/aplicaciones/es/aeat/tike/cont/ws/"

NamespaceSF = NamespacePrefix + "SuministroInformacion.xsd"
NamespaceSFLR = NamespacePrefix + "SuministroLR.xsd"
NamespaceTikR = NamespacePrefix + "RespuestaSuministro.xsd"
NamespaceCon = NamespacePrefix + "ConsultaLR.xsd"
NamespaceTikLRRC = NamespacePrefix + "RespuestaConsultaLR.xsd"
NamespaceSf = NamespacePrefix + "EventosSIF.xsd"
NamespaceDs = "http://www.w3.org/2000/09/xmldsig#"
NamespaceXades = "http://uri.etsi.org/01903/v1.3.2#"
NamespaceVNifV2Ent = "http://www2.agenciatributaria.gob.es/static_files/common/internet/dep/aplicaciones/es/aeat/burt/jdit/ws/VNifV2Ent.xsd"
NamespaceVNifV2Sal = "http://www2.agenciatributaria.gob.es/static_files/common/internet/dep/aplicaciones/es/aeat/burt/jdit/ws/VNifV2Sal.xsd"
NamespaceSoap = "http://schemas.xmlsoap.org/soap/envelope/"

Items = {
    "soapenv": NamespaceSoap,
    "sum": NamespaceSFLR,
    "sum1": NamespaceSF,
    "con": NamespaceCon,
}

EventItems = {
    "sf": NamespaceSf,
    "ds": NamespaceDs,
}

NifItems = {
    "soapenv": NamespaceSoap,
    "VNifV2Ent": NamespaceVNifV2Ent,
    "VNifV2Sal": NamespaceVNifV2Sal,
}
