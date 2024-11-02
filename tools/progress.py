import json
import os
import sys
import time
if __name__=='__main__':
    from gui import gui
else:
    from tools.gui import gui

# initializes the progress object if the file doesn't exist
def _init_progress(progress_filename='progress.json') -> dict:
    parent_dir = input('enter the full path of your show/movie folder:\n')
    progress = {"parent_dir":"", "media":{}}
    progress["parent_dir"] = parent_dir
    save_progress(progress, progress_filename)
    print(f'initialized {progress_filename} 👍')
    return progress


# just used to save object to progress file, uses pretty indentation
def save_progress(progress, progress_filename='progress.json') -> None:
    with open(progress_filename, 'w') as f:
        json.dump(progress, f, indent=4)


### old function, now we use the gui/fuzzyfinder method to add a new element
#
# def add_element(progress, req, progress_filename='progress.json') -> None:
#     if input(f'{req} isn\'t in the progress file... do you want to add it? [y]/n:\n').lower() == 'n':
#         print('ok, see ya later!')
#         exit()
#     print(f'adding {req} to progress file...')
#     progress[req] = { "parent_dir":"", "episode":"" }

#     # get full path of parent dir
#     parent_dir = input(f'what is the full path of {req}?\n')
#     while not os.path.exists(parent_dir):
#         parent_dir = input('that directory doesn\'t exist. try again:\n')
#     progress[req]["parent_dir"] = parent_dir

#     # save progress to file, with empty episode field
#     save_progress(progress, progress_filename)
#     print(f'added {req}.')



def add_element(progress, req, progress_filename='progress.json'):
    if input(f'{req} isn\'t in the progress file... do you want to add it? [y]/n:\n').lower() == 'n':
        print('ok, see ya later!')
        exit()
    print(f'adding {req} to progress file...')
    progress["media"][req] = { "name":"", "episode":"" }

    result = gui(progress["parent_dir"], req)
    if result == None:
        print('ok bye!')
        exit(0)
    progress["media"][req]["name"] = result

    # save progress to file, with empty episode field
    save_progress(progress, progress_filename)
    print(f'added {req}.')


def load_progress(progress_filename='progress.json') -> dict:

    progress = {}
    # if file already exists
    if os.path.exists(progress_filename):
        with open(progress_filename, 'r') as f:
            progress = json.load(f)
        
        if 'parent_dir' not in progress or 'media' not in progress:
            print('file exists, but has bad format. recreating...')
            progress = _init_progress(progress_filename)
    
    # if file doesn't exist
    else:
        progress = _init_progress(progress_filename)

    return progress


if __name__ == '__main__':
    progress_filename = 'progress2.json'
    if len(sys.argv) != 2:
        print('expecting python progress.py <request>')
        exit(1)
    request = sys.argv[1]
    progress = load_progress(progress_filename)
    if request not in progress["media"]:
        add_element(progress, request, progress_filename)
    parent_dir = progress["parent_dir"]
    path = os.path.join(parent_dir, progress["media"][request]["name"])
    curr_ep = progress["media"][request]["episode"]
    print(path)
    print(f"'{curr_ep}'")

    print('success!')