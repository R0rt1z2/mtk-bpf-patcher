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
    def __init__(self, log_file = None, debug = False) -> None:
        '''
        Constructor for the logger.
        @param log_file: The log file to write to.
        @param debug: Whether to enable debug mode.
        return: None
        '''
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

    def __del__(self) -> None:
        '''
        Destructor for the logger.
        return: None
        '''
        if self.log_handle:
            try:
                self.log_handle.close()
            except OSError:
                exit("FATAL: could not close log file!")

    def log(self, verbosity, msg) -> None:
        '''
        Logs a message to the console and the log file.
        @param verbosity: The verbosity level of the message.
        @param msg: The message to log.
        return: None
        '''
        message = f"{VERBOSITY_LEVELS[verbosity]} {msg}\033[0m"
        if verbosity == 4 and not self.debug: return
        print(message)
        if self.log_handle:
            # Remove ANSI escape codes from the message before writing to the log file.
            self.log_handle.write(re.sub("\033\[[0-9;]*m", "", message) + "\n")

        # If the message is an error, exit.
        if verbosity == 2: exit(1)

    def print_banner(self) -> None:
        '''
        Prints the banner.
        return: None
        '''
        print("\033[0;35m")
        print("  _            __               _       _               ")
        print(" | |__  _ __  / _|  _ __   __ _| |_ ___| |__   ___ _ __ ")
        print(" | '_ \| '_ \| |_  | '_ \ / _` | __/ __| '_ \ / _ \ '__|")
        print(" | |_) | |_) |  _| | |_) | (_| | || (__| | | |  __/ |   ")
        print(" |_.__/| .__/|_|   | .__/ \__,_|\__\___|_| |_|\___|_|   ")
        print("       |_|   |_|   |_| \033[0;31mmade by @R0rt1z2       ")
        print("\033[0m")