import csv, copy

# Key: header_infile_name
# Value: file name used in excel
header_dict = {
	"Tracking Number": "Tracking Number",
	"Service Level": "Service Level",
	"Weight": "Weight",
	"Zone": "Zone",
	"Reference No": "Reference No.1"
}

# Index starts at 0
# Key: header_infile_name
header_row_index = {}

ups_data = {}

def f():
	print(header_row_index)

def set_header(row):
	h_row_index = {}
	for header_infile_name, header in header_dict.items():
		h_row_index[header_infile_name] = row.index(header)
	return h_row_index

def get_ups_data(row):
	ups_data = {}
	for header_infile_name, header in header_dict.items():
		ups_data[header_infile_name] = row[ header_row_index[header_infile_name] ] 
	return ups_data

def read(file_name):
	ups_data = {}

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

		for row in reader:
			try:
				data = get_ups_data(row)
				ups_data[ data["Reference No"] ] = data
			except IndexError:
				pass

	return ups_data