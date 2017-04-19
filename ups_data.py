import copy, re
import math

class UPS_Data():
	# This is for the ups_simple data
	service_level_index = {}
	charge_type_index = {}
	charge_symbol_index = {}



	def __init__(self, tracking_num, simple_data_list, detail_data_list):
		self.tracking_number = tracking_num
		self.data = self.match_and_converge(simple_data_list, detail_data_list)
		print(simple_data_list, detail_data_list)
		print(self.tracking_number, self.data)
		self.date = self.data[0]["Pickup Date"]

	def match_and_converge(self, simple_data_list, detail_data_super_list):
		data_list = []
		for simple_data in simple_data_list:
			charge = simple_data["Billed Charge"]
			# print(charge)
			charge_re = re.compile(r"\d+\.\d+")
			t = charge_re.search(charge)
			if charge[0] != "(":
				conv_charge = float(t[0])
			else:
				conv_charge = -float(t[0])
			simple_data["Billed Charge"] = conv_charge

			for detail_data_list in detail_data_super_list:
				total_charge = 0

				for detail_data in detail_data_list:
					total_charge += float(detail_data["Billed Charge"])
					# print(conv_charge, total_charge, conv_charge == total_charge)

				# Match simple & detail data by total billed charge
				if math.isclose(conv_charge, total_charge, abs_tol=0.001):
					simple_data["detail"] = copy.deepcopy(detail_data_list)
					del(detail_data_list)
					data_list.append(simple_data)
					break

		return data_list

	def __str__(self):
		return self.date + " " + self.tracking_number + " " + str(self.data)

	def talk(self):
		print(self.tracking_number + " " + self.date)

	def input_service_level_index(self):
		for d in self.data:
			service_level = d["Service Level"]
			if service_level not in self.service_level_index:
				self.service_level_index[service_level] = None

	def input_charge_type_index(self):
		for d in self.data:
			for d_detail in d["detail"]:
				charge_type = d_detail["Charge Type"]
				if charge_type not in self.charge_type_index:
					self.charge_type_index[charge_type] = None

	def input_charge_symbol_index(self):
		for d in self.data:
			for d_detail in d["detail"]:
				charge_symbol = d_detail["Charge Symbol"]
				if charge_symbol not in self.charge_symbol_index:
					self.charge_symbol_index[charge_symbol] = None

	def get_num_service_level(self):
		return len(self.data)