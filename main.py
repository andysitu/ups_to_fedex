import csv, shelve
import ffile
import make_excel

import ups_reader_simple, ups_reader_detail

py_filename = "ups"


def print_ups_data():
	for ups in ups_data:
		print(ups_data[ups])


def save_ups_data():
	ffile.move_dir('ups_data')

	shelfFile = shelve.open(py_filename)
	shelfFile['ups_data'] = ups_data
	shelfFile.close()

	ffile.dir_back()

ups_data = ups_reader_simple.read('data/ups_simple.csv')
ups_reader_detail.add_details('data/ups_detail.csv', ups_data)

for tracking_num, data in ups_data.items():
	print(tracking_num, data)
	break


# ups_data = ups_reader_detail.read('data/ups_detail.csv')

make_excel.make(ups_data)

# print_upKs_data()
# save_ups_data()

# with open('ups_detail.csv') as f_detail:
# 	reader = csv.reader(f_detail)