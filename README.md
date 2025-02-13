# KataGo 定式库构建 / KataGo Joseki Library Construction

你可以直接下载提取好的定式：

You can directly download the extracted joseki.

[从训练对局中提取的定式 (Joseki extracted from training games)](https://github.com/yusaaki/JosekiExtraction/raw/main/katago_training_joseki.sgf)

[从评估对局中提取的定式 (Joseki extracted from rating games)](https://github.com/yusaaki/JosekiExtraction/raw/main/katago_rating_joseki.sgf)

![Joseki Example](https://github.com/yusaaki/JosekiExtraction/raw/main/joseki_example.png)

## 目录 / Table of Contents

### 中文
- [概述](#概述)
- [文件功能](#文件功能)
- [环境要求](#环境要求)
- [使用指南](#使用指南)
- [参考文献](#参考文献)
- [许可协议](#许可协议)

### English
- [Overview](#overview)
- [File Descriptions](#file-descriptions)
- [Environment Requirements](#environment-requirements)
- [Usage Guide](#usage-guide)
- [Reference](#reference)
- [License](#license)

---

## 中文

### 概述

本代码实现从KataGo海量棋谱（也可适应其他棋谱集）中自动提取围棋定式的功能，包含棋谱下载、定式提取筛选、统计分析等步骤，可生成标准SGF格式的定式树文件。

### 文件功能

| 文件名                  | 功能描述                              |
|-----------------------|-----------------------------------|
| download_katago_archive | 棋谱下载，支持指定日期范围下载KataGo官方存档            |
| extract_joseki         | 定式提取，含非标准对局过滤、坐标标准化与序列处理逻辑        |
| postprocess_joseki_tree | 定式树优化模块，实现分支修剪（去除出现频率<1%或<10次的分支）与子节点按局面出现频率排序 |
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
   # 修改 download_katago_archive.py 中的参数:
   base_url = "https://katagoarchive.org/kata1/ratinggames/" # 下载地址头，训练棋谱需改为 "https://katagoarchive.org/kata1/trainingdata/"
   start_date = "2025-01-01"  # 起始日期
   end_date = "2025-01-05"    # 结束日期
   save_dir = ".\\sgf_archive"  # 存储路径
   file_name = date.strftime("%Y-%m-%d") + "rating.tar.bz2" # 下载地址尾，训练棋谱需改为 + "npzs.tgz"
   ```

2. **提取定式**
   ```python
   # 修改 extract_joseki.py 中的参数：
   ARCHIVE_FOLDER = r'.\\sgf_archive' # 棋谱存储文件夹（需包含压缩包）
   OUTPUT_PATH = r".\\joseki.sgf"     # 初步提取的定式树输出路径
   max_len = 45                       # 定式长度（默认45手）
   # 角部坐标范围可在代码的坐标标准化部分调整
   ```

3. **优化定式树**
   ```python
   # 删除出现频率<1% 或 总次数<10 的分支（数值可调）
   if child_c < parent_c * 0.01 or child_c < 10:
       child.delete()
   ```

4. **统计叶节点**
   ```python
   file_path = '.\\joseki_postprocessed.sgf' # 待统计的定式树文件
   ```

### 参考文献

谷蓉,刘学民,朱仲涛,等.一种围棋定式的机器学习方法[J].计算机工程, 2004, 30(6):4.DOI:10.3969/j.issn.1000-3428.2004.06.056.

### 许可协议

本项目采用 [MIT 许可证](https://opensource.org/licenses/MIT) 发布，须遵守以下条款：
1. 使用或分发代码时须显著标注本项目信息
2. 作者不承担任何使用风险，使用者需自行负责

---

## English

### Overview

This code automates the extraction of Go joseki (established patterns) from KataGo's massive game records (Can also be adapted to other game collections). The pipeline includes game downloading, joseki extraction/filtering, statistical analysis, and generates SGF-format joseki trees.

### File Descriptions

| Filename               | Description                              |
|------------------------|------------------------------------------|
| download_katago_archive | Downloads game records with date range support from KataGo archives |
| extract_joseki         | Extracts joseki with non-standard game filtering, coordinate normalization, and sequence processing |
| postprocess_joseki_tree | Optimizes joseki tree by pruning branches (remove moves with <1% frequency or <10 occurrences) and sorting child nodes by position frequency |
| count_leaf             | Counts variations in joseki tree (number of leaf nodes) |

### Environment Requirements

- Windows 10
- Python 3.11.4
- Dependencies: 
  ```bash
  pip install requests sgfmill
  ```

### Usage Guide

1. **Download Games**
   ```python
   # Modify parameters in download_katago_archive.py:
   base_url = "https://katagoarchive.org/kata1/ratinggames/" # For training games, use "https://katagoarchive.org/kata1/trainingdata/"
   start_date = "2025-01-01"  # Start date
   end_date = "2025-01-05"    # End date
   save_dir = ".\\sgf_archive"  # Save path
   file_name = date.strftime("%Y-%m-%d") + "rating.tar.bz2" # For training data, use + "npzs.tgz"
   ```

2. **Extract Joseki**
   ```python
   # Configure extract_joseki.py:
   ARCHIVE_FOLDER = r'.\\sgf_archive' # Folder containing game archives
   OUTPUT_PATH = r".\\joseki.sgf"     # Output path for raw joseki tree
   max_len = 45                       # Maximum joseki length (default 45 moves)
   # Adjust corner coordinate range in normalization section
   ```

3. **Optimize Tree**
   ```python
   # Prune branches with <1% frequency OR <10 total occurrences (adjustable)
   if child_c < parent_c * 0.01 or child_c < 10:
       child.delete()
   ```

4. **Count Variations**
   ```python
   file_path = '.\\joseki_postprocessed.sgf' # Target joseki tree file
   ```

### Reference

Rong, G. U. , Xuemin, L. , Zhongtao, Z. , & Jie, Z. . (2004). A machine learning method of joseki database for computer go. Computer Engineering, 30(6), 142-143.

### License

This project is licensed under [MIT License](https://opensource.org/licenses/MIT):
1. Attribution is required when using/distributing the code.
2. Authors hold no liability. Users assume all risks.

--- 
