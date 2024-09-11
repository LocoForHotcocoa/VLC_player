import subprocess
import sys

vlc_process = None

def run_vlc(playlist_file='playlist.m3u'):
	global vlc_process
	# vlc playlist.m3u --extraintf http --http-port 8080 --http-password admin
	# runs this command in new subprocess, with no output or error messages (I think my VLC is a little buggy)
	vlc_process = subprocess.Popen(['vlc', playlist_file, '--extraintf', 'http', '--http-port', '8080', '--http-password', 'admin'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

	vlc_process.wait()

def stop_vlc():
	global vlc_process
	print("quiting vlc...")

	if vlc_process is not None:
		vlc_process.terminate()

	sys.exit(0)