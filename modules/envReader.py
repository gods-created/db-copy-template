import os, json

file_dir = './.env'

def init():
	if not os.path.exists(file_dir):
		return {}

	with open(file_dir, 'r') as file:
		lines = file.readlines()

	data = {}
	for line in lines:
		record = line.split('=')
		data[record[0]] = record[1].replace('\n', '').strip()

	return data 