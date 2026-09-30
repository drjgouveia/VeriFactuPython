VeriFactu (Python)
==================

[![License](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://github.com/mdiago/VeriFactu/blob/main/LICENSE)

Port a Python 3.14 de la librería .NET [VeriFactu](https://github.com/mdiago/VeriFactu):
generación, conservación y envío de registros de facturación al sistema
**VERI*FACTU** de la AEAT (Agencia Española de Administración Tributaria).

> La compatibilidad con la librería .NET se verifica con tests: el cálculo de
> la huella (`hash`) de un registro de alta reproduce exactamente el ejemplo
> del README original
> (`4EECCE4DD48C0539665385D61D451BA921B7160CA6FEF46CD3C2E2BC5C778E14`).

Instalación
-----------

```bash
git clone <este repositorio>
cd VeriFactuPython
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

Dependencias opcionales:

```bash
pip install requests cryptography   # comunicaciones SOAP con la AEAT
pip install qrcode pillow           # generación de códigos QR
```

Quickstart
----------

### Configuración del certificado

La configuración del sistema es accesible mediante la propiedad estática
`Settings.current` (equivalente a `Settings.Current` en C#):

```python
from verifactu import Settings

# Valores actuales de configuración de certificado
print(Settings.current.certificate_path)
print(Settings.current.certificate_password)

# Establezco nuevos valores (carga desde fichero .pfx / .p12)
Settings.current.certificate_path = "/ruta/CERTIFICADO.pfx"
Settings.current.certificate_password = "pass certificado"

# Guardo los cambios
Settings.save()
```

### Envío de facturas

```python
from datetime import datetime
from decimal import Decimal

from verifactu import Invoice, TaxItem, TipoFactura, InvoiceEntry

# Creamos una instancia de la clase factura
invoice = Invoice("GIT-EJ-0002", datetime(2024, 11, 15), "B72877814")
invoice.invoice_type = TipoFactura.F1
invoice.seller_name = "WEFINZ GANDIA SL"
invoice.buyer_id = "B44531218"
invoice.buyer_name = "WEFINZ SOLUTIONS SL"
invoice.text = "PRESTACION SERVICIOS DESARROLLO SOFTWARE"
invoice.tax_items = [
    TaxItem(tax_rate=Decimal("4"),  tax_base=Decimal("10"),  tax_amount=Decimal("0.4")),
    TaxItem(tax_rate=Decimal("21"), tax_base=Decimal("100"), tax_amount=Decimal("21")),
]

# Creamos la entrada de la factura (valida las reglas de negocio)
invoice_entry = InvoiceEntry(invoice)

# Guardamos la factura: contabiliza en la cadena de bloques y envía a la AEAT
invoice_entry.save()

# Consultamos el estado
print(f"Respuesta de la AEAT:\n{invoice_entry.status}")

if invoice_entry.status == "Correcto":
    print(f"CSV: {invoice_entry.csv}")
else:
    print(f"{invoice_entry.error_code}: {invoice_entry.error_description}")

print(f"Respuesta de la AEAT:\n{invoice_entry.response}")
```

### Anulación de facturas

```python
from verifactu import Invoice, InvoiceCancellation

invoice = Invoice("GIT-EJ-0002", datetime(2024, 11, 15), "B72877814")
invoice.seller_name = "WEFINZ GANDIA SL"

invoice_cancellation = InvoiceCancellation(invoice)
invoice_cancellation.save()

print(f"Respuesta de la AEAT:\n{invoice_cancellation.response}")
```

### Generación de la huella (hash) de un registro de alta

```python
from verifactu import Invoice, TaxItem, RegistroAlta, Encadenamiento, RegistroAnterior

invoice = Invoice("GITHUB-EJ-003", datetime(2024, 11, 4), "B72877814")
invoice.buyer_id = "B44531218"
invoice.buyer_name = "WEFINZ SOLUTIONS SL"
invoice.tax_items = [
    TaxItem(tax_rate=Decimal("4"),  tax_base=Decimal("10"),  tax_amount=Decimal("0.4")),
    TaxItem(tax_rate=Decimal("21"), tax_base=Decimal("100"), tax_amount=Decimal("21")),
]

registro = invoice.get_registro_alta()

# Forzamos el valor de FechaHoraHusoGenRegistro para que coincida con el
# último envío a la AEAT
registro.fecha_hora_huso_gen_registro = "2024-11-04T12:36:39+01:00"

# Establecemos el valor del encadenamiento anterior
registro.encadenamiento = Encadenamiento()
registro.encadenamiento.registro_anterior = RegistroAnterior()
registro.encadenamiento.registro_anterior.huella = (
    "8C8DCEFB120522E0C71BC19902F44D5334FF6C98E74F0E3AC1D1E5A30C2EA836")

hash_value = registro.get_hash_output()
# 4EECCE4DD48C0539665385D61D451BA921B7160CA6FEF46CD3C2E2BC5C778E14
```

### URL de cotejo (QR)

```python
registro = invoice.get_registro_alta()
url_validacion = registro.get_url_validate()
# https://prewww2.aeat.es/wlpl/TIKE-CONT/ValidarQR?nif=B72877814&numserie=GITHUB-EJ-004&fecha=04-11-2024&importe=131.4

# Imagen QR (requiere qrcode + pillow)
qr_bytes = registro.get_validate_qr()
```

### Cadena de bloques

```python
from verifactu import Blockchain

blockchain = Blockchain.get(invoice.seller_id)
blockchain.add(registro)
```

### Control de flujo

La AEAT establece que la aplicación debe respetar los tiempos de espera
entre envíos (1.000 registros pendientes o el tiempo indicado en la
respuesta):

```python
from verifactu import InvoiceQueue, InvoiceEntry

queue = InvoiceQueue.active_invoice_queue()
queue.add(InvoiceEntry(invoice))   # los envíos se realizan de forma asíncrona

# Al finalizar la aplicación:
if queue.count == 0:
    InvoiceQueue.exit()
```

Estructura del paquete
----------------------

| Módulo | Descripción |
| ------ | ----------- |
| `verifactu.business` | Objetos de negocio: `Invoice`, `TaxItem`, `InvoiceEntry`... |
| `verifactu.business.operations` | Acciones de alta/anulación: validación, contabilización y envío. |
| `verifactu.business.flow_control` | Control de flujo de envíos a la AEAT. |
| `verifactu.business.validation` | Validaciones de negocio según las especificaciones AEAT. |
| `verifactu.xml` | Modelos XML y serializador (namespaces AEAT reales). |
| `verifactu.xml.soap` | Sobre SOAP. |
| `verifactu.blockchain` | Cadena de bloques de registros de facturación. |
| `verifactu.eventchain` | Cadena de eventos (modo NO VERI*FACTU). |
| `verifactu.config` | Configuración (`Settings`). |
| `verifactu.net` | Cliente SOAP (`Wsd`) y cliente REST (`ApiClient`). |
| `verifactu.qrcode` | Generación de códigos QR. |
| `verifactu.common` | Utilidades, log y excepciones. |

Equivalencias con la librería .NET
----------------------------------

| C# | Python |
| -- | ------ |
| `Settings.Current.X` | `Settings.current.x` |
| `new Invoice(id, date, seller)` | `Invoice(id, date, seller)` |
| `invoice.GetRegistroAlta()` | `invoice.get_registro_alta()` |
| `invoiceEntry.Save()` | `invoice_entry.save()` |
| `invoiceEntry.Status` | `invoice_entry.status` |
| `TipoFactura.F1` | `TipoFactura.F1` |
| `Blockchain.Get(seller)` | `Blockchain.get(seller)` |
| `InvoiceQueue.ActiveInvoiceQueue` | `InvoiceQueue.active_invoice_queue()` |

Ejecutar los tests
------------------

```bash
python -m unittest discover tests -v
```

Licencia
--------

GNU Affero General Public License v3.0 (mismo licenciamiento que la
librería original).
