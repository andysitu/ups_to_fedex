from . import reader

def read_ups_data():
	reader.read_simple_ups("032517_ups_simple.csv", "ups_invoices")


read_ups_data()