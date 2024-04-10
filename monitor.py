import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime  # Import datetime module

class Watcher:
    DIRECTORY_TO_WATCH = "../critical"

    def __init__(self):
        self.observer = Observer()

    def run(self): 
        print("Monitoring...")
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:  # It's better to specifically catch KeyboardInterrupt
            self.observer.stop()
            print("Observer Stopped")
        self.observer.join()
 

class Handler(FileSystemEventHandler):
    LOG_FILE = "event_log.txt"  # Define the log file name

    @staticmethod
    def log_event(message):
        """Write the event message to the log file with a timestamp."""
        with open(Handler.LOG_FILE, "a") as log_file:  # Open file in append mode
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp} - {message}\n")

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        message = ""
        if event.event_type == 'created':
            # When a file is created
            message = f"Received created event - {event.src_path}."
            print(f"Received created event - {event.src_path}.")
        elif event.event_type == 'modified':
            # When a file is modified
            message = f"Received modified event - {event.src_path}."
            print(f"Received modified event - {event.src_path}.")
        elif event.event_type == 'deleted':
            # When a file is deleted
            message = f"Received deleted event - {event.src_path}."
            print(f"Received deleted event - {event.src_path}.")
        if message:
            Handler.log_event(message)


if __name__ == "__main__":
    w = Watcher()
    w.run()
