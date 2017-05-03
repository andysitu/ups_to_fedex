from src import excel_helper

def test_equal(val1, val2):
	if val1 == val2:
		return 1
	else:
		msg = str(val1) + ' and ' + str(val2) +" are not equal."
		raise Exception(msg)

test_equal(excel_helper.get_column_num("AAA"), 703)
test_equal(excel_helper.get_column_letters(1), 'A')
test_equal(excel_helper.get_column_letters(16), 'P')

# Test zones
test_equal(excel_helper.get_zone("Zone 5")["start"], "5")
test_equal(excel_helper.get_zone("Zone 5")["end"], "5")
test_equal(excel_helper.get_zone("Zone 5-10")["start"], "5")
test_equal(excel_helper.get_zone("Zone 5-10")["end"], "10")
test_equal(excel_helper.get_zone("Zone 5 - 10")["start"], "5")
test_equal(excel_helper.get_zone("Zone 5 - 10")["end"], "10")
test_equal(excel_helper.get_zone("5")["start"], "5")