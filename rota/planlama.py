"""8.1 Basit rota planlama: A* ile engellerden kacan rota."""
import heapq
import math


def engel_haritasi(genislik, yukseklik, engeller, guvenlik=3.0):
    """Engele guvenlik mesafesinden yakin hucreleri kapali sayar."""
    kapali = set()
    for x in range(genislik):
        for y in range(yukseklik):
            for ex, ey in engeller:
                if math.hypot(x - ex, y - ey) <= guvenlik:
                    kapali.add((x, y))
                    break
    return kapali