import fedex_rates

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
		"Ground Return to Sender": False,
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
		"SmartPost - 1 lb or Greater": True,
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
		self.convert_first_ups_rate_data_to_fedex(date, ups_rate_data_list)

	def convert_first_ups_rate_data_to_fedex(self, date, ups_rate_data_list):
		ups_rate_data = ups_rate_data_list[0]

		weight = ups_rate_data["simple"]["Weight"]
		zone = ups_rate_data["simple"]["Zone"]
		service_level = ups_rate_data["simple"]["Service Level"]

		detail_list = ups_rate_data['detail']
		# print(detail_list)

		fedex_charge_dic = {}
		
		for detail_dic in detail_list:
			charge_type = detail_dic["Charge Type"]
			billed_charge = detail_dic["Billed Charge"]

			fedex_charge_type = self.convert_ups_to_fedex_charge_type(charge_type)
			fedex_calc_funct = self.get_fedex_calc_function(charge_type)
			# fedex_rate = fedex_calc_funct
			# if len(detail_list) > 2:
			# 	print(charge_type, billed_charge)

	def convert_ups_to_fedex_charge_type(self, ups_charge_type):
		fedex_charge_type = self.ups_to_fedex_charge_type_index[ups_charge_type]
		return fedex_charge_type

	def get_fedex_calc_function(self, ups_charge_type):
		fedex_charge_type = self.convert_ups_to_fedex_charge_type(ups_charge_type)
		return self.fedex_charge_type_to_func_index[fedex_charge_type]