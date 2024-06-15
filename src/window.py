import random
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt6.QtCore import QTimer
from togglebutton import ToggleButton, ToggleButtonState


class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        # Window settings
        self.setFixedSize(450, 230)
        self.setWindowTitle('Windscribe On/Off Button')
        self.setStyleSheet('background: #0E1A2B')

        # Create toggle button
        self.toggle_button = ToggleButton(self)
        self.toggle_button.clicked.connect(self.toggle_button_clicked)
        self.toggle_button.stateChanged.connect(self.toggle_button_state_changed)

        # Create timer for toggle button
        self.toggle_button_timer = QTimer(self)

        # Create main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.toggle_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def toggle_button_clicked(self):
        if self.toggle_button.getState() != ToggleButtonState.OFF:
            # Start timer that sets the state of the toggle button to ON after a
            # random delay of 1750 - 3000 milliseconds if the state is still TURNING_ON
            # (You would normally run your turning on functionality here instead of a random delay)
            self.toggle_button_timer = QTimer(self)
            self.toggle_button_timer.setSingleShot(True)
            self.toggle_button_timer.timeout.connect(self.toggle_button_timer_finished)
            self.toggle_button_timer.start(random.randint(1750, 3000))
        else:
            # If the button has been clicked and turned off again, stop timer
            self.toggle_button_timer.stop()

    def toggle_button_state_changed(self, state):
        # Print the new state
        print(state)

    def toggle_button_timer_finished(self):
        # If the state is still TURNING_ON, set the state to ON
        if self.toggle_button.state == ToggleButtonState.TURNING_ON:
            self.toggle_button.setState(ToggleButtonState.ON)
