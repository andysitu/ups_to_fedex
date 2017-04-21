import os
import shelve

def move_dir(folder_name):
	# Uses os.chdir to move to a directory.
	# If it doesn't exist (with FileNotFoundError),
	# 	then the directory will be made.
	try:
		os.chdir('./' + folder_name)
	except(FileNotFoundError):
		os.mkdir(folder_name)
		os.chdir(folder_name)

def dir_back(num_times = 1):
	# Moves back to a previous dir.
	# num_times is num of prev dir ('..') to move.
	for i in range(num_times):
		os.chdir('..')

def save_ups_data(ups_data):
	move_dir("data")
	move_dir("ups_data")

	with shelve.open("ups_data") as db:
		db["data"] = ups_data

	dir_back(2)

def open_ups_data():
	move_dir("data")
	move_dir("ups_data")
	d = None

	with shelve.open("ups_data") as db:
		d = db["data"]

	dir_back(2)
	return d

def save_fedex_rates(fedex_data):
	move_dir("data")
	move_dir("fedex_rates")

	with shelve.open("fedex_rates") as db:
		db["data"] = fedex_data

	dir_back(2)

def open_fedex_rates():
	move_dir("data")
	move_dir("fedex_rates")
	d = None

	with shelve.open("fedex_rates") as db:
		d = db["data"]

	dir_back(2)
	return d