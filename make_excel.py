import openpyxl
import ffile

alphabet_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'K', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def output_raw_data(raw_ups_data):
	ffile.move_dir("excel")

	wb = openpyxl.Workbook()
	sheet = wb.active
	i = 1

	for tracking_num, data_types in raw_ups_data.items():
		sheet['A' + str(i)] = tracking_num
		i += 1
		for data_type, data_list in data_types.items():
			sheet['A' + str(i)] = data_type
			i += 1
			for data in data_list:
				sheet['A' + str(i)] = str(data)
				# for j, key in enumerate(data):
				# 	sheet[alphabet_list[j * 2] + str(i)] = key
				# 	sheet[alphabet_list[j * 2 + 1] + str(i)] = str(data[key])
				i += 1
	wb.save('ups_raw_data.xlsx')

	ffile.dir_back()

	ffile.dir_back()