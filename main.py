"""Foxai Settings — modern, kapsamlı Linux ayarlar uygulaması (YaST benzeri)."""

from __future__ import annotations

import sys

from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QColorDialog,
    QTabWidget,
)

from database import (
    account_exists,
    create_account,
    create_profile,
    delete_profile,
    get_profiles,
    init_db,
    set_default_profile,
    verify_account,
)
from pages.accounts import AccountsPage
from pages.appearance import AppearancePage
from pages.bluetooth import BluetoothPage
from pages.display import DisplayPage
from pages.keyboard import KeyboardPage
from pages.mouse import MousePage
from pages.network import NetworkPage
from pages.notifications import NotificationsPage
from pages.power import PowerPage
from pages.privacy import PrivacyPage
from pages.software import SoftwarePage
from pages.system_info import SystemInfoPage
from pages.boot import BootPage
from pages.users import UsersPage
from pages.firewall import FirewallPage
from pages.audio import AudioPage
from pages.system_services import SystemServicesPage
from theme import (
    ACCENT,
    ACCENT_HOVER,
    BG,
    BORDER,
    CARD,
    DANGER,
    SIDEBAR,
    SIDEBAR_ACTIVE,
    SIDEBAR_HOVER,
    TEXT,
    TEXT_MUTED,
    STYLESHEET,
)


class LoginPage(QWidget):
    """Giriş / kayıt ekranı."""

    login_success = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("loginPage")
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addStretch()

        center = QFrame()
        center.setObjectName("loginCard")
        center.setFixedWidth(420)
        center.setStyleSheet(
            f"""
            QFrame#loginCard {{
                background: {CARD};
                border: 1px solid {BORDER};
                border-radius: 20px;
            }}
            QLabel#loginTitle {{
                color: {TEXT}; font-size: 26px; font-weight: 800;
                background: transparent; padding-bottom: 4px;
            }}
            QLabel#loginSub {{
                color: {TEXT_MUTED}; font-size: 13px; background: transparent;
                padding-bottom: 24px;
            }}
            QLineEdit {{
                background: #334155; border: 1px solid {BORDER};
                border-radius: 10px; padding: 10px 14px; color: {TEXT};
                min-height: 42px;
            }}
            QLineEdit:focus {{ border-color: {ACCENT}; }}
            QPushButton#primary {{
                background: {ACCENT}; border: none; border-radius: 10px;
                color: #fff; font-weight: 700; padding: 10px; min-height: 42px;
            }}
            QPushButton#primary:hover {{ background: {ACCENT_HOVER}; }}
            """
        )
        cl = QVBoxLayout(center)
        cl.setContentsMargins(32, 32, 32, 32)
        cl.setSpacing(14)

        logo = QLabel("FOXAI")
        logo.setStyleSheet(
            f"color: {ACCENT}; font-size: 34px; font-weight: 900; letter-spacing: -1px; background: transparent;"
        )
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cl.addWidget(logo)

        title = QLabel("Hoş geldiniz")
        title.setObjectName("loginTitle")
        cl.addWidget(title)

        sub = QLabel("Hesabınızla giriş yapın veya yeni bir hesap oluşturun.")
        sub.setObjectName("loginSub")
        sub.setWordWrap(True)
        cl.addWidget(sub)

        tabs = QTabWidget()
        tabs.setStyleSheet(
            "QTabWidget::pane { border: none; background: transparent; } "
            "QTabBar::tab { background: transparent; color: #94a3b8; "
            "font-size: 13px; font-weight: 700; padding: 10px 16px; "
            "border-bottom: 2px solid transparent; } "
            "QTabBar::tab:selected { color: #409eff; border-bottom: 2px solid #409eff; }"
        )

        login_w = self._build_login_tab()
        reg_w = self._build_register_tab()
        tabs.addTab(login_w, "Giriş Yap")
        tabs.addTab(reg_w, "Hesap Oluştur")
        cl.addWidget(tabs)
        cl.addStretch()

        wrap = QVBoxLayout()
        wrap.addStretch()
        center_h = QHBoxLayout()
        center_h.addStretch()
        center_h.addWidget(center)
        center_h.addStretch()
        wrap.addLayout(center_h)
        wrap.addStretch()
        root.addLayout(wrap)

        self.tabs = tabs

    def _build_login_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)
        self.login_user = QLineEdit()
        self.login_user.setPlaceholderText("Kullanıcı adı veya e-posta")
        self.login_pass = QLineEdit()
        self.login_pass.setPlaceholderText("Şifre")
        self.login_pass.setEchoMode(QLineEdit.EchoMode.Password)
        btn = QPushButton("Giriş yap")
        btn.setObjectName("primary")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self._do_login)
        lay.addWidget(self.login_user)
        lay.addWidget(self.login_pass)
        lay.addWidget(btn)
        lay.addStretch()
        return w

    def _build_register_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)
        self.reg_user = QLineEdit()
        self.reg_user.setPlaceholderText("Kullanıcı adı")
        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("E-posta")
        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("Şifre")
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        btn = QPushButton("Hesap oluştur")
        btn.setObjectName("primary")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self._do_register)
        lay.addWidget(self.reg_user)
        lay.addWidget(self.reg_email)
        lay.addWidget(self.reg_pass)
        lay.addWidget(btn)
        lay.addStretch()
        return w

    def _do_login(self) -> None:
        user = self.login_user.text().strip()
        pwd = self.login_pass.text()
        if not user or not pwd:
            QMessageBox.warning(self, "Eksik bilgi", "Kullanıcı adı ve şifre giriniz.")
            return
        aid = verify_account(user, pwd)
        if aid is None:
            QMessageBox.warning(
                self, "Giriş başarısız", "Kullanıcı adı veya şifre hatalı."
            )
            return
        self.login_success.emit(aid)

    def _do_register(self) -> None:
        user = self.reg_user.text().strip()
        email = self.reg_email.text().strip()
        pwd = self.reg_pass.text()
        if not user or not email or not pwd:
            QMessageBox.warning(self, "Eksik bilgi", "Tüm alanları doldurunuz.")
            return
        if account_exists(user, email):
            QMessageBox.warning(
                self, "Mevcut", "Bu kullanıcı adı veya e-posta zaten kayıtlı."
            )
            return
        create_account(user, email, pwd)
        QMessageBox.information(
            self, "Oluşturuldu", "Hesabınız oluşturuldu. Giriş yapabilirsiniz."
        )
        self.tabs.setCurrentIndex(0)
        self.login_user.setText(user)
        self.login_pass.setText(pwd)


class NavItem(QPushButton):
    def __init__(self, text: str, icon: str = "", parent=None):
        super().__init__(icon + "  " + text, parent)
        self.setObjectName("navItem")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(44)


class ProfileItem(QPushButton):
    def __init__(
        self, pid: int, name: str, color: str, active: bool, on_click, parent=None
    ):
        super().__init__(name, parent)
        self.pid = pid
        self.setCheckable(True)
        self.setChecked(active)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(40)
        self.clicked.connect(lambda: on_click(pid))
        self._refresh(color, active)

    def _refresh(self, color: str, active: bool) -> None:
        if active:
            self.setStyleSheet(
                f"QPushButton {{ background: {SIDEBAR_ACTIVE}; color: {TEXT}; "
                f"border: none; border-radius: 10px; text-align: left; padding: 8px 14px; "
                f"font-weight: 700; border-left: 4px solid {ACCENT}; }}"
            )
        else:
            self.setStyleSheet(
                f"QPushButton {{ background: transparent; color: {TEXT_MUTED}; "
                f"border: none; border-radius: 10px; text-align: left; padding: 8px 14px; "
                f"font-size: 13px; }}"
                f"QPushButton:hover {{ background: {SIDEBAR_HOVER}; color: {TEXT}; }}"
            )


class MainWindow(QWidget):
    """Ana ayarlar penceresi — 15 modül, YaST benzeri."""

    def __init__(self, account_id: int, parent=None):
        super().__init__(parent)
        self.account_id = account_id
        self.active_profile_id = self._load_default_profile()
        self.setWindowTitle("Foxai Settings")
        self.resize(1200, 800)
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(STYLESHEET)
        self.pages: list[QWidget] = []
        self.nav_items: list[NavItem] = []
        self._build_ui()
        self._show_page(0)

    def _load_default_profile(self) -> int:
        profiles = get_profiles(self.account_id)
        for p in profiles:
            if p["is_default"]:
                return p["id"]
        return profiles[0]["id"] if profiles else -1

    def _build_ui(self) -> None:
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ---------- Kenar çubuğu ----------
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sl = QVBoxLayout(sidebar)
        sl.setContentsMargins(0, 0, 0, 0)
        sl.setSpacing(0)

        title = QLabel("FOXAI")
        title.setObjectName("appTitle")
        title.setStyleSheet(
            f"color: {ACCENT}; font-size: 22px; font-weight: 900; letter-spacing: -0.5px; "
            f"background: transparent; padding: 26px 20px 12px 20px;"
        )
        sub = QLabel("Ayarlar Merkezi · Fedora")
        sub.setObjectName("appSubtitle")
        sl.addWidget(title)
        sl.addWidget(sub)

        # Tüm modüller (YaST benzeri)
        nav_defs = [
            ("Hesap & Profiller", "👤", 0),
            ("Görünüm", "🎨", 1),
            ("Ekran", "🖥️", 2),
            ("Bildirimler", "🔔", 3),
            ("Gizlilik & Güvenlik", "🔒", 4),
            ("Klavye", "⌨️", 5),
            ("Fare & Touchpad", "🖱️", 6),
            ("Güç & Pil", "🔋", 7),
            ("Ağ & İnternet", "🌐", 8),
            ("Bluetooth", "📶", 9),
            ("Ses & Ayagıt", "🔊", 10),
            ("Yazılım & Güncelleme", "📦", 11),
            ("Donanım & Bilgi", "ℹ️", 12),
            ("Önyükleyici (GRUB)", "⚙️", 13),
            ("Kullanıcılar & Gruplar", "👥", 14),
            ("Güvenlik Duvarı", "🛡️", 15),
            ("Sistem Servisleri", "⚙️", 16),
        ]
        for text, icon, idx in nav_defs:
            btn = NavItem(text, icon)
            btn.clicked.connect(lambda _, i=idx: self._show_page(i))
            sl.addWidget(btn)
            self.nav_items.append(btn)

        sl.addStretch()

        sl.addWidget(self._section_label("Profillerim"))
        self.profile_box = QVBoxLayout()
        self.profile_box.setContentsMargins(12, 0, 12, 0)
        self.profile_box.setSpacing(6)
        sl.addLayout(self.profile_box)

        btn_new_prof = QPushButton("+ Yeni profil")
        btn_new_prof.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_new_prof.setStyleSheet(
            f"QPushButton {{ background: transparent; border: 1px dashed {BORDER}; "
            f"color: {TEXT_MUTED}; border-radius: 10px; padding: 8px 14px; font-size: 12px; }}"
            f"QPushButton:hover {{ background: {SIDEBAR_HOVER}; color: {TEXT}; border-color: #64748b; }}"
        )
        btn_new_prof.clicked.connect(self._add_profile)
        sl.addWidget(btn_new_prof)
        sl.addSpacing(12)

        btn_logout = QPushButton("Çıkış yap")
        btn_logout.setObjectName("danger")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self._logout)
        sl.addWidget(btn_logout)
        sl.addSpacing(16)

        root.addWidget(sidebar)

        # ---------- Ana içerik ----------
        content = QFrame()
        content.setObjectName("contentFrame")
        cl = QVBoxLayout(content)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        top = QFrame()
        top.setFixedHeight(70)
        top.setStyleSheet("background: transparent;")
        tl = QHBoxLayout(top)
        tl.setContentsMargins(30, 12, 30, 12)
        tl.setSpacing(14)
        self.avatar = QLabel("●")
        self.avatar.setFixedSize(32, 32)
        self.avatar.setStyleSheet(
            f"color: {ACCENT}; font-size: 20px; background: transparent;"
        )
        self.lbl_profile_name = QLabel("Profil")
        self.lbl_profile_name.setStyleSheet(
            f"color: {TEXT}; font-size: 16px; font-weight: 700; background: transparent;"
        )
        self.lbl_profile_email = QLabel("Hesap · Fedora")
        self.lbl_profile_email.setStyleSheet(
            f"color: {TEXT_MUTED}; font-size: 12px; background: transparent;"
        )
        info = QVBoxLayout()
        info.setContentsMargins(0, 0, 0, 0)
        info.setSpacing(2)
        info.addWidget(self.lbl_profile_name)
        info.addWidget(self.lbl_profile_email)
        tl.addWidget(self.avatar)
        tl.addLayout(info, 1)
        tl.addStretch()
        cl.addWidget(top)

        self.page_title = QLabel("Hesap & Profiller")
        self.page_title.setObjectName("pageTitle")
        self.page_title.setStyleSheet(
            f"color: {TEXT}; font-size: 26px; font-weight: 800; background: transparent;"
        )
        self.page_desc = QLabel("Hesabınızı ve profillerinizi yönetin.")
        self.page_desc.setObjectName("pageDesc")
        self.page_desc.setStyleSheet(
            f"color: {TEXT_MUTED}; font-size: 14px; background: transparent;"
        )
        header = QVBoxLayout()
        header.setContentsMargins(30, 18, 30, 0)
        header.setSpacing(4)
        header.addWidget(self.page_title)
        header.addWidget(self.page_desc)
        cl.addLayout(header)

        self.stack = QStackedWidget()
        cl.addWidget(self.stack, 1)

        root.addWidget(content, 1)

        self._refresh_profiles()
        self._update_top_bar()

    def _section_label(self, text: str) -> QWidget:
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(16, 10, 16, 4)
        lbl = QLabel(text)
        lbl.setStyleSheet(
            f"color: {TEXT_MUTED}; font-size: 11px; font-weight: 800; "
            f"text-transform: uppercase; letter-spacing: 1px; background: transparent;"
        )
        l.addWidget(lbl)
        return w

    def _refresh_profiles(self) -> None:
        while self.profile_box.count():
            item = self.profile_box.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        profiles = get_profiles(self.account_id)
        for p in profiles:
            item = ProfileItem(
                p["id"],
                p["name"],
                p["avatar_color"],
                p["id"] == self.active_profile_id,
                on_click=self._switch_profile,
            )
            self.profile_box.addWidget(item)

        self.profile_box.addStretch()

    def _update_top_bar(self) -> None:
        profiles = get_profiles(self.account_id)
        active = None
        for p in profiles:
            if p["id"] == self.active_profile_id:
                active = p
                break
        if active:
            self.avatar.setStyleSheet(
                f"color: {active['avatar_color']}; font-size: 20px; background: transparent;"
            )
            self.lbl_profile_name.setText(active["name"])
            self.lbl_profile_email.setText(
                f"Hesap #{self.account_id} · Profil #{active['id']}"
            )
        else:
            self.lbl_profile_name.setText("Profil yok")

    def _switch_profile(self, pid: int) -> None:
        self.active_profile_id = pid
        set_default_profile(pid)
        self._refresh_profiles()
        self._update_top_bar()
        self._reload_pages()

    def _add_profile(self) -> None:
        name, ok = QInputDialog.getText(self, "Yeni profil", "Profil adı:")
        if not ok or not name.strip():
            return
        color = QColorDialog.getColor(QColor(ACCENT), self, "Avatar rengi")
        if not color.isValid():
            return
        pid = create_profile(self.account_id, name.strip(), color.name())
        self.active_profile_id = pid
        set_default_profile(pid)
        self._refresh_profiles()
        self._update_top_bar()
        self._reload_pages()

    def _reload_pages(self) -> None:
        while self.stack.count():
            w = self.stack.widget(0)
            self.stack.removeWidget(w)
            w.deleteLater()
        self.pages = []
        self._show_page(0)

    def _show_page(self, index: int) -> None:
        for i, btn in enumerate(self.nav_items):
            btn.setChecked(i == index)

        while self.stack.count() <= index:
            self._create_page(self.stack.count())

        self.stack.setCurrentIndex(index)
        page = self.stack.widget(index)
        if hasattr(page, "refresh_profiles"):
            page.refresh_profiles()

        titles = [
            "Hesap & Profiller",
            "Görünüm",
            "Ekran",
            "Bildirimler",
            "Gizlilik & Güvenlik",
            "Klavye",
            "Fare & Touchpad",
            "Güç & Pil",
            "Ağ & İnternet",
            "Bluetooth",
            "Ses & Ayagıt",
            "Yazılım & Güncelleme",
            "Donanım & Sistem Bilgisi",
            "Önyükleyici (GRUB)",
            "Kullanıcılar & Gruplar",
            "Güvenlik Duvarı",
            "Sistem Servisleri",
        ]
        descs = [
            "Hesabınızı ve profillerinizi yönetin.",
            "Tema, renk ve yazı tipi ayarlarını özelleştirin.",
            "Ekran çözünürlüğü, yenileme hızı ve parlaklık.",
            "Sistem ve uygulama bildirimlerini yapılandırın.",
            "Konum, kamera, mikrofon ve telemetri ayarları.",
            "Klavye dili, tuş tekrarı ve erişilebilirlik.",
            "Fare hassasiyeti, kaydırma ve davranış ayarları.",
            "Güç modu, uyku süresi ve ekran kilidi.",
            "Wi-Fi, Ethernet, VPN ve proxy bağlantıları.",
            "Bluetooth cihazlarını yönetin ve eşleştirin.",
            "Çıkış aygıtı, ses seviyeleri ve sistem sesleri.",
            "Yazılım depoları, paket güncellemeleri ve kurulumlar.",
            "İşlemci, bellek, disk, GPU ve sistem sürüm bilgileri.",
            "GRUB önyükleyici, çekirdek parametreleri ve önyükleme sırası.",
            "Sistem kullanıcı hesapları, gruplar ve yetkiler.",
            "Güvenlik duvarı kuralları, portlar ve erişim politikaları.",
            "Arka plan servislerini etkinleştirin veya devre dışı bırakın.",
        ]
        self.page_title.setText(titles[index])
        self.page_desc.setText(descs[index])

    def _create_page(self, index: int) -> None:
        pid = self.active_profile_id if self.active_profile_id != -1 else 0
        if index == 0:
            page = AccountsPage(pid, self.account_id, self._switch_profile)
        elif index == 1:
            page = AppearancePage(pid)
        elif index == 2:
            page = DisplayPage(pid)
        elif index == 3:
            page = NotificationsPage(pid)
        elif index == 4:
            page = PrivacyPage(pid)
        elif index == 5:
            page = KeyboardPage(pid)
        elif index == 6:
            page = MousePage(pid)
        elif index == 7:
            page = PowerPage(pid)
        elif index == 8:
            page = NetworkPage(pid)
        elif index == 9:
            page = BluetoothPage(pid)
        elif index == 10:
            page = AudioPage(pid)
        elif index == 11:
            page = SoftwarePage(pid)
        elif index == 12:
            page = SystemInfoPage(pid)
        elif index == 13:
            page = BootPage(pid)
        elif index == 14:
            page = UsersPage(pid)
        elif index == 15:
            page = FirewallPage(pid)
        elif index == 16:
            page = SystemServicesPage(pid)
        else:
            page = QWidget()
        self.pages.append(page)
        self.stack.addWidget(page)

    def _logout(self) -> None:
        self.account_id = -1
        self.active_profile_id = -1
        self.logout_requested.emit()

    logout_requested = pyqtSignal()


class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setStyle("Fusion")
        init_db()
        self.login = LoginPage()
        self.login.login_success.connect(self._open_main)
        self.login.show()
        self.main = None

    def _open_main(self, account_id: int) -> None:
        self.main = MainWindow(account_id)
        self.main.logout_requested.connect(self._back_to_login)
        self.main.show()
        self.login.hide()

    def _back_to_login(self) -> None:
        if self.main:
            self.main.hide()
            self.main.deleteLater()
            self.main = None
        self.login = LoginPage()
        self.login.login_success.connect(self._open_main)
        self.login.show()


def main() -> None:
    app = App(sys.argv)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
