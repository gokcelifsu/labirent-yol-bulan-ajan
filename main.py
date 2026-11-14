import pygame
import sys
from collections import deque
import heapq
import random
pygame.init()

SATIR_SAYISI = 20
SUTUN_SAYISI = 50
KARE_BOYUTU = 20

GENISLIK = SUTUN_SAYISI * KARE_BOYUTU
YUKSEKLIK = SATIR_SAYISI * KARE_BOYUTU

PENCERE = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("20x50 BFS Yol Bulma Simülasyonu")

BEYAZ = (255, 255, 255)
SIYAH = (40, 40, 40)
GRI = (220, 220, 220)
YESIL = (46, 204, 113)
MOR = (155, 89, 182)
MAVI = (52, 152, 219)
SARI = (241, 196, 15)
CAMUR = (139, 69, 19)
TURKUAZ = (26, 188, 156)

class Hucre:
    def __init__(self, satir, sutun):
        self.satir = satir
        self.sutun = sutun
        self.x = sutun * KARE_BOYUTU
        self.y = satir * KARE_BOYUTU
        self.renk = BEYAZ
        self.komsular = []
    def camur_mu(self):
        return self.renk == CAMUR

    def camur_yap(self):
        self.renk = CAMUR

    def ciz(self, pencere):
        pygame.draw.rect(pencere, self.renk, (self.x, self.y, KARE_BOYUTU, KARE_BOYUTU))
        pygame.draw.rect(pencere, GRI, (self.x, self.y, KARE_BOYUTU, KARE_BOYUTU), 1)

    def komsulari_guncelle(self, izgara, capraz=False):
        self.komsular = []
        yonler = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if capraz:
            yonler.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
        for dr, dc in yonler:
            r, c = self.satir + dr, self.sutun + dc
            if 0 <= r < SATIR_SAYISI and 0 <= c < SUTUN_SAYISI and izgara[r][c].renk != SIYAH:
                self.komsular.append(izgara[r][c])

def izgara_olustur():
    izgara = []
    for i in range(SATIR_SAYISI):
        satir = []
        for j in range(SUTUN_SAYISI):
            satir.append(Hucre(i, j))
        izgara.append(satir)
    
    # Varsayılan Başlangıç (Yeşil) ve Bitiş (Kırmızı) noktaları
    izgara[10][5].renk = YESIL
    izgara[10][45].renk = MOR
    return izgara, izgara[10][5], izgara[10][45]

def labirent_olustur(izgara, baslangic, hedef):
    for satir in izgara:
        for hucre in satir:
            hucre.renk = SIYAH

    yigin = [(1, 1)]
    izgara[1][1].renk = BEYAZ

    while yigin:
        r, c = yigin[-1]
        komsular = []
        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < SATIR_SAYISI and 0 <= nc < SUTUN_SAYISI and izgara[nr][nc].renk == SIYAH:
                komsular.append((nr, nc, dr // 2, dc // 2))

        if komsular:
            nr, nc, ar, ac = random.choice(komsular)
            izgara[r + ar][c + ac].renk = BEYAZ
            izgara[nr][nc].renk = BEYAZ
            yigin.append((nr, nc))
        else:
            yigin.pop()

    # Başlangıç ve hedef noktalarının duvar içinde kalmamasını sağla
    if baslangic:
        baslangic.renk = YESIL
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = baslangic.satir + dr, baslangic.sutun + dc
            if 0 <= nr < SATIR_SAYISI and 0 <= nc < SUTUN_SAYISI and izgara[nr][nc] != hedef:
                izgara[nr][nc].renk = BEYAZ

    if hedef:
        hedef.renk = MOR
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = hedef.satir + dr, hedef.sutun + dc
            if 0 <= nr < SATIR_SAYISI and 0 <= nc < SUTUN_SAYISI and izgara[nr][nc] != baslangic:
                izgara[nr][nc].renk = BEYAZ

def draw(pencere, izgara):
    pencere.fill(BEYAZ)
    for satir in izgara:
        for hucre in satir:
            hucre.ciz(pencere)
    pygame.display.update()

def yolu_ciz(ciz_fonksiyonu, gelinen_yer, baslangic, hedef):
    temp = hedef
    yol_listesi = []
    
    # Önce sarı yolu çiz
    while temp in gelinen_yer:
        yol_listesi.append(temp)
        temp = gelinen_yer[temp]
        if temp != baslangic:
            temp.renk = SARI
        ciz_fonksiyonu()
        pygame.time.delay(15)
    hedef.renk = MOR

    # Şimdi robotu (ajanı) baştan sona yürüt
    yol_listesi.reverse()
    for adim in yol_listesi:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        ciz_fonksiyonu()
        # Robot gövdesi (kırmızı daire) ve gözleri
        merkez_x = adim.x + KARE_BOYUTU // 2
        merkez_y = adim.y + KARE_BOYUTU // 2
        pygame.draw.circle(PENCERE, (231, 76, 60), (merkez_x, merkez_y), KARE_BOYUTU // 2 - 2)
        pygame.draw.circle(PENCERE, BEYAZ, (merkez_x - 3, merkez_y - 2), 2)
        pygame.draw.circle(PENCERE, BEYAZ, (merkez_x + 3, merkez_y - 2), 2)
        pygame.display.update()
        pygame.time.delay(45)

    return len(yol_listesi)

def bfs(ciz_fonksiyonu, izgara, baslangic, hedef):
    kuyruk = deque([baslangic])
    gelinen_yer = {}
    ziyaret_edildi = {baslangic}
    bakilan_kare = 0

    while kuyruk:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mevcut = kuyruk.popleft()
        bakilan_kare += 1

        if mevcut == hedef:
            uzunluk = yolu_ciz(ciz_fonksiyonu, gelinen_yer, baslangic, hedef)
            return True, bakilan_kare, uzunluk

        for komsu in mevcut.komsular:
            if komsu not in ziyaret_edildi:
                ziyaret_edildi.add(komsu)
                gelinen_yer[komsu] = mevcut
                if komsu != hedef and not komsu.camur_mu():
                    komsu.renk = MAVI
                kuyruk.append(komsu)

        ciz_fonksiyonu()
        pygame.time.delay(8)

    return False, bakilan_kare, 0

def sezgisel(h1, h2):
    return abs(h1.satir - h2.satir) + abs(h1.sutun - h2.sutun)

def a_star(ciz_fonksiyonu, izgara, baslangic, hedef):
    sayac = 0
    acik_kume = []
    heapq.heappush(acik_kume, (0, sayac, baslangic))
    gelinen_yer = {}
    g_skoru = {h: float("inf") for s in izgara for h in s}
    g_skoru[baslangic] = 0
    f_skoru = {h: float("inf") for s in izgara for h in s}
    f_skoru[baslangic] = sezgisel(baslangic, hedef)
    acik_kume_seti = {baslangic}
    bakilan_kare = 0

    while acik_kume:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mevcut = heapq.heappop(acik_kume)[2]
        acik_kume_seti.remove(mevcut)
        bakilan_kare += 1

        if mevcut == hedef:
            uzunluk = yolu_ciz(ciz_fonksiyonu, gelinen_yer, baslangic, hedef)
            return True, bakilan_kare, uzunluk

        for komsu in mevcut.komsular:
            adim_maliyeti = 5 if komsu.camur_mu() else 1
            gecici_g = g_skoru[mevcut] + adim_maliyeti
            if gecici_g < g_skoru[komsu]:
                gelinen_yer[komsu] = mevcut
                g_skoru[komsu] = gecici_g
                f_skoru[komsu] = gecici_g + sezgisel(komsu, hedef)
                if komsu not in acik_kume_seti:
                    sayac += 1
                    heapq.heappush(acik_kume, (f_skoru[komsu], sayac, komsu))
                    acik_kume_seti.add(komsu)
                    if komsu != hedef and not komsu.camur_mu():
                        komsu.renk = TURKUAZ

        ciz_fonksiyonu()
        pygame.time.delay(8)

    return False, bakilan_kare, 0

def hibrit_calistir(ciz_fonksiyonu, izgara, baslangic, hedef):
    camur_var_mi = any(h.camur_mu() for s in izgara for h in s)
    if camur_var_mi:
        basari, kare, uzunluk = a_star(ciz_fonksiyonu, izgara, baslangic, hedef)
        return "Hibrit (Dinamik A*)", basari, kare, uzunluk
    else:
        basari, kare, uzunluk = bfs(ciz_fonksiyonu, izgara, baslangic, hedef)
        return "Hibrit (BFS)", basari, kare, uzunluk

def main():
    izgara, baslangic, hedef = izgara_olustur()
    calisiyor = True
    capraz = False
    sonuclar = {}

    while calisiyor:
        draw(PENCERE, izgara)

        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calisiyor = False

            # Sol tık: Duvar örme / Başlangıç-Bitiş belirleme
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                satir = pos[1] // KARE_BOYUTU
                sutun = pos[0] // KARE_BOYUTU
                hucre = izgara[satir][sutun]

                if not baslangic and hucre != hedef:
                    baslangic = hucre
                    baslangic.renk = YESIL
                elif not hedef and hucre != baslangic:
                    hedef = hucre
                    hedef.renk = MOR
                elif hucre != baslangic and hucre != hedef:
                    if pygame.key.get_pressed()[pygame.K_w]:
                        hucre.camur_yap()
                    else:
                        hucre.renk = SIYAH

            # Sağ tık: Silme
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                satir = pos[1] // KARE_BOYUTU
                sutun = pos[0] // KARE_BOYUTU
                hucre = izgara[satir][sutun]
                hucre.renk = BEYAZ
                if hucre == baslangic:
                    baslangic = None
                elif hucre == hedef:
                    hedef = None

            if olay.type == pygame.KEYDOWN:
                # Boşluk Tuşu: BFS Çalıştır
                if olay.key == pygame.K_SPACE and baslangic and hedef:
                    for s in izgara:
                        for h in s:
                            h.komsulari_guncelle(izgara, capraz)
                    _, kare, _ = bfs(lambda: draw(PENCERE, izgara), izgara, baslangic, hedef)
                    sonuclar["BFS"] = f"BFS: {kare} kare"
                    pygame.display.set_caption(" | ".join(sonuclar.values()))

                # A Tuşu: A* Çalıştır (Bonus Karşılaştırma)
                if olay.key == pygame.K_a and baslangic and hedef:
                    for s in izgara:
                        for h in s:
                            h.komsulari_guncelle(izgara, capraz)
                    _, kare, _ = a_star(lambda: draw(PENCERE, izgara), izgara, baslangic, hedef)
                    sonuclar["A*"] = f"A*: {kare} kare"
                    pygame.display.set_caption(" | ".join(sonuclar.values()))

                # H Tuşu: Hibrit Algoritma (Çamur varsa A*, yoksa BFS)
                if olay.key == pygame.K_h and baslangic and hedef:
                    for s in izgara:
                        for h in s:
                            h.komsulari_guncelle(izgara, capraz)
                    mod, _, kare, _ = hibrit_calistir(lambda: draw(PENCERE, izgara), izgara, baslangic, hedef)
                    pygame.display.set_caption(f"{mod} -> {kare} kare")

                # C Tuşu: EKRANI SIFIRLAMA (Düzeltildi)
                if olay.key == pygame.K_c:
                    izgara, baslangic, hedef = izgara_olustur()

                # R Tuşu: RASTGELE DUVAR EKLEME
                if olay.key == pygame.K_r:
                    for satir in izgara:
                        for hucre in satir:
                            if hucre != baslangic and hucre != hedef:
                                if random.random() < 0.25:
                                    hucre.renk = SIYAH
                                else:
                                    hucre.renk = BEYAZ

                # T Tuşu: Duvarları bozmadan sadece yolu temizle
                if olay.key == pygame.K_t:
                    for satir in izgara:
                        for hucre in satir:
                            if hucre.renk in (MAVI, TURKUAZ, SARI):
                               hucre.renk = BEYAZ
                    if baslangic:
                        baslangic.renk = YESIL
                    if hedef:
                        hedef.renk = MOR    

                # D Tuşu: Çapraz hareketi aç/kapat (Bunu ekle)
                if olay.key == pygame.K_d:
                    capraz = not capraz      
                    pygame.display.set_caption(f"Çapraz Hareket: {'AÇIK' if capraz else 'KAPALI'}") 

                # M Tuşu: Gerçek labirent oluştur
                if olay.key == pygame.K_m:
                    labirent_olustur(izgara, baslangic, hedef)

if __name__ == "__main__":
    main()
