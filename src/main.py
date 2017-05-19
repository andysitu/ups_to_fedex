from . import reader
from src import ship_data_handler
from src import fedex_rates
from src import excel_maker

from inspect import signature
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

def make_excel_rates_file(s_data_handler, excel_filename, foldername):
	max_earned_discount_num = 5

	def make_excel_data_list(header_list, data_dic):
		data_list = []
		for header in header_list:
			data_list.append(data_dic[header])
		return data_list

	def make_data_dic(date="",zone="",weight= "",
					  ups="",ups_rate ="",fedex="",
					  fedex_rate="",diff="",diff_amnt=""):
		return {
			"Date": date,
			"Zone": zone,
			"Weight": weight,
			"UPS": ups,
			"Track Num/ Rate": ups_rate,
			"Fedex": fedex,
			"Fedex Rate": fedex_rate,
			"Diff": diff,
			"Diff Amount": diff_amnt,
		}

	def make_header_dic(data_dic_func):
		sig = signature(data_dic_func)
		params = sig.parameters
		arg_length = len(params)
		num_list = list(range(1,arg_length+1))
		header_dic = make_data_dic(*num_list)
		return header_dic

	def make_header_list(header_dic):
		header_list = []
		for i in range(1, len(header_dic) + 1):
			for header in header_dic:
				if header_dic[header] == i:
					header_list.append(header)
		return header_list

	header_dic = make_header_dic(make_data_dic)
	header_list = make_header_list(header_dic)

	def create_and_add_data_list():
		title_dic = make_data_dic(date=item_info["pickup_date"], zone=item_info["zone"],
								  weight=item_info["weight"], ups="UPS",
								  ups_rate=track_num, fedex="Fedex", )
		title_list = make_excel_data_list(header_list, title_dic)
		excel_data_list.append(title_list)

	track_num_list = s_data_handler.track_num_index

	data_dict_for_make_excel = {}

	#
	for earned_discount_num in range(max_earned_discount_num + 1):
		total_ups_billed_charge = 0.00
		total_fedex_billed_charge = 0.00

		fedex_rate_dic = fedex_rates.process_excel_fedex(earned_discount_num)
		excel_data_list = []
		excel_data_list.append(header_list)

		for track_num in track_num_list:
			total_fedex_data_list = get_fedex_rate_data(s_data_handler, track_num, fedex_rate_dic)
			total_ups_data_list = get_ups_rate_data(s_data_handler, track_num)

			for num_id,ups_data_list in enumerate(total_ups_data_list):
				item_info = s_data_handler.get_ship_data_info(track_num, num_id)
				fedex_data_list = total_fedex_data_list[num_id]

				title_dic = make_data_dic(date=item_info["pickup_date"],zone=item_info["zone"],
									   weight=item_info["weight"],ups="UPS",
									   ups_rate=track_num,fedex="Fedex",)
				title_list = make_excel_data_list(header_list, title_dic)
				excel_data_list.append(title_list)

				ups_charges = 0
				fedex_charges = 0

				for i, ups_data_dic in enumerate(ups_data_list):
					fedex_data_dic = fedex_data_list[i]
					u_charge_type = ups_data_dic["charge_type"]
					u_charge = ups_data_dic["billed_charge"]

					f_charge_type = fedex_data_dic["charge_type"]
					f_charge = fedex_data_dic["billed_charge"]


					ups_charges += u_charge
					fedex_charges += f_charge
					total_ups_billed_charge += u_charge
					total_fedex_billed_charge += f_charge


					charges_dic = make_data_dic(ups=u_charge_type,ups_rate=u_charge,
											  fedex=f_charge_type,fedex_rate=f_charge )
					charges_list = make_excel_data_list(header_list, charges_dic)
					excel_data_list.append(charges_list)

				charges_dic = make_data_dic(ups="UPS TOTAL", ups_rate=ups_charges,
											fedex="FEDEX TOTAL", fedex_rate=fedex_charges,
											diff="Difference", diff_amnt=ups_charges-fedex_charges)
				charges_list = make_excel_data_list(header_list, charges_dic)
				excel_data_list.append(charges_list)




		sheetname = str(earned_discount_num) + " earned discount"
		# Row 2 for total UPS
		excel_data_list[1].append("Total UPS")
		excel_data_list[1].append(total_ups_billed_charge)

		# Row 3 for total Fedex
		excel_data_list[2].append("Total Fedex")
		excel_data_list[2].append(total_fedex_billed_charge)

		# Row 4 for difference
		ups_fed_diff = total_ups_billed_charge - total_fedex_billed_charge
		excel_data_list[3].append("Tot. Difference")
		excel_data_list[3].append(ups_fed_diff)

		# Row 5 for difference
		excel_data_list[4].append("% Diff. from UPS")
		excel_data_list[4].append(ups_fed_diff / total_ups_billed_charge)

		data_dict_for_make_excel[sheetname] = excel_data_list

		# make_excel_data_list(header_list, data_dict_for_make_excel)

	def change_sheet_function(sheet):
		sheet.freeze_panes = 'A2'

		UPS_column_width = 30
		tracking_num_width = 20
		fedex_column_width = 30
		sheet.column_dimensions['D'].width = UPS_column_width
		sheet.column_dimensions['E'].width = tracking_num_width
		sheet.column_dimensions['F'].width = fedex_column_width

	excel_maker.make_excel_file(data_dict_for_make_excel, excel_filename, foldername, change_sheet_function)

def make_rate_excel(month_str, day_str, year_str):
	s_data_handler = process_ups_data(month_str, day_str, year_str)
	date_string = month_str + day_str + year_str
	file_name = date_string + " Rates.xlsx"
	# get_rates(s_data_handler, 2)
	make_excel_rates_file(s_data_handler, file_name , "rates")

