import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QFrame, QLabel, QLineEdit, QTextEdit, 
                             QPushButton, QComboBox, QScrollArea, QGridLayout, 
                             QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor, QCursor

class ScriptoriumApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scriptorium - Archival Services")
        self.resize(1200, 900)
        
        # Estilo Global
        self.setStyleSheet("""
            QMainWindow { background-color: #faf9f8; }
            * { font-family: 'Manrope', 'Segoe UI', sans-serif; color: #1a1c1c; }
            
            /* Scrollbar Personalizada al estilo Chrome */
            QScrollBar:vertical {
                border: none;
                background: #faf9f8;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #dcdbd9;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover { background: #c4c6cd; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setup_sidebar()
        
        # Contenedor de Contenido (Header + Form)
        self.content_container = QVBoxLayout()
        self.content_container.setSpacing(0)
        self.setup_topbar()
        self.setup_form_area()
        
        self.main_layout.addLayout(self.content_container)

    def setup_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-right: 1px solid #E8E4D9;
            }
            QPushButton {
                text-align: left;
                padding: 12px 24px;
                border: none;
                font-size: 14px;
                color: #64748b;
                background: transparent;
            }
            QPushButton:hover {
                background-color: #f8fafc;
                color: #1A2E44;
            }
            QPushButton#active {
                color: #1A2E44;
                font-weight: bold;
                border-right: 4px solid #1A2E44;
                background-color: #f8fafc;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 40, 0, 20)

        # Logo
        brand_container = QVBoxLayout()
        brand_container.setContentsMargins(24, 0, 24, 40)
        
        brand_label = QLabel("Scriptorium")
        brand_label.setStyleSheet("font-size: 26px; font-weight: 600; color: #1A2E44; font-family: 'serif'; italic;")
        
        sub_brand = QLabel("ARCHIVAL SERVICES")
        sub_brand.setStyleSheet("font-size: 10px; letter-spacing: 2px; color: #94a3b8; font-weight: bold;")
        
        brand_container.addWidget(brand_label)
        brand_container.addWidget(sub_brand)
        layout.addLayout(brand_container)

        # Menú
        menu_items = [
            ("library_books", "Collection"),
            ("add_circle", "Add Book"),
            ("import_export", "Data Manager"),
            ("settings", "Archive Settings")
        ]

        for icon, text in menu_items:
            btn = QPushButton(f"  {text}")
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            if text == "Add Book":
                btn.setObjectName("active")
            layout.addWidget(btn)

        layout.addStretch()

        # Footer Sidebar (Ayuda y Perfil)
        help_btn = QPushButton("  Help Center")
        help_btn.setStyleSheet("border-top: 1px solid #E8E4D9; padding-top: 20px; color: #64748b;")
        layout.addWidget(help_btn)

        profile = QFrame()
        profile.setStyleSheet("border: none; padding: 10px 20px;")
        p_layout = QHBoxLayout(profile)
        
        avatar = QLabel()
        avatar.setFixedSize(32, 32)
        avatar.setStyleSheet("background-color: #e2e8f0; border-radius: 16px; border: 1px solid #E8E4D9;")
        
        p_text = QLabel("<b>Librarian</b><br><span style='color: #64748b; font-size: 10px;'>Admin Access</span>")
        
        p_layout.addWidget(avatar)
        p_layout.addWidget(p_text)
        layout.addWidget(profile)

        self.main_layout.addWidget(sidebar)

    def setup_topbar(self):
        topbar = QFrame()
        topbar.setFixedHeight(64)
        topbar.setStyleSheet("background-color: rgba(255, 255, 255, 0.9); border-bottom: 1px solid #E8E4D9;")
        
        layout = QHBoxLayout(topbar)
        layout.setContentsMargins(32, 0, 32, 0)

        search = QLineEdit()
        search.setPlaceholderText("Buscar en el catálogo...")
        search.setFixedWidth(400)
        search.setStyleSheet("""
            QLineEdit {
                background-color: #eeeeed;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 13px;
            }
        """)

        export_btn = QPushButton("Export Library")
        export_btn.setCursor(QCursor(Qt.PointingHandCursor))
        export_btn.setStyleSheet("""
            QPushButton {
                border: 1.5px solid #775a19;
                color: #775a19;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #fed488; }
        """)

        layout.addWidget(search)
        layout.addStretch()
        layout.addWidget(export_btn)
        
        self.content_container.addWidget(topbar)

    def setup_form_area(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        container = QWidget()
        container.setStyleSheet("background-color: #faf9f8;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(30)

        # Header de sección
        header_widget = QWidget()
        h_layout = QVBoxLayout(header_widget)
        h_layout.setContentsMargins(0, 0, 0, 10)
        
        title = QLabel("Añadir Nuevo Volumen")
        title.setStyleSheet("font-size: 32px; color: #03192e; font-family: serif; font-style: italic;")
        subtitle = QLabel("Complete los detalles para integrar el libro en el inventario permanente.")
        subtitle.setStyleSheet("color: #64748b; font-size: 15px;")
        
        h_layout.addWidget(title)
        h_layout.addWidget(subtitle)
        header_widget.setStyleSheet("border-bottom: 1px solid #E8E4D9;")
        layout.addWidget(header_widget)

        # Info Box (Amarillo/Beige)
        info_box = QFrame()
        info_box.setStyleSheet("""
            QFrame {
                background-color: #eeeeed;
                border: 1px solid #E8E4D9;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        ib_layout = QVBoxLayout(info_box)
        ib_title = QLabel("Guía de Catalogación Local")
        ib_title.setStyleSheet("font-weight: bold; font-size: 13px; border: none;")
        ib_desc = QLabel("• Título completo • ISBN obligatorio • Use etiquetas para búsqueda")
        ib_desc.setStyleSheet("color: #43474d; font-size: 12px; border: none;")
        ib_layout.addWidget(ib_title)
        ib_layout.addWidget(ib_desc)
        layout.addWidget(info_box)

        # Secciones del Formulario
        layout.addWidget(self.create_form_section("Información Bibliográfica", [
            ("Título", "Ej: Cien años de soledad", 0, 0, 1, 2),
            ("Autor", "Gabriel García Márquez", 1, 0, 1, 1),
            ("Editorial", "Editorial Sudamericana", 1, 1, 1, 1)
        ]))

        layout.addWidget(self.create_form_section("Clasificación y Control", [
            ("Categoría", ["Novela", "Ensayo", "Poesía"], 0, 0, 1, 1, True),
            ("Código", "ISBN-...", 0, 1, 1, 1),
            ("Referencia", "REF-001", 0, 2, 1, 1),
            ("Cantidad", "1", 1, 0, 1, 1),
            ("Estado", "Nuevo", 1, 1, 1, 1),
            ("Prestado", ["No", "Sí"], 1, 2, 1, 1, True)
        ]))

        # Área de Texto Final
        notes_card = self.create_form_section("Notas y Descripción", [])
        notes_input = QTextEdit()
        notes_input.setPlaceholderText("Escriba una breve descripción...")
        notes_input.setFixedHeight(120)
        notes_input.setStyleSheet("""
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            padding: 10px;
            background-color: #faf9f8;
        """)
        notes_card.layout().addWidget(notes_input)
        layout.addWidget(notes_card)

        # Botones de Acción
        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setStyleSheet("color: #64748b; font-weight: 600; border: none; padding: 10px;")
        
        save_btn = QPushButton("  Guardar Libro")
        save_btn.setFixedHeight(45)
        save_btn.setFixedWidth(180)
        save_btn.setCursor(QCursor(Qt.PointingHandCursor))
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #03192e;
                color: white;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #1a2e44; }
        """)
        
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

        scroll.setWidget(container)
        self.content_container.addWidget(scroll)

    def create_form_section(self, title, fields):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #E8E4D9;
                border-radius: 12px;
            }
        """)
        
        # Efecto de sombra suave
        shadow = QGraphicsDropShadowEffect(blurRadius=10, xOffset=0, yOffset=2)
        shadow.setColor(QColor(0, 0, 0, 20))
        card.setGraphicsEffect(shadow)
        
        v_layout = QVBoxLayout(card)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)

        header = QLabel(title.upper())
        header.setStyleSheet("""
            background-color: #f8fafc;
            padding: 12px 24px;
            border-bottom: 1px solid #E8E4D9;
            font-size: 11px;
            font-weight: bold;
            color: #64748b;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
        """)
        v_layout.addWidget(header)

        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setContentsMargins(24, 24, 24, 24)
        grid.setSpacing(20)

        for f in fields:
            label_text, placeholder, row, col, rs, cs = f[:6]
            is_combo = f[6] if len(f) > 6 else False
            
            field_box = QVBoxLayout()
            field_label = QLabel(label_text)
            field_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #334155; border: none;")
            
            if is_combo:
                input_widget = QComboBox()
                input_widget.addItems(placeholder)
            else:
                input_widget = QLineEdit()
                input_widget.setPlaceholderText(str(placeholder))
            
            input_widget.setStyleSheet("""
                QLineEdit, QComboBox {
                    border: 1px solid #cbd5e1;
                    border-radius: 4px;
                    padding: 10px;
                    background-color: #faf9f8;
                    font-size: 14px;
                }
                QLineEdit:focus { border: 1.5px solid #03192e; background-color: #ffffff; }
            """)
            
            field_box.addWidget(field_label)
            field_box.addWidget(input_widget)
            grid.addLayout(field_box, row, col, rs, cs)

        v_layout.addWidget(grid_container)
        return card

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Ajuste de escala para monitores High DPI
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    window = ScriptoriumApp()
    window.show()
    sys.exit(app.exec())