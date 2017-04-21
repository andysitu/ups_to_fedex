class Fedex_Data():

	ups_charge_type_index = {
		"Ground Commercial": None,
		"Fuel Surcharge": None,
		"Additional Handling": None,
		"Ground Residential": None,
		"Residential Surcharge": None,
		"Delivery Area Surcharge": None,
		"2nd Day Air Commercial": None,
		"Delivery Area Surcharge - Extended": None,
		"Delivery Confirmation Signature": None,
		"2nd Day Air Residential": None,
		"UPS SurePost - 1 lb or Greater": None,
		"Remote Area Surcharge": None,
		"Delivery Confirmation Response": None,
		"Large Package Surcharge": None,
		"Non-machinable Charge": None,
	}

	def __init__(self, date, ups_rate_data_list):
		self.date = date
		print(ups_rate_data)