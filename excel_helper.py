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

