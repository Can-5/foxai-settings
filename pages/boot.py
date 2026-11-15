"""Önyükleyici (GRUB) & Çekirdek ayarları sayfası (gerçek GRUB2 desteği)."""

from __future__ import annotations

import datetime
import os
import re
import tempfile

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pages._root import output_tail, run_ro, safe_kernel_args
from pages.base_page import BasePage
from widgets import Card, SectionLabel, SelectControl, SettingRow, SpinControl

GRUB_FILE = "/etc/default/grub"
GRUB_CFG = "/boot/grub2/grub.cfg"


class BootPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._kv: dict[str, str] = {}
        self._build_ui()

    # ---- /etc/default/grub okuma ----

    def _read_grub_defaults(self) -> dict[str, str]:
        kv: dict[str, str] = {}
        try:
            with open(GRUB_FILE, "r", encoding="utf-8") as fh:
                for raw in fh:
                    m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)=("?)(.*?)\2\s*$', raw.rstrip("\n"))
                    if m:
                        kv[m.group(1)] = m.group(3)
        except OSError as exc:
            kv["_error"] = str(exc)
        return kv

    def _kv_row(self, key: str) -> QWidget:
        row = QWidget()
        from PyQt6.QtWidgets import QHBoxLayout

        rlay = QHBoxLayout(row)
        rlay.setContentsMargins(0, 0, 0, 0)
        rlay.setSpacing(12)
        k = QLabel(key)
        k.setStyleSheet(
            "color: #94a3b8; font-size: 12px; font-weight: 700; background: transparent; min-width: 200px;"
        )
        v = QLabel(self._kv.get(key, "—"))
        v.setStyleSheet(
            "color: #f8fafc; font-size: 12px; font-family: monospace; background: #334155; "
            "padding: 6px 10px; border-radius: 6px; border: 1px solid #475569;"
        )
        v.setWordWrap(True)
        rlay.addWidget(k, 0)
        rlay.addWidget(v, 1)
        return row

    # ---- UI ----

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        self._kv = self._read_grub_defaults()
        if "_error" in self._kv:
            lay.addWidget(SectionLabel("Önyükleyici (GRUB2)"))
            err_card = Card(
                "GRUB varsayılanları okunamadı",
                f"{GRUB_FILE} okunamadı: {self._kv['_error']}",
            )
            lay.addWidget(err_card)
            lay.addStretch()
            return

        lay.addWidget(SectionLabel("Geçerli GRUB2 ayarları (/etc/default/grub)"))
        info = Card("Durum", "Dosyadan canlı okunan değerler (salt okunur).")
        for key in (
            "GRUB_TIMEOUT",
            "GRUB_TIMEOUT_STYLE",
            "GRUB_DISTRIBUTOR",
            "GRUB_DEFAULT",
            "GRUB_DISABLE_SUBMENU",
            "GRUB_DISABLE_RECOVERY",
        ):
            if key in self._kv:
                info.add_widget(self._kv_row(key))
        if not any(k in self._kv for k in ("GRUB_TIMEOUT", "GRUB_DISTRIBUTOR")):
            info.add_widget(
                QLabel("(Dosyada beklenen anahtarlar bulunamadı — farklı bir GRUB kurulumu olabilir.)")
            )
        lay.addWidget(info)

        lay.addWidget(SectionLabel("Düzenle"))
        card = Card(
            "Uygulanabilir değişiklikler",
            "Değişiklikler /etc/default/grub'a pkexec ile yazılır ve grub2-mkconfig çalıştırılır.",
        )
        # Menü bekleme süresi
        try:
            timeout_val = int(self._kv.get("GRUB_TIMEOUT", "5") or "5")
        except ValueError:
            timeout_val = 5
        timeout_spin = SpinControl(0, 120, timeout_val)
        self._timeout_spin = timeout_spin
        card.add_widget(
            SettingRow(
                "Menü bekleme süresi (GRUB_TIMEOUT)",
                "Otomatik önyükleme öncesi saniye cinsinden bekleme.",
                timeout_spin,
            )
        )
        # Çekirdek parametreleri
        params_edit = QLineEdit(self._kv.get("GRUB_CMDLINE_LINUX", ""))
        params_edit.setStyleSheet(
            "background: #334155; border: 1px solid #475569; border-radius: 8px; "
            "padding: 8px 12px; color: #f8fafc; font-family: monospace;"
        )
        self._params_edit = params_edit
        card.add_widget(
            SettingRow(
                "GRUB_CMDLINE_LINUX",
                "Çekirdeğe geçen parametreler. Örn: quiet splash",
                params_edit,
            )
        )
        btn_apply = QPushButton("Değişiklikleri uygula (yedek + mkconfig)")
        btn_apply.setObjectName("primary")
        btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_apply.clicked.connect(self._apply_changes)
        card.content_lay.addWidget(btn_apply)
        self._apply_status = QLabel("")
        self._apply_status.setStyleSheet(
            "color: #94a3b8; font-size: 12px; background: transparent;"
        )
        self._apply_status.setWordWrap(True)
        card.add_widget(self._apply_status)
        lay.addWidget(card)

        lay.addWidget(SectionLabel("Menü girdileri (salt okunur)"))
        menu_card = Card("/boot/grub2/grub.cfg", "Yüklü çekirdek girdileri.")
        rc, out, err = run_ro(
            ["awk", "-F'", "/^menuentry/{print $2}", GRUB_CFG], timeout=10
        )
        if rc == 0 and out.strip():
            for line in out.strip().splitlines():
                lbl = QLabel("• " + line.strip())
                lbl.setStyleSheet("color: #e2e8f0; font-size: 12px; background: transparent;")
                lbl.setWordWrap(True)
                menu_card.add_widget(lbl)
        elif rc == 0:
            menu_card.add_widget(QLabel("(Menü girdisi bulunamadı.)"))
        else:
            menu_card.add_widget(
                QLabel(f"grub.cfg okunamadı (rc={rc}): {output_tail(err or out, 3) or 'izin gerekli'}")
            )
        lay.addWidget(menu_card)

        lay.addStretch()

    # ---- uygulama ----

    def _apply_changes(self) -> None:
        kernel_args = self._params_edit.text().strip()
        if not safe_kernel_args(kernel_args):
            QMessageBox.warning(
                self,
                "Geçersiz çekirdek parametresi",
                "GRUB_CMDLINE_LINUX yalnızca şu karakterleri içerebilir:\n"
                "harf, rakam, '=', ' ', '_', '.', ',', '-', '/'",
            )
            return

        new_timeout = self._timeout_spin.value()
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = f"{GRUB_FILE}.foxai-yedek-{ts}"

        cmds = [
            f"pkexec cp {GRUB_FILE} {backup}",
            f"pkexec cp <geçici-dosya> {GRUB_FILE}",
            f"pkexec grub2-mkconfig -o {GRUB_CFG}",
        ]
        ret = QMessageBox.question(
            self,
            "GRUB2 — değişiklikleri uygula",
            "Şu işlemler çalıştırılacak:\n  • " + "\n  • ".join(cmds)
            + f"\n\nYedek: {backup}\nGRUB_TIMEOUT={new_timeout}\n"
            + f"GRUB_CMDLINE_LINUX=\"{kernel_args}\"\n\n"
            "Önyükleyici bozulursa Fedora canlı USB ile kurtarma gerekebilir.\nDevam edilsin mi?",
        )
        if ret != QMessageBox.StandardButton.Yes:
            return

        # geçici dosyayı hazırla
        try:
            with open(GRUB_FILE, "r", encoding="utf-8") as fh:
                content = fh.read()
        except OSError as exc:
            QMessageBox.critical(self, "GRUB2", f"{GRUB_FILE} okunamadı: {exc}")
            return

        content = self._replace_key(content, "GRUB_TIMEOUT", str(new_timeout))
        content = self._replace_key(content, "GRUB_CMDLINE_LINUX", kernel_args, quoted=True)

        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", prefix="foxai-grub-", suffix=".cfg", delete=False
        ) as tf:
            tf.write(content)
            tmp_path = tf.name

        steps = [
            ["pkexec", "cp", GRUB_FILE, backup],
            ["pkexec", "cp", tmp_path, GRUB_FILE],
            ["pkexec", "grub2-mkconfig", "-o", GRUB_CFG],
        ]
        out_all = []
        ok = True
        for step in steps:
            rc, out, err = run_ro(step, timeout=300)
            out_all.append(rc and output_tail(err or out, 6) or (out or "").strip())
            if rc != 0:
                ok = False
                break

        summary = "\n\n".join(out_all).strip()
        if ok:
            self._apply_status.setText(f"Uygulandı. Yedek: {backup}")
            QMessageBox.information(
                self, "GRUB2", f"Değişiklikler uygulandı.\nYedek: {backup}\n\n{output_tail(summary, 18)}"
            )
            self._kv = self._read_grub_defaults()
        else:
            self._apply_status.setText("Uygulama başarısız oldu — yedek ve çıktıya bakın.")
            QMessageBox.critical(
                self,
                "GRUB2 — HATA",
                f"İşlem başarısız. Yedek (varsa): {backup}\n\n{output_tail(summary, 25)}",
            )
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    def _replace_key(self, content: str, key: str, value: str, quoted: bool = False) -> str:
        replacement_value = f'"{value}"' if quoted else str(value)
        pattern = re.compile(rf"^{re.escape(key)}=.*$", re.MULTILINE)
        if pattern.search(content):
            return pattern.sub(f"{key}={replacement_value}", content, count=1)
        if not content.endswith("\n"):
            content += "\n"
        return content + f"{key}={replacement_value}\n"
