from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import QPointF, Qt, QTimeLine, QEasingCurve, QRectF, pyqtSignal
from PyQt6.QtWidgets import QWidget
from toggle_button_state import ToggleButtonState
from utils import Utils


class ToggleButton(QWidget):

    # Signals
    clicked = pyqtSignal()
    stateChanged = pyqtSignal(ToggleButtonState)

    # Constants
    ACCENT_COLOR_ON = QColor('#61ff8a')
    ACCENT_COLOR_TURNING_ON = QColor('#9ffdd9')
    TIMELINE_ACCURACY_BOOST = 10

    def __init__(self, parent=None):
        super(ToggleButton, self).__init__()

        # Init attributes
        self.state = ToggleButtonState.OFF
        self.current_color = self.ACCENT_COLOR_TURNING_ON
        self.fixed_size = 86

        # Widget settings
        self.setFixedSize(self.fixed_size, self.fixed_size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Timeline for the outer circle rotation animation
        self.outer_circle_rotation_timeline = QTimeLine(3000, self)
        self.outer_circle_rotation_timeline.setEasingCurve(QEasingCurve.Type.Linear)
        self.outer_circle_rotation_timeline.setFrameRange(-360 * 16, 360 * 16)
        self.outer_circle_rotation_timeline.frameChanged.connect(self.update)
        self.outer_circle_rotation_timeline.finished.connect(self.outer_circle_rotation_timeline.start)

        # Timeline for the outer circle width animation
        self.outer_circle_width_timeline = QTimeLine(250, self)
        self.outer_circle_width_timeline.setEasingCurve(QEasingCurve.Type.Linear)
        self.outer_circle_width_timeline.setFrameRange(0, 4 * self.TIMELINE_ACCURACY_BOOST)

        # Timeline for the outer circle opacity animation
        self.outer_circle_opacity_timeline = QTimeLine(200, self)
        self.outer_circle_opacity_timeline.setFrameRange(0, 255)

        # Timeline for the icon rotation animation
        self.icon_rotation_timeline = QTimeLine(200, self)
        self.icon_rotation_timeline.setEasingCurve(QEasingCurve.Type.Linear)
        self.icon_rotation_timeline.setFrameRange(0, 180 * self.TIMELINE_ACCURACY_BOOST)

    def paintEvent(self, event):
        # Start painter and set render hint to Antialiasing for better quality
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate center
        center = QPointF(self.fixed_size / 2, self.fixed_size / 2)

        # Draw white filled circle
        white_circle_radius = 35

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor('#FFFFFF')))
        painter.drawEllipse(center, white_circle_radius, white_circle_radius)

        # Draw straight line of the icon
        icon_line_width = 3.0
        icon_straight_line_length = 25
        icon_straight_line_angle = 90 + self.icon_rotation_timeline.currentFrame() / self.TIMELINE_ACCURACY_BOOST
        icon_straight_line_point = Utils.get_point_on_circle(center, icon_straight_line_length,
                                                             icon_straight_line_angle)

        painter.setPen(QPen(QColor('#000000'), icon_line_width, cap=Qt.PenCapStyle.RoundCap))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(center, icon_straight_line_point)

        # Draw arched line of the icon
        icon_arched_line_rect_size = 38
        icon_arched_line_offset = (self.fixed_size - icon_arched_line_rect_size) / 2
        icon_arched_line_rect = QRectF(icon_arched_line_offset, icon_arched_line_offset,
                                       icon_arched_line_rect_size, icon_arched_line_rect_size)
        icon_rotation_timeline_frame = int(self.icon_rotation_timeline.currentFrame() / self.TIMELINE_ACCURACY_BOOST)
        icon_arched_line_start_angle = (-107 - icon_rotation_timeline_frame) * 16
        icon_arched_line_span_angle = -326 * 16

        painter.setPen(QPen(QColor('#000000'), icon_line_width, cap=Qt.PenCapStyle.FlatCap))
        painter.drawArc(icon_arched_line_rect, icon_arched_line_start_angle, icon_arched_line_span_angle)

        # Calculations for outer circle / outer half circles
        outer_circle_pen_width = self.outer_circle_width_timeline.currentFrame() / self.TIMELINE_ACCURACY_BOOST
        outer_circle_line_width = 4.0
        outer_circle_rect_size = self.fixed_size - outer_circle_line_width
        outer_circle_offset = outer_circle_line_width / 2
        outer_circle_rect = QRectF(outer_circle_offset, outer_circle_offset,
                                   outer_circle_rect_size, outer_circle_rect_size)

        # State TURNING_ON
        if self.state == ToggleButtonState.TURNING_ON:
            # Set current color
            if self.current_color != self.ACCENT_COLOR_TURNING_ON:
                self.current_color = self.ACCENT_COLOR_TURNING_ON

            # Draw outer half circles
            pen_color = QColor(self.ACCENT_COLOR_TURNING_ON.red(), self.ACCENT_COLOR_TURNING_ON.green(),
                               self.ACCENT_COLOR_TURNING_ON.blue(), self.outer_circle_opacity_timeline.currentFrame())
            outer_half_circle_1_start_angle = -95 * 16 - self.outer_circle_rotation_timeline.currentFrame()
            outer_half_circle_2_start_angle = 85 * 16 - self.outer_circle_rotation_timeline.currentFrame()
            outer_half_circle_span_angle = 170 * 16

            painter.setPen(QPen(pen_color, outer_circle_pen_width))
            painter.drawArc(outer_circle_rect, outer_half_circle_1_start_angle, outer_half_circle_span_angle)
            painter.drawArc(outer_circle_rect, outer_half_circle_2_start_angle, outer_half_circle_span_angle)

        # State ON or OFF
        else:
            # Set current color if turned on and not already set
            if self.state == ToggleButtonState.ON:
                if self.current_color != self.ACCENT_COLOR_ON:
                    self.current_color = self.ACCENT_COLOR_ON

            # Draw outer circle if width not 0
            if self.outer_circle_width_timeline.currentFrame() > 0:
                pen_color = QColor(self.current_color.red(), self.current_color.green(),
                                   self.current_color.blue(), self.outer_circle_opacity_timeline.currentFrame())
                outer_circle_start_angle = 90 * 16
                outer_circle_span_angle = 360 * 16

                painter.setPen(QPen(pen_color, outer_circle_pen_width))
                painter.drawArc(outer_circle_rect, outer_circle_start_angle, outer_circle_span_angle)

        # End painter
        painter.end()

    def mousePressEvent(self, event):
        if self.state == ToggleButtonState.OFF:
            # Currently turned off -> turn on
            self.setState(ToggleButtonState.TURNING_ON)
        else:
            # Currently turned on or turning on -> turn off
            self.setState(ToggleButtonState.OFF)

        # Emit clicked signal
        self.clicked.emit()

    def getState(self) -> ToggleButtonState:
        return self.state

    def setState(self, state: ToggleButtonState):
        # Set new state
        current_state = self.state
        if current_state == state:
            # Return if current state is already the new state
            return
        self.state = state

        # Start animation depending on new state and current state
        if current_state == ToggleButtonState.OFF:
            if state == ToggleButtonState.TURNING_ON:
                self.start_animation_forward()
            elif state == ToggleButtonState.ON:
                self.start_animation_forward()
        elif current_state == ToggleButtonState.TURNING_ON:
            if state == ToggleButtonState.OFF:
                self.start_animation_backward()
        elif current_state == ToggleButtonState.ON:
            if state == ToggleButtonState.OFF:
                self.start_animation_backward()
            elif state == ToggleButtonState.TURNING_ON:
                self.start_animation_forward()

        # Emit state changed signal
        self.stateChanged.emit(self.state)

    def start_animation_forward(self):
        # Start outer circle animation timelines
        self.outer_circle_rotation_timeline.start()

        self.outer_circle_width_timeline.setDirection(QTimeLine.Direction.Forward)
        self.outer_circle_width_timeline.start()

        self.outer_circle_opacity_timeline.setDirection(QTimeLine.Direction.Forward)
        self.outer_circle_opacity_timeline.setEasingCurve(QEasingCurve.Type.OutQuint)
        self.outer_circle_opacity_timeline.start()

        # Start icon animation timeline
        self.icon_rotation_timeline.setDirection(QTimeLine.Direction.Forward)
        self.icon_rotation_timeline.start()

    def start_animation_backward(self):
        # Start outer circle animation timelines
        self.outer_circle_width_timeline.setDirection(QTimeLine.Direction.Backward)
        self.outer_circle_width_timeline.start()

        self.outer_circle_opacity_timeline.setDirection(QTimeLine.Direction.Backward)
        self.outer_circle_opacity_timeline.setEasingCurve(QEasingCurve.Type.InQuad)
        self.outer_circle_opacity_timeline.start()

        # Start icon animation timeline
        self.icon_rotation_timeline.setDirection(QTimeLine.Direction.Backward)
        self.icon_rotation_timeline.start()
