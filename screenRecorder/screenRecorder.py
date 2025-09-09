import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import cv2
import numpy as np
import mss
import time
import ctypes

# --- DPI aware, 保證物理像素座標 ---
ctypes.windll.user32.SetProcessDPIAware()


class ScreenRecorder:
    def __init__(self):
        self.is_recording = False
        self.is_paused = threading.Event()
        self.is_paused.set()  # 初始是錄影狀態

        self.monitor = None
        self.video_writer = None
        self.output_path = ""

        self.elapsed_time = 0
        self.timer_running = False

        self.root = tk.Tk()
        self.root.title("螢幕錄影程式")

        # GUI 按鈕
        tk.Button(self.root, text="選擇錄影範圍",
                  command=self.select_region).pack(pady=5)
        tk.Button(self.root, text="選擇輸出並開始錄影",
                  command=self.start_recording).pack(pady=5)

        # 暫停/繼續切換按鈕
        self.pause_resume_btn = tk.Button(
            self.root, text="暫停", command=self.toggle_pause)
        self.pause_resume_btn.pack(pady=5)

        tk.Button(self.root, text="停止錄影", command=self.stop).pack(pady=5)

        # 顯示錄影時間
        self.timer_label = tk.Label(
            self.root, text="錄影時間: 00:00:00", font=("Arial", 12))
        self.timer_label.pack(pady=5)

        # 顯示錄影狀態 (紅點 / 暫停 / 停止)
        self.status_label = tk.Label(
            self.root, text="■ 停止", font=("Arial", 12), fg="grey")
        self.status_label.pack(pady=5)

        self.root.mainloop()

    # -------- 滑鼠拖曳選擇錄影範圍 --------
    def select_region(self):
        def callback(x1, y1, x2, y2):
            x1_real = int(min(x1, x2))
            y1_real = int(min(y1, y2))
            width = int(abs(x2 - x1))
            height = int(abs(y2 - y1))
            self.monitor = {"top": y1_real, "left": x1_real,
                            "width": width, "height": height}
            print(f"[DEBUG] 錄影範圍設定: {self.monitor}")

        RegionSelector(self.root, callback)

    # -------- 開始錄影 --------
    def start_recording(self):
        if not self.monitor:
            messagebox.showwarning("警告", "請先選擇錄影範圍！")
            return

        self.output_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        if not self.output_path:
            return

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter(
            self.output_path, fourcc, 30.0,  # 目標 fps
            (self.monitor["width"], self.monitor["height"])
        )

        self.is_recording = True
        self.elapsed_time = 0
        self.timer_running = True
        self.is_paused.set()  # 開始錄影狀態
        self.pause_resume_btn.config(text="暫停")
        self.status_label.config(text="● REC", fg="red")  # 顯示錄影紅點
        print("[DEBUG] 開始錄影")
        self.update_timer()
        threading.Thread(target=self.record_thread, daemon=True).start()

    # -------- 錄影執行緒 --------
    def record_thread(self):
        target_fps = 30.0
        time_per_frame = 1.0 / target_fps

        with mss.mss() as sct:
            frame_count = 0
            start_time = time.time()
            last_print_time = start_time

            while self.is_recording:
                frame_start = time.time()

                # 暫停阻塞
                while not self.is_paused.is_set() and self.is_recording:
                    time.sleep(0.1)
                    frame_start = time.time()  # 暫停後重新計算幀開始時間

                if not self.is_recording:
                    break

                img = np.array(sct.grab(self.monitor))
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                self.video_writer.write(frame)
                frame_count += 1

                # 每秒打印一次實際幀率
                now = time.time()
                if now - last_print_time >= 1.0:
                    fps_actual = frame_count / (now - last_print_time)
                    # print(
                    #     f"[DEBUG] 已錄 {frame_count} 幀，實際 fps: {fps_actual:.2f}")
                    frame_count = 0
                    last_print_time = now

                # 動態 sleep 控制幀率
                elapsed = time.time() - frame_start
                sleep_time = max(0, time_per_frame - elapsed)
                time.sleep(sleep_time)

        self.video_writer.release()
        print(f"[DEBUG] 錄影結束，檔案已存: {self.output_path}")

    # -------- 更新錄影時間 --------
    def update_timer(self):
        if self.timer_running and self.is_paused.is_set():
            self.elapsed_time += 0.2
        h = int(self.elapsed_time // 3600)
        m = int((self.elapsed_time % 3600) // 60)
        s = int(self.elapsed_time % 60)
        self.timer_label.config(text=f"錄影時間: {h:02d}:{m:02d}:{s:02d}")
        if self.timer_running:
            self.root.after(200, self.update_timer)

    # -------- 暫停/繼續切換按鈕 --------
    def toggle_pause(self):
        if self.is_paused.is_set():
            # 暫停
            print("[DEBUG] 錄影暫停")
            self.is_paused.clear()
            self.pause_resume_btn.config(text="繼續")
            self.status_label.config(text="❚❚ 暫停", fg="black")
        else:
            # 繼續
            print("[DEBUG] 錄影繼續")
            self.is_paused.set()
            self.pause_resume_btn.config(text="暫停")
            self.status_label.config(text="● REC", fg="red")

    # -------- 停止錄影 --------
    def stop(self):
        print("[DEBUG] 錄影停止")
        self.is_recording = False
        self.timer_running = False
        self.is_paused.set()
        if self.video_writer:
            self.video_writer.release()
        self.status_label.config(text="■ 停止", fg="grey")
        self.root.quit()


# -------- 矩形框選範圍 GUI --------
class RegionSelector(tk.Toplevel):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
        self.start_x = self.start_y = 0
        self.rect = None

        self.attributes("-fullscreen", True)
        self.attributes("-alpha", 0.3)
        self.config(bg="black")

        # Canvas 用螢幕解析度
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)

        self.canvas = tk.Canvas(self, cursor="cross",
                                width=screen_width, height=screen_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="red", width=2
        )

    def on_move(self, event):
        self.canvas.coords(self.rect, self.start_x,
                           self.start_y, event.x, event.y)

    def on_button_release(self, event):
        x1, y1, x2, y2 = self.start_x, self.start_y, event.x, event.y
        print(f"[DEBUG] 選取範圍: ({x1}, {y1}) -> ({x2}, {y2})")
        self.callback(x1, y1, x2, y2)
        self.destroy()


if __name__ == "__main__":
    ScreenRecorder()
