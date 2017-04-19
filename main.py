import csv, shelve
import ffile
import make_excel

import ups_reader_simple, ups_reader_detail
from ups_data import *

py_filename = "ups"

def print_raw_ups_data():
	for ups in ups_data:
		print(ups_data[ups])

def save_ups_data():
	ffile.move_dir('saved_data')

	shelfFile = shelve.open(py_filename)
	shelfFile['ups_data'] = ups_data
	shelfFile.close()

	ffile.dir_back()

def convert_raw_data_to_data(raw_ups_data_dic, func):
	for tracking_num, data in raw_ups_data_dic.items():
		simple_data_list = data["simple"]
		detail_data_super_list = data["detail"]
		# print(tracking_num)
		# print(simple_data_list)
		# print(detail_data_super_list)
		ups_data = UPS_Data(tracking_num, simple_data_list, detail_data_super_list)
		print(ups_data)

raw_ups_data = ups_reader_simple.read('data/ups_simple.csv')

ups_reader_detail.add_details('data/ups_detail.csv', raw_ups_data)

# ups_data = ups_reader_detail.read('data/ups_detail.csv')

# make_excel.make(raw_ups_data)

data = convert_raw_data_to_data(raw_ups_data)

# print_upKs_data()
# save_ups_data()

# with open('ups_detail.csv') as f_detail:
# 	reader = csv.reader(f_detail)