from tools.video_checker import is_video_file
import os

def create_playlist(parent_dir: str, curr_episode: str, playlist_filename='playlist.m3u') -> list[str]:

	# gives ordered list of all video files in the current directory
	playlist = [file for file in sorted(os.listdir(parent_dir)) if is_video_file(os.path.join(parent_dir,file))]

	# takes out all episodes before current epsiode. if no episode is declared, then it lists full playlist
	if curr_episode != '':
		current_index = playlist.index(curr_episode)
		playlist = playlist[current_index:]

	# write this to a file
	write_to_playlist_file(playlist, parent_dir, playlist_filename)

	# also needs to return the list, used to update current episode
	return playlist


def write_to_playlist_file(playlist: list[str], parent_dir: str, playlist_filename='playlist.m3u') -> None:
	# writes 'parent_dir/episode' to playlist_file
	with open(playlist_filename, 'w') as f:
		for ep in playlist:
			f.write(f'{os.path.join(parent_dir, ep)}\n')

def get_next_episode(playlist: list[str], curr_episode: str):
	current_index = playlist.index(curr_episode)
	# if current index is at the end of the playlist, then the season is over!
	if current_index == len(playlist) - 1:
		return None
	
	return playlist[current_index + 1]