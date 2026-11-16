"""8.2 Dinamik yaklasma: hedefe yaklasirken hizi dusurme."""


def hiz_komutu(mesafe, v_hedef=15.0, v_max=30.0, k=0.2, d_guvenli=20.0):
    """Hedefe olan mesafeye gore aracin hizini (m/s) dondurur.
       Küçük k daha yumuşak ve daha yavaş tepki verir. Hedefin 
       hızını doğru biliyorsak sonunda yine yetişir; yanlış biliyorsak 
       daha geride kalır.k = sınır / (v_max - v_hedef)."""
    v = v_hedef + k * (mesafe - d_guvenli)
    return max(0.0, min(v_max, v))

print(hiz_komutu(20))