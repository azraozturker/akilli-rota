"""8.3 Rota sapma duzeltmesi: XTE'ye gore roll acisi."""
import math

G = 9.81


def roll_komutu(xte, xte_hizi, wn=0.5, zeta=1.0, roll_limit=30.0):
    """Sapmaya gore roll acisini (derece) dondurur.

    xte: sapma (m), saga dogru arti.
    xte_hizi: sapmanin degisim hizi (m/s).
    Donen deger: roll acisi (derece), saga dogru arti.
    """
    kp = wn ** 2
    kd = 2 * zeta * wn
    ivme = -(kp * xte + kd * xte_hizi)
    roll = math.degrees(math.atan(ivme / G)) #formul karışık readme'de açıklanacak.
    return max(-roll_limit, min(roll_limit, roll))

def xte_simulasyonu(y0, V=20.0, ruzgar=0.0, wn=0.5, zeta=1.0, roll_limit=30.0, dt=0.05, sure=40.0):
    """Dogrusal rotada (zaman, sapma, roll) kayitlarini dondurur."""
    y = y0
    # chi: rotaya gore yon acisi (radyan)
    chi = 0.0 #Sapmanın fark edildiği ilk anda araç rotaya paralel gidiyordur, yani sapma hızı sıfırdır.
    kayit = []
    for i in range(int(sure / dt)):
        y_hizi = V * math.sin(chi) + ruzgar #yana hız sin kullanılıyor ve rüzgar ekleniyor
        roll = roll_komutu(y, y_hizi, wn, zeta, roll_limit) #anlık değerleri alıyoruz ki:
        kayit.append((i * dt, y, roll)) #grafik için toplanıyor
        chi += G * math.tan(math.radians(roll)) / V * dt #uçak yana yatınca döner; ne kadar yatarsa o kadar hızlı döner.
        y += y_hizi * dt #güncelleme
    return kayit


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    print("Sapma (m) -> ilk roll (derece)")
    for sapma in [5, 10, 15, 30, 50]:
        print(sapma, "->", round(roll_komutu(sapma, 0.0), 1)) #sonucu ondalığı yuvarlayarak yazıyo

    fig, (ust, alt) = plt.subplots(2, 1, figsize=(8, 6), sharex=True) #grafik ayarları
    for sapma in [5, 15, 30]:
        t, y, roll = zip(*xte_simulasyonu(sapma)) #yaklasmadakiyle aynı iş ama farklı bir değişkene atamıyor
        ust.plot(t, y, label=f"Baslangic sapmasi {sapma} m")
        alt.plot(t, roll, label=f"{sapma} m")
    t, y, roll = zip(*xte_simulasyonu(0.0, ruzgar=5.0)) #rüzgarlı çizim için tablodan atama

    ust.plot(t, y, linestyle="--", label="Sapma yok, 5 m/s yan ruzgar")
    alt.plot(t, roll, linestyle="--", label="5 m/s yan ruzgar")
    
    ust.set_ylabel("XTE (m)") #grafik ayarları...
    ust.legend()
    ust.grid(True)
    alt.set_ylabel("Roll (derece)")
    alt.set_xlabel("Zaman (s)")
    alt.grid(True)
    plt.tight_layout()
    plt.savefig("gorseller/xte.png", dpi=150)
    plt.show()

