import ffile
import openpyxl

def open_file(filename, folder_name):
	ffile.move_dir(folder_name)

	wb = openpyxl.load_workbook(filename)
	sheet_names = wb.get_sheet_names()

	for sheet_name in sheet_names:
		sheet = wb.get_sheet_by_name(sheet_name)
		get_zones(sheet)

	ffile.dir_back()


def save_file(filename):
	pass

def get_zones(sheet):
	print(sheet)