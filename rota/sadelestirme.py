"""8.4 Rota sadelestirme: Douglas-Peucker algoritmasi"""
import math

def dik_uzaklik(p, a, b):
        """p noktasinin a-b dogrusuna dik uzakligi"""
        (px, py), (ax, ay), (bx, by) = p,a,b
        uzunluk = math.hypot(bx - ax, by - ay)
        if uzunluk == 0:
            return math.hypot(px - ax, py - ay)
        alan = abs((bx - ax) * (ay - py) - (ax - px) * (by - ay))
        return alan / uzunluk

def douglas_peucker (noktalar, epsilon):
      """epsilon'dan az sapan ara noktalari atarak sadelestirir"""
      if len(noktalar) < 3:
        return list(noktalar)
      en_uzak, indeks = 0.0, 0
      for i in range(1, len(noktalar) - 1):
           d = dik_uzaklik(noktalar[i], noktalar[0], noktalar[-1])
           if d > en_uzak:
               en_uzak, indeks = d, i
      if en_uzak > epsilon:
           sol = douglas_peucker(noktalar[:indeks + 1], epsilon)
           sag = douglas_peucker(noktalar[indeks:], epsilon)
           return sol[:-1] + sag
      return [noktalar[0], noktalar[-1]] 



      

