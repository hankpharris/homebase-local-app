from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMenu
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QPen, QColor

class BurgerButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-radius: 20px;
            }
        """)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Set pen for drawing lines
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        
        # Draw three lines for burger icon
        center_x = self.width() // 2
        spacing = 6
        start_y = (self.height() - spacing * 2) // 2
        
        # Draw three horizontal lines
        for i in range(3):
            y = start_y + i * spacing
            painter.drawLine(center_x - 10, y, center_x + 10, y)

class DropdownMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # Store reference to main window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create burger button
        self.burger_button = BurgerButton()
        self.burger_button.clicked.connect(self.show_menu)
        
        # Create menu
        self.menu = QMenu(self)
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 3px;
                color: #2c3e50;
                font-size: 14px;
            }
            QMenu::item:selected {
                background-color: #e0e0e0;
                color: #2c3e50;
            }
            QMenu::separator {
                height: 1px;
                background: #ccc;
                margin: 5px 0px;
            }
        """)
        
        # Add menu items
        self.menu.addAction("Home", lambda: self.navigate("home"))
        self.menu.addSeparator()
        self.menu.addAction("About", lambda: self.navigate("about"))
        self.menu.addAction("Settings", lambda: self.navigate("settings"))
        
        layout.addWidget(self.burger_button)
        self.setLayout(layout)

    def show_menu(self):
        # Show menu below the burger button
        self.menu.exec(self.burger_button.mapToGlobal(
            self.burger_button.rect().bottomLeft()
        ))

    def navigate(self, page):
        print(f"Menu: Attempting to navigate to {page}")  # Debug print
        if self.main_window and hasattr(self.main_window, 'navigate_to'):
            print(f"Menu: Found main window, calling navigate_to")  # Debug print
            self.main_window.navigate_to(page)
        else:
            print(f"Menu: Could not find main window or navigate_to method")  # Debug print 