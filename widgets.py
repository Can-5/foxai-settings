"""Kullanıcı arabirimi yapı taşları: ayar satırları, kartlar, butonlar."""

from __future__ import annotations

from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPalette
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from theme import ACCENT, TEXT, TEXT_MUTED


class SettingRow(QWidget):
    """Tek bir ayar satırı: açıklama + kontrol."""

    def __init__(self, title: str, desc: str, control: QWidget, parent=None):
        super().__init__(parent)
        self.setObjectName("settingRow")
        lay = QHBoxLayout(self)
        lay.setContentsMargins(20, 14, 20, 14)
        lay.setSpacing(16)

        info = QWidget()
        ilay = QVBoxLayout(info)
        ilay.setContentsMargins(0, 0, 0, 0)
        ilay.setSpacing(4)
        t = QLabel(title)
        t.setObjectName("rowTitle")
        t.setStyleSheet(
            f"color: {TEXT}; font-size: 14px; font-weight: 700; background: transparent;"
        )
        d = QLabel(desc)
        d.setObjectName("rowDesc")
        d.setStyleSheet(
            f"color: {TEXT_MUTED}; font-size: 12px; background: transparent;"
        )
        d.setWordWrap(True)
        ilay.addWidget(t)
        ilay.addWidget(d)

        lay.addWidget(info, 1)
        lay.addWidget(control, 0, Qt.AlignmentFlag.AlignVCenter)

    # Stil için satır arkaplanı
    def set_selected(self, selected: bool) -> None:
        if selected:
            self.setStyleSheet("background: #334155; border-radius: 10px;")
        else:
            self.setStyleSheet("background: transparent; border-radius: 10px;")


class Card(QFrame):
    """İçerik kartı."""

    def __init__(self, title: str = "", desc: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(22, 20, 22, 22)
        lay.setSpacing(10)
        if title:
            t = QLabel(title)
            t.setObjectName("cardTitle")
            t.setStyleSheet(
                "color: #f8fafc; font-size: 17px; font-weight: 700; background: transparent;"
            )
            lay.addWidget(t)
        if desc:
            d = QLabel(desc)
            d.setObjectName("cardDesc")
            d.setStyleSheet("color: #94a3b8; font-size: 13px; background: transparent;")
            d.setWordWrap(True)
            lay.addWidget(d)
        self.content = QWidget()
        self.content_lay = QVBoxLayout(self.content)
        self.content_lay.setContentsMargins(0, 10, 0, 0)
        self.content_lay.setSpacing(10)
        lay.addWidget(self.content)

    def add_widget(self, widget: QWidget) -> None:
        self.content_lay.addWidget(widget)

    def add_stretch(self) -> None:
        self.content_lay.addStretch()


class SectionLabel(QWidget):
    """Bölüm başlığı."""

    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 12, 0, 6)
        lbl = QLabel(text)
        lbl.setObjectName("sectionLabel")
        lbl.setStyleSheet(
            "color: #94a3b8; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; background: transparent;"
        )
        lay.addWidget(lbl)


class Divider(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("divider")
        self.setFixedHeight(1)


class ScrollPage(QScrollArea):
    """Kaydıralı bir ayar sayfası."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        container = QWidget()
        container.setObjectName("pageContainer")
        container.setStyleSheet("background: transparent;")
        self.lay = QVBoxLayout(container)
        self.lay.setContentsMargins(30, 24, 30, 24)
        self.lay.setSpacing(20)
        self.setWidget(container)


# ---------- Kontrol öğeleri ----------


class ToggleControl(QCheckBox):
    toggled_value = pyqtSignal(bool)

    def __init__(self, checked: bool = False, parent=None):
        super().__init__(parent)
        self.setObjectName("toggle")
        self.setChecked(checked)
        self.toggled.connect(self.toggled_value.emit)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class SelectControl(QComboBox):
    changed = pyqtSignal(object)

    def __init__(self, items: list[tuple[str, object]], value: object, parent=None):
        super().__init__(parent)
        self._map: dict[str, object] = {}
        for label, val in items:
            self.addItem(label)
            self._map[label] = val
        # mevcut değeri seç
        for i in range(self.count()):
            if self.itemData(i, role=Qt.ItemDataRole.UserRole) is None:
                # veri ayrı saklanıyor; _map üzerinden eşle
                pass
        self._select_value(value)
        self.currentIndexChanged.connect(self._on_change)

    def _select_value(self, value: object) -> None:
        for label, val in self._map.items():
            if val == value:
                self.setCurrentText(label)
                return
        if self.count():
            self.setCurrentIndex(0)

    def _on_change(self, index: int) -> None:
        label = self.itemText(index)
        self.changed.emit(self._map.get(label))

    def value(self) -> object:
        label = self.currentText()
        return self._map.get(label)


class SliderControl(QWidget):
    changed = pyqtSignal(int)

    def __init__(
        self,
        minimum: int = 0,
        maximum: int = 100,
        value: int = 50,
        unit: str = "",
        parent=None,
    ):
        super().__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(minimum, maximum)
        self.slider.setValue(value)
        self.slider.valueChanged.connect(self.changed.emit)
        self.value_label = QLabel(f"{value}{unit}")
        self.value_label.setFixedWidth(40)
        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.value_label.setStyleSheet(
            "color: #94a3b8; font-size: 12px; background: transparent;"
        )
        self.slider.valueChanged.connect(
            lambda v: self.value_label.setText(f"{v}{unit}")
        )
        lay.addWidget(self.slider, 1)
        lay.addWidget(self.value_label, 0)

    def value(self) -> int:
        return self.slider.value()


class SpinControl(QSpinBox):
    def __init__(
        self,
        minimum: int = 0,
        maximum: int = 9999,
        value: int = 0,
        parent=None,
    ):
        super().__init__(parent)
        self.setRange(minimum, maximum)
        self.setValue(value)
        self.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)


class TextControl(QWidget):
    changed = pyqtSignal(str)

    def __init__(self, text: str = "", placeholder: str = "", parent=None):
        super().__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.edit = QLineEdit(text)
        self.edit.setPlaceholderText(placeholder)
        self.edit.textChanged.connect(self.changed.emit)
        lay.addWidget(self.edit)

    def value(self) -> str:
        return self.edit.text()


class ActionRow(QWidget):
    """Sağda bir eylem butonu olan ayar satırı."""

    clicked = pyqtSignal()

    def __init__(
        self, title: str, desc: str, button_text: str = "Değiştir", parent=None
    ):
        super().__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(20, 14, 20, 14)
        lay.setSpacing(16)
        info = QWidget()
        ilay = QVBoxLayout(info)
        ilay.setContentsMargins(0, 0, 0, 0)
        ilay.setSpacing(4)
        t = QLabel(title)
        t.setStyleSheet(
            "color: #f8fafc; font-size: 14px; font-weight: 700; background: transparent;"
        )
        d = QLabel(desc)
        d.setStyleSheet("color: #94a3b8; font-size: 12px; background: transparent;")
        d.setWordWrap(True)
        ilay.addWidget(t)
        ilay.addWidget(d)
        self.btn = QPushButton(button_text)
        self.btn.setObjectName("ghost")
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.clicked.connect(self.clicked.emit)
        lay.addWidget(info, 1)
        lay.addWidget(self.btn, 0)
