import sys
import os
import threading
import time

from tools.playlist import create_playlist
from tools.progress import add_element, load_progress, save_progress
from tools.signal_handler import setup_signal_handling
from tools.status_checker import check_vlc_status
from tools.vlc_controller import run_vlc

# main script -------------------------------------------------------------------------------------
#

# script explanation:
# progress file contains parent directory and current filename for each show
# 
#	- playlist is created, starts at whatever is in progress[request]["episode"]
#	- signal handling starts, waits for ctrl+c which will start the graceful quitting process; signal_handler.py
#	- main thread starts, the vlc subprocess; vlc_controller.py
#	- wait 2 seconds
#	- daemon thread starts, the status checker, which keeps track of current episode from http interface, and increments it when necessary;
#	  status_checker.py
#	- end script when ctrl+c is registered.

def main():
    
    
    # setup -----------------------------------------
    if (len(sys.argv) != 2):
        print("py watch.py <something to watch>")
        exit()

    # works from any cwd
    progress_file = os.path.join(sys.path[0], 'progress.json')
    playlist_file = os.path.join(sys.path[0], 'playlist.m3u')
    # parent_dir = '/Users/matthewbradley/Movies/torrents'

    check_interval = 10 # check status every x seconds
    
    # will check with progress file
    request = str(sys.argv[1])
    
    # Load progress from progress file, or initialize it if it doesn't exist
    progress = load_progress(progress_file)


    # if its a new show, add element and set curr_ep to ""
    if request not in progress["media"]:
        add_element(progress, request, progress_file)
    
    
    parent_dir = progress["parent_dir"]
    path = os.path.join(parent_dir, progress["media"][request]["name"])
    curr_ep = progress["media"][request]["episode"]

    # if new season, playlist will start from beginning. writes to playlist file
    playlist = create_playlist(path, curr_ep, playlist_file)

    # main logic ------------------------------------

    # set up ctrl+c signal watch
    setup_signal_handling()

    # start vlc thread
    vlc_thread = threading.Thread(target=run_vlc, args=(playlist_file,))
    vlc_thread.start()

    # delay to get everything started
    time.sleep(3)

    # start status thread
    status_thread = threading.Thread(target=check_vlc_status, args=(progress, request, playlist, check_interval), daemon=True)
    status_thread.start()

    vlc_thread.join()
    
    # when everything is done, and vlc process is terminated, save progress to progress file
    save_progress(progress, progress_file)
    print("see ya later!")

if __name__ == '__main__':
    main()
