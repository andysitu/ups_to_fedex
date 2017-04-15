

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

def convert_ups_data(row):
	ups_data = {}
	for header_infile_name, header in header_dict.items():
		ups_data[header_infile_name] = row[ header_row_index[header_infile_name] ] 
	return ups_data

ups_data = {}