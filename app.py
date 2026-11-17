"""Akilli Rota projesinin Streamlit sitesi."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

from rota.yaklasma import yaklasma_simulasyonu
from rota.xte import roll_komutu, xte_simulasyonu
import math

from rota.planlama import engel_haritasi, astar, rota_uzunlugu
from rota.sadelestirme import douglas_peucker
from main import HUCRE, rotayi_takip_et
ENGELLER = [(15, 15), (20, 22), (25, 25), (30, 28),
            (35, 35), (25, 10), (10, 30)]
BASLANGIC, HEDEF = (2, 2), (47, 47)


def engele_en_yakin(noktalar, engeller, adim=50):
    """Cizgi parcalari uzerinde engellere en yakin mesafe."""
    en_yakin = float("inf")
    for (ax, ay), (bx, by) in zip(noktalar, noktalar[1:]):
        for i in range(adim + 1):
            x = ax + (bx - ax) * i / adim
            y = ay + (by - ay) * i / adim
            for ex, ey in engeller:
                mesafe = math.dist((x, y), (ex, ey))
                en_yakin = min(en_yakin, mesafe)
    return en_yakin

st.set_page_config(page_title="Akıllı Rota", layout="wide")

st.title("Akıllı Rota Gerçeklemesi")
st.write(
    "Çelebi İHA takımı, Proje 8. Engellerden kaçan rota, "
    "rota sadeleştirme, rüzgâr altında sapma düzeltmesi ve "
    "hareketli hedefe yaklaşma."
)

rota_sekmesi, kontrol_sekmesi = st.tabs(["Rota", "Kontrol"])

with rota_sekmesi:
    st.header("8.1 A* ve 8.4 Douglas-Peucker")
    sol, sag = st.columns([1, 2])

    with sol:
        guvenlik = st.slider("Güvenlik payı (hücre)",
                             1.0, 5.0, 3.0, 0.5)
        epsilon = st.slider("Epsilon (hücre)", 0.0, 4.0, 1.0, 0.25)

    kapali = engel_haritasi(50, 50, ENGELLER, guvenlik)
    rota = astar(BASLANGIC, HEDEF, kapali, 50, 50)

    if rota is None:
        st.error("Bu güvenlik payıyla başlangıçtan hedefe yol yok.")
    else:
        sade = douglas_peucker(rota, epsilon)
        yakin = engele_en_yakin(sade, ENGELLER)

        with sol:
            st.metric("A* rotası", f"{len(rota)} nokta")
            st.metric("Rota uzunluğu",
                      f"{rota_uzunlugu(rota):.1f} hücre")
            st.metric("Sade rota", f"{len(sade)} nokta")
            st.metric("Engele en yakın", f"{yakin:.2f} hücre")
            if yakin < guvenlik:
                st.warning("Sade rota güvenlik bölgesine giriyor. "
                           "Epsilon'u küçültün.")

        with sag:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.scatter(*zip(*kapali), s=8, color="lightgray",
                       label="Güvenlik bölgesi")
            ax.scatter(*zip(*ENGELLER), color="red", marker="x",
                       label="Engel")
            ax.plot(*zip(*rota), color="orange",
                    label=f"A* ({len(rota)} nokta)")
            ax.plot(*zip(*sade), "o--", color="blue",
                    label=f"Sade ({len(sade)} nokta)")
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_aspect("equal")
            ax.grid(True)
            ax.legend(loc="upper left")
            st.pyplot(fig)
            plt.close(fig)

        st.divider()
        st.header("Senaryo: rüzgâr altında uçuş")
        sol2, sag2 = st.columns([1, 2])

        with sol2:
            ruzgar_x = st.slider("Rüzgâr x (m/s)",
                                 -8.0, 8.0, -4.0, 0.5)
            ruzgar_y = st.slider("Rüzgâr y (m/s)",
                                 -8.0, 8.0, 3.0, 0.5)

        sade_m = [(x * HUCRE, y * HUCRE) for x, y in sade]
        iz, sapmalar = rotayi_takip_et(
            sade_m, ruzgar=(ruzgar_x, ruzgar_y))
        engeller_m = [(x * HUCRE, y * HUCRE) for x, y in ENGELLER]
        ucus_yakin = min(math.dist(p, e)
                         for p in iz for e in engeller_m)

        with sol2:
            en_buyuk = max(abs(s) for s in sapmalar)
            st.metric("En büyük sapma", f"{en_buyuk:.1f} m")
            st.metric("Uçuş süresi",
                      f"{len(sapmalar) * 0.05:.0f} s")
            st.metric("Engele en yakın", f"{ucus_yakin:.0f} m")
            if ucus_yakin < guvenlik * HUCRE:
                st.warning("Uçuş izi güvenlik bölgesine giriyor.")

        with sag2:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.scatter([x * HUCRE for x, y in kapali],
                       [y * HUCRE for x, y in kapali],
                       s=6, color="lightgray")
            ax.plot(*zip(*sade_m), "o--", color="blue",
                    label="Sade rota")
            ax.plot(*zip(*iz), color="green", label="Uçuş izi")
            ax.set_xlabel("X (m)")
            ax.set_ylabel("Y (m)")
            ax.set_aspect("equal")
            ax.grid(True)
            ax.legend(loc="upper left")
            st.pyplot(fig)
            plt.close(fig)

with kontrol_sekmesi:
    st.header("8.2 Hareketli hedefe yaklaşma")
    sol, sag = st.columns([1, 2])

    with sol:
        k = st.slider("k (yaklaşma kazancı)", 0.05, 1.0, 0.2, 0.05)
        v_hedef = st.slider("Hedefin hızı (m/s)", 5.0, 25.0, 15.0)
        v_max = st.slider("Aracın en yüksek hızı (m/s)",
                          20.0, 40.0, 30.0)

    if v_max <= v_hedef:
        st.warning("Araç hedeften hızlı değil, yetişemez.")

    kayit = yaklasma_simulasyonu(k=k, v_hedef=v_hedef, v_max=v_max)
    t, d, v = zip(*kayit)
    yavaslama = max(
        (v[i] - v[i + 1]) / 0.1 for i in range(len(v) - 1)
    )

    with sol:
        st.metric("En büyük yavaşlama", f"{yavaslama:.1f} m/s²")
        st.metric("60 s sonunda mesafe", f"{d[-1]:.1f} m")

    with sag:
        fig, (ust, alt) = plt.subplots(2, 1, figsize=(8, 5),
                                       sharex=True)
        ust.plot(t, d)
        ust.axhline(20, color="gray", linestyle="--")
        ust.set_ylabel("Mesafe (m)")
        ust.grid(True)
        alt.plot(t, v)
        alt.axhline(v_hedef, color="gray", linestyle="--")
        alt.set_ylabel("Hız (m/s)")
        alt.set_xlabel("Zaman (s)")
        alt.grid(True)
        st.pyplot(fig)
        plt.close(fig)
    st.divider()
    st.header("8.3 Rota sapma (XTE) düzeltmesi")
    sol2, sag2 = st.columns([1, 2])

    with sol2:
        sapma = st.slider("Başlangıç sapması (m, sağa)",
                          0.0, 50.0, 15.0, 1.0)
        ruzgar = st.slider("Yan rüzgâr (m/s)", 0.0, 10.0, 0.0, 0.5)
        wn = st.slider("wn (düzeltme hızı)", 0.2, 1.0, 0.5, 0.05)

    kayit = xte_simulasyonu(sapma, ruzgar=ruzgar, wn=wn)
    t, y, roll = zip(*kayit)

    ilk_roll = roll_komutu(sapma, 0.0, wn=wn)
    en_buyuk = max(abs(s) for s in y)

    # sapmanin 0,5 m'nin altina inip bir daha cikmadigi an
    oturma = None
    if abs(y[-1]) < 0.5:
        oturma = 0.0
        for zaman, s in zip(reversed(t), reversed(y)):
            if abs(s) >= 0.5:
                oturma = zaman
                break

    with sol2:
        if ilk_roll < 0:
            yon = "sola"
        elif ilk_roll > 0:
            yon = "sağa"
        else:
            yon = "yatış yok"
        st.metric("İlk roll komutu", f"{abs(ilk_roll):.1f}° {yon}")
        st.metric("En büyük sapma", f"{en_buyuk:.2f} m")
        if oturma is None:
            st.metric("Rotaya oturma (0,5 m)", "40 s içinde değil")
        else:
            st.metric("Rotaya oturma (0,5 m)", f"{oturma:.1f} s")

    with sag2:
        fig, (ust, alt) = plt.subplots(2, 1, figsize=(8, 5),
                                       sharex=True)
        ust.plot(t, y)
        ust.axhline(0, color="gray", linestyle="--")
        ust.set_ylabel("XTE (m)")
        ust.grid(True)
        alt.plot(t, roll)
        alt.axhline(0, color="gray", linestyle="--")
        alt.set_ylabel("Roll (derece)")
        alt.set_xlabel("Zaman (s)")
        alt.grid(True)
        st.pyplot(fig)
        plt.close(fig)