"""Hesap ve profil yönetimi sayfası."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from database import (
    create_account,
    create_profile,
    delete_profile,
    get_profiles,
    verify_account,
)
from pages.base_page import BasePage
from theme import ACCENT, DANGER
from widgets import ActionRow, Card, SectionLabel, SettingRow, ToggleControl


class AccountsPage(BasePage):
    def __init__(
        self, profile_id: int, account_id: int, on_profile_changed, parent=None
    ):
        super().__init__(profile_id, parent)
        self.account_id = account_id
        self.on_profile_changed = on_profile_changed
        self._build_ui()
        self.refresh_profiles()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        # Kart: Aktif profil
        self.card_active = Card("Etkin Profil", "Şu anda oturum açmış olan profiliniz.")
        self.lbl_active_name = QLabel()
        self.lbl_active_name.setStyleSheet(
            "color: #f8fafc; font-size: 16px; font-weight: 700; background: transparent;"
        )
        self.lbl_active_email = QLabel()
        self.lbl_active_email.setStyleSheet(
            "color: #94a3b8; font-size: 13px; background: transparent;"
        )
        btn_switch = QPushButton("Profili değiştir")
        btn_switch.setObjectName("ghost")
        btn_switch.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_switch.clicked.connect(self._switch_profile_dialog)
        h = QHBoxLayout()
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(12)
        info = QWidget()
        hl = QVBoxLayout(info)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(2)
        hl.addWidget(self.lbl_active_name)
        hl.addWidget(self.lbl_active_email)
        h.addWidget(info, 1)
        h.addWidget(btn_switch, 0)
        self.card_active.content_lay.addLayout(h)
        lay.addWidget(self.card_active)

        # Kart: Profillerim
        lay.addWidget(SectionLabel("Profillerim"))
        self.card_profiles = Card()
        lay.addWidget(self.card_profiles)

        # Kart: Yeni profil ekle
        lay.addWidget(SectionLabel("Yeni Profil Oluştur"))
        self.card_new = Card()
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Profil adı (örn. İş, Oyun, Kişisel)")
        self.input_color = QLineEdit("#409eff")
        self.input_color.setPlaceholderText("Avatar rengi (hex)")
        btn_add = QPushButton("Profili Ekle")
        btn_add.setObjectName("primary")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self._add_profile)
        nlay = QVBoxLayout()
        nlay.setSpacing(10)
        r1 = QHBoxLayout()
        r1.setSpacing(10)
        r1.addWidget(self.input_name, 1)
        r1.addWidget(self.input_color)
        nlay.addLayout(r1)
        nlay.addWidget(btn_add)
        self.card_new.content_lay.addLayout(nlay)
        lay.addWidget(self.card_new)

        lay.addStretch()

    def refresh_profiles(self) -> None:
        # Etkin profili göster
        profiles = get_profiles(self.account_id)
        active = None
        for p in profiles:
            if p["is_default"]:
                active = p
                break
        if active:
            self.lbl_active_name.setText(active["name"])
            self.lbl_active_email.setText(
                f"Hesap #{self.account_id} · Profil #{active['id']}"
            )
        else:
            self.lbl_active_name.setText("Profil yok")
            self.lbl_active_email.setText("Lütfen bir profil oluşturun.")

        # Profiller listesi
        self.card_profiles.content_lay.takeAt(
            0
        ) if self.card_profiles.content_lay.count() else None
        # eski widget'ları temizle
        while self.card_profiles.content_lay.count():
            item = self.card_profiles.content_lay.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        for p in profiles:
            row = QWidget()
            rlay = QHBoxLayout(row)
            rlay.setContentsMargins(0, 0, 0, 0)
            rlay.setSpacing(12)
            dot = QLabel("●")
            dot.setFixedWidth(14)
            dot.setStyleSheet(
                f"color: {p['avatar_color']}; font-size: 16px; background: transparent;"
            )
            name = QLabel(p["name"])
            name.setStyleSheet(
                "color: #f8fafc; font-size: 14px; font-weight: 600; background: transparent;"
            )
            if p["is_default"]:
                name.setText(name.text() + "  (etkin)")
                name.setStyleSheet(
                    "color: #409eff; font-size: 14px; font-weight: 700; background: transparent;"
                )
            btn_del = QPushButton("Sil")
            btn_del.setObjectName("danger")
            btn_del.setFixedSize(70, 32)
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.clicked.connect(lambda _, pid=p["id"]: self._delete_profile(pid))
            rlay.addWidget(dot)
            rlay.addWidget(name, 1)
            rlay.addWidget(btn_del, 0)
            row.setStyleSheet("background: transparent; border-radius: 8px;")
            row.setCursor(Qt.CursorShape.PointingHandCursor)
            row.mousePressEvent = lambda _, pid=p["id"]: self._set_default(pid)
            self.card_profiles.content_lay.addWidget(row)

    def _set_default(self, profile_id: int) -> None:
        from database import set_default_profile

        set_default_profile(profile_id)
        self.on_profile_changed(profile_id)
        self.refresh_profiles()

    def _switch_profile_dialog(self) -> None:
        profiles = get_profiles(self.account_id)
        if not profiles:
            QMessageBox.information(self, "Profiller", "Henüz profil oluşturulmamış.")
            return
        names = "\n".join(
            f"• {p['name']}" + (" (etkin)" if p["is_default"] else "") for p in profiles
        )
        QMessageBox.information(self, "Profillerim", names)

    def _add_profile(self) -> None:
        name = self.input_name.text().strip()
        color = self.input_color.text().strip() or "#409eff"
        if not name:
            QMessageBox.warning(self, "Eksik bilgi", "Lütfen profil adı giriniz.")
            return
        pid = create_profile(self.account_id, name, color)
        self.input_name.clear()
        self.on_profile_changed(pid)
        self.refresh_profiles()

    def _delete_profile(self, profile_id: int) -> None:
        profiles = get_profiles(self.account_id)
        if len(profiles) <= 1:
            QMessageBox.warning(self, "Silinemez", "En az bir profil kalmalıdır.")
            return
        reply = QMessageBox.question(
            self,
            "Profili sil",
            "Bu profili silmek istediğinizden emin misiniz? Bu işlem geri alınamaz.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            delete_profile(profile_id)
            self.refresh_profiles()
