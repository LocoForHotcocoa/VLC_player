import subprocess

vlc_process = None

def run_vlc(playlist_file: str) -> None:
	global vlc_process
	
	# runs this command in new subprocess, with no output or error messages (I think my VLC is a little buggy)
	cmd = f'vlc {playlist_file} --extraintf http --http-port 8080 --http-password admin'
	vlc_process = subprocess.Popen([cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

	vlc_process.wait()

def stop_vlc() -> None:
	global vlc_process
	print("\nquiting watch.py...")

	if vlc_process is not None:
		vlc_process.terminate()
