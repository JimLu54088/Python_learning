from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import time
import re
import os
import sys

# --------- 配置 ---------
video_page_url = sys.argv[1]
output_dir = sys.argv[2]
os.makedirs(output_dir, exist_ok=True)
video_title = sys.argv[3]

# --------- Selenium 配置 ---------
chrome_options = Options()
chrome_options.add_argument("--headless")  # 隱藏瀏覽器
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

# --------- 開啟影片頁 ---------
driver.get(video_page_url)
time.sleep(5)  # 等 JS 載入 m3u8

html = driver.page_source

# --------- 抓 m3u8 ---------
m3u8_match = re.search(r'https://.*?\.m3u8', html)
if not m3u8_match:
    print("找不到 m3u8，影片可能還沒載入或需要等待更久")
    driver.quit()
    exit(1)

m3u8_url = m3u8_match.group(0)
print("找到 m3u8:", m3u8_url)
driver.quit()

# --------- ffmpeg 下載影片 ---------
output_path = os.path.join(output_dir, f"{video_title}.mp4")
ffmpeg_cmd = [
    sys.argv[4],
    "-i", m3u8_url,
    "-c", "copy",
    "-bsf:a", "aac_adtstoasc",
    output_path
]

print("開始下載影片...")
subprocess.run(ffmpeg_cmd)
print("下載完成:", output_path)
