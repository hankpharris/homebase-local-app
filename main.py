import sys
import speech_recognition as sr
from simplejustwatchapi.justwatch import search
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QPushButton, QLabel, QLineEdit, QMessageBox,
                            QTextEdit, QScrollArea, QFrame, QHBoxLayout, QStackedWidget)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl, QSize, QPointF, QTimer
from PyQt6.QtGui import QPixmap, QDesktopServices, QPainter, QIcon, QMouseEvent
import os
from urllib.parse import quote
import pyautogui
import time
import webbrowser
from components.menu import DropdownMenu
from components.footer import Footer
from pages.about import AboutPage
from pages.settings import SettingsPage
from PyQt6.QtCore import QSettings

class StreamingIcon(QLabel):
    def __init__(self, provider, url, icon_path, provider_icons):
        super().__init__()
        self.provider = provider
        self.url = url
        self.provider_icons = provider_icons
        self.setFixedSize(40, 40)
        self.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 5px;
            }
            QLabel:hover {
                background-color: #e9ecef;
                border-color: #ced4da;
            }
        """)
        
        # Load and set icon
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            self.setPixmap(icon.pixmap(30, 30))
        else:
            self.setText(provider[:2].upper())
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(f"Watch on {provider}")
        
        # Set up the settings
        self.settings = QSettings('HomeBase', 'Settings')
        
    def get_network_lag(self):
        return self.settings.value('network_lag', 1.0, type=float)
        
    def get_system_lag(self):
        return self.settings.value('system_lag', 1.0, type=float)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Get the show/movie title from the parent window
            parent = self.parent()
            while parent and not isinstance(parent, MainWindow):
                parent = parent.parent()
            
            if parent:
                title = parent.results_area.toPlainText().split('(')[0].strip()
                self.open_streaming_service(title)
    
    def open_streaming_service(self, title):
        # Service-specific handling
        service = None
        for s, data in self.provider_icons.items():
            if any(pattern in self.url.lower() for pattern in data['patterns']):
                service = s
                break

        if not service:
            QDesktopServices.openUrl(QUrl(self.url))
            return

        # Service-specific handling
        if service == 'hulu':
            self.handle_hulu_search(title)
        elif service == 'hbo max':
            self.handle_hbo_max_search(title)
        elif service == 'disney plus':
            self.handle_disney_plus_search(title)
        elif service == 'netflix':
            self.handle_netflix_search(title)
        elif service == 'prime':
            self.handle_prime_video_search(title)
        else:
            # Default URL-based search for other services
            service_urls = {
                'apple tv': f'https://tv.apple.com/search?q={quote(title)}',
                'google play': f'https://play.google.com/store/search?q={quote(title)}&c=movies',
                'fandango': f'https://www.fandango.com/search?q={quote(title)}'
            }
            
            if service in service_urls:
                QDesktopServices.openUrl(QUrl(service_urls[service]))
            else:
                QDesktopServices.openUrl(QUrl(self.url))

    def handle_hulu_search(self, title):
        if not title:
            QMessageBox.warning(None, "Error", "No title provided for search")
            return
            
        try:
            # Open Hulu search page directly
            print("Opening Hulu search page")
            webbrowser.open('https://www.hulu.com/search')
            time.sleep(4 * self.get_network_lag() * self.get_system_lag())
            
            # Navigating to the search bar and enter title
            print("Navigating to the search bar and enter title")
            pyautogui.press('tab')
            time.sleep(0.5 * self.get_system_lag())
            pyautogui.press('enter')
            time.sleep(0.5 * self.get_network_lag() * self.get_system_lag())
            pyautogui.press('tab')
            time.sleep(0.5 * self.get_system_lag())
            pyautogui.write(title)
            time.sleep(2 * self.get_network_lag() * self.get_system_lag())
            
            print("Selecting the first result")
            pyautogui.press('down')
            time.sleep(0.1 * self.get_system_lag())
            pyautogui.press('enter')
            time.sleep(2 * self.get_network_lag() * self.get_system_lag())

            # Navigating to and selecting the play button
            print("Navigating to and selecting the play button")
            pyautogui.press('tab')
            time.sleep(0.1 * self.get_system_lag())
            pyautogui.press('tab')
            time.sleep(0.25 * self.get_system_lag())
            pyautogui.press('enter')
            time.sleep(1.5 * self.get_network_lag() * self.get_system_lag())

            # Entering fullscreen
            print("Entering fullscreen")
            pyautogui.press('tab')
            pyautogui.press('f')
            
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Failed to perform Hulu search: {str(e)}")
            # Fallback to opening Hulu search page
            QDesktopServices.openUrl(QUrl('https://www.hulu.com/search'))

    def handle_hbo_max_search(self, title):
        if not title:
            QMessageBox.warning(None, "Error", "No title provided for search")
            return
            
        try:
            # Open HBO Max search page
            print("Opening HBO Max search page for: ", title)
            webbrowser.open(f'https://play.max.com/search?q={quote(title)}')
            time.sleep(4 * self.get_network_lag() * self.get_system_lag())
            
            #Select the first result
            print("Selecting the first result")
            pyautogui.press('down')
            time.sleep(0.01 * self.get_system_lag())
            pyautogui.press('down')
            time.sleep(0.5 * self.get_system_lag())
            pyautogui.press('enter')

            #Start the video
            print("Starting the video")
            time.sleep(0.5 * self.get_network_lag() * self.get_system_lag())
            pyautogui.press('tab')
            time.sleep(0.5 * self.get_system_lag())
            pyautogui.press('enter')
            time.sleep(5.0 * self.get_network_lag() * self.get_system_lag())
            pyautogui.press('tab')
            pyautogui.press('f')
            
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Failed to perform HBO Max search: {str(e)}")
            # Fallback to opening HBO Max search page
            QDesktopServices.openUrl(QUrl('https://play.max.com/search'))

    def handle_disney_plus_search(self, title):
        if not title:
            QMessageBox.warning(None, "Error", "No title provided for search")
            return
            
        try:
            # Open Disney+ page (URL is already set by JustWatch)
            webbrowser.open(self.url)
            time.sleep(4 * self.get_network_lag() * self.get_system_lag())
            
            # Execute the selection sequence: tab, enter, enter
            pyautogui.press('tab')
            time.sleep(0.5 * self.get_system_lag())
            pyautogui.press('enter')
            time.sleep(0.5 * self.get_network_lag() * self.get_system_lag())
            pyautogui.press('enter')
            time.sleep(2 * self.get_network_lag() * self.get_system_lag())
            pyautogui.press('f')
            
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Failed to perform Disney+ search: {str(e)}")
            # Fallback to opening Disney+ homepage
            QDesktopServices.openUrl(QUrl('https://www.disneyplus.com'))

    def handle_netflix_search(self, title):
        if not title:
            QMessageBox.warning(None, "Error", "No title provided for search")
            return
            
        try:
            # Open Netflix page directly (URL is already set by JustWatch)
            webbrowser.open(self.url)
            time.sleep(4 * self.get_network_lag() * self.get_system_lag())
            
            # Execute the selection sequence: tab (3 times), enter
            for _ in range(3):
                pyautogui.press('tab')
                time.sleep(0.5 * self.get_system_lag())
            
            pyautogui.press('enter')
            time.sleep(5.0 * self.get_network_lag() * self.get_system_lag())
            pyautogui.press('f')
            
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Failed to perform Netflix search: {str(e)}")
            # Fallback to opening Netflix homepage
            QDesktopServices.openUrl(QUrl('https://www.netflix.com'))

    def handle_prime_video_search(self, title):
        if not title:
            QMessageBox.warning(None, "Error", "No title provided for search")
            return
            
        try:
            # Open Prime Video search page
            webbrowser.open(f'https://www.amazon.com/s?k={quote(title)}+prime+video')
            time.sleep(4 * self.get_network_lag() * self.get_system_lag())
            
            # First sequence: tab, enter
            pyautogui.press('tab')
            time.sleep(0.5 * self.get_system_lag())
            pyautogui.press('enter')
            time.sleep(0.5 * self.get_network_lag() * self.get_system_lag())
            
            # Second sequence: tab (4 times quickly)
            for _ in range(4):
                pyautogui.press('tab')
                time.sleep(0.01 * self.get_system_lag())
            
            # Third sequence: enter, enter
            pyautogui.press('enter')
            time.sleep(0.5 * self.get_network_lag() * self.get_system_lag())
            pyautogui.press('enter')
            time.sleep(0.5 * self.get_network_lag() * self.get_system_lag())
            
            # Final sequence: f for fullscreen
            time.sleep(5.0 * self.get_network_lag() * self.get_system_lag())
            pyautogui.press('f')
            
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Failed to perform Prime Video search: {str(e)}")
            # Fallback to opening Prime Video homepage
            QDesktopServices.openUrl(QUrl('https://www.amazon.com/Prime-Video'))

class SearchThread(QThread):
    results_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def __init__(self, query):
        super().__init__()
        self.query = query

    def run(self):
        try:
            # Search with the simple-justwatch-python-api
            # Parameters: title, country, language, max_results, include_offers
            # Search with max_results=1 to only get the top result
            results = search(self.query, "US", "en", 1, True)
            self.results_ready.emit(results)
        except Exception as e:
            self.error_occurred.emit(f"Error searching: {str(e)}")

class SpeechRecognitionThread(QThread):
    text_recognized = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def run(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                self.text_recognized.emit(text)
        except sr.UnknownValueError:
            self.error_occurred.emit("Could not understand audio")
        except sr.RequestError as e:
            self.error_occurred.emit(f"Could not request results; {str(e)}")
        except Exception as e:
            self.error_occurred.emit(f"Error: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HomeBase")
        self.setMinimumSize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create top bar for menu and search
        top_bar = QHBoxLayout()
        
        # Add dropdown menu
        self.menu = DropdownMenu(self)
        top_bar.addWidget(self.menu)
        
        # Add title label
        title = QLabel("Show/Movie Search")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        top_bar.addWidget(title)
        
        # Add stretch to push title to center
        top_bar.addStretch()
        
        # Add top bar to main layout
        main_layout.addLayout(top_bar)
        
        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # Create home page
        self.home_page = QWidget()
        self.stacked_widget.addWidget(self.home_page)
        
        # Initialize settings
        self.settings = QSettings('HomeBase', 'Settings')
        
        # Initialize UI
        self.init_ui()
        
        # Check if voice control should auto-start
        if self.settings.value('auto_start_voice', False, type=bool):
            QTimer.singleShot(1000, self.toggle_voice_recognition)  # Delay by 1 second to ensure UI is ready
        
        # Initialize voice recognition state
        self.is_listening = False
        
        # Create and add pages to stacked widget
        self.about_page = AboutPage()
        self.settings_page = SettingsPage()
        
        self.stacked_widget.addWidget(self.about_page)
        self.stacked_widget.addWidget(self.settings_page)
        
        # Show home page by default
        self.stacked_widget.setCurrentWidget(self.home_page)
        
        # Initialize threads
        self.speech_thread = None
        self.search_thread = None
        
        # Provider to icon mapping with URL patterns
        self.provider_icons = {
            'netflix': {
                'icon': 'icons/icons8-netflix-desktop-app.svg',
                'patterns': ['netflix.com']
            },
            'hulu': {
                'icon': 'icons/icons8-hulu.svg',
                'patterns': ['hulu.com']
            },
            'hbo max': {
                'icon': 'icons/icons8-hbo-max.svg',
                'patterns': ['max.com', 'hbomax.com', 'play.max.com']
            },
            'disney plus': {
                'icon': 'icons/icons8-disney-plus.svg',
                'patterns': ['disneyplus.com', 'disney.com']
            },
            'prime': {
                'icon': 'icons/icons8-amazon-prime-video.svg',
                'patterns': ['amazon.com', 'primevideo.com', 'watch.amazon.com']
            },
            'apple tv': {
                'icon': 'icons/icons8-apple-tv.svg',
                'patterns': ['apple.com', 'tv.apple.com']
            },
            'google play': {
                'icon': 'icons/icons8-google-play.svg',
                'patterns': ['play.google.com', 'google.com']
            },
            'fandango': {
                'icon': 'icons/fandango.svg',
                'patterns': ['fandango.com', 'athome.fandango.com']
            },
            'youtube': {
                'icon': 'icons/icons8-youtube.svg',
                'patterns': ['youtube.com']
            }
        }
    
    def init_ui(self):
        # Main layout
        home_layout = QVBoxLayout(self.home_page)
        
        # Search bar with horizontal layout
        search_layout = QHBoxLayout()
        
        # Search input
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter show or movie title")
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
                margin: 10px;
            }
            QLineEdit:focus {
                border: 1px solid #007bff;
            }
        """)
        search_layout.addWidget(self.input_field)
        
        # Search button (icon only)
        search_button = QPushButton("🔍")
        search_button.setFixedHeight(self.input_field.sizeHint().height())
        search_button.setToolTip("Search")
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #302c2c;
                border: 1px solid #ffffff;
                border-radius: 5px;
                margin: 10px 5px 10px 0px;
                padding: 0px 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3a3636;
            }
        """)
        search_button.clicked.connect(self.start_search)
        search_layout.addWidget(search_button)
        
        # Voice button (icon only)
        self.voice_button = QPushButton("🎤")
        self.voice_button.setFixedHeight(self.input_field.sizeHint().height())
        self.voice_button.setToolTip("Voice Search (Click to toggle)")
        self.voice_button.setStyleSheet("""
            QPushButton {
                background-color: #302c2c;
                border: 1px solid #ffffff;
                border-radius: 5px;
                margin: 10px 10px 10px 0px;
                padding: 0px 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3a3636;
            }
            QPushButton:checked {
                background-color: #dc3545;
                border: 1px solid #ffffff;
            }
            QPushButton:checked:hover {
                background-color: #c82333;
            }
        """)
        self.voice_button.setCheckable(True)
        self.voice_button.clicked.connect(self.toggle_voice_recognition)
        search_layout.addWidget(self.voice_button)
        
        home_layout.addLayout(search_layout)
        
        # Add results area
        self.results_area = QTextEdit()
        self.results_area.setReadOnly(True)
        self.results_area.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        home_layout.addWidget(self.results_area)
        
        # Create a widget to hold streaming icons
        self.streaming_widget = QWidget()
        self.streaming_layout = QHBoxLayout(self.streaming_widget)
        self.streaming_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.streaming_layout.setSpacing(10)
        home_layout.addWidget(self.streaming_widget)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        home_layout.addWidget(self.status_label)
        
        # Add footer to home page
        footer = Footer(self)
        home_layout.addWidget(footer)
    
    def display_results(self, results):
        if not results:
            self.results_area.setText("No results found.")
            self.status_label.setText("Search completed - No results")
            return
        
        # Clear previous streaming icons
        for i in reversed(range(self.streaming_layout.count())): 
            self.streaming_layout.itemAt(i).widget().setParent(None)
        
        # Get the single result
        item = results[0]
        try:
            title = item.title if hasattr(item, 'title') else 'Unknown Title'
            year = item.year if hasattr(item, 'year') else 'N/A'
            item_type = item.type if hasattr(item, 'type') else 'Unknown Type'
            
            # Display basic info
            display_text = f"<h2 style='color: #2c3e50; margin-bottom: 10px;'>{title} ({year})</h2>"
            display_text += f"<p style='color: #34495e; margin-bottom: 10px;'><strong>Type:</strong> {item_type}</p>"
            self.results_area.setHtml(display_text)
            
            # Track which services we've already displayed
            displayed_services = set()
            
            # Get saved service order from settings
            settings = QSettings('HomeBase', 'Settings')
            saved_order = settings.value('service_order', [])
            
            # First display services in the saved order
            if saved_order:
                for service_name in saved_order:
                    if hasattr(item, 'offers'):
                        for offer in item.offers:
                            url = offer.url if hasattr(offer, 'url') else ''
                            if url:
                                for service, data in self.provider_icons.items():
                                    if any(pattern in url.lower() for pattern in data['patterns']):
                                        if service not in displayed_services and service.lower() == service_name.lower():
                                            icon_path = data['icon']
                                            provider = service
                                            displayed_services.add(service)
                                            icon = StreamingIcon(provider, url, icon_path, self.provider_icons)
                                            self.streaming_layout.addWidget(icon)
                                            break
            
            # Then display any remaining services that weren't in the saved order
            if hasattr(item, 'offers'):
                for offer in item.offers:
                    url = offer.url if hasattr(offer, 'url') else ''
                    if url:
                        for service, data in self.provider_icons.items():
                            if any(pattern in url.lower() for pattern in data['patterns']):
                                if service not in displayed_services:
                                    icon_path = data['icon']
                                    provider = service
                                    displayed_services.add(service)
                                    icon = StreamingIcon(provider, url, icon_path, self.provider_icons)
                                    self.streaming_layout.addWidget(icon)
                                    break
            
            self.status_label.setText("Search completed")
        except Exception as e:
            self.results_area.setText(f"Error processing result: {str(e)}")
            self.status_label.setText("Error processing result")
    
    def start_search(self):
        query = self.input_field.text().strip()
        if query:
            self.status_label.setText("Searching...")
            self.search_thread = SearchThread(query)
            self.search_thread.results_ready.connect(self.display_results)
            self.search_thread.error_occurred.connect(self.handle_search_error)
            self.search_thread.start()
        else:
            QMessageBox.warning(self, "Warning", "Please enter a search query!")
    
    def handle_search_error(self, error_message):
        self.status_label.setText(error_message)
        QMessageBox.warning(self, "Search Error", error_message)
    
    def toggle_voice_recognition(self):
        if not self.is_listening:
            # Ensure any existing thread is properly cleaned up
            if self.speech_thread:
                self.speech_thread.terminate()
                self.speech_thread.wait()
                self.speech_thread = None
            self.start_voice_recognition()
        else:
            self.stop_voice_recognition()
    
    def start_voice_recognition(self):
        # Always create a new thread when starting
        self.speech_thread = SpeechRecognitionThread()
        self.speech_thread.text_recognized.connect(self.handle_recognized_text)
        self.speech_thread.error_occurred.connect(self.handle_recognition_error)
        self.is_listening = True
        self.voice_button.setChecked(True)
        self.status_label.setText("Listening... Speak now! Use 'search' or 'play' commands")
        self.speech_thread.start()
    
    def stop_voice_recognition(self):
        self.is_listening = False
        self.voice_button.setChecked(False)
        if self.speech_thread and self.speech_thread.isRunning():
            self.speech_thread.terminate()
            self.speech_thread.wait()
            self.speech_thread = None  # Clear the thread reference
        self.status_label.setText("Voice recognition stopped")
    
    def handle_recognized_text(self, text):
        self.status_label.setText("Voice input received!")
        
        # Process the command
        text = text.lower().strip()
        if text.startswith("search "):
            # Regular search
            query = text[7:].strip()  # Remove "search " prefix
            self.input_field.setText(query)
            self.start_search()
            # Restart voice recognition after a short delay for search commands
            QTimer.singleShot(1000, self.start_voice_recognition)
        elif text.startswith("play "):
            # Search and start with highest priority service
            query = text[5:].strip()  # Remove "play " prefix
            self.input_field.setText(query)
            self.stop_voice_recognition()
            self.start_search_and_play()
            # Stop voice recognition after play commands
            
        else:
            # Ignore any other voice input
            self.status_label.setText("Please use 'search' or 'play' commands")
            # Restart voice recognition after a short delay for unrecognized commands
            QTimer.singleShot(1000, self.start_voice_recognition)
    
    def handle_recognition_error(self, error_message):
        self.status_label.setText(error_message)
        #QMessageBox.warning(self, "Voice Recognition Error", error_message)
        self.stop_voice_recognition()
        self.status_label.setText("Recognition error, restarting...")
        QTimer.singleShot(1000, self.start_voice_recognition)
    
    def start_search_and_play(self):
        query = self.input_field.text().strip()
        if query:
            self.status_label.setText("Searching and preparing to play...")
            self.search_thread = SearchThread(query)
            self.search_thread.results_ready.connect(self.display_and_play_results)
            self.search_thread.error_occurred.connect(self.handle_search_error)
            self.search_thread.start()
        else:
            QMessageBox.warning(self, "Warning", "Please enter a search query!")
    
    def display_and_play_results(self, results):
        if not results:
            self.results_area.setText("No results found.")
            self.status_label.setText("Search completed - No results")
            return
        
        # First display results normally
        self.display_results(results)
        
        # Then try to play with highest priority service
        try:
            # Get the single result
            item = results[0]
            if hasattr(item, 'offers'):
                # Get saved service order from settings
                settings = QSettings('HomeBase', 'Settings')
                saved_order = settings.value('service_order', [])
                
                # Try to find the highest priority service that has the content
                if saved_order:
                    for service_name in saved_order:
                        for offer in item.offers:
                            url = offer.url if hasattr(offer, 'url') else ''
                            if url:
                                for service, data in self.provider_icons.items():
                                    if any(pattern in url.lower() for pattern in data['patterns']):
                                        if service.lower() == service_name.lower():
                                            # Found a matching service, create an icon and call its handler directly
                                            title = item.title if hasattr(item, 'title') else 'Unknown Title'
                                            icon = StreamingIcon(service, url, data['icon'], self.provider_icons)
                                            
                                            # Call the appropriate handler based on the service
                                            if service == 'hulu':
                                                icon.handle_hulu_search(title)
                                            elif service == 'hbo max':
                                                icon.handle_hbo_max_search(title)
                                            elif service == 'disney plus':
                                                icon.handle_disney_plus_search(title)
                                            elif service == 'netflix':
                                                icon.handle_netflix_search(title)
                                            elif service == 'prime':
                                                icon.handle_prime_video_search(title)
                                            else:
                                                # Default URL-based search for other services
                                                service_urls = {
                                                    'apple tv': f'https://tv.apple.com/search?q={quote(title)}',
                                                    'google play': f'https://play.google.com/store/search?q={quote(title)}&c=movies',
                                                    'fandango': f'https://www.fandango.com/search?q={quote(title)}'
                                                }
                                                
                                                if service in service_urls:
                                                    QDesktopServices.openUrl(QUrl(service_urls[service]))
                                                else:
                                                    QDesktopServices.openUrl(QUrl(url))
                                            return
        except Exception as e:
            print(f"Error in auto-play: {str(e)}")
            # Don't show error to user, just continue with normal display

    def navigate_to(self, page):
        print(f"MainWindow: Attempting to navigate to {page}")  # Debug print
        if page == 'home':
            self.stacked_widget.setCurrentWidget(self.home_page)
        elif page == 'about':
            self.stacked_widget.setCurrentWidget(self.about_page)
        elif page == 'settings':
            self.stacked_widget.setCurrentWidget(self.settings_page)
        self.current_page = page
        print(f"MainWindow: Successfully navigated to {page}")  # Debug print

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 