"""Tüm ayar sayfalarının temel sınıfı."""

from __future__ import annotations

from PyQt6.QtWidgets import QWidget

from database import get_setting, set_setting
from widgets import ScrollPage, SettingRow, ToggleControl


class BasePage(ScrollPage):
    """Kaydırılabilir ayar sayfası temeli — içeriği 30/24 marjinli viewport'a yazar."""

    def __init__(self, profile_id: int, parent=None):
        super().__init__(parent)
        self.profile_id = profile_id

    def get(self, key: str, default=None):
        return get_setting(self.profile_id, key, default)

    def set(self, key: str, value) -> None:
        set_setting(self.profile_id, key, value)

    def _bool_row(self, title: str, desc: str, key: str) -> SettingRow:
        ctrl = ToggleControl(self.get(key, True))
        ctrl.toggled_value.connect(lambda v: self.set(key, v))
        return SettingRow(title, desc, ctrl)
