import ffile
import openpyxl
from . import excel_helper

def open_file(filename, folder_name):
	ffile.move_dir(folder_name)

	wb = openpyxl.load_workbook(filename)
	sheet_names = wb.get_sheet_names()

	for sheet_name in sheet_names:
		sheet = wb.get_sheet_by_name(sheet_name)
		zones_dic = excel_helper.get_zones(sheet)
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

def get_calc_func(sheet_name):
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

	if zone >= 2 and zone <= 8:
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
