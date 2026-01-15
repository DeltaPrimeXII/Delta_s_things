#Utilities

class Vector2:
    """Class for using simple 2D vector"""
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
    
    def __eq__(self, other:"Vector2") -> bool:
        return self.x == other.x and self.y == other.y

    def __add__(self, other:"Vector2") -> "Vector2":
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other:"Vector2") -> "Vector2":
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, factor) -> "Vector2":
        if (type(factor) is int) or (type(factor) is float):
            return Vector2(self.x * factor, self.y * factor)
        elif type(factor) is Vector2:
            return Vector2(self.x * factor.x, self.y * factor.y)#Mathematicaly incorrect but i don't care

def dot(vec1:"Vector2", vec2:"Vector2") -> float:
    return (vec1.x * vec2.x) + (vec1.y * vec2.y)

def right_vector(vec:"Vector2"):
    return Vector2(vec.y, -(vec.x))

def symmetry(vec:"Vector2", normal:"Vector2"):
    """Return the symmetric of (vec) across the normal vector's surface"""
    axe = right_vector(normal)
    return (axe * dot(vec, axe) * 2) - vec

if __name__ == "__main__":
    test = Vector2(1, 2)
    print(test)
    abc = test + Vector2(3, 10)
    print(abc)
    test += Vector2(-1, -1)
    print(test)
    print(abc * 10)

    print(dot(test, abc))
    print(dot(Vector2(10,0), Vector2(0, 3)))