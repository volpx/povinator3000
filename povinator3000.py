#!/usr/bin/env python3
import subprocess

# edit accordingly
EMAIL_FIELD=1
DEGREE_FIELD=2
DEGREE_COURSE_FIELD=3
COMMISSION_NUMBER_FIELD=4
ROOM_FIELD=5
FILES_FIELD=6

OUTPUT_FOLDER='Lauree'

DOWNLOAD_COMMAND='curl -O -J -L https://drive.google.com/uc?id={file_id}'

def get_id(url):
	pieces=url.split('&')
	for p in pieces:
		if p[0:3] == 'id=':
			return p[3:]

def get_filename(response):
	start=response.find(' \'')+2
	end=len(response)-4
	return response[start:end]



if __name__ == "__main__":
	import sys
	response_file=sys.argv[1]

	print('Make output directory ...')
	subprocess.run(['mkdir', '-p', OUTPUT_FOLDER])

	print('Reading file ...')
	with open(response_file,'r') as file:
		for line in file.readlines():
			lp=line.replace('\n','').replace('"','').split(',')
			# print(lp)
			if lp[0]=='Timestamp':
				# skip first line
				continue

			# create destination folder
			# modify the list below to modify
			# the folders pattern
			dd='/'.join([
				OUTPUT_FOLDER,
				lp[DEGREE_FIELD],
				lp[DEGREE_COURSE_FIELD],
				lp[ROOM_FIELD]+'-'+lp[COMMISSION_NUMBER_FIELD],lp[EMAIL_FIELD]])
			subprocess.run(['mkdir', '-p', dd])

			# download files
			print('Getting files of',lp[EMAIL_FIELD],'...')
			files_urls=lp[FILES_FIELD].split(';')
			for i,url in enumerate(files_urls):
				# get the id field
				file_id=get_id(url)

				response=subprocess.run(DOWNLOAD_COMMAND.format(file_id=file_id).split(' '),capture_output=True)

				filename=get_filename(str(response.stdout))

				subprocess.run(['mv',filename,dd])
