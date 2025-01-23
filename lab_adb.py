import subprocess
import cv2
import numpy as np

class Simulator:
    def __init__(self, name, device_id, match_threshold=0.8):
        self.name = name
        self.device_id = device_id
        self.match_threshold = match_threshold  # 默認匹配閾值

    # 截取屏幕畫面
    def capture_screen(self):
        command = f'adb -s {self.device_id} exec-out screencap -p > screenshot.png'
        subprocess.run(command, shell=True)
        image = cv2.imread('screenshot.png')
        if image is None:
            raise ValueError("Failed to capture screen or read the screenshot file.")
        return image

    # 模擬點擊
    def tap_screen(self, x, y):
        command = f'adb -s {self.device_id} shell input tap {x} {y}'
        subprocess.run(command, shell=True)

    # 查找並點擊圖標
    def find_and_tap_icon(self, icon_path):
        # 截取屏幕
        screen = self.capture_screen()
        
        # 讀取圖標模板
        icon = cv2.imread(icon_path)
        if icon is None:
            raise ValueError(f"Failed to read icon file: {icon_path}")
        
        # 如果圖像是彩色的，轉換為灰度
        if len(icon.shape) == 3:
            icon_gray = cv2.cvtColor(icon, cv2.COLOR_BGR2GRAY)
        else:
            icon_gray = icon  # 如果已經是灰度圖像，直接使用

        # 使用灰度圖像進行模板匹配，減少顏色差異影響
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(screen_gray, icon_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        # 使用指定的匹配閾值進行比較
        if max_val > self.match_threshold:
            x, y = max_loc
            print(f"Icon found at: {x}, {y}")
            # 點擊圖標
            self.tap_screen(x + 10, y + 10)  # 加 10 是為了避免點擊到圖片的邊緣
        else:
            print("Icon not found")

# 設置不同遊戲的閾值
blhx_simulator = Simulator(name="blhx", device_id="emulator-5554", match_threshold=0.53)
arknights_simulator = Simulator(name="arknights", device_id="emulator-5556", match_threshold=0.8)

# 測試查找並點擊圖標
blhx_simulator.find_and_tap_icon('blhx_icon.png')
arknights_simulator.tap_screen(1200, 220)
