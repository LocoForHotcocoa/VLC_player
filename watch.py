import json
import os
import sys
import threading

from tools import helpers

# main script --------------------------------------------------------------------------------------------------------------

def main():
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
		helpers.add_element(request, progress)

	helpers.create_playlist(request, progress, playlist_file)

	# now start watching!
	watch_thread = threading.Thread(target=helpers.start_watch, args=(playlist_file,))
	watch_thread.start()
	# will be stuck in subprocess until the user exits

	# when the user exits, then update the episode counter
	# episode = helpers.extract_episode_number(last_played)

	# progress[request]["episode"] = episode
	# helpers.save_progress(request, progress)
	helpers.check_vlc_status(progress, request, progress_file, check_interval)

	watch_thread.join()

if __name__ == '__main__':
	main()