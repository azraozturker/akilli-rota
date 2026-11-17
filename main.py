"""Dort parcayi tek senaryoda birlestirir."""
import math
import matplotlib.pyplot as plt

from rota.planlama import engel_haritasi, astar
from rota.sadelestirme import douglas_peucker
from rota.xte import roll_komutu, G
from rota.yaklasma import yaklasma_simulasyonu

HUCRE = 50.0  # bir harita hucresi kac metre