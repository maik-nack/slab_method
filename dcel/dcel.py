from typing import Iterable, List

from .edge import Edge
from .point import Point


class DCEL:
    vertexes: List[Point]
    edges: List[Edge]
    incident_edge_indices: List[int]

    def __init__(self, vertexes: List[dict], edges: List[dict]):
        self.vertexes = [Point(**vertex_dict) for vertex_dict in vertexes]
        self.incident_edge_indices = [-1 for _ in range(len(self.vertexes))]
        self.edges = [self._init_edge(edge_dict) for edge_dict in edges]
        self._init_incident_edge_indices()

    def _init_edge(self, edge_dict: dict) -> Edge:
        edge = Edge(**edge_dict)
        if self.vertexes[edge.v1].y > self.vertexes[edge.v2].y:
            edge.rotate180()
        return edge

    def _init_incident_edge_indices(self):
        for edge_index, edge in enumerate(self.edges):
            for v in ['v1', 'v2']:
                vertex_index = getattr(edge, v)
                if self.incident_edge_indices[vertex_index] == -1:
                    self.incident_edge_indices[vertex_index] = edge_index
                else:
                    incident_edge = self.edges[self.incident_edge_indices[vertex_index]]
                    adjacent_vertex_index = incident_edge.v2 if incident_edge.v1 == vertex_index else incident_edge.v1
                    new_adjacent_vertex_index = edge.v2 if v == 'v1' else edge.v1
                    if self.vertexes[new_adjacent_vertex_index].x < self.vertexes[adjacent_vertex_index].x:
                        self.incident_edge_indices[vertex_index] = edge_index
        if -1 in self.incident_edge_indices:
            raise Exception('Incorrect graph: vertex without incident edges')

    def get_incident_edges_for_vertex(self, vertex_index: int) -> Iterable[Edge]:
        edge_index = first_edge_index = self.incident_edge_indices[vertex_index]
        while True:
            yield self.edges[edge_index]
            if self.edges[edge_index].v1 == vertex_index:
                if edge_index == self.edges[edge_index].p1:
                    raise Exception('Incorrect graph: pointer points on the same edge')
                edge_index = self.edges[edge_index].p1
            else:
                if edge_index == self.edges[edge_index].p2:
                    raise Exception('Incorrect graph: pointer points on the same edge')
                edge_index = self.edges[edge_index].p2
            if edge_index == first_edge_index:
                break
