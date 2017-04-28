import csv, shelve
import ffile
import make_excel

import ups_reader_simple, ups_reader_detail
from ups_data import *
import fedex_rates, fedex_list

py_filename = "ups"

def print_raw_ups_data():
	for ups in raw_ups_data:
		print(raw_ups_data[ups])

def convert_raw_data_to_data_obj(raw_ups_data_dic, conv_more_than_one_service_level=True):
	ups_data_dict = {}
	for tracking_num, data in raw_ups_data_dic.items():
		# print(tracking_num, data)
		simple_data_list = data["simple"]
		if not conv_more_than_one_service_level:
			if len(simple_data_list) > 1:
				continue
		# print(tracking_num, data)
		try:
			detail_data_super_list = data["detail"]
		except KeyError:
			msg = tracking_num + " was missing in detail."
			print(msg)
			continue
		# print(simple_data_list)
		# print(detail_data_super_list)
		ups_data = UPS_Data(tracking_num, simple_data_list, detail_data_super_list)
		date = ups_data.date
		if date in ups_data_dict:
			ups_data_dict[date][tracking_num] = ups_data
		else:
			ups_data_dict[date] = {tracking_num: ups_data,}
		# print(ups_data)
	return ups_data_dict

raw_ups_data = ups_reader_simple.read('data/ups_simple.csv')

ups_reader_detail.add_details('data/ups_detail.csv', raw_ups_data)

# print_raw_ups_data()

# make_excel.output_raw_data(raw_ups_data)

ups_converted_data = convert_raw_data_to_data_obj(raw_ups_data, False)

# make_excel.output_conv_ups_data(ups_converted_data)

ffile.save_ups_data(ups_converted_data)

ups_converted_data = ffile.open_ups_data()

def get_num_1_service_level(data_insts):
	num = 0
	num_x = 0
	for date in data_insts:
		for tracking_num in data[date]:
			num_service_level = data[date][tracking_num].get_num_service_level()
			if num_service_level == 1:
				num += 1
			else:
				num_x += 1
	return (num, num_x)

def print_service_level(ups_data):
	data_with_one_level, data_with_many_level = get_num_1_service_level(ups_data)
	print("Data with one level service: " + str(data_with_one_level))
	print("Data with adjustments: " + str(data_with_many_level))

# print_service_level(data)

def iter_thru_data(data, func, *args):
	for date in data:
		for tracking_num in data[date]:
			func(data[date][tracking_num])

def print_indexes(ups_converted_data):
	def run_data_inst(data_inst):
		data_inst.input_service_level_index()
		data_inst.input_invoice_section_index()
		data_inst.input_charge_type_index()
		data_inst.input_charge_symbol_index()

	iter_thru_data(ups_converted_data, run_data_inst)

	print("Service Level Index")
	service_level_index = UPS_Data.service_level_index
	for service_level in service_level_index:
		print(service_level)
	print("")

	print("Invoice Section Index")
	invoice_section_index = UPS_Data.invoice_section_index
	for invoice_section in invoice_section_index:
		print(invoice_section)
	print("")

	print("CHARGE SYMBOL Index")
	charge_symbol_index = UPS_Data.charge_symbol_index
	for charge_symbol in charge_symbol_index:
		print(charge_symbol)
	print("")

	print("CHARGE TYPE Index")
	charge_type_index = UPS_Data.charge_type_index
	for charge_type in charge_type_index:
		print(charge_type)
	print("")

print_indexes(ups_converted_data)

fedex_rates.fill_fuel_rates()

# FEDEX RATES
rates = fedex_rates.process_excel_fedex("fedex_standard_list_base_rate.xlsx")
fedex_rates.save_fedex_rates(rates)
rates = fedex_rates.open_rates()
# print(fedex_rates.rates)
print(fedex_rates.get_rate('Priority Overnight', 1, 7))

fx_list = fedex_list.Fedex_List()

fx_list.convert_ups_to_fdx(ups_converted_data, 1)

print("UPS USED CHARGE TYPES")
for charge_type in fx_list.ups_to_fedex_charge_type_index:
	print(charge_type)

# print(fedex_rates.calc_ground_commercial(4, 4))
# fedex_rates.fill_fuel_rates()
# print(fedex_rates.fuel_rate_dic)

make_excel.output_fedex_ups_dat(fx_list)