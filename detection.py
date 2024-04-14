import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(filename='ransomware_detection.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

class RansomwareDetectionHandler(FileSystemEventHandler):
    def __init__(self):
        self.file_access_log = pd.DataFrame(columns=['timestamp', 'file_path', 'event_type'])
        self.time_window = timedelta(minutes=1)  
        super().__init__()

    def on_modified(self, event):
        if not event.is_directory:
            self.log_event(event.src_path, 'modified')
    
    def on_created(self, event):
        if not event.is_directory:     
            self.log_event(event.src_path, 'created')

    def log_event(self, path, event_type):
        now = datetime.now()
        new_event = pd.DataFrame({'timestamp': [now], 'file_path': [path], 'event_type': [event_type]})
        self.file_access_log = pd.concat([self.file_access_log, new_event], ignore_index=True)
        self.detect_anomaly(now)

    def detect_anomaly(self, current_time):
        recent_events = self.file_access_log[self.file_access_log['timestamp'] > current_time - self.time_window]
        high_freq_activities = recent_events.groupby('file_path').size()
        high_freq_activities = high_freq_activities[high_freq_activities > 10]  # More than 10 modifications/creations per minute

        encrypted_files = recent_events[recent_events['file_path'].str.endswith('.enc')]

        if not high_freq_activities.empty or not encrypted_files.empty:
            message = "Potential ransomware activity detected:"
            if not high_freq_activities.empty:
                message += f"\nHigh frequency of file operations:\n{high_freq_activities}"
            if not encrypted_files.empty:
                message += f"\nFiles with suspicious extensions detected:\n{encrypted_files}"
            
            print(message)
            logging.info(message)  

# Setup the observer and event handler
path_to_monitor = "./critical"
event_handler = RansomwareDetectionHandler()
observer = Observer()
observer.schedule(event_handler, path_to_monitor, recursive=True)

# Start the monitoring
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
