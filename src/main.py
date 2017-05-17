from . import reader
from src import ship_data_handler
from src import fedex_rates
from src import excel_maker

def process_ups_data(month_string, day_string, year_string):
	date_string = month_string + day_string + year_string
	folder_name = "ups_invoices"
	simple_ups_filename = date_string + " ups_simple.csv"
	detail_ups_filename = date_string + " ups_detail.csv"
	total_simple_ups_data = reader.read_simple_ups(simple_ups_filename, folder_name)
	total_detail_ups_data = reader.read_detail_ups(detail_ups_filename, folder_name)
	# for tracking_num, detail_list in detail_ups_data.items():
	# 	if len(detail_list) >= 2:
	# 		print("OK")
	# 	print(len(detail_list))
	# 	print(detail_list)
	# 	pass
	s_data_handler = ship_data_handler.Ship_Data_Handler(date_string, total_simple_ups_data, total_detail_ups_data)

	return s_data_handler

def get_fedex_rate_data(track_num, fedex_rate_dic):
	return s_data_handler.get_fedex_rate_data(track_num, fedex_rate_dic)

def get_ups_rate_data(track_num):
	return s_data_handler.get_ups_rate_data(track_num)

def get_rates(s_data_handler, earned_discount = 0):
	fedex_rate_dic = fedex_rates.process_excel_fedex(earned_discount)

	track_num_list = s_data_handler.track_num_index

	for track_num in track_num_list:
		f = get_fedex_rate_data(track_num, fedex_rate_dic)
		u = get_ups_rate_data(track_num)
		# print(u)
		# print(f)


get_rates()
