class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'<Point ({self.x}, {self.y})>'

    def __iter__(self):
        yield self.x
        yield self.y
