from fedex_data import Fedex_Data
import copy

class Fedex_List():
	# def __init__(self):
	# 	self.pickup_date = pickup_date

	service_level_index = copy.deepcopy(Fedex_Data.service_level_index)

	invoice_section_index = {
		"Outbound": True,
		"Adjustments & Other Charges": False,
		"Void Credits": False,
	}

	ups_to_fedex_charge_type_index = copy.deepcopy(Fedex_Data.ups_to_fedex_charge_type_index)

	# charge_type_filter = {
	# 	"Ground Commercial"
	# 	"Fuel Surcharge"
	# 	"Ground Hundredweight"
	# 	"Additional Handling"
	# 	"Ground Residential"
	# 	"Residential Surcharge"
	# 	"Delivery Area Surcharge"
	# 	"2nd Day Air Commercial"
	# 	"Delivery Area Surcharge - Extended"
	# 	"Delivery Confirmation Signature"
	# 	"2nd Day Air Residential"
	# 	"Worldwide Expedited"
	# 	"Extended Area Surcharge"
	# 	"Ground Undeliverable Return"
	# 	"UPS SurePost - 1 lb or Greater"
	# 	"Remote Area Surcharge"
	# 	"Shipment Residential Surcharge"
	# 	"Delivery Confirmation Response"
	# 	"Residential Adjustment"
	# 	"Shipping Charge Correction UPS SurePost - 1 LB or Greater"
	# 	"Shipping Charge Correction Fuel Surcharge"
	# 	"Shipping Charge Correction Additional Handling"
	# 	"Shipping Charge Correction Ground"
	# 	"Shipping Charge Correction Large Package Surcharge"
	# 	"Large Package Surcharge"
	# 	"Not Previously Billed Canada Residential Surcharge"
	# 	"Not Previously Billed Fuel Surcharge"
	# 	"Void Ground Residential"
	# 	"Void Residential Surcharge"
	# 	"Void Delivery Area Surcharge"
	# 	"Void Fuel Surcharge"
	# 	"Shipping Charge Correction Expedited"
	# 	"Standard Shipment"
	# 	"Address Correction Ground"
	# 	"Worldwide Express"
	# 	"Address Correction Expedited"
	# 	"Worldwide Standard"
	# 	"Ground Return to Sender"
	# 	"Return To Sender - Phone Request"
	# 	"Non-machinable Charge"
	# }

	fedex_data_dic = {}

	def add_data(self, date, ups_tracking_num, ups_rate_data_list):
		# print(ups_rate_data_list)
		if date not in self.fedex_data_dic:
			self.fedex_data_dic[date] = {}
		fx_d_dic = self.fedex_data_dic[date]
		#Check if tracking_num exists. If so, then throw error in else.
		if ups_tracking_num not in fx_d_dic:
			if self.filter_ups_simple_data_list(ups_rate_data_list):
				# print(ups_tracking_num)
				f_d = Fedex_Data(date, ups_rate_data_list)
				fx_d_dic[ups_tracking_num] = f_d
				self.index_charge_type(ups_rate_data_list)
				return True
		else:
			e_msg = "fedex list already has an existing"
			e_msg += " data instance with ups "
			e_msg += "tracking num of " + ups_tracking_num
			raise Exception(e_msg)
		return False

	def filter_ups_simple_data_list(self, ups_rate_data_list):
		status = True
		for ups_rate_data in ups_rate_data_list:
			service_level = ups_rate_data["simple"]["Service Level"]
			invoice_section = ups_rate_data["simple"]["Invoice Section"]
			zone = int(ups_rate_data['simple']['Zone'])
			status = self.check_service_level(service_level) and self.check_invoice_section(invoice_section) and self.check_zone(zone)
			# if status:
			# 	print("Service Level: ", service_level, " Invoice Section: ", invoice_section, " Zone: ", zone)
		return status

	def check_service_level(self, service_level):
		return self.service_level_index[service_level]

	def check_invoice_section(self, invoice_section):
		return self.invoice_section_index[invoice_section]

	def check_zone(self, zone):
	# zone should be an int
		return zone >= 2 and zone <= 8

	def index_charge_type(self, ups_rate_data_list):
	# Used in add_data
		for ups_data in ups_rate_data_list:
			for detail_ups_obj  in ups_data["detail"]:
				charge_type = detail_ups_obj["Charge Type"]
				if charge_type not in self.ups_to_fedex_charge_type_index:
					msg = "Index Charge not seen: " + charge_type
					# print(msg)
					# self.ups_charge_type_index[charge_type] = None
					raise Exception(msg)

	def convert_ups_to_fdx(self, ups_data, max_service_level_num, count_status = False):
		count = 0
		count_x = 0
		for date, data_track_num_obj in ups_data.items():
			for track_num, ups_data_obj in data_track_num_obj.items():
				formatted_ups_data = ups_data_obj.get_rate_data()
				# add_status = True, if Fedex_Dat was created
				add_status = self.add_data(date, track_num, formatted_ups_data)
				if count_status:
					if add_status:
						count += 1
					else:
						count_x += 1
				# print(formatted_ups_data)
		if count_status:
			print(count, count_x)