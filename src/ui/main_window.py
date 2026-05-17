"""
CountBooks — Ventana principal
Tres secciones en una sola ventana navegable.
Estilo fiel a los HTML de referencia: Newsreader + Manrope,
paleta #03192e / #faf9f8 / #E8E4D9 / #fed488.
"""

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QFormLayout, QComboBox, QSpinBox,
    QFrame, QAbstractItemView, QListWidget, QListWidgetItem,
    QStackedWidget, QMessageBox, QFileDialog, QRadioButton,
    QCheckBox, QButtonGroup, QScrollArea, QProgressBar, QSizePolicy,
    QGridLayout,
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QColor, QCursor

# ══════════════════════════════════════════════════════════════════════════════
# Tokens de diseño — extraídos 1:1 del HTML
# ══════════════════════════════════════════════════════════════════════════════
C_PRIMARY        = "#03192e"
C_PRIMARY_MED    = "#1a2e44"
C_ACCENT         = "#775a19"
C_ACCENT_LIGHT   = "#fed488"
C_BG             = "#faf9f8"
C_BG_ALT         = "#f4f3f2"
C_SLATE_50       = "#f8fafc"
C_SURFACE        = "#ffffff"
C_BORDER         = "#E8E4D9"
C_TEXT           = "#1a1c1c"
C_TEXT_MUTED     = "#43474d"
C_TEXT_LIGHT     = "#74777d"
C_SLATE_400      = "#94a3b8"
C_SLATE_500      = "#64748b"
C_SLATE_600      = "#475569"
C_GREEN_700      = "#15803d"
C_GREEN_50       = "#f0fdf4"
C_ERROR          = "#ba1a1a"
C_ERROR_BG       = "#ffdad6"
C_WARN_BG        = "#fff8e1"
C_WARN           = "#7a5c00"
C_BLUE_50        = "#eff6ff"
C_BLUE_700       = "#1d4ed8"
C_BLUE_950       = "#172554"
C_PURPLE_50      = "#faf5ff"
C_PURPLE_700     = "#7e22ce"

FONT_SERIF = "Georgia"
FONT_SANS  = "Segoe UI"

# ══════════════════════════════════════════════════════════════════════════════
# Stylesheet global
# ══════════════════════════════════════════════════════════════════════════════
QSS = f"""
QWidget {{
    background-color: {C_BG};
    color: {C_TEXT};
    font-family: '{FONT_SANS}';
    font-size: 13px;
}}
#sidebar {{
    background-color: {C_SLATE_50};
    border-right: 1px solid {C_BORDER};
    min-width: 224px;
    max-width: 224px;
}}
#brand_title {{
    font-family: '{FONT_SERIF}';
    font-size: 22px;
    font-style: italic;
    font-weight: bold;
    color: {C_BLUE_950};
    background: transparent;
}}
#brand_sub {{
    font-size: 10px;
    color: {C_SLATE_500};
    font-style: italic;
    background: transparent;
}}
#status_lbl {{
    font-size: 10px;
    color: {C_SLATE_400};
    font-weight: bold;
    letter-spacing: 2px;
    background: transparent;
    padding: 0 20px;
}}
QPushButton#nav_btn {{
    background-color: transparent;
    color: {C_SLATE_600};
    border: none;
    border-left: 4px solid transparent;
    padding: 12px 20px;
    text-align: left;
    font-size: 13px;
}}
QPushButton#nav_btn:hover {{
    color: {C_PRIMARY_MED};
    background-color: rgba(232,228,217,0.3);
}}
QPushButton#nav_btn[active=true] {{
    color: {C_BLUE_950};
    font-weight: bold;
    border-left: 4px solid {C_BLUE_950};
    background-color: rgba(232,228,217,0.2);
}}
#topbar {{
    background-color: {C_SURFACE};
    border-bottom: 1px solid {C_BORDER};
    min-height: 56px;
    max-height: 56px;
}}
QLineEdit#search_input {{
    background-color: {C_BG_ALT};
    border: 1px solid {C_BORDER};
    border-radius: 2px;
    padding: 5px 12px;
    font-size: 13px;
    min-width: 220px;
}}
QLineEdit#search_input:focus {{ border: 1px solid {C_PRIMARY}; }}
QPushButton#btn_primary {{
    background-color: {C_PRIMARY};
    color: white;
    border: none;
    border-radius: 2px;
    padding: 8px 22px;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
}}
QPushButton#btn_primary:hover {{ background-color: {C_PRIMARY_MED}; }}
QPushButton#btn_secondary {{
    background-color: transparent;
    color: {C_ACCENT};
    border: 1px solid {C_ACCENT};
    border-radius: 2px;
    padding: 7px 16px;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
}}
QPushButton#btn_secondary:hover {{
    background-color: {C_ACCENT_LIGHT};
    color: {C_PRIMARY};
}}
QPushButton#btn_ghost {{
    background-color: transparent;
    color: {C_SLATE_600};
    border: 1px solid {C_BORDER};
    border-radius: 2px;
    padding: 5px 12px;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
}}
QPushButton#btn_ghost:hover {{ background-color: {C_BG_ALT}; }}
QPushButton#btn_danger {{
    background-color: transparent;
    color: {C_ERROR};
    border: 1px solid {C_ERROR};
    border-radius: 2px;
    padding: 5px 12px;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
}}
QPushButton#btn_danger:hover {{
    background-color: {C_ERROR_BG};
}}
QPushButton#btn_purple {{
    background-color: {C_PURPLE_700};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: bold;
}}
QPushButton#btn_purple:hover {{
    background-color: #5b1598;
}}
QTableWidget {{
    background-color: {C_SURFACE};
    border: 1px solid {C_BORDER};
    gridline-color: {C_BORDER};
    font-size: 13px;
    outline: none;
}}
QTableWidget::item {{
    padding: 9px 12px;
    border: none;
    color: {C_TEXT};
}}
QTableWidget::item:selected {{
    background-color: rgba(209,228,255,0.5);
    color: {C_PRIMARY};
}}
QHeaderView::section {{
    background-color: {C_PRIMARY};
    color: {C_ACCENT_LIGHT};
    padding: 10px 12px;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
    border: none;
    border-right: 1px solid {C_PRIMARY_MED};
}}
QHeaderView::section:last-child {{ border-right: none; }}
QLineEdit#form_input, QLineEdit#modal_input {{
    background-color: {C_BG};
    border: 1px solid #cbd5e1;
    border-radius: 2px;
    padding: 10px 12px;
    font-size: 13px;
    color: {C_TEXT};
}}
QLineEdit#form_input:focus, QLineEdit#modal_input:focus {{
    border: 1px solid {C_PRIMARY};
    background-color: {C_SURFACE};
}}
QComboBox#form_combo, QComboBox#modal_combo {{
    background-color: {C_BG};
    border: 1px solid #cbd5e1;
    border-radius: 2px;
    padding: 10px 12px;
    font-size: 13px;
}}
QSpinBox#form_spin, QSpinBox#modal_spin {{
    background-color: {C_BG};
    border: 1px solid #cbd5e1;
    border-radius: 2px;
    padding: 10px 12px;
    font-size: 13px;
}}
QComboBox::drop-down {{ border: none; width: 24px; }}
QDialog {{ background-color: {C_SURFACE}; }}
QListWidget#search_list {{
    background-color: {C_SURFACE};
    border: none;
    outline: none;
}}
QListWidget#search_list::item {{ border-bottom: 1px solid {C_BORDER}; padding: 0; }}
QListWidget#search_list::item:hover {{ background-color: {C_BG}; }}
QListWidget#search_list::item:selected {{ background-color: transparent; }}
QScrollBar:vertical {{
    background: {C_BG_ALT}; width: 6px; margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {C_BORDER}; border-radius: 3px; min-height: 30px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{ height: 0; }}
#card {{
    background-color: {C_SURFACE};
    border: 1px solid {C_BORDER};
}}
#card_header {{
    background-color: {C_SLATE_50};
    border-bottom: 1px solid {C_BORDER};
}}
#detail_panel {{
    background-color: {C_SURFACE};
    border: 1px solid {C_BORDER};
}}
#badge_green {{
    color: {C_GREEN_700}; background-color: {C_GREEN_50};
    border-radius: 2px; padding: 2px 7px;
    font-size: 10px; font-weight: bold; letter-spacing: 1px;
}}
#badge_red {{
    color: {C_ERROR}; background-color: {C_ERROR_BG};
    border-radius: 2px; padding: 2px 7px;
    font-size: 10px; font-weight: bold; letter-spacing: 1px;
}}
#badge_blue {{
    color: {C_BLUE_700}; background-color: {C_BLUE_50};
    border-radius: 2px; padding: 2px 7px;
    font-size: 10px; font-weight: bold; letter-spacing: 1px;
}}
#badge_amber {{
    color: {C_ACCENT}; background-color: {C_ACCENT_LIGHT};
    border-radius: 2px; padding: 2px 7px;
    font-size: 10px; font-weight: bold; letter-spacing: 1px;
}}
#badge_purple {{
    color: {C_PURPLE_700}; background-color: {C_PURPLE_50};
    border-radius: 2px; padding: 2px 7px;
    font-size: 10px; font-weight: bold; letter-spacing: 1px;
}}
"""


# ══════════════════════════════════════════════════════════════════════════════
# Utilidades de UI
# ══════════════════════════════════════════════════════════════════════════════

def sep_line() -> QFrame:
    f = QFrame()
    f.setFrameShape(QFrame.HLine)
    f.setStyleSheet(f"background: {C_BORDER}; max-height: 1px; border: none;")
    f.setFixedHeight(1)
    return f


def section_title(text: str, size: int = 40) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"font-family: '{FONT_SERIF}'; font-size: {size}px; font-style: italic; "
        f"font-weight: bold; color: {C_PRIMARY}; background: transparent;"
    )
    return lbl


def field_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"font-size: 11px; font-weight: bold; color: {C_SLATE_500}; "
        f"letter-spacing: 1px; background: transparent;"
    )
    return lbl


def card_header_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"font-size: 11px; font-weight: bold; color: {C_SLATE_500}; "
        f"letter-spacing: 2px; background: transparent;"
    )
    return lbl


def make_card() -> tuple:
    """Devuelve (card_widget, header_hbox, body_vbox)."""
    card = QWidget()
    card.setObjectName("card")
    cl = QVBoxLayout(card)
    cl.setContentsMargins(0, 0, 0, 0)
    cl.setSpacing(0)

    hdr = QWidget()
    hdr.setObjectName("card_header")
    hl = QHBoxLayout(hdr)
    hl.setContentsMargins(20, 12, 20, 12)

    body = QWidget()
    body.setStyleSheet(f"background: {C_SURFACE};")
    bl = QVBoxLayout(body)
    bl.setContentsMargins(20, 18, 20, 20)
    bl.setSpacing(14)

    cl.addWidget(hdr)
    cl.addWidget(body)
    return card, hl, bl


# ══════════════════════════════════════════════════════════════════════════════
# Modal — Búsqueda
# ══════════════════════════════════════════════════════════════════════════════

class SearchModal(QDialog):
    book_selected = Signal(dict)

    def __init__(self, results: list, query: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Búsqueda")
        self.setMinimumSize(600, 460)
        self.setStyleSheet(QSS)
        self._build(results, query)

    def _build(self, results: list, query: str):
        lay = QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)

        hdr = QWidget()
        hdr.setStyleSheet(f"background-color: {C_PRIMARY};")
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(24, 16, 24, 16)
        t = QLabel(f"{len(results)} resultado(s) — \"{query}\"")
        t.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background: transparent;")
        hl.addWidget(t)
        lay.addWidget(hdr)

        if not results:
            empty = QLabel("No se encontraron libros con ese criterio.")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet(
                f"color: {C_TEXT_LIGHT}; font-style: italic; padding: 48px; background: {C_SURFACE};"
            )
            lay.addWidget(empty, 1)
        else:
            lw = QListWidget()
            lw.setObjectName("search_list")
            for book in results:
                item = QListWidgetItem()
                item.setData(Qt.UserRole, book)
                row = QWidget()
                row.setStyleSheet(f"background: {C_SURFACE}; border-bottom: 1px solid {C_BORDER};")
                rl = QVBoxLayout(row)
                rl.setContentsMargins(20, 12, 20, 12)
                rl.setSpacing(3)

                tl = QLabel(book.get("titulo", "—"))
                tl.setStyleSheet(
                    f"font-family: '{FONT_SERIF}'; font-size: 14px; font-weight: bold; "
                    f"color: {C_PRIMARY}; background: transparent;"
                )
                al = QLabel(book.get("autor", "—"))
                al.setStyleSheet(f"font-size: 12px; color: {C_TEXT_MUTED}; background: transparent;")

                meta = QHBoxLayout()
                meta.setSpacing(8)
                if book.get("categoria"):
                    cat = QLabel(book["categoria"])
                    cat.setObjectName("badge_amber")
                    meta.addWidget(cat)
                if book.get("codigo_isbn"):
                    isbn = QLabel(f"ISBN {book['codigo_isbn']}")
                    isbn.setStyleSheet(f"font-size: 11px; color: {C_TEXT_LIGHT}; background: transparent;")
                    meta.addWidget(isbn)
                # Badge perdido en la búsqueda
                if str(book.get("perdido", "NO")).upper() == "SI":
                    perdido_lbl = QLabel("PERDIDO")
                    perdido_lbl.setObjectName("badge_purple")
                    meta.addWidget(perdido_lbl)
                meta.addStretch()

                rl.addWidget(tl)
                rl.addWidget(al)
                rl.addLayout(meta)
                item.setSizeHint(QSize(0, 80))
                lw.addItem(item)
                lw.setItemWidget(item, row)

            lw.itemDoubleClicked.connect(lambda i: (
                self.book_selected.emit(i.data(Qt.UserRole)), self.accept()
            ))
            lay.addWidget(lw, 1)

            hint = QLabel("Doble clic para ver el libro en el inventario")
            hint.setAlignment(Qt.AlignCenter)
            hint.setStyleSheet(
                f"font-size: 11px; color: {C_SLATE_400}; font-style: italic; "
                f"background: {C_BG_ALT}; border-top: 1px solid {C_BORDER}; padding: 8px;"
            )
            lay.addWidget(hint)

        ft = QWidget()
        ft.setStyleSheet(f"background: {C_SLATE_50}; border-top: 1px solid {C_BORDER};")
        fl = QHBoxLayout(ft)
        fl.setContentsMargins(20, 10, 20, 10)
        fl.addStretch()
        cb = QPushButton("CERRAR")
        cb.setObjectName("btn_secondary")
        cb.clicked.connect(self.reject)
        fl.addWidget(cb)
        lay.addWidget(ft)


# ══════════════════════════════════════════════════════════════════════════════
# Modal — Editar libro
# ══════════════════════════════════════════════════════════════════════════════

class EditBookModal(QDialog):
    book_updated = Signal(dict)

    MODAL_CSS = """
    QDialog { background: #ffffff; }
    QLineEdit { background: #faf9f8; border: 1px solid #cbd5e1;
                border-radius: 2px; padding: 7px 10px; font-size: 13px; color: #1a1c1c; }
    QLineEdit:focus { border: 1px solid #03192e; background: #ffffff; }
    QComboBox { background: #faf9f8; border: 1px solid #cbd5e1;
                border-radius: 2px; padding: 7px 10px; font-size: 13px; color: #1a1c1c; }
    QComboBox::drop-down { border: none; width: 20px; }
    QSpinBox { background: #faf9f8; border: 1px solid #cbd5e1;
               border-radius: 2px; padding: 7px 10px; font-size: 13px; color: #1a1c1c; }
    QPushButton#btn_cancel {
        background: transparent; color: #475569; border: 1px solid #E8E4D9;
        border-radius: 2px; padding: 8px 18px; font-size: 12px; font-weight: bold;
        min-width: 90px;
    }
    QPushButton#btn_cancel:hover { background: #f4f3f2; }
    QPushButton#btn_save {
        background: #03192e; color: white; border: none;
        border-radius: 2px; padding: 8px 18px; font-size: 12px; font-weight: bold;
        min-width: 140px;
    }
    QPushButton#btn_save:hover { background: #1a2e44; }
    QPushButton#btn_save:pressed { background: #061d32; }
    """

    def __init__(self, book: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar libro — " + book.get("titulo", ""))
        self.setFixedWidth(620)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.setStyleSheet(self.MODAL_CSS)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.original = book
        self.inputs = {}
        self._build(book)

    def _inp(self, key, val):
        w = QLineEdit(str(val) if val else "")
        self.inputs[key] = w
        return w

    def _cmb(self, key, opts, current):
        w = QComboBox()
        w.addItems(opts)
        w.setCurrentIndex(max(0, w.findText((str(current) or opts[0]).upper())))
        self.inputs[key] = w
        return w

    def _cell(self, label, widget):
        cell = QWidget()
        cell.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(cell)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)
        lbl = QLabel(label)
        lbl.setStyleSheet(
            "font-size: 10px; font-weight: bold; color: #64748b; "
            "letter-spacing: 1px; background: transparent;"
        )
        lay.addWidget(lbl)
        lay.addWidget(widget)
        return cell

    def _build(self, b):
        root = QVBoxLayout(self)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        # Header
        hdr = QWidget()
        hdr.setStyleSheet("background-color: #03192e;")
        hdr.setFixedHeight(68)
        hl = QVBoxLayout(hdr)
        hl.setContentsMargins(20, 10, 20, 10)
        hl.setSpacing(2)
        title_row = QHBoxLayout()
        tl = QLabel(b.get("titulo", "Libro"))
        tl.setWordWrap(True)
        tl.setStyleSheet(
            "font-family: Georgia; font-size: 14px; font-style: italic; "
            "font-weight: bold; color: white; background: transparent;"
        )
        title_row.addWidget(tl, 1)
        if str(b.get("perdido", "NO")).upper() == "SI":
            badge = QLabel("PERDIDO")
            badge.setStyleSheet(
                "color: white; background-color: #7e22ce; border-radius: 2px; "
                "padding: 2px 7px; font-size: 10px; font-weight: bold;"
            )
            title_row.addWidget(badge, 0, Qt.AlignVCenter)
        hl.addLayout(title_row)
        sub = QLabel("Editar campos del registro")
        sub.setStyleSheet("font-size: 11px; color: #fed488; background: transparent;")
        hl.addWidget(sub)
        root.addWidget(hdr)

        # Grid de campos
        body = QWidget()
        body.setStyleSheet("background: #ffffff;")
        gr = QGridLayout(body)
        gr.setContentsMargins(20, 14, 20, 10)
        gr.setHorizontalSpacing(14)
        gr.setVerticalSpacing(10)
        gr.setColumnStretch(0, 1)
        gr.setColumnStretch(1, 1)

        gr.addWidget(self._cell("TITULO *",    self._inp("titulo",      b.get("titulo",""))),     0, 0, 1, 2)
        gr.addWidget(self._cell("AUTOR *",     self._inp("autor",       b.get("autor",""))),      1, 0)
        gr.addWidget(self._cell("EDITORIAL",   self._inp("editorial",   b.get("editorial",""))),  1, 1)
        gr.addWidget(self._cell("CATEGORIA",   self._inp("categoria",   b.get("categoria",""))),  2, 0)
        gr.addWidget(self._cell("COD. REF.",   self._inp("codigo_ref",  b.get("codigo_ref",""))), 2, 1)
        gr.addWidget(self._cell("ISBN",        self._inp("codigo_isbn", b.get("codigo_isbn",""))),3, 0)
        gr.addWidget(self._cell("REFERENCIA",  self._inp("referencia",  b.get("referencia",""))), 3, 1)

        fecha_w = self._inp("fecha", b.get("fecha",""))
        spin = QSpinBox()
        spin.setRange(0, 9999)
        spin.setValue(int(b.get("cantidad", 1) or 1))
        self.inputs["cantidad"] = spin
        gr.addWidget(self._cell("FECHA",      fecha_w), 4, 0)
        gr.addWidget(self._cell("CANTIDAD *", spin),    4, 1)

        gr.addWidget(self._cell("ESTADO",
            self._cmb("estado", ["BUENO","REGULAR","MALO","DETERIORADO"], b.get("estado","BUENO"))), 5, 0)
        gr.addWidget(self._cell("DONADO",
            self._cmb("donado", ["NO","SI"], b.get("donado","NO"))), 5, 1)

        gr.addWidget(self._cell("PERDIDO",
            self._cmb("perdido", ["NO","SI"], b.get("perdido","NO"))), 6, 0)
        prestado_w = self._inp("prestado", b.get("prestado","NO"))
        prestado_w.setPlaceholderText("Nombre o NO")
        gr.addWidget(self._cell("PRESTADO A", prestado_w), 6, 1)

        root.addWidget(body)

        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background: #E8E4D9; max-height: 1px; border: none;")
        root.addWidget(sep)

        # Footer fijo
        ft = QWidget()
        ft.setStyleSheet("background: #f8fafc;")
        ft.setFixedHeight(54)
        fl = QHBoxLayout(ft)
        fl.setContentsMargins(20, 8, 20, 8)
        fl.setSpacing(10)
        fl.addStretch()

        c_btn = QPushButton("CANCELAR")
        c_btn.setCursor(QCursor(Qt.PointingHandCursor))
        c_btn.setStyleSheet(
            "QPushButton { background: transparent; color: #475569; "
            "border: 1px solid #c4c6cd; border-radius: 2px; "
            "padding: 8px 18px; font-size: 12px; font-weight: bold; min-width: 90px; }"
            "QPushButton:hover { background: #f4f3f2; }"
        )
        c_btn.clicked.connect(self.close)

        s_btn = QPushButton("  GUARDAR CAMBIOS  ")
        s_btn.setCursor(QCursor(Qt.PointingHandCursor))
        s_btn.setStyleSheet(
            "QPushButton { background-color: #03192e; color: white; border: none; "
            "border-radius: 2px; padding: 8px 18px; font-size: 12px; "
            "font-weight: bold; min-width: 150px; }"
            "QPushButton:hover { background-color: #1a2e44; }"
            "QPushButton:pressed { background-color: #061d32; }"
        )
        s_btn.clicked.connect(self._save)

        fl.addWidget(c_btn)
        fl.addWidget(s_btn)
        root.addWidget(ft)

    def _v(self, k):
        w = self.inputs.get(k)
        if isinstance(w, QLineEdit): return w.text().strip()
        if isinstance(w, QComboBox): return w.currentText().strip()
        if isinstance(w, QSpinBox):  return w.value()
        return ""

    def _save(self):
        if not self._v("titulo"):
            QMessageBox.warning(self, "Campo requerido", "El titulo es obligatorio.")
            return
        if not self._v("autor"):
            QMessageBox.warning(self, "Campo requerido", "El autor es obligatorio.")
            return
        self.book_updated.emit({
            "id": self.original.get("id"),
            **{k: self._v(k) for k in [
                "titulo","autor","editorial","categoria","codigo_ref",
                "codigo_isbn","referencia","fecha","cantidad","estado",
                "prestado","donado","perdido",
            ]}
        })
        self.accept()

# ══════════════════════════════════════════════════════════════════════════════

COLS = [
    ("ID",        "id"),
    ("Título",    "titulo"),
    ("Categoría", "categoria"),
    ("Editorial", "editorial"),
    ("Código",    "codigo_ref"),
    ("ISBN",      "codigo_isbn"),
    ("Referencia","referencia"),
    ("Cant.",     "cantidad"),
    ("Estado",    "estado"),
    ("Autor",     "autor"),
    ("Prestado",  "prestado"),
    ("Donado",    "donado"),
    ("Perdido",   "perdido"),
    ("",          None),          # columna de acciones
]
MAX_COLLECTION_LOAD = 300


class CollectionSection(QWidget):
    def __init__(self, service=None, parent=None):
        super().__init__(parent)
        self.service = service
        self.loaded_book_ids: list[int] = []
        self.total_books = 0
        self.current_page = 0
        self.page_size = 100  # Carga 100 libros por página
        self._loading = False
        self._search_active = False
        self._build()
        self._load()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 28, 40, 28)
        root.setSpacing(18)

        # Encabezado
        hdr_row = QHBoxLayout()
        left_col = QVBoxLayout()
        left_col.setSpacing(4)

        title = section_title("Inventario CountBooks", size=42)
        self.subtitle = QLabel("Repositorio Activo: 0 volúmenes catalogados")
        self.subtitle.setStyleSheet(
            f"font-family: '{FONT_SERIF}'; font-size: 16px; font-style: italic; "
            f"color: {C_TEXT_MUTED}; background: transparent;"
        )
        left_col.addWidget(title)
        left_col.addWidget(self.subtitle)

        self.btn_show_all = QPushButton("Ver catálogo completo")
        self.btn_show_all.setObjectName("btn_purple")
        self.btn_show_all.setVisible(False)
        self.btn_show_all.setFixedHeight(36)
        self.btn_show_all.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_show_all.clicked.connect(self._show_full_collection)

        hdr_row.addLayout(left_col)
        hdr_row.addStretch()
        hdr_row.addWidget(self.btn_show_all)
        root.addLayout(hdr_row)

        # Tabla + panel detalle
        body_row = QHBoxLayout()
        body_row.setSpacing(20)

        self.table = self._make_table()
        body_row.addWidget(self.table, 1)

        self.detail_panel = self._make_detail_panel()
        body_row.addWidget(self.detail_panel)

        root.addLayout(body_row, 1)

        # Stats pie
        stats_row = QHBoxLayout()
        stats_row.setSpacing(48)

        for attr, label in [
            ("lbl_prestados", "PRÉSTAMOS ACTIVOS"),
            ("lbl_perdidos",  "LIBROS PERDIDOS"),
        ]:
            lbl_num = QLabel("0")
            lbl_num.setStyleSheet(
                f"font-family: '{FONT_SERIF}'; font-size: 28px; font-weight: bold; "
                f"color: {C_PRIMARY}; background: transparent;"
            )
            setattr(self, attr, lbl_num)
            col = QVBoxLayout()
            col.setSpacing(2)
            col.addWidget(lbl_num)
            sub = QLabel(label)
            sub.setStyleSheet(
                f"font-size: 10px; color: {C_SLATE_500}; letter-spacing: 1px; background: transparent;"
            )
            col.addWidget(sub)
            stats_row.addLayout(col)

        stats_row.addStretch()
        root.addLayout(stats_row)

    def _make_table(self) -> QTableWidget:
        t = QTableWidget()

        t.setColumnCount(len(COLS))
        t.setHorizontalHeaderLabels([c[0] for c in COLS])

        t.setEditTriggers(QAbstractItemView.NoEditTriggers)

        t.setSelectionBehavior(QAbstractItemView.SelectRows)
        t.setSelectionMode(QAbstractItemView.SingleSelection)

        t.verticalHeader().setVisible(False)

        # HEADER
        header = t.horizontalHeader()

        header.setStretchLastSection(False)

        # evita columnas demasiado pequeñas
        header.setMinimumSectionSize(80)

        # ID
        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        # TITULO (columna principal)
        header.setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        # ancho inicial del título
        t.setColumnWidth(1, 420)

        # RESTO DE COLUMNAS
        for i in range(2, len(COLS)):
            header.setSectionResizeMode(
                i,
                QHeaderView.ResizeToContents
            )

        # OPTIMIZACIONES
        t.setWordWrap(False)

        t.setSortingEnabled(False)

        t.setAlternatingRowColors(False)

        t.setShowGrid(True)

        # estilo del header
        t.setStyleSheet(f"""
            QHeaderView::section {{
                background-color: {C_PRIMARY};
                color: white;
                padding: 8px;
                border: none;
                font-size: 11px;
                font-weight: bold;
            }}

            QTableWidget {{
                gridline-color: #d9dee7;
                font-size: 12px;
            }}
        """)

        t.itemSelectionChanged.connect(
            self._on_row_selected
        )

        # Scroll dinámico para cargar más libros cuando se acerca al final
        t.verticalScrollBar().valueChanged.connect(self._on_scroll)

        return t


    def _make_detail_panel(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("detail_panel")
        panel.setFixedWidth(268)
        self._dp_lay = QVBoxLayout(panel)
        self._dp_lay.setContentsMargins(0, 0, 0, 0)
        self._dp_lay.setSpacing(0)
        self._dp_placeholder()
        return panel

    def _dp_placeholder(self):
        self._dp_clear()
        lbl = QLabel("Selecciona una fila\npara ver el detalle")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet(
            f"color: {C_TEXT_LIGHT}; font-size: 13px; font-style: italic; "
            f"padding: 40px 16px; background: transparent;"
        )
        self._dp_lay.addWidget(lbl)
        self._dp_lay.addStretch()

    def _dp_clear(self):
        while self._dp_lay.count():
            c = self._dp_lay.takeAt(0)
            if c.widget():
                c.widget().deleteLater()

    def _load(self):
        """Carga la primera página de libros."""
        if self.service:
            self.total_books = self.service.count_books()
            raw = self.service.get_books_paginated(offset=0, limit=self.page_size)
            books = [b.a_book() for b in raw] if raw else []
            self.loaded_book_ids = [b.get("id") for b in books]
        else:
            books = _demo_books()
            self.total_books = len(books)
            self.loaded_book_ids = [b.get("id") for b in books]

        self.current_page = 1
        self._search_active = False
        self._fill_table(books)
    
    def _load_more(self):
        """Carga más libros (página siguiente)."""
        if self._loading or not self.service:
            return
        
        if len(self.loaded_book_ids) >= self.total_books:
            return  # Ya cargamos todos
        
        self._loading = True
        offset = len(self.loaded_book_ids)
        raw = self.service.get_books_paginated(offset=offset, limit=self.page_size)
        
        if raw:
            new_books = [b.a_book() for b in raw]
            self._append_table(new_books)
            self.loaded_book_ids.extend([b.get("id") for b in new_books])
            self.current_page += 1
        
        self._loading = False

    def _show_full_collection(self):
        """Vuelve a la vista normal de la colección tras una búsqueda."""
        self._search_active = False
        self.loaded_book_ids.clear()
        self.current_page = 0
        self._load()

    def _load_until_offset(self, target_offset: int):
        """Carga páginas hasta que el registro esté incluido en la colección."""
        if not self.service:
            return

        while len(self.loaded_book_ids) <= target_offset and len(self.loaded_book_ids) < self.total_books:
            self._load_more()
            if self._loading:
                break

    def _on_scroll(self):
        """Detecta cuando el usuario llega al final del scroll para cargar más."""
        if not self.service or self._loading or self._search_active:
            return

        scrollbar = self.table.verticalScrollBar()
        if scrollbar.maximum() <= 0:
            return
        if scrollbar.value() >= scrollbar.maximum() - scrollbar.pageStep():
            self._load_more()

    def _fill_table(self, books: list):
        """Limpia la tabla y la llena desde cero (usado en carga inicial)."""
        self.table.setUpdatesEnabled(False)
        self.table.setRowCount(0)
        prestados = 0
        perdidos  = 0
        self.table.setRowCount(len(books))

        for row, book in enumerate(books):
            for col, (_, key) in enumerate(COLS):
                if key is None:
                    btn = QPushButton("EDITAR")
                    btn.setObjectName("btn_ghost")
                    btn.setFixedHeight(24)
                    btn.setCursor(QCursor(Qt.PointingHandCursor))
                    btn.clicked.connect(
                        lambda _, book_id=book.get("id"): self._open_edit(book_id)
                    )
                    cell = QWidget()
                    cl = QHBoxLayout(cell)
                    cl.setContentsMargins(4, 2, 4, 2)
                    cl.addWidget(btn)
                    self.table.setCellWidget(row, col, cell)
                else:
                    val = book.get(key, "")
                    item = QTableWidgetItem(
                        str(val) if val is not None else "—"
                    )
                    if col == 0:
                        item.setData(Qt.UserRole, book.get("id"))
                    if key == "estado":
                        e = str(val).upper()
                        if e == "BUENO":
                            item.setForeground(QColor(C_GREEN_700))
                            item.setText(f"• {e}")
                        elif e in ("MALO", "DETERIORADO"):
                            item.setForeground(QColor(C_ERROR))
                            item.setText(f"• {e}")
                        else:
                            item.setForeground(QColor(C_WARN))
                            item.setText(f"• {e}")
                    if key == "prestado":
                        if val and str(val).upper() != "NO":
                            item.setBackground(QColor(C_WARN_BG))
                            item.setForeground(QColor(C_WARN))
                            prestados += 1
                    if key == "perdido":
                        if str(val).upper() == "SI":
                            item.setBackground(QColor(C_PURPLE_50))
                            item.setForeground(QColor(C_PURPLE_700))
                            item.setText("• SI")
                            perdidos += 1
                        else:
                            item.setText("• NO")
                            item.setForeground(QColor(C_TEXT_LIGHT))
                    self.table.setItem(row, col, item)

        loaded_count = len(books)
        if self._search_active:
            self.subtitle.setText(f"Mostrando {loaded_count} de {self.total_books} resultados — filtro de búsqueda")
        elif self.service and self.total_books > self.page_size:
            self.subtitle.setText(f"Mostrando {loaded_count} de {self.total_books} volúmenes (scroll para cargar más)")
        else:
            self.subtitle.setText(f"Repositorio Activo: {loaded_count} volúmenes catalogados")

        if hasattr(self, 'btn_show_all'):
            self.btn_show_all.setVisible(self._search_active)

        total_prestados = self.service.count_books_prestados() if self.service else prestados
        total_perdidos = self.service.count_books_perdidos() if self.service else perdidos
        self.lbl_prestados.setText(str(total_prestados))
        self.lbl_perdidos.setText(str(total_perdidos))
        self.table.setUpdatesEnabled(True)

    def _append_table(self, books: list):
        """Añade libros al final de la tabla (usado en lazy loading)."""
        current_rows = self.table.rowCount()
        self.table.setUpdatesEnabled(False)
        self.table.setRowCount(current_rows + len(books))

        for row, book in enumerate(books, start=current_rows):
            for col, (_, key) in enumerate(COLS):
                if key is None:
                    btn = QPushButton("EDITAR")
                    btn.setObjectName("btn_ghost")
                    btn.setFixedHeight(24)
                    btn.setCursor(QCursor(Qt.PointingHandCursor))
                    btn.clicked.connect(
                        lambda _, book_id=book.get("id"): self._open_edit(book_id)
                    )
                    cell = QWidget()
                    cl = QHBoxLayout(cell)
                    cl.setContentsMargins(4, 2, 4, 2)
                    cl.addWidget(btn)
                    self.table.setCellWidget(row, col, cell)
                else:
                    val = book.get(key, "")
                    item = QTableWidgetItem(
                        str(val) if val is not None else "—"
                    )
                    if col == 0:
                        item.setData(Qt.UserRole, book.get("id"))
                    if key == "estado":
                        e = str(val).upper()
                        if e == "BUENO":
                            item.setForeground(QColor(C_GREEN_700))
                            item.setText(f"• {e}")
                        elif e in ("MALO", "DETERIORADO"):
                            item.setForeground(QColor(C_ERROR))
                            item.setText(f"• {e}")
                        else:
                            item.setForeground(QColor(C_WARN))
                            item.setText(f"• {e}")
                    if key == "prestado":
                        if val and str(val).upper() != "NO":
                            item.setBackground(QColor(C_WARN_BG))
                            item.setForeground(QColor(C_WARN))
                    if key == "perdido":
                        if str(val).upper() == "SI":
                            item.setBackground(QColor(C_PURPLE_50))
                            item.setForeground(QColor(C_PURPLE_700))
                            item.setText("• SI")
                        else:
                            item.setText("• NO")
                            item.setForeground(QColor(C_TEXT_LIGHT))
                    self.table.setItem(row, col, item)

        loaded_count = self.table.rowCount()
        if self.service and self.total_books > self.page_size:
            self.subtitle.setText(f"Mostrando {loaded_count} de {self.total_books} volúmenes (scroll para cargar más)")
        else:
            self.subtitle.setText(f"Repositorio Activo: {loaded_count} volúmenes catalogados")

        self.table.setUpdatesEnabled(True)

    def _render_detail(self, b: dict):
        self._dp_clear()

        hdr = QWidget()
        hdr.setStyleSheet(f"background-color: {C_PRIMARY};")
        hl = QVBoxLayout(hdr)
        hl.setContentsMargins(14, 14, 14, 14)
        hl.setSpacing(6)

        title_row = QHBoxLayout()
        tl = QLabel(b.get("titulo","—"))
        tl.setWordWrap(True)
        tl.setStyleSheet(
            f"font-family: '{FONT_SERIF}'; font-size: 14px; font-style: italic; "
            f"font-weight: bold; color: white; background: transparent;"
        )
        title_row.addWidget(tl, 1)
        if str(b.get("perdido","NO")).upper() == "SI":
            p_badge = QLabel("PERDIDO")
            p_badge.setStyleSheet(
                f"color: white; background-color: {C_PURPLE_700}; "
                f"border-radius: 2px; padding: 2px 6px; font-size: 9px; font-weight: bold;"
            )
            title_row.addWidget(p_badge, 0, Qt.AlignTop)
        hl.addLayout(title_row)

        al = QLabel(b.get("autor","—"))
        al.setStyleSheet(f"font-size: 11px; color: {C_ACCENT_LIGHT}; background: transparent;")
        hl.addWidget(al)
        self._dp_lay.addWidget(hdr)

        body = QWidget()
        body.setStyleSheet(f"background: {C_SURFACE};")
        bl = QVBoxLayout(body)
        bl.setContentsMargins(14, 14, 14, 14)
        bl.setSpacing(8)

        for lbl_t, val in [
            ("Editorial",   b.get("editorial","—")),
            ("Categoría",   b.get("categoria","—")),
            ("Cód. ref.",   b.get("codigo_ref","—")),
            ("ISBN",        b.get("codigo_isbn","—")),
            ("Referencia",  b.get("referencia","—")),
            ("Cantidad",    str(b.get("cantidad","—"))),
            ("Estado",      b.get("estado","—")),
            ("Prestado a",  b.get("prestado","NO")),
            ("Donado",      b.get("donado","NO")),
            ("Perdido",     b.get("perdido","NO")),
            ("Fecha",       b.get("fecha","—")),
        ]:
            rw = QHBoxLayout()
            rw.setSpacing(6)
            lbl = QLabel(lbl_t)
            lbl.setStyleSheet(
                f"font-size: 11px; font-weight: bold; color: {C_SLATE_500}; "
                f"min-width: 72px; background: transparent;"
            )
            display_val = val if val else "—"
            vl = QLabel(display_val)
            vl.setWordWrap(True)

            # Color especial para perdido = SI
            if lbl_t == "Perdido" and str(val).upper() == "SI":
                vl.setStyleSheet(f"font-size: 12px; color: {C_PURPLE_700}; font-weight: bold; background: transparent;")
            elif lbl_t == "Prestado a" and str(val).upper() not in ("NO", "—", ""):
                vl.setStyleSheet(f"font-size: 12px; color: {C_WARN}; background: transparent;")
            else:
                vl.setStyleSheet(f"font-size: 12px; color: {C_TEXT}; background: transparent;")

            rw.addWidget(lbl)
            rw.addWidget(vl, 1)
            bl.addLayout(rw)

        self._dp_lay.addWidget(body, 1)

    def show_book(self, book: dict):
        self._render_detail(book)
        target_id = book.get("id")
        if target_id is None:
            return

        if target_id not in self.loaded_book_ids:
            self._search_active = True
            if self.service:
                model = self.service.get_book_by_id(target_id)
                if model:
                    self._fill_table([model.a_book()])
                else:
                    self._fill_table([book])
            else:
                self._fill_table([book])

        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.data(Qt.UserRole) == target_id:
                self.table.selectRow(row)
                self.table.scrollToItem(item)
                break

    def _on_row_selected(self):
        items = self.table.selectedItems()
        if not items:
            return
        book_id = items[0].data(Qt.UserRole)
        if not book_id:
            return
        if self.service:
            model = self.service.get_book_by_id(book_id)
            if not model:
                return
            book = model.a_book()
        else:
            book = next((b for b in _demo_books() if b.get("id") == book_id), None)
            if not book:
                return
        self._render_detail(book)

    def _open_edit(self, book_id: int):
        if self.service:
            model = self.service.get_book_by_id(book_id)
            if model:
                book = model.a_book()
            else:
                return
        else:
            book = next((b for b in _demo_books() if b.get("id") == book_id), None)
            if not book:
                return

        if hasattr(self, "_edit_modal") and self._edit_modal is not None:
            try:
                self._edit_modal.close()
            except Exception:
                pass
        modal = EditBookModal(book, parent=None)  # sin parent para no bloquear
        modal.book_updated.connect(self._on_updated)
        modal.setWindowModality(Qt.NonModal)
        modal.show()
        modal.raise_()
        modal.activateWindow()
        self._edit_modal = modal

    def _on_updated(self, updated: dict):
        """Actualiza la colección cuando se edita un libro."""
        if self.service:
            try:
                from src.models.bookModel import BookModel

                m = BookModel(
                    **{
                        k: v
                        for k, v in updated.items()
                        if k != "id"
                    }
                )

                self.service.update_book(updated["id"], m)

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    str(e)
                )
                return

        self.refresh_collection()
        self._render_detail(updated)
    
    def refresh_collection(self):
        """Recarga la colección desde cero (útil después de importar datos)."""
        self.loaded_book_ids.clear()
        self.current_page = 0
        self._search_active = False
        self._load()


# ══════════════════════════════════════════════════════════════════════════════
# Sección 2 — Añadir libro
# ══════════════════════════════════════════════════════════════════════════════

class AddBookSection(QWidget):
    book_saved = Signal()  # se emite tras guardar exitosamente
    def __init__(self, service=None, parent=None):
        super().__init__(parent)
        self.service = service
        self.inputs = {}
        self._build()

    def _input_col(self, key: str, label: str, placeholder: str = "",
                   widget=None) -> QVBoxLayout:
        col = QVBoxLayout()
        col.setSpacing(5)
        col.addWidget(field_label(label))
        if widget is None:
            w = QLineEdit()
            w.setObjectName("form_input")
            w.setPlaceholderText(placeholder)
        else:
            w = widget
        self.inputs[key] = w
        col.addWidget(w)
        return col

    def _build(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        cont = QWidget()
        root = QVBoxLayout(cont)
        root.setContentsMargins(40, 28, 40, 32)
        root.setSpacing(20)

        # Encabezado
        root.addWidget(section_title("Añadir Nuevo Volumen"))
        sub = QLabel(
            "Complete los detalles para integrar el libro en el inventario permanente de CountBooks."
        )
        sub.setStyleSheet(f"font-size: 13px; color: {C_TEXT_MUTED}; background: transparent;")
        root.addWidget(sub)
        root.addWidget(sep_line())

        # Guía
        g_card, g_hdr, g_body = make_card()
        g_hdr.addWidget(card_header_label("GUÍA DE CATALOGACIÓN LOCAL"))
        g_txt = QLabel(
            "• Use el título completo del folio original.     "
            "• Las etiquetas ayudan en la recuperación rápida.\n"
            "• Los datos se guardarán en la base de datos local del sistema."
        )
        g_txt.setStyleSheet(f"font-size: 12px; color: {C_SLATE_600}; background: transparent;")
        g_body.addWidget(g_txt)
        root.addWidget(g_card)

        # Card bibliográfica
        b_card, b_hdr, b_body = make_card()
        b_hdr.addWidget(card_header_label("INFORMACIÓN BIBLIOGRÁFICA"))
        gr1 = QGridLayout()
        gr1.setSpacing(16)
        gr1.addLayout(self._input_col("titulo",    "TÍTULO *",   "Ej: Cien años de soledad"), 0, 0, 1, 3)
        gr1.addLayout(self._input_col("autor",     "AUTOR *",    "Gabriel García Márquez"),   1, 0)
        gr1.addLayout(self._input_col("editorial", "EDITORIAL",  "No tiene"),                 1, 1)
        b_body.addLayout(gr1)
        root.addWidget(b_card)

        # Card clasificación
        c_card, c_hdr, c_body = make_card()
        c_hdr.addWidget(card_header_label("CLASIFICACIÓN Y CONTROL"))
        gr2 = QGridLayout()
        gr2.setSpacing(16)
        gr2.addLayout(self._input_col("categoria",   "CATEGORÍA",  "No tiene"), 0, 0)
        gr2.addLayout(self._input_col("codigo_ref",  "CÓDIGO",     "No tiene"), 0, 1)
        gr2.addLayout(self._input_col("codigo_isbn", "ISBN",       "No tiene"), 0, 2)
        gr2.addLayout(self._input_col("referencia",  "REFERENCIA", "No tiene"), 1, 0)

        spin = QSpinBox()
        spin.setObjectName("form_spin")
        spin.setRange(1, 9999)
        spin.setValue(1)
        self.inputs["cantidad"] = spin
        gr2.addLayout(self._input_col("cantidad", "CANTIDAD", widget=spin), 1, 1)

        estado_cb = QComboBox()
        estado_cb.setObjectName("form_combo")
        estado_cb.addItems(["BUENO","REGULAR","MALO","DETERIORADO"])
        self.inputs["estado"] = estado_cb
        gr2.addLayout(self._input_col("estado", "ESTADO", widget=estado_cb), 1, 2)

        donado_cb = QComboBox()
        donado_cb.setObjectName("form_combo")
        donado_cb.addItems(["NO","SI"])
        self.inputs["donado"] = donado_cb
        gr2.addLayout(self._input_col("donado", "DONADO", widget=donado_cb), 2, 0)

        perdido_cb = QComboBox()
        perdido_cb.setObjectName("form_combo")
        perdido_cb.addItems(["NO","SI"])
        self.inputs["perdido"] = perdido_cb
        gr2.addLayout(self._input_col("perdido", "PERDIDO", widget=perdido_cb), 2, 1)

        gr2.addLayout(self._input_col("prestado", "PRESTADO A (NOMBRE O NO)", "NO"), 2, 2)
        gr2.addLayout(self._input_col("fecha", "FECHA (AAAA-MM-DD)", ""), 3, 0)

        c_body.addLayout(gr2)
        root.addWidget(c_card)
        root.addWidget(sep_line())

        act = QHBoxLayout()
        act.addStretch()
        cancel_btn = QPushButton("CANCELAR")
        cancel_btn.setObjectName("btn_ghost")
        cancel_btn.clicked.connect(self._reset)
        save_btn = QPushButton("GUARDAR LIBRO")
        save_btn.setObjectName("btn_primary")
        save_btn.clicked.connect(self._save)
        act.addWidget(cancel_btn)
        act.addSpacing(10)
        act.addWidget(save_btn)
        root.addLayout(act)
        root.addStretch()

        scroll.setWidget(cont)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def _get(self, k):
        w = self.inputs.get(k)
        if isinstance(w, QLineEdit): return w.text().strip()
        if isinstance(w, QComboBox): return w.currentText().strip()
        if isinstance(w, QSpinBox):  return w.value()
        return ""

    def _reset(self):
        for w in self.inputs.values():
            if isinstance(w, QLineEdit): w.clear()
            elif isinstance(w, QComboBox): w.setCurrentIndex(0)
            elif isinstance(w, QSpinBox): w.setValue(1)

    def _save(self):
        if not self._get("titulo"):
            QMessageBox.warning(self, "Requerido", "El título es obligatorio.")
            return
        if not self._get("autor"):
            QMessageBox.warning(self, "Requerido", "El autor es obligatorio.")
            return
        if self.service:
            try:
                from src.models.bookModel import BookModel
                m = BookModel(**{k: self._get(k) for k in self.inputs})
                ok, err = self.service.add_book(m)
                if not ok:
                    QMessageBox.critical(self, "Error", err)
                    return
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                return
        titulo = self._get("titulo")
        QMessageBox.information(self, "Libro guardado",
            f"\"{titulo}\" fue agregado al inventario correctamente.")
        self._reset()
        self.book_saved.emit()


# ══════════════════════════════════════════════════════════════════════════════
# Sección 3 — Gestor de datos
# ══════════════════════════════════════════════════════════════════════════════

from PySide6.QtCore import QThread


class ImportWorker(QThread):
    progress = Signal(int)
    finished = Signal(dict)
    error    = Signal(str)

    def __init__(self, db_path, ruta):
        super().__init__()
        self.db_path = db_path   # solo la ruta, NO el objeto Database
        self.ruta    = ruta

    def run(self):
        try:
            from src.utils.excel import leer_excel
            from src.database.database import Database
            from src.repository.bookRepo import BookRepo
            from src.services.bookServices import BookService

            # Crear conexion propia dentro de este hilo
            db      = Database(self.db_path)
            repo    = BookRepo(db)
            service = BookService(repo)

            libros = leer_excel(self.ruta)
            self.progress.emit(50)
            result = service.add_books_from_excel(libros)
            self.progress.emit(100)
            db.close()
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class DataManagerSection(QWidget):
    data_imported = Signal(dict)

    def __init__(self, service=None, parent=None):
        super().__init__(parent)
        self.service = service
        self.import_path = None
        self._build()

    def _build(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        cont = QWidget()
        root = QVBoxLayout(cont)
        root.setContentsMargins(40, 28, 40, 32)
        root.setSpacing(20)

        root.addWidget(section_title("Gestión de Datos"))
        sub = QLabel(
            "Sincronice su colección física con nuestra infraestructura digital de precisión. "
            "Herramientas avanzadas para la preservación y exportación de metadatos académicos."
        )
        sub.setWordWrap(True)
        sub.setStyleSheet(f"font-size: 13px; color: {C_TEXT_MUTED}; background: transparent;")
        root.addWidget(sub)
        root.addWidget(sep_line())

        # ─── Card importar ───
        imp, imp_hdr, imp_body = make_card()
        imp_hdr.addWidget(card_header_label("IMPORT FROM EXCEL"))
        imp_desc = QLabel(
            "Suba archivos .xlsx o .csv con el esquema estandarizado de la biblioteca."
        )
        imp_desc.setStyleSheet(f"font-size: 13px; color: {C_TEXT_MUTED}; background: transparent;")
        imp_body.addWidget(imp_desc)

        drop = QWidget()
        drop.setStyleSheet(
            f"border: 2px dashed {C_BORDER}; background-color: {C_BG}; border-radius: 2px;"
        )
        drop.setMinimumHeight(130)
        dl = QVBoxLayout(drop)
        dl.setAlignment(Qt.AlignCenter)
        dl.setSpacing(6)
        self.import_name_lbl = QLabel("Drag and drop file here")
        self.import_name_lbl.setAlignment(Qt.AlignCenter)
        self.import_name_lbl.setStyleSheet(
            f"font-size: 13px; font-weight: bold; color: {C_PRIMARY}; "
            f"background: transparent; border: none;"
        )
        drop_hint = QLabel("or click to browse local directory")
        drop_hint.setAlignment(Qt.AlignCenter)
        drop_hint.setStyleSheet(
            f"font-size: 12px; color: {C_TEXT_LIGHT}; background: transparent; border: none;"
        )
        sel_btn = QPushButton("SELECT FILE")
        sel_btn.setObjectName("btn_primary")
        sel_btn.setCursor(QCursor(Qt.PointingHandCursor))
        sel_btn.clicked.connect(self._select_file)
        dl.addWidget(self.import_name_lbl)
        dl.addWidget(drop_hint)
        dl.addSpacing(8)
        dl.addWidget(sel_btn, 0, Qt.AlignCenter)
        imp_body.addWidget(drop)

        schema = QLabel(
            "Columnas soportadas: titulo, autor, cantidad, categoria, editorial, "
            "codigo_ref, codigo_isbn, referencia, estado, prestado, donado, fecha, perdido"
        )
        schema.setWordWrap(True)
        schema.setStyleSheet(
            f"font-size: 11px; color: {C_TEXT_LIGHT}; font-style: italic; background: transparent;"
        )
        imp_body.addWidget(schema)

        self.import_btn = QPushButton("IMPORTAR LIBROS")
        self.import_btn.setObjectName("btn_secondary")
        self.import_btn.setEnabled(False)
        self.import_btn.clicked.connect(self._run_import)
        imp_body.addWidget(self.import_btn)

        self.import_progress = QProgressBar()
        self.import_progress.setVisible(False)
        self.import_progress.setMaximumHeight(4)
        self.import_progress.setTextVisible(False)
        self.import_progress.setStyleSheet(
            f"QProgressBar {{ border: none; background: {C_BG_ALT}; border-radius: 2px; }}"
            f"QProgressBar::chunk {{ background: {C_PRIMARY}; border-radius: 2px; }}"
        )
        imp_body.addWidget(self.import_progress)
        root.addWidget(imp)

        # ─── Card exportar ───
        exp, exp_hdr, exp_body = make_card()
        exp_hdr.addWidget(card_header_label("EXPORT LIBRARY"))
        exp_hdr.addStretch()
        exp_btn = QPushButton("EXPORTAR EXCEL")
        exp_btn.setObjectName("btn_primary")
        exp_btn.clicked.connect(self._run_export)
        exp_hdr.addWidget(exp_btn)

        exp_desc = QLabel(
            "Genera un archivo Excel (.xlsx) con todos los registros del inventario. "
            "El archivo puede reimportarse directamente a CountBooks."
        )
        exp_desc.setWordWrap(True)
        exp_desc.setStyleSheet(
            f"font-size: 13px; color: {C_TEXT_MUTED}; background: transparent;"
        )
        exp_body.addWidget(exp_desc)

        # Indicador de formato fijo
        fmt_row = QHBoxLayout()
        fmt_row.setSpacing(10)
        fmt_icon = QLabel("✓")
        fmt_icon.setStyleSheet(f"font-size: 14px; color: {C_GREEN_700}; background: transparent;")
        fmt_lbl = QLabel("Excel Spreadsheet (.xlsx)")
        fmt_lbl.setStyleSheet(f"font-size: 13px; color: {C_TEXT}; background: transparent;")
        fmt_row.addWidget(fmt_icon)
        fmt_row.addWidget(fmt_lbl)
        fmt_row.addStretch()
        exp_body.addLayout(fmt_row)
        root.addWidget(exp)

        root.addStretch()

        scroll.setWidget(cont)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def _select_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo", "",
            "Excel / CSV (*.xlsx *.xls *.csv)"
        )
        if path:
            self.import_path = path
            self.import_name_lbl.setText(os.path.basename(path))
            self.import_btn.setEnabled(True)

    def _run_import(self):
        if not self.import_path or not self.service:
            return
        self.import_btn.setEnabled(False)
        self.import_progress.setVisible(True)

        # Pasamos db_path para que el worker cree su propia conexion en su hilo
        from src.database.database import DB_PATH
        self._worker = ImportWorker(DB_PATH, self.import_path)
        self._worker.progress.connect(self.import_progress.setValue)
        self._worker.finished.connect(self._on_import_done)
        self._worker.error.connect(lambda e: (
            QMessageBox.critical(self, "Error de importación", e),
            self.import_btn.setEnabled(True),
        ))
        self._worker.start()

    def _on_import_done(self, result):
        self.import_btn.setEnabled(True)
        msg = (
            f"Importación completada.\n\n"
            f"✔ Exitosos: {result['exitosos']}\n"
            f"✘ Fallidos: {result['fallidos']}"
        )
        if result["fallidos"] > 0:
            errores_str = "\n".join(
                f"  Fila {e['fila']}: {e['titulo']} — {e['error']}"
                for e in result["errores"][:5]
            )
            msg += f"\n\nPrimeros errores:\n{errores_str}"
        QMessageBox.information(self, "Importación completada", msg)
        self.data_imported.emit(result)

    def _run_export(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar biblioteca", "inventario_countbooks.xlsx",
            "Excel (*.xlsx)"
        )
        if not path:
            return
        if self.service:
            try:
                from src.utils.excel import exportar_excel
                libros = self.service.get_books()
                exportar_excel(libros, path)
                QMessageBox.information(self, "Exportación completada",
                    f"Archivo guardado en:\n{path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.information(self, "Demo", f"Exportación simulada:\n{path}")


# ══════════════════════════════════════════════════════════════════════════════
# Datos demo
# ══════════════════════════════════════════════════════════════════════════════

def _demo_books() -> list:
    return [
        {
            "id": 1, "titulo": "Cien años de soledad", "autor": "Gabriel García Márquez",
            "editorial": "Sudamericana", "categoria": "Literatura", "codigo_ref": "LIT-001",
            "codigo_isbn": "978-0060883287", "referencia": "FIC-A1-01", "cantidad": 4,
            "estado": "BUENO", "prestado": "NO", "donado": "NO", "fecha": "2020-01-15",
            "perdido": "NO",
        },
        {
            "id": 2, "titulo": "El Principito", "autor": "Antoine de Saint-Exupéry",
            "editorial": "Salamandra", "categoria": "Infantil", "codigo_ref": "INF-003",
            "codigo_isbn": "978-8498381498", "referencia": "FIC-B2-03", "cantidad": 8,
            "estado": "REGULAR", "prestado": "Juan Pérez", "donado": "SI",
            "fecha": "2019-05-20", "perdido": "NO",
        },
        {
            "id": 3, "titulo": "Sapiens: De animales a dioses", "autor": "Yuval Noah Harari",
            "editorial": "Debate", "categoria": "Historia", "codigo_ref": "HIS-012",
            "codigo_isbn": "978-8499924212", "referencia": "HIS-C3-12", "cantidad": 2,
            "estado": "BUENO", "prestado": "NO", "donado": "NO", "fecha": "2021-03-10",
            "perdido": "NO",
        },
        {
            "id": 4, "titulo": "Estructuras de datos en Python", "autor": "Lee & Hubbard",
            "editorial": "O'Reilly", "categoria": "Tecnología", "codigo_ref": "TEC-007",
            "codigo_isbn": "978-1449367879", "referencia": "TEC-D4-07", "cantidad": 3,
            "estado": "MALO", "prestado": "NO", "donado": "NO", "fecha": "2018-11-01",
            "perdido": "SI",
        },
        {
            "id": 5, "titulo": "Don Quijote de la Mancha", "autor": "Miguel de Cervantes",
            "editorial": "Alfaguara", "categoria": "Literatura", "codigo_ref": "LIT-002",
            "codigo_isbn": "978-8420412146", "referencia": "FIC-A1-02", "cantidad": 6,
            "estado": "DETERIORADO", "prestado": "María López", "donado": "NO",
            "fecha": "2015-07-22", "perdido": "NO",
        },
    ]


# ══════════════════════════════════════════════════════════════════════════════
# Ventana principal
# ══════════════════════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    def __init__(self, service=None):
        super().__init__()
        self.service = service
        self.setWindowTitle("CountBooks")
        self.setMinimumSize(1280, 780)
        self.setStyleSheet(QSS)
        self._build()
        self._nav_to(0)

    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(self._sidebar())
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setSpacing(0)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.addWidget(self._topbar())
        rl.addWidget(self._stack(), 1)
        root.addWidget(right, 1)

    def _sidebar(self) -> QWidget:
        sb = QWidget()
        sb.setObjectName("sidebar")
        lay = QVBoxLayout(sb)
        lay.setContentsMargins(0, 28, 0, 28)
        lay.setSpacing(0)

        brand = QWidget()
        brand.setStyleSheet("background: transparent;")
        bl = QVBoxLayout(brand)
        bl.setContentsMargins(24, 0, 24, 36)
        bl.setSpacing(2)
        t = QLabel("CountBooks")
        t.setObjectName("brand_title")
        s = QLabel("Archival Services")
        s.setObjectName("brand_sub")
        bl.addWidget(t)
        bl.addWidget(s)
        lay.addWidget(brand)

        self.nav_btns = []
        for i, text in enumerate(["Colección", "Añadir libro", "Gestor de datos"]):
            btn = QPushButton(text)
            btn.setObjectName("nav_btn")
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.clicked.connect(lambda _, idx=i: self._nav_to(idx))
            self.nav_btns.append(btn)
            lay.addWidget(btn)

        lay.addStretch()

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"background: {C_BORDER}; max-height: 1px; margin: 0 20px;")
        lay.addWidget(line)
        lay.addSpacing(12)

        status = QLabel("SYSTEM STATUS: OPTIMAL")
        status.setObjectName("status_lbl")
        lay.addWidget(status)
        return sb

    def _topbar(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("topbar")
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(28, 0, 28, 0)
        lay.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_input")
        self.search_input.setPlaceholderText("Search archive...")
        self.search_input.returnPressed.connect(self._on_search)
        lay.addWidget(self.search_input)

        search_btn = QPushButton("Buscar")
        search_btn.setObjectName("btn_primary")
        search_btn.clicked.connect(self._on_search)
        lay.addWidget(search_btn)
        lay.addStretch()

        export_btn = QPushButton("Export Library")
        export_btn.setObjectName("btn_secondary")
        export_btn.clicked.connect(lambda: self._nav_to(2))
        lay.addWidget(export_btn)
        return bar

    def _stack(self) -> QStackedWidget:
        self.stack = QStackedWidget()
        self.sec_collection   = CollectionSection(service=self.service)
        self.sec_add_book     = AddBookSection(service=self.service)
        self.sec_data_manager = DataManagerSection(service=self.service)
        for sec in [self.sec_collection, self.sec_add_book, self.sec_data_manager]:
            self.stack.addWidget(sec)
        # Al guardar un libro -> recargar coleccion y navegar a ella
        self.sec_add_book.book_saved.connect(self._on_book_saved)
        self.sec_data_manager.data_imported.connect(self._on_data_imported)
        return self.stack

    def _nav_to(self, idx: int):
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self.nav_btns):
            btn.setProperty("active", i == idx)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _on_book_saved(self):
        self.sec_collection.refresh_collection()
        self._nav_to(0)

    def _on_data_imported(self, result: dict):
        self.sec_collection.refresh_collection()
        self._nav_to(0)

    def _on_search(self):
        query = self.search_input.text().strip()
        if not query:
            return
        if self.service:
            raw = self.service.search_books(query)
            results = [b.a_book() for b in raw] if raw else []
        else:
            q = query.lower()
            results = [
                b for b in _demo_books()
                if any(q in str(b.get(k,"")).lower()
                       for k in ["titulo","autor","codigo_isbn","categoria","editorial"])
            ]
        modal = SearchModal(results, query, parent=self)
        modal.book_selected.connect(self._on_book_from_search)
        modal.exec()

    def _on_book_from_search(self, book: dict):
        self._nav_to(0)
        self.sec_collection.show_book(book)


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

def run_app(service=None):
    app = QApplication.instance() or QApplication(sys.argv)
    w = MainWindow(service=service)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()