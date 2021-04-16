# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "posawesome"
app_title = "POS Awesome"
app_publisher = "Youssef Restom"
app_description = "POS Awesome"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "youssef@totrox.com"
app_license = "GPLv3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/posawesome/css/posawesome.css"
# app_include_js = "/assets/posawesome/js/posawesome.js"
app_include_js = [
    "/assets/posawesome/node_modules/vuetify/dist/vuetify.js",
    "/assets/js/toConsole.min.js",
    "/assets/js/posapp.min.js",
]

# include js, css files in header of web template
# web_include_css = "/assets/posawesome/css/posawesome.css"
# web_include_js = "/assets/posawesome/js/posawesome.js"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"POS Profile": "posawesome/api/pos_profile.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "posawesome.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "posawesome.install.before_install"
# after_install = "posawesome.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "posawesome.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"posawesome.tasks.all"
# 	],
# 	"daily": [
# 		"posawesome.tasks.daily"
# 	],
# 	"hourly": [
# 		"posawesome.tasks.hourly"
# 	],
# 	"weekly": [
# 		"posawesome.tasks.weekly"
# 	]
# 	"monthly": [
# 		"posawesome.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "posawesome.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "posawesome.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "posawesome.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                (
                    "Sales Invoice-posa_pos_opening_shift",
                    "Item Barcode-posa_uom",
                    "POS Profile-posa_pos_awesome_settings",
                    "POS Profile-posa_allow_delete",
                    "POS Profile-posa_allow_user_to_edit_rate",
                    "POS Profile-posa_allow_user_to_edit_additional_discount",
                    "POS Profile-posa_allow_user_to_edit_item_discount",
                    "POS Profile-posa_display_items_in_stock",
                    "POS Profile-posa_allow_submissions_in_background_job",
                    "POS Profile-posa_allow_partial_payment",
                    "POS Profile-posa_allow_credit_sale",
                    "POS Profile-posa_pos_awesome_advance_settings",
                    "Batch-posa_btach_price",
                    "POS Profile-posa_max_discount_allowed",
                    "POS Profile-posa_allow_return",
                    "POS Profile-posa_col_1",
                    "POS Profile-posa_scale_barcode_start",
                    "Sales Invoice-posa_is_printed",
                    "POS Profile-posa_local_storage",
                    "POS Profile-posa_cash_mode_of_payment",
                    "POS Profile-use_customer_credit",
                    "POS Profile-use_cashback",
                    "POS Profile-posa_hide_closing_shift",
                ),
            ]
        ],
    },
    {
        "doctype": "Property Setter",
        "filters": [["name", "in", ("Sales Invoice-posa_pos_opening_shift-no_copy")]],
    },
]
