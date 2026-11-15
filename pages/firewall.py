"""Güvenlik Duvarı — gerçek firewalld durumu ve kuralları (pkexec)."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from pages._root import output_tail, run_ro
from pages.base_page import BasePage
from widgets import Card, SectionLabel, SettingRow, SelectControl, ToggleControl


class FirewallPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._active_zone: str | None = None
        self._build_ui()

    # ---- gerçek firewalld sorguları ----

    def _fw(self, *args: str):
        return run_ro(["firewall-cmd", *args], timeout=15)

    def _detect_state(self) -> dict:
        state: dict = {"active": False}
        rc, out, err = run_ro(["systemctl", "is-active", "firewalld"], timeout=10)
        state["service"] = out.strip() if rc in (0, 3) else f"bilinmiyor (rc={rc})"
        state["active"] = out.strip() == "active"
        if not state["active"]:
            state["detail"] = err.strip() or out.strip()
            return state
        rc, out, _ = self._fw("--get-default-zone")
        state["default_zone"] = out.strip() if rc == 0 else "?"
        rc, out, _ = self._fw("--get-active-zones")
        state["zones"] = out.strip() if rc == 0 else "(alınamadı)"
        # ilk aktif zone: satır formatı "zonadı\n  interfaces: wlo1\n..."
        first_zone = None
        for line in (out or "").splitlines():
            if line and not line.startswith((" ", "\t")):
                first_zone = line.split()[0]
                break
        self._active_zone = first_zone or state["default_zone"]
        rc, out, _ = self._fw("--zone", self._active_zone or "public", "--list-services")
        state["services"] = out.strip().split() if rc == 0 else []
        rc, out, _ = self._fw("--zone", self._active_zone or "public", "--list-ports")
        state["ports"] = out.strip().split() if rc == 0 else []
        return state

    # ---- UI ----

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        # Gerçek durum kartı
        lay.addWidget(SectionLabel("Gerçek Durum (firewalld)"))
        self._status_card = Card("Durum", "firewalld servisi ve aktif zone canlı sorgulanır (salt okunur).")
        self._status_box = QVBoxLayout()
        self._status_box.setSpacing(6)
        self._status_card.content_lay.addLayout(self._status_box)
        refresh = QPushButton("Durumu yenile")
        refresh.setObjectName("ghost")
        refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh.clicked.connect(self._reload_status)
        self._status_card.content_lay.addWidget(refresh)
        lay.addWidget(self._status_card)

        # Port kuralları
        lay.addWidget(SectionLabel(f"Port Kuralları (zone: {self._active_zone or '…'})"))
        self._ports_card = Card(
            "Açık portlar",
            "firewall-cmd ile gerçek port kuralları. Ekleme/kaldırma pkexec ister.",
        )
        self._ports_box = QVBoxLayout()
        self._ports_box.setSpacing(4)
        self._ports_card.content_lay.addLayout(self._ports_box)
        port_in = QLineEdit()
        port_in.setPlaceholderText("Port (1-65535)")
        port_in.setFixedWidth(110)
        self._port_in = port_in
        proto = SelectControl([("TCP", "tcp"), ("UDP", "udp")], "tcp")
        self._port_proto = proto
        btn_add = QPushButton("Portu aç")
        btn_add.setObjectName("primary")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self._add_port)
        rlay = QHBoxLayout()
        rlay.setSpacing(10)
        rlay.addWidget(port_in)
        rlay.addWidget(proto)
        rlay.addWidget(btn_add)
        rlay.addStretch()
        self._ports_card.content_lay.addLayout(rlay)
        lay.addWidget(self._ports_card)

        # Servisler
        lay.addWidget(SectionLabel(f"Servisler (zone: {self._active_zone or '…'})"))
        self._svc_card = Card(
            "Açık servisler",
            "firewall-cmd ile zone'da açık servisler. Ekleme/kaldırma pkexec ister.",
        )
        self._svc_box = QVBoxLayout()
        self._svc_box.setSpacing(4)
        self._svc_card.content_lay.addLayout(self._svc_box)
        svc_in = QLineEdit()
        svc_in.setPlaceholderText("Servis adı (örn. ssh, http, samba)")
        svc_in.setFixedWidth(240)
        self._svc_in = svc_in
        btn_svc = QPushButton("Servisi aç")
        btn_svc.setObjectName("primary")
        btn_svc.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_svc.clicked.connect(self._add_service)
        rlay2 = QHBoxLayout()
        rlay2.setSpacing(10)
        rlay2.addWidget(svc_in)
        rlay2.addWidget(btn_svc)
        rlay2.addStretch()
        self._svc_card.content_lay.addLayout(rlay2)
        lay.addWidget(self._svc_card)

        # Foxai profil tercihleri (iyilikle, ama gerçek değil — etiket dürüst)
        lay.addWidget(SectionLabel("Foxai Profil Tercihleri (yerel kayıt)"))
        card = Card("Tercihler", "Bu ayarlar yalnızca Foxai profili veritabanına kaydedilir; firewalld'i değiştirmez.")
        fw = ToggleControl(self.get("firewall_enabled", False))
        fw.toggled_value.connect(lambda v: self.set("firewall_enabled", v))
        card.add_widget(
            SettingRow("Güvenlik duvarı etkin (tercih)", "Hatırlatıcı tercih; gerçek arayüz değil.", fw)
        )
        mode = SelectControl(
            [("Güvenli", "strict"), ("Dengeli", "balanced"), ("Kapalı", "off")],
            self.get("firewall_mode", "balanced"),
        )
        mode.changed.connect(lambda v: self.set("firewall_mode", v))
        card.add_widget(SettingRow("İşlem modu (tercih)", "Yalnızca kayıt.", mode))
        lay.addWidget(card)

        lay.addStretch()
        self._reload_status()

    # ---- içerik doldurma ----

    def _clear_layout(self, box: QVBoxLayout) -> None:
        while box.count():
            item = box.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

    def _kv_label(self, key: str, value: str, color: str = "#f8fafc") -> QWidget:
        row = QWidget()
        rlay = QHBoxLayout(row)
        rlay.setContentsMargins(0, 0, 0, 0)
        rlay.setSpacing(12)
        k = QLabel(key)
        k.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 700; background: transparent; min-width: 170px;")
        v = QLabel(value)
        v.setStyleSheet(f"color: {color}; font-size: 12px; background: transparent;")
        v.setWordWrap(True)
        rlay.addWidget(k, 0)
        rlay.addWidget(v, 1)
        return row

    def _reload_status(self) -> None:
        state = self._detect_state()
        self._clear_layout(self._status_box)
        service_color = "#22c55e" if state["active"] else "#ef4444"
        self._status_box.addWidget(self._kv_label("firewalld servisi", state.get("service", "?"), service_color))
        if not state["active"]:
            self._status_box.addWidget(
                self._kv_label("Not", "firewalld çalışmıyor — kurallar uygulanamaz.", "#f59e0b")
            )
            return
        self._status_box.addWidget(self._kv_label("Varsayılan zone", state.get("default_zone", "?")))
        for line in (state.get("zones") or "").splitlines():
            if line.strip():
                self._status_box.addWidget(self._kv_label("Aktif zone", line.rstrip()))

        self._clear_layout(self._ports_box)
        if state.get("ports"):
            for p in state["ports"]:
                self._ports_box.addWidget(self._rule_row(p, kind="port"))
        else:
            self._ports_box.addWidget(QLabel("(Açık port kuralı yok)"))

        self._clear_layout(self._svc_box)
        if state.get("services"):
            for s in state["services"]:
                self._svc_box.addWidget(self._rule_row(s, kind="service"))
        else:
            self._svc_box.addWidget(QLabel("(Zone'da açık servis yok)"))

    def _rule_row(self, item: str, kind: str) -> QWidget:
        row = QWidget()
        rlay = QHBoxLayout(row)
        rlay.setContentsMargins(0, 0, 0, 0)
        rlay.setSpacing(12)
        lbl = QLabel(item)
        lbl.setStyleSheet(
            "color: #f8fafc; font-size: 12px; font-family: monospace; background: transparent;"
        )
        btn = QPushButton("Kaldır")
        btn.setObjectName("danger")
        btn.setFixedSize(70, 28)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if kind == "port":
            btn.clicked.connect(lambda _=False, it=item: self._remove_rule("port", it))
        else:
            btn.clicked.connect(lambda _=False, it=item: self._remove_rule("service", it))
        rlay.addWidget(lbl, 1)
        rlay.addWidget(btn, 0)
        row.setStyleSheet("background: transparent; border-radius: 8px;")
        return row

    # ---- pkexec işlemleri ----

    def _zone(self) -> str:
        return self._active_zone or "public"

    def _confirm_and_run(self, title: str, cmds: list[list[str]]) -> None:
        text = "Şu komutlar çalıştırılacak:\n  • " + "\n  • ".join(
            " ".join(c) for c in cmds
        )
        ret = QMessageBox.question(self, title, text + "\n\nDevam edilsin mi?")
        if ret != QMessageBox.StandardButton.Yes:
            return
        for cmd in cmds:
            rc, out, err = run_ro(["pkexec", *cmd], timeout=120)
            if rc != 0:
                QMessageBox.critical(
                    self, title, f"'{' '.join(cmd)}' rc={rc}\n{output_tail(err or out, 15)}"
                )
                return
        QMessageBox.information(self, title, "İşlem tamamlandı.")

    def _add_port(self) -> None:
        raw = self._port_in.text().strip()
        try:
            port = int(raw)
        except ValueError:
            QMessageBox.warning(self, "Port", "Port 1-65535 arası bir sayı olmalı.")
            return
        if not (1 <= port <= 65535):
            QMessageBox.warning(self, "Port", "Port 1-65535 arası olmalı.")
            return
        proto = self._port_proto.value()
        self._confirm_and_run(
            "Port aç",
            [
                ["firewall-cmd", "--zone", self._zone(), f"--add-port={port}/{proto}", "--permanent"],
                ["firewall-cmd", "--reload"],
            ],
        )
        self._port_in.clear()
        self._reload_status()

    def _add_service(self) -> None:
        svc = self._svc_in.text().strip()
        if not svc or not svc.replace("-", "").replace("_", "").isalnum():
            QMessageBox.warning(self, "Servis", "Geçerli bir servis adı girin (harf, rakam, -, _).")
            return
        self._confirm_and_run(
            "Servis aç",
            [
                ["firewall-cmd", "--zone", self._zone(), f"--add-service={svc}", "--permanent"],
                ["firewall-cmd", "--reload"],
            ],
        )
        self._svc_in.clear()
        self._reload_status()

    def _remove_rule(self, kind: str, item: str) -> None:
        flag = f"--remove-{'port' if kind == 'port' else 'service'}={item}"
        self._confirm_and_run(
            "Kuralı kaldır",
            [
                ["firewall-cmd", "--zone", self._zone(), flag, "--permanent"],
                ["firewall-cmd", "--reload"],
            ],
        )
        self._reload_status()
