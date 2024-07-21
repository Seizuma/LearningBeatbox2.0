import lib.config_generator
from config.config import *
from lib.listen import start_nonblocking_listen_loop, load_running_classifier, stop_listening as stop_listening_func
from lib.mode_switcher import ModeSwitcher
import sys, getopt
import lib.ipc_manager as ipc_manager
import threading

def start_recording():
    if ipc_manager.getParrotState() != "running":
        classifier = load_running_classifier(DEFAULT_CLF_FILE)
        mode_switcher = ModeSwitcher(INPUT_TESTING_MODE)
        ipc_manager.requestParrotState("running")
        ipc_manager.setParrotState("running")
        mode_switcher.switchMode(STARTING_MODE)

        start_nonblocking_listen_loop(classifier, mode_switcher, SAVE_REPLAY_DURING_PLAY, SAVE_FILES_DURING_PLAY, -1, True)

def stop_listening():
    stop_listening_func()
    ipc_manager.setParrotState("not_running")

def main(argv):
    if ipc_manager.getParrotState() != "not_running":
        print("Parrot might already be running somewhere, stopping that instance...")
        ipc_manager.requestParrotState("stopped")

    opts, args = getopt.getopt(argv, "tc:m:", ["testing:", "classifier=", "mode="])
       
    for opt, arg in opts:
        if opt in ("-c", "--classifier"):
            global DEFAULT_CLF_FILE
            DEFAULT_CLF_FILE = arg
        elif opt in ("-t", "--testing"):
            global INPUT_TESTING_MODE
            INPUT_TESTING_MODE = True
            print("Enabling testing mode - No inputs will be sent to the keyboard and mouse!")
        elif opt in ("-m", "--mode"):
            global STARTING_MODE
            STARTING_MODE = arg

if __name__ == "__main__":
   main(sys.argv[1:])
