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
