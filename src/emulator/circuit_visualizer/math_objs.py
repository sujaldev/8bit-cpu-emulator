class Vector:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = float(x)
        self.y = float(y)

    @property
    def xy(self):
        return self.x, self.y

    def __add__(self, other: "Vector"):
        return Vector(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(self, other: "Vector"):
        return Vector(
            self.x - other.x,
            self.y - other.y,
        )
