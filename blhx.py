import time
import subprocess
import cv2
import numpy as np
import datetime



class Simulator:

    

    def __init__(self, name, device_id, match_threshold=0.8,tap_delay=1.5,dbg_print = 1):
        self.name = name
        self.device_id = device_id
        self.match_threshold = match_threshold  # 默認匹配閾值
        self.tap_delay = tap_delay
        self.dbg_print = dbg_print

    # 截取屏幕畫面
    def capture_screen(self, x=None, y=None, width=None, height=None):
        command = f'adb -s {self.device_id} exec-out screencap -p > screenshot.png'
        subprocess.run(command, shell=True)
        image = cv2.imread('screenshot.png')
        if image is None:
            raise ValueError("Failed to capture screen or read the screenshot file.")
        
        if x is not None and y is not None and width is not None and height is not None:
            image = image[y:y+height, x:x+width]

        return image

    def error_handler(self , event):
        if(event == 0):
            print("[Error handler] : x and y eq 0 error")
        elif(event == 1):
            print("[Error handler] : x < 0 or y < 0 error")
        exit()

    # 模擬點擊
    def tap_screen(self, x, y):
        if x==0 and y==0:
            self.error_handler(0)
        elif x<0 or y<0:
            self.error_handler(1)
        command = f'adb -s {self.device_id} shell input tap {x} {y}'
        subprocess.run(command, shell=True)
        time.sleep(self.tap_delay)

    


    # 查找並點擊圖標
    def find_and_tap_icon(self, icon_path):
        # 截取屏幕
        screen = self.capture_screen()
        
        # 讀取圖標模板
        icon = cv2.imread(icon_path)
        if icon is None:
            raise ValueError(f"Failed to read icon file: {icon_path}")
        
        # 如果需要使用彩色匹配
      
        # 灰度匹配
        icon_gray = cv2.cvtColor(icon, cv2.COLOR_BGR2GRAY)
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screen_gray, icon_gray, cv2.TM_CCOEFF_NORMED)

        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        # 使用指定的匹配閾值進行比較
        if max_val > self.match_threshold:
            x, y = max_loc
            print(f"Icon found at: {x}, {y}")

            if self.dbg_print :
                screenshot = screen
                template = icon
                threshold = self.match_threshold
                locations = np.where(result >= threshold)
                # 畫出匹配的位置
                for loc in zip(*locations[::-1]):
                    cv2.rectangle(screenshot, loc, (loc[0] + template.shape[1], loc[1] + template.shape[0]), (0, 255, 0), 2)
                # 顯示結果
                cv2.imshow('Detected', screenshot)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            # 點擊圖標
            self.tap_screen(x + 10, y + 10)  # 加 10 是為了避免點擊到圖片的邊緣
            return 1
        else:
            print("Icon not found")
            return 0
        
    # def find_icon(self, icon_path,limit_x=None, limit_y=None):
    #      # 截取屏幕
    #     screen = self.capture_screen()
        
    #     # 讀取圖標模板
    #     icon = cv2.imread(icon_path)
    #     if icon is None:
    #         raise ValueError(f"Failed to read icon file: {icon_path}")
        
    #     # 如果需要使用彩色匹配
      
    #     # 灰度匹配
    #     icon_gray = cv2.cvtColor(icon, cv2.COLOR_BGR2GRAY)
    #     screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    #     result = cv2.matchTemplate(screen_gray, icon_gray, cv2.TM_CCOEFF_NORMED)

    #     _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
    #     # 使用指定的匹配閾值進行比較
    #     if max_val > self.match_threshold:
    #         x, y = max_loc
    #         print(f"Icon found at: {x}, {y}")

    #         if Simulator.dbg_print :
    #             screenshot = screen
    #             template = icon
    #             threshold = self.match_threshold
    #             locations = np.where(result >= threshold)
    #             # 畫出匹配的位置
    #             for loc in zip(*locations[::-1]):
    #                 cv2.rectangle(screenshot, loc, (loc[0] + template.shape[1], loc[1] + template.shape[0]), (0, 255, 0), 2)
    #             # 顯示結果
    #             cv2.imshow('Detected', screenshot)
    #             cv2.waitKey(0)
    #             cv2.destroyAllWindows()
    #         return x,y
    #     else:
    #         print("Icon not found")
    #         return 0,0

    def find_icon(self, icon_path, limit_x=None, limit_y=None,dbg_print=False):
        # 截取屏幕
        screen = self.capture_screen()
        
        # 讀取圖標模板
        icon = cv2.imread(icon_path)
        if icon is None:
            raise ValueError(f"Failed to read icon file: {icon_path}")
        
        # 灰度匹配
        icon_gray = cv2.cvtColor(icon, cv2.COLOR_BGR2GRAY)
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screen_gray, icon_gray, cv2.TM_CCOEFF_NORMED)

        threshold = self.match_threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))  # 轉換為 (x, y) 座標對

        if locations:
            # 過濾符合限制的匹配位置
            filtered_locations = [(x, y) for x, y in locations if (limit_x is None or x >= limit_x) and (limit_y is None or y >= limit_y)]
            
            if filtered_locations:
                # 找到匹配值最大的位置
                best_match_idx = np.argmax([result[y, x] for x, y in filtered_locations])
                best_match = filtered_locations[best_match_idx]
                x, y = best_match

                print(f"Icon found at: {x}, {y} with value: {result[y, x]}")

                if dbg_print:
                    screenshot = screen
                    for loc in filtered_locations:
                        cv2.rectangle(screenshot, loc, (loc[0] + icon.shape[1], loc[1] + icon.shape[0]), (0, 255, 0), 2)

                    cv2.rectangle(screenshot, (x, y), (x + icon.shape[1], y + icon.shape[0]), (0, 0, 255), 2)
                    cv2.imshow('Detected', screenshot)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

                return x, y
            else:
                print("Icon not found within specified limits")
                return -1,-1
        else:
            print("Icon not found")
            return -1,-1


    def find_icon_group(self, icon_path, dbg_print=False):
        # 截取屏幕
        screen = self.capture_screen()
        
        # 讀取圖標模板
        icon = cv2.imread(icon_path)
        if icon is None:
            raise ValueError(f"Failed to read icon file: {icon_path}")
        
        # 灰度匹配
        icon_gray = cv2.cvtColor(icon, cv2.COLOR_BGR2GRAY)
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screen_gray, icon_gray, cv2.TM_CCOEFF_NORMED)

        # 查找所有匹配的座標
        threshold = self.match_threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))  # 转换为 (x, y) 坐标对

        if locations:
            # 直接返回所有匹配位置
            if dbg_print:
                screenshot = screen
                for loc in locations:
                    cv2.rectangle(screenshot, loc, (loc[0] + icon.shape[1], loc[1] + icon.shape[0]), (0, 255, 0), 2)
                # 显示调试截图
                cv2.imshow('Detected', screenshot)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            # 返回所有匹配的坐标
            return locations
        else:
            print("Icon not found")
            return []




    def swipe_screen(self, x1=1853, y1=740, x2=1853, y2=240, duration=500):
        """
        在屏幕上從 (x1, y1) 拖動到 (x2, y2)。
        
        :param x1: 起始點的 x 坐標
        :param y1: 起始點的 y 坐標
        :param x2: 終點的 x 坐標
        :param y2: 終點的 y 坐標
        :param duration: 拖動的持續時間（毫秒）
        """
        command = f'adb -s {self.device_id} shell input swipe {x1} {y1} {x2} {y2} {duration}'
        subprocess.run(command, shell=True)
        time.sleep(duration / 1000 + 0.5)  # 根據持續時間添加延遲

def idle_wakeup(blhx_simulator):
    blhx_simulator.tap_screen(1100,500)

def left_arrow(blhx_simulator):
    blhx_simulator.tap_screen(50,300)

def get_gas(blhx_simulator):
    blhx_simulator.tap_screen(200,80)

def get_money(blhx_simulator):
    blhx_simulator.tap_screen(510,80)

def get_exp(blhx_simulator):
    blhx_simulator.tap_screen(700,80)

def get_resource(blhx_simulator):
    blhx_simulator.tap_delay = 0.25
    for i in range(3):
        get_gas(blhx_simulator)
    for i in range(3):
        get_money(blhx_simulator)
    for i in range(3):
        get_exp(blhx_simulator)
    blhx_simulator.tap_delay = 1

def get_delegation(blhx_simulator):
    for i in range(7):
        blhx_simulator.tap_screen(700,440)
        blhx_simulator.tap_screen(700,440)

def set_delegation(blhx_simulator):
    blhx_simulator.tap_delay = 0.75
    blhx_simulator.tap_screen(900,440)
    blhx_simulator.tap_screen(1400,540)
    blhx_simulator.tap_screen(1640,540)
    blhx_simulator.tap_screen(900,230)

    blhx_simulator.tap_screen(900,460)
    blhx_simulator.tap_screen(1400,540)
    blhx_simulator.tap_screen(1640,540)
    blhx_simulator.tap_screen(900,230)

    blhx_simulator.tap_screen(900,700)
    blhx_simulator.tap_screen(1400,540)
    blhx_simulator.tap_screen(1640,540)
    blhx_simulator.tap_screen(900,230)

    blhx_simulator.tap_screen(900,900)
    blhx_simulator.tap_screen(1400,540)
    blhx_simulator.tap_screen(1640,540)
    blhx_simulator.tap_screen(900,230)
    blhx_simulator.tap_delay = 1

def back_to_top(blhx_simulator):
    blhx_simulator.tap_screen(1845,55)

def tap_attack(blhx_simulator):
    blhx_simulator.tap_screen(1770,750)

def tap_job_outside(blhx_simulator):
    blhx_simulator.tap_screen(1080,920)

def back_last_layer(blhx_simulator):
    blhx_simulator.match_threshold = 0.5
    x,y=blhx_simulator.find_icon("./blhx/last.png",dbg_print=0)
    if x>=0 and y>=0:
        blhx_simulator.tap_screen(x+80,y+80)

def tap_job_inside_job(blhx_simulator):
    blhx_simulator.tap_screen(950,520)
    blhx_simulator.tap_screen(990,300)
    blhx_simulator.tap_screen(1600,480)
    blhx_simulator.tap_screen(1600,480)
    back_last_layer(blhx_simulator)

def tap_job_inside(blhx_simulator):
    weekday = datetime.date.today().weekday() +1 # trans to 1-index base
    print(weekday)
    tap_job_inside_job(blhx_simulator)
    if weekday in {2,5}:
        blhx_simulator.tap_screen(1860,540)
        blhx_simulator.tap_screen(1860,540)
        tap_job_inside_job(blhx_simulator)
    elif weekday in {3,6}:
        blhx_simulator.tap_screen(1860,540)
        tap_job_inside_job(blhx_simulator)
    elif weekday in {1,4}:
        blhx_simulator.tap_screen(1860,540)
        blhx_simulator.tap_screen(1860,540)
        blhx_simulator.tap_screen(1860,540)
        tap_job_inside_job(blhx_simulator)
    elif weekday == 7:
        blhx_simulator.tap_screen(1860,540)
        tap_job_inside_job(blhx_simulator)
        blhx_simulator.tap_screen(1860,540)
        tap_job_inside_job(blhx_simulator)
        blhx_simulator.tap_screen(1860,540)
        tap_job_inside_job(blhx_simulator)

def tap_fight(blhx_simulator): #編隊出擊
    blhx_simulator.tap_screen(1714,953)

def tap_drill(blhx_simulator):
    blhx_simulator.tap_screen(1566,913)
    blhx_simulator.tap_screen(319,348)
    blhx_simulator.tap_screen(971,865)
    tap_fight(blhx_simulator)

def tap_life_area(blhx_simulator):
    blhx_simulator.tap_screen(843,1015)

def tap_home_food_supply(blhx_simulator):
    blhx_simulator.tap_screen(686,741) 
    time.sleep(1)
    blhx_simulator.tap_screen(1641,931)  #判斷是否收經驗 #TODO
    blhx_simulator.tap_screen(1804,759) #收好感
    blhx_simulator.tap_screen(429,1002) #食物
    for i in range(8):
        blhx_simulator.tap_screen(1254,667) #食物5000
        #判斷食物是否滿了超過 #TODO
    blhx_simulator.tap_screen(68,71) #上一步
    blhx_simulator.tap_screen(68,71) #上一步

def tap_home_cat(blhx_simulator):
    blhx_simulator.tap_screen(965,721)
    time.sleep(1)
    blhx_simulator.tap_screen(1748,931)#確定
    blhx_simulator.tap_screen(1309,942)#喵窩
    blhx_simulator.tap_screen(171,438)#掃除
    blhx_simulator.tap_screen(171,438)#掃除
    blhx_simulator.tap_screen(171,438)#掃除
    blhx_simulator.tap_screen(171,438)#掃除
    blhx_simulator.tap_screen(1532,196) #XX 
    blhx_simulator.tap_screen(1549,940) #訂購
    blhx_simulator.tap_screen(1367,714) #結算
    blhx_simulator.tap_screen(1181,673) #確認
    time.sleep(2)
    blhx_simulator.tap_screen(1181,673) #確認
    blhx_simulator.tap_screen(958,132) #關閉視窗

    blhx_simulator.tap_screen(1775,928) #訓練
    blhx_simulator.tap_screen(1229,849) #全部完成
    time.sleep(5)
    blhx_simulator.tap_screen(1746,55) #skip
    blhx_simulator.tap_screen(1165,683) #確認

    blhx_simulator.tap_screen(967,252) #
    blhx_simulator.tap_screen(1455,855) #開始訓練
    blhx_simulator.tap_screen(1214,833) #一鍵選擇
    blhx_simulator.tap_screen(1455,855) #開始訓練
    blhx_simulator.tap_screen(1165,683) #確認
    blhx_simulator.tap_screen(1526,233) #XX
    blhx_simulator.tap_screen(68,71) #上一步

def check_drill_victory(blhx_simulator):
    
    for i in range(6):
    # for i in range(1):
        time.sleep(30)
        blhx_simulator.match_threshold = 0.3
        x,y=blhx_simulator.find_icon("./blhx/victory_0.png",dbg_print=0)
        if x>=0 and y>=0:
            blhx_simulator.tap_screen(1752,992) #戰鬥勝利:確定
            blhx_simulator.tap_screen(1752,992) #戰鬥勝利:確定
            time.sleep(3)
            blhx_simulator.tap_screen(1752,992) #戰鬥勝利:確定
            break

        blhx_simulator.match_threshold = 0.6
        x,y=blhx_simulator.find_icon("./blhx/victory_1.png",dbg_print=0)
        if x>=0 and y>=0:
            blhx_simulator.tap_screen(1752,992) #戰鬥勝利:確定
            blhx_simulator.tap_screen(1752,992) #戰鬥勝利:確定
            time.sleep(3)
            blhx_simulator.tap_screen(1752,992) #戰鬥勝利:確定
            break

        blhx_simulator.match_threshold = 0.3
        x,y=blhx_simulator.find_icon("./blhx/defeat_0.png",dbg_print=0)
        if x>=0 and y>=0:
            blhx_simulator.tap_screen(1752,992) #戰鬥勝利:確定
            blhx_simulator.tap_screen(1752,992) #戰鬥勝利:確定
            time.sleep(3)
            blhx_simulator.tap_screen(1752,992) #戰鬥勝利:確定
            blhx_simulator.tap_screen(943,918) #戰鬥失敗:確定
            blhx_simulator.tap_screen(1752,992) #戰鬥勝利:確定
            break

        blhx_simulator.match_threshold = 0.4
        x,y=blhx_simulator.find_icon("./blhx/defeat_1.png",limit_x=821 , limit_y=158,dbg_print=0)
        if x>=0 and y>=0:
            blhx_simulator.tap_screen(1752,992) #戰鬥勝利:確定
            blhx_simulator.tap_screen(1752,992) #戰鬥勝利:確定
            time.sleep(3)
            blhx_simulator.tap_screen(1752,992) #戰鬥勝利:確定
            blhx_simulator.tap_screen(943,918) #戰鬥失敗:確定
            # blhx_simulator.tap_screen(1752,992) #戰鬥勝利:確定
            break

def blhx_daily1(blhx_simulator): #收菜
    idle_wakeup(blhx_simulator)
    left_arrow(blhx_simulator)
    get_resource(blhx_simulator)
    get_delegation(blhx_simulator)
    idle_wakeup(blhx_simulator)
    set_delegation(blhx_simulator)
    back_to_top(blhx_simulator)

def blhx_daily2(blhx_simulator): #挑戰
    idle_wakeup(blhx_simulator)
    tap_attack(blhx_simulator)
    tap_job_outside(blhx_simulator)
    tap_job_inside(blhx_simulator)
    back_to_top(blhx_simulator)

def blhx_daily3(blhx_simulator): #后宅
    idle_wakeup(blhx_simulator)
    tap_life_area(blhx_simulator)
    tap_home_food_supply(blhx_simulator)
    tap_life_area(blhx_simulator)
    tap_home_cat(blhx_simulator)

def blhx_daily4(blhx_simulator): #籌備
    idle_wakeup(blhx_simulator)
    blhx_simulator.tap_screen(1787,1017) #大艦隊
    time.sleep(1)
    blhx_simulator.tap_screen(74,652) #後勤
    blhx_simulator.tap_screen(1716,953) #後勤
    blhx_simulator.tap_screen(1716,953) #後勤

    blhx_simulator.tap_screen(1714,453) #每周任務
    blhx_simulator.tap_screen(1714,453) #每周任務

    #========================================== 先手動執行 上面可自動
    for i in range(3):
        blhx_simulator.match_threshold = 0.5
        x,y=blhx_simulator.find_icon("./blhx/food_0.png",dbg_print=0)
        if x>=0 and y>=0:
            blhx_simulator.tap_screen(x+80,y+220)
            blhx_simulator.tap_screen(1182,766) #確定
            blhx_simulator.tap_screen(1182,766) #確定
            continue

        blhx_simulator.match_threshold = 0.7
        x,y=blhx_simulator.find_icon("./blhx/food_1.png",limit_y=690,dbg_print=0)
        print(f"x={x},y={y}")
        if x>=0 and y>=0:
            blhx_simulator.tap_screen(x+80,y+220)
            blhx_simulator.tap_screen(1182,766) #確定
            blhx_simulator.tap_screen(1182,766) #確定
            continue
        
        blhx_simulator.match_threshold = 0.54
        x,y=blhx_simulator.find_icon("./blhx/material_1.png",dbg_print=0) #白菜飛機
        if x>=0 and y>=0:
            blhx_simulator.tap_screen(x+80,y+220)
            blhx_simulator.tap_screen(1182,766) #確定
            blhx_simulator.tap_screen(1182,766) #確定
            continue

        blhx_simulator.match_threshold = 0.54
        x,y=blhx_simulator.find_icon("./blhx/material_3.png",dbg_print=0) #白菜飛機
        if x>=0 and y>=0:
            blhx_simulator.tap_screen(x+80,y+220)
            blhx_simulator.tap_screen(1182,766) #確定
            blhx_simulator.tap_screen(1182,766) #確定
            continue

        blhx_simulator.match_threshold = 0.52
        x,y=blhx_simulator.find_icon("./blhx/material_2.png",dbg_print=0) #白菜通用
        if x>=0 and y>=0:
            blhx_simulator.tap_screen(x+80,y+220)
            blhx_simulator.tap_screen(1182,766) #確定
            blhx_simulator.tap_screen(1182,766) #確定
            continue

        blhx_simulator.match_threshold = 0.6
        x,y=blhx_simulator.find_icon("./blhx/material_0.png",dbg_print=0) #藍菜
        if x>=0 and y>=0:
            blhx_simulator.tap_screen(x+80,y+220)
            blhx_simulator.tap_screen(1182,766) #確定
            blhx_simulator.tap_screen(1182,766) #確定
            continue

        blhx_simulator.match_threshold = 0.6
        x,y=blhx_simulator.find_icon("./blhx/material_5.png",dbg_print=0) #紫菜
        if x>=0 and y>=0:
            blhx_simulator.tap_screen(x+80,y+220)
            blhx_simulator.tap_screen(1182,766) #確定
            blhx_simulator.tap_screen(1182,766) #確定
            continue

        blhx_simulator.match_threshold = 0.6
        x,y=blhx_simulator.find_icon("./blhx/money_0.png",dbg_print=0)
        if x>=0 and y>=0:
            blhx_simulator.tap_screen(x+80,y+220)
            blhx_simulator.tap_screen(1182,766) #確定
            blhx_simulator.tap_screen(1182,766) #確定
            continue
    back_to_top(blhx_simulator)

def blhx_daily5(blhx_simulator): #演習
    idle_wakeup(blhx_simulator)
    tap_attack(blhx_simulator)
    tap_drill(blhx_simulator)
    check_drill_victory(blhx_simulator)
    back_to_top(blhx_simulator)

def meta1_fight(blhx_simulator):
    idle_wakeup(blhx_simulator)
    left_arrow(blhx_simulator)
    blhx_simulator.tap_screen(930,539) #進meta 

    blhx_simulator.tap_screen(646,558) #選meta1

    blhx_simulator.tap_screen(980,475) #情報解析
    
    blhx_simulator.tap_screen(1417,985) #支援
    blhx_simulator.tap_screen(1309,517) #世界
    blhx_simulator.tap_screen(1249,778) #確定

    for i in range(5):
        #meta1 當期 不可自動
        blhx_simulator.match_threshold = 0.5
        x,y=blhx_simulator.find_icon("./blhx/battle_start.png",dbg_print=0)
        if x>=0 and y>=0:
            blhx_simulator.tap_screen(x+130,y+50)
            tap_fight(blhx_simulator) #出擊
            time.sleep(120)
            for i in range(15):
                blhx_simulator.match_threshold = 0.5
                x,y=blhx_simulator.find_icon("./blhx/success_check.png",dbg_print=0)
                if x>=0 and y>=0:
                    blhx_simulator.tap_screen(x+100,y+30)
                    break
                time.sleep(10)

        blhx_simulator.match_threshold = 0.6
        x,y=blhx_simulator.find_icon("./blhx/collect_reward.png",dbg_print=0)
        if x>=0 and y>=0:
            blhx_simulator.tap_screen(x+100,y+30)
            blhx_simulator.tap_screen(x+100,y+30)
            break

        time.sleep(10)
    back_to_top(blhx_simulator)

def meta2_fight(blhx_simulator):
    # meta2 可自動
    idle_wakeup(blhx_simulator)
    left_arrow(blhx_simulator)
    blhx_simulator.tap_screen(930,539) #進meta 
    blhx_simulator.tap_screen(1289,558) #選meta2
    blhx_simulator.tap_screen(980,475) #情報解析
    blhx_simulator.match_threshold = 0.5
    x,y=blhx_simulator.find_icon("./blhx/battle_start.png",dbg_print=0)
    if x>=0 and y>=0:
        blhx_simulator.tap_screen(x+130,y+50)
        tap_fight(blhx_simulator) #出擊
        time.sleep(120)
        for i in range(15):
            blhx_simulator.match_threshold = 0.5
            x,y=blhx_simulator.find_icon("./blhx/success_check.png",dbg_print=0)
            if x>=0 and y>=0:
                blhx_simulator.tap_screen(x+100,y+30)
                break
            time.sleep(10)
    blhx_simulator.tap_screen(1204,1011)#自動作戰
    blhx_simulator.tap_screen(1279,776)#開始
    back_to_top(blhx_simulator)

if __name__ == "__main__":
    # 設置不同遊戲的閾值
    blhx_simulator = Simulator(name="blhx", device_id="emulator-5554", match_threshold=0.53)


    blhx_daily1(blhx_simulator) #收資源
    blhx_daily2(blhx_simulator) #每日挑戰
    blhx_daily3(blhx_simulator) #后宅 & 指揮貓
    blhx_daily4(blhx_simulator) #籌備
    blhx_daily5(blhx_simulator) #演習

    #====== 上面可以自動完成=====
    # meta1_fight(blhx_simulator)
    # meta2_fight(blhx_simulator)

    # back_to_top(blhx_simulator)

