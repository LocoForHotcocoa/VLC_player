import os
import curses
from fuzzywuzzy import fuzz, process
import time

# ima be real, most of this is from chatgpt.
# just wanted to mess around with fuzzyfinder

# Function to get a list of files in a directory
def get_files_in_directory(directory):
    return os.listdir(directory)

# Curses app for fuzzy file finder
def fuzzy_finder(stdscr, directory, query) -> (str | None):
    curses.curs_set(1)  # Enable cursor for typing
    curses.start_color()
    curses.use_default_colors() # use existing terminal color theme
    files = get_files_in_directory(directory)
    selected = 0        # Selected item index

    while True:
        stdscr.clear()
        
        # Display instructions
        stdscr.addstr(0, 0, "Type to search, UP/DOWN to navigate, ENTER to select, ESC to quit")

        # Show current query
        stdscr.addstr(1, 0, f"Search: {query}")
        
        # Perform fuzzy matching and get top 5 results
        if query:
            matches = process.extract(query, files, limit=5, scorer=fuzz.partial_ratio)
        else:
            matches = [(f, 100) for f in files]  # Display top files without filtering

        # Display matches
        for i, (filename, score) in enumerate(matches):
            if i == selected:
                stdscr.addstr(i + 2, 0, f"{filename} - {score}", curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 0, f"{filename} - {score}")

        # Capture user input
        key = stdscr.getch()

        # Handle input
        if key == curses.KEY_DOWN:
            selected = (selected + 1) % len(matches)
        elif key == curses.KEY_UP:
            selected = (selected - 1) % len(matches)
        elif key in (10, 13) or key == curses.KEY_ENTER:  # Enter key
            stdscr.addstr(15, 0, f"Selected: {matches[selected][0]}")
            stdscr.refresh()
            time.sleep(1)
            return matches[selected][0]
        elif key == 27:  # ESC key
            stdscr.addstr(15, 0, "okay, bye.")
            stdscr.refresh()
            time.sleep(0.5)
            return None
        elif key == curses.KEY_BACKSPACE or key == 127:
            query = query[:-1]
        elif 32 <= key <= 126:
            query += chr(key)

# Wrapper for curses
def main():
    directory = "/Users/matthewbradley/Movies/torrents"  # Set to the directory you want to search
    output = curses.wrapper(fuzzy_finder, directory, 'test')
    print(output)

def gui(directory: str, query: str):
    return curses.wrapper(fuzzy_finder, directory, query)

if __name__ == "__main__":
    main()
