import asyncio
import os
from typing import Dict, List
import time
import cv2
import numpy as np
import win32con
import win32gui
import win32ui
from pynput import keyboard
import yaml
import logging
import uuid
import hashlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

with open('resources/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

record_none = config.get('screenshot_unpressed', False)

def screen_shot(hwnd: int) -> np.ndarray:
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    width, height = right - left, bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (left, top), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    img_array = np.frombuffer(bmpstr, np.uint8).reshape(bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return img_array

def get_key_combo(key_states: Dict[str, bool]) -> str:
    direction = get_direction(key_states)
    actions = get_action(key_states)
    
    combo = [direction] if direction != 'none' else []
    combo.extend(actions)
    
    combo = combo[:2]  # Limit to at most 2 elements
    
    return '+'.join(combo) if combo else 'none'

def get_direction(key_states: Dict[str, bool]) -> str:
    pressed_keys = ''.join(sorted([k for k, v in key_states.items() if v and k in 'wasd']))
    return config['directions'].get(pressed_keys, 'none')

def get_action(key_states: Dict[str, bool]) -> List[str]:
    return [config['actions'][k] for k in config['action_priority'] if key_states.get(k, False)][:2]

class KeyLogger:
    def __init__(self):
        self.key_states = {k: False for k in config['keys']}
        self.running = True
        self.paused = False
        self.save_dir = config['save_dir']
        os.makedirs(self.save_dir, exist_ok=True)
        self.prev_time = time.perf_counter()
        self.fps = 0
        self.frame_count = 0

    def on_press(self, key):
        try:
            k = key.char
            if k in self.key_states:
                self.key_states[k] = True
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            k = key.char
            if k in self.key_states:
                self.key_states[k] = False
        except AttributeError:
            pass

        if key == keyboard.Key.esc:
            self.running = False
            self.paused = True
            return False

    def generate_unique_name(self, key_combo: str, img: np.ndarray) -> str:
        unique_id = uuid.uuid4()
        img_hash = hashlib.sha256(img.tobytes()).hexdigest()[:16]
        timestamp = int(time.time() * 1000)
        unique_name = f"{key_combo}_{unique_id}_{img_hash}_{timestamp}.jpg"
        return unique_name

    def save_image(self, img: np.ndarray, key_combo: str) -> str:
        folder_path = os.path.join(self.save_dir, key_combo.split('+')[-1] if '+' in key_combo else key_combo)
        os.makedirs(folder_path, exist_ok=True)
        
        if key_combo == 'none' and not record_none:
            return None
        
        unique_name = self.generate_unique_name(key_combo, img)
        img_path = os.path.join(folder_path, unique_name)
        
        try:
            if cv2.imwrite(img_path, img, [cv2.IMWRITE_JPEG_QUALITY, 85]):
                logging.info(f"Saved: {img_path}")
                return img_path
            else:
                logging.error(f"Error saving image: {img_path}")
                return None
        except Exception as e:
            logging.error(f"Error saving image: {e}")
            return None

    async def capture_loop(self):
        hwnd = win32gui.FindWindow(None, config['window_name'])
        if not hwnd:
            logging.error(f"{config['window_name']} window not found")
            return

        while self.running:
            key_combo = get_key_combo(self.key_states)
            img = screen_shot(hwnd)
            self.save_image(img, key_combo)
                
            if config['fps_enabled']:
                self.frame_count += 1
                curr_time = time.perf_counter()
                if curr_time - self.prev_time >= 1:
                    self.fps = self.frame_count / (curr_time - self.prev_time)
                    self.frame_count = 0
                    self.prev_time = curr_time
                
                display_img = img.copy()
                cv2.putText(display_img, f'FPS: {self.fps:.0f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                cv2.putText(display_img, f'Keys: {key_combo}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                cv2.imshow('NeuroNeon Eyes', display_img)
                
                if cv2.waitKey(1) & 0xFF == 27:
                    cv2.destroyAllWindows()
                    break

            await asyncio.sleep(0.01)  # Small delay to reduce CPU usage

    async def run(self):
        await asyncio.sleep(8)
        print('Starting capture of images')
        while True:
            self.running = True
            self.paused = False
            
            capture_task = asyncio.create_task(self.capture_loop())

            with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                await capture_task
                listener.join()

            logging.info("Script paused. Press Enter to start a new loop or 'q' to quit.")
            user_input = input().strip().lower()
            if user_input == 'q':
                break
            elif user_input == '':
                logging.info("Starting new loop...")
                await asyncio.sleep(7)  # 7 second delay before starting new loop
            else:
                logging.info("Invalid input. Press Enter to start a new loop or 'q' to quit.")

if __name__ == "__main__":
    keylogger = KeyLogger()
    asyncio.run(keylogger.run())
