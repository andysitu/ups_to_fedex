import math, re

alphabet_dic = {'A': 1, 'B': 2, 'C':3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11,
				'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21,
				'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26,}

rev_alphabet_dic = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K',
					12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U',
					22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z',}

weight_column = 'A'
zone_row = '1'

def get_zone(sheet_value):
	"""
	Gets a sheet value (ex: "Zone 5-14")
	Returns {"start": [num],
			["end": [num]]}
	If there is no range, then start value will equal end.
	Num is in string format.
	"""
	multiple_zone_re = r"(\d+)\s*-\s*(\d+)"
	zone_re = r"(\d)+"

	sheet_str = str(sheet_value)
	
	match_1 = re.search(multiple_zone_re, sheet_str)
	match_2 = re.search(zone_re, sheet_str)
	if match_1 != None:
		return {
			"start": match_1[1], 
			"end": match_1[2],
		}
	elif match_2 != None:
		return {"start": match_2[0],
				"end": match_2[0]}
	else:
		return None

def get_zones(sheet):
	"""
	Input: sheet from wb of openpyxl
	Returns the dict of the start and end of the zones.
		Returns None for the weight column.
	Output: { [weight_column_letter]: 'weight',
			  [zone_column_letter]: 
				{"start": [num], "end": [num] }
			}
	"""
	zone_index = {}
	max_columns = sheet.max_column
	for i in range(1, max_columns + 1):
		column_letter = get_column_letters(i)
		if column_letter == weight_column:
			zone_index[column_letter] = 'weight'
		else:
			cell_location = column_letter + zone_row
			zone_str = sheet[cell_location].value

			zone_dic = get_zone(zone_str)

			zone_index[column_letter] = zone_dic
	return zone_index
	
def get_column_num(letters):
	"""
	Input: letters str (e.g. "AAB")
	Output: int of the column number. Starts with 1.
	"""
	letter_list = list(letters)[::-1]

	total = 0
	for i, letter in enumerate(letter_list):
		total += math.pow(26, i) * alphabet_dic[letter]
	return int(total)

def get_column_letters(column_num):
	""" 
	Input: int of column number
	Output: string of the column (used for excel, e.g. 'AAA')
	"""
	column_letters = ''
	
	# Get highest exponential power
	num_pow = 0
	for i in range(10):
		base = math.pow(26, i)
		remainder = column_num / base
		if remainder <= 26:
			num_pow = i
			break
	total = column_num

	for i in range(num_pow, -1, -1):
		base = math.pow(26, i)
		letter_num = int(total / base)
		total -= letter_num * base
		column_letters += rev_alphabet_dic[letter_num]

	return column_letters