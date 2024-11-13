// Copyright (c) 2023, RFID and contributors
// For license information, please see license.txt

frappe.ui.form.on('RFID Print Queue',
	"onload", function(frm) {
		frm.set_query("item_code", function() {
			return {
				"filters": {
					"has_variants" : 0
				}
			};
		});
});
