import math
from PyQt6.QtCore import QPointF


class Utils:

    @staticmethod
    def get_point_on_circle(center: QPointF, radius: int, angle: int | float) -> QPointF:
        # Calculate point on the circle with given center, radius and angle
        x = center.x() + radius * math.cos(math.radians(angle))
        y = center.y() + radius * math.sin(math.radians(angle))
        return QPointF(x, y)
