import enum

from typing import Union

from dcel import Edge


class Color(enum.Enum):
    red = 0
    black = 1


class RBNode:
    def __init__(self, version: int, color: Color, edge: Union[Edge, None], key, left: 'RBNode' = None,
                 right: 'RBNode' = None):
        self.version = version
        self.color = color
        self.edge = edge
        self.key = key
        self.left = left
        self.right = right

    def copy(self, version: int = None) -> 'RBNode':
        if version == self.version:
            return self
        if version is None:
            version = self.version
        return RBNode(version, self.color, self.edge, self.key, self.left, self.right)
