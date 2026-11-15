"""Yazılım & Güncelleme sayfası (depo, paket, güncelleme yönetimi)."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pages.base_page import BasePage
from theme import ACCENT
from widgets import (
    Card,
    SectionLabel,
    SettingRow,
    SelectControl,
    ToggleControl,
    TextControl,
)


class SoftwarePage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        # Güncellemeler
        lay.addWidget(SectionLabel("Yazılım Güncellemeleri"))
        card = Card(
            "Güncelleme politikası",
            "Sistem ve uygulama paketlerini güncellemeleri kontrol edin.",
        )
        card.add_widget(
            self._bool_row(
                "Otomatik güncellemeleri denetle",
                "Yeni sürümleri arka planda arar.",
                "sw_auto_check",
            )
        )
        card.add_widget(
            self._bool_row(
                "Güvenlik güncellemelerini otomatik kur",
                "Önemli yamaları anında uygular.",
                "sw_security_auto",
            )
        )
        card.add_widget(
            self._bool_row(
                "Flatpak güncellemelerini dahil et",
                "Flatpak uygulamalarını da güncelleme denetimine ekler.",
                "sw_flatpak",
            )
        )
        btn_check = QPushButton("Güncellemeleri denetle")
        btn_check.setObjectName("primary")
        btn_check.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_check.clicked.connect(
            lambda: self._notify(
                "Güncelleme denetleme",
                "3 güncelleme bulundu: linux-firmware, mesa, firefox.",
            )
        )
        card.content_lay.addWidget(btn_check)
        lay.addWidget(card)

        # Depolar
        lay.addWidget(SectionLabel("Yazılım Depoları"))
        card2 = Card("Etkin depolar", "Paket kaynaklarını yönetin.")
        repos = [
            ("fedora", "Fedora resmi deposu", True),
            ("updates", "Kararlı güncellemeler", True),
            ("rpmfusion-free", "RPM Fusion — özgür yazılım (free)", False),
            ("rpmfusion-nonfree", "RPM Fusion — freeware (nonfree)", False),
        ]
        for repo, desc, enabled in repos:
            row = QWidget()
            rlay = QHBoxLayout(row)
            rlay.setContentsMargins(0, 0, 0, 0)
            rlay.setSpacing(12)
            info = QWidget()
            ilay = QVBoxLayout(info)
            ilay.setContentsMargins(0, 0, 0, 0)
            ilay.setSpacing(2)
            r = QLabel(repo)
            r.setStyleSheet(
                "color: #f8fafc; font-size: 13px; font-weight: 700; background: transparent;"
            )
            d = QLabel(desc)
            d.setStyleSheet("color: #94a3b8; font-size: 12px; background: transparent;")
            ilay.addWidget(r)
            ilay.addWidget(d)
            tgl = ToggleControl(enabled)
            tgl.toggled_value.connect(lambda _, n=repo: self.set(f"repo_{n}", _))
            rlay.addWidget(info, 1)
            rlay.addWidget(tgl, 0)
            row.setStyleSheet("background: transparent; border-radius: 8px;")
            card2.content_lay.addWidget(row)
        lay.addWidget(card2)

        # Paket kurulumu
        lay.addWidget(SectionLabel("Paket Yönetimi"))
        card3 = Card("Paket ara ve kur", "Depodan paket arayın ve kurun.")
        search = TextControl("", "Paket adı girin (örn. gimp, vlc, libreoffice)")
        btn_install = QPushButton("Ara ve Kur")
        btn_install.setObjectName("primary")
        btn_install.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_install.clicked.connect(
            lambda: self._notify(
                "Kurulum", f"'{search.value()}' paketi kuyruğa alındı."
            )
        )
        slay = QHBoxLayout()
        slay.setSpacing(10)
        slay.addWidget(search, 1)
        slay.addWidget(btn_install, 0)
        card3.content_lay.addLayout(slay)
        lay.addWidget(card3)

        lay.addStretch()

    def _notify(self, title: str, msg: str) -> None:
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.information(self, title, msg)
