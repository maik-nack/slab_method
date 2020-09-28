class Edge:
    def __init__(self, v1: int, v2: int, f1: int, f2: int, p1: int, p2: int):
        self.v1 = v1
        self.v2 = v2
        self.f1 = f1
        self.f2 = f2
        self.p1 = p1
        self.p2 = p2

    def rotate180(self):
        self.v1, self.v2 = self.v2, self.v1
        self.f1, self.f2 = self.f2, self.f1
        self.p1, self.p2 = self.p2, self.p1
