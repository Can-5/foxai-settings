"""Donanım & Sistem Bilgisi sayfası."""

from __future__ import annotations

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from pages.base_page import BasePage
from widgets import Card, SectionLabel, SettingRow


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

        # İşletim sistemi
        lay.addWidget(SectionLabel("İşletim Sistemi"))
        card = Card("Sistem sürümü", "Çalıştırılan dağıtım ve çekirdek bilgileri.")
        card.add_widget(self._kv("Dağıtım", "CachyOS (Arch tabanlı)"))
        card.add_widget(self._kv("Çekirdek", "Linux 6.12.x-cachyos"))
        card.add_widget(self._kv("Masaüstü ortamı", "KDE Plasma / Foxai"))
        card.add_widget(self._kv("Sürüm", "Foxai Settings 1.0.0"))
        lay.addWidget(card)

        # İşlemci
        lay.addWidget(SectionLabel("İşlemci (CPU)"))
        card2 = Card("İşlemci bilgisi", "Model, çekirdek sayı ve saat hızı.")
        card2.add_widget(self._kv("Model", "Intel Core i7 (Monster Tulpar T7)"))
        card2.add_widget(
            self._kv("Çekirdek / İş parçacığı", "8 Çekirdek · 16 İş parçacığı")
        )
        card2.add_widget(self._kv("Maks. saat", "4.80 GHz"))
        lay.addWidget(card2)

        # Bellek
        lay.addWidget(SectionLabel("Bellek (RAM)"))
        card3 = Card("Sistem belleği", "Kullanılabilir ve toplam RAM.")
        card3.add_widget(self._kv("Toplam bellek", "16 GB DDR5"))
        card3.add_widget(self._kv("Kullanılabilir", "8.2 GB"))
        card3.add_widget(self._kv("Kullanım", "%42"))
        lay.addWidget(card3)

        # Disk
        lay.addWidget(SectionLabel("Depolama (Disk)"))
        card4 = Card("Disk bölümleri", "Sürücülerin kapasite ve kullanım durumu.")
        card4.add_widget(self._kv("Ana bölüm (/)", "NVMe SSD · 512 GB · %38 kullanım"))
        lay.addWidget(card4)

        # GPU
        lay.addWidget(SectionLabel("Ekran Kartı (GPU)"))
        card5 = Card("Grafik işlemci", "GPU modeli ve sürücü bilgisi.")
        card5.add_widget(self._kv("Model", "NVIDIA RTX 3060 · 12 GB VRAM"))
        card5.add_widget(self._kv("Sürücü", "NVIDIA 570.x — Kurulu ve etkin"))
        lay.addWidget(card5)

        lay.addStretch()
