"""
过滤给定定式树一些不常用的分支，并按照出现次数排序子节点
"""

import json
from sgfmill import sgf

# 输入文件路径
INPUT_FILE = r'.\\joseki.sgf'
# 输出文件路径
OUTPUT_FILE = r'.\\joseki_postprocessed.sgf'

def main():
    # 加载SGF文件
    with open(INPUT_FILE, "rb") as f:
        game = sgf.Sgf_game.from_bytes(f.read())

    def process_node(node, depth=0):
        """
        递归处理节点并执行以下操作：
        1. 删除C值小于父节点1%或小于10的子节点
        2. 对子节点按C值降序排序
        
        参数:
            node: 当前处理的节点对象
            depth: 当前节点在树中的深度（用于进度显示）
        """
        # 显示当前处理进度
        move = node.get_move()
        if move is not None:
            c, m = move
            print(f"Processing depth {depth}: {c} {m}" + " "*20, end='\r')
        else:
            print(f"Starting to process root node (depth {depth})", end='\r')

        children = list(node)  # 获取当前节点的所有子节点副本

        if not children:
            return  # 递归终止条件

        # 计算父节点C值（根节点特殊处理）
        if node is game.get_root():
            parent_c = sum(json.loads(child.get("C"))['count'] for child in children)
        else:
            parent_c = json.loads(node.get("C"))['count']

        # 第一轮遍历：删除不符合条件的子节点
        for child in children:
            child_c = json.loads(child.get("C"))['count']
            
            # 删除条件：C值小于父节点1% 或 小于10次
            if child_c < parent_c * 0.01 or child_c < 10:
                child.delete()
            else:
                # 递归处理子节点（深度+1）
                process_node(child, depth + 1)

        # 第二轮处理：对剩余子节点排序
        remaining_children = list(node)
        if len(remaining_children) > 1:
            # 按C值降序排序
            sorted_children = sorted(
                remaining_children,
                key=lambda x: -json.loads(x.get("C"))['count']
            )
            # 重新调整节点顺序
            for idx, child in enumerate(sorted_children):
                child.reparent(node, idx)

    # 从根节点开始处理
    process_node(game.get_root())

    # 保存处理后的SGF文件
    with open(OUTPUT_FILE, "wb") as f:
        f.write(game.serialise())
    print(f"Processing complete. Results have been saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()