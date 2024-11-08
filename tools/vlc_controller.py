import subprocess

vlc_process = None

def run_vlc(playlist_file: str) -> None:
	global vlc_process
	# vlc playlist.m3u --extraintf http --http-port 8080 --http-password admin
	# runs this command in new subprocess, with no output or error messages (I think my VLC is a little buggy)
	vlc_process = subprocess.Popen(['vlc', playlist_file, '--extraintf', 'http', '--http-port', '8080', '--http-password', 'admin'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

	vlc_process.wait()

def stop_vlc() -> None:
	global vlc_process
	print("\nquiting watch.py...")

	if vlc_process is not None:
		vlc_process.terminate()