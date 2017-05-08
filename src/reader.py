import ffile, csv
from . import excel_helper

simple_ups_fieldnames = {
	"tracking_num": "Tracking Number",
	"service_level": "Service Level",
	"weight": "Weight",
	"zone": "Zone",
	# "Reference No": "Reference No.1",
	"pickup_date": "Pickup Date",
	"billed_charge": "Billed Charge",
	"invoice_section": "Invoice Section",
	"incentive_credit": "Incentive Credit"
}

def read_simple_ups(simple_ups_filename, folder_name):
	fieldnames_index = {}

	ffile.move_dir(folder_name)

	simple_ups_data = {}

	def get_fieldnames(row):
		fieldnames_dic = {}
		for infile_name, file_fieldname in simple_ups_fieldnames.items():
			fieldnames_dic[infile_name] = row.index(file_fieldname)
		return fieldnames_dic

	def extract_data(row):
		ups_simple_dic = {}
		for fieldname, column in fieldnames_index.items():
			ups_simple_dic[fieldname] = row[column]
		return ups_simple_dic


	with open(simple_ups_filename) as f_simple:
		reader = csv.reader(f_simple)

		# find row with fieldnames & set fieldnames_index
		for row in reader:
			try:
				if "Account Number" in row:
					fieldnames_index = get_fieldnames(row)
					break
			except IndexError:
				pass

		tracking_num_column = fieldnames_index["tracking_num"]

		for row in reader:
			tracking_num = row[tracking_num_column]
			ups_data = extract_data(row)
			value = ups_data["incentive_credit"]
			simple_ups_data[tracking_num] = ups_data


	ffile.dir_back()

	return simple_ups_data

detail_ups_index = {
	#"N" seems to be inaccurate as the multiple packages
	# would have the same tracking num in "N"
	"tracking_num": "U",
	"charge_type": "AT",
	# "Charge Symbol": "AR",
	"billed_charge": "BA",
	"incentive_credit": "AZ",
}

def get_detail_fieldnames_index():
	f_index = {}
	for fieldname, column_letter in detail_ups_index.items():
		column_num = excel_helper.get_column_num(column_letter)
		f_index[fieldname] = column_num
	return f_index

def read_detail_ups(detail_ups_filename, folder_name):
	total_detail_ups_data = {}

	fieldnames_index = {}
	prev_track_num = ""

	def extract_data_from_row(row):
		# Extracts data from the row of csv file using
		# fieldnames_index dic which gives which and what columns to extract
		ups_detail_dic = {}
		for fieldname, column_num in fieldnames_index.items():
			ups_detail_dic[fieldname] = row[column_num]
		return ups_detail_dic

	ffile.move_dir(folder_name)

	fieldnames_index = get_detail_fieldnames_index()

	with open(detail_ups_filename) as f_detail:
		reader = csv.reader(f_detail)

		for row in reader:
			detail_ups_dic = extract_data_from_row(row)

			# skip those without tracking number or with 0 billed charge
			tracking_num = detail_ups_dic["tracking_num"]
			if tracking_num == "":
				continue
			billed_charge = detail_ups_dic["billed_charge"]
			if billed_charge == 0:
				continue

			if tracking_num not in total_detail_ups_data:
				total_detail_ups_data[tracking_num] = [[total_detail_ups_data,]]
			else:
				d_list = total_detail_ups_data[tracking_num]
				if prev_track_num == tracking_num:
					# print(d_list[len(d_list) -1])
					d_list[len(d_list) -1].append(total_detail_ups_data)
				else:
					d_list.append([total_detail_ups_data,])
			# print(tracking_num, prev_track_num, tracking_num == prev_track_num, tracking_num not in total_detail_ups_data)
			prev_track_num = tracking_num


				# print(detail_ups_dic)
	# print(fieldnames_index)
	ffile.dir_back()

	# print(total_detail_ups_data['1Z0019850396816706'])

	return total_detail_ups_data