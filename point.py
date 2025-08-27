# 三次元空間の点を表すクラス
class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance_to(self, other):
        # TODO: ここに距離計算のコードを追加
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def __str__(self):
        # TODO: 文字列表現を返す
        return f"Point3D({self.x}, {self.y}, {self.z})"
    