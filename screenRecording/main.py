import cv2
import numpy as np
import pyautogui
import time
import sys
import keyboard


def main():
    print("Recording Start.")
    # 設定錄影參數
    screen_size = pyautogui.size()  # 獲取螢幕解析度
    fps = 20.0  # 設定幀率
    fourcc = cv2.VideoWriter_fourcc(*"XVID")  # 使用 XVID 編碼
    output = cv2.VideoWriter("screen_recording.avi", fourcc, fps, screen_size)

    # 開始錄影
    start_time = time.time()
    duration = 10  # 設定錄影時間 (秒數)

    while True:
        # 截取螢幕畫面
        img = pyautogui.screenshot()
        frame = np.array(img)  # 將螢幕畫面轉為 numpy 陣列
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 將顏色從 BGR 轉為 RGB

        # 將幀寫入視頻文件
        output.write(frame)

        # 結束條件
        # if time.time() - start_time > duration:  # 錄製 10 秒後停止
        if keyboard.is_pressed('q'):
            break

    print("Recording End.")
    # 釋放資源
    output.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
