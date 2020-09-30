from typing import List

from dcel import Edge, Point


def get_area(edge: Edge, point: Point, vertexes: List[Point]) -> int:
    vertex1 = vertexes[edge.v1]
    vertex2 = vertexes[edge.v2]
    return vertex1.x * vertex2.y + vertex1.y * point.x + vertex2.x * point.y \
        - vertex2.y * point.x - vertex1.y * vertex2.x - vertex1.x * point.y
