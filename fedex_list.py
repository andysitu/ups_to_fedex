from fedex_data import Fedex_Data
import copy

class Fedex_List():
	# def __init__(self):
	# 	self.pickup_date = pickup_date

	invoice_section_index = {
		"Outbound": True,
		"Adjustments & Other Charges": False,
		"Void Credits": False,
	}

	ups_service_level_index = copy.deepcopy(Fedex_Data.ups_service_level_index)
	ups_to_fedex_charge_type_index = copy.deepcopy(Fedex_Data.ups_to_fedex_charge_type_index)

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
			# print(self.check_service_level(service_level), self.check_invoice_section(invoice_section), self.check_zone(zone), status)
			# if status:
			# 	print("Service Level: ", service_level, " Invoice Section: ", invoice_section, " Zone: ", zone)
		return status

	def check_service_level(self, ups_service_level):
		if self.ups_service_level_index[ups_service_level] != False:
			return True
		else:
			return False

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
					# print(self.ups_to_fedex_charge_type_index)
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

	def get_dates(self):
		return self.fedex_data_dic.keys()

	def get_ups_tracking_nums(self, date):
		tracking_num_list = []
		data_dic =self.fedex_data_dic[date]
		for tracking_num, data in data_dic.items():
			tracking_num_list.append(tracking_num)

		return tracking_num_list

	def get_all_ups_tracking_nums(self):
		tracking_num_list= []
		dates_list = self.get_dates()
		for date in dates_list:
			tracking_num_list += self.get_ups_tracking_nums(date)
		return tracking_num_list

	def get_first_dataset(self, date, tracking_num):
		data_inst = self.fedex_data_dic[date][tracking_num]
		return data_inst.get_first_dataset()