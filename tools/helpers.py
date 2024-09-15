import re
import json
import os

# get episode number from episode filename
def extract_episode_number(filename) -> int:
    # Regular expression to match and capture 2 digit episode numbers
	matches = re.findall(r'\d{2}', filename)
	

	# return episode number, assuming it is in the form "showname season 01 episode 02"
	if len(matches) >= 2:
		return int(matches[1])
	elif len(matches) == 1:
		return int(matches[0]) # last chance, if is in the form "showname episode 02", 
	return None  # Return None if no episode number is found, or it 


# add new changes to progress file
def save_progress(prog, progress_file='progress.json') -> None:
	with open(progress_file, 'w') as f:
		json.dump(prog, f, indent=4)

# returns dict like { 01 : path/to/01,
# 					  03 : path/to/03,
#                     ...
#				    }
# used to ensure that playlist works even when some numbers are missing
# this is probably overcomplicating it lol

def _create_episode_dict(req, prog) -> dict:
	series_folder = prog[req]["parent_dir"] # grab parent dir from prog file
	current_episode = prog[req]["episode"]
	
	episode_dict = {}
	for file in sorted(os.listdir(series_folder)):
		episode_number = extract_episode_number(file)
		if episode_number is not None and episode_number >= current_episode:
			# print(f'file: {file}, match: {episode_number}')
			episode_dict[episode_number] = os.path.join(series_folder, file)

	return episode_dict

# creates the playlist.m3u file
def create_playlist(req, prog, playlist_file='playlist.m3u') -> bool:
	episode_dict = _create_episode_dict(req, prog)
	if len(episode_dict) == 0:
		print("out of episodes? playlist is empty! try again!")
		return False
	with open(playlist_file, 'w') as f:
		for key in sorted(episode_dict.keys()):
			f.write(f"{episode_dict[key]}\n")
	return True
	

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