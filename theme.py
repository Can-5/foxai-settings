"""Modern koyu tema stil dosyası (QSS)."""

ACCENT = "#409eff"  # mavi vurgu
ACCENT_HOVER = "#3489e6"
ACCENT_ACTIVE = "#2a79d2"
BG = "#0f172a"  # ana arkaplan (koyu slate)
SIDEBAR = "#1e293b"  # kenar çubuğu
SIDEBAR_HOVER = "#334155"
SIDEBAR_ACTIVE = "#3b5c8c"
CARD = "#1e293b"  # kart arkaplanı
CARD_HOVER = "#334155"
TEXT = "#f8fafc"  # ana metin
TEXT_MUTED = "#94a3b8"  # ikincil metin
BORDER = "#334155"  # kenarlık
DANGER = "#ef4444"
DANGER_HOVER = "#dc2626"
SUCCESS = "#22c55e"
WARN = "#f59e0b"


STYLESHEET = f"""
QWindow, QWidget {{
    background: {BG};
    color: {TEXT};
    font-family: 'Inter', 'Segoe UI', 'Roboto', 'Ubuntu', 'DejaVu Sans', sans-serif;
    font-size: 13px;
}}

QLabel {{
    color: {TEXT};
    background: transparent;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 0px;
}}
QScrollBar::handle:vertical {{
    background: #475569;
    min-height: 60px;
    border-radius: 5px;
}}
QScrollBar::handle:vertical:hover {{
    background: #64748b;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* ---------- Kenar çubuğu ---------- */
QFrame#sidebar {{
    background: {SIDEBAR};
    border-right: 1px solid {BORDER};
    min-width: 240px;
    max-width: 240px;
}}
QLabel#appTitle {{
    color: {TEXT};
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.5px;
    padding: 24px 20px 16px 20px;
}}
QLabel#appSubtitle {{
    color: {TEXT_MUTED};
    font-size: 11px;
    padding: 0 20px 24px 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

QPushButton#navItem {{
    background: transparent;
    border: none;
    border-radius: 10px;
    text-align: left;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: 600;
    color: {TEXT_MUTED};
    margin: 4px 12px;
}}
QPushButton#navItem:hover {{
    background: {SIDEBAR_HOVER};
    color: {TEXT};
}}
QPushButton#navItem:checked {{
    background: {SIDEBAR_ACTIVE};
    color: {TEXT};
    border-left: 4px solid {ACCENT};
    font-weight: 700;
}}
QPushButton#navItem:checked:hover {{
    background: {ACCENT};
}}

/* ---------- Ana içerik ---------- */
QFrame#contentFrame {{
    background: {BG};
}}
QLabel#pageTitle {{
    color: {TEXT};
    font-size: 28px;
    font-weight: 800;
    padding: 0 0 8px 0;
}}
QLabel#pageDesc {{
    color: {TEXT_MUTED};
    font-size: 15px;
    padding: 0 0 24px 0;
}}

/* ---------- Kartlar ---------- */
QFrame#card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
}}
QLabel#cardTitle {{
    color: {TEXT};
    font-size: 17px;
    font-weight: 700;
}}
QLabel#cardDesc {{
    color: {TEXT_MUTED};
    font-size: 13px;
}}

/* ---------- Açıklama metni ---------- */
QLabel#hint {{
    color: {TEXT_MUTED};
    font-size: 12px;
}}

/* ---------- Toggle ---------- */
QCheckBox#toggle::indicator {{
    width: 44px;
    height: 24px;
    border-radius: 12px;
    background: #475569;
    border: none;
}}
QCheckBox#toggle::indicator:checked {{
    background: {ACCENT};
}}
QCheckBox#toggle::indicator:unchecked:hover {{
    background: #64748b;
}}
QCheckBox#toggle::indicator:checked:hover {{
    background: {ACCENT_HOVER};
}}

/* ---------- ComboBox ---------- */
QComboBox {{
    background: #334155;
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 8px 12px;
    color: {TEXT};
    min-height: 36px;
}}
QComboBox:hover {{
    border-color: {ACCENT};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox QAbstractItemView {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 8px;
    selection-background-color: {ACCENT};
    color: {TEXT};
    padding: 4px;
}}

/* ---------- SpinBox / Slider ---------- */
QSpinBox, QDoubleSpinBox {{
    background: #334155;
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 6px 10px;
    color: {TEXT};
    min-height: 34px;
}}
QSlider::groove:horizontal {{
    border: none;
    height: 6px;
    background: #475569;
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    background: {ACCENT};
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
}}
QSlider::handle:horizontal:hover {{
    background: {ACCENT_HOVER};
}}

/* ---------- LineEdit ---------- */
QLineEdit {{
    background: #334155;
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 10px 14px;
    color: {TEXT};
    min-height: 40px;
}}
QLineEdit:focus {{
    border-color: {ACCENT};
}}

/* ---------- Butonlar ---------- */
QPushButton#primary {{
    background: {ACCENT};
    border: none;
    border-radius: 10px;
    color: #ffffff;
    font-weight: 700;
    padding: 10px 20px;
    min-height: 40px;
}}
QPushButton#primary:hover {{
    background: {ACCENT_HOVER};
}}
QPushButton#primary:pressed {{
    background: {ACCENT_ACTIVE};
}}
QPushButton#ghost {{
    background: transparent;
    border: 1px solid {BORDER};
    border-radius: 10px;
    color: {TEXT};
    font-weight: 600;
    padding: 9px 18px;
    min-height: 38px;
}}
QPushButton#ghost:hover {{
    background: {CARD_HOVER};
    border-color: #64748b;
}}
QPushButton#danger {{
    background: {DANGER};
    border: none;
    border-radius: 10px;
    color: #ffffff;
    font-weight: 700;
    padding: 9px 16px;
    min-height: 38px;
}}
QPushButton#danger:hover {{
    background: {DANGER_HOVER};
}}
QPushButton#success {{
    background: {SUCCESS};
    border: none;
    border-radius: 10px;
    color: #ffffff;
    font-weight: 700;
    padding: 9px 16px;
    min-height: 38px;
}}
QPushButton#success:hover {{
    background: #16a34a;
}}

QFrame#divider {{
    background: {BORDER};
    max-height: 1px;
    border: none;
}}

QLabel#sectionLabel {{
    color: {TEXT_MUTED};
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding-top: 8px;
}}
"""
