import json
import os

def save_progress(progress, progress_filename='progress.json') -> None:
	with open(progress_filename, 'w') as f:
		json.dump(progress, f, indent=4)

def add_element(progress, req, progress_filename='progress.json') -> None:
	if input(f'{req} isn\'t in the progress file... do you want to add it? [y]/n:\n').lower() == 'n':
		print('ok, see ya later!')
		exit()
	print(f'adding {req} to progress file...')
	progress[req] = { "parent_dir":"", "episode":"" }

	# get full path of parent dir
	parent_dir = input(f'what is the full path of {req}?\n')
	while not os.path.exists(parent_dir):
		parent_dir = input('that directory doesn\'t exist. try again:\n')
	progress[req]["parent_dir"] = parent_dir

	# save progress to file, with empty episode field
	save_progress(progress, progress_filename)
	print(f'added {req}.')

def load_progress(progress_filename='progress.json') -> dict:

	progress = {}
	if os.path.exists(progress_filename):
		with open(progress_filename, 'r') as f:
			progress = json.load(f)

	return progress
