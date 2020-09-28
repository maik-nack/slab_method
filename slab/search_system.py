from typing import List

from dcel import Edge, DCEL, Point
from slab.rbtree import RBTree


class SearchSystem:
    dcel: DCEL
    tree: RBTree
    lines: List[int]

    def __init__(self, dcel: DCEL):
        self.dcel = dcel
        self.tree = RBTree()
        self.lines = []
        self._init_slabs()

    def _init_slabs(self):
        vertexes_count = len(self.dcel.vertexes)
        sorted_vertex_indexes = sorted(range(vertexes_count), key=lambda ind: tuple(self.dcel.vertexes[ind])[::-1])

        y = self.dcel.vertexes[sorted_vertex_indexes[0]].y
        i = 0
        while self.dcel.vertexes[sorted_vertex_indexes[i]].y == y:
            for edge in self.dcel.get_incident_edges_for_vertex(sorted_vertex_indexes[i]):
                if self.dcel.vertexes[edge.v2].y > y:
                    self.tree.insert(edge, (self.dcel.vertexes[edge.v2].x, self.dcel.vertexes[edge.v1].x))
            i += 1
        self.lines.append(y)

        while i < vertexes_count - 1:
            self.tree.increase_version()
            y = self.dcel.vertexes[sorted_vertex_indexes[i]].y
            while i < vertexes_count and self.dcel.vertexes[sorted_vertex_indexes[i]].y == y:
                for edge in self.dcel.get_incident_edges_for_vertex(sorted_vertex_indexes[i]):
                    key = (self.dcel.vertexes[edge.v2].x, self.dcel.vertexes[edge.v1].x)
                    if self.dcel.vertexes[edge.v2].y > y:
                        self.tree.insert(edge, key)
                    elif self.dcel.vertexes[edge.v1].y < y:
                        self.tree.delete(edge, key)
                i += 1
            self.lines.append(y)
        if i == vertexes_count - 1:
            self.lines.append(self.dcel.vertexes[sorted_vertex_indexes[i]].y)

    def _search_band(self, y: int) -> int:
        if y < self.lines[0] or y > self.lines[-1]:
            return -1
        lines_count = len(self.lines)
        l, r = -1, lines_count
        while r - l > 1:
            m = (l + r) // 2
            if self.lines[m] < y:
                l = m
            else:
                r = m
        if y == self.lines[r]:
            return r if r < lines_count - 1 else lines_count - 2
        return r - 1 if r > 0 else 0

    def _get_area(self, edge: Edge, point: Point) -> int:
        vertex1 = self.dcel.vertexes[edge.v1]
        vertex2 = self.dcel.vertexes[edge.v2]
        return vertex1.x * vertex2.y + vertex1.y * point.x + vertex2.x * point.y \
            - vertex2.y * point.x - vertex1.y * vertex2.x - vertex1.x * point.y

    def _search_face(self, point: Point, band_index: int) -> int:
        node = self.tree.get_root(band_index)
        while True:
            area = self._get_area(node.edge, point)
            if area == 0:
                return node.edge.f2 if node.edge.f2 != -1 else node.edge.f1
            elif area > 0:
                if node.left == self.tree.null:
                    return node.edge.f1
                node = node.left
            else:
                if node.right == self.tree.null:
                    return node.edge.f2
                node = node.right

    def locate_point(self, point: Point) -> int:
        band_index = self._search_band(point.y)
        if band_index == -1:
            return -1
        return self._search_face(point, band_index)
