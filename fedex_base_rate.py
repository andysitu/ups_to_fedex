import ffile, openpyxl
import re

column_letters = [
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
	'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

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

def match_sheet_names(sheet_name):
	s_name = sheet_name.lower()
	sheet_name_regex_delivery_type_index = {
		r"priority overnight": calc_pri_overnight,
		r'standard overnight': calc_overnight,
		r'2 day am': calc_2day_am,
		r'2 day': calc_2day,
		r'express saver': calc_express_saver,
		r'ground': calc_ground,
		r'home': calc_ground,
		r'smart post.*1-16 oz': calc_smartpost_oz,
		r'smart post.*lbs': calc_smartpost_lb,
	}

	for regex in sheet_name_regex_delivery_type_index:
		result = re.search(regex, s_name)
		# print(regex, sheet_name_regex_delivery_type_index[regex], result)
		if result != None:
			return sheet_name_regex_delivery_type_index[regex]

def find_zones(sheet_value):
	"""
	Gets a sheet value (ex: "Zone 5-14")
	Returns a dict containing "start" and "end"
		which corresponds to the starting zone and ending.
	It would be {"start": 5, "end": 14} in the ex.
	If it's just 1 zone, then it would just return
		dic with just "start".
	"""
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


#Functions to calculate the discounted rates
def calc_earned_discount(annual_charge, ground_or_home = False):
	annual_charge = float(annual_charge)
	if annual_charge >= 5000000.00:
		if not ground_or_home:
			return 0.08
		else:
			return 0.04
	elif annual_charge >= 4000000.00 and annual_charge <= 4999999.99:
		if not ground_or_home:
			return 0.07
		else:
			return 0.03
	elif annual_charge >= 3000000.00 and annual_charge <= 3999999.99:
		if not ground_or_home:
			return 0.06
		else:
			return 0.02
	elif annual_charge >= 2000000.00 and annual_charge <= 2999999.99:
		if not ground_or_home:
			return 0.05
		else:
			return 0.015
	elif annual_charge >= 1000000.00 and annual_charge <= 1999999.99:
		if not ground_or_home:
			return 0.04
		else:
			return 0.01
	else:
		if not ground_or_home:
			return 0.00
		else:
			return 0.00

def calc_pri_overnight(zone, weight, full_rate, annual_charge, type_status):
	earned_discount = calc_earned_discount(annual_charge, False)

	discount = .60

	total_discount = earned_discount + discount
	new_rate = full_rate * (1-total_discount)

	if type_status == "envelope":
		new_rate = test_min_charge(new_rate, "priority_overnight_envelope")
	else:
		new_rate = test_min_charge(new_rate, "priority_overnight")
	return new_rate

def calc_overnight(zone, weight, full_rate, annual_charge, type_status):
	earned_discount = calc_earned_discount(annual_charge, False)

	discount = .60

	total_discount = earned_discount + discount
	new_rate = full_rate * (1-total_discount)

	if type_status == "envelope":
		new_rate = test_min_charge(new_rate, "overnight_envelope")
	else:
		new_rate = test_min_charge(new_rate, "overnight")
	return new_rate

def calc_2day_am(zone, weight, full_rate, annual_charge, type_status):
	earned_discount = calc_earned_discount(annual_charge, False)

	discount = .50

	total_discount = earned_discount + discount
	new_rate = full_rate * (1-total_discount)

	if type_status == "envelope":
		new_rate = test_min_charge(new_rate, "2day_am_envelope")
	else:
		new_rate = test_min_charge(new_rate, "2day_am")
	return new_rate

def calc_2day(zone, weight, full_rate, annual_charge, type_status):
	earned_discount = calc_earned_discount(annual_charge, False)

	discount = .55

	total_discount = earned_discount + discount
	new_rate = full_rate * (1-total_discount)

	if type_status == "envelope":
		new_rate = test_min_charge(new_rate, "2day_envelope")
	else:
		new_rate = test_min_charge(new_rate, "2day")
	return new_rate

def calc_express_saver(zone, weight, full_rate, annual_charge, type_status):
	earned_discount = calc_earned_discount(annual_charge, False)

	discount = .55

	total_discount = earned_discount + discount
	new_rate = full_rate * (1-total_discount)

	if type_status == "envelope":
		new_rate = test_min_charge(new_rate, "express_saver_envelope")
	else:
		new_rate = test_min_charge(new_rate, "express_saver")
	return new_rate

def calc_ground(zone, weight, full_rate, annual_charge, type_status):
	earned_discount = calc_earned_discount(annual_charge, True)

	if zone >= 2 or zone <= 8:
		if weight < 11:
			discount = 0.30
		elif weight < 31.0:
			discount = 0.43
		else:
			discount = 0.46
	elif zone == 9 or zone == 17:
		discount = .25
	else:
		discount = 0.00

	total_discount = earned_discount + discount
	new_rate = full_rate * (1-total_discount)

	if zone >= 2 and zone <= 8:
		new_rate = test_min_charge(new_rate, "ground_home_2_to_8")
	elif zone == 9:
		new_rate = test_min_charge(new_rate, "ground_home_9")
	elif zone == 17:
		new_rate = test_min_charge(new_rate, "ground_home_17")
	return new_rate

def calc_smartpost_oz(zone, weight, full_rate, annual_charge, type_status):
	earned_discount = calc_earned_discount(annual_charge, False)

	discount = .30

	total_discount = earned_discount + discount
	new_rate = full_rate * (1-total_discount)

	if zone >= 2 and zone <= 8:
		new_rate = test_min_charge(new_rate, "smartpost_oz_2_to_8")
	else:
		new_rate = test_min_charge(new_rate, "smartpost_oz_9_10_17_99")
	return new_rate

def calc_smartpost_lb(zone, weight, full_rate, annual_charge, type_status):
	earned_discount = calc_earned_discount(annual_charge, False)

	if type_status == "oversize":
		discount = 0.00
	elif weight < 10:
		discount = 0.30
	elif weight < 71:
		discount = 0.10
	else:
		msg = "weight is too heavy in smartpost lb, but it's not oversize. "
		msg += "Weight: " + str(weight) + " ZONE: " + str(zone)
		raise Exception(msg)

	total_discount = earned_discount + discount
	new_rate = full_rate * (1-total_discount)

	if zone >= 2 and zone <= 8:
		new_rate = test_min_charge(new_rate, "smartpost_lb_2_to_8")
	else:
		new_rate = test_min_charge(new_rate, "smartpost_lb_9_10_17_26_99")
	return new_rate

min_charges_dic = {
# POSSIBILITY OF AUTOMATING THIS
	"priority_overnight_envelope": 10.50,
	"priority_overnight": 13.75,
	"overnight_envelope": 10.25,
	'overnight': 11.90,
	'2day_am': 6.30,
	'2day_am_envelope': 6.26,
	'2day': 5.45,
	'2day_envelope': 5.50,
	'express_saver_envelope': 4.80,
	'express_saver': 4.80,
	"ground_home_2_to_8": (7.25 - 0.50),
	"ground_home_9": 27.69,
	"ground_home_17": 27.69,
	"smartpost_oz_2_to_8": (7.25 - 3.00),
	"smartpost_oz_9_10_17_99": (17.01 - 9.00),
	"smartpost_lb_2_to_8": (7.25 - 2.00),
	"smartpost_lb_9_10_17_26_99": (17.01 - 6.00),
}

def test_min_charge(rate, delivery_name_key):
	#Delivery_name refers to the keys used in min_charges
	min_charge = min_charges_dic[delivery_name_key]
	if rate < min_charge:
		return min_charge
	else:
		return rate
