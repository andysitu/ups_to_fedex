alphabet_dic = {	'A': 1, 'B': 2, 'C':3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11,
				'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21,
				'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26,}

def get_zone(sheet_value):
	"""
	Gets a sheet value (ex: "Zone 5-14")
	Returns {"start": [num],
			["end": [num]]}
		"end" is present only with zones that have a range.
	"""
	multiple_zone_re = r"(\d+)-(\d+)"
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
		return {"start": match_2[0],}
	else:
		return None

