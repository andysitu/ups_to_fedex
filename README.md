UPS to Fedex
============

This converts UPS charges from the invoices on the excel files to Fedex charges.

These instructions are temporarily and are for record keeping.

ups_simple refers to the lite invoice data, whereas ups_detail refers to the UPS billing data. Both of these files have to be in ups_to_fedex/data, and the terminal will ask for their date (e.g. 042017) and for the earned discount ("no", "1st", "2nd", "3rd", "4th", "5th"). 

The invoices should have the names of [date] ups_detail.csv and [date] ups_simple.csv.

The fedex rates should be in excel form and should also be in ups_to_fedex/data. It should have the name of "fedex_standard_list_base_rate.xlsx". A copy of it is also in the root directory. To convert this to the discount fedex rates, """ python test.py """ should be used.

To convert the rates, """ python main.py """ shhould be used to actually convert the rates.