import csv, math

# Gives the column for excel file
header_index = {
	"Tracking Number": "N",
	"Charge Type": "AT",
	"Charge Symbol": "AR",
	"Billed Charge": "BA",
}

alphabet_list = {	'A': 1, 'B': 2, 'C':3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11,
				'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21,
				'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26,}

def get_header_num(letters):
	letter_list = list(letters)[::-1]

	total = 0
	for i, letter in enumerate(letter_list):
		total += math.pow(26, i) * alphabet_list[letter]
	return int(total - 1)

def make_header_num_dic(header_index):
	header_num_dic = {}
	for header, header_letters in header_index.items():
		header_num_dic[header] = get_header_num(header_letters)
	return header_num_dic

header_num_dic = make_header_num_dic(header_index)

def add_details(file_name, simple_ups_data):
	header_num_dic = make_header_num_dic(header_index)
	previous_tracking_num = ""

	with open(file_name) as f_detail:
		reader = csv.reader(f_detail)

		# row_num = 0
		# error_row = 0

		for row in reader:
			# row_num += 1

			tracking_num = row[header_num_dic["Tracking Number"]]
			if tracking_num == "":
				# error_row += 1
				continue

			data_dic = {}

			try:
				if "detail" not in simple_ups_data[tracking_num]:
					simple_ups_data[tracking_num]["detail"] = []
			except KeyError:
				print(tracking_num + " not found in ups billing data(detail)")
				print("but it was present in ups invoice data (simple).")
				continue
			
			detail_list = simple_ups_data[tracking_num]["detail"]

			data = {}
			for header, header_num in header_num_dic.items():
				if header == "Tracking Number":
					continue
				data[header] = row[header_num]

			# Batch products by tracking num order
			# in the same list.
			if previous_tracking_num == tracking_num:
				detail_list[len(detail_list) - 1].append(data)
			else:
				detail_list.append([data,])
			previous_tracking_num = tracking_num
			# print(row_num, simple_ups_data[tracking_num]["detail"])
		# print(error_row)