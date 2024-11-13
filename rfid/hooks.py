from . import __version__ as app_version

app_name = "rfid"
app_title = "Rfid"
app_publisher = "RFID"
app_description = "RFID"
app_email = "rfid@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/rfid/css/rfid.css"
# app_include_js = "/assets/rfid/js/rfid.js"

# include js, css files in header of web template
# web_include_css = "/assets/rfid/css/rfid.css"
# web_include_js = "/assets/rfid/js/rfid.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "rfid/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {
    "Stock Entry" : "rfid/doctype/stock_entry/stock_entry.js"
    }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
doctype_list_js = {
    "Serial No" : "rfid/doctype/serial_no/serial_no_list.js",
    "Asset" : "rfid/doctype/asset/asset_list.js",
    }
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "rfid.utils.jinja_methods",
#	"filters": "rfid.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "rfid.install.before_install"
# after_install = "rfid.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "rfid.uninstall.before_uninstall"
# after_uninstall = "rfid.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "rfid.utils.before_app_install"
# after_app_install = "rfid.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "rfid.utils.before_app_uninstall"
# after_app_uninstall = "rfid.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "rfid.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

doc_events = {
	"Item": {
		"before_save": "rfid.rfid.doctype.item.item.before_save"
	},
    "Stock Entry": {
		"on_submit": "rfid.rfid.doctype.stock_entry.stock_entry.on_submit"
	},
    "Asset": {
		"before_save": "rfid.rfid.doctype.asset.asset.before_save"
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"rfid.tasks.all"
#	],
#	"daily": [
#		"rfid.tasks.daily"
#	],
#	"hourly": [
#		"rfid.tasks.hourly"
#	],
#	"weekly": [
#		"rfid.tasks.weekly"
#	],
#	"monthly": [
#		"rfid.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "rfid.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "rfid.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "rfid.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["rfid.utils.before_request"]
# after_request = ["rfid.utils.after_request"]

# Job Events
# ----------
# before_job = ["rfid.utils.before_job"]
# after_job = ["rfid.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"rfid.auth.validate"
# ]

fixtures = [
    {"dt": "Custom Field", "filters": [
        [
            "name", "in", [
				"Asset-custom_rfid",
            ]
        ]
    ]}
]

# fixtures = [
#     {"dt": "Property Setter", "filters": [
#         [
#             "name", "in", [
# 				"Asset-main-field_order",
#             ]
#         ]
#     ]}
# ]