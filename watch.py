import json
import os
import sys
import threading
import time

from tools.helpers import add_element, create_playlist
from tools.signal_handler import *
from tools.status_checker import *
from tools.vlc_controller import *

# main script -------------------------------------------------------------------------------------
#
def main():
	# setup -----------------------------------------
	if (len(sys.argv) != 2):
		print("py watch.py <something to watch>")
		exit()

	progress_file = 'progress.json'
	playlist_file= 'playlist.m3u'
	check_interval = 10 # check status every x seconds

	# will check with progress file
	request = str(sys.argv[1])
	progress = {}

	# Load progress from progress file
	if os.path.exists(progress_file):
		with open(progress_file, 'r') as f:
			progress = json.load(f)

	# if request isn't in progress file, then add new json element
	if request not in progress:
		add_element(request, progress)

	create_playlist(request, progress, playlist_file)


	# main logic ------------------------------------

	# set up ctrl+c signal watch
	setup_signal_handling()

	# start vlc thread
	vlc_thread = threading.Thread(target=run_vlc, args=(playlist_file,))
	vlc_thread.start()

	# delay to get everything initialized
	time.sleep(2)

	# start status thread
	status_thread = threading.Thread(target=check_vlc_status, args=(progress, request, progress_file, check_interval))
	status_thread.start()

	vlc_thread.join()
	status_thread.join()
	stop_vlc()

if __name__ == '__main__':
	main()