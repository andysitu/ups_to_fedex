import re


def convert_charge_string_to_float(charge_string):
    """
    :param charge_string: string from CSV ups simple file (ex. -$5.55)
    :return: float of the charge_value
    """
    charge = 0.00
    # charge_re = re.compile(r"(\-*).*(\d+\.\d+)")
    bill_charge_re = re.compile(r"\d+\.\d+")
    charge_re_result = (bill_charge_re.search(charge_string))[0]

    if charge_string[0] == '-':
        # Negative charge values have a negative sign (eg "-4.24")
        charge = -float(charge_re_result)
    else:
        charge = float(charge_re_result)

    return charge

class Simple_UPS_Ship_Data():
    def __init__(self, simple_ups_data, ):
        self.total_bill_charge = simple_ups_data["billed_charge"]
        self.invoice_section = simple_ups_data["invoice_section"]
        self.service_level = simple_ups_data["service_level"]
        self.weight = simple_ups_data["weight"]
        self.zone = simple_ups_data["zone"]
        self.pickup_date = simple_ups_data["pickup_date"]
        self.incentive_credit = convert_charge_string_to_float(simple_ups_data["incentive_credit"])
        self.invoice_date = simple_ups_data["invoice_date"]

class Detail_UPS_Ship_Data():
    def __init__(self, detail_ups_data):
        self.charge_type = detail_ups_data["charge_type"]
        self.billed_charge = detail_ups_data["billed_charge"]
        self.incentive_credit = detail_ups_data["incentive_credit"]