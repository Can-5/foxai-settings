"""Güvenlik Duvarı ayarları sayfası."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pages.base_page import BasePage
from theme import ACCENT
from widgets import Card, SectionLabel, SettingRow, SelectControl, ToggleControl


class FirewallPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        lay.addWidget(SectionLabel("Güvenlik Duvarı"))
        card = Card("Durum", "Gelen ve giden ağ trafiğini filtreleyin.")
        fw = ToggleControl(self.get("firewall_enabled", False))
        fw.toggled_value.connect(lambda v: self.set("firewall_enabled", v))
        card.add_widget(
            SettingRow("Güvenlik duvarı etkin", "Tüm portları filtrele ve kısıtla.", fw)
        )
        mode = SelectControl(
            [
                ("Güvenli (tümünü engelle)", "strict"),
                ("Dengeli (sadece gerekli)", "balanced"),
                ("Kapalı", "off"),
            ],
            self.get("firewall_mode", "balanced"),
        )
        mode.changed.connect(lambda v: self.set("firewall_mode", v))
        card.add_widget(SettingRow("İşlem modu", "Varsayılan erişim politikası.", mode))
        lay.addWidget(card)

        # Port kuralı ekle
        lay.addWidget(SectionLabel("Port Kuralı Ekle"))
        card2 = Card("Yeni kural", "Gelen trafiğe özel bir port kuralı ekleyin.")
        port_in = QLineEdit()
        port_in.setPlaceholderText("Port (örn. 80, 443, 22)")
        proto = SelectControl(
            [("TCP", "tcp"), ("UDP", "udp"), ("TCP+UDP", "both")],
            "tcp",
        )
        action = SelectControl(
            [("İzin ver", "allow"), ("Engelle", "deny")],
            "allow",
        )
        btn_add = QPushButton("Kuralı ekle")
        btn_add.setObjectName("primary")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(
            lambda: self._notify(
                "Kural",
                f"Port {port_in.text()} ({proto.value()}) → {action.value()} eklendi.",
            )
        )
        rlay = QHBoxLayout()
        rlay.setSpacing(10)
        rlay.addWidget(port_in, 0)
        rlay.addWidget(QLabel("/"), 0)
        rlay.addWidget(proto, 0)
        rlay.addWidget(action, 0)
        rlay.addWidget(btn_add, 0)
        rlay.addStretch()
        card2.content_lay.addLayout(rlay)
        lay.addWidget(card2)

        # Mevcut kurallar
        lay.addWidget(SectionLabel("Etkin Kurallar"))
        card3 = Card("Kural listesi", "Şu anda etkin güvenlik duvarı kuralları.")
        rules = [
            ("22/tcp", "SSH", "İzin ver"),
            ("80/tcp", "HTTP", "İzin ver"),
            ("443/tcp", "HTTPS", "İzin ver"),
        ]
        for rule, name, action_txt in rules:
            row = QWidget()
            rlay2 = QHBoxLayout(row)
            rlay2.setContentsMargins(0, 0, 0, 0)
            rlay2.setSpacing(12)
            rlbl = QLabel(rule)
            rlbl.setStyleSheet(
                "color: #f8fafc; font-size: 12px; font-family: monospace; background: transparent;"
            )
            nlbl = QLabel(name)
            nlbl.setStyleSheet(
                "color: #94a3b8; font-size: 12px; background: transparent;"
            )
            albl = QLabel(action_txt)
            albl.setStyleSheet(
                f"color: {'#22c55e' if action_txt == 'İzin ver' else '#ef4444'}; "
                f"font-size: 11px; font-weight: 700; background: transparent;"
            )
            btn_del = QPushButton("Sil")
            btn_del.setObjectName("danger")
            btn_del.setFixedSize(60, 28)
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            rlay2.addWidget(rlbl, 1)
            rlay2.addWidget(nlbl, 0)
            rlay2.addWidget(albl, 0)
            rlay2.addWidget(btn_del, 0)
            row.setStyleSheet("background: transparent; border-radius: 8px;")
            card3.content_lay.addWidget(row)
        lay.addWidget(card3)

        lay.addStretch()

    def _notify(self, title: str, msg: str) -> None:
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.information(self, title, msg)
