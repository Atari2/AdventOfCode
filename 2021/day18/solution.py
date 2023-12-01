from __future__ import annotations
from typing import Union, Optional
from functools import reduce

def read_from_input():
    with open('input.txt', 'r') as f:
        return f.readlines()

class IntTreeNode:
    value: int
    parent: Optional[PairTreeNode]

    def __init__(self, value: int) -> None:
        self.value = value
    
    def __str__(self):
        return f"{self.value}"
    
    def reduce(self, depth: int = 0):
        if self.value >= 10:
            self.split()
            return True
    
    def split(self) -> PairTreeNode:
        node = PairTreeNode()
        node.parent = self.parent
        node.left = IntTreeNode(self.value // 2)
        node.left.parent = node
        node.right = IntTreeNode(self.value - node.left.value)
        node.right.parent = node
        if self.parent.left is self:
            self.parent.left = node
        else:
            self.parent.right = node
    
    def add_to_left_child(self, value: IntTreeNode):
        self.value += value.value

    def add_to_right_child(self, value: IntTreeNode):
        self.value += value.value

class PairTreeNode:
    left: Optional[Union[PairTreeNode, IntTreeNode]]
    right: Optional[Union[PairTreeNode, IntTreeNode]]
    parent: Optional[PairTreeNode]

    def __init__(self) -> None:
        self.left = None
        self.right = None
        self.parent = None
    
    def insert_leaf(self, value: Union[PairTreeNode, IntTreeNode]) -> None:
        if self.left == None:
            self.left = value
        elif self.right == None:
            self.right = value
        else:
            self.left.insert_leaf(value)

    def __str__(self) -> str:
        if not self.left and not self.right:
            return ""
        return f"[{self.left}, {self.right}]"

    def explode(self):
        assert(isinstance(self.left, IntTreeNode))
        assert(isinstance(self.right, IntTreeNode))
        temp = self.parent
        self.add_left_child(self.left)
        self.add_right_child(self.right)
        if temp.left is self:
            temp.left = IntTreeNode(0)
            temp.left.parent = temp
        else:
            temp.right = IntTreeNode(0)
            temp.right.parent = temp


    def reduce(self, depth: int = 0) -> bool:
        if depth >= 4:
            self.explode()
            return True
        if self.left and self.right:
            if self.left.reduce(depth + 1):
                return True
            elif self.right.reduce(depth + 1):
                return True
        return False

    def add_left_child(self, value: IntTreeNode):
        if not self.parent:
            return
        if self.parent.left is self:
            self.parent.add_left_child(value)
        else:
            self.parent.left.add_to_right_child(value)

    def add_right_child(self, value: IntTreeNode):
        if not self.parent:
            return
        if self.parent.right is self:
            self.parent.add_right_child(value)
        else:
            self.parent.right.add_to_left_child(value)

    def add_to_right_child(self, value: IntTreeNode):
        self.right.add_to_right_child(value)

    def add_to_left_child(self, value: IntTreeNode):
        self.left.add_to_left_child(value)

class PairTree:
    head: Optional[PairTreeNode]

    def __init__(self) -> None:
        self.head = None

    def insert_leaf(self, value: Union[PairTreeNode, IntTreeNode]) -> None:
        if self.head == None:
            self.head = value
        else:
            self.head.insert_leaf(value)

    def __str__(self) -> str:
        return f"{self.head}"

    def print(self) -> None:
        if self.head == None:
            print("Empty Tree")
        else:
            print(f"{self.head}")
    
    def __add__(self, other: PairTree):
        result = PairTree()
        result.head = PairTreeNode()
        result.head.left = self.head
        result.head.right = other.head
        self.head.parent = result.head
        other.head.parent = result.head
        return result
    
    def reduce(self):
        return self.head.reduce()

    @staticmethod
    def reduce_sum(a: PairTree, b: PairTree) -> PairTree:
        summed = a + b
        while summed.reduce():
            pass
        return summed


def parse_snail_number(number: str):
    stack: list[PairTreeNode] = []
    tree = PairTree()
    for c in number:
        if c == '[':
            stack.append(PairTreeNode())
        elif c == ']':
            right_node = stack.pop()
            left_node = stack.pop()
            parent_node = stack.pop()
            right_node.parent = parent_node
            left_node.parent = parent_node
            parent_node.left = left_node
            parent_node.right = right_node
            stack.append(parent_node)
        elif c == ',':
            pass
        else:
            stack.append(IntTreeNode(int(c)))
    tree.head = stack.pop()
    return tree

trees = []
for line in read_from_input():
    tree = parse_snail_number(line.strip())
    trees.append(tree)
tree_sum: PairTree = reduce(lambda x, y: PairTree.reduce_sum(x, y), trees)
tree_sum.print()