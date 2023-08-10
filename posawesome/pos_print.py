import os

from PyPDF2 import PdfWriter
from PyPDF2 import PdfFileWriter
from frappe.utils.file_manager import save_file
from frappe.utils import get_site_base_path, get_url, get_files_path, logger

import time
import frappe
from frappe import _
from frappe.core.doctype.access_log.access_log import make_access_log
from frappe.translate import print_language
from frappe.utils.pdf import get_pdf

no_cache = 1

base_template_path = "www/printview.html"
standard_format = "templates/print_formats/standard.html"

logger.set_log_level("DEBUG")
logger = frappe.logger("File url", allow_site=True, file_count=1)

from frappe.www.printview import validate_print_permission


@frappe.whitelist()
def pos_print(doctype, name, print_format=None, doc=None, no_letterhead=0):
    try:
        # Generate the file name with the current date
        file_name = f"Sales-Invoice-{name}-{frappe.utils.nowdate()}.pdf"

        # Generate the PDF file using PyPDF2 and save it to the site's public files directory
        output = PdfFileWriter()
        output = frappe.get_print(
            doctype, name, print_format, doc=doc, no_letterhead=no_letterhead, as_pdf=True, output=output
        )
        file_path = os.path.join(get_site_base_path(), get_files_path(), file_name)

        with open(file_name, "wb") as f:
            output.write(f)
            
        with open(file_name, "rb") as f:
            filedata = f.read()
        # Get the DocType and DocName for the File Manager entry (you can modify this as needed)
        dt = "Project"
        dn = f"Sales-Invoice-{name}-{frappe.utils.nowdate()}.pdf"

        # Save the PDF file in the File Manager
        file_url = save_file(file_name, filedata, dt, dn)

        # Delete the temporary PDF file from the local filesystem
        # os.remove(file_path)

        # Return the complete URL of the saved PDF file with the site name
        return file_url
    except OSError as e:
        if (
            "ContentNotFoundError" in e.message
            or "ContentOperationNotPermittedError" in e.message
            or "UnknownContentError" in e.message
            or "RemoteHostClosedError" in e.message
        ):
            frappe.throw(_("PDF generation failed"))
            
            
@frappe.whitelist()
def delete_file_by_name(file_name):
    try:
        # Find the File document by file name
        file = frappe.get_doc("File", {"file_name": file_name})
        if file:
            # Introduce a delay of 5 seconds before deleting the file
            time.sleep(120)  # Delay for 5 seconds

            # Delete the File document
            file.delete()

            return True
        else:
            return False
    except Exception as e:
        frappe.log_error(f"Error deleting file {file_name}: {str(e)}")
        return False  
    
@frappe.whitelist()
def get_doc(doctype, doc):
    doc = frappe.get_doc(doctype, doc)
    return doc.as_dict()         
