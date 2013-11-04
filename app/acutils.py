import subprocess
import os

# this function will run raspivid or raspistill and return the output or an error text
def run_cmd(cmd):
	myexec = '/usr/local/bin/rpshooter'
	cmd.insert(0, myexec)
	try:
		subprocess.Popen(cmd, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
		return cmd
	except Exception as e:
		return e

def get_photos():
	imgstore = '/opt/data/torz/dev/python/actionCam/app/static/photos'
	filesinstore = os.listdir(imgstore)
	photos = []
	for f in filesinstore:
		if 'jpg' in f:
			photos.append(f)
	return photos


