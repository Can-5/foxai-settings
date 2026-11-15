"""Kullanıcılar & Gruplar sayfası (sistem seviyesinde hesap yönetimi)."""

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
from widgets import Card, SectionLabel, SettingRow, TextControl, ToggleControl


class UsersPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        lay.addWidget(SectionLabel("Kullanıcı Hesapları"))
        card = Card(
            "Sistem kullanıcıları", "Bilgisayara giriş yapabilen hesapları yönetin."
        )
        users = [
            ("ilkaycan", "Yönetici", True, "#409eff"),
            ("misafir", "Kullanıcı", False, "#94a3b8"),
        ]
        for username, role, active, color in users:
            row = QWidget()
            rlay = QHBoxLayout(row)
            rlay.setContentsMargins(0, 0, 0, 0)
            rlay.setSpacing(12)
            dot = QLabel("●")
            dot.setFixedWidth(14)
            dot.setStyleSheet(
                f"color: {color}; font-size: 14px; background: transparent;"
            )
            info = QWidget()
            ilay = QVBoxLayout(info)
            ilay.setContentsMargins(0, 0, 0, 0)
            ilay.setSpacing(2)
            un = QLabel(username)
            un.setStyleSheet(
                "color: #f8fafc; font-size: 13px; font-weight: 700; background: transparent;"
            )
            rl = QLabel(role)
            rl.setStyleSheet(
                "color: #94a3b8; font-size: 11px; background: transparent;"
            )
            ilay.addWidget(un)
            ilay.addWidget(rl)
            status = QLabel("Etkin" if active else "Devre dışı")
            status.setStyleSheet(
                f"color: {'#22c55e' if active else '#ef4444'}; font-size: 11px; font-weight: 700; background: transparent;"
            )
            rlay.addWidget(dot, 0)
            rlay.addWidget(info, 1)
            rlay.addWidget(status, 0)
            row.setStyleSheet("background: transparent; border-radius: 8px;")
            card.content_lay.addWidget(row)

        btn_add_user = QPushButton("Yeni kullanıcı ekle")
        btn_add_user.setObjectName("primary")
        btn_add_user.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_user.clicked.connect(self._add_user)
        card.content_lay.addWidget(btn_add_user)
        lay.addWidget(card)

        # Şifre & yetki
        lay.addWidget(SectionLabel("Şifre & Yetkilendirme"))
        card2 = Card("Hesap güvenliği", "Şifre değiştirme ve sudo yetkisi ayarları.")
        btn_change = QPushButton("Şifreyi değiştir")
        btn_change.setObjectName("ghost")
        btn_change.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_change.clicked.connect(
            lambda: self._notify("Şifre", "Şifre değişikliği işlemi başlatıldı.")
        )
        card2.content_lay.addWidget(btn_change)
        sudo = ToggleControl(self.get("user_sudo", True))
        sudo.toggled_value.connect(lambda v: self.set("user_sudo", v))
        card2.add_widget(
            SettingRow("Sudo yetkisi", "Kullanıcıya yönetici yetkisi ver.", sudo)
        )
        lay.addWidget(card2)

        lay.addStretch()

    def _add_user(self) -> None:
        name, ok = QInputDialog.getText(self, "Yeni kullanıcı", "Kullanıcı adı:")
        if not ok or not name.strip():
            return
        pwd, ok2 = QInputDialog.getText(
            self, "Şifre", f"'{name.strip()}' için şifre:", QLineEdit.EchoMode.Password
        )
        if not ok2 or not pwd:
            return
        QMessageBox.information(
            self, "Oluşturuldu", f"Kullanıcı '{name.strip()}' oluşturuldu."
        )
