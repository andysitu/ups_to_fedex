import fedex_base_rate

def test_equal(val1, val2):
	if val1 == val2:
		return 1
	else:
		msg = str(val1) + ' and ' + str(val2) +" are not equal."
		raise Exception(msg)


fedex_base_rate.convert_file("fedex_standard_list_base_rate.xlsx", "data", "fedex_discount_rates_no_earned.xlsx")


test_equal(fedex_base_rate.calc_earned_discount(1000000), 0.04)
test_equal(fedex_base_rate.calc_earned_discount(100000), 0.00)
test_equal(fedex_base_rate.calc_earned_discount(5000000), 0.08)
test_equal(fedex_base_rate.calc_earned_discount(4999999.98), 0.07)
test_equal(fedex_base_rate.calc_earned_discount(2000000.01), 0.05)
test_equal(fedex_base_rate.calc_earned_discount(1000000, True), 0.01)
test_equal(fedex_base_rate.calc_earned_discount(100000, True), 0.00)
test_equal(fedex_base_rate.calc_earned_discount(5000000, True), 0.04)
test_equal(fedex_base_rate.calc_earned_discount(4999999.98, True), 0.03)
test_equal(fedex_base_rate.calc_earned_discount(2000000.01, True), 0.015)