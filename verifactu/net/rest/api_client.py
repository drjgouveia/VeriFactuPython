"""REST API client for VeriFactu."""

import json
import requests
from typing import Optional, Dict, Any, List
from dataclasses import asdict

from verifactu.config.settings import Settings
from verifactu.net.rest.api import Api
from verifactu.business.invoice import Invoice
from verifactu.business.operations.invoice_query import InvoiceQuery
from verifactu.net.rest.list.filter_set import FilterSet
from verifactu.business.flow_control.invoice_batch import InvoicesBatch


class ApiClient:
    """REST API client for Irene Solutions VeriFactu API."""
    
    def __init__(self):
        self._settings = Settings.current
    
    @property
    def api(self) -> Api:
        return self._settings.api
    
    def _post(self, input_obj: Any, url: str) -> Dict[str, Any]:
        """Make a POST request to the API."""
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'data': json.dumps(input_obj, default=lambda o: o.__dict__ if hasattr(o, '__dict__') else str(o)),
            'service_key': self.api.service_key,
        }
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def create(self, invoice: Invoice) -> Dict[str, Any]:
        """Create an invoice via API."""
        return self._post(invoice, self.api.end_point_create)
    
    def cancel(self, invoice: Invoice) -> Dict[str, Any]:
        """Cancel an invoice via API."""
        return self._post(invoice, self.api.end_point_cancel)
    
    def get_qr(self, invoice: Invoice) -> Dict[str, Any]:
        """Get QR code for invoice via API."""
        return self._post(invoice, self.api.end_point_get_qr_code)
    
    def get_sellers(self) -> Dict[str, Any]:
        """Get sellers via API."""
        dummy_invoice = Invoice("", None, "")
        return self._post(dummy_invoice, self.api.end_point_get_sellers)
    
    def validate_nif(self, invoice: Invoice) -> Dict[str, Any]:
        """Validate NIF via API."""
        return self._post(invoice, self.api.end_point_validate_nif)
    
    def get_aeat_invoices(self, invoice: Invoice) -> Dict[str, Any]:
        """Get AEAT invoices via API."""
        return self._post(invoice, self.api.end_point_get_aeat_invoices)
    
    def get_filtered_list(self, filter_set: FilterSet) -> Dict[str, Any]:
        """Get filtered list via API."""
        return self._post(filter_set, self.api.end_point_get_filtered_list)
    
    def create_batch(self, invoices_batch: InvoicesBatch) -> Dict[str, Any]:
        """Create batch of invoices via API."""
        return self._post(invoices_batch, self.api.end_point_create_batch)
    
    def validate_nifs(self, invoices_batch: InvoicesBatch) -> Dict[str, Any]:
        """Validate multiple NIFs via API."""
        return self._post(invoices_batch, self.api.end_point_validate_nifs)
    
    def validate_vies_vat_number(self, invoice: Invoice) -> Dict[str, Any]:
        """Validate VIES VAT number via API."""
        return self._post(invoice, self.api.end_point_validate_vies_vat_number)