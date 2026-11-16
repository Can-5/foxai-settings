"""Ağ ayarları sayfası."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from pages.base_page import BasePage
from theme import ACCENT, TEXT, TEXT_MUTED
from widgets import Card, SectionLabel, SettingRow, TextControl, ToggleControl


class NetworkPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = self.lay

        lay.addWidget(SectionLabel("Ağ ve internet"))
        card = Card("Kablosuz ağ (Wi-Fi)", "Kablosuz ağları yönetin.")
        wifi = ToggleControl(self.get("wifi_enabled", True))
        wifi.toggled_value.connect(lambda v: self.set("wifi_enabled", v))
        card.add_widget(
            SettingRow("Wi-Fi etkin", "Kablosuz ağları ara ve bağlan.", wifi)
        )
        ssid = QLabel("Bağlı ağ: Foxai-Home")
        ssid.setStyleSheet(
            f"color: {TEXT}; font-size: 13px; font-weight: 600; background: transparent;"
        )
        card.content_lay.addWidget(ssid)
        btn_scan = QPushButton("Ağları tara")
        btn_scan.setObjectName("ghost")
        btn_scan.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_scan.clicked.connect(
            lambda: self._notify("Wi-Fi tarama", "Foxai-Home · Güçlü")
        )
        card.content_lay.addWidget(btn_scan)
        lay.addWidget(card)

        card2 = Card("Kablolu ağ (Ethernet)", "Kablolu bağlantı ayarları.")
        eth = ToggleControl(self.get("ethernet_enabled", True))
        eth.toggled_value.connect(lambda v: self.set("ethernet_enabled", v))
        card2.add_widget(
            SettingRow("Ethernet etkin", "Kablolu ağ bağlantısını kullan.", eth)
        )
        dhcp = ToggleControl(self.get("dhcp_enabled", True))
        dhcp.toggled_value.connect(lambda v: self.set("dhcp_enabled", v))
        card2.add_widget(
            SettingRow("Otomatik IP (DHCP)", "IP adresini otomatik al.", dhcp)
        )
        card2.add_widget(
            SettingRow(
                "IP adresi", "192.168.1.45", TextControl("192.168.1.45", "IP adresi")
            )
        )
        lay.addWidget(card2)

        card3 = Card("VPN ve proxy", "Gizli ve yönlendirilmiş bağlantı.")
        vpn = ToggleControl(self.get("vpn_enabled", False))
        vpn.toggled_value.connect(lambda v: self.set("vpn_enabled", v))
        card3.add_widget(
            SettingRow("VPN etkin", "Trafiği şifreli tünelle geçirin.", vpn)
        )
        proxy = QLabel("Proxy yapılandırılmadı")
        proxy.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 13px; background: transparent;")
        card3.content_lay.addWidget(proxy)
        lay.addWidget(card3)

        lay.addStretch()

    def _notify(self, title: str, msg: str) -> None:
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.information(self, title, msg)
