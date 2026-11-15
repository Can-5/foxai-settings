"""Bildirim ayarları sayfası."""

from __future__ import annotations

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


class NotificationsPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        lay.addWidget(SectionLabel("Bildirimler"))
        card = Card(
            "Bildirimleri yönet",
            "Uygulamaların size bildirim görebilmesini kontrol edin.",
        )
        card.add_widget(
            self._bool_row(
                "Bildirimleri etkinleştir",
                "Sistem ve uygulama bildirimlerini gösterir.",
                "notifications_enabled",
            )
        )
        sound = ToggleControl(self.get("notification_sound", True))
        sound.toggled_value.connect(lambda v: self.set("notification_sound", v))
        card.add_widget(
            SettingRow(
                "Bildirim sesi", "Yeni bildirim geldiğinde sesli uyarı verir.", sound
            )
        )
        do_not = ToggleControl(self.get("do_not_disturb", False))
        do_not.toggled_value.connect(lambda v: self.set("do_not_disturb", v))
        card.add_widget(
            SettingRow(
                "Rahatsız etmeyin",
                "Bildirimleri susturur ama günlüğe kaydeder.",
                do_not,
            )
        )
        lay.addWidget(card)

        card2 = Card("Bildirim ses seviyesi", "Bildirimlerin ses gücü.")
        vol = SliderControl(0, 100, self.get("notification_volume", 70), "%")
        vol.changed.connect(lambda v: self.set("notification_volume", v))
        card2.add_widget(SettingRow("Ses", "Bildirim sesi seviyesi.", vol))
        lay.addWidget(card2)

        card3 = Card(
            "Uygulama bildirimleri",
            "Hangi uygulamaların bildirim yapabileceğini seçin.",
        )
        apps = [
            ("Tarayıcı", True),
            ("E-posta", True),
            ("Sistem güncellemeleri", True),
            ("İndiriciler", False),
        ]
        for app_name, enabled in apps:
            row = QWidget()
            from PyQt6.QtCore import Qt
            from PyQt6.QtWidgets import QHBoxLayout

            rlay = QHBoxLayout(row)
            rlay.setContentsMargins(0, 0, 0, 0)
            rlay.setSpacing(12)
            lbl = QLabel(app_name)
            lbl.setStyleSheet(
                "color: #f8fafc; font-size: 13px; font-weight: 600; background: transparent;"
            )
            tgl = ToggleControl(enabled)
            tgl.toggled_value.connect(
                lambda _, n=app_name: self.set(f"app_notif_{n}", _)
            )
            rlay.addWidget(lbl, 1)
            rlay.addWidget(tgl, 0)
            row.setStyleSheet("background: transparent; border-radius: 8px;")
            card3.content_lay.addWidget(row)
        lay.addWidget(card3)

        lay.addStretch()
