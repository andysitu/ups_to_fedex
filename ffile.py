import os
import shelve

def move_dir(folder_name):
	try:
		os.chdir('./' + folder_name)
	except(FileNotFoundError):
		os.mkdir(folder_name)
		os.chdir(folder_name)

def dir_back():
	os.chdir('..')

def save_ups_data(ups_data):
	move_dir("ups_data")

	with shelve.open("ups_data") as db:
		db["data"] = ups_data

	dir_back()

def open_ups_data():
	move_dir("ups_data")
	d = None

	with shelve.open("ups_data") as db:
		d = db["data"]

	dir_back()
	return d