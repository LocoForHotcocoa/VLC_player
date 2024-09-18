import json
import os
import sys
import threading
import time

from tools.playlist import create_playlist
from tools.progress import add_element
from tools.signal_handler import setup_signal_handling
from tools.status_checker import check_vlc_status
from tools.vlc_controller import run_vlc

# main script -------------------------------------------------------------------------------------
#

# script explanation:
# progress file contains parent directory and current filename for each show
# 
#	- playlist is created, starts at whatever is in progress[request]["episode"]
#	- signal handling starts, waits for ctrl+c which will start the graceful quitting process; signal_handler.py
#	- main thread starts, the vlc subprocess; vlc_controller.py
#	- wait 2 seconds
#	- daemon thread starts, the status checker, which keeps track of current episode from http interface, and increments it when necessary;
#	  status_checker.py
#	- end script when ctrl+c is registered.

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


	# if its a new season, add element and set curr_ep to ""
	if request not in progress:
		add_element(progress, request, progress_file)

	parent_dir = progress[request]["parent_dir"]
	curr_ep = progress[request]["episode"]

	# if new season, playlist will start from beginning. writes to playlist file
	playlist = create_playlist(parent_dir, curr_ep, playlist_file)

	# main logic ------------------------------------

	# set up ctrl+c signal watch
	setup_signal_handling()

	# start vlc thread
	vlc_thread = threading.Thread(target=run_vlc, args=(playlist_file,))
	vlc_thread.start()

	# delay to get everything started
	time.sleep(2)

	# start status thread
	status_thread = threading.Thread(target=check_vlc_status, args=(progress, request, playlist, progress_file, check_interval), daemon=True)
	status_thread.start()

	vlc_thread.join()
	sys.exit(0)

if __name__ == '__main__':
	main()