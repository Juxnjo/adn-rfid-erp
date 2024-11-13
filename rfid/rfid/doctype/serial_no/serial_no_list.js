frappe.listview_settings['Serial No'] = {
    onload: function(me) {
		me.page.add_action_item('Print RFID', function() {
            const serial_no = me.get_checked_items();
            frappe.call({
                  method: "rfid.rfid.api.create_print_rfid_sn",
                  freeze: true,
                  args:{
                        Serial_no_list: serial_no
                  },
                  // callback: function (r) {
                  //       if (r.message) {
                  //             frappe.set_route("query-report", "BOQ Stock Report",
                  //             { boq: r.message});
                  //       }
                  // }
            });
		});
	},
}