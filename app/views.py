from flask import render_template, request
from app import app
from acutils import run_cmd, get_media
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
	selecttab = [ options.noofpics, options.delay, options.exposure, options.res ]
	return render_template('shoot.html', title='Picture', selecttab=selecttab, action='/pic/shoot')

# Take snapshots using the args provided
@app.route('/pic/shoot')
def take_pic():
	cmd = []
	cmd.append('still')
	# delay between pics
	cmd.append(request.args.get('delay', type=str))
	# how many pics to take
	cmd.append(request.args.get('pics', type=str))
	# Set image width <size>, height <size> 
	if 	request.args.get('res', type=str) == 'high':
		cmd.append('-w 2592 -h 1944')
	elif request.args.get('res', type=str) == 'low':
		cmd.append('-w 1280 -h 1024')
	# Set jpeg quality <0 to 100>
	cmd.append('-q 75')
	# Output filename <filename>
	cmd.append('-o ' + options.photostore + '/img%04d.jpg')
	# timeout
	cmd.append('-t 0')
	# Set thumbnail parameters (x:y:quality) 
	cmd.append('-th 0:0:0')
	# Do not display a preview window
	cmd.append('-n')
	# set exposure
	cmd.append('-ex ' + request.args.get('exposure', type=str))
	msg = run_cmd(cmd)
	return render_template('index.html', title='Pic Shoot', message=msg)

#############
#   VIDEO   #
#############
# Form to get arguments
@app.route('/video')
def get_video_args():
	selecttab = [ options.vidlength, options.delay, options.exposure, options.res ]
	return render_template('shoot.html', title='Video', selecttab=selecttab, action='/video/shoot')

# This function should start recording video with the parameters provided
@app.route('/video/shoot')
def start_video():
	cmd = []
	cmd.append('video')
	# delay before video starts
	cmd.append(request.args.get('delay', type=str))
	# Set image width <size>, height <size>
	if request.args.get('res', type=str) == 'high':
		cmd.append('-w 1920 -h 1080 -b 15000000')
	elif request.args.get('res', type=str) == 'low':
		res = '-w 1280 -h 720 -b 10000000'
	# get length
	cmd.append('-t ' + request.args.get('length', type=str))
	# Output filename <filename>
	cmd.append('-o ' + options.vidoestore + '/vid%04d.h264')
	# set exposure
	cmd.append('-ex ' + request.args.get('exposure', type=str))
	msg = run_cmd(cmd)
	return render_template('index.html', title='Video Record', message=msg)

@app.route('/gallery')
def show_gallery():
	message = ['Gallery']
	photos = []
	return render_template('gallery.html', title='Gallery', message=message, photos=photos)

# List the vids and pics
@app.route('/gallery/photos')
def photo_gallery():
	message = ['Photo gallery']
	photos = get_media(options.photostore, '.jpg')
	return render_template('gallery.html', title='File List', message=message, photos=photos)

@app.route('/gallery/video')
def vid_gallery():
	message = ['Video gallery']
	videos = get_media(options.vidoestore, '.h264')
	return render_template('vidgallery.html', title='Video gallery', message=message, videos=videos)
