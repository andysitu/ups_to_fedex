import csv, math

# Gives the column for excel file
header_index = {
	#"N" seems to be inaccurate as the multiple packages
	# would have the same tracking num in "N"
	"Tracking Number": "U",
	"Charge Type": "AT",
	"Charge Symbol": "AR",
	"Billed Charge": "BA",
}

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

			#Check if Billed Charge is 0
			billed_charge = float(row[header_num_dic["Billed Charge"]])
			# print(billed_charge == 0, billed_charge)
			if billed_charge == 0:
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