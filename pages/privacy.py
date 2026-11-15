"""Gizlilik ve güvenlik ayarları sayfası."""

from __future__ import annotations

from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from pages.base_page import BasePage
from theme import ACCENT
from widgets import ActionRow, Card, SectionLabel, SettingRow, ToggleControl


class PrivacyPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        lay.addWidget(SectionLabel("Gizlilik"))
        card = Card(
            "Konum, kamera ve mikrofon",
            "Uygulamaların cihaz Sensörlerine erişimini kontrol edin.",
        )
        loc = ToggleControl(self.get("location_access", False))
        loc.toggled_value.connect(lambda v: self.set("location_access", v))
        card.add_widget(
            SettingRow("Konum erişimi", "Harita ve hava durumu uygulamaları için.", loc)
        )
        cam = ToggleControl(self.get("camera_access", False))
        cam.toggled_value.connect(lambda v: self.set("camera_access", v))
        card.add_widget(
            SettingRow("Kamera erişimi", "Görüşme ve kayıt uygulamaları için.", cam)
        )
        mic = ToggleControl(self.get("microphone_access", False))
        mic.toggled_value.connect(lambda v: self.set("microphone_access", v))
        card.add_widget(
            SettingRow(
                "Mikrofon erişimi", "Sesli komut ve görüşme uygulamaları için.", mic
            )
        )
        lay.addWidget(card)

        card2 = Card(
            "Telemetri ve veri", "Foxai Settings sıfır telemetri ilkesine bağlıdır."
        )
        card2.add_widget(
            SettingRow(
                "Kullanım verileri gönder",
                "Hiçbir veri gönderilmez.",
                ToggleControl(False),
            )
        )
        card2.add_widget(
            SettingRow(
                "Hata raporları",
                "Otomatik çöküş raporları devre dışı.",
                ToggleControl(False),
            )
        )
        lay.addWidget(card2)

        card3 = Card("Erişim ve şifre", "Kullanıcı hesabı güvenliği.")
        card3.add_widget(
            ActionRow(
                "Şifreyi değiştir",
                "Mevcut hesabınızın şifresini güncelleyin.",
                "Değiştir",
            )
        )
        card3.add_widget(
            ActionRow(
                "İki faktörlü doğrulama",
                "Ek güvenlik katmanını etkinleştirin.",
                "Ayarla",
            )
        )
        lay.addWidget(card3)

        lay.addStretch()
