"""
2D座標クラス - シンプルな2次元座標の表現
2D Point Class - Simple representation of 2D coordinates

2D空間での点の位置を管理し、距離計算などの基本的な幾何計算を提供します。
"""
import math

class Point2D:
    """
    2次元座標を表すクラス
    Class representing 2D coordinates
    
    Attributes:
        x (float): X座標 / X coordinate
        y (float): Y座標 / Y coordinate
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other):
        """
        他の点との距離を計算 / Calculate distance to another point
        
        Args:
            other (Point2D): 距離を計算する対象の点 / Target point for distance calculation
            
        Returns:
            float: ユークリッド距離 / Euclidean distance
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def __str__(self):
        """文字列表現 / String representation"""
        return f"Point2D({self.x}, {self.y})"
