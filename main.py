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
		simple_data_list = data["simple"]
		detail_data_super_list = data["detail"]
		# print(tracking_num)
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

# ups_data = ups_reader_detail.read('data/ups_detail.csv')

# make_excel.make(raw_ups_data)

data = convert_raw_data_to_data(raw_ups_data)

ffile.save_ups_data(data)


# with open('ups_detail.csv') as f_detail:
# 	reader = csv.reader(f_detail)