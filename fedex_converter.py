def convert(ups_data, fedex_list, max_service_level_num):
	for date, data_track_num_obj in ups_data.items():
		for track_num, ups_data_obj in data_track_num_obj.items():
			formatted_ups_data = ups_data_obj.get_rate_data()
			fedex_list.add_data(date, track_num, formatted_ups_data)