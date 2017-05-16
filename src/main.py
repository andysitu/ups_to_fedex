from . import reader
from src import ship_data_handler
from src import fedex_rates
from src import excel_maker

def process_ups_data(month_string, day_string, year_string, rate_dic):
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
	s_data_handler = ship_data_handler.Ship_Data_Handler()

	s_data_handler.process(total_simple_ups_data, total_detail_ups_data, rate_dic)

	return s_data_handler

def get_fedex_rates(earned_discount = 0):
	rate_dic = fedex_rates.process_excel_fedex(0)

	s_data_handler = process_ups_data("03", "25", "17", rate_dic)

get_fedex_rates()