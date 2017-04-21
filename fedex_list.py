import fedex_data

class Fedex_List():
	# def __init__(self):
	# 	self.pickup_date = pickup_date

	fedex_data_dic = {}
	def add_data(self, date, ups_tracking_num, data):
		if date not in fedex_data_dic:
			fedex_data_date_dic[date] = {}
		fx_d_dic = fedex_data_dic[date]
		if ups_tracking_num not in fedex_data_date_dic:
			fx_d_dic[ups_tracking_num] = Fedex_Data(date)
		else:
			raise Exception("fedex list already has an existing data instance with ups tracking num of " + ups_tracking_num)