"""Görünüm ayarları sayfası."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from pages.base_page import BasePage
from theme import ACCENT, DANGER, SUCCESS, WARN
from widgets import (
    ActionRow,
    Card,
    SectionLabel,
    SelectControl,
    SettingRow,
    SliderControl,
)


class AppearancePage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = self.lay

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
        card2 = Card("Vurgu rengi", "Tüm etkileşimli elemanların rengi.")
        colors = [
            ("Pirinç", f"{ACCENT}"),
            ("Yosun", f"{SUCCESS}"),
            ("Kiremit", f"{DANGER}"),
            ("Yunus", "#3e7a8a"),
            ("Göktaşı", "#5a7a9a"),
            ("Krem", "#e9e6df"),
        ]
        color_row = QWidget()
        cl = QHBoxLayout(color_row)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(10)
        for label, hexv in colors:
            btn = QPushButton(label)
            btn.setFixedSize(70, 34)
            dark_text = {f"{ACCENT}".lower(), f"{SUCCESS}".lower(), f"{WARN}".lower(), "#e9e6df"}
            ink = "#14171a" if hexv.lower() in dark_text else "#ffffff"
            btn.setStyleSheet(
                f"background: {hexv}; border: none; border-radius: 10px; color: {ink}; "
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
