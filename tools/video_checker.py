import magic
import os

mime = magic.Magic(mime=True)

def is_video_file(path: str) -> bool:
    
    # check if it's not a directory first, then check if its a video file with python-magic module
    if os.path.isfile(path):
        if mime.from_file(path).find('video') != -1:
            return True
    
    return False
