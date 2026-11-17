"""Dort parcayi tek senaryoda birlestirir."""
import math
import matplotlib.pyplot as plt

from rota.planlama import engel_haritasi, astar
from rota.sadelestirme import douglas_peucker
from rota.xte import roll_komutu, G
from rota.yaklasma import yaklasma_simulasyonu

HUCRE = 50.0  # bir harita hucresi kac metre

def rotayi_takip_et(rota_m, V=20.0, ruzgar=(0.0, 0.0), donus_payi=70.0, dt=0.05):
    """Aracin rota boyunca ruzgar altinda ucusunu simule eder."""
    x, y = rota_m[0]
    psi = math.atan2(rota_m[1][1] - y, rota_m[1][0] - x)  # burun yonu
    iz, sapmalar = [(x, y)], []
    parca = 0
    for _ in range(200000):
        (ax, ay), (bx, by) = rota_m[parca], rota_m[parca + 1]
        uzunluk = math.hypot(bx - ax, by - ay)
        tx, ty = (bx - ax) / uzunluk, (by - ay) / uzunluk  # rota yonu
        ileri = (x - ax) * tx + (y - ay) * ty  # rota boyunca yol
        xte = (x - ax) * ty - (y - ay) * tx  # saga sapma +

        son_parca = parca == len(rota_m) - 2
        if son_parca and ileri >= uzunluk:
            break
        if not son_parca and ileri >= uzunluk - donus_payi:
            parca += 1
            continue

        vx = V * math.cos(psi) + ruzgar[0]
        vy = V * math.sin(psi) + ruzgar[1]
        xte_hizi = vx * ty - vy * tx
        roll = roll_komutu(xte, xte_hizi)
        psi -= G * math.tan(math.radians(roll)) / V * dt  # saga roll saga dondurur
        x += vx * dt
        y += vy * dt
        iz.append((x, y))
        sapmalar.append(xte)
    return iz, sapmalar

if __name__ == "__main__":
    engeller = [(15, 15), (20, 22), (25, 25), (30, 28), (35, 35), (25, 10), (10, 30)]
    kapali = engel_haritasi(50, 50, engeller)
    rota = astar((2, 2), (47, 47), kapali, 50, 50)               # 8.1
    sade = douglas_peucker(rota, 1.0)                            # 8.4
    sade_m = [(x * HUCRE, y * HUCRE) for x, y in sade]
    iz, sapmalar = rotayi_takip_et(sade_m, ruzgar=(-4.0, 3.0))   # 8.3
    yaklasma = yaklasma_simulasyonu()                            # 8.2
    print("A*:", len(rota), "nokta, sade:", len(sade), "nokta")
    print("En buyuk sapma:", round(max(abs(s) for s in sapmalar), 1), "m")

    fig = plt.figure(figsize=(12, 6))

    harita = fig.add_subplot(1, 2, 1)
    harita.scatter([x * HUCRE for x, y in kapali], [y * HUCRE for x, y in kapali],
                   s=6, color="lightgray")
    harita.plot([x * HUCRE for x, y in rota], [y * HUCRE for x, y in rota],
                color="orange", label=f"A* ({len(rota)} nokta)")
    harita.plot(*zip(*sade_m), "o--", color="blue", label=f"Sade ({len(sade)} nokta)")
    harita.plot(*zip(*iz), color="green", label="Ucus izi (ruzgarli)")
    harita.set_xlabel("X (m)")
    harita.set_ylabel("Y (m)")
    harita.axis("equal")
    harita.legend()

    sapma = fig.add_subplot(2, 2, 2)
    sapma.plot([i * 0.05 for i in range(len(sapmalar))], sapmalar)
    sapma.set_ylabel("XTE (m)")
    sapma.grid(True)

    hiz = fig.add_subplot(2, 2, 4)
    t, d, v = zip(*yaklasma)
    hiz.plot(t, v)
    hiz.set_ylabel("Yaklasma hizi (m/s)")
    hiz.set_xlabel("Zaman (s)")
    hiz.grid(True)

    plt.tight_layout()
    plt.savefig("gorseller/senaryo.png", dpi=150)
    plt.show()