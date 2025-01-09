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


def make_chamfered_ring(
    diameter_i: float, diameter_o: float, height: float, z_offset: float = 0
) -> Part.Shape:
    """Creates the shape of a hole with chamfered edges at origin"""
    p0 = Vector(0, diameter_i / 2 + CHAMFER, 0)
    p1 = Vector(0, diameter_o / 2 - CHAMFER, 0)
    p2 = Vector(0, diameter_o / 2, CHAMFER)
    p3 = Vector(0, diameter_o / 2, height - CHAMFER)
    p4 = Vector(0, diameter_o / 2 - CHAMFER, height)
    p5 = Vector(0, diameter_i / 2 + CHAMFER, height)
    p6 = Vector(0, diameter_i / 2, height - CHAMFER)
    p7 = Vector(0, diameter_i / 2, CHAMFER)
    lines = [
        Part.makeLine(p0, p1),
        Part.makeLine(p1, p2),
        Part.makeLine(p2, p3),
        Part.makeLine(p3, p4),
        Part.makeLine(p4, p5),
        Part.makeLine(p5, p6),
        Part.makeLine(p6, p7),
        Part.makeLine(p7, p0),
    ]
    face = Part.Face(Part.Wire(lines))
    ring = face.revolve(Vector(0, 0, 0), Vector(0, 0, 1))
    ring.Placement = Placement(Vector(0, 0, z_offset), Rotation())
    return ring


def make_stemfie_shape(height: float) -> Part.Shape:
    # TODO: replace boolean operation with single extrusion
    p = Part.makeCylinder(
        BLOCK_UNIT_HALF + 0.1,
        height,
        Vector(0, 0, 0),
        Vector(0, 0, 1),
    )  # radius, height, position, rotation
    p = p.cut(
        Part.makeCylinder(HOLE_DIAMETER_STANDARD / 2, height, Vector(0, 0, 0), Vector(0, 0, 1))
    )
    p = p.cut(Part.makeCylinder(4.9, height, Vector(10, 0, 0), Vector(0, 0, 1)))
    p = p.cut(Part.makeCylinder(4.9, height, Vector(-10, 0, 0), Vector(0, 0, 1)))
    p = p.cut(Part.makeCylinder(4.9, height, Vector(0, 10, 0), Vector(0, 0, 1)))
    p = p.cut(Part.makeCylinder(4.9, height, Vector(0, -10, 0), Vector(0, 0, 1)))
    return p


def make_slot_wire_rr(length: float, radius: float) -> Part.Wire:
    """
    Create slot shape on X axis, left circumference at origin, size given by
    - length (distance between circumferences)
    - radius
    """
    if length == 0:
        raise ValueError("Length must not be zero.")

    #  ---- Genero puntos de los contornos
    p1 = Vector(0, -radius, 0)
    p2 = Vector(length, -radius, 0)
    p3 = Vector(length, radius, 0)
    p4 = Vector(0, radius, 0)
    #  ---- Genero puntos para círculos
    pc2 = Vector(length + radius, 0, 0)
    pc4 = Vector(-radius, 0, 0)
    #  ---- Creamos lineas y arcos
    l1 = Part.LineSegment(p1, p2)  # down
    c2 = Part.Arc(p2, pc2, p3)  # left
    l3 = Part.LineSegment(p3, p4)  # up
    c4 = Part.Arc(p4, pc4, p1)  # right
    #  ---- Creo el contorno
    s = Part.Shape([l1, c2, l3, c4])
    return Part.Wire(s.Edges)


def make_slot_wire_sr(length: float, radius: float) -> Part.Wire:
    """
    Create slot shape on X axis, left circumference at origin, size given by
    - length (distance between circumferences)
    - radius
    """
    if length == 0:
        raise ValueError("Length must not be zero.")

    p1 = Vector(0, -radius, 0)
    p2 = Vector(length, -radius, 0)
    p3 = Vector(length, radius, 0)
    p4 = Vector(0, radius, 0)
    #  ---- Genero punto para arco
    pc2 = Vector(length + radius, 0, 0)
    #  ---- Creamos lineas y arcos
    l1 = Part.LineSegment(p1, p2)
    c2 = Part.Arc(p2, pc2, p3)  # left
    l3 = Part.LineSegment(p3, p4)
    l4 = Part.LineSegment(p4, p1)
    s = Part.Shape([l1, c2, l3, l4])
    return Part.Wire(s.Edges)


def make_slot_wire_rs(length: float, radius: float) -> Part.Wire:
    """
    Create slot shape on X axis, left circumference at origin, size given by
    - length (distance between circumferences)
    - radius
    """
    if length == 0:
        raise ValueError("Length must not be zero.")

    p1 = Vector(0, -radius, 0)
    p2 = Vector(length, -radius, 0)
    p3 = Vector(length, radius, 0)
    p4 = Vector(0, radius, 0)
    #  ---- Genero punto para arco
    pc4 = Vector(-radius, 0, 0)
    #  ---- Creamos lineas y arcos
    l1 = Part.LineSegment(p1, p2)
    l2 = Part.LineSegment(p2, p3)
    l3 = Part.LineSegment(p3, p4)
    c4 = Part.Arc(p4, pc4, p1)  # right
    s = Part.Shape([l1, l2, l3, c4])
    return Part.Wire(s.Edges)


def make_rectangle_wire(length: float, width: float, dx: float = 0, dy: float = 0) -> Part.Wire:
    """
    Create rectangle shape on X-Y plane, with given length and width, and offsets dx and dy.
    """
    if length <= 0 or width <= 0:
        raise ValueError("Length and width must be greater than zero.")

    p1 = Vector(dx, dy, 0)
    p2 = Vector(dx + length, dy, 0)
    p3 = Vector(dx + length, dy + width, 0)
    p4 = Vector(dx, dy + width, 0)

    rectangle_shape = Part.Shape(
        [
            Part.LineSegment(p1, p2),
            Part.LineSegment(p2, p3),
            Part.LineSegment(p3, p4),
            Part.LineSegment(p4, p1),
        ]
    )
    return Part.Wire(rectangle_shape.Edges)
