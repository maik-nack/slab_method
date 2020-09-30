from typing import Callable, List, Tuple

from .node import Color, RBNode
from dcel import Edge


class RBTree:
    null: RBNode
    roots: List[RBNode]
    edge_compare: Callable[[Edge, Edge], bool]

    def __init__(self, edge_compare: Callable[[Edge, Edge], bool]):
        """
        :param edge_compare: function for comparison of two edges that returns True if first edge is `less` than second
        """
        self.null = RBNode(0, Color.black, None, None)
        self.roots = [self.null]
        self.version = 0
        self.edge_compare = edge_compare

    def get_root(self, version: int = None) -> RBNode:
        return self.roots[self.version] if version is None else self.roots[version]

    root = property(get_root)

    def increase_version(self):
        self.roots += [self.roots[self.version]]
        self.version += 1
        if self.roots[self.version] != self.null:
            self.roots[self.version] = self.roots[self.version].copy(self.version)

    def _rotate_left(self, x: RBNode, x_parent: RBNode):
        """
            (x_parent)           (x_parent)
                 |                    |
                (x)                  (y)
               /   \      --->      /   \
             (a)   (y)            (x)   (c)
                  /   \          /   \
                (b)   (c)      (a)   (b)
        """
        y = x.right
        x.right = y.left
        if x_parent == self.null:
            self.roots[x.version] = y
        elif x == x_parent.left:
            x_parent.left = y
        else:
            x_parent.right = y
        y.left = x

    def _rotate_right(self, y: RBNode, y_parent: RBNode):
        """
              (y_parent)           (y_parent)
                   |                    |
                  (y)                  (x)
                 /   \      --->      /   \
               (x)   (c)            (a)   (y)
              /   \                      /   \
            (a)   (b)                  (b)   (c)
        """
        x = y.left
        y.left = x.right
        if y_parent == self.null:
            self.roots[y.version] = x
        elif y == y_parent.left:
            y_parent.left = x
        else:
            y_parent.right = x
        x.right = y

    def _insert_fixup_case1(self, way: List[RBNode], i: int, uncle_ptr: str) -> int:
        """
            uncle_ptr - right:
                      (i-3)                    (i-3)
                        |                        |
                     (i-2,b)                  (i-2,r)
                    /       \      --->      /       \
                (i-1,r)    (u,r)         (i-1,b)    (u,b)
               /                        /
            (i,r)                    (i,r)
        """
        uncle = getattr(way[i - 2], uncle_ptr).copy(self.version)
        setattr(way[i - 2], uncle_ptr, uncle)
        way[i - 1].color = Color.black
        uncle.color = Color.black
        way[i - 2].color = Color.red
        return i - 2

    def _insert_fixup_case2(self, way: List[RBNode], i: int, sibling_ptr: str):
        """
            sibling_ptr - left: left rotate on parent of way[i]
        """
        getattr(self, f'_rotate_{sibling_ptr}')(way[i - 1], way[i - 2])
        way[i], way[i - 1] = way[i - 1], way[i]

    def _insert_fixup_case3(self, way: List[RBNode], i: int, uncle_ptr: str) -> Tuple[List[RBNode], int]:
        """
            uncle_ptr - right:
                      (i-3)                    (i-3)
                        |                        |
                     (i-2,b)                  (i-1,b)
                    /       \      --->      /       \
                (i-1,r)    (u,b)          (i,r)    (i-2,r)
               /                                          \
            (i,r)                                        (u,b)
        """
        way[i - 1].color = Color.black
        way[i - 2].color = Color.red
        getattr(self, f'_rotate_{uncle_ptr}')(way[i - 2], way[i - 3])
        way = way[:i - 2] + way[i - 1:]
        return way, i - 1

    def _insert_fixup(self, way: List[RBNode]):
        i = len(way) - 1
        while way[i - 1].color == Color.red:
            if way[i - 1] == way[i - 2].left:
                if way[i - 2].right.color == Color.red:
                    i = self._insert_fixup_case1(way, i, 'right')
                else:
                    if way[i] == way[i - 1].right:
                        self._insert_fixup_case2(way, i, 'left')
                    way, i = self._insert_fixup_case3(way, i, 'right')
            else:
                if way[i - 2].left.color == Color.red:
                    i = self._insert_fixup_case1(way, i, 'left')
                else:
                    if way[i] == way[i - 1].left:
                        self._insert_fixup_case2(way, i, 'right')
                    way, i = self._insert_fixup_case3(way, i, 'left')
        self.root.color = Color.black

    def _do_step_by_edge(self, node: RBNode, parent: RBNode, edge: Edge, is_left: bool,
                         way: List[RBNode]) -> Tuple[RBNode, RBNode, bool]:
        node = node.copy(self.version)
        if parent != self.null:
            if is_left:
                parent.left = node
            else:
                parent.right = node

        parent = node
        way.append(node)
        is_left = self.edge_compare(edge, node.edge)
        if is_left:
            node = node.left
        else:
            node = node.right
        return node, parent, is_left

    def insert(self, edge: Edge):
        node = RBNode(self.version, Color.red, edge, self.null, self.null)
        y = self.null
        x = self.root
        way = [y]
        is_left = True

        while x != self.null:
            x, y, is_left = self._do_step_by_edge(x, y, edge, is_left, way)

        if y == self.null:
            self.roots[self.version] = node
        elif is_left:
            y.left = node
        else:
            y.right = node
        way.append(node)
        self._insert_fixup(way)

    def _transplant(self, way: List[RBNode], node: RBNode, is_left: bool):
        if len(way) == 1:
            self.roots[self.version] = node
        elif is_left:
            way[-1].left = node
        else:
            way[-1].right = node

    def _get_way_to_min(self, node: RBNode) -> List[RBNode]:
        if node.version != self.version:
            node = node.copy(self.version)
        way_min = [node]
        node = node.left
        while node != self.null:
            node = node.copy(self.version)
            way_min[-1].left = node
            way_min.append(node)
            node = node.left
        return way_min

    def _delete_fixup_case1(self, way: List[RBNode], i: int, sibling: RBNode, i_ptr: str) -> Tuple[List[RBNode], int]:
        """
            child_ptr - left:
                  (i-2)                    (i-2)
                    |                        |
                 (i-1,b)                  (s,b)
                /       \      --->      /
            (i,b)      (s,r)         (i-1,r)
                                    /
                                 (i,b)
        """
        sibling.color = Color.black
        way[i - 1].color = Color.red
        getattr(self, f'_rotate_{i_ptr}')(way[i - 1], way[i - 2])
        way = way[:i - 1] + [sibling] + way[i - 1:]
        return way, i + 1

    def _delete_fixup_case2(self, i: int, sibling: RBNode) -> int:
        """
            repaint sibling to red if its both children are black
        """
        sibling.color = Color.red
        return i - 1

    def _delete_fixup_case3(self, way: List[RBNode], i: int, sibling: RBNode, sibling_ptr: str) -> RBNode:
        """
            sibling_ptr - right:
                 (i-2)                    (i-2)
                   |                        |
                (i-1,r)                  (i-1,r)
               /       \      --->      /       \
            (i,b)     (s,b)          (i,b)    (s.l,b)
                     /     \                         \
                 (s.l,r) (s.r,b)                    (s,r)
                                                         \
                                                       (s.r,b)
        """
        child_ptr = 'left' if sibling_ptr == 'right' else 'right'
        setattr(sibling, child_ptr, getattr(sibling, child_ptr).copy(self.version))
        getattr(sibling, child_ptr).color = Color.black
        sibling.color = Color.red
        getattr(self, f'_rotate_{sibling_ptr}')(sibling, way[i - 1])
        return getattr(way[i - 1], sibling_ptr)

    def _delete_fixup_case4(self, way: List[RBNode], i: int, sibling: RBNode,
                            sibling_ptr: str) -> Tuple[List[RBNode], int]:
        """
            sibling_ptr - right:
                 (i-2)                   (i-2)
                   |                       |
                (i-1,r)                  (s,r)
               /       \      --->      /     \
            (i,b)     (s,b)         (i-1,b) (s.r,b)
                     /     \       /       \
                 (s.l,r) (s.r,r)(i,b)    (s.l,r)
        """
        sibling.color = way[i - 1].color
        way[i - 1].color = Color.black
        setattr(sibling, sibling_ptr, getattr(sibling, sibling_ptr).copy(self.version))
        getattr(sibling, sibling_ptr).color = Color.black
        getattr(self, f"_rotate_{'left' if sibling_ptr == 'right' else 'right'}")(way[i - 1], way[i - 2])
        way = way[:i - 1] + [sibling] + way[i - 1:]
        return way, 1

    def _delete_fixup(self, way: List[RBNode]):
        i = len(way) - 1
        while way[i] != self.root and way[i].color == Color.black:
            if way[i] == way[i - 1].left:
                sibling = way[i - 1].right = way[i - 1].right.copy(self.version)
                if sibling.color == Color.red:
                    way, i = self._delete_fixup_case1(way, i, sibling, 'left')
                    sibling = way[i - 1].right = way[i - 1].right.copy(self.version)
                if sibling.left.color == Color.black and sibling.right.color == Color.black:
                    i = self._delete_fixup_case2(i, sibling)
                else:
                    if sibling.right.color == Color.black:
                        sibling = self._delete_fixup_case3(way, i, sibling, 'right')
                    way, i = self._delete_fixup_case4(way, i, sibling, 'right')
            else:
                sibling = way[i - 1].left = way[i - 1].left.copy(self.version)
                if sibling.color == Color.red:
                    way, i = self._delete_fixup_case1(way, i, sibling, 'right')
                    sibling = way[i - 1].left = way[i - 1].left.copy(self.version)
                if sibling.left.color == Color.black and sibling.right.color == Color.black:
                    i = self._delete_fixup_case2(i, sibling)
                else:
                    if sibling.left.color == Color.black:
                        sibling = self._delete_fixup_case3(way, i, sibling, 'left')
                    way, i = self._delete_fixup_case4(way, i, sibling, 'left')
        way[i].color = Color.black

    def delete(self, edge: Edge):
        y = self.null
        z = self.root
        way = [y]
        is_left = True

        while z != self.null and z.edge != edge:
            z, y, is_left = self._do_step_by_edge(z, y, edge, is_left, way)

        color = z.color
        if z == self.null:
            return
        elif z.left == self.null:
            x = z.right.copy(self.version) if z.right != self.null else z.right
            self._transplant(way, x, is_left)
            way.append(x)
        elif z.right == self.null:
            x = z.left.copy(self.version)
            self._transplant(way, x, is_left)
            way.append(x)
        else:
            way_min = self._get_way_to_min(z.right)
            y = way_min[-1]
            color = y.color
            x = y.right
            if x != self.null:
                x = x.copy(self.version)
                y.right = x
            if len(way_min) > 1:
                way_min[-2].left = x
                y.right = way_min[0]
            self._transplant(way, y, is_left)
            y.left = z.left
            y.color = z.color
            way += [y] + way_min[:-1] + [x]
        if color == Color.black:
            self._delete_fixup(way)
