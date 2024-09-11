import re
import json
import os

# get episode number from episode filename
def extract_episode_number(filename) -> int:
    # Regular expression to match and capture two-digit episode numbers
    episode_pattern = re.compile(r'.*(\d{2}).*')
	
    # Search for the episode number in the filename
    match = episode_pattern.search(filename)
    if match:
        return int(match.group(1))  # Return the captured episode number
    return None  # Return None if no episode number is found


# add new changes to progress file
def save_progress(prog, progress_file='progress.json') -> None:
	with open(progress_file, 'w') as f:
		json.dump(prog, f, indent=4)

# returns dict like { 01 : path/to/01,
# 					  03 : path/to/03,
#                     ...
#				    }
# used to ensure that playlist works even when some numbers are missing

def _create_episode_dict(req, prog) -> dict:
	series_folder = prog[req]["parent_dir"] # grab parent dir from prog file
	current_episode = prog[req]["episode"]
	
	episode_dict = {}
	episode_pattern = re.compile(r'.*(\d{2}).*')
	for file in os.listdir(series_folder):
		match = episode_pattern.match(file)
		if match:
			episode_number = int(match.group(1))
			if episode_number >= current_episode:
				episode_dict[int(episode_number)] = os.path.join(series_folder, file)

	return episode_dict

# creates the playlist.m3u file
def create_playlist(req, prog, playlist_file='playlist.m3u') -> None:
	episode_dict = _create_episode_dict(req, prog)
	
	with open(playlist_file, 'w') as f:
		for key in sorted(episode_dict.keys()):
			f.write(f"{episode_dict[key]}\n")
	

# if element isn't found in progress.json, then add it!
# includes some UI
def add_element(req, prog) -> None:
	
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
	print(f'added {req}.')