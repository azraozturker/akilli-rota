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

if __name__ == "__main__":
    import random
    import matplotlib.pyplot as plt

    random.seed(1)
    rota = []
    for x in range(0, 101):
        y = 10 * math.sin(x / 15) + random.uniform(-0.8, 0.8)
        rota.append((x, y))

    fig, eksenler = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
    for eksen, eps in zip(eksenler, [0.5, 1.5, 4.0]):
        sade = douglas_peucker(rota, eps)
        print("epsilon:", eps, "nokta:", len(rota), "->", len(sade))
        eksen.plot(*zip(*rota), color="lightgray", marker=".",
                   label=f"Orijinal ({len(rota)} nokta)")
        eksen.plot(*zip(*sade), color="blue", marker="o",
                   label=f"Sade ({len(sade)} nokta)")
        eksen.set_title(f"epsilon = {eps} m")
        eksen.legend()
        eksen.grid(True)
    plt.tight_layout()
    plt.savefig("gorseller/douglas_peucker.png", dpi=150)
    plt.show()
   

      

