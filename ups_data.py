import copy, re
import math

class UPS_Data():
	# self.data is propagated in __init__ by match_and_converge
	# It has format [{k: prop, detail: [ [{}]. [{}]] }, {etc }]
	service_level_index = {}
	charge_type_index = {}
	charge_symbol_index = {}

	def __init__(self, tracking_num, simple_data_list, detail_data_list):
		self.tracking_number = tracking_num
		self.data = self.match_and_converge(simple_data_list, detail_data_list)
		# print(self.tracking_number, self.data)
		# print(simple_data_list, detail_data_list)
		# print(self.tracking_number, self.data)
		try:
			self.date = self.data[0]["Pickup Date"]
		except IndexError as e:
			print(e)
			print("TRACKING NUM " + self.tracking_number)
			print("SIMPLE DATA LIST" + str(simple_data_list))
			print("DETAIL DATA LIST" + str(detail_data_list))
			print("SELF.DATA " + str(self.data))

	def match_and_converge(self, simple_data_list, detail_data_super_list):
		data_list = []

		for simple_data in simple_data_list:
			charge = simple_data["Billed Charge"]
			charge_re = re.compile(r"\d+\.\d+")
			t = charge_re.search(charge)
			if charge[0] != "-":
				conv_charge = float(t[0])
			else:
				conv_charge = -float(t[0])
			# print(charge, conv_charge)
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
		return str(self.data)

	def input_service_level_index(self):
	# Takes service level from ups_simple and fills in any
	# that is not there yet.
		for d in self.data:
			service_level = d["Service Level"]
			if service_level not in self.service_level_index:
				self.service_level_index[service_level] = None

	def input_charge_type_index(self):
	# Takes charge type from ups_detail and fills in any
	# that is not there yet.
		for d in self.data:
			for d_detail in d["detail"]:
				charge_type = d_detail["Charge Type"]
				if charge_type not in self.charge_type_index:
					self.charge_type_index[charge_type] = None

	def input_charge_symbol_index(self):
	# Takes charge symbol from ups_detail and fills in any
	# that is not there yet.
		for d in self.data:
			for d_detail in d["detail"]:
				charge_symbol = d_detail["Charge Symbol"]
				if charge_symbol not in self.charge_symbol_index:
					self.charge_symbol_index[charge_symbol] = None

	def get_num_service_level(self):
		return len(self.data)

	def get_simple_datalist_str(self):
	# Gets the simple ups data and outputs it into a 
	# list containing strings.
		simple_list = []

		for data_obj in self.data:
			data_string = ""
			for k, v in data_obj.items():
				if k != 'detail':
					data_string += str(k) + " " + str(v) + " "
			simple_list.append(data_string)
		return simple_list

	def get_detail_datalist_str(self):
	# Gets the detail ups detail and outputs it into a 
	# list containing strings.
		detail_list = []

		for data_obj in self.data: 
			#self.data is a list containing data_obj's
			for data_detail_obj in data_obj["detail"]:
				detail_list.append(str(data_detail_obj))

		return detail_list

	def get_rate(self):
		rate = 0
		for data_obj in self.data:
			rate += data_obj["Billed Charge"]
		retun rate