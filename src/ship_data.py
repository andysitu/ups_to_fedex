import re

class Ship_Data():
	def __init__(self, simple_ups_data_list, detail_ups_data_list):
		# print(simple_ups_data_list)
		# print(detail_ups_data_list)

		self.match_simple_and_detail_ups(simple_ups_data_list, detail_ups_data_list)


	def match_simple_and_detail_ups(self, simple_ups_data_list, detail_ups_data_list):
		for simple_data in simple_ups_data_list:
			bill_charge_value = simple_data["billed_charge"]
			# charge_re = re.compile(r"(\-*).*(\d+\.\d+)")
			bill_charge_re = re.compile(r"\d+\.\d+")
			charge = ( bill_charge_re.search(bill_charge_value) )[0]

			if bill_charge_value[0] == '-':
				self.total_bill_charge = -float(charge)
			else:
				self.total_bill_charge = float(charge)
