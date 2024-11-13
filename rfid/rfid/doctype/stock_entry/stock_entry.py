import frappe
# import itertools
# import hashlib
from rfid.rfid.api import generate_unique_hex

def on_submit(doc,method=None):
    serials = frappe.db.get_list('Serial No',{'purchase_document_no':doc.name}, pluck='name')
    for serial in serials:
        # input_string = serial
        # # Calculate the SHA-256 hash of the input string
        # sha256_hash = hashlib.sha256(input_string.encode()).hexdigest()

        # # Ensure the output is up to 10 characters
        # output_length = min(len(sha256_hash), 10)
        # rfid_data = sha256_hash[:output_length]

        rfid_data = generate_unique_hex(12)
        frappe.db.set_value('Serial No',serial,'custom_barcode',rfid_data)
    frappe.db.commit()