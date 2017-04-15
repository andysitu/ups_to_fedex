import csv, shelve
import ffile

py_filename = "ups"

def get_row_headers():
	print("HELLO")

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

def get_ups_data(row):
	ups_data = {}
	for header_infile_name, header in header_dict.items():
		ups_data[header_infile_name] = row[ header_row_index[header_infile_name] ] 
	return ups_data

ups_data = {}

def set_header(row):
	header_row_index = {}
	for header_infile_name, header in header_dict.items():
		header_row_index[header_infile_name] = row.index(header)
	return header_row_index

def print_ups_data():
	for ups in ups_data:
		print(ups_data[ups])

def save_ups_data():
	shelfFile = shelve.open(py_filename)
	shelfFile['ups_data'] = ups_data
	shelfFile.close()

#open ups simple csv file & convert to shelve
with open('ups_simple.csv') as f_simple:
	reader = csv.reader(f_simple)

	for row in reader:
		try:
			if "Account Number" in row:
				header_row_index = set_header(row)
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

print_ups_data()
save_ups_data()

# with open('ups_detail.csv') as f_detail:
# 	reader = csv.reader(f_detail)