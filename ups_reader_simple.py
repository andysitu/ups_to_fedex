import csv, copy

# Key: header_infile_name
# Value: file name used in excel
header_dict = {
	"Tracking Number": "Tracking Number",
	"Service Level": "Service Level",
	"Weight": "Weight",
	"Zone": "Zone",
	# "Reference No": "Reference No.1",
	"Pickup Date": "Pickup Date",
	"Billed Charge": "Billed Charge",
	"Invoice Section": "Invoice Section",
}

# Index starts at 0
# Key: header_infile_name
# ex: {'Service Level': 11, 'Weight': 9, 'Zone': 10, 'Reference No': 6, 
# 'Pickup Date': 12, 'Billed Charge': 27, 'Invoice Section': 29}
header_row_index = {}

raw_ups_data = {}

def f():
	print(header_row_index)

def set_header(row):
	h_row_index = {}
	for header_infile_name, header in header_dict.items():
		h_row_index[header_infile_name] = row.index(header)
	return h_row_index

def get_raw_ups_data(row):
	raw_ups_data = {}
	for header_infile_name, header in header_dict.items():
		raw_ups_data[header_infile_name] = row[ header_row_index[header_infile_name] ]
	return raw_ups_data

def read(file_name):
	raw_ups_data = {}

	#open ups simple csv file & convert to shelve
	with open(file_name) as f_simple:
		reader = csv.reader(f_simple)

		for row in reader:
			try:
				if "Account Number" in row:
					h = set_header(row)
					for k, v in h.items():
						header_row_index[k] = v
					break
			except IndexError:
				pass

		# print(header_row_index)

		# Skip the empty rows (by looking for "Service Charge")
		for row in reader:
			try:
				if "Service Charge" in row:
					break
			except IndexError:
				pass

		# Extract the actual UPS data
		for row in reader:
			try:
				data = get_raw_ups_data(row)
				tracking_num = data["Tracking Number"]
				if tracking_num not in raw_ups_data:
					raw_ups_data[tracking_num] = {"simple": []}
				raw_ups_data[tracking_num]["simple"].append(data)

				del(data["Tracking Number"])

				# if len(raw_ups_data[ tracking_num]["simple"]) >= 3:
				# 	print(raw_ups_data[ tracking_num]["simple"])
				# print(raw_ups_data[tracking_num]["simple"])
			except IndexError:
				pass

	return raw_ups_data