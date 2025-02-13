"""
从 KataGO 网站上下载棋谱
"""

import os
import time
import requests

from urllib.parse import urljoin
from datetime import datetime, timedelta

# 下载链接前半部分
base_url = "https://katagoarchive.org/kata1/ratinggames/" # 或者 "https://katagoarchive.org/kata1/trainingdata/"

# 棋谱存放位置
save_dir = ".\\sgf_archive"
os.makedirs(save_dir, exist_ok=True)

# 棋谱日期范围
start_date = "2025-01-01"
end_date = "2025-01-05"

start_date = datetime.strptime(start_date, "%Y-%m-%d")
end_date = datetime.strptime(end_date, "%Y-%m-%d")
date_list = [start_date + timedelta(days=x) for x in range(0, (end_date - start_date).days + 1)]

for date in date_list:
    # 生成下载链接和文件名
    file_name = date.strftime("%Y-%m-%d") + "rating.tar.bz2" # 或者 + "npzs.tgz"
    file_url = urljoin(base_url, file_name)
    save_path = os.path.join(save_dir, file_name)
    
    # 下载棋谱
    print(f"Downloading {file_url} to {save_path}...")
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        absolute_path = os.path.abspath(save_path)
        print(f"Downloaded {file_name} successfully. File saved to: {absolute_path}")
        time.sleep(10)
    else:
        print(f"Failed to download {file_name}. Status code: {response.status_code}")
        exit()