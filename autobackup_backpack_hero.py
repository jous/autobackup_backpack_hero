# 
# 1) To install:
# 
# python.exe -m pip install --upgrade pip
# pip install watchdog
# pip install pypiwin32
# 
# 2) To configure, edit lines 15 and 16 below to point to your 7zip and game install executables.
#
# 3) To run the game and autobackupper:
#
# python autobackup_backpack_hero.py
#

exec_7zip = r"C:\Program Files\7-Zip\7z.exe"
exec_game = r"C:\Games\Backpack Hero\Backpack Hero.exe"

import os # environment variables, paths, rename, exit
home_folder = os.environ["USERPROFILE"] # C:\Users\[your_username]
base_folder = home_folder + r"\AppData\LocalLow\TheJaspel\Backpack Hero"
write_backups_to = home_folder + r"\AppData\LocalLow\TheJaspel\Backpack Hero\backups"

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time # for sleep()
from datetime import datetime # gets current time
import subprocess # calling 7zip and tasklist
import logging # combined screen+log writing

import win32event # for checking that we run only one autobackupper at a time
import win32api
from winerror import ERROR_ALREADY_EXISTS

# start the game for convenience
subprocess.Popen([exec_game])

# lets not run multiple autobackuppers
mutex = win32event.CreateMutex(None, False, "autobackup_backpack_hero")
last_error = win32api.GetLastError()

if last_error == ERROR_ALREADY_EXISTS:
   print("Autobackup already running")
   os._exit(0)

# outputs to file and stdout when using loglevel INFO or more serious
handlers = [logging.FileHandler(base_folder + r"\autobackup_backpack_hero.log"), logging.StreamHandler()]
logging.basicConfig(level = logging.INFO, format = ' %(message)s', handlers = handlers)


def string_now():
    return datetime.today().strftime("%y%m%d_%H%M%S")

def get_timestamp():
    now = datetime.now()
    return datetime.timestamp(now)

def get_filename(in_string):
    return in_string.split("\\")[-1]

def allowed_extension(in_string):
    return in_string[-4:] in [".png", ".sav"]

def wait_for_file_fully_written(in_filename):
    file_size = -1
    try:
        while file_size != os.path.getsize(in_filename):
            file_size = os.path.getsize(in_filename)
            time.sleep(0.1)
    except:
        return True

def wait_for_open_file_pointers(in_filename):
    file_done = False
    while not file_done:
        try:
            os.rename(in_filename, in_filename)
            file_done = True
        except:
            return True

def on_modified(event):

    input_file = event.src_path

    # we only want certain files
    if allowed_extension(input_file):

        # lets speak that we only want get change notifications
        if not hasattr(on_modified, get_filename(input_file)):
            setattr(on_modified, get_filename(input_file), 0)

        # sanitycheck, because we will get multiple notifications of the same file.
        lastrun = getattr(on_modified, get_filename(input_file))
        if lastrun < get_timestamp() - 3:

            try:
                # we don't want ancient notification (>10min)
                save_last_modified = os.path.getmtime(input_file)
                if save_last_modified > get_timestamp() - 600:

                    setattr(on_modified, get_filename(input_file), get_timestamp())

                    # just play cool until the file is fully written
                    wait_for_file_fully_written(input_file)

                    # lets just check one more time that no other process is accessing the file
                    wait_for_open_file_pointers(input_file)

                    extra = "_" + get_filename(input_file).strip().replace("bph", "").replace("Mode", "")[0:-4]
                    output_file = write_backups_to + "\\" + string_now() + extra + ".zip"
                    log_string = "Adding " + get_filename(input_file).rjust(29) + " to " + output_file.replace(base_folder, ".").ljust(45)

                    result = subprocess.run([exec_7zip, "a", "-tzip", output_file, input_file], capture_output = True, text = True)
                    if result.returncode == 0:
                        stdout_lines = result.stdout.split("\n")
                        parts = stdout_lines[-3].split("(") # Archive size: ????? bytes (?? KiB)
                        logging.info(log_string + ("(" + parts[-1]).rjust(9))
                    else:
                        logging.info(log_string + result.stderr)
                else:
                    # print(get_filename(input_file) + " was too old! 10min allowed, but got %.1fmin" % ((get_timestamp() - save_last_modified) / 60))
                    pass
            except FileNotFoundError:
                logging.info("File " + get_filename(input_file), "vanished when trying to read the modification time!")
                pass
        else:
            # print(get_filename(input_file) + " was too new! Only %.4f seconds since last notification." % (get_timestamp() - lastrun))
            pass
    else:
        # print("not allowed file: " + get_filename(input_file))
        pass



def process_exists(process_name):
    call = "TASKLIST", "/FI", "imagename eq %s" % process_name
    result = subprocess.run(call, capture_output = True, text = True)
    return result.stdout.count("\n") > 1 # if we got more than one line, the process is running very much indeeed.



if __name__ == "__main__":

    logging.info("Started at " + string_now())
    logging.info("Watching folder \"" + base_folder + "\"")

    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = True # do not care about directories
    case_sensitive = False
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_modified = on_modified
    path = base_folder
    go_recursively = False # do not check inside subfolders
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    my_observer.start()
    try:
        while True:
            time.sleep(1)
            # if the game is not running, why bother?
            if not process_exists("Backpack Hero.exe"):
               os._exit(0)

    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
