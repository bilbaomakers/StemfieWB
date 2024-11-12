#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import FreeCAD
import Part
from FreeCAD import Placement, Rotation, Vector

from freecad.stemfie import (
    BLOCK_UNIT,
    BLOCK_UNIT_HALF,
    BLOCK_UNIT_QUARTER,
    COS_30,
    COS_60,
    FILLET_RADIUS,
    HOLE_DIAMETER_STANDARD,
    PLATE_BORDER_OFFSET,
    PLATE_UPPER_FACE_DIAMETER,
    PLATE_UPPER_FACE_POCKET,
    SIN_30,
    SIN_45,
    SIN_60,
    make_hole,
)

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP

hole = make_hole(HOLE_DIAMETER_STANDARD, BLOCK_UNIT_QUARTER)


class PLT_TRI:
    """
    Plancha Triangular Stemfie
    """

    def __init__(self, obj):
        obj.Proxy = self
        self.minimum = 2
        obj.addProperty(
            "App::PropertyString",
            QT_TRANSLATE_NOOP("App::Property", "Code"),
            QT_TRANSLATE_NOOP("App::Property", "Designation"),
            QT_TRANSLATE_NOOP("App::Property", "STEMFIE part number"),
        )
        obj.setEditorMode("Code", 1)
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "RowsNumber"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of horizontal rows in X\nMinimum = 2"),
        ).RowsNumber = 3

    def onChanged(self, obj, prop):
        # Check valid parameter
        if prop == "RowsNumber" and obj.RowsNumber < self.minimum:
            obj.RowsNumber = self.minimum

    def execute(self, obj):
        #  ---- Genero puntos de los contornos, simetría en eje Y
        p1 = Vector(-(obj.RowsNumber - 1) * BLOCK_UNIT_HALF, 0, 0)
        p2 = Vector((obj.RowsNumber - 1) * BLOCK_UNIT_HALF, 0, 0)
        # angulo entre rectas sobre 2 -> 60°/2 = 30°
        p3 = Vector(
            (obj.RowsNumber - 1) * BLOCK_UNIT_HALF + FILLET_RADIUS * COS_30,
            FILLET_RADIUS * (1 + SIN_30),
            0,
        )
        p4 = Vector(
            FILLET_RADIUS * COS_30,
            (obj.RowsNumber - 1) * BLOCK_UNIT * SIN_60 + FILLET_RADIUS * (1 + SIN_30),
            0,
        )
        p5 = Vector(
            -FILLET_RADIUS * COS_30,
            (obj.RowsNumber - 1) * BLOCK_UNIT * SIN_60 + FILLET_RADIUS * (1 + SIN_30),
            0,
        )
        p6 = Vector(
            -(obj.RowsNumber - 1) * BLOCK_UNIT_HALF - FILLET_RADIUS * COS_30,
            FILLET_RADIUS * (1 + SIN_30),
            0,
        )
        #  ---- Genero puntos para circunferencias
        pc1 = Vector(
            (obj.RowsNumber - 1) * BLOCK_UNIT_HALF + FILLET_RADIUS * COS_30,
            FILLET_RADIUS * (1 - SIN_30),
            0,
        )
        pc2 = Vector(
            0, (obj.RowsNumber - 1) * BLOCK_UNIT * SIN_60 + FILLET_RADIUS * (1 + SIN_30 + COS_60), 0
        )
        pc3 = Vector(
            -(obj.RowsNumber - 1) * BLOCK_UNIT_HALF - FILLET_RADIUS * COS_30,
            FILLET_RADIUS * (1 - SIN_30),
            0,
        )
        #  ---- Creamos lineas y arcos
        l1 = Part.LineSegment(p1, p2)
        c1 = Part.Arc(p2, pc1, p3)
        l2 = Part.LineSegment(p3, p4)
        c2 = Part.Arc(p4, pc2, p5)
        l3 = Part.LineSegment(p5, p6)
        c3 = Part.Arc(p6, pc3, p1)

        #  ---- Creo el contorno
        s = Part.Shape([l1, c1, l2, c2, l3, c3])
        w = Part.Wire(s.Edges)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)

        #  ---- Creo la cara con el contorno
        f = Part.Face(w)
        #  ---- Le doy Volumen a la cara
        p = f.extrude(Vector(0, 0, BLOCK_UNIT_QUARTER))

        x0 = -(obj.RowsNumber - 1) * BLOCK_UNIT_HALF
        y0 = BLOCK_UNIT_HALF
        wire_holes = []

        # NOTE: Imagine a lattice of equilateral triangles with l = BLOCK_UNIT
        # - Create ascending lines of holes at an angle of 60°,
        #     decreasing the holes number in one for the next lines.
        # - Cut the chamfered holes on the shape.
        # - Add circles to the `wire_holes` array to then create a "cheese" face.
        for x in range(obj.RowsNumber):
            x1 = x0 + x * BLOCK_UNIT * COS_60
            for y in range(obj.RowsNumber - x):
                pos = Vector(x1 + x * BLOCK_UNIT * COS_60, y0 + y * BLOCK_UNIT * SIN_60, 0)
                hole.Placement = Placement(pos, Rotation())
                p = p.cut(hole)
                circle = Part.Circle(
                    pos, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
                )  # center, normal, radius
                wire_holes.append(Part.Wire(circle.toShape()))
                x1 += BLOCK_UNIT * COS_60

        inset_face = Part.Face([inset_wire] + wire_holes, "Part::FaceMakerCheese")
        inset_face.Placement = Placement(
            Vector(0, 0, BLOCK_UNIT_QUARTER - PLATE_UPPER_FACE_POCKET), Rotation()
        )
        upper_cut = inset_face.extrude((Vector(0, 0, PLATE_UPPER_FACE_POCKET)))
        p = p.cut(upper_cut)  # cut thin upper face with holes

        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "PLT-TRI-" + str(obj.RowsNumber)

        obj.Shape = p


class PLT_SQR:
    """
    Plancha Cuadrada Stemfie
    """

    def __init__(self, obj):
        obj.Proxy = self
        self.minimum = 2
        obj.addProperty(
            "App::PropertyString",
            QT_TRANSLATE_NOOP("App::Property", "Code"),
            QT_TRANSLATE_NOOP("App::Property", "Designation"),
            QT_TRANSLATE_NOOP("App::Property", "STEMFIE part number"),
        )
        obj.setEditorMode("Code", 1)
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberX"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in X\nMinimum = 2"),
        ).HolesNumberX = 4
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in Y\nMinimum = 2"),
        ).HolesNumberY = 3

    def onChanged(self, obj, prop):
        # Compruebo que Numero_Agujeros sea mayor de 1
        if prop == "HolesNumberX" and obj.HolesNumberX < self.minimum:
            obj.HolesNumberX = self.minimum
        if prop == "HolesNumberY" and obj.HolesNumberY < self.minimum:
            obj.HolesNumberY = self.minimum

    def execute(self, obj):
        # NOTE: Same code as in the previous implementation, only variable name changes

        #  ---- Genero puntos de los contornos
        p1 = Vector(0, -FILLET_RADIUS, 0)
        p2 = Vector((obj.HolesNumberX - 1) * BLOCK_UNIT, -FILLET_RADIUS, 0)

        p3 = Vector(((obj.HolesNumberX - 1) * BLOCK_UNIT) + FILLET_RADIUS, 0, 0)
        p4 = Vector(
            ((obj.HolesNumberX - 1) * BLOCK_UNIT) + FILLET_RADIUS,
            (obj.HolesNumberY - 1) * BLOCK_UNIT,
            0,
        )

        p5 = Vector(
            (obj.HolesNumberX - 1) * BLOCK_UNIT,
            ((obj.HolesNumberY - 1) * BLOCK_UNIT) + FILLET_RADIUS,
            0,
        )
        p6 = Vector(0, ((obj.HolesNumberY - 1) * BLOCK_UNIT) + FILLET_RADIUS, 0)

        p7 = Vector(-FILLET_RADIUS, ((obj.HolesNumberY - 1) * BLOCK_UNIT), 0)
        p8 = Vector(-FILLET_RADIUS, 0, 0)
        #  ---- Genero puntos para círculos, radio = FILLET_RADIUS
        pc1 = Vector(
            ((obj.HolesNumberX - 1) * BLOCK_UNIT) + (SIN_45 * FILLET_RADIUS),
            SIN_45 * -FILLET_RADIUS,
            0,
        )
        pc2 = Vector(
            ((obj.HolesNumberX - 1) * BLOCK_UNIT) + (SIN_45 * FILLET_RADIUS),
            ((obj.HolesNumberY - 1) * BLOCK_UNIT) + (SIN_45 * FILLET_RADIUS),
            0,
        )
        pc3 = Vector(
            (SIN_45 * FILLET_RADIUS) * -1,
            ((obj.HolesNumberY - 1) * BLOCK_UNIT) + (SIN_45 * FILLET_RADIUS),
            0,
        )
        pc4 = Vector((SIN_45 * FILLET_RADIUS) * -1, (SIN_45 * FILLET_RADIUS) * -1, 0)
        #  ---- Creamos lineas y arcos
        l1 = Part.LineSegment(p1, p2)
        c1 = Part.Arc(p2, pc1, p3)
        l2 = Part.LineSegment(p3, p4)
        c2 = Part.Arc(p4, pc2, p5)
        l3 = Part.LineSegment(p5, p6)
        c3 = Part.Arc(p6, pc3, p7)
        l4 = Part.LineSegment(p7, p8)
        c4 = Part.Arc(p8, pc4, p1)
        #  ---- Creo el contorno
        # W = Part.Wire([l1,c2,l3,c4])

        s = Part.Shape([l1, c1, l2, c2, l3, c3, l4, c4])
        w = Part.Wire(s.Edges)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)

        #  ---- Creo la cara con el contorno
        f = Part.Face(w)
        #  ---- Le doy Volumen a la cara
        p = f.extrude(Vector(0, 0, BLOCK_UNIT_QUARTER))
        wire_holes = []

        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberX):
            for y in range(obj.HolesNumberY):
                pos = Vector(x * BLOCK_UNIT, y * BLOCK_UNIT, 0)
                hole.Placement = Placement(pos, Rotation())
                p = p.cut(hole)
                circle = Part.Circle(
                    pos, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
                )  # center, normal, radius
                wire_holes.append(Part.Wire(circle.toShape()))

        inset_face = Part.Face([inset_wire] + wire_holes, "Part::FaceMakerCheese")
        inset_face.Placement = Placement(
            Vector(0, 0, BLOCK_UNIT_QUARTER - PLATE_UPPER_FACE_POCKET), Rotation()
        )
        upper_cut = inset_face.extrude((Vector(0, 0, PLATE_UPPER_FACE_POCKET)))
        p = p.cut(upper_cut)  # cut thin upper face with holes

        #  ---- Ponemos Nombre a la pieza con las variables de la misma

        obj.Code = "PLT-SQR-" + str(obj.HolesNumberX) + "x" + str(obj.HolesNumberY)

        obj.Shape = p


class PLT_HEX:
    """
    Plancha Hexagonal Stemfie
    """

    def __init__(self, obj):
        obj.Proxy = self
        self.minimum = 1
        obj.addProperty(
            "App::PropertyString",
            QT_TRANSLATE_NOOP("App::Property", "Code"),
            QT_TRANSLATE_NOOP("App::Property", "Designation"),
            QT_TRANSLATE_NOOP("App::Property", "STEMFIE part number"),
        )
        obj.setEditorMode("Code", 1)
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "RingsNumber"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP(
                "App::Property", "Number of rings around the central hole\nMinimum = 1"
            ),
        ).RingsNumber = 2

    def onChanged(self, obj, prop):
        # Check valid parameter
        if prop == "RingsNumber" and obj.RingsNumber < self.minimum:
            obj.RingsNumber = self.minimum

    def execute(self, obj):
        #  ---- Genero puntos de los contornos
        dx = obj.RingsNumber * BLOCK_UNIT * COS_60
        dy = obj.RingsNumber * BLOCK_UNIT * SIN_60 + BLOCK_UNIT_HALF

        p1 = Vector(-dx, -dy, 0)
        p2 = Vector(dx, -dy, 0)

        p3 = Vector(dx + FILLET_RADIUS * COS_30, -dy + FILLET_RADIUS * (1 - SIN_30), 0)
        p4 = Vector(
            obj.RingsNumber * BLOCK_UNIT + FILLET_RADIUS * COS_30, -FILLET_RADIUS * SIN_30, 0
        )

        p5 = Vector(
            obj.RingsNumber * BLOCK_UNIT + FILLET_RADIUS * COS_30, FILLET_RADIUS * SIN_30, 0
        )
        p6 = Vector(dx + FILLET_RADIUS * COS_30, dy - FILLET_RADIUS * (1 - SIN_30), 0)

        p7 = Vector(dx, dy, 0)
        p8 = Vector(-dx, dy, 0)

        p9 = Vector(-dx - FILLET_RADIUS * COS_30, dy - FILLET_RADIUS * (1 - SIN_30), 0)
        p10 = Vector(
            -obj.RingsNumber * BLOCK_UNIT - FILLET_RADIUS * COS_30, FILLET_RADIUS * SIN_30, 0
        )

        p11 = Vector(
            -obj.RingsNumber * BLOCK_UNIT - FILLET_RADIUS * COS_30, -FILLET_RADIUS * SIN_30, 0
        )
        p12 = Vector(-dx - FILLET_RADIUS * COS_30, -dy + FILLET_RADIUS * (1 - SIN_30), 0)

        #  ---- Genero puntos para circunferencias
        pc1 = Vector(dx + FILLET_RADIUS * COS_60, -dy + FILLET_RADIUS * (1 - SIN_60), 0)
        pc2 = Vector(obj.RingsNumber * BLOCK_UNIT + FILLET_RADIUS, 0, 0)
        pc3 = Vector(dx + FILLET_RADIUS * COS_60, dy - FILLET_RADIUS * (1 - SIN_60), 0)
        pc4 = Vector(-dx - FILLET_RADIUS * COS_60, dy - FILLET_RADIUS * (1 - SIN_60), 0)
        pc5 = Vector(-obj.RingsNumber * BLOCK_UNIT - FILLET_RADIUS, 0, 0)
        pc6 = Vector(-dx - FILLET_RADIUS * COS_60, -dy + FILLET_RADIUS * (1 - SIN_60), 0)

        #  ---- Creamos lineas y arcos
        l1 = Part.LineSegment(p1, p2)
        c1 = Part.Arc(p2, pc1, p3)
        l2 = Part.LineSegment(p3, p4)
        c2 = Part.Arc(p4, pc2, p5)
        l3 = Part.LineSegment(p5, p6)
        c3 = Part.Arc(p6, pc3, p7)
        l4 = Part.LineSegment(p7, p8)
        c4 = Part.Arc(p8, pc4, p9)
        l5 = Part.LineSegment(p9, p10)
        c5 = Part.Arc(p10, pc5, p11)
        l6 = Part.LineSegment(p11, p12)
        c6 = Part.Arc(p12, pc6, p1)

        #  ---- Creo el contorno
        s = Part.Shape([l1, c1, l2, c2, l3, c3, l4, c4, l5, c5, l6, c6])
        w = Part.Wire(s.Edges)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)

        #  ---- Creo la cara con el contorno
        f = Part.Face(w)
        #  ---- Le doy Volumen a la cara
        p = f.extrude(Vector(0, 0, BLOCK_UNIT_QUARTER))

        x0 = -obj.RingsNumber * BLOCK_UNIT * (1 + COS_60)
        y0 = -obj.RingsNumber * BLOCK_UNIT * SIN_60
        wire_holes = []

        # NOTE: Imagine a lattice of equilateral triangles with l = BLOCK_UNIT
        # - Create ascending lines of holes at an angle of 60°,
        #     all the holes take romboid shape, there are more than needed
        # - Cut the chamfered holes on the shape.
        # - Add circles to the `wire_holes` array to then create a "cheese" face.
        for x in range(obj.RingsNumber * 2 + 1):
            x1 = x0 + x * BLOCK_UNIT * COS_60
            for y in range(obj.RingsNumber * 2 + 1):
                pos = Vector(x1 + x * BLOCK_UNIT * COS_60, y0 + y * BLOCK_UNIT * SIN_60, 0)
                hole.Placement = Placement(pos, Rotation())
                p = p.cut(hole)
                circle = Part.Circle(
                    pos, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
                )  # center, normal, radius
                wire_holes.append(Part.Wire(circle.toShape()))
                x1 += BLOCK_UNIT * COS_60

        inset_face = Part.Face([inset_wire] + wire_holes, "Part::FaceMakerCheese")
        inset_face.Placement = Placement(
            Vector(0, 0, BLOCK_UNIT_QUARTER - PLATE_UPPER_FACE_POCKET), Rotation()
        )
        upper_cut = inset_face.extrude((Vector(0, 0, PLATE_UPPER_FACE_POCKET)))
        p = p.cut(upper_cut)  # cut thin upper face with holes

        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "PLT-HEX-" + str(obj.RingsNumber * 2 + 1)

        obj.Shape = p
