import threading
import time

import cv2
import numpy as np
import torch
import win32con
import win32gui
import win32ui
import yaml
from pynput.keyboard import Key
from ultralytics import YOLO

# Load configuration file
with open('resources/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    press_time = config['press_timing']

gpu = torch.cuda.is_available()

print('Checking PyTorch and CUDA setup...')
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {gpu}')

model = YOLO('resources/models/best.pt', task='classify')
model.cuda() if gpu else model.cpu()
model.predict('resources/others/Capture.JPG', imgsz=224)

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
    
    """def press_hypercharge(self):
        print('pressing the hypercharge button')
        self.send_keys_to_window(['r'], 0.05)"""

    def exit_match(self):
        print('leaving the match')
        self.send_keys_to_window(['u'], press_time['short'])
        for _ in range(3):
            self.send_keys_to_window(['q'], press_time['short'])
            time.sleep(3)
        
def create_thread(processes):
    for process in processes:
        thread = threading.Thread(target=process)
        threads.append(thread)
        thread.start()

def send_keys_loop():
    control = ControllerInstance(config['instance_name'])
    combo_keys = {
        0: control.auto_attack,
        1: control.auto_super_attack,
        2: control.exit_match,
        3: control.move_down,
        4: control.press_gadget,
        5: control.move_left,
        6: [control.move_down, control.move_left],
        7: [control.move_down, control.move_right],
        8: control.move_right,
        9: control.move_up,
        10: [control.move_up, control.move_left],
        11: [control.move_up, control.move_right],
    }

    control.press_gadget()
    time.sleep(7.5)
    
    while True:
        results = model(control.screen_shot())
        for result in results:
            best_action = result.probs.top1
            break
        
        action = combo_keys.get(best_action)
        if action:
            if isinstance(action, list):
                create_thread(action)
                for thread in threads: # Clean up all threads
                    thread.join()
            else:
                action()
        
        time.sleep(0.01) # Adjust delay to prevent spamming and to allow proper threading

if __name__ == "__main__":
    send_keys_loop()
