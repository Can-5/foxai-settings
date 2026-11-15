"""Donanım & Sistem Bilgisi sayfası."""

from __future__ import annotations

import os
import platform
import shutil

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from pages.base_page import BasePage
from widgets import Card, SectionLabel, SettingRow


def _os_release() -> dict[str, str]:
    """/etc/os-release dosyasını salt-okunur ayrıştırır."""
    data: dict[str, str] = {}
    try:
        with open("/etc/os-release", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                data[key.strip()] = value.strip().strip('"')
    except OSError:
        pass
    return data


def _meminfo() -> dict[str, int]:
    """/proc/meminfo değerlerini kB cinsinden döndürür (salt-okunur)."""
    data: dict[str, int] = {}
    try:
        with open("/proc/meminfo", encoding="utf-8") as f:
            for line in f:
                parts = line.replace(":", " ").split()
                if len(parts) >= 2 and parts[1].isdigit():
                    data[parts[0]] = int(parts[1])
    except OSError:
        pass
    return data


def _cpu_model() -> str:
    try:
        with open("/proc/cpuinfo", encoding="utf-8") as f:
            for line in f:
                if line.lower().startswith(("model name", "model")):
                    _, _, value = line.partition(":")
                    if value.strip():
                        return value.strip()
    except OSError:
        pass
    return platform.processor() or "bilinmiyor"


def _cpu_max_ghz() -> str:
    for path in (
        "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq",
        "/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq",
    ):
        try:
            with open(path, encoding="utf-8") as f:
                khz = int(f.read().strip())
                if khz > 0:
                    return f"{khz / 1_000_000:.2f} GHz"
        except (OSError, ValueError):
            continue
    return "bilinmiyor"


def _gpu_driver() -> str:
    """DRM kartlarının sürücü adını /sys üzerinden okur (salt-okunur)."""
    drivers: list[str] = []
    drm = "/sys/class/drm"
    try:
        for entry in sorted(os.listdir(drm)):
            if not entry.startswith("card") or "-" in entry:
                continue
            uevent = os.path.join(drm, entry, "device", "uevent")
            try:
                with open(uevent, encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("DRIVER="):
                            drv = line.partition("=")[2].strip()
                            if drv and drv not in drivers:
                                drivers.append(drv)
            except OSError:
                continue
    except OSError:
        pass
    return ", ".join(drivers) if drivers else "Algılanamadı"


def _gb(kb: int) -> str:
    return f"{kb / 1024 / 1024:.1f} GB"


class SystemInfoPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _kv(self, title: str, value: str) -> SettingRow:
        return SettingRow(title, "", QLabel(value))

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        osrel = _os_release()
        mem = _meminfo()
        total_kb = mem.get("MemTotal", 0)
        avail_kb = mem.get("MemAvailable", 0)
        mem_used_pct = (
            round((1 - avail_kb / total_kb) * 100) if total_kb and avail_kb else None
        )
        try:
            usage = shutil.disk_usage("/")
            disk_total = usage.total / 1024**3
            disk_pct = round(usage.used / usage.total * 100)
            disk_text = f"{disk_total:.0f} GB · %{disk_pct} kullanım"
        except OSError:
            disk_text = "bilinmiyor"

        # İşletim sistemi
        lay.addWidget(SectionLabel("İşletim Sistemi"))
        card = Card("Sistem sürümü", "Çalıştırılan dağıtım ve çekirdek bilgileri.")
        card.add_widget(
            self._kv("Dağıtım", osrel.get("PRETTY_NAME", platform.system()))
        )
        card.add_widget(self._kv("Çekirdek", f"Linux {platform.release()}"))
        card.add_widget(
            self._kv(
                "Masaüstü ortamı",
                os.environ.get("XDG_CURRENT_DESKTOP", "bilinmiyor"),
            )
        )
        card.add_widget(self._kv("Sürüm", "Foxai Settings 1.0.0"))
        lay.addWidget(card)

        # İşlemci
        cpu_count = os.cpu_count() or 0
        lay.addWidget(SectionLabel("İşlemci (CPU)"))
        card2 = Card("İşlemci bilgisi", "Model, çekirdek sayı ve saat hızı.")
        card2.add_widget(self._kv("Model", _cpu_model()))
        card2.add_widget(self._kv("İş parçacığı", str(cpu_count) if cpu_count else "bilinmiyor"))
        card2.add_widget(self._kv("Maks. saat", _cpu_max_ghz()))
        lay.addWidget(card2)

        # Bellek
        lay.addWidget(SectionLabel("Bellek (RAM)"))
        card3 = Card("Sistem belleği", "Kullanılabilir ve toplam RAM.")
        card3.add_widget(
            self._kv("Toplam bellek", _gb(total_kb) if total_kb else "bilinmiyor")
        )
        card3.add_widget(
            self._kv("Kullanılabilir", _gb(avail_kb) if avail_kb else "bilinmiyor")
        )
        card3.add_widget(
            self._kv(
                "Kullanım",
                f"%{mem_used_pct}" if mem_used_pct is not None else "bilinmiyor",
            )
        )
        lay.addWidget(card3)

        # Disk
        lay.addWidget(SectionLabel("Depolama (Disk)"))
        card4 = Card("Disk bölümleri", "Sürücülerin kapasite ve kullanım durumu.")
        card4.add_widget(self._kv("Ana bölüm (/)", disk_text))
        lay.addWidget(card4)

        # GPU
        lay.addWidget(SectionLabel("Ekran Kartı (GPU)"))
        card5 = Card("Grafik işlemci", "GPU sürücü bilgisi (DRM).")
        card5.add_widget(self._kv("Sürücü", _gpu_driver()))
        lay.addWidget(card5)

        lay.addStretch()
