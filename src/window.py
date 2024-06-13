import random
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from toggle_button import ToggleButton


class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        # Window settings
        self.setFixedSize(450, 230)
        self.setWindowTitle('Windscribe On/Off Button')
        self.setStyleSheet('background: #0E1A2B')

        # Create toggle button
        self.toggle_button = ToggleButton(self)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.toggle_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
