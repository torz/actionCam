import subprocess
from time import sleep

# this function will run raspivid or raspistill and return the output or an error text
def run_cmd(cmd, delay=1, timesrun=1):
	cmdout = []
	for i in range(timesrun):
		#sleep(delay)
		try:
			#subprocess.Popen(cmd, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
			cmdout.append(subprocess.check_output(cmd, stderr=subprocess.STDOUT))
		except Exception as e:
			cmdout.append(e)
	return cmdout
