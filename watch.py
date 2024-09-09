import subprocess as sp
import json
import os
import sys
import fnmatch

progress_file = 'progress.json'

def save_progress(prog):
	with open(progress_file, 'w') as f:
		json.dump(prog, f, indent=4)

def start_watch(req, prog):
	episode_path = ""
	episode = prog[req]["episode"]
	episode_pattern = f"*{episode:>02}.*"
	series_folder = prog[req]["parent_dir"]
	files = [f for f in os.listdir(series_folder) if fnmatch.fnmatch(f, episode_pattern)]
	if len(files) == 1:
		episode_path = os.path.join(series_folder, files[0])
	else:
		print('error with start_watch()')
		exit()

	sp.run(['vlc', episode_path], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
	prog[req]["episode"] += 1
	save_progress(prog)


def add_element(req, prog):
	if input(f'{req} isn\'t in the progress file... do you want to add it? [y]/n') == 'n':
		print('ok, try again!')
		exit()
	print(f'adding {req} to progress file...')
	prog[req] = { "parent_dir":"", "episode":1 }
	prog[req]["parent_dir"] = input(f'what is the path of {req}?\n')
	save_progress(prog)
	print('added!')

def main():
	# get input
	if (len(sys.argv) != 2):
		print("py watch.py <something to watch>")
		exit()

	# will check with progress file
	request = str(sys.argv[1])
	progress = {}

	# Load progress
	if os.path.exists(progress_file):
		with open(progress_file, 'r') as f:
			progress = json.load(f)

	if request not in progress:
		add_element(request, progress)

	start_watch(request, progress)
	

	# episode = 1
	# vlc_command = ["vlc", episode_file]

	# sp.run(vlc_command)


if __name__ == '__main__':
	main()