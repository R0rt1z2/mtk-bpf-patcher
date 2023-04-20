import os
import re

VERBOSITY_LEVELS = {
    0: "\033[0;34m[?]",
    1: "\033[0;33m[!]",
    2: "\033[0;31m[x]",
    3: "\033[0;32m[+]",
    4: "\033[0;36m[~]" # This is used for debugging.
}

class Logger:
    '''Initializes the logger.'''
    def __init__(self, log_file = None, debug = False):
        self.log_handle = None
        self.debug = debug

        if log_file:
            self.log_file = os.path.abspath(log_file)
            try:
                self.log_handle = open(self.log_file, "a")
            except FileNotFoundError:
                pass  # This is fine, since that means the file doesn't exist yet.
            except OSError:
                print("Error: could not open log file")

    '''Destructor for the logger.'''
    def __del__(self):
        if self.log_handle:
            try:
                self.log_handle.close()
            except OSError:
                exit("FATAL: could not close log file!")

    '''Logs a message to the console and/or log file.'''
    def log(self, verbosity, msg):
        message = f"{VERBOSITY_LEVELS[verbosity]} {msg}\033[0m"
        if verbosity == 4 and not self.debug: return
        print(message)
        if self.log_handle:
            # Remove ANSI escape codes from the message before writing to the log file.
            self.log_handle.write(re.sub("\033\[[0-9;]*m", "", message) + "\n")

        # If the message is an error, exit.
        if verbosity == 2: exit(1)

    '''Prints our fancy banner.'''
    def print_banner(self):
        print("\033[0;35m")
        print("  _            __               _       _               ")
        print(" | |__  _ __  / _|  _ __   __ _| |_ ___| |__   ___ _ __ ")
        print(" | '_ \| '_ \| |_  | '_ \ / _` | __/ __| '_ \ / _ \ '__|")
        print(" | |_) | |_) |  _| | |_) | (_| | || (__| | | |  __/ |   ")
        print(" |_.__/| .__/|_|   | .__/ \__,_|\__\___|_| |_|\___|_|   ")
        print("       |_|   |_|   |_| \033[0;31mmade by @R0rt1z2       ")
        print("\033[0m")