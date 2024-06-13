from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import QSize, QPointF, Qt, QTimeLine, QEasingCurve, QTimer
from PyQt6.QtWidgets import QWidget
from toggle_button_state import ToggleButtonState


class ToggleButton(QWidget):

    def __init__(self, parent=None):
        super(ToggleButton, self).__init__()

        self.state = ToggleButtonState.OFF
        self.fixed_size = QSize(86, 86)

        self.setFixedSize(self.fixed_size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.circle_rotation_timeline = QTimeLine(3000, self)
        self.circle_rotation_timeline.setEasingCurve(QEasingCurve.Type.Linear)
        self.circle_rotation_timeline.setFrameRange(-360 * 16, 360 * 16)
        self.circle_rotation_timeline.frameChanged.connect(self.update)
        self.circle_rotation_timeline.finished.connect(self.circle_rotation_timeline.start)

        self.circle_width_timeline = QTimeLine(250, self)
        self.circle_width_timeline.setEasingCurve(QEasingCurve.Type.Linear)
        self.circle_width_timeline.setFrameRange(0, 4 * 10)

        self.circle_opacity_timeline = QTimeLine(200, self)
        self.circle_opacity_timeline.setFrameRange(0, 255)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen()
        pen.setColor(QColor('#FFFFFF'))

        brush = QBrush(QColor('#FFFFFF'))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(brush)
        painter.drawEllipse(QPointF(self.fixed_size.width() / 2, self.fixed_size.height() / 2), 35, 35)

        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setWidth(3)
        pen.setColor(QColor('#000000'))
        painter.setPen(pen)
        painter.drawLine(QPointF(self.fixed_size.width() / 2, self.fixed_size.height() / 2),
                         QPointF(self.fixed_size.width() / 2, self.fixed_size.height() / 2 + 28))

        pen.setCapStyle(Qt.PenCapStyle.SquareCap)
        pen.setColor(QColor('#000000'))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawArc(24, 24, 38, 38, -109 * 16, -322 * 16)
        #painter.drawArc(24, 24, 38, 38, 71 * 16, -322 * 16)

        if self.state == ToggleButtonState.TURNING_ON:
            pen.setColor(QColor(159, 253, 217, self.circle_opacity_timeline.currentFrame()))
            pen.setWidthF(self.circle_width_timeline.currentFrame() / 10)

            painter.setPen(pen)
            painter.drawArc(2, 2, self.fixed_size.width() - 4, self.fixed_size.height() - 4,
                            -95 * 16 - self.circle_rotation_timeline.currentFrame(), -170 * 16)

            painter.setPen(pen)
            painter.drawArc(2, 2, self.fixed_size.width() - 4, self.fixed_size.height() - 4,
                            85 * 16 - self.circle_rotation_timeline.currentFrame(), -170 * 16)

        elif self.state == ToggleButtonState.ON or self.state == ToggleButtonState.OFF:
            if self.circle_width_timeline.currentFrame() > 0:
                pen.setColor(QColor(97, 255, 138, self.circle_opacity_timeline.currentFrame()))
                pen.setWidthF(self.circle_width_timeline.currentFrame() / 10)

                painter.setPen(pen)
                painter.drawArc(2, 2, self.fixed_size.width() - 4,
                                self.fixed_size.height() - 4, -90 * 16, -360 * 16)

        painter.end()

    def mousePressEvent(self, event):
        if self.state == ToggleButtonState.OFF:
            self.state = ToggleButtonState.TURNING_ON

            self.circle_rotation_timeline.start()

            self.circle_width_timeline.setDirection(QTimeLine.Direction.Forward)
            self.circle_width_timeline.start()

            self.circle_opacity_timeline.setDirection(QTimeLine.Direction.Forward)
            self.circle_opacity_timeline.setEasingCurve(QEasingCurve.Type.OutQuint)
            self.circle_opacity_timeline.start()

            timer = QTimer(self)
            timer.setSingleShot(True)
            def toggle_button_state_on(): self.state = ToggleButtonState.ON
            timer.timeout.connect(toggle_button_state_on)
            timer.start(2000)

        else:
            self.state = ToggleButtonState.OFF
            self.circle_width_timeline.setDirection(QTimeLine.Direction.Backward)
            self.circle_width_timeline.start()

            self.circle_opacity_timeline.setDirection(QTimeLine.Direction.Backward)
            self.circle_opacity_timeline.setEasingCurve(QEasingCurve.Type.InQuad)
            self.circle_opacity_timeline.start()
