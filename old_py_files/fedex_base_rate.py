import ffile, openpyxl
import re



def convert_file(filename, folder_name, new_filename ='fedex_rates.xlsx', annual_charge = 0.00):
	""" 
	Opens an excel file containing standard base Fedex rates and will
		convert it to the appropriate values based on the discount
		and the absolute minimum. Will change the excel file itself.
	The excel filel will have first row containing zone information,
		and the first column containing weights.
	"""

	weight_column = 'A'

	ffile.move_dir(folder_name)

	wb = openpyxl.load_workbook(filename)

	sheet_names_list = wb.get_sheet_names()

	for sheet_name in sheet_names_list:
		sheet = wb.get_sheet_by_name(sheet_name)

		calc_func = match_sheet_names(sheet_name)

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

		for row_num in range(2, max_rows + 1):
			row = str(row_num)

			weight = sheet[weight_column + row].value
			for zone, column_letter in column_index.items():
				if zone != "weight":
					cell_loc = column_letter + row
					rate = sheet[cell_loc].value

					#blank rates are returned back
					if rate == '-':
						new_rate = rate
					else:
						new_rate = process_rate(calc_func, zone, weight, rate, annual_charge)
					# print(rate, new_rate)

					sheet[cell_loc] = new_rate
				else:
					# print("weight: " + str(sheet[column_letter + row].value))
					continue

	wb.save(new_filename)
	ffile.dir_back()


def process_column_zone_index(column_index, zone_dic, col_letter):
	"""
	zone_dic refers to the dictionary returned by find_zones
	Indexes key to zone number and value to column letter.
	Only start will be used as index for column index
	"""
	start = int(zone_dic['start'])
	column_index[start] = col_letter

	# if "end" not in zone_dic:
	# 	column_index[start] = col_letter
	# else:
	# 	end = int(zone_dic['end'])
	# 	for zone_num in range(start, end + 1):
	# 		column_index[zone_num] = col_letter

def process_rate(calc_func, zone, weight, full_rate, annual_charge):
	type_status = False

	zone = int(zone)
	full_rate = float(full_rate)
	#convert all parameters into right type
	try:
		weight = int(weight)
	except ValueError:
		weight = weight.lower()
		env_re = r"envelope"
		over_re = r'oversize'
		if re.search(env_re, weight) != None:
			type_status = "weight"
		elif re.search(over_re, weight) != None:
			type_status = "oversize"
	# print(full_rate)
	new_rate = calc_func(zone, weight, full_rate, annual_charge, type_status)
	return new_rate