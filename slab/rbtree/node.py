import enum

from typing import Union

from dcel import Edge


class Color(enum.Enum):
    red = 0
    black = 1


class RBNode:
    def __init__(self, version: int, color: Color, edge: Union[Edge, None], left: 'RBNode' = None,
                 right: 'RBNode' = None):
        self.version = version
        self.color = color
        self.edge = edge
        self.left = left
        self.right = right

    def _repr_edge(self):
        return self.edge.__repr__() if self.edge is not None else None

    def __repr__(self):
        return f'<RBNode version={self.version} color={self.color} ' \
               f'edge={self._repr_edge()} left={self.left._repr_edge() if self.left is not None else None} ' \
               f'right={self.right._repr_edge() if self.right is not None else None}>'

    def copy(self, version: int = None) -> 'RBNode':
        if version == self.version:
            return self
        if version is None:
            version = self.version
        return RBNode(version, self.color, self.edge, self.left, self.right)
