import os
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOG_FILE = "/home/ubuntu/bsm/logs/changes.json"

class ChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        self.log_event("created", event)

    def on_deleted(self, event):
        self.log_event("deleted", event)

    def on_modified(self, event):
        self.log_event("modified", event)

    def log_event(self, action, event):
        if not event.is_directory:
            data = {
                "event": action,
                "file": event.src_path,
                "timestamp": datetime.now().isoformat()
            }
            with open(LOG_FILE, "a") as log_file:
                log_file.write(json.dumps(data) + "\n")

if __name__ == "__main__":
    path_to_watch = "/home/ubuntu/bsm/test"
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()  # Log dosyasını oluştur
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=True)
    observer.start()

    print(f"Watching directory: {path_to_watch}")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
