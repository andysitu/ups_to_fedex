from . import ship_data

class Ship_Data_Handler():
    def __init__(self):
        self._ship_data_dic = {}
        pass

    def process(self, total_simple_ups_data, total_detail_ups_detail, rates_dic):
        for track_num, simple_ups_data_list in total_simple_ups_data.items():
            detail_ups_data_list = total_detail_ups_detail[track_num]

            if self.filter_ship_data(simple_ups_data_list, detail_ups_data_list):
                s_data = ship_data.Ship_Data(track_num, simple_ups_data_list, detail_ups_data_list)
                s_data.get_fedex_rates(0, rates_dic)
                self._ship_data_dic[track_num] = s_data
        # for track_num, ups_data_dic in detail_ups_detail.items():
        #     print(simple_ups_data[track_num])

    def filter_ship_data(self, simple_ups_data_list, detail_ups_data_list):
    # Returns True if the Ship_Data instance should be added.

    # Filter any adjustments or anything without adjustments.

        if len(simple_ups_data_list) > 1:
            return False

        # Assumes that simple_ups_data_list is length 1 because
        # previous line filters it out.
        for simple_ups_data in simple_ups_data_list:
            invoice_section = simple_ups_data["invoice_section"]
            ups_service_level = simple_ups_data["service_level"]


            if invoice_section== "Outbound":
                zone_str = simple_ups_data["zone"]
                if zone_str == '':
                    return False
                zone = int(zone_str)
                if zone <= 8 and zone >= 2 and ship_data.Ship_Data.convert_ups_to_fedex_service_level(ups_service_level):
                    return True
                else:
                    return False
            elif invoice_section == "Adjustments & Other Charges":
                return False
            elif invoice_section == "Adjustments":
                return False
            elif invoice_section == "Void Credits":
                return False
            else:
                msg = "filter_ship_data of Ship_Data_Handler seen unknown invoice section " + invoice_section
                raise Exception(msg)