from . import reader
from src import ship_data_handler

def read_ups_data():
	simple_ups_data = reader.read_simple_ups("041517 ups_simple.csv", "ups_invoices")
	detail_ups_data = reader.read_detail_ups("041517 ups_detail.csv", "ups_invoices")
	for tracking_num, detail_list in detail_ups_data.items():
		# if len(detail_list) >= 2:
		# 	print("OK")
		# print(len(detail_list))
		pass
	s_data_handler = ship_data_handler.Ship_Data_Handler()

	s_data_handler.process(simple_ups_data, detail_ups_data)


read_ups_data()