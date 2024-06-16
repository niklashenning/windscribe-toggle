from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import QPointF, Qt, QTimeLine, QEasingCurve, QRectF, pyqtSignal
from PyQt6.QtWidgets import QWidget
from .enums import ToggleButtonState
from .utils import Utils


class ToggleButton(QWidget):

    # Signals
    clicked = pyqtSignal()
    stateChanged = pyqtSignal(ToggleButtonState)

    # Color constants for the outer circle
    ACCENT_COLOR_ON = QColor('#61ff8a')
    ACCENT_COLOR_TURNING_ON = QColor('#9ffdd9')

    def __init__(self, parent=None):
        super(ToggleButton, self).__init__()

        # Init attributes
        self.state = ToggleButtonState.OFF
        self.current_color = self.ACCENT_COLOR_TURNING_ON
        self.fixed_size = 86

        # Set widget size and cursor
        self.setFixedSize(self.fixed_size, self.fixed_size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Init timeline for the outer circle rotation animation with a frame range
        # of 0 - 170 because the half circles have a span of 170 degrees
        # The timeline starts again every time it finishes and calls
        # the update function every frame change to fire the paint event
        self.outer_circle_rotation_timeline = QTimeLine(700, self)
        self.outer_circle_rotation_timeline.setEasingCurve(QEasingCurve.Type.Linear)
        self.outer_circle_rotation_timeline.setFrameRange(0, 170)
        self.outer_circle_rotation_timeline.frameChanged.connect(self.update)
        self.outer_circle_rotation_timeline.finished.connect(self.outer_circle_rotation_timeline.start)

        # Init timeline for the outer circle width animation with a frame range
        # of 0 - 40 to animate a width from 0.0 - 4.0 with steps of 0.1
        self.outer_circle_width_timeline = QTimeLine(250, self)
        self.outer_circle_width_timeline.setEasingCurve(QEasingCurve.Type.Linear)
        self.outer_circle_width_timeline.setFrameRange(0, 4 * 10)
        self.outer_circle_width_timeline.frameChanged.connect(self.update)

        # Init timeline for the outer circle opacity animation with a frame range
        # of 0 - 255 to animate the opacity of an RGBA color
        self.outer_circle_opacity_timeline = QTimeLine(200, self)
        self.outer_circle_opacity_timeline.setFrameRange(0, 255)
        self.outer_circle_opacity_timeline.frameChanged.connect(self.update)

        # Init timeline for the icon rotation animation with a frame range
        # of 0 - 180 because the icon rotates 180 degrees
        self.icon_rotation_timeline = QTimeLine(200, self)
        self.icon_rotation_timeline.setEasingCurve(QEasingCurve.Type.Linear)
        self.icon_rotation_timeline.setFrameRange(0, 180)
        self.icon_rotation_timeline.frameChanged.connect(self.update)

    def paintEvent(self, event):
        # Init painter and set render hint to Antialiasing for better quality
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate center of the button
        center = QPointF(self.fixed_size / 2, self.fixed_size / 2)

        # Draw white filled circle in the center
        # A brush is used instead of a pen to fill the circle
        white_circle_radius = 35

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor('#FFFFFF')))
        painter.drawEllipse(center, white_circle_radius, white_circle_radius)

        # Draw the straight line part of the icon starting at an angle of
        # 90 degrees (pointing down) and adding the timeline value (0-180)
        # for a max angle of 270 (pointing up)
        # The utils method get_point_on_circle() is used to calculate
        # the point on the circle with the given center, line length and angle
        icon_line_width = 3.0
        icon_straight_line_length = 25
        icon_straight_line_angle = 90 + self.icon_rotation_timeline.currentFrame()
        icon_straight_line_point = Utils.get_point_on_circle(center, icon_straight_line_length,
                                                             icon_straight_line_angle)

        painter.setPen(QPen(QColor('#000000'), icon_line_width, cap=Qt.PenCapStyle.RoundCap))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(center, icon_straight_line_point)

        # Draw the arched line part of the icon starting at an angle of
        # -73 degrees and adding the timeline value (0-180) for a
        # max angle of -253 degrees with a span of 326 degrees
        icon_arched_line_rect_size = 38
        icon_arched_line_offset = (self.fixed_size - icon_arched_line_rect_size) / 2
        icon_arched_line_rect = QRectF(icon_arched_line_offset, icon_arched_line_offset,
                                       icon_arched_line_rect_size, icon_arched_line_rect_size)
        icon_arched_line_start_angle = (-73 - self.icon_rotation_timeline.currentFrame()) * 16
        icon_arched_line_span_angle = 326 * 16

        painter.setPen(QPen(QColor('#000000'), icon_line_width, cap=Qt.PenCapStyle.FlatCap))
        painter.drawArc(icon_arched_line_rect, icon_arched_line_start_angle, icon_arched_line_span_angle)

        # Calculations for outer circle / outer half circles
        outer_circle_pen_width = self.outer_circle_width_timeline.currentFrame() / 10
        outer_circle_line_width = 4.0
        outer_circle_rect_size = self.fixed_size - outer_circle_line_width
        outer_circle_offset = outer_circle_line_width / 2
        outer_circle_rect = QRectF(outer_circle_offset, outer_circle_offset,
                                   outer_circle_rect_size, outer_circle_rect_size)

        # State TURNING_ON
        if self.state == ToggleButtonState.TURNING_ON:
            # Draw outer half circles with spans of 170 degrees at start angles
            # of -95 and 85 degrees and adding the timeline value (0-170)
            # for a smooth infinite half circle rotation animation
            pen_color = QColor(self.ACCENT_COLOR_TURNING_ON.red(), self.ACCENT_COLOR_TURNING_ON.green(),
                               self.ACCENT_COLOR_TURNING_ON.blue(), self.outer_circle_opacity_timeline.currentFrame())
            outer_half_circle_1_start_angle = (-95 - self.outer_circle_rotation_timeline.currentFrame()) * 16
            outer_half_circle_2_start_angle = (85 - self.outer_circle_rotation_timeline.currentFrame()) * 16
            outer_half_circle_span_angle = 170 * 16

            painter.setPen(QPen(pen_color, outer_circle_pen_width))
            painter.drawArc(outer_circle_rect, outer_half_circle_1_start_angle, outer_half_circle_span_angle)
            painter.drawArc(outer_circle_rect, outer_half_circle_2_start_angle, outer_half_circle_span_angle)

        # State ON or OFF
        else:
            if self.outer_circle_width_timeline.currentFrame() > 0:
                # If circle width not null, draw outer circle at a start angle
                # of 0 degrees and with a span of 360 degrees (full circle)
                pen_color = QColor(self.current_color.red(), self.current_color.green(),
                                   self.current_color.blue(), self.outer_circle_opacity_timeline.currentFrame())
                outer_circle_start_angle = 0
                outer_circle_span_angle = 360 * 16

                painter.setPen(QPen(pen_color, outer_circle_pen_width))
                painter.drawArc(outer_circle_rect, outer_circle_start_angle, outer_circle_span_angle)

        # End painter
        painter.end()

    def mousePressEvent(self, event):
        # Check if button is left mouse button
        if event.button() == Qt.MouseButton.LeftButton:
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
            # Start normal animation (OFF -> any state)
            self.start_animation_forward()
        elif current_state == ToggleButtonState.TURNING_ON:
            if state == ToggleButtonState.OFF:
                # Start reverse animation (TURNING_ON -> OFF)
                self.start_animation_backward()
        elif current_state == ToggleButtonState.ON:
            if state == ToggleButtonState.OFF:
                # Start reverse animation (ON -> OFF)
                self.start_animation_backward()
            elif state == ToggleButtonState.TURNING_ON:
                # Start normal animation (ON -> TURNING_ON)
                self.start_animation_forward()

        # Set current color of the outer circle
        if state == ToggleButtonState.ON:
            self.current_color = self.ACCENT_COLOR_ON
        elif state == ToggleButtonState.TURNING_ON:
            self.current_color = self.ACCENT_COLOR_TURNING_ON

        # Emit state changed signal
        self.stateChanged.emit(self.state)

    def start_animation_forward(self):
        # Start outer circle animation timelines in forward mode
        self.outer_circle_rotation_timeline.start()

        self.outer_circle_width_timeline.setDirection(QTimeLine.Direction.Forward)
        self.outer_circle_width_timeline.start()

        self.outer_circle_opacity_timeline.setDirection(QTimeLine.Direction.Forward)
        self.outer_circle_opacity_timeline.setEasingCurve(QEasingCurve.Type.OutQuint)
        self.outer_circle_opacity_timeline.start()

        # Start icon animation timeline in forward mode
        self.icon_rotation_timeline.setDirection(QTimeLine.Direction.Forward)
        self.icon_rotation_timeline.start()

    def start_animation_backward(self):
        # Stop outer circle rotation timeline
        self.outer_circle_rotation_timeline.stop()

        # Start outer circle animation timelines in backward mode
        self.outer_circle_width_timeline.setDirection(QTimeLine.Direction.Backward)
        self.outer_circle_width_timeline.start()

        self.outer_circle_opacity_timeline.setDirection(QTimeLine.Direction.Backward)
        self.outer_circle_opacity_timeline.setEasingCurve(QEasingCurve.Type.InQuad)
        self.outer_circle_opacity_timeline.start()

        # Start icon animation timeline in backward mode
        self.icon_rotation_timeline.setDirection(QTimeLine.Direction.Backward)
        self.icon_rotation_timeline.start()
