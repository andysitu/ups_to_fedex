import openpyxl, ffile

def save_fedex_rates(rates):
	ffile.save_fedex_rates(rates)
	return rates

def process_excel_fedex(file_name="fedex_rates.xlsx"):
	ffile.move_dir("data")

	wb = openpyxl.load_workbook(file_name)
	sheetnames_list = wb.get_sheet_names()

	rate_dic = {}

	for delivery_name, para_list in fedex_rate_proc_index.items():
		sheet = wb.get_sheet_by_name(delivery_name)
		rates = proc_sheet_for_rates(sheet, *para_list)
		# print(delivery_name)
		# print(rates)
		rate_dic[delivery_name] = rates

	# sheet = wb.get_sheet_by_name('Standard Overnight')
	# rates = proc_sheet_for_rates(sheet)
	# print(rates)

	ffile.dir_back()

	return rate_dic

def get_rates():
	r = ffile.open_fedex_rates()
	return r

column_letters = [
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
	'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

def get_zone_dic(zone_list, col_letters_list, zone_limit = 8):
	zone_dic = {}

	for i, letter in enumerate(col_letters_list):
		zone_dic[letter] = zone_list[i]

		if zone_list[i] == zone_limit:
			break
	
	return zone_dic

def proc_sheet_for_rates(sheet, zone_row_num=2, rate_start_row_num=6, total_columns=11):
# Skip row 3, b/c Envelopes are usually not used for overnight.
	max_rows = sheet.max_row
	max_columns = sheet.max_column
	col_letters = column_letters[:total_columns]

	zone_list = []
	# Get Zones on second row
	for letter in col_letters:
		zone = sheet[letter + str(zone_row_num)].value
		zone_list.append(zone)

		# if zone == 8:
			# break
	zone_dic = get_zone_dic(zone_list, col_letters)

	##Start translate rows and weight for rate
	weight_dic = {}
	for row in range(rate_start_row_num, max_rows + 1):
		weight = 1
		for letter, zone in zone_dic.items():
			if letter == 'A':
				weight = sheet[letter + str(row)].value
				weight_dic[weight] = {}
			else:
				price = sheet[letter + str(row)].value
				weight_dic[weight][zone] = price
	return weight_dic

fedex_rate_proc_index = {	
# This is for the parameters to use in proc_sheet_for_rates
# Will be iterated to match with the sheet names of the
# 	fedex excel files of the rates in each sheet.
	'Priority Overnight': [2,6,10],
	'Standard Overnight': [2,6,10],
	'2 Day AM': [2,6,10],
	'2 Day': [2,6,11],
	'Express Saver (3 Day)': [2,3,8],
	'Ground': [2,3,8],
	'Home Delivery': [2,3,8],
	'Smart Post 1-16 oz': [2,3,8],
	'Smart Post 1-70 lbs': [2,3,8],

	#Tese are delivery to weird areas

	# 'Deferred Smart Post 1-16 oz': None,
	# 'Deferred Smart Post 1-70 lbs': None,
}

