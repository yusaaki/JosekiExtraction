from sgfmill import sgf

file_path = '.\\joseki_postprocessed.sgf'

with open(file_path, "rb") as f:
    joseki_tree = sgf.Sgf_game.from_bytes(f.read())

def count_leaf_nodes(node):
    children = list(node)
    # 如果没有子节点，当前节点是叶节点，返回1
    if not children:
        return 1
    # 否则递归统计所有子节点的叶节点数目之和
    return sum(count_leaf_nodes(child) for child in children)

# 调用函数并输出结果
leaf_count = count_leaf_nodes(joseki_tree.get_root())
print("count of variation (leaf nodes):", leaf_count)