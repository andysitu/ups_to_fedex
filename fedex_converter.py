def convert(ups_data, fedex_list, max_service_level_num, count_status = False):
	count = 0
	count_x = 0
	for date, data_track_num_obj in ups_data.items():
		for track_num, ups_data_obj in data_track_num_obj.items():
			formatted_ups_data = ups_data_obj.get_rate_data()
			add_status = fedex_list.add_data(date, track_num, formatted_ups_data)
			if count_status:
				if add_status:
					count += 1
				else:
					count_x += 1
			# print(formatted_ups_data)
	if count_status:
		print(count, count_x)