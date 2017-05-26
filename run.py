from src import fedex_base_rates, excel_helper
from src import main

from src import fedex_rates

# fedex_base_rates.get_discounted_rate_files()
# #

#
# s_data_handler = main.open_s_handler(date_str)
# main.make_excel_rates_file(s_data_handler, excel_file_name , "rates")
# print(s)
# print(main.open_s_handler_index())


# print(s.get_ship_data_info('1Z001985YW94090406', 0))
# main.make_rate_excel(s)

# main.process_ship_handler("03", "25", "17")
# main.process_ship_handler("04", "01", "17")
# main.process_ship_handler("04", "08", "17")
# main.process_ship_handler("04", "15", "17")
# main.process_ship_handler("04", "22", "17")
# main.process_ship_handler("04", "29", "17")
# main.process_ship_handler("05", "13", "17")
# main.process_ship_handler("05", "06", "17")
# main.process_ship_handler("05", "22", "17")
# main.process_ship_handler("03", "18", "17")
# main.process_ship_handler("03", "11", "17")
# main.process_ship_handler("03", "04", "17")



s_handler_index = main.open_s_handler_index()
for s_handler_invoice_date in s_handler_index:
    print(s_handler_invoice_date)
    excel_file_name = s_handler_invoice_date + " Rates.xlsx"
    s_handler_inst = main.open_s_handler(s_handler_invoice_date)
    main.make_excel_rates_file(s_handler_inst, excel_file_name , "rates")
#     info_dic = main.get_categorize_info_dic(s_handler_inst)
#     main.make_cat_info_excel_from_categorize_info_dic(info_dic)
    # main.make_total_excel_from_categorize_info_dic(info_dic, s_handler_invoice_date)
    # main.make_avg_excel_from_categorize_info_dic(info_dic, s_handler_invoice_date)
    # main.make_num_items_excel_from_categorize_info_dic(info_dic, s_handler_invoice_date)
    # main.make_abs_total_excel_from_categorize_info_dic(info_dic, s_handler_invoice_date)

# date_str = "05" + "22" + "17"
# excel_file_name = date_str + " Rates.xlsx"
#
# s_data_handler = main.open_s_handler(date_str)
# main.make_excel_rates_file(s_data_handler, excel_file_name , "rates")

# total_info_dic = main.combine_all_info_dic()
#
#
# main.make_cat_info_excel_from_categorize_info_dic(total_info_dic)
#
# charge_type_total_info_dic = main.combine_all_charge_type_info_dic()
# main.make_charge_info_excel_from_charge_info_dic(charge_type_total_info_dic)