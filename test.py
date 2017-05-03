import src.excel_helper

def test_equal(val1, val2):
	if val1 == val2:
		return 1
	else:
		msg = str(val1) + ' and ' + str(val2) +" are not equal."
		raise Exception(msg)

test_equal(excel_helper.get_column_num("AAA"), 703)
test_equal(excel_helper.get_column_letters(1), 'A')
test_equal(excel_helper.get_column_letters(16), 'Q')