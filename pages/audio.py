"""Ses & Ayagıt ayarları sayfası."""

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
from widgets import (
    Card,
    SectionLabel,
    SelectControl,
    SettingRow,
    SliderControl,
    ToggleControl,
)


class AudioPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        lay.addWidget(SectionLabel("Ses"))
        card = Card("Çalma aygıtı", "Varsayılan ses çıkışını seçin.")
        out = SelectControl(
            [
                ("Hoparlörler", "speakers"),
                ("Kulaklık", "headphones"),
                ("HDMI / Ekran", "hdmi"),
                ("Bluetooth hoparlör", "bluetooth"),
            ],
            self.get("audio_output", "speakers"),
        )
        out.changed.connect(lambda v: self.set("audio_output", v))
        card.add_widget(
            SettingRow("Çıkış aygıtı", "Sesin hangi aygıttan çıkacağını belirler.", out)
        )
        lay.addWidget(card)

        card2 = Card("Ses seviyeleri", "Çıkış ve giriş sesini ayarlayın.")
        master = SliderControl(0, 100, self.get("audio_master", 75), "%")
        master.changed.connect(lambda v: self.set("audio_master", v))
        card2.add_widget(SettingRow("Ana ses", "Genel çıkış ses seviyesi.", master))
        mic = SliderControl(0, 100, self.get("audio_mic", 60), "%")
        mic.changed.connect(lambda v: self.set("audio_mic", v))
        card2.add_widget(SettingRow("Mikrofon", "Giriş mikrofon ses seviyesi.", mic))
        lay.addWidget(card2)

        card3 = Card("Davranış", "Sesli uyarmalar ve sistem sesleri.")
        sys_sound = ToggleControl(self.get("audio_system_sound", True))
        sys_sound.toggled_value.connect(lambda v: self.set("audio_system_sound", v))
        card3.add_widget(
            SettingRow(
                "Sistem sesleri", "Uyarı ve bildirim seslerini etkinleştir.", sys_sound
            )
        )
        lay.addWidget(card3)

        lay.addStretch()
