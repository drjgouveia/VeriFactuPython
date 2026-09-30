"""API configuration for VeriFactu REST API."""

from typing import Optional


class Api:
    """API REST configuration for Irene Solutions VeriFactu."""
    
    def __init__(self):
        self.end_point_create: str = ""
        self.end_point_cancel: str = ""
        self.end_point_get_qr_code: str = ""
        self.end_point_get_sellers: str = ""
        self.end_point_get_records: str = ""
        self.end_point_validate_nif: str = ""
        self.end_point_get_aeat_invoices: str = ""
        self.end_point_get_filtered_list: str = ""
        self.end_point_create_batch: str = ""
        self.end_point_validate_nifs: str = ""
        self.end_point_validate_vies_vat_number: str = ""
        self.service_key: str = ""