# Windows sürümü (Foxai-Settings.exe)

Linux'ta native Windows (.exe) derlemesi **mümkün değildir**; Windows binary'si yalnızca
Windows üzerinde (veya GitHub Actions `windows-latest` runner'ında) derlenebilir.

## Seçenek 1 — GitHub Actions (önerilen, makine gerekmez)

Repo'ya `.github/workflows/windows-build.yml` workflow'u eklenirse
(`git push` sonrası otomatik çalışır):

1. Repo sayfasında **Actions** sekmesi → **windows-build**.
2. En üstteki (veya seçtiğiniz) çalıştırma → **Artifacts** → `foxai-settings-windows` indirin.
3. İndirdiğiniz `.zip` içinde `Foxai-Settings.exe` bulunur.

Bu workflow projeye dahildir; ek onay gerektirmeden CI'da derlenir.

## Seçenek 2 — Windows makinede yerel derleme

Gereksinimler: Windows 10/11 + Python 3.11+ (python.org'dan, "Add python.exe to PATH" işaretli).

```bat
packaging\windows\Build-Windows.bat
```

Çıktı: `dist\Foxai-Settings.exe` (tek dosya, PyQt6 gömülü, ~180 MB).

## Notlar

- Exe **imzasız**; SmartScreen uyarısında "Diğer bilgiler → Yine de çalıştır" gerekir.
- Uygulama yine SQLite'ı `%USERPROFILE%\.local\share\foxai-settings\settings.db` içine değil;
  `database.py` `Path.home()` kullandığı için Windows'ta da kullanıcı klasörü kapsamındadır.
- Sistem çağrıları (dnf / GRUB2 / firewalld) hâlâ Linux'a özgüdür; Windows'ta bu sayfalar
  ilgili araçlar yok diye gösterir/no-op kalır. Uygulama açılır; sistem yönetimi bölümü
  Linux içindir.
