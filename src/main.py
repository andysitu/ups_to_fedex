from . import reader
from src import ship_data_handler
from src import fedex_rates
from src import excel_maker
import openpyxl
import ffile

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

def get_fedex_rate_data(s_data_handler, track_num, fedex_rate_dic):
	return s_data_handler.get_fedex_rate_data(track_num, fedex_rate_dic)

def get_ups_rate_data(s_data_handler, track_num):
	return s_data_handler.get_ups_rate_data(track_num)

def get_rates(s_data_handler, earned_discount = 0):
	fedex_rate_dic = fedex_rates.process_excel_fedex(earned_discount)

	track_num_list = s_data_handler.track_num_index

	for track_num in track_num_list:
		f = get_fedex_rate_data(s_data_handler, track_num, fedex_rate_dic)
		u = get_ups_rate_data(s_data_handler, track_num)
		# print(u)
		# print(f)

s_data_handler = process_ups_data("03", "25", "17")
get_rates(s_data_handler, 2)

def make_excel_rates_file(s_data_handler, excel_filename, foldername):
	max_earned_discount_num = 5

	header_list = []
	header_dic = {"Date": 1, "Zone": 2, "Weight": 3, "UPS":4,
				  "Track Num/Rate": 5, "Fedex": 6, "Fedex Rate": 7,
				  "Diff": 8, "Diff Amount": 9}

	# Fill out header_list
	for i in range(1, len(header_dic) + 1):
		for header in header_dic:
			if header_dic[header] == i:
				header_list.append(header)


	data_dict_for_make_excel = {}

	for invoice_date in invoice_date_list:
		excel_data_list = []
		excel_data_list.append(header_list)
		data_dict_for_make_excel[invoice_date] = excel_data_list

	def change_sheet_function(sheet):
		sheet.freeze_panes = 'A2'

		UPS_column_width = 30
		tracking_num_width = 20
		fedex_column_width = 30
		sheet.column_dimensions['D'].width = UPS_column_width
		sheet.column_dimensions['E'].width = tracking_num_width
		sheet.column_dimensions['F'].width = fedex_column_width

	excel_maker.make_excel_file(data_dict_for_make_excel, excel_filename, foldername, change_sheet_function)

make_excel_rates_file(s_data_handler, "test.xlsx", "test")