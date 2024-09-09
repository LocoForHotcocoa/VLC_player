import subprocess as sp
import json
import os
import sys
import fnmatch

progress_file = 'progress.json'

# add new changes to progress file
def save_progress(prog):
	with open(progress_file, 'w') as f:
		json.dump(prog, f, indent=4)


# start watching a new episode, and increment episode # by 1
def start_watch(req, prog):
	episode_path = ""
	episode = prog[req]["episode"] # grab episode number from prog file
	series_folder = prog[req]["parent_dir"] # grab parent dir from prog file

	# this is the glob pattern that I want to use to find new episodes. all episodes must be in this format!
	# an example is : "Better Call Saul S01 {01}.mkv"
	# this bit of logic down below will always look for the *01.* at the end of filename
	# the logic is kinda weird, idk if theres an easier way to do it but it works
	episode_pattern = f"*{episode:>02}.*"

	files = [f for f in os.listdir(series_folder) if fnmatch.fnmatch(f, episode_pattern)]

	if len(files) == 1: # iff it finds one file match:
		episode_path = os.path.join(series_folder, files[0])
	else:
		print('error with start_watch()')
		exit()

	# runs this command in new subprocess, with no output or error messages (I think my VLC is a little buggy)
	sp.run(['vlc', episode_path], stdout=sp.DEVNULL, stderr=sp.DEVNULL)

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