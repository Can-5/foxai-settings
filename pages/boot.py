"""Önyükleyici (GRUB) & Çekirdek ayarları sayfası."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from pages.base_page import BasePage
from theme import ACCENT, ACCENT_HOVER
from widgets import Card, SectionLabel, SelectControl, SettingRow, ToggleControl


class BootPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        lay.addWidget(SectionLabel("Önyükleyici"))
        card = Card("GRUB önyükleyici", "Sistem başlangıç ayarlarını yapılandırın.")
        os_sel = SelectControl(
            [("CachyOS", "cachyos"), ("Windows", "windows"), ("Diğer", "other")],
            self.get("boot_default_os", "cachyos"),
        )
        os_sel.changed.connect(lambda v: self.set("boot_default_os", v))
        card.add_widget(
            SettingRow(
                "Varsayılan işletim sistemi",
                "Önyükleme menüsünde öncelikli gösterilen sistem.",
                os_sel,
            )
        )
        timeout = SelectControl(
            [("3 saniye", 3), ("5 saniye", 5), ("10 saniye", 10), ("30 saniye", 30)],
            self.get("boot_timeout", 5),
        )
        timeout.changed.connect(lambda v: self.set("boot_timeout", v))
        card.add_widget(
            SettingRow(
                "Menü bekleme süresi",
                "Otomatik önyükleme öncesi bekleme süresi.",
                timeout,
            )
        )
        hidden = ToggleControl(self.get("boot_hidden_menu", False))
        hidden.toggled_value.connect(lambda v: self.set("boot_hidden_menu", v))
        card.add_widget(
            SettingRow("Gizli menü", "Menüyü gizle, kısayol tuşu ile göster.", hidden)
        )
        lay.addWidget(card)

        card2 = Card(
            "Çekirdek parametreleri",
            "Önyükleme sırasında çekirdeğe geçirilecek seçenekler.",
        )
        current = self.get("boot_kernel_params", "quiet splash")
        param_edit = QLabel(current)
        param_edit.setStyleSheet(
            "color: #f8fafc; font-size: 13px; font-family: monospace; background: #334155; "
            "padding: 8px 12px; border-radius: 8px; border: 1px solid #475569;"
        )
        card2.content_lay.addWidget(
            SettingRow(
                "Çekirdek seçenekleri", "Örnek: quiet splash nomodeset", param_edit
            )
        )
        btn_apply = QPushButton("Değişiklikleri uygula")
        btn_apply.setObjectName("primary")
        btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_apply.clicked.connect(
            lambda: self._notify(
                "Önyükleyici",
                "GRUB yapılandırması güncellendi. Yeniden başlatma gerekli.",
            )
        )
        card2.content_lay.addWidget(btn_apply)
        lay.addWidget(card2)

        lay.addStretch()

    def _notify(self, title: str, msg: str) -> None:
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.information(self, title, msg)
