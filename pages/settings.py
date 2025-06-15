from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QCheckBox, 
                            QComboBox, QPushButton, QHBoxLayout, QSlider, 
                            QDoubleSpinBox, QGridLayout, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, QSettings, QSize
from PyQt6.QtGui import QIcon

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings('HomeBase', 'Settings')
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Settings")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Create a grid layout for settings
        settings_grid = QGridLayout()
        settings_grid.setSpacing(20)  # Add some vertical spacing between rows
        
        # Auto-start Voice Control Setting
        voice_label = QLabel("Auto-start Voice Control:")
        voice_label.setStyleSheet("font-size: 14px;")
        voice_label.setFixedWidth(150)  # Fixed width for alignment
        settings_grid.addWidget(voice_label, 0, 0)
        
        self.voice_checkbox = QCheckBox()
        self.voice_checkbox.setChecked(False)
        settings_grid.addWidget(self.voice_checkbox, 0, 1)
        
        # Network Lag Setting
        network_label = QLabel("Network Lag:")
        network_label.setStyleSheet("font-size: 14px;")
        network_label.setFixedWidth(100)  # Fixed width for alignment
        settings_grid.addWidget(network_label, 1, 0)
        
        self.network_slider = QSlider(Qt.Orientation.Horizontal)
        self.network_slider.setMinimum(0)
        self.network_slider.setMaximum(200)  # 0-2 with 0.01 steps
        self.network_slider.setValue(100)  # Default to 1.0
        self.network_slider.valueChanged.connect(self.update_network_spinbox)
        settings_grid.addWidget(self.network_slider, 1, 1)
        
        self.network_spinbox = QDoubleSpinBox()
        self.network_spinbox.setMinimum(0)
        self.network_spinbox.setMaximum(2)
        self.network_spinbox.setSingleStep(0.01)
        self.network_spinbox.setValue(1.0)
        self.network_spinbox.setFixedWidth(80)  # Fixed width for spinbox
        self.network_spinbox.valueChanged.connect(self.update_network_slider)
        settings_grid.addWidget(self.network_spinbox, 1, 2)
        
        # System Lag Setting
        system_label = QLabel("System Lag:")
        system_label.setStyleSheet("font-size: 14px;")
        system_label.setFixedWidth(100)  # Fixed width for alignment
        settings_grid.addWidget(system_label, 2, 0)
        
        self.system_slider = QSlider(Qt.Orientation.Horizontal)
        self.system_slider.setMinimum(0)
        self.system_slider.setMaximum(200)  # 0-2 with 0.01 steps
        self.system_slider.setValue(100)  # Default to 1.0
        self.system_slider.valueChanged.connect(self.update_system_spinbox)
        settings_grid.addWidget(self.system_slider, 2, 1)
        
        self.system_spinbox = QDoubleSpinBox()
        self.system_spinbox.setMinimum(0)
        self.system_spinbox.setMaximum(2)
        self.system_spinbox.setSingleStep(0.01)
        self.system_spinbox.setValue(1.0)
        self.system_spinbox.setFixedWidth(80)  # Fixed width for spinbox
        self.system_spinbox.valueChanged.connect(self.update_system_slider)
        settings_grid.addWidget(self.system_spinbox, 2, 2)
        
        # Add the grid to the main layout
        layout.addLayout(settings_grid)
        
        # Service Preferences Section
        service_label = QLabel("Service Preferences")
        service_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(service_label)
        
        # Service list with drag and drop
        self.service_list = QListWidget()
        self.service_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.service_list.setIconSize(QSize(32, 32))  # Set icon size for the entire list
        self.service_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                height: 50px;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #b3b3b3;
                color: white;
            }
        """)
        
        # Define services with their icons and names
        self.services = [
            ('icons/icons8-netflix-desktop-app.svg', 'Netflix'),
            ('icons/icons8-hulu.svg', 'Hulu'),
            ('icons/icons8-hbo-max.svg', 'HBO Max'),
            ('icons/icons8-disney-plus.svg', 'Disney+'),
            ('icons/icons8-amazon-prime-video.svg', 'Prime Video'),
            ('icons/icons8-apple-tv.svg', 'Apple TV+'),
            ('icons/icons8-google-play.svg', 'Google Play'),
            ('icons/fandango.svg', 'Fandango'),
            ('icons/icons8-youtube.svg', 'YouTube')
        ]
        
        # Load saved order or use default
        saved_order = self.settings.value('service_order', [])
        if not saved_order:
            saved_order = [name for _, name in self.services]
        
        # Create items in the saved order
        for service_name in saved_order:
            # Find the icon path for this service
            icon_path = next((path for path, name in self.services if name == service_name), None)
            if icon_path:
                item = QListWidgetItem()
                item.setIcon(QIcon(icon_path))
                item.setText(service_name)
                item.setSizeHint(QSize(0, 50))  # Set fixed height for items
                self.service_list.addItem(item)
        
        layout.addWidget(self.service_list)
        
        # Add instructions label
        instructions = QLabel("Drag and drop services to set their display order")
        instructions.setStyleSheet("color: #666; font-style: italic; margin-top: 5px;")
        layout.addWidget(instructions)
        
        # Button layout for settings buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save Settings")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        save_button.clicked.connect(self.save_all_settings)
        button_layout.addWidget(save_button)
        
        reset_button = QPushButton("Reset Settings")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        reset_button.clicked.connect(self.reset_settings)
        button_layout.addWidget(reset_button)
        
        layout.addLayout(button_layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        self.setLayout(layout)

    def save_all_settings(self):
        # Save voice control setting
        self.settings.setValue('auto_start_voice', self.voice_checkbox.isChecked())
        
        # Save lag settings
        self.settings.setValue('network_lag', self.network_spinbox.value())
        self.settings.setValue('system_lag', self.system_spinbox.value())
        
        # Save service order
        service_order = []
        for i in range(self.service_list.count()):
            item = self.service_list.item(i)
            service_order.append(item.text())
        self.settings.setValue('service_order', service_order)
        
        # Sync all settings
        self.settings.sync()

    def update_network_spinbox(self, value):
        # Convert slider value (0-200) to spinbox value (0-2)
        self.network_spinbox.setValue(value / 100)

    def update_network_slider(self, value):
        # Convert spinbox value (0-2) to slider value (0-200)
        self.network_slider.setValue(int(value * 100))

    def update_system_spinbox(self, value):
        # Convert slider value (0-200) to spinbox value (0-2)
        self.system_spinbox.setValue(value / 100)

    def update_system_slider(self, value):
        # Convert spinbox value (0-2) to slider value (0-200)
        self.system_slider.setValue(int(value * 100))

    def reset_settings(self):
        # Reset lag settings
        self.network_spinbox.setValue(1.0)
        self.system_spinbox.setValue(1.0)
        self.voice_checkbox.setChecked(False)
        
        # Reset service order to default
        self.service_list.clear()
        for icon_path, service_name in self.services:
            item = QListWidgetItem()
            item.setIcon(QIcon(icon_path))
            item.setText(service_name)
            item.setSizeHint(QSize(0, 50))
            self.service_list.addItem(item)
        
        # Save the reset values
        self.save_all_settings()

    def load_settings(self):
        # Load saved values or use defaults
        self.network_spinbox.setValue(self.settings.value('network_lag', 1.0, type=float))
        self.system_spinbox.setValue(self.settings.value('system_lag', 1.0, type=float))
        self.voice_checkbox.setChecked(self.settings.value('auto_start_voice', False, type=bool))
        
        # Load service order
        saved_order = self.settings.value('service_order', [])
        if saved_order:
            # Clear existing items
            self.service_list.clear()
            
            # Add items in saved order
            for service_name in saved_order:
                icon_path = next((path for path, name in self.services if name == service_name), None)
                if icon_path:
                    item = QListWidgetItem()
                    item.setIcon(QIcon(icon_path))
                    item.setText(service_name)
                    item.setSizeHint(QSize(0, 50))
                    self.service_list.addItem(item) 