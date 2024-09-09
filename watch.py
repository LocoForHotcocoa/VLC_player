import subprocess as sp
import json
import os
import sys
import fnmatch
import re

progress_file = 'progress.json'
playlist_file = 'playlist.m3u'

# add new changes to progress file
def save_progress(prog):
	with open(progress_file, 'w') as f:
		json.dump(prog, f, indent=4)

# returns dict like { 01 : path/to/01,
# 					  02 : path/to/02
#				    }

def get_episode_list(req, prog) -> dict:
	series_folder = prog[req]["parent_dir"] # grab parent dir from prog file

	episode_dict = {}
	episode_pattern = re.compile(r'.*(\d{2}).*')
	for file in os.listdir(series_folder):
		match = episode_pattern.match(file)
		if match:
			episode_number = match.group(1)
			episode_dict[int(episode_number)] = os.path.join(series_folder, file)
	
	return episode_dict

# start watching a new episode, and increment episode # by 1
def start_watch(req, prog):
	episode = prog[req]["episode"] # grab episode number from prog file

	episode_dict = get_episode_list(req, prog)

	with open(playlist_file, 'w') as f:
		for key in sorted(k for k in episode_dict.keys() if k >= episode):
			f.write(f"{episode_dict[key]}\n")

	# runs this command in new subprocess, with no output or error messages (I think my VLC is a little buggy)
	sp.run(['vlc', playlist_file], stdout=sp.DEVNULL, stderr=sp.DEVNULL)

	# increment episode count and save progress file
	prog[req]["episode"] += 1
	save_progress(prog)

# if element isn't found in progress.json, then add it!
def add_element(req, prog):
	if input(f'{req} isn\'t in the progress file... do you want to add it? \n[y]/n:  ') == 'n':
		print('ok, see ya later!')
		exit()
	print(f'adding {req} to progress file...')
	prog[req] = { "parent_dir":"", "episode":1 }

	# get full path of parent dir
	parent_dir = input(f'what is the full path of {req}?\n')
	while not os.path.exists(parent_dir):
		parent_dir = input('that directory doesn\'t exist. try again:\n')

	prog[req]["parent_dir"] = parent_dir
	
	save_progress(prog)
	print('added')

def main():
	if (len(sys.argv) != 2):
		print("py watch.py <something to watch>")
		exit()

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

	# now start watching!
	start_watch(request, progress)


if __name__ == '__main__':
	main()