"""FoxAI Settings tema — "atölye enstrümanı".

Sıcak grafit zemin + pirinç vurgu. Düz yüzeyler, 1px hatlar, focus halkası görünür.
Token'ları yalnız burada tanımla; sayfalarda hardcode hex kullanma.
Yön gerekçesi: DESIGN.md
"""

ACCENT = "#d6a13e"        # pirinç
ACCENT_HOVER = "#e0b056"
ACCENT_ACTIVE = "#b9832f"
BG = "#14171a"            # pencere zemini
SIDEBAR = "#181c20"       # sol ray
SIDEBAR_HOVER = "#20252a"
SIDEBAR_ACTIVE = "#23292f"   # seçili satır (sol accent bar ile)
CARD = "#1c2126"          # kart yüzeyi
CARD_HOVER = "#22282e"
INPUT = "#232a31"         # girdi / seçili satır yüzeyi
BORDER = "#2a3138"        # 1px hat
TEXT = "#e9e6df"          # sıcak kırık beyaz
TEXT_MUTED = "#a8a59c"    # ~6.6 kontrast (AA ✓)
DANGER = "#c75450"
DANGER_HOVER = "#b14440"
SUCCESS = "#8ab06f"
SUCCESS_HOVER = "#96bc7a"
WARN = "#cd8a4e"          # bakır — accent'ten ayrı ama sıcak

_FONT = "'Cantarell', 'DejaVu Sans', sans-serif"
_MONO = "'Liberation Mono', 'DejaVu Sans Mono', monospace"


STYLESHEET = f"""
QWindow, QWidget {{
    background: {BG};
    color: {TEXT};
    font-family: {_FONT};
    font-size: 13px;
}}

QLabel {{
    color: {TEXT};
    background: transparent;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    margin: 0px;
}}
QScrollBar::handle:vertical {{
    background: #3a424a;
    min-height: 48px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical:hover {{
    background: #4a545e;
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
    font-size: 19px;
    font-weight: 700;
}}
QLabel#appSubtitle {{
    color: {TEXT_MUTED};
    font-size: 11px;
    font-weight: 400;
}}

QPushButton#navItem {{
    background: transparent;
    border: none;
    border-left: 3px solid transparent;
    border-radius: 6px;
    text-align: left;
    padding: 10px 17px;
    font-size: 13px;
    font-weight: 600;
    color: {TEXT_MUTED};
    margin: 2px 10px;
}}
QPushButton#navItem:hover {{
    background: {SIDEBAR_HOVER};
    color: {TEXT};
}}
QPushButton#navItem:checked {{
    background: {SIDEBAR_ACTIVE};
    color: {TEXT};
    border-left: 3px solid {ACCENT};
    font-weight: 700;
}}
QPushButton#navItem:checked:hover {{
    background: {SIDEBAR_ACTIVE};
    color: {TEXT};
}}
QPushButton#navItem:focus {{
    border-left: 3px solid {ACCENT};
}}

/* ---------- Ana içerik ---------- */
QFrame#contentFrame {{
    background: {BG};
}}
QLabel#pageTitle {{
    color: {TEXT};
    font-size: 22px;
    font-weight: 700;
}}
QLabel#pageDesc {{
    color: {TEXT_MUTED};
    font-size: 13px;
}}

/* ---------- Kartlar ---------- */
QFrame#card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}
QLabel#cardTitle {{
    color: {TEXT};
    font-size: 15px;
    font-weight: 700;
}}
QLabel#cardDesc {{
    color: {TEXT_MUTED};
    font-size: 12px;
}}

/* ---------- Açıklama metni ---------- */
QLabel#hint {{
    color: {TEXT_MUTED};
    font-size: 12px;
}}

/* ---------- Toggle ---------- */
QCheckBox#toggle::indicator {{
    width: 40px;
    height: 22px;
    border-radius: 11px;
    background: #3a424a;
    border: none;
}}
QCheckBox#toggle::indicator:checked {{
    background: {ACCENT};
}}
QCheckBox#toggle::indicator:unchecked:hover {{
    background: #475260;
}}
QCheckBox#toggle::indicator:checked:hover {{
    background: {ACCENT_HOVER};
}}
QCheckBox#toggle::indicator:focus {{
    border: 2px solid {ACCENT};
}}

/* ---------- ComboBox ---------- */
QComboBox {{
    background: {INPUT};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 8px 12px;
    color: {TEXT};
    min-height: 36px;
}}
QComboBox:hover {{
    border-color: {ACCENT};
}}
QComboBox:focus {{
    border: 2px solid {ACCENT};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox QAbstractItemView {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 6px;
    selection-background-color: {ACCENT};
    selection-color: #14171a;
    color: {TEXT};
    padding: 4px;
}}

/* ---------- SpinBox / Slider ---------- */
QSpinBox, QDoubleSpinBox {{
    background: {INPUT};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 6px 10px;
    color: {TEXT};
    min-height: 34px;
}}
QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 2px solid {ACCENT};
}}
QSlider::groove:horizontal {{
    border: none;
    height: 6px;
    background: #3a424a;
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    background: {ACCENT};
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}}
QSlider::handle:horizontal:hover {{
    background: {ACCENT_HOVER};
}}

/* ---------- LineEdit ---------- */
QLineEdit {{
    background: {INPUT};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 10px 14px;
    color: {TEXT};
    min-height: 40px;
    selection-background-color: {ACCENT};
    selection-color: #14171a;
}}
QLineEdit:focus {{
    border: 2px solid {ACCENT};
}}

/* ---------- Butonlar ---------- */
QPushButton#primary {{
    background: {ACCENT};
    border: none;
    border-radius: 6px;
    color: #14171a;
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
QPushButton#primary:focus {{
    border: 2px solid {TEXT};
}}
QPushButton#ghost {{
    background: transparent;
    border: 1px solid {BORDER};
    border-radius: 6px;
    color: {TEXT};
    font-weight: 600;
    padding: 9px 18px;
    min-height: 38px;
}}
QPushButton#ghost:hover {{
    background: {CARD_HOVER};
    border-color: {ACCENT};
}}
QPushButton#ghost:focus {{
    border: 2px solid {ACCENT};
}}
QPushButton#danger {{
    background: {DANGER};
    border: none;
    border-radius: 6px;
    color: #f6e9e7;
    font-weight: 700;
    padding: 9px 16px;
    min-height: 38px;
}}
QPushButton#danger:hover {{
    background: {DANGER_HOVER};
}}
QPushButton#danger:focus {{
    border: 2px solid {TEXT};
}}
QPushButton#success {{
    background: {SUCCESS};
    border: none;
    border-radius: 6px;
    color: #14171a;
    font-weight: 700;
    padding: 9px 16px;
    min-height: 38px;
}}
QPushButton#success:hover {{
    background: {SUCCESS_HOVER};
}}
QPushButton#success:focus {{
    border: 2px solid {TEXT};
}}

QFrame#divider {{
    background: {BORDER};
    max-height: 1px;
    border: none;
}}

QLabel#sectionLabel {{
    color: {TEXT_MUTED};
    font-size: 12px;
    font-weight: 600;
    padding-top: 8px;
}}
"""
