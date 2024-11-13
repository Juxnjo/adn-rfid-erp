import frappe
import json
import itertools
import hashlib
from frappe.utils import (
	get_link_to_form
)
import secrets
from frappe.utils import now_datetime

@frappe.whitelist()
def create_print_rfid_se(doc):
    doc = json.loads(doc)
    
    serial_no_list = frappe.db.get_list('Serial No',{'purchase_document_no':doc.get('name')}, ['name','item_code','custom_barcode'])
    if serial_no_list:
        created_numbers = []
        for serial_no in serial_no_list:
            created_numbers.append(serial_no.get('name'))
            rfid_doc = frappe.new_doc('RFID Print Queue')
            rfid_doc.item_code = serial_no.get('item_code')
            rfid_doc.qty = 1
            rfid_doc.status = 'Pending'
            rfid_doc.rfid = serial_no.get('custom_barcode')
            rfid_doc.flags.ignore_permissions = 1
            rfid_doc.save()

        form_links = list(map(lambda d: get_link_to_form("Serial No", d), created_numbers))

        # Setting up tranlated title field for all cases
        singular_title = ("Added RFID in Print Queue")
        multiple_title = ("Added RFIDs in Print Queue")

        if len(form_links) == 1:
            frappe.msgprint(("Serial No {0} Added in RFID Print Queue").format(form_links[0]), singular_title)
        elif len(form_links) > 0:
            message = ("The following RFIDs were added: <br><br> {0}").format(
                get_items_html(form_links, 'RFID')
            )
            frappe.msgprint(message, multiple_title)

@frappe.whitelist()
def create_print_rfid_sn(Serial_no_list):
    doc = json.loads(Serial_no_list)
    
    if doc:
        created_numbers = []
        for item in doc:
            rfid_doc = frappe.new_doc('RFID Print Queue')
            created_numbers.append(item.get('name'))
            if 'asset_name' in list(item.keys()):
                rfid_doc.item_code = frappe.db.get_value('Asset',item.get('name'),'item_code')
            else:
                rfid_doc.item_code = item.get('item_code')
            rfid_doc.qty = 1
            rfid_doc.status = 'Pending'
            if 'asset_name' in list(item.keys()):
                rfid_data = frappe.db.get_value('Asset',item.get('name'),'custom_rfid')
            else:
                rfid_data = frappe.db.get_value('Serial No',item.get('name'),'custom_barcode')
            rfid_doc.rfid = rfid_data
            rfid_doc.flags.ignore_permissions = 1
            rfid_doc.save()
        
        form_links = list(map(lambda d: get_link_to_form("Serial No", d), created_numbers))

        # Setting up tranlated title field for all cases
        singular_title = ("Added RFID in Print Queue")
        multiple_title = ("Added RFIDs in Print Queue")

        if len(form_links) == 1:
            if 'asset_name' in list(doc[0].keys()):
                frappe.msgprint(("Asset {0} Added in RFID Print Queue").format(form_links[0]), singular_title)    
            else:
                frappe.msgprint(("Serial No {0} Added in RFID Print Queue").format(form_links[0]), singular_title)
        elif len(form_links) > 0:
            message = ("The following RFIDs were added: <br><br> {0}").format(
                get_items_html(form_links, 'RFID')
            )
            frappe.msgprint(message, multiple_title)

def get_items_html(serial_nos, item_code):
	body = ", ".join(serial_nos)
	return """<details><summary>
		<b>{0}:</b> {1} RFID Numbers <span class="caret"></span>
	</summary>
	<div class="small">{2}</div></details>
	""".format(
		item_code, len(serial_nos), body
	)

def generate_unique_hex(len):
    return secrets.token_hex(len)
    
@frappe.whitelist()
def create_se(**kwargs):
    body = json.loads(frappe.request.data)
    doc = frappe.new_doc('Stock Entry')
    doc.stock_entry_type = "Material Receipt"
    doc.to_warehouse = body.get("to_warehouse")
    for i in body.get("items"):
        doc.append("items",{"item_code": i.get("item_code"),"qty": i.get("qty"),"basic_rate": i.get("basic_rate")})
    doc.save(ignore_permissions=1)
    doc.submit()
    return doc
