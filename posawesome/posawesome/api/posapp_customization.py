import frappe

@frappe.whitelist()
def get_available_credit(customer = None):
    total_credit = []
    
    outstanding_invoices = frappe.get_all("Sales Invoice", {
        "outstanding_amount": ["<", 0],
        "docstatus": 1,
        "customer": customer
    }, ["name", "outstanding_amount"])
    
    for row in outstanding_invoices:
        outstanding_amount = -(row.outstanding_amount)
        row = {
            "type": "Invoice",
            "credit_origin": row.name,
            "total_credit": outstanding_amount,
            "credit_to_redeem": 0    
        }
        
        total_credit.append(row)
    
    advances = frappe.get_all("Payment Entry", {
        "unallocated_amount": [">", 0],
        "party_type": "Customer",
        "party": customer,
    }, ["name", "unallocated_amount"])
   
    for row in advances:
        row = {
            "type": "Advance",
            "credit_origin": row.name,
            "total_credit": row.unallocated_amount,
            "credit_to_redeem": 0    
        }
        
        total_credit.append(row)
     
    return total_credit