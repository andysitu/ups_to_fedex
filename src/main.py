from . import reader
from src import ship_data_handler

def process_ups_data(date_string):
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
	s_data_handler = ship_data_handler.Ship_Data_Handler()

	s_data_handler.process(total_simple_ups_data, total_detail_ups_data, rate_dic)

process_ups_data("032517")