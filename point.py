import math


class Point2D:
    """
    2次元座標上の点を表すクラス
    
    2次元空間上の点を表現し、他の点との距離計算をサポートします。
    
    Attributes:
        x: X座標
        y: Y座標
    """
    
    def __init__(self, x, y):
        """
        Point2Dインスタンスを初期化
        
        Args:
            x: X座標
            y: Y座標
        """
        self.x = x
        self.y = y

    def distance_to(self, other):
        """
        別の点までのユークリッド距離を計算
        
        Args:
            other: 距離を計算する対象のPoint2Dインスタンス
        
        Returns:
            2点間のユークリッド距離
        
        Example:
            >>> p1 = Point2D(0, 0)
            >>> p2 = Point2D(3, 4)
            >>> p1.distance_to(p2)
            5.0
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def __str__(self):
        """
        文字列表現を返す
        
        Returns:
            Point2D(x, y)形式の文字列
        """
        return f"Point2D({self.x}, {self.y})"
