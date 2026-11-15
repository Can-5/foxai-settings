"""Panel — YaST tarzı ana yönetim ekranı: canlı sistem özeti + hızlı eylemler."""

from __future__ import annotations

import shutil
import time

from PyQt6.QtCore import QProcess, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pages._root import run_pkexec, run_ro, output_tail
from pages.base_page import BasePage
from pages.system_info import _cpu_model, _os_release
from theme import ACCENT, TEXT, TEXT_MUTED
from widgets import Card, ScrollPage, SectionLabel


def _read_uptime() -> str:
    try:
        with open("/proc/uptime", encoding="utf-8") as f:
            secs = float(f.read().split()[0])
    except (OSError, ValueError):
        return "bilinmiyor"
    days, rem = divmod(int(secs), 86400)
    hours, rem = divmod(rem, 3600)
    minutes = rem // 60
    if days:
        return f"{days}g {hours}s"
    return f"{hours}s {minutes}d"


def _ram_usage() -> str:
    mem: dict[str, int] = {}
    try:
        with open("/proc/meminfo", encoding="utf-8") as f:
            for line in f:
                parts = line.replace(":", " ").split()
                if len(parts) >= 2 and parts[1].isdigit():
                    mem[parts[0]] = int(parts[1])
    except OSError:
        return "bilinmiyor"
    total = mem.get("MemTotal", 0)
    avail = mem.get("MemAvailable", 0)
    if not total:
        return "bilinmiyor"
    used = total - avail
    return f"{used / 1e6:.1f} / {total / 1e6:.1f} GB"


def _disk_usage() -> str:
    try:
        du = shutil.disk_usage("/")
    except OSError:
        return "bilinmiyor"
    return f"{du.used / 1e9:.0f} / {du.total / 1e9:.0f} GB"


def _stat_tile(title: str, value: str, detail: str = "") -> Card:
    tile = Card()
    tile.layout().setSpacing(2)
    t = QLabel(title)
    t.setStyleSheet(
        f"color: {TEXT_MUTED}; font-size: 11px; font-weight: 700; "
        "text-transform: uppercase; letter-spacing: 1px; background: transparent;"
    )
    v = QLabel(value)
    v.setWordWrap(True)
    v.setStyleSheet(
        f"color: {TEXT}; font-size: 15px; font-weight: 800; background: transparent;"
    )
    tile.add_widget(t)
    tile.add_widget(v)
    if detail:
        d = QLabel(detail)
        d.setWordWrap(True)
        d.setStyleSheet(
            f"color: {TEXT_MUTED}; font-size: 11px; background: transparent;"
        )
        tile.add_widget(d)
    return tile


class PanelPage(BasePage):
    """Tek ekranda Fedora sistem durumu + yönetimsel hızlı eylemler."""

    navigate = pyqtSignal(str)

    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._dnf_proc: QProcess | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        page = ScrollPage()
        root = QVBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)

        rel = _os_release()
        root.addWidget(SectionLabel("Sistem Paneli"))

        # ---------- Canlı istatistikler ----------
        stats = QHBoxLayout()
        stats.setSpacing(12)
        stats.addWidget(_stat_tile("Dağıtım", rel.get("PRETTY_NAME", "Fedora")))
        stats.addWidget(_stat_tile("İşlemci", _cpu_model()))
        stats.addWidget(_stat_tile("Bellek", _ram_usage()))
        stats.addWidget(_stat_tile("Disk (/)", _disk_usage()))
        stats.addWidget(_stat_tile("Çalışma süresi", _read_uptime()))
        root.addLayout(stats)

        # ---------- Güncellemeler (gerçek dnf) ----------
        upd = Card(
            "Güncellemeler",
            "dnf üzerinden gerçek paket durumunu sorgular (salt-okunur); "
            "kurulum ve yükseltme polkit ile sizin onayınızı ister.",
        )
        self.upd_status = QLabel("Henüz denetlenmedi.")
        self.upd_status.setWordWrap(True)
        self.upd_status.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.upd_status.setStyleSheet(
            "color: #e2e8f0; font-size: 12px; font-family: monospace; "
            "background: #1e293b; padding: 10px 12px; border-radius: 8px; border: 1px solid #334155;"
        )
        upd.add_widget(self.upd_status)
        btns = QHBoxLayout()
        btns.setSpacing(10)
        b_check = QPushButton("Güncellemeleri denetle")
        b_check.setObjectName("primary")
        b_check.setCursor(Qt.CursorShape.PointingHandCursor)
        b_check.clicked.connect(self._check_updates)
        b_sec = QPushButton("Güvenlik güncellemeleri")
        b_sec.setObjectName("ghost")
        b_sec.setCursor(Qt.CursorShape.PointingHandCursor)
        b_sec.clicked.connect(self._security_updates)
        b_upg = QPushButton("Sistemi güncelle…")
        b_upg.setObjectName("ghost")
        b_upg.setCursor(Qt.CursorShape.PointingHandCursor)
        b_upg.clicked.connect(self._upgrade)
        btns.addWidget(b_check)
        btns.addWidget(b_sec)
        btns.addWidget(b_upg)
        btns.addStretch(1)
        upd.content_lay.addLayout(btns)
        root.addWidget(upd)

        # ---------- Güvenlik durumu ----------
        sec = Card("Güvenlik durumu", "Salt-okunur; hiçbir ayar değiştirmez.")
        fw = run_ro(["systemctl", "is-active", "firewalld"], timeout=10)[1].strip() or "bilinmiyor"
        rc, se, _ = run_ro(["getenforce"], timeout=10)
        selinux = se.strip() if rc == 0 else "kurulu değil"
        kern = run_ro(["uname", "-r"], timeout=10)[1].strip() or "bilinmiyor"
        sec.add_widget(self._kv("firewalld", fw))
        sec.add_widget(self._kv("SELinux", selinux))
        sec.add_widget(self._kv("Çekirdek", kern))
        failed = run_ro(
            ["systemctl", "list-units", "--state=failed", "--no-legend", "--plain"],
            timeout=10,
        )[1].strip()
        sec.add_widget(self._kv("Hatalı servis", failed if failed else "yok"))
        root.addWidget(sec)

        # ---------- Hızlı eylemler ----------
        quick = Card("Hızlı eylemler", "İlgili modüle atlar.")
        grid = QGridLayout()
        grid.setSpacing(10)
        actions = [
            ("AI Asistan", "ai"),
            ("Yazılım & Güncelleme", "software"),
            ("Önyükleyici (GRUB2)", "boot"),
            ("Sistem Servisleri", "services"),
            ("Güvenlik Duvarı", "firewall"),
            ("Kullanıcılar & Gruplar", "users"),
        ]
        for i, (label, key) in enumerate(actions):
            btn = QPushButton(label)
            btn.setObjectName("ghost")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, k=key: self.navigate.emit(k))
            grid.addWidget(btn, i // 3, i % 3)
        quick.content_lay.addLayout(grid)
        root.addWidget(quick)

        page.lay.addLayout(root)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(page)

    # ---------- yardımcı satır ----------
    def _kv(self, key: str, value: str) -> QWidget:
        row = QWidget()
        h = QHBoxLayout(row)
        h.setContentsMargins(0, 0, 0, 0)
        k = QLabel(key)
        k.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px; background: transparent;")
        v = QLabel(value)
        v.setWordWrap(True)
        v.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        v.setStyleSheet(f"color: {TEXT}; font-size: 12px; font-weight: 700; background: transparent;")
        h.addWidget(k, 0)
        h.addStretch(1)
        h.addWidget(v, 0)
        return row

    # ---------- dnf eylemleri ----------
    def _check_updates(self) -> None:
        if self._dnf_proc is not None:
            return
        self.upd_status.setText("Denetleniyor: dnf check-update…")
        proc = QProcess(self)
        self._dnf_proc = proc
        proc.finished.connect(self._on_check_finished)
        proc.start("dnf", ["check-update", "--quiet"])

    def _on_check_finished(self, code: int, _status) -> None:
        proc = self._dnf_proc
        self._dnf_proc = None
        out = bytes(proc.readAllStandardOutput()).decode("utf-8", "replace") if proc else ""
        if code == 100:
            pkgs = [ln.split()[0] for ln in out.splitlines() if ln.split()]
            preview = "\n".join(pkgs[:15])
            more = f"\n… ve {len(pkgs) - 15} paket daha" if len(pkgs) > 15 else ""
            self.upd_status.setText(f"{len(pkgs)} güncelleme mevcut:\n{preview}{more}")
        elif code == 0:
            self.upd_status.setText("Güncel. Bekleyen güncelleme yok.")
        else:
            self.upd_status.setText(f"dnf check-update hata verdi (rc={code}):\n{output_tail(out)}")
        proc.deleteLater()

    def _security_updates(self) -> None:
        rc, out, err = run_ro(["dnf", "updateinfo", "list", "--security"], timeout=120)
        body = output_tail((out + "\n" + err).strip(), 15)
        QMessageBox.information(self, "Güvenlik güncellemeleri", body or "Kayıt bulunamadı.")

    def _upgrade(self) -> None:
        ans = QMessageBox.question(
            self,
            "Sistemi güncelle",
            "Tüm paketler dnf upgrade ile güncellenecek.\n"
            "Komut: pkexec dnf upgrade -y\n\nDevam edilsin mi?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if ans != QMessageBox.StandardButton.Yes:
            return
        rc, out, err = run_pkexec(["dnf", "upgrade", "-y"], timeout=3600)
        QMessageBox.information(
            self, "Güncelleme sonucu", output_tail((out + "\n" + err).strip(), 18) or f"rc={rc}"
        )
