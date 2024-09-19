import requests
from requests.auth import HTTPBasicAuth
import time

from tools.playlist import get_next_episode
from tools.vlc_controller import stop_vlc

url = "http://localhost:8080/requests/status.json"

def check_vlc_status(prog, req, playlist, interval=10):

	while True:
		try:
			# Send a request to get the status of VLC
			response = requests.get(url, auth=HTTPBasicAuth('', 'admin'))  # set password to admin
			if response.status_code == 200:
				status = response.json()  # Parse the JSON response
				curr_ep = status["information"]["category"]["meta"]["filename"] # get filename from this super large json object

				current_time = status["time"]
				end_time = status["length"]
				if end_time - current_time < 120:
					next_ep = get_next_episode(playlist, curr_ep)
					if next_ep == None:
						print('all out of episodes! pick next show!')
					else:
						prog[req]["episode"] = next_ep
						print('rounded to next episode, less than 2 min remaining')
				else:
					prog[req]["episode"] = curr_ep

				print(f'updated progress, episode: {prog[req]["episode"]}')
			else:
				print(f"Failed to get VLC status: {response.status_code}")
		except Exception as e:
					print(f"Error fetching VLC status: {e}")
					stop_vlc()
		time.sleep(interval)
		