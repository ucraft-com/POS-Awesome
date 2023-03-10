import frappe


def execute():
    pass
    items_list={
    "VEGETABLE SAUCE":"VEGETABLE SAUCE",
    "COMPLETE CHICKENMAN FRIED RICE":"COMPLETE CHICKENMAN FRIED RICE",
    "COMPLETE CHICKENMAN JOLLOF RICE":"COMPLETE CHICKENMAN JOLLOF RICE",
    "COMPLETE FRIEDRICE":"COMPLETE FRIEDRICE",
    "COMPLETE JOLLOF":"COMPLETE JOLLOF",
    "Cut Beef Cubes":"Cut Beef Cubes",
    "Cooked Rice":"Cooked Rice",
    "Cooked Jollof Sauce":"Cooked Jollof Sauce",
    "Cooked Jollof":"Cooked Jollof",
    "Cooked Green Chilli":"Cooked Green Chilli",
    "Cooked Drumsticks":"Cooked Drumsticks",
    "Cooked Chicken Breast":"Cooked Chicken Breast",
    "Cooked Beef Cubes":"Cooked Beef Cubes",
    "Barbeque sauce":"Barbeque sauce",
    "Tossed Beef Cubes":"Tossed Beef Cubes",
    "Tomato Pulp":"Tomato Pulp",
    "Sugar Mixture":"Sugar Mixture",
    "Spring onions":"Spring onions",
    "Squid Tubes":"Squid Tubes",
    "Yeast":"Yeast",
    "Tuna":"Tuna",
    "Tomatoes":"Tomatoes",
    "Sugar":"Sugar",
    "Spaghetti":"Spaghetti",
    "Shrimps":"Shrimps",
    "Salt":"Salt",
    "RED PEPPER":"RED PEPPER",
    "Red Chilli":"Red Chilli",
    "RAW RICE (LELE)":"RAW RICE (LELE)",
    "Raw Rice":"Raw Rice",
    "Raw Pork":"Raw Pork",
    "Raw Green Chilli":"Raw Green Chilli",
    "Raw Chicken Breast":"Raw Chicken Breast",
    "Raw Beef Cubes":"Raw Beef Cubes",
    "Raw beef":"Raw beef",
    "Prepared Beef":"Prepared Beef",
    "Powdered Fish":"Powdered Fish",
    "Pizza Sauce":"Pizza Sauce",
    "Peporoni":"Peporoni",
    "Cooked Chicken Wings":"Cooked Chicken Wings",
    "DOUGH":"DOUGH",
    "Onion":"Onion",
    "Mushroom":"Mushroom",
    "Mortadella":"Mortadella",
    "Margarine":"Margarine",
    "Maggi":"Maggi",
    "Kelewele":"Kelewele",
    "Ham":"Ham",
    "Cheese":"Cheese",
    "Gizzard":"Gizzard",
    "Ginger":"Ginger",
    "Garlic":"Garlic",
    "Flour":"Flour",
    "Carrot":"Carrot",
    "Brisket":"Brisket",
    "Cabbage":"Cabbage",
    "Ketch up":"Ketch up",
    "Martin Spice":"Martin Spice",
    "Peeled Shrimps":"Peeled Shrimps",
    "Oyster Sauce":"Oyster Sauce",
    "Green Pepper":"Green Pepper",
    "Goat Meat":"Goat Meat",
    "Fish Fillet":"Fish Fillet",
    "Chicken Maggie":"Chicken Maggie",
    "Chicken Fillet":"Chicken Fillet",
    "Cheddar Hamburger":"Cheddar Hamburger",
    "CHEDDAR CHEESE":"CHEDDAR CHEESE",
    "Butter flavour":"Butter flavour",
    "beef fillet":"beef fillet",
    }

    keys = list(items_list.keys())
    for row in keys:
        if frappe.db.exists("Material Request Item", {"item_code": row}):
            mtr_list=frappe.db.get_list('Material Request Item',filters={'item_code': row},fields=['name','parent'])
            for mtr in mtr_list:
                doc = frappe.get_doc('Material Request Item', mtr.name)
                if doc.item_code in items_list:
                    doc.stock_uom='kg'
                    doc.uom='kg'
                    doc.db_set('stock_uom','kg')
                    doc.db_set('uom','kg')
        frappe.db.commit()