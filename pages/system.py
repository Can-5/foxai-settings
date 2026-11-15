"""Sistem ayarları sayfası."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from pages.base_page import BasePage
from theme import ACCENT
from widgets import (
    ActionRow,
    Card,
    SectionLabel,
    SettingRow,
    TextControl,
    ToggleControl,
)


class SystemPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        # Cihaz
        lay.addWidget(SectionLabel("Cihaz"))
        card = Card("Cihaz adı", "Ağda ve sistemde gösterilecek isim.")
        card.add_widget(
            SettingRow(
                "Cihaz ismi",
                "Bu bilgisayarın ağdaki görünen adıdır.",
                TextControl(self.get("device_name", "CachyOS-PC"), "Cihaz ismi"),
            )
        )
        lay.addWidget(card)

        # Güncellemeler
        lay.addWidget(SectionLabel("Güncellemeler"))
        card2 = Card(
            "Yazılım güncellemeleri", "Sistem ve uygulama güncellemelerini yönetin."
        )
        card2.add_widget(
            self._bool_row(
                "Otomatik güncellemeleri denetle",
                "Yeni sürümleri arka planda kontrol eder.",
                "auto_updates",
            )
        )
        card2.add_widget(
            self._bool_row(
                "Güvenlik yamalarını otomatik kur",
                "Önemli güvenlik güncellemelerini otomatik uygular.",
                "security_updates",
            )
        )
        btn_check = QPushButton("Güncellemeleri denetle")
        btn_check.setObjectName("primary")
        btn_check.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_check.clicked.connect(
            lambda: self._notify("Güncelleme denetleme", "Sisteminiz güncel.")
        )
        card2.add_widget(
            ActionRow(
                "Güncellemeleri denetle", "Mevcut güncellemeleri arar.", "Denetle"
            )
        )
        lay.addWidget(card2)

        # Tarih ve saat
        lay.addWidget(SectionLabel("Tarih ve Saat"))
        card3 = Card("Zaman ayarları", "Sistem saati ve dilim ayarları.")
        card3.add_widget(
            SettingRow(
                "Otomatik saat",
                "İnternet üzerinden zamanı senkronize eder.",
                ToggleControl(True),
            )
        )
        card3.add_widget(
            SettingRow(
                "Bölge / Dilim",
                "Coğrafi konumunuza göre saat dilimi.",
                QLabel("İstanbul (GMT+3)"),
            )
        )
        lay.addWidget(card3)

        # Hakkında
        lay.addWidget(SectionLabel("Hakkında"))
        card4 = Card(
            "Foxai Settings", "Modern, gizlilik odaklı Linux ayarlar uygulaması."
        )
        about = QLabel(
            "Sürüm 1.0.0 · CachyOS / Arch Linux\n"
            "Geliştirici: İlkaycan (Can-5)\n"
            "Gizlilik odaklı · Sıfır telemetri · Açık kaynak"
        )
        about.setStyleSheet(
            "color: #94a3b8; font-size: 13px; line-height: 1.6; background: transparent;"
        )
        about.setWordWrap(True)
        card4.content_lay.addWidget(about)
        lay.addWidget(card4)

        lay.addStretch()

    def _notify(self, title: str, msg: str) -> None:
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.information(self, title, msg)
