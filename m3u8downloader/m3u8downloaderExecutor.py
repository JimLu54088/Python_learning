from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import subprocess
import time
import re
import os
import sys

try:
    video_page_url = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)
    video_title = sys.argv[3]

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(60)   # <--- ✅ 設定載入超時

    try:
        driver.get(video_page_url)
    except TimeoutException:
        print("Web load time out")
        driver.quit()
        sys.exit(1)

    time.sleep(5)
    html = driver.page_source

    m3u8_match = re.search(r'https://.*?\.m3u8', html)
    if not m3u8_match:
        print("Cannot find m3u8")
        driver.quit()
        sys.exit(1)

    m3u8_url = m3u8_match.group(0)
    print("Finded m3u8:", m3u8_url)
    driver.quit()

    output_path = os.path.join(output_dir, f"{video_title}.mp4")
    ffmpeg_cmd = [
        sys.argv[4],
        "-i", m3u8_url,
        "-c", "copy",
        "-bsf:a", "aac_adtstoasc",
        output_path
    ]

    print("Start to download Video...")
    subprocess.run(ffmpeg_cmd, check=True)  # <--- ✅ 出錯會直接丟 exception
    print("Video downloaded successfully:", output_path)

except Exception as e:
    print("Error occurred:", str(e))
    sys.exit(1)

sys.exit(0)
