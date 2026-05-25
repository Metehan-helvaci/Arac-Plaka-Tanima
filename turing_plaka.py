"""
Turing Makinesi ile Araç Plaka Formatı Tanıyıcı
Format: NNLLNNN (N=Rakam, L=Büyük harf)
"""

class TuringMakinesi:
    def __init__(self):
        # Durum kümesi
        self.durumlar = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q_red'}
        
        # Başlangıç, kabul ve red durumları
        self.baslangic_durumu = 'q0'
        self.kabul_durumu = 'q7'
        self.red_durumu = 'q_red'
        
        # Giriş alfabesi
        self.giris_alfabesi = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        
        # Bant alfabesi (giriş + boşluk sembolü)
        self.bant_alfabesi = self.giris_alfabesi | {'_'}
        
        # Geçiş fonksiyonu: (durum, sembol) -> (yeni_durum, yazılacak_sembol, hareket)
        # Hareket: 'R' = Sağ, 'L' = Sol, 'S' = Dur
        self.gecis_fonksiyonu = self._gecis_tablosunu_olustur()

    def _gecis_tablosunu_olustur(self):
        gecisler = {}
        rakamlar = set('0123456789')
        harfler = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        # q0: 1. karakter rakam olmalı
        for r in rakamlar:
            gecisler[('q0', r)] = ('q1', r, 'R')
        for h in harfler:
            gecisler[('q0', h)] = ('q_red', h, 'S')
        gecisler[('q0', '_')] = ('q_red', '_', 'S')

        # q1: 2. karakter rakam olmalı
        for r in rakamlar:
            gecisler[('q1', r)] = ('q2', r, 'R')
        for h in harfler:
            gecisler[('q1', h)] = ('q_red', h, 'S')
        gecisler[('q1', '_')] = ('q_red', '_', 'S')

        # q2: 3. karakter büyük harf olmalı
        for h in harfler:
            gecisler[('q2', h)] = ('q3', h, 'R')
        for r in rakamlar:
            gecisler[('q2', r)] = ('q_red', r, 'S')
        gecisler[('q2', '_')] = ('q_red', '_', 'S')

        # q3: 4. karakter büyük harf olmalı
        for h in harfler:
            gecisler[('q3', h)] = ('q4', h, 'R')
        for r in rakamlar:
            gecisler[('q3', r)] = ('q_red', r, 'S')
        gecisler[('q3', '_')] = ('q_red', '_', 'S')

        # q4: 5. karakter rakam olmalı
        for r in rakamlar:
            gecisler[('q4', r)] = ('q5', r, 'R')
        for h in harfler:
            gecisler[('q4', h)] = ('q_red', h, 'S')
        gecisler[('q4', '_')] = ('q_red', '_', 'S')

        # q5: 6. karakter rakam olmalı
        for r in rakamlar:
            gecisler[('q5', r)] = ('q6', r, 'R')
        for h in harfler:
            gecisler[('q5', h)] = ('q_red', h, 'S')
        gecisler[('q5', '_')] = ('q_red', '_', 'S')

        # q6: 7. karakter rakam olmalı
        for r in rakamlar:
            gecisler[('q6', r)] = ('q7', r, 'R')
        for h in harfler:
            gecisler[('q6', h)] = ('q_red', h, 'S')
        gecisler[('q6', '_')] = ('q_red', '_', 'S')

        # q7: Kabul durumu - burada boşluk/_ beklenir (fazla karakter kontrolü)
        gecisler[('q7', '_')] = ('q7', '_', 'S')  # Kabul
        for r in rakamlar:
            gecisler[('q7', r)] = ('q_red', r, 'S')  # Fazla karakter
        for h in harfler:
            gecisler[('q7', h)] = ('q_red', h, 'S')  # Fazla karakter

        return gecisler

    def calistir(self, girdi, verbose=True):
        # Bandı oluştur: girdi + boşluk sembolü
        bant = list(girdi) + ['_']
        kafa = 0
        mevcut_durum = self.baslangic_durumu

        if verbose:
            print(f"\n{'='*60}")
            print(f"Girdi: {girdi}")
            print(f"{'='*60}")
            print(f"{'Durum':<10} {'Okunan':<10} {'Yeni Durum':<12} {'Hareket':<10} {'Bant'}")
            print(f"{'-'*70}")

        adim = 0
        while True:
            # Mevcut sembolü oku
            if kafa < len(bant):
                sembol = bant[kafa]
            else:
                sembol = '_'

            # Geçiş anahtarı
            anahtar = (mevcut_durum, sembol)

            if verbose:
                bant_goster = ''.join(bant)
                kafa_goster = ' ' * kafa + '^'
                print(f"{mevcut_durum:<10} {sembol:<10}", end='')

            # Geçiş var mı?
            if anahtar not in self.gecis_fonksiyonu:
                if verbose:
                    print(f"{'q_red':<12} {'S':<10} {bant_goster}")
                    print(f"{'':10} {'':10} {'':12} {'':10} {kafa_goster}")
                mevcut_durum = self.red_durumu
                break

            yeni_durum, yazilacak, hareket = self.gecis_fonksiyonu[anahtar]

            # Banda yaz
            if kafa < len(bant):
                bant[kafa] = yazilacak
            else:
                bant.append(yazilacak)

            if verbose:
                bant_goster = ''.join(bant)
                kafa_goster = ' ' * kafa + '^'
                print(f"{yeni_durum:<12} {hareket:<10} {bant_goster}")
                print(f"{'':10} {'':10} {'':12} {'':10} {kafa_goster}")

            mevcut_durum = yeni_durum

            # Kabul veya Red durumuna ulaşıldı mı?
            if mevcut_durum == self.kabul_durumu:
                # Sonraki sembol boşluk mu kontrol et (fazla karakter yok mu?)
                kafa += 1
                if kafa < len(bant) and bant[kafa] != '_':
                    mevcut_durum = self.red_durumu
                break
            elif mevcut_durum == self.red_durumu:
                break

            # Kafa hareketi
            if hareket == 'R':
                kafa += 1
            elif hareket == 'L':
                kafa = max(0, kafa - 1)

            adim += 1

        # Sonuç
        if verbose:
            print(f"\n{'-'*70}")

        if mevcut_durum == self.kabul_durumu:
            sonuc = "KABUL"
        else:
            sonuc = "RED"

        if verbose:
            print(f"Sonuç: {sonuc}")
            print(f"{'='*60}\n")

        return sonuc


def gecis_tablosunu_yazdir(tm):
    print("\n" + "="*70)
    print("GEÇİŞ TABLOSU")
    print("="*70)
    print(f"{'Durum':<10} {'Okunan':<12} {'Yeni Durum':<14} {'Yazılan':<10} {'Hareket'}")
    print("-"*60)

    durum_sirasi = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7']
    ozel_semboller = [
        ('Rakam (0-9)', '5'),
        ('Büyük Harf (A-Z)', 'A'),
        ('Boşluk', '_'),
    ]

    for durum in durum_sirasi:
        for aciklama, ornek in ozel_semboller:
            anahtar = (durum, ornek)
            if anahtar in tm.gecis_fonksiyonu:
                yd, yaz, har = tm.gecis_fonksiyonu[anahtar]
                print(f"{durum:<10} {aciklama:<20} {yd:<14} {yaz:<10} {har}")
            else:
                print(f"{durum:<10} {aciklama:<20} {'q_red':<14} {ornek:<10} S")
    print("="*70)


def test_et():
    tm = TuringMakinesi()

    gecerli_girdiler = [
        "55AB123",
        "34TR456",
        "06AA789",
        "01ZZ000",
        "99XY999",
    ]

    gecersiz_girdiler = [
        "5AB123",    # Eksik karakter
        "555AB12",   # Yanlış format
        "34A1234",   # 4. pozisyonda rakam
        "AB34123",   # 1. pozisyonda harf
        "34AB12X",   # Son pozisyonda harf
        "55ab123",   # Küçük harf
        "34TR4567",  # Fazla karakter
        "",          # Boş girdi
    ]

    print("\n" + "="*60)
    print("GEÇERLİ GİRDİ TESTLERİ")
    print("="*60)
    for girdi in gecerli_girdiler:
        sonuc = tm.calistir(girdi, verbose=True)

    print("\n" + "="*60)
    print("GEÇERSİZ GİRDİ TESTLERİ")
    print("="*60)
    for girdi in gecersiz_girdiler:
        sonuc = tm.calistir(girdi, verbose=True)

    gecis_tablosunu_yazdir(tm)


def kullanici_modu():
    tm = TuringMakinesi()
    print("\n" + "="*60)
    print("  Turing Makinesi - Araç Plaka Formatı Tanıyıcı")
    print("  Format: NNLLNNN (N=Rakam, L=Büyük Harf)")
    print("="*60)

    while True:
        girdi = input("\nPlaka girin (çıkmak için 'q'): ").strip()
        if girdi.lower() == 'q':
            print("Program sonlandırıldı.")
            break
        sonuc = tm.calistir(girdi, verbose=True)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        test_et()
    else:
        kullanici_modu()
