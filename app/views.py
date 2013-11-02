from flask import render_template, request
from app import app
import os
from acutils import run_cmd
import options

# not much to see here
@app.route('/')
def index():
	msg = ['This is the main page of actionCam!!!', 'Powered by a Raspberry Pi', 'model A']
	return render_template('index.html', title='actionCam', message=msg)

#############
#   IMAGE   #
#############
# Form to get arguments
@app.route('/pic')
def get_pic_args():
	return render_template('shoot.html', title='Picture', selecttab=options.picture, action='/pic/shoot')

# Take snapshots using the args provided
@app.route('/pic/shoot')
def take_pic():
	#stillexec = '/usr/bin/raspistill'
	# temp exec file for testing
	stillexec = '/home/torz/data/dev/python/actionCam/bin/raspistill'
	fname = '-o /opt/data/pictures/img%04d.jpg'
	otherargs = '-t 0 -q 75'
	cmd = []
	cmd.extend((stillexec, fname, otherargs))
	# get the args from the URL
	noofpics = request.args.get('pics', type=int)
	delay = request.args.get('delay', type=int)
	# set exposure
	cmd.append('-ex ' + request.args.get('exposure', type=str))
	# set the res low
	if request.args.get('res', type=str) == 'low':
		cmd.append('-w 1280 -h 1024')
	# add them to the command
	msg = run_cmd(cmd, delay, noofpics)
	return render_template('index.html', title='Pic Shoot', message=msg)

#############
#   VIDEO   #
#############
# Form to get arguments
@app.route('/video')
def get_video_args():
	return render_template('shoot.html', title='Video', selecttab=options.video, action='/video/shoot')

# This function should start recording video with the parameters provided
@app.route('/video/shoot')
def start_video():
	#videxec = '/usr/bin/raspivid'
	# temp exec file for testing
	videxec = '/home/torz/data/dev/python/actionCam/bin/raspivid'
	fname = '-o /opt/data/video/vid%04d.h264'
	otherargs = ''
	cmd = []
	cmd.extend((videxec, fname, otherargs))
	# get length
	cmd.append('-t ' + request.args.get('length', type=str))
	delay = request.args.get('delay', type=int) * 1000
	# set quality
	if request.args.get('res', type=str) == 'low':
		cmd.append('-w 1280 -h 720 -b 10000000')
	else:
		cmd.append('-b 15000000')
	# add them to the command
	msg = run_cmd(cmd, delay)
	return render_template('index.html', title='Video Record', message=msg)

# List the vids and pics
@app.route('/files')
def list_files():
	cwd = os.getcwd()
	message = 'Listing dir: ' + cwd
	filesincwd = os.listdir(cwd)
	files = []
	for f in filesincwd:
		myfile = {}
		myfile['name'] = f
		myfile['fullpath'] = os.path.join(cwd, f)
		files.append(myfile)
	return render_template('files.html', title='File List', message=message, files=files)
