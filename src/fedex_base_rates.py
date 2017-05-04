import ffile
import openpyxl

def open_file(filename, folder_name):
	ffile.move_dir(folder_name)

	wb = openpyxl.load_workbook(filename)
	sheet_names = wb.get_sheet_names()

	for sheet_name in sheet_names:
		sheet = wb.get_sheet_by_name(sheet_name)
		zone_dic = excel_helper.get_zones(sheet)
		# print(zone_dic)

		num_rows = sheet.max_row
		weight_column = excel_helper.weight_column
		for row_num in range( int(excel_helper.zone_row) + 1, num_rows + 1):
			weight = sheet[weight_column + str(row_num)].value
			print(weight)
			# for col_letter, zone
	ffile.dir_back()

def save_file(filename):
	pass