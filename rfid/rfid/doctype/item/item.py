import frappe
# import itertools
from rfid.rfid.api import generate_unique_hex

def before_save(doc,method=None):
    # ascii_list = list(itertools.chain(*map(lambda x: map(ord, x), doc.item_code)))
    # ascii_list_new = (''.join(map(str, ascii_list)))
    # doc.custom_barcode = ascii_list_new
    doc.custom_barcode = generate_unique_hex(6)
    if doc.serial_no_series == None:
        doc.serial_no_series = doc.item_code + '.######'
        