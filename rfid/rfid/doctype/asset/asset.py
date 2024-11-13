import frappe
from rfid.rfid.api import generate_unique_hex

def before_save(doc,method=None):
    item_barcode = frappe.db.get_value('Item',doc.item_code,'custom_barcode')
    if item_barcode:
        doc.custom_rfid =  generate_unique_hex(12)
        