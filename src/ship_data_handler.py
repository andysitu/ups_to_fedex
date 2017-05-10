from . import ship_data

class Ship_Data_Handler():
    def __init__(self):
        self._ship_data_dic = {}
        pass

    def process(self, total_simple_ups_data, total_detail_ups_detail):
        for track_num, simple_ups_data_list in total_simple_ups_data.items():
            detail_ups_data_list = total_detail_ups_detail[track_num]

            if self.filter_ship_data(simple_ups_data_list, detail_ups_data_list):
                ship_data.Ship_Data(simple_ups_data_list, detail_ups_data_list)
        # for track_num, ups_data_dic in detail_ups_detail.items():
        #     print(simple_ups_data[track_num])

    def filter_ship_data(self, simple_ups_data_list, detail_ups_data_list):
    # Returns True if the Ship_Data instance should be added.

    # Filter any adjustments or anything without adjustments.

        if len(simple_ups_data_list) > 1:
            return False

        for simple_ups_data in simple_ups_data_list:
            invoice_section = simple_ups_data["invoice_section"]
            if invoice_section== "Outbound":
                return True
            elif invoice_section == "Adjustments & Other Charges":
                return False
            elif invoice_section == "Adjustments":
                return False
            elif invoice_section == "Void Credits":
                return False
            else:
                msg = "filter_ship_data of Ship_Data_Handler seen unknown invoice section " + invoice_section
                raise Exception(msg)