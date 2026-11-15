"""Ekran (görüntü) ayarları sayfası."""

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


class DisplayPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        # Çözünürlük
        lay.addWidget(SectionLabel("Ekran"))
        card = Card("Ekran çözünürlüğü", "Müntazam görünüm için piksel boyutu.")
        resolutions = [
            ("1920 × 1080 (Full HD)", "1920x1080"),
            ("2560 × 1440 (QHD)", "2560x1440"),
            ("3840 × 2160 (4K UHD)", "3840x2160"),
            ("1366 × 768 (HD)", "1366x768"),
        ]
        current = self.get("resolution", "1920x1080")
        res_ctrl = SelectControl(resolutions, current)
        res_ctrl.changed.connect(lambda v: self.set("resolution", v))
        card.add_widget(SettingRow("Çözünürlük", "Ekrandaki piksel sayısı.", res_ctrl))
        lay.addWidget(card)

        # Yenileme hızı
        card2 = Card("Yenileme hızı", "Ekranın saniyede kaç kare gösterdiği.")
        rates = [("60 Hz", 60), ("75 Hz", 75), ("120 Hz", 120), ("144 Hz", 144)]
        current_rate = self.get("refresh_rate", 60)
        rate_ctrl = SelectControl(rates, current_rate)
        rate_ctrl.changed.connect(lambda v: self.set("refresh_rate", v))
        card2.add_widget(
            SettingRow(
                "Yenileme hızı",
                "Daha yüksek değer daha akıcı görünüm sağlar.",
                rate_ctrl,
            )
        )
        lay.addWidget(card2)

        # Parlaklık
        card3 = Card("Parlaklık", "Ekranın aydınlık seviyesini ayarlayın.")
        brightness = SliderControl(0, 100, self.get("brightness", 80), "%")
        brightness.changed.connect(lambda v: self.set("brightness", v))
        card3.add_widget(
            SettingRow(
                "Ekran parlaklığı",
                "Göz yorgunluğunu azaltmak için düşürün.",
                brightness,
            )
        )
        lay.addWidget(card3)

        gece = ToggleControl(self.get("night_light", False))
        gece.toggled_value.connect(lambda v: self.set("night_light", v))
        card3.add_widget(
            SettingRow(
                "Gece ışığı", "Mavi ışığı azaltarak geceleri gözünü korur.", gece
            )
        )
        lay.addWidget(card3)

        # Çoklu ekran
        card4 = Card("Çoklu ekran", "İkincil monitörleri yapılandırın.")
        multi = QLabel("İkincil ekran: Bağlı değil")
        multi.setStyleSheet("color: #94a3b8; font-size: 13px; background: transparent;")
        card4.content_lay.addWidget(multi)
        btn_detect = QPushButton("Ekranları denetle")
        btn_detect.setObjectName("ghost")
        btn_detect.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_detect.clicked.connect(
            lambda: self._notify("Ekran denetleme", "İkincil ekran bulunamadı.")
        )
        card4.content_lay.addWidget(btn_detect)
        lay.addWidget(card4)

        lay.addStretch()

    def _notify(self, title: str, msg: str) -> None:
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.information(self, title, msg)
