# MEMORY.md — Foxai Settings (Proje Notları)

## Proje Amacı
Linux için modern, gizlilik odaklı, YaST benzeri kapsamlı ayarlar uygulaması.  
Sistemdeki bütün ayarları (hesap, profil, görünüm, ekran, ağ, bluetooth, ses, yazılım, donanım, GRUB, kullanıcılar, güvenlik duvarı, sistem servisleri) tek bir arayüzden yönetir.

## Klasör Yapısı
```
foxai-settings/
├── main.py              # Giriş ekranı + ana pencere + modül yönlendirme (17 modül)
├── database.py          # SQLite veritabanı (hesap, profil, ayarlar)
├── theme.py             # QSS moderne koyu tema
├── widgets.py           # Tekrar kullanılabilir UI bileşenleri
├── requirements.txt     # PyQt6
├── run.sh               # Çalıştırma betiği (.venv otomatik oluşturur)
├── foxai-settings.desktop # Masaüstü kısayolu
├── LICENSE              # MIT
├── README.md            # Kullanım ve özellikler
├── MEMORY.md            # Bu dosya
└── pages/
    ├── base_page.py     # Tüm sayfaların temel sınıfı
    ├── accounts.py      # Hesap & Profiller (giriş/kayıt/çoklu profil)
    ├── appearance.py    # Görünüm (tema, renk, yazı)
    ├── display.py       # Ekran (çözünürlük, yenileme hızı, parlaklık, gece ışığı)
    ├── notifications.py # Bildirimler (aç/kapa, ses, rahatsız etmeyin)
    ├── privacy.py       # Gizlilik & Güvenlik (konum/kamera/mikrofon, telemetri)
    ├── keyboard.py      # Klavye (dil, tuş tekrarı, erişilebilirlik)
    ├── mouse.py         # Fare & Touchpad (hassasiyet, kaydırma, doğal kaydırma)
    ├── power.py         # Güç & Pil (güç modu, uyku, ekran kilidi)
    ├── network.py       # Ağ & İnternet (Wi-Fi, Ethernet/DHCP, VPN, proxy)
    ├── bluetooth.py     # Bluetooth (cihaz keşfi/eşleştirme)
    ├── audio.py         # Ses & Ayagıt (çıkış aygıtı, seviyeler, sistem sesleri)
    ├── software.py      # Yazılım & Güncelleme (depolar, paket kurulum, otomatik güncelleme)
    ├── system_info.py   # Donanım & Sistem Bilgisi (CPU, RAM, disk, GPU, çekirdek)
    ├── boot.py          # Önyükleyici (GRUB: varsayılan OS, bekleme süresi, çekirdek parametreleri)
    ├── users.py         # Kullanıcılar & Gruplar (sistem hesapları, sudo, şifre)
    ├── firewall.py      # Güvenlik Duvarı (etkin/devre dışı, işlem modu, port kuralı)
    └── system_services.py # Sistem Servisleri (arka plan servisleri etkin/devre dışı)
```

## Mimari Kararları
- **Sıfır telemetri**: Tüm veriler yerel SQLite veritabanında (`~/.local/share/foxai-settings/settings.db`) tutulur. Buluta hiçbir veri gitmez.
- **Profille ayar izolasyonu**: Her profilin kendi ayar kümesi vardır. Profil değiştirildiğinde ilgili ayarlar yüklenir.
- **Güvenli şifre saklama**: Şifreler hash'lenmiş olarak saklanır (örnek için SHA-256; üretimde bcrypt/argon2 önerilir).
- **PyQt6 + Fusion stil**: Modern Qt6 tabanlı arayüz.
- **YaST benzeri modüler yapı**: Her kategori ayrı bir sayfa; tek bir kenar çubuğundan erişilir.

## Nasıl Çalıştırılır (CachyOS / Arch)
```bash
cd "/home/ilkaycan/Belgeler/Varsayılan Proje/foxai-settings"
chmod +x run.sh
./run.sh
```

## Fedora'ya Geçiş Notları (Plan)
Bu proje CachyOS (Arch tabanlı) üzerinde geliştirildi. Fedora'ya taşınırken aşağıdaki değişiklikler gerekecek:

1. **Bağımlılık kurulumu (dnf)**
   ```bash
   sudo dnf install python3-qt6 python3-qt6-qtwebengine python3-pip git
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
   Fedora depolarında `PyQt6` wheels yoksa sistem paketi `python3-qt6` kullanılır; venv içinde sistem paketine erişmek için `--system-site-packages` gerekebilir.

2. **SELinux**
   Fedora varsayılan olarak SELinux'u etkinleştirir. Uygulama yerel SQLite dosyası (`~/.local/share/foxai-settings/`) yazmaya çalışırsa SEPolitikası engelleyebilir. Gerekirse:
   ```bash
   sudo semanage fcontext -a -t user_home_t "/home/ilkaycan/.local/share/foxai-settings(/.*)?"
   sudo restorecon -Rv /home/ilkaycan/.local/share/foxai-settings
   ```

3. **Firewall (firewalld)**
   Güvenlik Duvarı modülü gerçek sistem entegrasyonu yaparken `firewalld` servisi (`systemctl status firewalld`) kullanılmalıdır. Arch'taki `iptables/nftables` varsayımı Fedora'da farklıdır.

4. **Paket yöneticisi**
   `software.py` modülünde Arch için `pacman` yerine Fedora için `dnf` çağrıları entegre edilmelidir.

5. **GRUB / Önyükleyici**
   Fedora genelde GRUB2 kullanır; `boot.py` üzerinden gerçek GRUB yapılandırma dosyaları (`/boot/grub2/grub.cfg`, `/etc/default/grub`) doğru yolla işaret edilmelidir.

6. **Masaüstü entegrasyonu**
   `foxai-settings.desktop` dosyası `/usr/share/applications/` veya `~/.local/share/applications/` kopyalanmalı ve `Exec` yolu Fedora dosya yapısına göre güncellenmeli.

## Geliştirici
İlkaycan (Can-5) — https://github.com/Can-5  
Foxai ekosistemi (Foxai Browser, Foxai Shield, Jarvis-ai, Foxai Sentinel)'nin bir parçasıdır.

## Lisans
[MIT](LICENSE)
