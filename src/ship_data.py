import re
import locale

class Ship_Data():
	def __init__(self, simple_ups_data_list, detail_ups_data_list):
		# print(simple_ups_data_list)
		# print(detail_ups_data_list)

		locale.setlocale(locale.LC_ALL, 'English_United States.1252')

		for simple_data in simple_ups_data_list:
			charge_value = simple_data["billed_charge"]
			charge_re = re.compile(r"\d+\.\d+")
			charge = charge_re.search(charge_value)
			# print(locale.currency(charge_value, grouping=True))
			print(charge_value, charge[0])