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

def astar(baslangic, hedef, kapali, genislik, yukseklik):
    """Baslangictan hedefe en kisa rotayi dondurur. Yol yoksa None."""
    komsular = [(1, 0), (-1, 0), (0, 1), (0, -1),(1, 1), (1, -1), (-1, 1), (-1, -1)] #bir hucreden gidilebilecek 8 olası yön
    acik = [(0.0, baslangic)]    #(tahmini toplam maliyet, hucre)
    maliyet = {baslangic: 0.0}   #baslangictan o hucreye gercek maliyet
    onceki = {}  #hucreye hangi hucreden gelindi

    while acik:
        _, simdiki = heapq.heappop(acik) #en küçük puanlıyı çekiyoruz
        if simdiki == hedef:
            rota = [simdiki]
            while simdiki in onceki:
                simdiki = onceki[simdiki]
                rota.append(simdiki)
            return rota[::-1]  #hedefse geriyi takip etti

        for dx, dy in komsular: #8 komşuyu dolaşır 
            komsu = (simdiki[0] + dx, simdiki[1] + dy)
            if not 0 <= komsu[0] < genislik:
                continue
            if not 0 <= komsu[1] < yukseklik:
                continue
            if komsu in kapali:
                continue
            yeni = maliyet[simdiki] + math.hypot(dx, dy) #yeni maliyet
            if yeni < maliyet.get(komsu, float("inf")): #daha ucuzsa o yazılır
                maliyet[komsu] = yeni
                onceki[komsu] = simdiki
                kalan = math.dist(komsu, hedef)
                heapq.heappush(acik, (yeni + kalan, komsu)) #puanıyla listeye eklendi
    return None


def rota_uzunlugu(rota):
    """Rotadaki ardisik noktalar arasi mesafelerin toplami."""
    toplam = 0.0
    for i in range(len(rota) - 1):
        toplam += math.dist(rota[i], rota[i + 1])
    return toplam

