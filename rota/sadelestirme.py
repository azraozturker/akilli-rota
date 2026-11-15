"""8.4 Rota sadelestirme: Douglas-Peucker algoritmasi."""
import math

def dik_uzaklik(p, a, b):
        """p noktasinin a-b dogrusuna dik uzakligi."""
        (px, py), (ax, ay), (bx, by) = p,a,b
        uzunluk = math.hypot(bx - ax, by - ay)
        if uzunluk == 0:
            return math.hypot(px - ax, py - ay)
        alan = abs((bx - ax) * (ay - py) - (ax - px) * (by - ay))
        return alan / uzunluk



