import signal
import sys
from tools.vlc_controller import stop_vlc


def signal_handler(sig, frame):
    stop_vlc()

def setup_signal_handling():
    # Register the signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)