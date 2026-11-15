"""Görünüm ayarları sayfası."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from pages.base_page import BasePage
from theme import ACCENT
from widgets import (
    ActionRow,
    Card,
    SectionLabel,
    SelectControl,
    SettingRow,
    SliderControl,
    ToggleControl,
)


class AppearancePage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _bool_row(self, title: str, desc: str, key: str) -> SettingRow:
        ctrl = ToggleControl(self.get(key, True))
        ctrl.toggled_value.connect(lambda v: self.set(key, v))
        return SettingRow(title, desc, ctrl)

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        # Tema
        lay.addWidget(SectionLabel("Tema ve Renk"))
        card = Card("Görünüm teması", "Uygulamanın genel renk şemasını seçin.")
        card.add_widget(
            self._bool_row(
                "Koyu tema", "Göz yorgunluğunu azaltan koyu arayüz.", "dark_theme"
            )
        )
        color_lbl = QLabel(ACCENT)
        color_lbl.setStyleSheet(
            f"color: {ACCENT}; font-weight: 700; background: transparent; "
            f"padding: 6px 12px; border: 1px solid {ACCENT}; border-radius: 8px;"
        )
        card.add_widget(SettingRow("Vurgu rengi", "Etkin öğelerin rengi.", color_lbl))
        lay.addWidget(card)

        # Akcent rengi butonları
        card2 = Card("Vurgu (akcent) rengi", "Tüm etkileşimli elemanların rengi.")
        colors = [
            ("Mavi", "#409eff"),
            ("Yeşil", "#22c55e"),
            ("Kırmızı", "#ef4444"),
            ("Mor", "#a855f7"),
            ("Turuncu", "#f59e0b"),
            ("Siyan", "#06b6d4"),
        ]
        color_row = QWidget()
        cl = QHBoxLayout(color_row)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(10)
        for label, hexv in colors:
            btn = QPushButton(label)
            btn.setFixedSize(70, 34)
            btn.setStyleSheet(
                f"background: {hexv}; border: none; border-radius: 10px; color: #fff; "
                f"font-weight: 700; font-size: 12px;"
            )
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, h=hexv: self.set("accent_color", h))
            cl.addWidget(btn)
        cl.addStretch()
        card2.add_widget(color_row)
        lay.addWidget(card2)

        # Yazı tipi boyutu
        card3 = Card("Yazı tipi", "Arayüz metinlerinin görünümü.")
        font_sizes = [("Küçük", 12), ("Normal", 14), ("Büyük", 16), ("Çok Büyük", 18)]
        current = self.get("font_size", 14)
        font_ctrl = SelectControl(font_sizes, current)
        font_ctrl.changed.connect(lambda v: self.set("font_size", v))
        card3.add_widget(
            SettingRow("Yazı boyutu", "Arayüz genelindeki metin boyutu.", font_ctrl)
        )
        lay.addWidget(card3)

        # Duvar kağıdı
        card4 = Card("Duvar kağıdı", "Arka plan görselini seçin.")
        card4.add_widget(
            ActionRow(
                "Duvar kağıdı seç", "Bilgisayarınızdan bir görsel seçin.", "Gözat"
            )
        )
        lay.addWidget(card4)

        lay.addStretch()
