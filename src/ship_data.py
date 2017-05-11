import re
from . import ups_ship_data

class Ship_Data():
# Assume that only outbound charges will be used, meaning no adjustments.
	def __init__(self, tracking_num, simple_ups_data_list, total_detail_ups_data_list):
		# print(simple_ups_data_list)
		# print(total_detail_ups_data_list)
		self.tracking_num = tracking_num

		self.simple_ups_data_instances = {}

		# Values consists of list scontaining detail_ups_instances
		# Each list corresponds to the key (num) with the'
		# simple_ups_data_instances
		self.total_detail_ups_data_instances_dic = {}

		# id for simple_ups_data. It goes up by self.add_simple_ups_data
		# It will be used for id of simple_ups_data and detail_ups_data
		#	Also, will match them together.
		self.num = 0

		self.create_ups_ship_data(simple_ups_data_list, total_detail_ups_data_list)

	def match_simple_and_detail_ups(self, simple_ups_data_list, total_detail_ups_data_list):
		# Not used since anything with length > 1 is filtered out in ship_data_handler
		length_list =len(simple_ups_data_list)

	def create_ups_ship_data(self, simple_ups_data_list, total_detail_ups_data_list):
		for simple_ups_data in simple_ups_data_list:
			simple_ups_data = ups_ship_data.Simple_UPS_Ship_Data(simple_ups_data)

		for detail_ups_data_list in total_detail_ups_data_list:
			for detail_ups_data in detail_ups_data_list:
				d_ups_data = ups_ship_data.Detail_UPS_Ship_Data(detail_ups_data)

	def add_simple_ups_data(self, simple_ups_instance):
		self.simple_ups_data_inst[self.num] = simple_ups_instance
		self.num += 1
		return self.num - 1

	def add_detail_ups_data(self, num, detail_ups_instance):
		if num not in self.total_detail_ups_data_instances_dic:
			self.total_detail_ups_data_instances_dic[num] = [detail_ups_instance, ]
		else:
			self.total_detail_ups_data_instances_dic[num].append(detail_ups_instance)