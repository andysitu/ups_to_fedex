from fedex_data import Fedex_Data

class Fedex_List():
	# def __init__(self):
	# 	self.pickup_date = pickup_date

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

	fedex_data_dic = {}
	def add_data(self, date, ups_tracking_num, ups_rate_data_list):
		if date not in self.fedex_data_dic:
			self.fedex_data_dic[date] = {}
		fx_d_dic = self.fedex_data_dic[date]
		#Check if tracking_num exists. If so, then throw error in else.
		if ups_tracking_num not in fx_d_dic:
			if self.check_service_level(ups_rate_data_list):
				f_d = Fedex_Data(date, ups_rate_data_list)
				fx_d_dic[ups_tracking_num] = f_d
		else:
			e_msg = "fedex list already has an existing"
			e_msg += " data instance with ups "
			e_msg += "tracking num of " + ups_tracking_num
			raise Exception(e_msg)

	def check_service_level(self, ups_rate_data_list):
		for ups_rate_data in ups_rate_data_list:
			service_level = ups_rate_data["simple"]["Service Level"]
			if self.service_level_index[service_level]:
				return True
			else:
				return False