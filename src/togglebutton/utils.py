import math
from PyQt6.QtCore import QPointF


class Utils:

    @staticmethod
    def get_point_on_circle(center: QPointF, radius: int, angle_degrees: int | float) -> QPointF:
        x = center.x() + radius * math.cos(math.radians(angle_degrees))
        y = center.y() + radius * math.sin(math.radians(angle_degrees))
        return QPointF(x, y)
