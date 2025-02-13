"""
该脚本用于从大量压缩包中的围棋棋谱文件中提取定式(joseki)，构建定式树并保存为SGF文件。
"""

import os
import json
import tarfile

from sgfmill import sgf



def extract_joseki(f, max_len=45):
    """
    从SGF棋谱文件中提取四个象限的定式序列
    参数:
        f: 文件对象
        max_len: 定式最大长度(默认45步)
    返回:
        tuple: (四个定式列表的元组, 获胜方)
    处理逻辑:
        1. 校验棋盘规格(19路)和让子情况
        2. 遍历棋谱着法记录
        3. 根据落子位置分配到四个象限(进行坐标翻转)
        4. 处理虚着(pass)情况
        5. 当定式达到最大长度时停止收集
    """
    try:
        sgf_game = sgf.Sgf_game.from_bytes(f.read())  # 解析SGF文件
    except:
        return [], None

    root = sgf_game.get_root()
    
    # 校验棋盘规格和初始设置(排除/非19路/让子棋/预制棋子)
    if root.get_size() != 19 or root.get_raw('HA') != b'0' or root.has_setup_stones():
        return [], None
    
    J1, J2, J3, J4 = [], [], [], []  # 分别对应四个象限的定式序列
    
    # 遍历棋谱主要着法序列
    for node in sgf_game.get_main_sequence_below(root):
        color, move = node.get_move()

        if color: # 过滤无颜色信息节点(通常是棋谱结果标记)
            if move is not None: # 如果是正常落子
                row, col = move
                # 将落子位置映射到四个象限并标准化坐标
                # 象限划分标准：将棋盘分为四个10x10区域
                # 通过翻转操作将定式转换到右上区域
                if len(J1) < max_len and 0 <= row <= 9 and 0 <= col <= 9:    # 原左下象限
                    _add_move(J1, color, (18 - row, 18 - col))  # 翻转至右上
                if len(J2) < max_len and 0 <= row <= 9 and 9 <= col <= 18:   # 原右下象限
                    _add_move(J2, color, (18 - row, col))       # 垂直翻转
                if len(J3) < max_len and 9 <= row <= 18 and 0 <= col <= 9:  # 原左上象限
                    _add_move(J3, color, (row, 18 - col))       # 水平翻转
                if len(J4) < max_len and 9 <= row <= 18 and 9 <= col <= 18: # 原右上象限
                    _add_move(J4, color, move)                   # 保持原坐标
            else: # 如果是虚着，同时添加到四个定式里
                for J in [J1, J2, J3, J4]:
                    J.append((color, None))
            
            if all(len(J) >= max_len for J in [J1, J2, J3, J4]):
                break  # 所有定式达最大长度时提前终止

    return (J1, J2, J3, J4), sgf_game.get_winner()

def _add_move(joseki_list, color, move):
    """ 内部辅助函数：添加着法到定式列表，处理连续同色落子 """
    if joseki_list and color == joseki_list[-1][0]:
        # 连续同色落子，则在中间插入虚着(pass)
        opponent = 'w' if color == 'b' else 'b'
        joseki_list.append((opponent, None))
    joseki_list.append((color, move))

def white_to_black(joseki, winner):
    """
    标准化定式序列为黑棋先行
    参数:
        joseki: 原始定式序列
        winner: 原始获胜方
    返回:
        tuple: (标准化后的定式序列, 调整后的获胜方)
    """
    if not joseki:
        return joseki, winner
    
    if joseki[0][0] == 'w': # 如果原始定式是白棋先行
        # 翻转所有着法颜色
        new_joseki = [('b' if c == 'w' else 'w', m) for c, m in joseki]
        new_winner = 'b' if winner == 'w' else 'w' if winner else None
        return new_joseki, new_winner
    return joseki, winner

def diag_filp(joseki):
    """
    沿主对角线翻转定式序列，确保首个非对角线落子在对角线下方区域
    参数:
        joseki: 原始定式序列
    返回:
        翻转后的定式序列(必要时)
    逻辑:
        检查首个非对角线落子位置，如果位于右上方则翻转坐标
    """
    for m in joseki:
        color, move = m
        if move is None:
            continue
        row, col = move
        if row == col:
            continue
        # 确定是否需要翻转：首个非对角线落子若落在对角线上方，则通过 (row, col) -> (col, row) 翻转到下方
        if row > col:
            return [(c, (m[1], m[0]) if m else None) for c, m in joseki]
        else:
            return joseki
    return joseki



# 初始化定式树数据结构
joseki_tree = sgf.Sgf_game(size=19)  # 创建19路棋盘为根的SGF树

# 配置路径参数
ARCHIVE_FOLDER = r'.\\sgf_archive'
OUTPUT_PATH = r".\\joseki.sgf"

def process_archives():
    """
    批量处理压缩包文件的主流程
    步骤:
        1. 遍历目录获取所有.tar.bz2文件路径
        2. 逐个解压处理内部SGF文件
        3. 对每个有效棋谱提取定式并更新定式树
    异常处理:
        捕获并打印处理异常，避免单个文件错误导致中断
    """
    archive_files = [os.path.join(root, f) 
                    for root, _, files in os.walk(ARCHIVE_FOLDER) 
                    for f in files if f.endswith('.tar.bz2')]

    for archive_path in archive_files:
        try:
            with tarfile.open(archive_path, 'r:bz2') as tar:
                total = len(tar.getmembers()[:6000])
                for idx, member in enumerate(tar.getmembers()[:6000]):
                    print(f"Processing {idx+1}/{total} in {archive_path} - {member.name}")
                    if not _valid_member(member):
                        continue
                    
                    with tar.extractfile(member) as f:
                        # 提取并处理定式
                        josekis, winner = extract_joseki(f)
                        if not josekis:
                            continue
                        
                        # 更新定式树
                        for seq in josekis:
                            processed_seq, adj_winner = white_to_black(diag_filp(seq), winner)
                            _update_tree(processed_seq, adj_winner)

        except Exception as e:
            print(f"Error processing {archive_path}: {str(e)}")

def _valid_member(member):
    """验证压缩包成员是否为有效SGF文件"""
    return member.isfile() and member.name.endswith('.sgf')

def _update_tree(joseki, winner):
    """
    将定式序列更新到定式树中
    参数:
        joseki: 标准化后的定式序列
        winner: 调整后的获胜方
    逻辑:
        1. 从根节点开始逐着法匹配
        2. 存在相同着法则更新统计信息
        3. 无匹配则创建新节点
    """
    current_node = joseki_tree.get_root()
    for color, move in joseki:
        found = False
        # 在现有子节点中查找匹配着法
        for child in current_node:
            if child.get_move() == (color, move):
                # 更新现有节点统计
                _update_node_stats(child, winner)
                current_node = child
                found = True
                break
        if not found:
            # 创建新节点并初始化统计
            new_node = current_node.new_child()
            new_node.set_move(color, move)
            new_node.set("C", json.dumps({'count': 1, 'b_win': 1 if winner == 'b' else 0, 'w_win': 1 if winner == 'w' else 0}))
            current_node = new_node

def _update_node_stats(node, winner):
    """更新节点统计信息"""
    try:
        stats = json.loads(node.get("C"))
    except:
        stats = {'count': 0, 'b_win': 0, 'w_win': 0}
    
    stats['count'] += 1
    if winner == 'b':
        stats['b_win'] += 1
    elif winner == 'w':
        stats['w_win'] += 1
    node.set("C", json.dumps(stats))

def save_joseki_tree():
    """序列化并保存定式树，带进度显示"""
    tree_data = joseki_tree.serialise()
    with open(OUTPUT_PATH, "wb") as f:
        total = len(tree_data)
        written = 0
        while written < total:
            chunk = tree_data[written:written+1024*1024]  # 分块写入(1MB)
            f.write(chunk)
            written += len(chunk)
            print(f"Save progress: {written/total:.1%}", end='\r')
    print("\nSave complete.")

if __name__ == "__main__":
    process_archives()
    save_joseki_tree()