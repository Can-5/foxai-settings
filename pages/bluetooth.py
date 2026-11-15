"""Bluetooth ayarları sayfası."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from pages.base_page import BasePage
from theme import ACCENT
from widgets import Card, SectionLabel, SettingRow, ToggleControl


class BluetoothPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        lay.addWidget(SectionLabel("Bluetooth"))
        card = Card("Bluetooth", "Kablosuz dış çevre birimlerini eşleştirin.")
        bt = ToggleControl(self.get("bluetooth_enabled", False))
        bt.toggled_value.connect(lambda v: self.set("bluetooth_enabled", v))
        card.add_widget(
            SettingRow("Bluetooth etkin", "Cihazları keşfet ve eşleştir.", bt)
        )
        status = QLabel("Cihaz bulunamadı · Eşleştirilmiş cihaz yok")
        status.setStyleSheet(
            "color: #94a3b8; font-size: 13px; background: transparent;"
        )
        card.content_lay.addWidget(status)
        btn_scan = QPushButton("Cihazları tara")
        btn_scan.setObjectName("ghost")
        btn_scan.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_scan.clicked.connect(
            lambda: self._notify("Bluetooth tarama", "Hiçbir cihaz bulunamadı.")
        )
        card.content_lay.addWidget(btn_scan)
        lay.addWidget(card)

        lay.addStretch()

    def _notify(self, title: str, msg: str) -> None:
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.information(self, title, msg)
