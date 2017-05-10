class Simple_UPS_Ship_Data():
    def __init__(self, simple_ups_data_list, ):
        for simple_data in simple_ups_data_list:
            self.total_bill_charge = simple_data["billed_charge"]
            self.invoice_section = simple_data["invoice_section"]
            self.service_level = simple_data["service_level"]
            self.weight = simple_data["weight"]
            self.zone = simple_data["zone"]
            self.pickup_date = simple_data["pickup_date"]
            self.incentive_credit = self.convert_charge_string_to_float(simple_data["incentive_credit"])
            self.invoice_date = simple_data["invoice_date"]

class Detail_UPS_Ship_Data():
    def __init__(self, detail_ups_data_list):
        print(detail_ups_data_list)
        pass
