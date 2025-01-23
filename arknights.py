import subprocess
import cv2
import numpy as np
import time

from blhx  import Simulator


def into_infra(arknights_simulator):
    arknights_simulator.tap_screen(1500,1000)

def infra_info(arknights_simulator):
    arknights_simulator.match_threshold = 0.7
    x,y = arknights_simulator.find_icon('./arknights/infra_notify.png',limit_x=1700,dbg_print=0)
    if x!=0 or y!=0:
        arknights_simulator.tap_screen(x,y)

    for i in range(5):
        arknights_simulator.tap_screen(276,1021)

    arknights_simulator.tap_screen(272,842) #回基建

def infra_backtop(arknights_simulator):
    for i in range(5):
        arknights_simulator.swipe_screen(y1=240,y2=740,duration=500) #back to top

    for i in range(10):
        arknights_simulator.match_threshold = 0.37
        x,y = arknights_simulator.find_icon('./arknights/infra_top.png',limit_x=0,dbg_print=0)
        if x>=0 and y>=0:
            break

        arknights_simulator.match_threshold = 0.7
        x,y = arknights_simulator.find_icon('./arknights/infra_top_2.png',dbg_print=0)
        if x>=0 and y>=0:
            break

        arknights_simulator.swipe_screen(y1=240,y2=740) #back to top

def infra_set_dorm(arknights_simulator):
    #set dorm
    dorm_cnt = 0
    for i in range(20):
        time.sleep(1)
        arknights_simulator.swipe_screen(duration = 2000)
        if i == 0:
            arknights_simulator.swipe_screen(duration = 2000)
        arknights_simulator.match_threshold = 0.7
        if dorm_cnt == 3:
            x,y = arknights_simulator.find_icon('./arknights/infra_dorm_55.png',limit_y = 700 ,dbg_print=0)
        else:
            x,y = arknights_simulator.find_icon('./arknights/infra_dorm_55.png',dbg_print=0)
        if x>=0 and y>=0:
            arknights_simulator.tap_delay = 2
            arknights_simulator.tap_screen(1000,y+30)

            arknights_simulator.tap_delay = 0.5
            arknights_simulator.tap_screen(750,1020)

            arknights_simulator.tap_screen(1160,720)
            arknights_simulator.tap_screen(1375,720)
            arknights_simulator.tap_screen(1600,720)
            arknights_simulator.tap_screen(1380,300)
            arknights_simulator.tap_screen(1590,300)

            arknights_simulator.tap_screen(1670,1000)
            dorm_cnt+=1
        
        arknights_simulator.match_threshold = 0.66
        x,y = arknights_simulator.find_icon('./arknights/check.png',dbg_print=0)
        if x>=0 and y>=0:
            arknights_simulator.tap_screen(x+500,y+100)

        if dorm_cnt == 4:
            break
    arknights_simulator.tap_delay = 1

def infra_set_central(arknights_simulator):
    arknights_simulator.tap_screen(1000,300)
    arknights_simulator.tap_delay = 0.5
    arknights_simulator.tap_screen(750,1020) #清空選擇

    arknights_simulator.tap_screen(1160,720)
    arknights_simulator.tap_screen(1375,720)
    arknights_simulator.tap_screen(1600,720)
    arknights_simulator.tap_screen(1380,300)
    arknights_simulator.tap_screen(1590,300)

    arknights_simulator.tap_screen(1670,1000) #確認

    arknights_simulator.match_threshold = 0.66
    x,y = arknights_simulator.find_icon('./arknights/check.png',dbg_print=1)
    if x>=0 and y>=0:
        arknights_simulator.tap_screen(x+500,y+100)
    arknights_simulator.tap_delay = 1

def infra_scan_set_trading_post(arknights_simulator):
    arknights_simulator.match_threshold = 0.7
    group = arknights_simulator.find_icon_group('./arknights/trading_post.png',dbg_print=0)
    x1 ,y1 = group[0]
    x2 ,y2 = group[-1]
    y1 = y1+50
    arknights_simulator.tap_delay = 2
    arknights_simulator.tap_screen(1000,y1)
    arknights_simulator.tap_screen(750,1020)

    arknights_simulator.tap_delay = 0.5
    arknights_simulator.tap_screen(720,320)
    arknights_simulator.tap_screen(720,740)
    arknights_simulator.tap_screen(940,320)

    arknights_simulator.tap_delay = 3
    arknights_simulator.tap_screen(1670,1000) #確認
    arknights_simulator.match_threshold = 0.66
    x,y = arknights_simulator.find_icon('./arknights/check.png',dbg_print=1)
    if x>=0 and y>=0:
        arknights_simulator.tap_screen(x+500,y+100)
    
    y2 = y2+50
    arknights_simulator.tap_screen(1000,y2)
    arknights_simulator.tap_delay = 0.5

    arknights_simulator.tap_screen(750,1020)
    arknights_simulator.tap_screen(720,320)
    arknights_simulator.tap_screen(720,740)
    arknights_simulator.tap_screen(940,320)

    arknights_simulator.tap_screen(1670,1000) #確認
    arknights_simulator.match_threshold = 0.66
    x,y = arknights_simulator.find_icon('./arknights/check.png',dbg_print=1)
    if x>=0 and y>=0:
        arknights_simulator.tap_screen(x+500,y+100)
    arknights_simulator.tap_delay = 2

def infra_scan_set_power_station(arknights_simulator):
    #增加判斷點 , 有時候少抓 #TODO
    arknights_simulator.match_threshold = 0.6
    x,y = arknights_simulator.find_icon('./arknights/power_station.png',dbg_print=0)
    if x>=0 and y>=0:
        y = y+50
        arknights_simulator.tap_delay = 1.5
        arknights_simulator.tap_screen(1000,y)
        time.sleep(1)
        arknights_simulator.tap_screen(750,1020)

        arknights_simulator.tap_delay = 0.5
        arknights_simulator.tap_screen(720,320)

        arknights_simulator.tap_delay = 3
        arknights_simulator.tap_screen(1670,1000) #確認
        arknights_simulator.match_threshold = 0.66
    x,y = arknights_simulator.find_icon('./arknights/check.png',dbg_print=0)
    if x>=0 and y>=0:
        arknights_simulator.tap_screen(x+500,y+100)

def infra_scan_set_manufacturing_station(arknights_simulator,manufacturing_station_cnt):
    arknights_simulator.match_threshold = 0.8
    group = arknights_simulator.find_icon_group('./arknights/manufacturing_station.png',dbg_print=0)
    if len(group) >= 2:
        x1 ,y1 = group[0]
        x2 ,y2 = group[-1]
        print("y2=",y2)
        print("y1=",y1)
        if(y2-y1 < 50):
            return manufacturing_station_cnt
        y1 = y1+50
        arknights_simulator.tap_delay = 2
        arknights_simulator.tap_screen(1000,y1)
        arknights_simulator.tap_screen(750,1020)

        arknights_simulator.tap_delay = 0.5
        arknights_simulator.tap_screen(720,320)
        arknights_simulator.tap_screen(720,740)
        arknights_simulator.tap_screen(940,320)

        arknights_simulator.tap_delay = 3
        arknights_simulator.tap_screen(1670,1000) #確認
        arknights_simulator.match_threshold = 0.66
        x,y = arknights_simulator.find_icon('./arknights/check.png',dbg_print=1)
        if x>=0 and y>=0:
            arknights_simulator.tap_screen(x+500,y+100)
        
        y2 = y2+50
        arknights_simulator.tap_screen(1000,y2)
        arknights_simulator.tap_delay = 0.5

        arknights_simulator.tap_screen(750,1020)
        arknights_simulator.tap_screen(720,320)
        arknights_simulator.tap_screen(720,740)
        arknights_simulator.tap_screen(940,320)

        arknights_simulator.tap_screen(1670,1000) #確認
        arknights_simulator.match_threshold = 0.66
        x,y = arknights_simulator.find_icon('./arknights/check.png',dbg_print=1)
        arknights_simulator.tap_delay = 2
        if x>=0 and y>=0:
            arknights_simulator.tap_screen(x+500,y+100)
        
        manufacturing_station_cnt +=2
    return manufacturing_station_cnt


def infra_scan_set_office(arknights_simulator):
    #增加判斷點 , 有時候少抓 #TODO
    arknights_simulator.match_threshold = 0.7
    x,y = arknights_simulator.find_icon('./arknights/office.png',dbg_print=1)
    if x>=0 and y>=0:
        y = y+50
        arknights_simulator.tap_delay = 1.5
        arknights_simulator.tap_screen(1000,y)
        arknights_simulator.tap_screen(750,1020)

        arknights_simulator.tap_delay = 0.5
        arknights_simulator.tap_screen(720,320)

        arknights_simulator.tap_delay = 3
        arknights_simulator.tap_screen(1670,1000) #確認
        arknights_simulator.match_threshold = 0.66
    x,y = arknights_simulator.find_icon('./arknights/check.png',dbg_print=1)
    if x>=0 and y>=0:
        arknights_simulator.tap_screen(x+500,y+100)

def infra_scan_set_reception_room(arknights_simulator):
    arknights_simulator.tap_delay = 1.5
    arknights_simulator.tap_screen(1000,550)
    arknights_simulator.tap_screen(750,1020) #清空選擇

    arknights_simulator.tap_screen(700,300)
    arknights_simulator.tap_screen(700,700)
    
    arknights_simulator.tap_screen(1670,1000) #確認

    arknights_simulator.match_threshold = 0.66
    x,y = arknights_simulator.find_icon('./arknights/check.png',dbg_print=1)
    if x>=0 and y>=0:
        arknights_simulator.tap_screen(x+500,y+100)
    arknights_simulator.tap_delay = 1

def infra_reorg(arknights_simulator): #基建排班
    arknights_simulator.tap_screen(163,180) #進駐總覽

    infra_backtop(arknights_simulator)
    infra_set_dorm(arknights_simulator)

    infra_backtop(arknights_simulator)
    infra_set_central(arknights_simulator)
    infra_scan_set_reception_room(arknights_simulator)

    trading_post_cnt = 0
    power_station_cnt = 0
    manufacturing_station_cnt = 0
    office_cnt = 0
    arknights_simulator.swipe_screen(y1=700,y2=500)
    for i in range(10):
        if trading_post_cnt < 2:
            infra_scan_set_trading_post(arknights_simulator)
            trading_post_cnt+=2
        arknights_simulator.swipe_screen(duration = 2000)
        time.sleep(1)
        if power_station_cnt < 3:
            infra_scan_set_power_station(arknights_simulator)
            power_station_cnt+=1
        if manufacturing_station_cnt < 4:
            manufacturing_station_cnt = infra_scan_set_manufacturing_station(arknights_simulator,manufacturing_station_cnt)
        if office_cnt < 1:
            infra_scan_set_office(arknights_simulator)
            office_cnt+=1

        
        if(trading_post_cnt+power_station_cnt+manufacturing_station_cnt+office_cnt==10):
            print("trading_post_cnt=",trading_post_cnt)
            print("power_station_cnt=",power_station_cnt)
            print("manufacturing_station_cnt=",manufacturing_station_cnt)
            print("office_cnt=",office_cnt)
            break
        else:
            print("trading_post_cnt=",trading_post_cnt)
            print("power_station_cnt=",power_station_cnt)
            print("manufacturing_station_cnt=",manufacturing_station_cnt)
            print("office_cnt=",office_cnt)

def back_top(arknights_simulator):
    arknights_simulator.tap_delay = 1
    arknights_simulator.tap_screen(400,60)
    arknights_simulator.tap_screen(138,416)
    time.sleep(10)

def back_last(arknights_simulator):
    arknights_simulator.tap_delay = 1
    arknights_simulator.tap_screen(122,52)
    time.sleep(1)

def tap_trading_station(arknights_simulator):
    arknights_simulator.tap_delay = 1
    arknights_simulator.tap_screen(304,479)
    time.sleep(1)
    arknights_simulator.tap_screen(524,934)
    for i in range(4):
        #判斷若無人機沒滿時處理 #TODO
        arknights_simulator.tap_screen(572,744)
        arknights_simulator.tap_screen(1446,502)
        arknights_simulator.tap_screen(1409,875)
        arknights_simulator.tap_screen(605,625)


def daily_infra(arknights_simulator):
    into_infra(arknights_simulator)
    time.sleep(10)
    infra_info(arknights_simulator)
    time.sleep(1)
    infra_reorg(arknights_simulator)
    back_last(arknights_simulator)
    tap_trading_station(arknights_simulator)
    back_top(arknights_simulator)

def daliy_recruit(arknights_simulator):
    arknights_simulator.tap_screen(1515,765)
    time.sleep(5)
    # 判斷是否滿了可收? #TODO
    arknights_simulator.tap_screen(481,575)
    time.sleep(5)
    arknights_simulator.tap_screen(1825,55)
    time.sleep(1)
    arknights_simulator.tap_screen(1825,55)

    arknights_simulator.tap_screen(1438,575)
    time.sleep(5)
    arknights_simulator.tap_screen(1825,55)
    time.sleep(1)
    arknights_simulator.tap_screen(1825,55)

    arknights_simulator.tap_screen(458,985)
    time.sleep(5)
    arknights_simulator.tap_screen(1825,55)
    time.sleep(1)
    arknights_simulator.tap_screen(1825,55)

    arknights_simulator.tap_screen(1416,983)
    time.sleep(5)
    arknights_simulator.tap_screen(1825,55)
    time.sleep(1)
    arknights_simulator.tap_screen(1825,55)

def daily_buy(arknights_simulator):
    arknights_simulator.tap_screen(1262,701)
    time.sleep(1)
    arknights_simulator.tap_screen(1775,160)
    arknights_simulator.tap_screen(1531,55)
    arknights_simulator.tap_screen(1531,55)

    arknights_simulator.tap_screen(180,392)
    arknights_simulator.tap_screen(1390,868)
    arknights_simulator.tap_screen(1390,868)

    arknights_simulator.tap_screen(583,415)
    arknights_simulator.tap_screen(1390,868)
    arknights_simulator.tap_screen(1390,868)

    arknights_simulator.tap_screen(969,424)
    arknights_simulator.tap_screen(1390,868)
    arknights_simulator.tap_screen(1390,868)

    back_top(arknights_simulator)

if __name__ == '__main__':
# 設置不同遊戲的閾值
    arknights_simulator = Simulator(name="arknights", device_id="emulator-5556", match_threshold=0.8)

    daily_infra(arknights_simulator)
    daily_buy(arknights_simulator)
    daliy_recruit(arknights_simulator)


    # back_top(arknights_simulator)

