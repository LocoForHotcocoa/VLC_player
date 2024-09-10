import subprocess as sp
import json
import os
import sys
import threading

import requests
from requests.auth import HTTPBasicAuth
import time

from tools import helpers

url = "http://localhost:8080/requests/status.json"

def check_vlc_status(prog, req, prog_file='progress.json', interval=60) -> None:
	while True:

		time.sleep(interval)
		try:
			# Send a request to get the status of VLC
			response = requests.get(url, auth=HTTPBasicAuth('', 'admin'))  # set password to admin
			if response.status_code == 200:
				status = response.json()  # Parse the JSON response
				filename = status["information"]["category"]["meta"]["filename"] # get filename from http
				prog[req]["episode"] = helpers.extract_episode_number(filename)
				helpers.save_progress(prog, prog_file)
				print(f'updated progress, on {filename}, episode {prog[req]["episode"]}')
			else:
				print(f"Failed to get VLC status: {response.status_code}")
		except Exception as e:
					print(f"Error fetching VLC status: {e}")

# start watching a new episode, and increment episode # by 1
def start_watch(playlist_file='playlist.m3u') -> None:
	# vlc playlist.m3u --extraintf http --http-port 8080 --http-password admin
	# runs this command in new subprocess, with no output or error messages (I think my VLC is a little buggy)
	sp.run(['vlc', playlist_file, '--extraintf', 'http', '--http-port', '8080', '--http-password', 'admin'], stdout=sp.DEVNULL, stderr=sp.DEVNULL)

# main script --------------------------------------------------------------------------------------------------------------
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
watch_thread = threading.Thread(target=start_watch, args=(playlist_file,))
watch_thread.start()
# will be stuck in subprocess until the user exits

# when the user exits, then update the episode counter
# episode = helpers.extract_episode_number(last_played)

# progress[request]["episode"] = episode
# helpers.save_progress(request, progress)
check_vlc_status(progress, request, progress_file, check_interval)

watch_thread.join()