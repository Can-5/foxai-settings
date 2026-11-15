"""Klavye ayarları sayfası."""

from __future__ import annotations

from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from pages.base_page import BasePage
from theme import ACCENT
from widgets import (
    Card,
    SectionLabel,
    SelectControl,
    SettingRow,
    SliderControl,
    ToggleControl,
)


class KeyboardPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        lay.addWidget(SectionLabel("Klavye"))
        card = Card(
            "Klavye dili ve düzen", "Girdi dili ve klavyenin tuş düzenini seçin."
        )
        langs = [
            ("Türkçe Q", "tr"),
            ("İngilizce US", "en"),
            ("Almanca", "de"),
            ("Fransızca", "fr"),
        ]
        current = self.get("keyboard_lang", "tr")
        lang_ctrl = SelectControl(langs, current)
        lang_ctrl.changed.connect(lambda v: self.set("keyboard_lang", v))
        card.add_widget(
            SettingRow(
                "Dil / düzen", "Sistem genelinde kullanılan klavye dili.", lang_ctrl
            )
        )
        lay.addWidget(card)

        card2 = Card("Tuş tekrarı", "Basılı tuşların tekrar hızını ayarlayın.")
        delay = SliderControl(100, 1000, self.get("key_repeat_delay", 500), " ms")
        delay.changed.connect(lambda v: self.set("key_repeat_delay", v))
        card2.add_widget(
            SettingRow(
                "Tekrar gecikmesi",
                "Tuşun tekrar başlamadan önceki bekleme süresi.",
                delay,
            )
        )
        rate = SliderControl(10, 200, self.get("key_repeat_rate", 30), "")
        rate.changed.connect(lambda v: self.set("key_repeat_rate", v))
        card2.add_widget(
            SettingRow("Tekrar hızı", "Saniyede kaç kez tekrar edileceği.", rate)
        )
        lay.addWidget(card2)

        card3 = Card(
            "Erişilebilirlik", "Klavyeyi daha kolay kullanım için yapılandırın."
        )
        sticky = ToggleControl(self.get("sticky_keys", False))
        sticky.toggled_value.connect(lambda v: self.set("sticky_keys", v))
        card3.add_widget(
            SettingRow(
                "Tuş kilidi (sticky keys)", "Tek tuşla komut kümeleri kullanın.", sticky
            )
        )
        filter_keys = ToggleControl(self.get("filter_keys", False))
        filter_keys.toggled_value.connect(lambda v: self.set("filter_keys", v))
        card3.add_widget(
            SettingRow(
                "Tuş filtreleme", "Kısa veya yanlış basımları yoksayar.", filter_keys
            )
        )
        lay.addWidget(card3)

        lay.addStretch()
