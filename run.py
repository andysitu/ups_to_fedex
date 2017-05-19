from src import fedex_base_rates, excel_helper
from src import main

# fedex_base_rates.get_discounted_rate_files()

s_data_handler = main.process_ups_data("03", "25", "17")

# date_str = "03" + "25" + "17"
# excel_file_name = date_string + " Rates.xlsx"
# make_excel_rates_file(s_data_handler, excel_file_name , "rates")

main.save_s_handler(s_data_handler)
s_handler_invoice_date = str(s_data_handler)
s = main.open_s_handler(s_handler_invoice_date)
print(s)
print(main.open_s_handler_index())
# print(s.get_ship_data_info('1Z001985YW94090406', 0))
# main.make_rate_excel(s)

# make_rate_excel("04", "01", "17")
# make_rate_excel("04", "08", "17")
# make_rate_excel("04", "15", "17")
# make_rate_excel("04", "22", "17")
# make_rate_excel("04", "29", "17")
# make_rate_excel("05", "13", "17")
# make_rate_excel("05", "06", "17")
