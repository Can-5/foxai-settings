"""AI Asistan — yerel Ollama ile konuşun. Veriler 127.0.0.1'de kalır, hiçbir şey gönderilmez.

Ollama kurulu değilse: `pkexec dnf install -y ollama` butonu (Fedora deposundadır).
Çalışmıyorsa: `pkexec systemctl start ollama` butonu.
"""

from __future__ import annotations

import json
import platform
import shutil
import urllib.request
import urllib.error

from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from pages._root import output_tail, run_pkexec, run_ro
from pages.base_page import BasePage
from pages.system_info import _os_release
from theme import ACCENT, TEXT_MUTED
from widgets import Card, ScrollPage, SectionLabel

_OLLAMA_URL = "http://127.0.0.1:11434"


def _ollama_version() -> str | None:
    try:
        with urllib.request.urlopen(_OLLAMA_URL + "/api/version", timeout=2) as r:
            return json.loads(r.read().decode()).get("version", "?")
    except Exception:
        return None


def _ollama_models() -> list[str]:
    try:
        with urllib.request.urlopen(_OLLAMA_URL + "/api/tags", timeout=3) as r:
            data = json.loads(r.read().decode())
        return [m.get("name", "?") for m in data.get("models", [])]
    except Exception:
        return []


def _system_context() -> str:
    rel = _os_release()
    rc, kern, _ = run_ro(["uname", "-r"], timeout=10)
    fw = run_ro(["systemctl", "is-active", "firewalld"], timeout=10)[1].strip()
    failed = run_ro(
        ["systemctl", "list-units", "--state=failed", "--no-legend", "--plain"], timeout=10
    )[1].strip()
    try:
        with open("/proc/uptime", encoding="utf-8") as f:
            up = int(float(f.read().split()[0]))
    except OSError:
        up = -1
    lines = [
        f"Dağıtım: {rel.get('PRETTY_NAME', 'Fedora')}",
        f"Çekirdek: {kern.strip()}",
        f"Makine: {platform.node()}",
        f"Çalışma süresi (saniye): {up}",
        f"firewalld: {fw or 'bilinmiyor'}",
        f"Hatalı servisler: {failed or 'yok'}",
    ]
    return "\n".join(lines)


class _ChatWorker(QThread):
    done = pyqtSignal(str, str)  # (model, cevap|hata)

    def __init__(self, model: str, prompt: str, system: str | None, parent=None):
        super().__init__(parent)
        self._model = model
        self._prompt = prompt
        self._system = system

    def run(self) -> None:
        body = {"model": self._model, "prompt": self._prompt, "stream": False}
        if self._system:
            body["system"] = self._system
        req = urllib.request.Request(
            _OLLAMA_URL + "/api/generate",
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = json.loads(r.read().decode())
            self.done.emit(self._model, data.get("response", "(boş cevap)").strip())
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:500]
            self.done.emit(self._model, f"HTTP {e.code}: {detail}")
        except Exception as e:  # bağlantı, zaman aşımı...
            self.done.emit(self._model, f"Hata: {e}")


class AiPage(BasePage):
    def __init__(self, profile_id: int, parent=None):
        super().__init__(profile_id, parent)
        self._worker: _ChatWorker | None = None
        self._build_ui()
        self._refresh_status()

    # ---------- UI ----------
    def _build_ui(self) -> None:
        page = ScrollPage()
        root = QVBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)
        root.addWidget(SectionLabel("AI Asistan"))

        # Durum / kurulum kartı
        st = Card(
            "Yerel yapay zeka (Ollama)",
            "Sorularınız bu makineden dışarı çıkmaz; Ollama 127.0.0.1 üzerinde çalışır. "
            "API anahtarı gerekmez, telemetri yoktur.",
        )
        self.status_lbl = QLabel("Durum denetleniyor…")
        self.status_lbl.setWordWrap(True)
        self.status_lbl.setStyleSheet(
            "color: #e2e8f0; font-size: 12px; background: #1e293b; padding: 10px 12px; "
            "border-radius: 8px; border: 1px solid #334155;"
        )
        st.add_widget(self.status_lbl)

        row = QHBoxLayout()
        row.setSpacing(10)
        b_refresh = QPushButton("Durumu yenile")
        b_refresh.setObjectName("ghost")
        b_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        b_refresh.clicked.connect(self._refresh_status)
        self.b_install = QPushButton("Ollama'yı kur (pkexec dnf install ollama)")
        self.b_install.setObjectName("primary")
        self.b_install.setCursor(Qt.CursorShape.PointingHandCursor)
        self.b_install.clicked.connect(self._install_ollama)
        self.b_start = QPushButton("Servisi başlat (pkexec systemctl start ollama)")
        self.b_start.setObjectName("ghost")
        self.b_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.b_start.clicked.connect(self._start_ollama)
        row.addWidget(b_refresh)
        row.addWidget(self.b_install)
        row.addWidget(self.b_start)
        row.addStretch(1)
        st.content_lay.addLayout(row)

        model_row = QHBoxLayout()
        model_row.setSpacing(10)
        model_row.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(220)
        self.model_combo.setEditable(False)
        model_row.addWidget(self.model_combo)
        b_pull = QPushButton("Model indir…")
        b_pull.setObjectName("ghost")
        b_pull.setCursor(Qt.CursorShape.PointingHandCursor)
        b_pull.clicked.connect(self._pull_model)
        model_row.addWidget(b_pull)
        model_row.addStretch(1)
        st.content_lay.addLayout(model_row)
        root.addWidget(st)

        # Sohbet kartı
        chat = Card("Sohbet", "Ollama'nın yerel modeline sorar. Oturum dışında kaydedilmez.")
        self.ctx_check = QCheckBox("Sistem bağlamını ekle (dağıtım, çekirdek, firewalld, hatalı servisler)")
        self.ctx_check.setChecked(True)
        self.ctx_check.setCursor(Qt.CursorShape.PointingHandCursor)
        chat.add_widget(self.ctx_check)

        self.transcript = QTextBrowser()
        self.transcript.setMinimumHeight(220)
        self.transcript.setStyleSheet(
            "QTextBrowser { background: #0f172a; color: #e2e8f0; border: 1px solid #334155; "
            "border-radius: 8px; padding: 10px; font-size: 13px; }"
        )
        chat.add_widget(self.transcript)

        input_row = QHBoxLayout()
        input_row.setSpacing(10)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Sorunuzu yazın… (örn. 'Güncellemeleri nasıl denetlerim?')")
        self.input.returnPressed.connect(self._send)
        b_send = QPushButton("Gönder")
        b_send.setObjectName("primary")
        b_send.setCursor(Qt.CursorShape.PointingHandCursor)
        b_send.clicked.connect(self._send)
        input_row.addWidget(self.input, 1)
        input_row.addWidget(b_send)
        chat.content_lay.addLayout(input_row)
        root.addWidget(chat)

        page.lay.addLayout(root)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(page)

    # ---------- durum ----------
    def _refresh_status(self) -> None:
        installed = shutil.which("ollama") is not None
        version = _ollama_version()
        self.b_install.setEnabled(not installed)
        if version:
            models = _ollama_models()
            self.status_lbl.setText(
                f"Ollama çalışıyor (v{version}). Yüklü modeller: {', '.join(models) or 'yok'}."
            )
            self.b_start.setEnabled(False)
            self._fill_models(models)
        elif installed:
            self.status_lbl.setText(
                "Ollama kurulu ama çalışmıyor. Servisi başlatmayı deneyin. "
                "Fedora paketi: ollama (systemd birimi: ollama.service)."
            )
            self.b_start.setEnabled(True)
        else:
            self.status_lbl.setText(
                "Ollama kurulu değil. Fedora 45 deposunda: ollama.x86_64 0.24.0. "
                "'Ollama'yı kur' butonu polkit ile kurar."
            )
            self.b_start.setEnabled(False)

    def _fill_models(self, models: list[str]) -> None:
        current = self.model_combo.currentText()
        self.model_combo.clear()
        if models:
            self.model_combo.addItems(models)
            if current in models:
                self.model_combo.setCurrentText(current)
        else:
            self.model_combo.addItem("(model yok — 'Model indir…' ile çekin)")

    def _install_ollama(self) -> None:
        ans = QMessageBox.question(
            self,
            "Ollama'yı kur",
            "Komut: pkexec dnf install -y ollama\n\nDevam edilsin mi?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if ans != QMessageBox.StandardButton.Yes:
            return
        rc, out, err = run_pkexec(["dnf", "install", "-y", "ollama"], timeout=1800)
        QMessageBox.information(
            self, "Kurulum", output_tail((out + "\n" + err).strip(), 18) or f"rc={rc}"
        )
        self._refresh_status()

    def _start_ollama(self) -> None:
        rc, out, err = run_pkexec(["systemctl", "start", "ollama"], timeout=60)
        if rc != 0:
            QMessageBox.warning(
                self, "Ollama", f"Servis başlatılamadı (rc={rc}):\n{output_tail(err or out)}"
            )
            return
        self._refresh_status()

    def _pull_model(self) -> None:
        name, ok = QInputDialog.getText(
            self, "Model indir", "Model adı (örn. qwen2.5:3b, llama3.2:3b, gemma3:1b):"
        )
        name = name.strip()
        if not ok or not name:
            return
        # İsim doğrulaması: ollama adlandırması [name][:tag]
        import re

        if not re.match(r"^[a-zA-Z0-9._\-]+(:[a-zA-Z0-9._\-]+)?$", name):
            QMessageBox.warning(self, "Model indir", "Geçersiz model adı.")
            return
        # Model indirme: ollama CLI yerel servise konuşur, root gerekmez.
        rc, out, err = run_ro(["ollama", "pull", name], timeout=3600)
        QMessageBox.information(
            self, "Model", output_tail((out + "\n" + err).strip(), 12) or f"rc={rc}"
        )
        self._refresh_status()

    # ---------- sohbet ----------
    def _send(self) -> None:
        text = self.input.text().strip()
        if not text or self._worker is not None:
            return
        model = self.model_combo.currentText()
        if not model or model.startswith("("):
            QMessageBox.information(self, "Model gerekli", "Önce bir model seçin veya indirin.")
            return
        system = _system_context() if self.ctx_check.isChecked() else None
        if system:
            system = (
                "Sen bir Fedora/KDE sistem yönetimi asistanısın. Kısa, somut ve doğru cevap ver. "
                "Gerekmedikçe komut önerme; önerirsen komutu kod bloğu içinde ver.\n\n" + system
            )
        self.transcript.append(f"<p><b>Siz:</b> {text}</p>")
        self.input.clear()
        self.input.setEnabled(False)
        self._worker = _ChatWorker(model, text, system, self)
        self._worker.done.connect(self._on_reply)
        self._worker.start()

    def _on_reply(self, model: str, reply: str) -> None:
        self._worker = None
        self.input.setEnabled(True)
        self.input.setFocus()
        esc = (
            reply.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        )
        self.transcript.append(f"<p><b>Ollama ({model}):</b><br>{esc}</p>")
