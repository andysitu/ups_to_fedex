import re
from . import ups_ship_data
from . import excel_helper
import math

class Ship_Data():
# Assume that only outbound charges will be used, meaning no adjustments.
	def __init__(self, tracking_num, simple_ups_data_list, total_detail_ups_data_list):
		# print(simple_ups_data_list)
		# print(total_detail_ups_data_list)
		self.tracking_num = tracking_num

		self.simple_ups_data_instances = {}
		self.simple_fedex_data_instances = {}

		# Values consists of list scontaining detail_ups_instances
		# Each list corresponds to the key (num) with the'
		# simple_ups_data_instances
		self.total_detail_ups_data_instances_dic = {}
		self.total_detail_fedex_data_instances_dic = {}

		# id for simple_ups_data. It goes up by self.add_simple_ups_data
		# It will be used for id of simple_ups_data and detail_ups_data
		#	Also, will match them together.
		self.num = 0

		for simple_ups_data in simple_ups_data_list:
			detail_data_list = self.match_simple_and_detail_ups(simple_ups_data, total_detail_ups_data_list)
			num_id = self.create_and_add_ups_ship_data(simple_ups_data, detail_data_list)

	def match_simple_and_detail_ups(self, simple_ups_data, total_detail_ups_data_list):
		# Not used since anything with length > 1 is filtered out in ship_data_handler
		total_billed_charge = excel_helper.convert_charge_string_to_float(simple_ups_data["billed_charge"])
		for detail_data_list in total_detail_ups_data_list:
			total_charge = 0

			for detail_ups_data in detail_data_list:
				detail_ups_charge = excel_helper.convert_charge_string_to_float(detail_ups_data["billed_charge"])
				total_charge += detail_ups_charge

			if math.isclose(total_billed_charge, total_charge, abs_tol=0.001):
				return detail_data_list

	def create_and_add_ups_ship_data(self, simple_ups_data, detail_ups_data_list):
		simple_ups_instance = ups_ship_data.Simple_UPS_Ship_Data(simple_ups_data)
		num_id = self.add_simple_ups_data_to_index(simple_ups_instance)

		for detail_ups_data in detail_ups_data_list:
			detail_ups_instance = ups_ship_data.Detail_UPS_Ship_Data(detail_ups_data)
			self.add_detail_ups_data_index(num_id, detail_ups_instance)
		return num_id

	def add_simple_ups_data_to_index(self, simple_ups_instance):
		self.simple_ups_data_instances[self.num] = simple_ups_instance
		self.num += 1
		return self.num - 1

	def add_detail_ups_data_index(self, num, detail_ups_instance):
		if num not in self.total_detail_ups_data_instances_dic:
			self.total_detail_ups_data_instances_dic[num] = [detail_ups_instance, ]
		else:
			self.total_detail_ups_data_instances_dic[num].append(detail_ups_instance)


	ups_to_fedex_service_level_index = {
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
		# Adjustments
		"Expedited": False,
		"Standard Shipment": False,
		"Worldwide Express": False,
		"Worldwide Standard": False,
		"Worldwide Expedited Shipment": False,
		"Ground Return to Sender": False,

		'Shipment Residential Surcharge': False,
		"Standard to Canada": False,
		"Worldwide Saver": False,

		# Not sure about this
		"2nd Day Air": False,
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

	def convert_to_fedex_ship_data(self, simple_ups_inst, detail_ups_inst_list):
		ups_service_level = simple_ups_inst.service_level
		ups_weight = simple_ups_inst.weight
		ups_total_charge = simple_ups_inst.total_bill_charge
		ups_zone = simple_ups_inst.zone

		fedex_service_level = self.convert_ups_to_fedex_charge_type(ups_service_level)

		for detail_ups_data in detail_ups_inst_list:
			ups_charge_type = detail_ups_data.charge_type
			ups_charge = detail_ups_data.billed_charge
			if ups_charge_type == "Fuel Surcharge":
				continue
			fedex_charge_type = self.ups_to_fedex_charge_type_index(ups_charge_type)

	def convert_ups_to_fedex_service_level(self, ups_service_level):
		return self.ups_to_fedex_service_level_index[ups_service_level]

	def convert_ups_to_fedex_charge_type(self, ups_charge_type):
		return self.ups_to_fedex_charge_type_index[ups_charge_type]

	def create_fedex_ship_data(self):
		pass

	def get_fedex_calc_function(self, fedex_charge_type):
		if fedex_charge_type == "Ground":
			return self.calc_ground_commercial,
		elif fedex_charge_type == "Fuel Surcharge":
			return self.calc_fuel_surcharge,
		elif fedex_charge_type == "Additional Handling Surcharge":
			return self.calc_add_handling,
		elif fedex_charge_type == "Home Delivery":
			return self.calc_ground_residential,
		elif fedex_charge_type == "Residential Delivery Charge":
			return self.calc_residential_charge,
		elif fedex_charge_type == "Delivery Area Surcharge":
			return self.calc_delivery_area_surcharge,
		elif fedex_charge_type == "Delivery Signature":
			return self.calc_signature,
		elif fedex_charge_type == 'Smart Post 1-70 lbs':
			return self.calc_smart_post_1lb_plus,
		elif fedex_charge_type == "Oversize Charge":
			return self.calc_oversize_charge,
		elif fedex_charge_type == "Non-Machinable":
			return self.calc_nonmachinable_charge,

	# Calculate the rates for fedex charges
	def get_rate(fedex_service_name, weight, zone):
		weight = int(weight)
		zone = int(zone)
		global rates
		if rates == None:
			rates = process_excel_fedex()
			save_fedex_rates(rates)
			rates = open_rates()
		try:
			return rates[fedex_service_name][weight][zone]
		except KeyError:
			print(rates[fedex_service_name])
			print(fedex_service_name)
			print(weight)
			print(zone)


	def calc_ground_commercial(weight, zone):
		return get_rate('Ground', weight, zone)


	def calc_ground_residential(weight, zone):
		return calc_ground_commercial(weight, zone)


	def calc_2_day_air_commercial(weight, zone):
		return get_rate('2 Day', weight, zone)


	def calc_smart_post_1lb_plus(weight, zone):
		return get_rate('Smart Post 1-70 lbs', weight, zone)


	def calc_residential_charge(weight, zone):
		res_surcharge = 3.45
		discount = 0.50
		return res_surcharge - discount


	def calc_oversize_charge(weight, zone):
		oversize_charge = 72.50
		discount = 0.00
		return oversize_charge - discount


	def calc_add_handling(weight, zone):
		add_handling = 11.00
		discount = add_handling * 0.25
		return add_handling - discount


	def calc_delivery_area_surcharge(service_type, residential, extended):
		# type refers to residential or commercial
		delivery_area_surcharge = 0
		if service_type == "Ground":
			if residential:
				if extended:
					delivery_area_surcharge = 4.2
				else:
					delivery_area_surcharge = 3.9
			else:
				delivery_area_surcharge = 2.45
		elif service_type == 'Priority Overnight' or service_type == 'Standard Overnight' or service_type == '2 Day AM' or service_type == '2 Day':
			if residential:
				if extended:
					delivery_area_surcharge = 4.2
				else:
					delivery_area_surcharge = 3.9
			else:
				delivery_area_surcharge = 2.6
		elif service_type == "Home Delivery":
			if extended:
				delivery_area_surcharge = 4.2
			else:
				delivery_area_surcharge = 3.35
		elif service_type == 'Smart Post 1-16 oz' or service_type == 'Smart Post 1-70 lbs':
			if extended:
				delivery_area_surcharge = 1.50
			else:
				delivery_area_surcharge = 1.00
		else:
			msg = "Unknown service_type " + service_type
			print(msg)

		discount = delivery_area_surcharge * 0.25

		return delivery_area_surcharge - discount


	def calc_signature(weight, zone):
		signature_rate = 4.5
		discount = signature_rate * 0.25
		return signature_rate - discount


	def calc_nonmachinable_charge(weight, zone):
		nonmachinable_charge = 2.5
		return nonmachinable_charge


	def calc_fuel_surcharge(date, fedex_detail_data_list, delivery_type, add_fuel_surcharge_index):
		# date is a string 'mm/dd/yyyy'
		# add_fuel_surcharge_index has True for those charge types where the total
		# is calculated with for the percentage calculation with fuel shortage
		fedex_total = 0
		fuel_dic = {"Charge Type": "Fuel Surcharge", }
		date_dic = get_date_from_string(date)

		year = date_dic["year"]
		month = date_dic["month"]
		day = date_dic["day"]

		# print(fedex_detail_data_list)
		for fedex_data_dic in fedex_detail_data_list:
			charge_type = fedex_data_dic["Charge Type"]
			charge_rate = fedex_data_dic["Billed Charge"]
			if add_fuel_surcharge_index[charge_type]:
				fedex_total += charge_rate
		fuel_surcharge_percent = get_fuel_rate(year, month, day, delivery_type) / 100.0

		rate = fedex_total * fuel_surcharge_percent

		fuel_dic["Billed Charge"] = rate
		return fuel_dic


	# Fuel rate percentages are stored in [Express_value, Ground_value]

	fuel_rate_index = {
		# Each date is for the entire week.
		"1/2/2017": [2.50, 4.00],
		"1/9/2017": [2.50, 4.00],
		"1/16/2017": [2.50, 4.00],
		"1/23/2017": [2.50, 4.00],
		"1/30/2017": [2.50, 4.00],
		"2/6/2017": [3.50, 4.50],
		"2/13/2017": [3.50, 4.25],
		"2/20/2017": [3.50, 4.50],
		"2/27/2017": [3.75, 4.50],
		"3/6/2017": [3.75, 4.50],
		"3/13/2017": [3.50, 4.50],
		"3/20/2017": [3.25, 4.50],
		"3/27/2017": [2.75, 4.25],
		"4/3/2017": [2.75, 4.25],
		"4/10/2017": [3.00, 4.25],
		"4/17/2017": [3.50, 4.50],
		"4/24/2017": [3.75, 4.50],
		"5/01/2017": [3.50, 4.50],
	}