from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("About HomeBase")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Content
        content = QLabel(
            "HomeBase is your ultimate streaming companion, designed to simplify your entertainment experience.\n\n"
            "Our mission is to make finding and watching your favorite content across multiple streaming services "
            "as seamless as possible. With HomeBase, you can search across all your streaming platforms in one place, "
            "get personalized recommendations, and discover new content that matches your interests.\n\n"
            "Version 1.0.0\n"
            "© 2024 HomeBase. All rights reserved."
        )
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content.setWordWrap(True)
        content.setStyleSheet("font-size: 14px; margin: 20px;")
        layout.addWidget(content)
        
        self.setLayout(layout) 