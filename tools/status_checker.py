import requests
from requests.auth import HTTPBasicAuth
import time
from tools.helpers import save_progress, extract_episode_number

url = "http://localhost:8080/requests/status.json"

def check_vlc_status(prog, req, prog_file='progress.json', interval=10) -> None:

	while True:
		try:
			# Send a request to get the status of VLC
			response = requests.get(url, auth=HTTPBasicAuth('', 'admin'))  # set password to admin
			if response.status_code == 200:
				status = response.json()  # Parse the JSON response
				filename = status["information"]["category"]["meta"]["filename"] # get filename from http
				prog[req]["episode"] = extract_episode_number(filename)
				save_progress(prog, prog_file)
				print(f'updated progress, on {filename}, episode {prog[req]["episode"]}')
				time.sleep(interval)
			else:
				print(f"Failed to get VLC status: {response.status_code}")
		except Exception as e:
					print(f"Error fetching VLC status: {e}")