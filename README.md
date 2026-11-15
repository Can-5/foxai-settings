# Foxai Settings

Modern, gizlilik odaklı ve kapsamlı bir Linux ayarlar uygulaması.  
YaST benzeri modüler yapıyla sistemin tamamında ince ayarlar yapabilirsiniz.

## Özellikler

- **Hesap & Profiller**: Kullanıcı girişi, kayıt, çoklu profil yönetimi, profil bazlı ayar izolasyonu
- **Görünüm**: Koyu tema, akcent rengi, yazı boyutu, duvar kağıdı
- **Ekran**: Çözünürlük, yenileme hızı, parlaklık, gece ışığı, çoklu ekran
- **Bildirimler**: Bildirim aç/kapa, ses, rahatsız etmeyin, uygulama bazlı izinler
- **Gizlilik & Güvenlik**: Konum/kamera/mikrofon erişimi, telemetri kontrolü, şifre ve 2FA
- **Klavye**: Dil/düzen, tuş tekrarı, erişilebilirlik (sticky/filter keys)
- **Fare & Touchpad**: Hassasiyet, kaydırma hızı, doğal kaydırma, dokunma ile tıkla
- **Güç & Pil**: Güç modu (verimlilik/dengeli/performans), uyku süresi, ekran kilidi
- **Ağ & İnternet**: Wi-Fi, Ethernet/DHCP, VPN, proxy
- **Bluetooth**: Cihaz keşfi ve eşleştirme
- **Yazılım & Güncelleme**: Depo yönetimi, paket arama/kurulum, otomatik güncelleme politikası
- **Donanım & Sistem Bilgisi**: CPU, RAM, disk, GPU, dağıtım ve çekirdek sürümü
- **Önyükleyici (GRUB)**: Varsayılan OS, menü bekleme süresi, gizli menü, çekirdek parametreleri
- **Kullanıcılar & Gruplar**: Sistem hesapları, rol atama, sudo yetkisi, şifre yönetimi
- **Güvenlik Duvarı**: Etkin/devre dışı, işlem modu, port kuralı ekleme, kural listesi

## Mimari

```
foxai-settings/
├── main.py              # Giriş ekranı + ana pencere + modül yönlendirme
├── database.py          # SQLite veritabanı (hesap, profil, ayarlar)
├── theme.py             # QSS moderne koyu tema
├── widgets.py           # Tekrar kullanılabilir UI bileşenleri
├── requirements.txt
├── run.sh
├── foxai-settings.desktop
├── LICENSE
└── pages/
    ├── base_page.py
    ├── accounts.py
    ├── appearance.py
    ├── display.py
    ├── notifications.py
    ├── privacy.py
    ├── keyboard.py
    ├── mouse.py
    ├── power.py
    ├── network.py
    ├── bluetooth.py
    ├── software.py
    ├── system_info.py
    ├── boot.py
    ├── users.py
    └── firewall.py
```

## Kurulum ve Çalıştırma

Fedora Linux üzerinde (geliştirme CachyOS/Arch üzerinde yapıldı, Fedora'ya taşındı):

```bash
# Sistem bağımlılıkları (gerekirse)
sudo dnf install python3 python3-pip git

# Proje klasörüne gir
cd "/home/ilkaycan/Belgeler/Varsayılan Proje/foxai-settings"

# Sanal ortam oluştur (ilk kez ise)
python3 -m venv .venv
source .venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı çalıştır
./run.sh
```

Veya doğrudan:

```bash
.venv/bin/python main.py
```

## Mimari Kararları

- **Sıfır telemetri**: Tüm veriler yerel SQLite veritabanında (`~/.local/share/foxai-settings/settings.db`) tutulur. Buluta hiçbir veri gönderilmez.
- **Profille ayar izolasyonu**: Her profilin kendi ayar kümesi vardır. Profil değiştirildiğinde ilgili ayarlar yüklenir.
- **Güvenli şifre saklama**: Şifreler hash'lenmiş olarak saklanır (örnek için SHA-256; üretimde bcrypt/argon2 önerilir).
- **PyQt6**: Modern Qt6 tabanlı arayüz, Fusion stilini kullanır.

## Geliştirici

İlkaycan (Can-5) — https://github.com/Can-5  
Foxai ekosistemi (Foxai Browser, Foxai Shield, Jarvis-ai, Foxai Sentinel)'nin bir parçasıdır.

## Lisans

[MIT](LICENSE)
