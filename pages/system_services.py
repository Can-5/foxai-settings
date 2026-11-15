"""Sistem Servisleri ayarları sayfası."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pages.base_page import BasePage
from theme import ACCENT
from widgets import Card, SectionLabel, SettingRow, ToggleControl


class SystemServicesPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        lay.addWidget(SectionLabel("Sistem Servisleri"))
        card = Card(
            "Arka plan servisleri",
            "Sistem servislerini etkinleştirin veya devre dışı bırakın.",
        )
        services = [
            ("Bluetooth servisi", "bluetooth", False),
            ("SSH sunucusu", "ssh", False),
            ("Cron / Zamanlayıcı", "cron", True),
            ("Güncelleme servisi", "updates", True),
            ("Telemetri toplayıcı", "telemetry", False),
            ("Yedekleme servisi", "backup", False),
        ]
        for name, key, enabled in services:
            tgl = ToggleControl(enabled)
            tgl.toggled_value.connect(lambda _, k=key: self.set(f"svc_{k}", _))
            row = QWidget()
            rlay = QHBoxLayout(row)
            rlay.setContentsMargins(0, 0, 0, 0)
            rlay.setSpacing(12)
            nm = QLabel(name)
            nm.setStyleSheet(
                "color: #f8fafc; font-size: 13px; font-weight: 600; background: transparent;"
            )
            desc = QLabel(key)
            desc.setStyleSheet(
                "color: #94a3b8; font-size: 11px; background: transparent;"
            )
            info = QWidget()
            ilay = QVBoxLayout(info)
            ilay.setContentsMargins(0, 0, 0, 0)
            ilay.setSpacing(2)
            ilay.addWidget(nm)
            ilay.addWidget(desc)
            rlay.addWidget(info, 1)
            rlay.addWidget(tgl, 0)
            row.setStyleSheet("background: transparent; border-radius: 8px;")
            card.content_lay.addWidget(row)
        lay.addWidget(card)

        card2 = Card(
            "Servis durumu", "Şu anda çalışan sistem servislerinin genel görünümü."
        )
        status = QLabel("Tüm temel servisler aktif · 2 servis durduruldu")
        status.setStyleSheet(
            "color: #94a3b8; font-size: 13px; background: transparent;"
        )
        card2.content_lay.addWidget(status)
        btn_refresh = QPushButton("Durumu yenile")
        btn_refresh.setObjectName("ghost")
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.clicked.connect(
            lambda: self._notify("Servisler", "Servis durumu güncellendi.")
        )
        card2.content_lay.addWidget(btn_refresh)
        lay.addWidget(card2)

        lay.addStretch()

    def _notify(self, title: str, msg: str) -> None:
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.information(self, title, msg)
