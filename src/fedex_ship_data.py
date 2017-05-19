class Simple_Fedex_Ship_Data():
    def __init__(self, service_level, weight, zone, pickup_date):
        # self.total_bill_charge = simple_ups_data["billed_charge"]
        # self.invoice_section = simple_ups_data["invoice_section"]
        self.service_level = service_level
        self.weight = int(weight)
        self.zone = int(zone)
        self.pickup_date = pickup_date
        # self.incentive_credit = excel_helper.convert_charge_string_to_float(simple_ups_data["incentive_credit"])
        # self.invoice_date = simple_ups_data["invoice_date"]

class Detail_Fedex_Ship_Data():
    def __init__(self, charge_type):
        self.charge_type = charge_type
        # self.billed_charge = detail_ups_data["billed_charge"]