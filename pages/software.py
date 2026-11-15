"""Yazılım & Güncelleme sayfası (depo, paket, güncelleme yönetimi)."""

from __future__ import annotations

from PyQt6.QtCore import Qt, QProcess
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from pages._root import output_tail, run_ro, valid_pkg_name
from pages.base_page import BasePage
from theme import ACCENT
from widgets import (
    Card,
    SectionLabel,
    SettingRow,
    ToggleControl,
    TextControl,
)


class SoftwarePage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._proc = None
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        # Güncellemeler
        lay.addWidget(SectionLabel("Yazılım Güncellemeleri"))
        card = Card(
            "Güncelleme politikası",
            "Sistem ve uygulama paketlerini güncellemeleri kontrol edin.",
        )
        card.add_widget(
            self._bool_row(
                "Otomatik güncellemeleri denetle",
                "Yeni sürümleri arka planda arar.",
                "sw_auto_check",
            )
        )
        card.add_widget(
            self._bool_row(
                "Güvenlik güncellemelerini otomatik kur",
                "Önemli yamaları anında uygular.",
                "sw_security_auto",
            )
        )
        card.add_widget(
            self._bool_row(
                "Flatpak güncellemelerini dahil et",
                "Flatpak uygulamalarını da güncelleme denetimine ekler.",
                "sw_flatpak",
            )
        )
        btn_check = QPushButton("Güncellemeleri denetle (dnf check-update)")
        btn_check.setObjectName("primary")
        btn_check.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_check.clicked.connect(self._check_updates)
        card.content_lay.addWidget(btn_check)
        btn_upgrade = QPushButton("Sistemi güncelle (pkexec dnf upgrade)")
        btn_upgrade.setObjectName("ghost")
        btn_upgrade.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_upgrade.clicked.connect(self._upgrade_system)
        card.content_lay.addWidget(btn_upgrade)
        self._updates_status = QLabel("Henüz denetlenmedi.")
        self._updates_status.setStyleSheet(
            "color: #94a3b8; font-size: 12px; background: transparent;"
        )
        self._updates_status.setWordWrap(True)
        card.add_widget(self._updates_status)
        self._updates_out = QTextEdit()
        self._updates_out.setReadOnly(True)
        self._updates_out.setFixedHeight(120)
        self._updates_out.setPlaceholderText("dnf çıktısı burada görünecek…")
        card.add_widget(self._updates_out)
        lay.addWidget(card)

        # Depolar
        lay.addWidget(SectionLabel("Yazılım Depoları (gerçek liste — dnf repolist)"))
        card2 = Card("Etkin depolar", "Sistemdeki gerçek dnf depoları. Aç/kapa pkexec gerektirir (dnf-plugins-core).")
        self._repos_box = QVBoxLayout()
        self._repos_box.setSpacing(4)
        card2.content_lay.addLayout(self._repos_box)
        repolist_btn = QPushButton("Depo listesini yenile")
        repolist_btn.setObjectName("ghost")
        repolist_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        repolist_btn.clicked.connect(self._load_repos)
        card2.content_lay.addWidget(repolist_btn)
        lay.addWidget(card2)

        # Paket kurulumu
        lay.addWidget(SectionLabel("Paket Yönetimi"))
        card3 = Card("Paket ara ve kur", "Depodan paket adını girip kurun (pkexec ile gerçek kurulum).")
        search = TextControl("", "Paket adı girin (örn. gimp, vlc, libreoffice)")
        self._search = search
        btn_install = QPushButton("Ara ve Kur (dnf install)")
        btn_install.setObjectName("primary")
        btn_install.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_install.clicked.connect(self._install_package)
        slay = QHBoxLayout()
        slay.setSpacing(10)
        slay.addWidget(search, 1)
        slay.addWidget(btn_install, 0)
        card3.content_lay.addLayout(slay)
        lay.addWidget(card3)

        lay.addStretch()
        self._load_repos()

    # ---- dnf async helpers ----

    def _start_proc(self, args: list[str], on_done):
        if self._proc is not None and self._proc.state() != QProcess.ProcessState.NotRunning:
            QMessageBox.warning(self, "dnf", "Başka bir işlem çalışıyor; bitmesini bekleyin.")
            return
        proc = QProcess(self)
        proc.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        proc.finished.connect(on_done)
        proc.start(args[0], args[1:])
        self._proc = proc

    def _check_updates(self) -> None:
        self._updates_status.setText("Denetleniyor (dnf check-update)…")
        self._updates_out.clear()
        self._start_proc(["dnf", "check-update", "--quiet"], self._check_updates_done)

    def _check_updates_done(self, exit_code, _status) -> None:
        out = bytes(self._proc.readAllStandardOutput()).decode("utf-8", "replace") if self._proc else ""
        if exit_code == 0:
            self._updates_status.setText("Sistem güncel — bekleyen güncelleme yok.")
        elif exit_code == 100:
            pkgs = [ln for ln in out.splitlines() if ln.strip() and not ln.startswith("Obsoleting")]
            self._updates_status.setText(f"{len(pkgs)} güncelleme bulundu.")
        else:
            self._updates_status.setText(f"Denetim başarısız (rc={exit_code}).")
        self._updates_out.setPlainText(out.strip() or "(çıktı yok)")

    def _upgrade_system(self) -> None:
        ret = QMessageBox.question(
            self,
            "Sistemi güncelle",
            "'pkexec dnf upgrade -y' komutu çalıştırılacak.\n"
            "Parola yalnızca polkit penceresine girilir — asla buraya değil.\n\nDevam edilsin mi?",
        )
        if ret != QMessageBox.StandardButton.Yes:
            return
        self._updates_status.setText("Güncelleme çalışıyor (bu pencere donabilir)…")
        self._updates_out.clear()
        self._start_proc(["pkexec", "dnf", "upgrade", "-y"], self._upgrade_done)

    def _upgrade_done(self, exit_code, _status) -> None:
        out = bytes(self._proc.readAllStandardOutput()).decode("utf-8", "replace") if self._proc else ""
        if exit_code == 0:
            self._updates_status.setText("Güncelleme tamamlandı.")
        else:
            self._updates_status.setText(f"Güncelleme rc={exit_code} (çıktıya bakın).")
        self._updates_out.setPlainText(output_tail(out, 30))

    def _install_package(self) -> None:
        pkg = self._search.value().strip()
        if not valid_pkg_name(pkg):
            QMessageBox.warning(
                self,
                "Geçersiz paket adı",
                "Paket adı yalnızca harf, rakam ve '. _ - +' içerebilir.",
            )
            return
        ret = QMessageBox.question(
            self,
            "Paket kur",
            f"'pkexec dnf install -y {pkg}' çalıştırılacak.\nDevam edilsin mi?",
        )
        if ret != QMessageBox.StandardButton.Yes:
            return
        self._updates_status.setText(f"'{pkg}' kuruluyor…")
        self._start_proc(["pkexec", "dnf", "install", "-y", pkg], self._install_done)

    def _install_done(self, exit_code, _status) -> None:
        out = bytes(self._proc.readAllStandardOutput()).decode("utf-8", "replace") if self._proc else ""
        if exit_code == 0:
            self._updates_status.setText("Kurulum tamamlandı.")
        else:
            self._updates_status.setText(f"Kurulum rc={exit_code} (çıktıya bakın).")
        self._updates_out.setPlainText(output_tail(out, 30))

    # ---- depolar ----

    def _load_repos(self) -> None:
        while self._repos_box.count():
            item = self._repos_box.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        rc, out, err = run_ro(["dnf", "repolist", "--enabled"], timeout=30)
        enabled_ids = self._parse_repolist(out)
        rc_all, out_all, _ = run_ro(["dnf", "repolist", "--all"], timeout=30)
        all_ids = self._parse_repolist(out_all) if rc_all == 0 else enabled_ids

        if not all_ids:
            lbl = QLabel(f"Depo listesi alınamadı (rc={rc}). {err.strip() or out.strip()}")
            lbl.setStyleSheet("color: #f59e0b; font-size: 12px; background: transparent;")
            lbl.setWordWrap(True)
            self._repos_box.addWidget(lbl)
            return

        for repo_id in all_ids:
            is_enabled = repo_id in enabled_ids
            row = QWidget()
            rlay = QHBoxLayout(row)
            rlay.setContentsMargins(0, 0, 0, 0)
            rlay.setSpacing(12)
            r = QLabel(repo_id)
            r.setStyleSheet(
                "color: #f8fafc; font-size: 13px; font-weight: 700; background: transparent;"
            )
            state = QLabel("etkin" if is_enabled else "kapalı")
            state.setStyleSheet(
                "color: #22c55e; font-size: 12px;" if is_enabled else "color: #64748b; font-size: 12px;"
            )
            btn = QPushButton("Kapat" if is_enabled else "Aç")
            btn.setObjectName("ghost")
            btn.clicked.connect(lambda _=False, rid=repo_id, en=is_enabled: self._set_repo(rid, en))
            rlay.addWidget(r, 1)
            rlay.addWidget(state, 0)
            rlay.addWidget(btn, 0)
            self._repos_box.addWidget(row)

    def _parse_repolist(self, output: str) -> list[str]:
        ids: list[str] = []
        for line in output.splitlines():
            line = line.strip()
            if not line or line.lower().startswith("repolist"):
                continue
            first = line.split()[0]
            if first.lower() == "repo":  # başlık satırı
                continue
            ids.append(first)
        return ids

    def _set_repo(self, repo_id: str, was_enabled: bool) -> None:
        action = "--set-disabled" if was_enabled else "--set-enabled"
        ret = QMessageBox.question(
            self,
            "Depoyu " + ("kapat" if was_enabled else "aç"),
            f"'pkexec dnf config-manager {action} {repo_id}' çalıştırılacak.\nDevam edilsin mi?",
        )
        if ret != QMessageBox.StandardButton.Yes:
            return
        rc, out, err = run_ro(
            ["pkexec", "dnf", "config-manager", action, repo_id], timeout=120
        )
        if rc == 0:
            QMessageBox.information(self, "Depolar", f"'{repo_id}' güncellendi.")
        else:
            QMessageBox.warning(
                self,
                "Depo değiştirilemedi",
                f"rc={rc}\n{output_tail(err or out, 15)}\n\n"
                "Not: bu işlem dnf-plugins-core paketini gerektirir.",
            )
        self._load_repos()
