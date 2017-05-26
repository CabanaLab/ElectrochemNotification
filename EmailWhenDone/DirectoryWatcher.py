# A script that checks to see when the 'log' file disappears from the 'Data' folder of the C:/DATA drive
# This script was written by Mike Plews (2015). Email me with any questions!

import time
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler
import os, sys, atexit

import message_preparation as mp, localsettings as ls

import logging

# Setup logging
logging.basicConfig(filename='/var/log/EmailWhenDone.log', level=logging.DEBUG)
log = logging.getLogger('DirectoryWatcher')
# log = logging.setFormatter(logging.Formatter("%(asctime)s;%(levelname)s;%(message)s","%Y-%m-%d %H:%M:%S"))

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.mpl"]

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print (event.src_path + ' ' + event.event_type)
        import send_notification as sn
        filename = event.src_path.encode('utf-8').replace(b'\\',b'/').replace(b'\x00', b'/')
        filename = filename.decode().rstrip('.mpl')
        log.debug("File %s deleted", filename)
        user_info = mp.find_user(filename)
        if is_valid(filename):  # Checks to see if the filename is valid
            log.debug("Filename %s is VALID", filename)
            if user_info[0]:
                log.debug("Sending note to %s(%s)", user_info[0], user_info[1])
                sn.notify(user_info[0], user_info[1], filename)
            else:
                log.debug("No matching email address for %s", filename)
        else:
            log.debug("Filename %s is INVALID", filename)

    def on_deleted(self, event):
        self.process(event)
        
    def on_created(self, event):
        print (event.src_path + ' ' + event.event_type)

    def on_modified(self, event):
        print (event.src_path + ' ' + event.event_type)

    def is_valid(filename, settingsfile=ls):
        for string in settingsfile.ignore_list:
            if string in filename:
                return False
        return True
        
if __name__ == '__main__':
    args = sys.argv[1:]
    #args = r'D://'
    observer = Observer()
    observer.schedule(MyHandler(), recursive = True, path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        #mp.message_me("The script stopped, probably a KeyboardInterrupt")

    observer.join()
    atexit.register(mp.message_me("Something happened to make the script exit. Not sure what it is. Go invesitgate."))
