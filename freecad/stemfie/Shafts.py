#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import sqrt

import FreeCAD
import Part
from FreeCAD import Vector

from freecad.stemfie.utils import (
    BLOCK_UNIT,
    BLOCK_UNIT_QUARTER,
    DOWEL_SHAFT_HOLE_DIAMETER,
    DOWEL_SHAFT_THICKNESS,
    make_hole,
)

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP


class SFT_PLN:
    """
    Shaft plain
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
            QT_TRANSLATE_NOOP("App::Property", "HolesNumber"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number\nMinimum = 1"),
        ).HolesNumber = 3

    def onChanged(self, obj, prop):
        # Check valid parameter
        if prop == "HolesNumber" and obj.HolesNumber < self.minimum:
            obj.HolesNumber = self.minimum

    def execute(self, obj):
        #  Profile symmetric to Y and Z axis
        dx = sqrt(BLOCK_UNIT_QUARTER**2 - (DOWEL_SHAFT_THICKNESS / 2) ** 2)
        p1 = FreeCAD.Vector(0, -dx, -DOWEL_SHAFT_THICKNESS / 2)
        p2 = FreeCAD.Vector(0, dx, -DOWEL_SHAFT_THICKNESS / 2)
        p3 = FreeCAD.Vector(0, dx, DOWEL_SHAFT_THICKNESS / 2)
        p4 = FreeCAD.Vector(0, -dx, DOWEL_SHAFT_THICKNESS / 2)
        #  ---- Genero puntos para circunferencias
        pc1 = FreeCAD.Vector(0, BLOCK_UNIT_QUARTER, 0)
        pc2 = FreeCAD.Vector(0, -BLOCK_UNIT_QUARTER, 0)
        #  ---- Creamos lineas y arcos
        l1 = Part.LineSegment(p1, p2)
        c1 = Part.Arc(p2, pc1, p3)
        l2 = Part.LineSegment(p3, p4)
        c2 = Part.Arc(p4, pc2, p1)

        s = Part.Shape([l1, c1, l2, c2])
        shaft_wire = Part.Wire(s.Edges)
        hole_wire = Part.Wire(
            Part.Circle(
                FreeCAD.Vector(0, 0, 0), Vector(1, 0, 0), DOWEL_SHAFT_HOLE_DIAMETER / 2
            ).toShape()
        )  # center, normal, radius

        f = Part.Face([shaft_wire, hole_wire], "Part::FaceMakerCheese")

        length = (obj.HolesNumber + 1) * BLOCK_UNIT_QUARTER
        p = f.extrude(FreeCAD.Vector(length, 0, 0))

        hole = make_hole(
            DOWEL_SHAFT_HOLE_DIAMETER, DOWEL_SHAFT_THICKNESS, -DOWEL_SHAFT_THICKNESS / 2
        )

        for x in range(obj.HolesNumber):
            hole.Placement = FreeCAD.Placement(
                FreeCAD.Vector((x + 1) * BLOCK_UNIT_QUARTER, 0, -DOWEL_SHAFT_THICKNESS / 2),
                FreeCAD.Rotation(),
            )
            p = p.cut(hole)

        obj.Code = "SFT-PLN-" + str(obj.HolesNumber)

        obj.Shape = p
