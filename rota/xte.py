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

print(roll_komutu(15,0.0))