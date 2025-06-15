from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QCursor
import webbrowser

class Footer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(0)  # Remove spacing between labels
        
        # Create separate labels for each part
        prefix = QLabel("Made by Henry Pharris, icons by ")
        prefix.setStyleSheet("color: #666;")
        
        icons8_link = QLabel("Icons8")
        icons8_link.setStyleSheet("""
            color: #2196F3;
            text-decoration: underline;
        """)
        icons8_link.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icons8_link.mousePressEvent = self.open_icons8
        
        suffix = QLabel(". Click here for details")
        suffix.setStyleSheet("color: #666;")
        suffix.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        suffix.mousePressEvent = lambda e: self.main_window.navigate_to('about') if self.main_window else None
        
        # Add all labels to layout
        layout.addWidget(prefix)
        layout.addWidget(icons8_link)
        layout.addWidget(suffix)
        
        # Center the entire footer
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)

    def open_icons8(self, event):
        # Use webbrowser instead of QDesktopServices
        webbrowser.open("https://icons8.com/icons")
        # Accept the event to prevent it from propagating
        event.accept() 