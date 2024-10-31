# VLC Player

This integrates into VLC CLI to keep track of where you are in a series. Once you add a series to the program, it will save the name and current data in a json file.

I made this to practice command line scripting in python. It utilizes these packages:
- `subprocess`
- `threading`
- `requests`
- `signal`
- `json`
- `time`
- `sys`
- `os`
- `python-magic`

### First Time Use

```bash
python watch.py good_show
```
(you can use any title for your show)

Follow the instructions, making sure to include the full path of your series folder, and it will launch VLC automatically.

### Subsequent Use
```bash
python watch.py good_show
```
That's it! It should launch VLC and keep track from where you left off!

### quitting the app
you can exit the app gracefully by closing out of VLC or by pressing `ctrl+C` in the python interface.
