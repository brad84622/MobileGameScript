import cv2
import numpy as np

# 讀取截圖和模板圖像
screenshot = cv2.imread('ss2028.png')
template = cv2.imread('template.png')

# 轉換為灰度圖像
screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# 模板匹配
result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)

# 設定匹配閾值
threshold = 0.8
locations = np.where(result >= threshold)

# 畫出匹配的位置
for loc in zip(*locations[::-1]):
    cv2.rectangle(screenshot, loc, (loc[0] + template.shape[1], loc[1] + template.shape[0]), (0, 255, 0), 2)

# 顯示結果
cv2.imshow('Detected', screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()
