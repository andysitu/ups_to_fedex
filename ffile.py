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

def save(foldername, filename, save_key_name, save_obj):
	move_dir(foldername)
	s = shelve.open(filename)
	s[save_key_name] = save_obj
	s.close()
	dir_back()

def open(foldername, filename, save_key_name):
	move_dir(foldername)
	o = shelve.open(filename)
	data = o[save_key_name]
	o.close()
	dir_back()
	return data

def add(foldername, filename, save_key_name, save_obj, obj_if_not_exist):
	move_dir(foldername)
	a = shelve.open(filename)
	try:
		data = a[save_key_name]
		if save_obj not in data:
			data.append(save_obj)
	except KeyError:
		data = obj_if_not_exist
		data.append(save_obj)
	finally:
		a[save_key_name] = data
	a.close()
	dir_back()