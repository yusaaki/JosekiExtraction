# KataGo 定式库构建 / KataGo Joseki Library Construction

## 中文

### 概述

代码实现了从KataGo海量棋谱中自动提取围棋定式(joseki)的功能，包含了棋谱下载、定式提取及筛选、统计分析等步骤，可生成标准SGF格式的定式树文件。

### 文件功能

| 文件名                  | 功能描述                              |
|-----------------------|-----------------------------------|
| download_katago_archive | 棋谱下载，支持指定日期范围下载KataGo官方存档            |
| extract_joseki         | 定式提取，含非标准对局过滤、坐标标准化与序列处理逻辑        |
| postprocess_joseki_tree | 定式树优化模块，实现分支修剪(去除出现频率<1%或<10次的分支)与子节点按局面出现频率排序          |
| count_leaf             | 统计定式文件的变化数（即子节点个数）              |

### 环境要求

- Windows 10
- Python 3.11.4
- 依赖库: 
  ```bash
  pip install requests sgfmill
  ```

### 使用指南

1. **下载棋谱**
   ```python
   # 修改download_katago_archive.py中的参数:
   base_url = "https://katagoarchive.org/kata1/ratinggames/" # 下载地址头，如下载训练棋谱则改为 "https://katagoarchive.org/kata1/trainingdata/"
   start_date = "2025-01-01"  # 起始日期
   end_date = "2025-01-05"    # 结束日期
   save_dir = ".\\sgf_archive"  # 存储路径
   file_name = date.strftime("%Y-%m-%d") + "rating.tar.bz2" # 下载地址尾，如下载训练棋谱则改为 + "npzs.tgz"
   ```

2. **提取定式**
   
   获取棋谱后，可开始提取定式
   ```python
   # 修改extract_joseki.py中的参数：
   ARCHIVE_FOLDER = r'.\\sgf_archive' # 棋谱文件储存文件夹，需包含若干个含有棋谱集的压缩包
   OUTPUT_PATH = r".\\joseki.sgf" # 初步提取的定式树的输出路径

   max_len = 45 # 定式长度，默认为45
   # 另外定式范围默认为角部的10×10区域，可在代码的坐标标准化部分自行调整
   ```

3. **优化定式树**
   
   初步提取的定式树很大，需要删除分支
   ```python
   # 此句删除了 后继概率小于1% 或 出现次数小于10次 的招法，可根据需要调整数值
   if child_c < parent_c * 0.01 or child_c < 10:
       child.delete()
   ```

4. **统计叶节点**
   
   统计定式树包含的变化数量
   ```python
   file_path = '.\\joseki_postprocessed.sgf' # 要统计的定式树
   ```

## 许可协议

本项目采用 [MIT 许可证](https://opensource.org/licenses/MIT) 发布，允许任何人自由使用、修改和分发代码，但需遵守以下条件：

1. **署名要求**：在使用或分发本项目的代码时，必须在显著位置标注原作者信息（即你的名字或项目链接）。

2. **免责声明**：作者不对代码的使用承担任何责任，使用者需自行承担风险。



---

## English

### Project Overview

This toolkit provides a complete solution for automatically extracting Go joseki patterns from KataGo's massive game records, including modules for game download, joseki extraction, structure optimization, and statistical analysis, generating standard SGF-format joseki trees.

### Key Features

1. **Batch Game Download**
   - Date-range specified download from KataGo archives
   - Automatic network request handling & chunked download
   - Compressed archive management

2. **Intelligent Joseki Extraction**
   - Multi-quadrant coordinate standardization
   - Automatic filtering of non-standard games (handicap/non-19x19)
   - Pass move processing
   - Color standardization (always black first)

3. **Joseki Tree Optimization**
   - Statistical-based pruning (frequency <1% or <10 occurrences)
   - Child node sorting by occurrence frequency
   - Node-level statistics (total count/B-W win rates)

4. **Visual Analysis**
   - Standard SGF viewer compatibility
   - Leaf node quantity statistics
   - Branch structure visualization

### Requirements

- Python 3.8+
- Dependencies:
  ```bash
  pip install requests sgfmill tqdm
  ```

### Quick Start

1. **Download Games**
   ```python
   # Modify in download_katago_archive.py:
   base_url = "https://katagoarchive.org/kata1/ratinggames/"
   start_date = "2025-01-01"  # Start date
   end_date = "2025-01-05"    # End date
   save_dir = ".\\sgf_archive"  # Storage path
   ```

2. **Extract Joseki**
   ```bash
   python extract_joseki.py
   ```

3. **Optimize Tree**
   ```bash
   python postprocess_joseki_tree.py
   ```

4. **Analyze Results**
   ```bash
   python count_leaf.py
   ```

### File Descriptions

| File                  | Description                          |
|-----------------------|--------------------------------------|
| download_katago_archive | Game downloader with resume support  |
| extract_joseki         | Core extraction engine with coordinate normalization |
| postprocess_joseki_tree | Tree optimization module            |
| count_leaf             | Statistical analysis module         |

### License

This project is licensed under the MIT License - see the LICENSE file for details.

---

_围棋人工智能研究团队 2025  
Go AI Research Team 2025_
