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

	def convert_charge_string_to_float(self, charge_string):
		"""
		:param charge_string: string from CSV ups simple file (ex. -$5.55)
		:return: float of the charge_value
		"""
		charge = 0.00
		# charge_re = re.compile(r"(\-*).*(\d+\.\d+)")
		bill_charge_re = re.compile(r"\d+\.\d+")
		charge_re_result = (bill_charge_re.search(charge_string))[0]

		if charge_string[0] == '-':
		# Negative charge values have a negative sign (eg "-4.24")
			charge = -float(charge_re_result)
		else:
			charge = float(charge_re_result)

		return charge