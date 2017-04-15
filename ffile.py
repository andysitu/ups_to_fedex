import os

def move_to_folder(folder_name, func):
	try:
		os.chdir('./' + folder_name)
	except(FileNotFoundError):
		os.mkdir(folder_name)
		os.chdir(folder_name)

	func()

	os.chdir('..')