"""Tüm ayar sayfalarının temel sınıfı."""

from __future__ import annotations

from PyQt6.QtWidgets import QWidget

from database import get_setting, set_setting


class BasePage(QWidget):
    """Bir profilin belirli ayar kategorisini gösteren sayfa."""

    def __init__(self, profile_id: int, parent=None):
        super().__init__(parent)
        self.profile_id = profile_id

    def get(self, key: str, default=None):
        return get_setting(self.profile_id, key, default)

    def set(self, key: str, value) -> None:
        set_setting(self.profile_id, key, value)
