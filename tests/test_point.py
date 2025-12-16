"""
Unit tests for Point2D class
"""
import unittest
import math
from point import Point2D


class TestPoint2D(unittest.TestCase):
    """Point2Dクラスのテストケース"""
    
    def test_init(self):
        """初期化のテスト"""
        point = Point2D(3, 4)
        self.assertEqual(point.x, 3)
        self.assertEqual(point.y, 4)
    
    def test_distance_to_same_point(self):
        """同じ点との距離のテスト"""
        point1 = Point2D(0, 0)
        point2 = Point2D(0, 0)
        self.assertEqual(point1.distance_to(point2), 0.0)
    
    def test_distance_to_horizontal(self):
        """水平方向の距離のテスト"""
        point1 = Point2D(0, 0)
        point2 = Point2D(3, 0)
        self.assertEqual(point1.distance_to(point2), 3.0)
    
    def test_distance_to_vertical(self):
        """垂直方向の距離のテスト"""
        point1 = Point2D(0, 0)
        point2 = Point2D(0, 4)
        self.assertEqual(point1.distance_to(point2), 4.0)
    
    def test_distance_to_diagonal(self):
        """対角線方向の距離のテスト（3-4-5三角形）"""
        point1 = Point2D(0, 0)
        point2 = Point2D(3, 4)
        self.assertEqual(point1.distance_to(point2), 5.0)
    
    def test_distance_to_negative_coordinates(self):
        """負の座標での距離のテスト"""
        point1 = Point2D(-3, -4)
        point2 = Point2D(0, 0)
        self.assertEqual(point1.distance_to(point2), 5.0)
    
    def test_distance_symmetry(self):
        """距離の対称性のテスト"""
        point1 = Point2D(1, 2)
        point2 = Point2D(4, 6)
        self.assertEqual(point1.distance_to(point2), point2.distance_to(point1))
    
    def test_str_representation(self):
        """文字列表現のテスト"""
        point = Point2D(3, 4)
        self.assertEqual(str(point), "Point2D(3, 4)")
    
    def test_str_representation_negative(self):
        """負の座標の文字列表現のテスト"""
        point = Point2D(-1, -2)
        self.assertEqual(str(point), "Point2D(-1, -2)")
    
    def test_distance_floating_point(self):
        """浮動小数点座標での距離のテスト"""
        point1 = Point2D(1.5, 2.5)
        point2 = Point2D(4.5, 6.5)
        expected = math.sqrt((4.5 - 1.5) ** 2 + (6.5 - 2.5) ** 2)
        self.assertAlmostEqual(point1.distance_to(point2), expected, places=10)


if __name__ == '__main__':
    unittest.main()
