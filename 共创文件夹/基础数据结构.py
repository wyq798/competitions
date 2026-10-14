# 线索二叉树
#@ 方法一 该方法一轮更新两个节点的指针，一个节点是前驱节点，更新他的右指针（当有指针为空的时候指向它的后继，后继就是当前遍历到的节点），然后再更新当前节点的前驱，也就是前面说的那个节点，这个过程中要注意，如果你的线索化采取的是先序/中序/后续来线索化那么你遍历的时候也必须用先序/中序/后续来遍历
# -*- coding: utf-8 -*-
"""
线索二叉树：先序线索化、中序线索化、后序线索化（含各自的线索遍历）

节点指针规则：
    ltag = 0 → left 指向左孩子；ltag = 1 → left 指向前驱（线索）
    rtag = 0 → right 指向右孩子；rtag = 1 → right 指向后继（线索）

三种线索化思路完全一致（用 pre 记录前驱，先序/中序/后序只是"处理节点"的时机不同）：
    ① 当前节点无左孩子 → left 指向前驱
    ② 前驱节点无右孩子 → 前驱的 right 指向当前节点（即前驱的后继）
"""


class ThreadNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.ltag = 0       # 0: 左孩子  1: 前驱线索
        self.rtag = 0       # 0: 右孩子  1: 后继线索
        self.parent = None  # 父指针：后序线索树的遍历需要它


def build_tree():
    """构造示例树（返回根节点和全部节点列表）
             A
           /   \
          B     C
         / \   / \
        D   E F   G
    """
    a, b, c = ThreadNode('A'), ThreadNode('B'), ThreadNode('C')
    d, e, f, g = ThreadNode('D'), ThreadNode('E'), ThreadNode('F'), ThreadNode('G')
    a.left, a.right = b, c
    b.left, b.right = d, e
    c.left, c.right = f, g
    for par, ch in ((a, b), (a, c), (b, d), (b, e), (c, f), (c, g)):
        ch.parent = par
    return a, [a, b, c, d, e, f, g]


# ==================== 普通递归遍历（对照验证用） ====================

def preorder_rec(node, res):
    if node:
        res.append(node.data)
        preorder_rec(node.left, res)
        preorder_rec(node.right, res)


def inorder_rec(node, res):
    if node:
        inorder_rec(node.left, res)
        res.append(node.data)
        inorder_rec(node.right, res)


def postorder_rec(node, res):
    if node:
        postorder_rec(node.left, res)
        postorder_rec(node.right, res)
        res.append(node.data)


# ==================== 三种线索化 ====================

def in_thread(root):
    """中序线索化（最经典的版本）
    按中序访问每个节点（先左子树 → 节点 → 右子树）：
      ① 节点无左孩子 → left 指向前驱
      ② 前驱无右孩子 → 前驱的 right 指向当前节点（后继）
    """
    pre = [None]  # 记录中序前驱（用列表实现递归闭包里的可变引用）

    def dfs(node):
        if node is None:
            return
        dfs(node.left)                     # 先访问左子树
        if node.left is None:              # ① 建立当前节点的前驱线索
            node.left = pre[0]
            node.ltag = 1
        if pre[0] is not None and pre[0].right is None:  # ② 建立前驱节点的后继线索
            pre[0].right = node
            pre[0].rtag = 1
        pre[0] = node                      # 更新前驱
        dfs(node.right)                    # 最后访问右子树

    dfs(root)


def pre_thread(root):
    """先序线索化
    和中序思路一样，只是"处理节点"的时机在最前。
    ⚠️ 关键区别：递归进入子树前必须判断 ltag / rtag——
       因为 left/right 可能已经被改成线索，直接递归会顺着线索绕圈（死循环）。
    """
    pre = [None]

    def dfs(node):
        if node is None:
            return
        if node.left is None:              # ① 建立当前节点的前驱线索
            node.left = pre[0]
            node.ltag = 1
        if pre[0] is not None and pre[0].right is None:  # ② 建立前驱节点的后继线索
            pre[0].right = node
            pre[0].rtag = 1
        pre[0] = node
        if node.ltag == 0:                 # 左指针仍是孩子才递归（防止踩进线索死循环）
            dfs(node.left)
        if node.rtag == 0:                 # 右指针仍是孩子才递归
            dfs(node.right)

    dfs(root)


def post_thread(root):
    """后序线索化
    线索化本身与中序完全同构：先递归左右子树，最后处理节点（后序）。
    ⚠️ 与中序/先序的真正区别在"遍历"阶段：
       后序中，有右孩子的节点的后继要"回溯到父节点"，
       所以后序线索遍历必须借助 parent 指针（build_tree 里已建立）。
    """
    pre = [None]

    def dfs(node):
        if node is None:
            return
        dfs(node.left)                     # 先左
        dfs(node.right)                    # 再右
        if node.left is None:              # ① 当前节点的前驱线索
            node.left = pre[0]
            node.ltag = 1
        if pre[0] is not None and pre[0].right is None:  # ② 前驱节点的后继线索
            pre[0].right = node
            pre[0].rtag = 1
        pre[0] = node                      # 最后处理节点（后序）

    dfs(root)


# ==================== 三种线索遍历 ====================

def inorder_traverse(root):
    """中序线索遍历：不需要栈，沿线索走即可"""
    res = []
    p = root
    while p is not None and p.ltag == 0:   # 先走到中序第一个节点（最左下的节点）
        p = p.left
    while p is not None:
        res.append(p.data)
        if p.rtag == 1:                    # 右指针是后继线索 → 直接跳过去
            p = p.right
        else:                              # 右指针是右孩子 → 后继是右子树最左下的节点
            p = p.right
            while p is not None and p.ltag == 0:
                p = p.left
    return res


def preorder_traverse(root):
    """先序线索遍历：后继规则最简单
    有左孩子 → 后继就是左孩子；否则右指针（孩子或线索）就是后继
    """
    res = []
    p = root
    while p is not None:
        res.append(p.data)
        p = p.left if p.ltag == 0 else p.right
    return res


def post_first(node):
    """后序第一个节点：沿"左孩子优先、否则右孩子"一路向下直到叶子"""
    while node is not None and (node.ltag == 0 or node.rtag == 0):
        node = node.left if node.ltag == 0 else node.right
    return node


def post_next(p):
    """后序线索树求后继（需要 parent 指针）"""
    if p.rtag == 1:                        # 右指针是后继线索 → 直接返回
        return p.right
    par = p.parent                         # 有真实右孩子：需要回溯父节点
    if par is None:                        # 根节点：遍历结束
        return None
    if par.left is p and par.rtag == 0 and par.right is not None:
        return post_first(par.right)       # p 是父的左孩子且父有右子树 → 后继在右子树里
    return par                             # 其余情况：后继就是父节点


def postorder_traverse(root):
    """后序线索遍历"""
    res = []
    p = post_first(root)
    while p is not None:
        res.append(p.data)
        p = post_next(p)
    return res


# ==================== 演示 ====================

def show_threads(nodes):
    """打印每个节点的指针状态，直观看到线索指向谁"""
    for n in nodes:
        if n.ltag == 1:
            left = f"前驱->{n.left.data if n.left else '∅'}"
        else:
            left = f"左孩->{n.left.data if n.left else '∅'}"
        if n.rtag == 1:
            right = f"后继->{n.right.data if n.right else '∅'}"
        else:
            right = f"右孩->{n.right.data if n.right else '∅'}"
        print(f"  {n.data}: [{left}] [{right}]")


if __name__ == '__main__':
    # ---- 中序 ----
    root, nodes = build_tree()
    ref = []
    inorder_rec(root, ref)      # 先递归遍历留底（线索化后递归会顺着线索死循环）
    in_thread(root)
    print("中序线索化：")
    show_threads(nodes)
    print("  线索遍历:", inorder_traverse(root))
    print("  递归对照:", ref)

    # ---- 先序 ----
    root, nodes = build_tree()
    ref = []
    preorder_rec(root, ref)
    pre_thread(root)
    print("\n先序线索化：")
    show_threads(nodes)
    print("  线索遍历:", preorder_traverse(root))
    print("  递归对照:", ref)

    # ---- 后序 ----
    root, nodes = build_tree()
    ref = []
    postorder_rec(root, ref)
    post_thread(root)
    print("\n后序线索化：")
    show_threads(nodes)
    print("  线索遍历:", postorder_traverse(root))
    print("  递归对照:", ref)



# 方法二
class Node:
    def __init__(self,val=None):
        self.val = val
        self.left = self.right = None
        self.rtag = self.ltag = 0
        self.father = None

class TBT:
    def __init__(self):
        self.root = Node()

    def build_tree(self):
        def solution(node):
            n = input()
            if n == "#":          # 修复：原 is 对 input() 的字符串永远为 False，输 # 无法结束递归
                return None
            node.val = n

            node.left = Node()
            node.left.father = node
            solution(node.left)

            node.right = Node()
            node.right.father = node
            solution(node.right)

        solution(self.root)

    def inorder_traverse(self):
        pre = [None]              # 中序前驱（原代码把左线索指向父节点是错的，前驱≠父节点）
        def solution(node):
            if node.val is None:
                return
            solution(node.left)
            if node.left.val is None:
                node.left = pre[0]  # 左孩子为空 → 左指针改指中序前驱
                node.ltag = 1
            if pre[0] is not None and pre[0].right.val is None:
                pre[0].right = node  # 前驱右孩子为空 → 右指针改指当前节点（后继）
                pre[0].rtag = 1
            pre[0] = node
            solution(node.right)
        solution(self.root)

    def inorder(self):
        if self.root.val is None:  # 空树
            return []
        p = self.root
        ans = []
        while p.ltag == 0 and p.left.val is not None:  # 用 ltag 判断，防止踩进线索
            p = p.left
        ans.append(p.val)
        while p.val is not None:
            if p.rtag == 1:
                if p.right is not None and p.right.val is not None:
                    ans.append(p.right.val)  # 修复：原 append(p.right) 附的是节点对象
                p = p.right
            else:
                q = p.right
                while q.val is not None and q.ltag == 0:  # 哨兵节点 left 为 None，必须加判断
                    q = q.left
                if q.val is not None:
                    ans.append(q.val)
                p = q
        return ans

    def preorder_traverse(self):
        pre = [None]              # 先序前驱（原代码用 father 推前驱的逻辑有误，改为 pre 指针）
        def solution(node):
            if node.val is None:
                return
            if node.left.val is None:
                node.left = pre[0]  # 左孩子为空 → 左指针改指先序前驱
                node.ltag = 1
            if pre[0] is not None and pre[0].right.val is None:
                pre[0].right = node  # 前驱右孩子为空 → 右指针改指当前节点（后继）
                pre[0].rtag = 1
            pre[0] = node
            if node.ltag == 0:      # 指针可能已被改成线索，必须判断后再递归，否则死循环
                solution(node.left)
            if node.rtag == 0:
                solution(node.right)
        solution(self.root)

    def preorder(self):
        if self.root.val is None:
            return []
        p = self.root
        ans = [p.val]
        while p.val is not None:
            if p.rtag == 1:
                if p.right is not None and p.right.val is not None:
                    ans.append(p.right.val)
                p = p.right
            else:
                if p.ltag == 0:       # 有真实左孩子 → 后继是左孩子
                    ans.append(p.left.val)
                    p = p.left
                else:                 # 左指针是线索 → 后继是右指针
                    if p.right.val is not None:
                        ans.append(p.right.val)
                    p = p.right
        return ans

    def postorder_traverse(self):
        pre = [None]              # 后序前驱（原 node.left = node.right 是错的，左线索只能靠 pre）
        def solution(node):
            if node.val is None:
                return
            solution(node.left)
            solution(node.right)
            if node == self.root and node.right.val is None:
                node.rtag = 1     # 根无右孩子：空哨兵 + rtag=1 作为遍历结束标记
            if node.left.val is None:
                node.left = pre[0]  # 左孩子为空 → 左指针改指后序前驱
                node.ltag = 1
            if node != self.root and node.right.val is None:
                if node == node.father.left and node.father.right.val is not None:
                    # 后继 = 父右子树的后序第一个节点（左优先、否则右）
                    p = node.father.right
                    while p.left.val is not None or p.right.val is not None:
                        p = p.left if p.left.val is not None else p.right
                    node.right = p
                    node.rtag = 1
                elif node == node.father.left and node.father.right.val is None or node == node.father.right:
                    node.right = node.father  # 后继 = 父节点
                    node.rtag = 1
            pre[0] = node
        solution(self.root)

    def postorder(self):
        if self.root.val is None:
            return []
        p = self.root
        ans = []
        while p.ltag == 0 or p.rtag == 0:     # 后序第一个节点：左优先、否则右（用 ltag/rtag 防踩线索）
            p = p.left if p.ltag == 0 else p.right
        ans.append(p.val)
        while p is not None and p.val is not None:
            if p.rtag == 1:
                if p.right is not None and p.right.val is not None:
                    ans.append(p.right.val)
                p = p.right
            else:
                if p.father is None:          # 根节点 → 结束（原代码此处 p.father.left 直接报错）
                    p = p.father
                elif p == p.father.left and p.father.right.val is not None:
                    p = p.father.right
                    while p.ltag == 0 or p.rtag == 0:
                        p = p.left if p.ltag == 0 else p.right
                    ans.append(p.val)
                elif p == p.father.left and p.father.right.val is None or p == p.father.right:
                    p = p.father
                    ans.append(p.val)
                else:
                    p = p.father
        return ans
