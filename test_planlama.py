"""A* icin test senaryolari. Calistirma: python test_planlama.py"""
import math
from rota.planlama import engel_haritasi, astar, rota_uzunlugu

# 1) Engel yokken rota duz kosegen olmali
rota = astar((2, 2), (47, 47), set(), 50, 50)
kus_ucusu = math.dist((2, 2), (47, 47))
assert abs(rota_uzunlugu(rota) - kus_ucusu) < 0.01
print("Engelsiz senaryo gecti")

# 2) Rota hicbir kapali hucreye girmemeli
engeller = [(15, 15), (20, 22), (25, 25), (30, 28), (35, 35)]
kapali = engel_haritasi(50, 50, engeller)
rota = astar((2, 2), (47, 47), kapali, 50, 50)
for hucre in rota:
    assert hucre not in kapali
print("Engelli senaryo gecti")

# 3) Duvarda tek bosluk varsa rota o bosluktan gecmeli
duvar = set()
for y in range(50):
    if y != 40:
        duvar.add((25, y))
rota = astar((2, 2), (47, 47), duvar, 50, 50)
assert (25, 40) in rota
print("Dar gecit senaryosu gecti")

# 4) Yol tamamen kapaliysa None donmeli
duvar = set()
for y in range(50):
    duvar.add((25, y))
assert astar((2, 2), (47, 47), duvar, 50, 50) is None
print("Kapali yol senaryosu gecti")