frappe.ui.form.on('Stock Entry', {
    refresh: function(frm) {
        if(frm.doc.docstatus === 1){
            frm.add_custom_button(__('Print RFID'), function(){
                // frm.trigger("print_rfid");
                frappe.call({
					method: "rfid.rfid.api.create_print_rfid_se",
					args: {
						doc: frm.doc,
					}
				});
    });
    }
  },
  print_rfid: function(frm) {
    const print_settings = frappe.model.get_doc(":Print Settings", "Print Settings");
   
    var d = new frappe.ui.Dialog({
        title: __('Print Documents'),
        fields: [
            {
                label: __("Print Size"),
                fieldname: "page_size",
                fieldtype: "Select",
                options: frappe.meta.get_print_sizes(),
                default: print_settings.pdf_page_size,
            },
            
            {
                fieldtype: "Float",
                label: __("Page Height (in mm)"),
                fieldname: "page_height",
                depends_on: 'eval:doc.page_size == "Custom"',
                default: print_settings.pdf_page_height,
            },
            {
                fieldtype: "Float",
                label: __("Page Width (in mm)"),
                fieldname: "page_width",
                depends_on: 'eval:doc.page_size == "Custom"',
                default: print_settings.pdf_page_width,
            },
        ],
        
    });
    d.set_primary_action(__("Print"), (args) => {
        if (!args) return;

        let globalVariable1;

        async function fetchData() {
        const serials_no = await frappe.db.get_list("Serial No", {
            filters: { "purchase_document_no": frm.doc.name },
            fields: ["name"]
        });
        const serials_name = serials_no.map(item => item.name);

        // Assign the resolved result to the global variable
        globalVariable1 = serials_name;
        }

        fetchData()
        .then(() => {
        
        const with_letterhead = 0;
        const print_format = 'RFID';
        const json_string = JSON.stringify(globalVariable1);
        const letterhead = "No Letterhead"

        let pdf_options;
        if (args.page_size === "Custom") {
            if (args.page_height === 0 || args.page_width === 0) {
                frappe.throw(__("Page height and width cannot be zero"));
            }
            pdf_options = JSON.stringify({
                "page-height": args.page_height,
                "page-width": args.page_width,
            });
        } else {
            pdf_options = JSON.stringify({ "page-size": args.page_size });
        }

        const w = window.open(
            "/api/method/frappe.utils.print_format.download_multi_pdf?" +
                "doctype=" +
                encodeURIComponent("Serial No") +
                "&name=" +
                encodeURIComponent(json_string) +
                "&format=" +
                encodeURIComponent(print_format) +
                "&no_letterhead=" +
                (with_letterhead ? "0" : "1") +
                "&letterhead=" +
                encodeURIComponent(letterhead) +
                "&options=" +
                encodeURIComponent(pdf_options)
        );

        if (!w) {
            frappe.msgprint(__("Please enable pop-ups"));
            return;
        }
    });
    });

    d.show();
    }
})
