import csv, shelve
import ffile
import make_excel

import ups_reader_simple, ups_reader_detail
from ups_data import *

py_filename = "ups"

def print_raw_ups_data():
	for ups in raw_ups_data:
		print(raw_ups_data[ups])

def convert_raw_data_to_data(raw_ups_data_dic):
	ups_data_dict = {}
	for tracking_num, data in raw_ups_data_dic.items():
		# print(tracking_num, data)
		simple_data_list = data["simple"]
		detail_data_super_list = data["detail"]
		# print(simple_data_list)
		# print(detail_data_super_list)
		ups_data = UPS_Data(tracking_num, simple_data_list, detail_data_super_list)
		date = ups_data.date
		if date in ups_data_dict:
			ups_data_dict[date][tracking_num] = ups_data
		else:
			ups_data_dict[date] = {tracking_num: ups_data,}
		# print(ups_data)
	return ups_data_dict

raw_ups_data = ups_reader_simple.read('data/ups_simple.csv')

ups_reader_detail.add_details('data/ups_detail.csv', raw_ups_data)

# print_raw_ups_data()

make_excel.make(raw_ups_data)

data = convert_raw_data_to_data(raw_ups_data)

ffile.save_ups_data(data)


data = ffile.open_ups_data()

# def run_data_inst(data_inst):
# 	data_inst.input_service_level_index()
# 	data_inst.input_charge_type_index()
# 	data_inst.input_charge_symbol_index()

def get_num_1_service_level(data_inst):
	num = 0
	num_x = 0
	for date in data:
		for tracking_num in data[date]:
			num_service_level = data[date][tracking_num].get_num_service_level()
			if num_service_level == 1:
				num += 1
			else:
				num_x += 1
	return (num, num_x)

def print_service_level(ups_data):
	data_with_one_level, data_with_many_level = get_num_1_service_level(data)
	print("Data with one level service: " + str(data_with_one_level))
	print("Data with adjustments: " + str(data_with_many_level))

print_service_level(data)

def iter_thru_data(data, func, *args):
	for date in data:
		for tracking_num in data[date]:
			run_data_inst(data[date][tracking_num])

# iter_thru_data(data, run_data_inst)

# service_level_index = UPS_Data.service_level_index
# for service_level in service_level_index:
# 	print(service_level)
# print("")

# print("CHARGE SYMBOL")
# charge_symbol_index = UPS_Data.charge_symbol_index
# for charge_symbol in charge_symbol_index:
# 	print(charge_symbol)
# print("")

# print("CHARGE TYPE")
# charge_type_index = UPS_Data.charge_type_index
# for charge_type in charge_type_index:
# 	print(charge_type)
# print("")
