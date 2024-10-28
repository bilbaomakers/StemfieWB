import os
from math import cos, pi, sin

__version__ = "1.0.0"

path = os.path.join(os.path.dirname(__file__), "resources")

ICONPATH = os.path.join(path, "icons")
TRANSLATIONSPATH = os.path.join(path, "translations")
UIPATH = os.path.join(path, "ui")

# NOTE: STEMFIE constants

BLOCK_UNIT = 12.5  # mm
BLOCK_UNIT_HALF = 6.25  # mm
BLOCK_UNIT_QUARTER = 3.125  # mm
FILLET_RADIUS = BLOCK_UNIT_HALF
HOLE_DIAMETER_STANDARD = 7  # mm
HOLE_DIAMETER_ENLARGED = 7.2  # mm
FASTENER_OUTER_DIAMETER = 4  # mm
DOWEL_SHAFT_THICKNESS = 5  # mm
FASTENER_HEAD_THICKNESS = 5  # mm
CHAMFER = 0.3  # mm
TOP_LEDGE = 0.2  # mm

# NOTE: Math constants

SIN_30 = sin(pi / 6)
SIN_45 = sin(pi / 4)
SIN_60 = sin(pi / 3)
COS_30 = cos(pi / 6)
COS_45 = cos(pi / 4)
COS_60 = cos(pi / 3)


def get_icon_path(icon_name: str) -> str:
    """Returns the path to the SVG icon."""
    return os.path.join(ICONPATH, icon_name + ".svg")
