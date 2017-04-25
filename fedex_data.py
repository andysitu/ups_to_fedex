import fedex_rates

class Fedex_Data():

	service_level_index = {
		"Ground Commercial": True,
		"Ground Hundredweight": False,
		"Ground Residential": True,
		"2nd Day Air Commercial": True,
		"2nd Day Air Residential": True,
		"UPS SurePost - 1 LB or Greater": True,

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

	ups_charge_type_index = {
		"Ground Commercial": None,
		"Fuel Surcharge": None,
		"Additional Handling": None,
		"Ground Residential": None,
		"Residential Surcharge": None,
		"Delivery Area Surcharge": None,
		"Delivery Area Surcharge - Extended": None,
		"Delivery Confirmation Signature": None,
		"UPS SurePost - 1 lb or Greater": None,
		"Delivery Confirmation Response": None,
		"Large Package Surcharge": None,
		"Non-machinable Charge": None,
	}

	def __init__(self, date, ups_rate_data_list):
		self.date = date
		ups_rate_data_list
		self.process_ups_data(date, ups_rate_data_list)

	def process_ups_data(self, date, ups_rate_data_list):
		self.convert_first_ups_rate_data(ups_rate_data_list)

	def convert_first_ups_rate_data(self, ups_rate_data_list):
		ups_rate_data = ups_rate_data_list[0]
		# print(ups_rate_data)

		weight = ups_rate_data["simple"]["Weight"]
		zone = ups_rate_data["simple"]["Zone"]
