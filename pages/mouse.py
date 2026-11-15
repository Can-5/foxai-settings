"""Fare ayarları sayfası."""

from __future__ import annotations

from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from pages.base_page import BasePage
from theme import ACCENT
from widgets import Card, SectionLabel, SliderControl, SettingRow, ToggleControl


class MousePage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        lay.addWidget(SectionLabel("Fare ve giriş cihazı"))
        card = Card("Fare hassasiyeti", "İşaretçi hareket hızını ayarlayın.")
        sens = SliderControl(1, 20, self.get("mouse_sensitivity", 10), "")
        sens.changed.connect(lambda v: self.set("mouse_sensitivity", v))
        card.add_widget(
            SettingRow(
                "Hassasiyet",
                "İşaretçiyi ne kadar hızlı hareket ettireceğini belirler.",
                sens,
            )
        )
        scroll = SliderControl(1, 20, self.get("scroll_speed", 5), " satır")
        scroll.changed.connect(lambda v: self.set("scroll_speed", v))
        card.add_widget(
            SettingRow("Kaydırma hızı", "Tek tekerlek kaydırmada satır sayısı.", scroll)
        )
        lay.addWidget(card)

        card2 = Card("Fare davranışı", "İki parmak ve davranış ayarları.")
        natural = ToggleControl(self.get("natural_scroll", False))
        natural.toggled_value.connect(lambda v: self.set("natural_scroll", v))
        card2.add_widget(
            SettingRow(
                "Doğal kaydırma", "İçeriği parmakla itmek gibi hareket eder.", natural
            )
        )
        tap = ToggleControl(self.get("tap_to_click", True))
        tap.toggled_value.connect(lambda v: self.set("tap_to_click", v))
        card2.add_widget(
            SettingRow(
                "Dokunma ile tıkla", "Touchpad üzerinde dokunarak tıklayın.", tap
            )
        )
        lay.addWidget(card2)

        card3 = Card("Sol / sağ takma", "Ekran kenarlarına otomatik oturtma.")
        snap = ToggleControl(self.get("snap_windows", True))
        snap.toggled_value.connect(lambda v: self.set("snap_windows", v))
        card3.add_widget(
            SettingRow(
                "Pencere oturtma",
                "Fareyle kenara sıçratınca pencereyi eşitleyin.",
                snap,
            )
        )
        lay.addWidget(card3)

        lay.addStretch()
