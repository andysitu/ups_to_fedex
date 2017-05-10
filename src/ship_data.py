import re

class Ship_Data():
	def __init__(self, simple_ups_data_list, detail_ups_data_list):
		# print(simple_ups_data_list)
		# print(detail_ups_data_list)

		self.match_simple_and_detail_ups(simple_ups_data_list, detail_ups_data_list)

	def match_simple_and_detail_ups(self, simple_ups_data_list, detail_ups_data_list):
		for simple_data in simple_ups_data_list:
			bill_charge_value = simple_data["billed_charge"]
			total_bill_charge = self.convert_charge_string_to_float(bill_charge_value)

			print(total_bill_charge)

