from . import ship_data

class Ship_Data_Handler():
    def __init__(self, invoice_date_str, total_simple_ups_data, total_detail_ups_detail):
        self._ship_data_dic = {}
        self.invoice_date_string = invoice_date_str
        self.track_num_index = []
        self.process(total_simple_ups_data, total_detail_ups_detail)
        pass

    def process(self, total_simple_ups_data, total_detail_ups_detail):
        for track_num, simple_ups_data_list in total_simple_ups_data.items():
            try:
                detail_ups_data_list = total_detail_ups_detail[track_num]
            except KeyError as e:
                msg = track_num + " was not in simple UPS data."
                print(msg)
                continue

            if self.filter_ship_data(simple_ups_data_list, detail_ups_data_list):
                s_data = ship_data.Ship_Data(track_num, simple_ups_data_list, detail_ups_data_list)
                self._ship_data_dic[track_num] = s_data
                self.track_num_index.append(track_num)
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

    def get_fedex_rate_data(self, track_num, fedex_rates_dic):
        """
        Returns list containing lists of dictionaries of each
            charge_type of fedex detail data
        :param track_num: String 
        :param fedex_rates_dic: dictionary of all fedex rates
        :return: List of lists of dictionaries of rates
        """
        ship_data_inst = self._ship_data_dic[track_num]
        num_id_lists = ship_data_inst.num_id_index
        rates_list = []

        for num_id in num_id_lists:
            rate_list = ship_data_inst.get_fedex_rates(num_id, fedex_rates_dic)
            rates_list.append(rate_list)

        return rates_list

    def get_ups_rate_data(self, track_num):
        """
        Returns list containing lists of dictionaries of each
            charge_type of ups detail data
        :param track_num: String 
        :return: List of lists of dictionaries of rates
        """
        ship_data_inst = self._ship_data_dic[track_num]
        num_id_lists = ship_data_inst.num_id_index
        rates_list = []

        for num_id in num_id_lists:
            rate_dic = ship_data_inst.get_ups_rates(num_id)
            rates_list.append(rate_dic)

        return rates_list

    def get_ship_data_info(self, track_num, num_id):
        """
        Gives date, zone, weight from ship data
        :param track_num: dic
        :param num_id: int
        :return: data_dic
        """
        data_dic = {}
        ship_data_inst = self._ship_data_dic[track_num]
        simple_ups_ship_inst = ship_data_inst.simple_ups_data_instances[num_id]
        data_dic["weight"] = simple_ups_ship_inst.weight
        data_dic["zone"] = simple_ups_ship_inst.zone
        data_dic["pickup_date"] = simple_ups_ship_inst.pickup_date
        return data_dic

    def __str__(self):
        return self.invoice_date_string