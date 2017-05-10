import re
from . import ups_ship_data

class Ship_Data():
# Assume that only outbound charges will be used, meaning no adjustments.
	def __init__(self, tracking_num, simple_ups_data_list, total_detail_ups_data_list):
		# print(simple_ups_data_list)
		# print(total_detail_ups_data_list)
		self.tracking_num = tracking_num
		self.create_ups_ship_data(simple_ups_data_list, total_detail_ups_data_list)

	def match_simple_and_detail_ups(self, simple_ups_data_list, total_detail_ups_data_list):
		# Not used since anything with length > 1 is filtered out in ship_data_handler
		length_list =len(simple_ups_data_list)

	def create_ups_ship_data(self, simple_ups_data_list, total_detail_ups_data_list):
		simple_ups_data = ups_ship_data.Simple_UPS_Ship_Data(simple_ups_data_list)
		detail_ups_data = ups_ship_data.Detail_UPS_Ship_Data(total_detail_ups_data_list)
		pass