import ffile, openpyxl
import re

column_letters = [
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
	'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

def convert_file(filename, folder_name):
	weight_column = 'A'

	ffile.move_dir(folder_name)

	wb = openpyxl.load_workbook(filename)



	sheet_names_list = wb.get_sheet_names()

	for sheet_name in sheet_names_list:
		match = match_sheet_names(sheet_name)

	for sheet_name in sheet_names_list:
		print(sheet_name)
		sheet = wb.get_sheet_by_name(sheet_name)

		max_rows = sheet.max_row
		max_columns = sheet.max_column
		col_letters_list = column_letters[:max_columns]

		# Indexes the zone that each column corresponds to (by index)
		column_index = {"weight": weight_column,}
		for letter in col_letters_list:
			zone_value = sheet[letter + '1'].value
			if letter == 'A':
				continue
			zone_dic = find_zones(zone_value)
			process_column_zone_index(column_index, zone_dic, letter)
		print(column_index)


	ffile.dir_back()

def match_sheet_names(sheet_name):
	s_name = sheet_name.lower()
	sheet_name_regex_delivery_type_index = {
		r"priority overnight": 0,
		r'standard overnight': 1,
		r'2 day am': 2,
		r'2 day': 3,
		r'express saver': 4,
		r'ground': 5,
		r'home': 6,
		r'smart post.*1-16 oz': 7,
		r'smart post.*lbs': 8,
	}

	for regex in sheet_name_regex_delivery_type_index:
		result = re.search(regex, s_name)
		# print(regex, sheet_name_regex_delivery_type_index[regex], result)
		if result != None:
			return sheet_name_regex_delivery_type_index[regex]

def find_zones(sheet_value):
	# Gets a sheet value (ex: "Zone 5-14")
	# Returns a dict containing "start" and "end"
	#	which corresponds to the starting zone and ending.
	# It would be {"start": 5, "end": 14} in the ex.
	# If it's just 1 zone, then it would just return
	#	dic with just "start".
	multiple_zone_re = r"(\d+)-(\d+)"
	zone_re = r"(\d)+"

	sheet_str = str(sheet_value)
	
	match_1 = re.search(multiple_zone_re, sheet_str)
	match_2 = re.search(zone_re, sheet_str)
	if match_1 != None:
		return {
			"start": match_1[1], 
			"end": match_1[2],
		}
	elif match_2 != None:
		return {"start": match_2[0],}

def process_column_zone_index(column_index, zone_dic, col_letter):
	# zone_dic referse to the dictinoary returned by find_zones
	# Indexes key to zone number and value to column letter.
	# If mult_zones (ex: 4-15) will have each zone corresponding
	#	to the same column letter
	start = int(zone_dic['start'])

	if "end" not in zone_dic:
		column_index[start] = col_letter
	else:
		end = int(zone_dic['end'])
		for zone_num in range(start, end + 1):
			column_index[zone_num] = col_letter
