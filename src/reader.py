import ffile, csv

simple_ups_fieldnames = {
	"tracking_num": "Tracking Number",
	"service_level": "Service Level",
	"weight": "Weight",
	"zone": "Zone",
	# "Reference No": "Reference No.1",
	"pickup_date": "Pickup Date",
	"charge": "Billed Charge",
	"invoice_section": "Invoice Section",
	"incentive": "Incentive Credit"
}

def read_simple_ups(simple_ups_filename, folder_name):
	fieldnames_index = {}

	ffile.move_dir(folder_name)

	simple_ups_data = []

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
			value = ups_data["incentive"]
			simple_ups_data.append(ups_data)
			# print(row)


	ffile.dir_back()

	return simple_ups_data

def read_detail_ups():
	pass