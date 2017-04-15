import os

def move_dir(folder_name):
	try:
		os.chdir('./' + folder_name)
	except(FileNotFoundError):
		os.mkdir(folder_name)
		os.chdir(folder_name)

def dir_back():
	os.chdir('..')