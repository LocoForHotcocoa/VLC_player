import requests
from requests.auth import HTTPBasicAuth
import time
from tools.helpers import save_progress, extract_episode_number

url = "http://localhost:8080/requests/status.json"

def check_vlc_status(prog, req, prog_file='progress.json', interval=10):

	while True:
		try:
			# Send a request to get the status of VLC
			response = requests.get(url, auth=HTTPBasicAuth('', 'admin'))  # set password to admin
			if response.status_code == 200:
				status = response.json()  # Parse the JSON response
				filename = status["information"]["category"]["meta"]["filename"] # get filename from very large json object

				current_time = status["time"]
				end_time = status["length"]
				if end_time - current_time < 120:
					prog[req]["episode"] = extract_episode_number(filename) + 1
					print('rounded to next episode, less than 2 min remaining')
				else:
					prog[req]["episode"] = extract_episode_number(filename)

				save_progress(prog, prog_file)
				print(f'updated progress, on {filename}, episode {prog[req]["episode"]}')
			else:
				print(f"Failed to get VLC status: {response.status_code}")
		except Exception as e:
					print(f"Error fetching VLC status: {e}")
		time.sleep(interval)
		