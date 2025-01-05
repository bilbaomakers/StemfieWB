from math import cos, pi, sin

import Part
from FreeCAD import Placement, Rotation, Vector

# NOTE: STEMFIE constants

BLOCK_UNIT = 12.5  # mm
BLOCK_UNIT_HALF = 6.25  # mm
BLOCK_UNIT_QUARTER = 3.125  # mm
FILLET_RADIUS = BLOCK_UNIT_HALF
HOLE_DIAMETER_STANDARD = 7  # mm
HOLE_DIAMETER_ENLARGED = 7.2  # mm
FASTENER_OUTER_DIAMETER = 4  # mm
DOWEL_SHAFT_THICKNESS = 5  # mm
DOWEL_SHAFT_HOLE_DIAMETER = 2  # mm
FASTENER_HEAD_THICKNESS = 5  # mm
PLATE_BORDER_OFFSET = 1.1  # mm
PLATE_UPPER_FACE_POCKET = 0.2  # mm
PLATE_UPPER_FACE_DIAMETER = 9  # mm
CHAMFER = 0.3  # mm
TOP_LEDGE = 0.2  # mm

# NOTE: Math constants

SIN_30 = sin(pi / 6)
SIN_45 = sin(pi / 4)
SIN_60 = sin(pi / 3)
COS_30 = cos(pi / 6)
COS_45 = cos(pi / 4)
COS_60 = cos(pi / 3)


# Based on Fasteners WB
def make_chamfered_hole(diameter: float, height: float, z_offset: float = 0) -> Part.Shape:
    """Creates the shape of a hole with chamfered edges at origin"""
    p0 = Vector(0, 0, 0)
    p1 = Vector(0, diameter / 2 + CHAMFER, 0)
    p2 = Vector(0, diameter / 2, CHAMFER)
    p3 = Vector(0, diameter / 2, height - CHAMFER)
    p4 = Vector(0, diameter / 2 + CHAMFER, height)
    p5 = Vector(0, 0, height)
    lines = [
        Part.makeLine(p0, p1),
        Part.makeLine(p1, p2),
        Part.makeLine(p2, p3),
        Part.makeLine(p3, p4),
        Part.makeLine(p4, p5),
        Part.makeLine(p5, p0),
    ]
    face = Part.Face(Part.Wire(lines))
    hole = face.revolve(Vector(0, 0, 0), Vector(0, 0, 1))
    hole.Placement = Placement(Vector(0, 0, z_offset), Rotation())
    return hole
