==========================================================================
PROJE ADI: Socket Programming - Data Transmission with Error Detection
KONU: Hata Tespit Yöntemleri ve Veri İletişim Simülasyonu
TARİH: 17.12.2025
==========================================================================

1. PROJE HAKKINDA
--------------------------------------------------------------------------
Bu proje, veri iletişiminde kullanılan hata tespit yöntemlerinin (Error 
Detection) ve veri bozulması (Data Corruption) senaryolarının simüle 
edildiği bir ağ uygulamasıdır. 

Proje, ödevde belirtilen Client-Server-Client mimarisine uygun olarak 
3 ana bileşenden oluşmaktadır:
1. Client 1 (Commander): Veriyi gönderen ve hata denetim kodunu ekleyen taraf.
2. Server (Jammer): Veriyi taşıyan ve kasıtlı olarak bozan ara düğüm.
3. Client 2 (Artillery): Veriyi alan ve bütünlüğünü doğrulayan taraf.

Sistem, terminal üzerinden interaktif bir "Savaş Oyunu" konseptiyle 
görselleştirilmiştir.

2. DOSYA YAPISI VE GÖREVLERİ
--------------------------------------------------------------------------

A) utils.py (Algoritma Kütüphanesi)
   - Projenin matematiksel işlem merkezidir.
   - Ödev gereksinimlerinde belirtilen algoritmaları içerir:
     * Parity Bit (Tek/Çift Parity) 
     * 2D Parity (Matris Tabanlı Kontrol) 
     * CRC (Cyclic Redundancy Check - Manuel Polinom Bölme) 
   - Hazır kütüphane fonksiyonları yerine algoritmalar manuel kodlanmıştır.

B) commander.py (Client 1 - Gönderici) 
   - Kullanıcıdan metin (askeri emir) girişi alır .
   - Kullanıcının seçtiği yönteme göre (Parity, 2D Parity, CRC) kontrol 
     bitsini üretir .
   - Veriyi "VERİ|YÖNTEM|KOD" formatında paketleyip sunucuya iletir .
   - Soket yapısı: TCP/IP, Non-persistent connection.

C) jammer.py (Server - Ara Düğüm ve Bozucu) 
   - Client 1'den gelen paketi dinler ve yakalar .
   - Kullanıcıya "Hata Enjeksiyonu" menüsü sunar :
     1. Bit Flip: Rastgele bir bitin ters çevrilmesi .
     2. Burst Error: Belirli bir aralıktaki verinin bozulması .
     3. No Error: Verinin olduğu gibi iletilmesi.
   - Bozulan (veya sağlam) paketi Client 2'ye iletir .

D) artillery.py (Client 2 - Alıcı) 
   - Sunucudan gelen paketi alır.
   - Paketi "split" ederek veri ve kontrol kodunu ayırır .
   - Gelen veriye göre kontrol kodunu yeniden hesaplar .
   - Gelen kod ile hesaplanan kodu karşılaştırarak "DATA CORRECT" veya 
     "DATA CORRUPTED" sonucunu ekrana basar .

3. GEREKSİNİMLERİN KARŞILANMA DURUMU
--------------------------------------------------------------------------
[✓] Socket Bağlantısı: İki istemci ve bir sunucu arasında TCP bağlantısı kuruldu.
[✓] Metin Girişi: Kullanıcıdan dinamik veri girişi sağlandı.
[✓] Yöntem Seçimi: Parity, 2D Parity ve CRC seçenekleri eklendi.
[✓] Paket Formatı: İletişim "DATA|METHOD|HASH" formatında sağlandı.
[✓] Hata Enjeksiyonu: Sunucu tarafında Bit Flip ve Burst Error uygulandı.
[✓] Doğrulama: Alıcı tarafında veri bütünlüğü kontrol edilip sonuç raporlandı.

4. KURULUM VE ÇALIŞTIRMA (HOW TO RUN)
--------------------------------------------------------------------------
Projenin çalışması için Python 3 ve 'colorama' kütüphanesi gereklidir.

Gerekli Kütüphane Kurulumu:
$ pip install colorama

Çalıştırma Sırası (3 Farklı Terminalde):
Sistemin doğru çalışması için aşağıdaki sıra takip edilmelidir:

1. Terminal -> python artillery.py  (Alıcı dinlemeye başlar)
2. Terminal -> python jammer.py     (Sunucu köprüyü kurar)
3. Terminal -> python commander.py  (Gönderici emri girer)

5. KULLANILAN TEKNOLOJİLER
--------------------------------------------------------------------------
- Dil: Python 3
- Kütüphaneler: socket, random, time, binascii
- Görselleştirme: colorama (Renkli terminal çıktıları için)

--------------------------------------------------------------------------