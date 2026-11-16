"""8.2 Dinamik yaklasma: hedefe yaklasirken hizi dusurme."""


def hiz_komutu(mesafe, v_hedef=15.0, v_max=30.0, k=0.2, d_guvenli=20.0):
   """Hedefe olan mesafeye gore aracin hizini (m/s) dondurur.
   Küçük k daha yumuşak ve daha yavaş tepki verir. Hedefin 
   hızını doğru biliyorsak sonunda yine yetişir; yanlış biliyorsak 
   daha geride kalır.k = sınır / (v_max - v_hedef)."""
   v = v_hedef + k * (mesafe - d_guvenli)
   return max(0.0, min(v_max, v))

def yaklasma_simulasyonu(d0=500.0, v_hedef=15.0, v_max=30.0, k=0.2, d_guvenli=20.0, dt=0.1, sure=60.0):
   """(zaman, mesafe, hiz) kayitlarinin listesini dondurur."""
   mesafe = d0
   kayit = []
   for i in range(int(sure / dt)): #adımlara bölüyor
      v = hiz_komutu(mesafe, v_hedef, v_max, k, d_guvenli) #o anki hızı alıyor
      kayit.append((i * dt, mesafe, v)) #listeye tuple tipinde veriyor
      # hedef uzaklasir, biz yaklasiriz
      mesafe += (v_hedef - v) * dt
   return kayit

if __name__ == "__main__":
   import matplotlib.pyplot as plt

   fig, (ust, alt) = plt.subplots(2, 1, figsize=(8, 6), sharex=True) #2 grafik, pencere boyutu, grafikler aynı zaman eksenini mi kullansın?
   for k in [0.1, 0.2, 0.5]: #farklı k değerleri
      kayit = yaklasma_simulasyonu(k=k)
      t, d, v = zip(*kayit) #dönen tuple'ın 1. 2. ve 3. değerlerini atıyor, (ayırma)
      ust.plot(t, d, label=f"k = {k}") #zamana karşı mesafe
      alt.plot(t, v, label=f"k = {k}") #zamana karşı hız
   ust.axhline(20, color="gray", linestyle="--") #yatay çizgi çekiyor 20 metre hedef takip metresi için
   ust.set_ylabel("Mesafe (m)")
   ust.legend()
   ust.grid(True) #arka plan ızgarası
   alt.axhline(15, color="gray", linestyle="--") #hedefin hızını çizer
   alt.set_ylabel("Hiz (m/s)")
   alt.set_xlabel("Zaman (s)")
   alt.grid(True)
   plt.tight_layout() #boşluk ayarlar
   plt.savefig("gorseller/yaklasma.png", dpi=150) #grafiği dosyaya kaydeder
   plt.show() #pencereyi ekrana aç