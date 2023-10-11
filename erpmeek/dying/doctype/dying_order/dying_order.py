# Copyright (c) 2023, Mehedi Abdullah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DyingOrder(Document):
    def before_save(self):
        total = 0
        for yarn in self.yarn_details:
            total += yarn.quantity

        # Inserting dying order in Yarn Status doctypes automatically
        yarn_status = frappe.new_doc('Yarn Status')
        yarn_status.style = self.style
        yarn_status.buyer = self.buyer
        yarn_status.order_quantity = self.quantity
        yarn_status.yarn_quantity = total
        yarn_status.insert()

        # Automatically fill the child table "yarn_details" in Yarn Status
        for yarn in self.yarn_details:
            yarn_status.append('yarn_details', {
                'color': yarn.color,
                'pantone_reference': yarn.pantone_reference,
				'shade': yarn.shade,
                'batch_number': yarn.batch_number,
                'quantity': yarn.quantity,
                'remarks': yarn.remarks,
            })
        yarn_status.save()  # Save the Yarn Status document with filled yarn_details

		# Inserting dying order in Yarn Status doctypes automatically
        yarn_receive = frappe.new_doc('Yarn Receive')
        yarn_receive.style = self.style
        yarn_receive.buyer = self.buyer
        yarn_receive.yarn_composition = self.yarn_composition
        yarn_receive.yarn_quantity = total
        yarn_receive.insert()

        # Automatically fill the child table "yarn_details" in Yarn Status
        for yarn in self.yarn_details:
            yarn_receive.append('yarn_details', {
                'color': yarn.color,
                'pantone_reference': yarn.pantone_reference,
				'shade': yarn.shade,
                'batch_number': yarn.batch_number,
                'quantity': 0,
                'remarks': yarn.remarks,
            })
        yarn_receive.save()
        

		# Inserting dying order in Yarn Status doctypes automatically
        yarn_distribute = frappe.new_doc('Yarn Distribute')
        yarn_distribute.distribute_style = self.style
        yarn_distribute.buyer = self.buyer
        yarn_distribute.yarn_composition = self.yarn_composition
        yarn_distribute.yarn_quantity = total
        yarn_distribute.insert()

        # Automatically fill the child table "yarn_details" in Yarn Distribute
        for yarn in self.yarn_details:
            yarn_distribute.append('yarn_details', {
                'color': yarn.color,
                'pantone_reference': yarn.pantone_reference,
				'shade': yarn.shade,
                'batch_number': yarn.batch_number,
                'quantity': 0,
                'remarks': yarn.remarks,
            })
        yarn_distribute.save()
        
        print(total)
