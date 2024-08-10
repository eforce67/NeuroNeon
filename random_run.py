import threading
import time
import secrets

import cv2
import yaml
import numpy as np
import win32con
import win32gui
import win32ui

# Load configuration file
with open('resources/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    press_time = config['press_timing']
    
threads = []

class ControllerInstance:
    def __init__(self, window_name):
        hwndMain = win32gui.FindWindow(None, window_name)
        self.hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)

    def screen_shot(self):
        left, top, right, bot = win32gui.GetClientRect(self.hwndChild)
        width, height = right - left, bot - top

        hwndDC = win32gui.GetWindowDC(self.hwndChild)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (left, top), win32con.SRCCOPY)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        img_array = cv2.cvtColor(np.frombuffer(bmpstr, np.uint8).reshape(bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4), cv2.COLOR_BGRA2BGR)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwndChild, hwndDC)
        
        return img_array

    def send_keys_to_window(self, keys, duration:float=press_time['default']):
        for key in keys:
            if isinstance(key, str):
                vk_code = ord(key.upper())
            else:
                vk_code = key.value.vk
            win32gui.PostMessage(self.hwndChild, win32con.WM_KEYDOWN, vk_code, 0)
            time.sleep(duration)  # Adjust delay to prevent spamming
            win32gui.PostMessage(self.hwndChild, win32con.WM_KEYUP, vk_code, 0)
            time.sleep(0.05)  # Adjust delay to prevent spamming

    """def send_clicks_to_window(self, x, y):
        lParam = win32api.MAKELONG(x, y)
        win32api.PostMessage(hwndChild, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(1.5)
        win32api.PostMessage(hwndChild, win32con.WM_LBUTTONUP, None, lParam)
        time.sleep(0.05)"""

    def move_up(self):
        print('moving up')
        self.send_keys_to_window(['w'])

    def move_down(self):
        print('moving down')
        self.send_keys_to_window(['s'])

    def move_left(self):
        print('moving left')
        self.send_keys_to_window(['a'])

    def move_right(self):
        print('moving right')
        self.send_keys_to_window(['d'])

    def press_gadget(self):
        self.send_keys_to_window(['q'], press_time['short'])
    
    def auto_attack(self):
        self.send_keys_to_window(['e'], press_time['short'])
    
    def auto_super_attack(self):
        self.send_keys_to_window(['f'], press_time['short'])
    
    def press_hypercharge(self):
        print('pressing the hypercharge button')
        self.send_keys_to_window(['r'], press_time['short'])
    
    """def manual_aim(self, x, y):
        # failed manual aim logic, more work and test must be done.
        create_thread(processes=[send_clicks_to_window(x, y), hold_aim])"""

def create_thread(processes):
    for process in processes:
        thread = threading.Thread(target=process)
        threads.append(thread)
        thread.start()

def send_keys_loop():
    control = ControllerInstance("LDPlayer")
    combo_keys = {
        "auto_attack": control.auto_attack,
        "auto_super_attack": control.auto_super_attack,
        "down": control.move_down,
        "gadget": control.press_gadget,
        "left": control.move_left,
        "lower_left": [control.move_down, control.move_left],
        "lower_right": [control.move_down, control.move_right],
        "right": control.move_right,
        "up": control.move_up,
        "upper_right": [control.move_up, control.move_right],
        "upper_left": [control.move_up, control.move_left],
    }
    control.press_gadget()
    time.sleep(7.5)
    
    while True:
        cv2.imwrite('screen_player.png', control.screen_shot())  # Take a photo of the current window
        decided_action = secrets.choice(list(combo_keys))
        action = combo_keys[decided_action]
        
        if isinstance(action, list):
            create_thread(processes=action)
            for thread in threads: # Cleaning up all threads
                thread.join()
        else:
            action()
            
        time.sleep(0.01)  # Adjust delay to prevent spamming and to allow proper threading

if __name__ == "__main__":
    send_keys_loop()
