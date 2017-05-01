import fedex_rates
import re
import copy

class Fedex_Data():

	ups_service_level_index = {
		"Ground Commercial": "Ground",
		"Ground Hundredweight": False,
		"Ground Residential": "Home Delivery",
		"2nd Day Air Commercial": '2 Day',
		"2nd Day Air Residential": '2 Day',
		"UPS SurePost - 1 LB or Greater": 'Smart Post 1-70 lbs',
		"Worldwide Expedited": False,
		"Ground Undeliverable Return": False,
		# Probably Adjustments
		"Residential": False,
		# Probably Adjustments
		"Ground": False,
		# Usually adjustments
		"Residential Surcharge": False,
		#Adjustments
		"Expedited": False,
		"Standard Shipment": False,
		"Worldwide Express": False,
		"Worldwide Standard": False,
		"Worldwide Expedited Shipment": False,
		"Ground Return to Sender": False,

		'Shipment Residential Surcharge': False,
		"Standard to Canada": False,
		"Worldwide Saver": False,

		#Not sure about this
		"2nd Day Air": False,
	}

	ups_service_level_residential_index = {
	# If True, then it's residential
		"Ground Commercial": False,
		"Ground Hundredweight": False,
		"Ground Residential": True,
		"2nd Day Air Commercial": False,
		"2nd Day Air Residential": True,
	}

	fedex_charge_type_to_func_index = {
		"Ground": fedex_rates.calc_ground_commercial,
		"Fuel Surcharge": fedex_rates.calc_fuel_surcharge,
		"Additional Handling Surcharge": fedex_rates.calc_add_handling,
		"Home Delivery": fedex_rates.calc_ground_residential,
		"Residential Delivery Charge": fedex_rates.calc_residential_charge,
		"Delivery Area Surcharge": fedex_rates.calc_delivery_area_surcharge,
		"Delivery Signature": fedex_rates.calc_signature,
		'Smart Post 1-70 lbs': fedex_rates.calc_smart_post_1lb_plus,
		"Oversize Charge": fedex_rates.calc_oversize_charge,
		"Non-Machinable": fedex_rates.calc_nonmachinable_charge,
	}

	ups_to_fedex_charge_type_index = {
		"Ground Commercial": "Ground",
		# "Ground Hundredweight": "Ground",
		"Fuel Surcharge": "Fuel Surcharge",
		"Additional Handling": "Additional Handling Surcharge",
		"Ground Residential": "Home Delivery",
		"Residential Surcharge": "Residential Delivery Charge",
		"Delivery Area Surcharge": "Delivery Area Surcharge",
		"Delivery Area Surcharge - Extended": "Delivery Area Surcharge",
		"Delivery Confirmation Signature": "Delivery Signature",
		"UPS SurePost - 1 lb or Greater": 'Smart Post 1-70 lbs',
		"Delivery Confirmation Response": "Delivery Signature",
		"Large Package Surcharge": "Oversize Charge",
		"Non-machinable Charge": "Non-Machinable",
	}

	add_fuel_surcharge_index = {
	# Charge types with True are calculated in fuel surcharge percentage
		"Ground": True,
		"Home Delivery": True,
		"Residential Delivery Charge": True,
		"Delivery Area Surcharge": True,
		'Smart Post 1-70 lbs': True,
		"Oversize Charge": True,
		"Non-Machinable": False,
		"Delivery Signature": False,
		"Additional Handling Surcharge": False,
		#This is false since it's calculated after everything
		"Fuel Surcharge": False,
	}

	fedex_delivery_type = {
		'Priority Overnight': "Express",
		'Standard Overnight': "Express",
		'2 Day AM': "Express",
		'2 Day': "Express",
		'Express Saver (3 Day)': "Express",	
		'Ground': "Ground",
		'Home Delivery': "Ground",
		'Smart Post 1-16 oz': "Ground",
		'Smart Post 1-70 lbs': "Ground",
	}

	def __init__(self, date, ups_rate_data_list):
		self.date = date
		self.process_ups_data(date, ups_rate_data_list)

	def process_ups_data(self, date, ups_rate_data_list):
		data_dic = self.convert_first_ups_rate_data_to_fedex(date, ups_rate_data_list)
		self.weight = data_dic["Weight"]
		self.zone = data_dic["Zone"]
		self.date = data_dic["Date"]
		self.ups = [data_dic["ups"],]
		self.fedex = [data_dic["fedex"],]
		self.num_service = len(self.fedex)

	def get_first_dataset(self):
		return {
			"Weight": self.weight,
			"Zone": self.zone,
			"Date": self.date,
			"ups": copy.deepcopy(self.ups[0]),
			"fedex": copy.deepcopy(self.fedex[0]),
			"Number of Services": self.num_service,
		}


	def convert_first_ups_rate_data_to_fedex(self, date, ups_rate_data_list):
		data_dic = {}

		ups_rate_data = ups_rate_data_list[0]

		weight = int(ups_rate_data["simple"]["Weight"])
		zone = int(ups_rate_data["simple"]["Zone"])
		ups_service_level = ups_rate_data["simple"]["Service Level"]

		ups_detail_list = ups_rate_data['detail']
		# print(detail_list)
		# print(date)

		fedex_charge_list = []
		
		for ups_detail_dic in ups_detail_list:
			ups_charge_type = ups_detail_dic["Charge Type"]
			if ups_charge_type == 'Fuel Surcharge':
				continue
			billed_charge = ups_detail_dic["Billed Charge"]

			fedex_rate_dic = self.calc_fedex_rate(weight, zone, ups_charge_type, ups_service_level, ups_detail_list)
			fedex_charge_list.append(fedex_rate_dic)
			# if len(detail_list) > 2:
			# 	print(charge_type, billed_charge)

		#Calculate fuel surcharge at the end
		fedex_service_level = self.ups_service_level_index[ups_service_level]
		delivery_type = self.fedex_delivery_type[fedex_service_level]
		fuel_dic = fedex_rates.calc_fuel_surcharge(date, fedex_charge_list, delivery_type, self.add_fuel_surcharge_index)
		fedex_charge_list.append(fuel_dic)

		fedex_data = {}
		ups_data = {}
		ups_data["Charges List"] = ups_detail_list
		ups_data["Service Level"] = ups_service_level
		ups_total_rate = self.calc_total(ups_detail_list)
		ups_data["Total Charge"] = ups_total_rate
		fedex_data["Charges List"] = fedex_charge_list
		fedex_data["Service Level"] = fedex_service_level
		fedex_total_rate = self.calc_total(fedex_charge_list)
		fedex_data["Total Charge"] = fedex_total_rate

		data_dic["fedex"] = fedex_data
		data_dic["ups"] = ups_data
		data_dic["Date"] = date
		data_dic["Weight"] = weight
		data_dic["Zone"] = zone
		# print(data_dic)
		return data_dic


	def convert_ups_to_fedex_charge_type(self, ups_charge_type):
		fedex_charge_type = self.ups_to_fedex_charge_type_index[ups_charge_type]
		return fedex_charge_type

	def get_fedex_calc_function(self, ups_charge_type):
		fedex_charge_type = self.convert_ups_to_fedex_charge_type(ups_charge_type)
		return self.fedex_charge_type_to_func_index[fedex_charge_type]

	def calc_fedex_rate(self, weight, zone, ups_charge_type, ups_service_level, ups_detail_list):
	# Returns a dict containing 'Billed Charge', 'Charge Type', and 

		fedex_charge_type = self.convert_ups_to_fedex_charge_type(ups_charge_type)
		fedex_calc_funct = self.get_fedex_calc_function(ups_charge_type)
		fedex_service_level = self.ups_service_level_index[ups_service_level]
		extended_status = re.search(r"Extended", ups_charge_type)

		if fedex_charge_type == "Delivery Area Surcharge":
			residential_status = self.get_residential_status(ups_detail_list)
			rate = fedex_calc_funct(fedex_service_level, residential_status, extended_status)
		elif fedex_charge_type == "Fuel Surcharge":
		# It should be skipped beforehand, since it needs to be calculated at the end.
			pass
			# rate = fedex_calc_funct(date, ups_detail_list)
		else:
			rate = fedex_calc_funct(weight, zone)
		return {'Billed Charge': rate, 'Charge Type': fedex_charge_type, 'Service Level': fedex_service_level}

	def get_residential_status(self, ups_detail_list):
		# Gets residential status by checking "Resident" is in any of the
		# charge types through the ups detail list
		for ups_detail_dict in ups_detail_list:
			ups_charge_type = ups_detail_dict["Charge Type"]
			extended_status = re.search(r"Resident", ups_charge_type)
			if extended_status:
				return True
		return False

	def calc_total(self, data_list):
		total = 0.00
		for d in data_list:
			total += float(d["Billed Charge"])
		return total