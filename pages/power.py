"""Güç yönetimi ayarları sayfası."""

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


class PowerPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        lay.addWidget(SectionLabel("Güç ve pil"))
        card = Card("Güç modu", "Performans ve tüketim dengelemesi.")
        modes = [
            ("Verimlilik", "eco"),
            ("Dengeli", "balanced"),
            ("Performans", "performance"),
        ]
        current = self.get("power_mode", "balanced")
        mode_ctrl = SelectControl(modes, current)
        mode_ctrl.changed.connect(lambda v: self.set("power_mode", v))
        card.add_widget(
            SettingRow(
                "Güç profili", "İşlemci ve ekran kartı tüketimini ayarlar.", mode_ctrl
            )
        )
        lay.addWidget(card)

        card2 = Card(
            "Uyku ve ekran kapanışı", "Cihazın ne zaman uyumasına karar verin."
        )
        sleep_ac = SelectControl(
            [
                ("Hiçbir zaman", -1),
                ("1 dakika", 1),
                ("5 dakika", 5),
                ("15 dakika", 15),
                ("30 dakika", 30),
            ],
            self.get("sleep_ac", 15),
        )
        sleep_ac.changed.connect(lambda v: self.set("sleep_ac", v))
        card2.add_widget(
            SettingRow("Şarj iken uyuma geç", "Şarj cihazı takılıyken.", sleep_ac)
        )
        sleep_bat = SelectControl(
            [
                ("Hiçbir zaman", -1),
                ("1 dakika", 1),
                ("5 dakika", 5),
                ("10 dakika", 10),
                ("15 dakika", 15),
            ],
            self.get("sleep_bat", 5),
        )
        sleep_bat.changed.connect(lambda v: self.set("sleep_bat", v))
        card2.add_widget(
            SettingRow("Pilde uyuma geç", "Pil ile çalışırken.", sleep_bat)
        )
        lay.addWidget(card2)

        card3 = Card("Ekran kilidi", "Güvenlik için kilitleme ayarları.")
        lock = ToggleControl(self.get("auto_lock", True))
        lock.toggled_value.connect(lambda v: self.set("auto_lock", v))
        card3.add_widget(
            SettingRow(
                "Otomatik ekran kilidi", "Belirli süre sonra ekranı kilitler.", lock
            )
        )
        lock_time = SelectControl(
            [
                ("30 saniye", 30),
                ("1 dakika", 60),
                ("5 dakika", 300),
                ("15 dakika", 900),
            ],
            self.get("lock_after", 60),
        )
        lock_time.changed.connect(lambda v: self.set("lock_after", v))
        card3.add_widget(
            SettingRow("Kilitlenme süresi", "Boşalma sonrası kilitlenme.", lock_time)
        )
        lay.addWidget(card3)

        lay.addStretch()
