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

def get_media(gallerydir, extension):
	filesinstore = os.listdir(gallerydir)
	mediafiles = []
	for f in filesinstore:
		if extension in f:
			mediafiles.append(f)
	return mediafiles


