#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import FreeCAD
import Part
from FreeCAD import Vector

from freecad.stemfie import (
    BLOCK_UNIT,
    BLOCK_UNIT_HALF,
    BLOCK_UNIT_QUARTER,
)

# FIXME: opening old files creates error
# pyException: <string>(1)<class 'AttributeError'>: Module freecad.stemfie.Piezas has no class TRH_H_BEM_SFT_1W
# How to redirect objects to new class?

# TODO: ask if it's better to reduce from 5 commands to a single one
# advantage: you can change shape on the same object
# alternative: join 5 commands in a single drop-down icon on the toolbar

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP

BU_FIVE_QUARTERS = BLOCK_UNIT + BLOCK_UNIT_QUARTER
lado_G = 4.9291
entre_caras_G = 11.9
lado_P = 3.7279
entre_caras_P = 9
altura = 4.6875


class CONN:
    """Base class for all STEMFIE connectors."""

    def __init__(self, obj):
        obj.Proxy = self
        self.connectors = []
        self.code = ""
        obj.addProperty(
            "App::PropertyString",
            QT_TRANSLATE_NOOP("App::Property", "Code"),
            QT_TRANSLATE_NOOP("App::Property", "Designation"),
            QT_TRANSLATE_NOOP("App::Property", "STEMFIE part number"),
        )
        obj.setEditorMode("Code", 1)

    def create_cube(self) -> Part.Shape:
        cube = Part.makeBox(
            BU_FIVE_QUARTERS,
            BU_FIVE_QUARTERS,
            BLOCK_UNIT,
            FreeCAD.Vector(-BU_FIVE_QUARTERS / 2, -BU_FIVE_QUARTERS / 2, -BLOCK_UNIT_HALF),
            FreeCAD.Vector(0, 0, 1),
        )

        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        cube = cube.cut(
            Part.makeBox(12.9, 12.9, 20, FreeCAD.Vector(-6.45, -6.45, -10), FreeCAD.Vector(0, 0, 1))
        )
        return cube

    def create_cone(self) -> Part.Shape:
        #  Puntos Polígono Grande
        pg1 = FreeCAD.Vector(entre_caras_G / 2, lado_G / 2, 0)
        pg2 = FreeCAD.Vector(lado_G / 2, entre_caras_G / 2, 0)
        pg3 = FreeCAD.Vector(-lado_G / 2, entre_caras_G / 2, 0)
        pg4 = FreeCAD.Vector(-entre_caras_G / 2, lado_G / 2, 0)
        pg5 = FreeCAD.Vector(-entre_caras_G / 2, -lado_G / 2, 0)
        pg6 = FreeCAD.Vector(-lado_G / 2, -entre_caras_G / 2, 0)
        pg7 = FreeCAD.Vector(lado_G / 2, -entre_caras_G / 2, 0)
        pg8 = FreeCAD.Vector(entre_caras_G / 2, -lado_G / 2, 0)
        #  Puntos Polígono Pequeño
        pp1 = FreeCAD.Vector(entre_caras_P / 2, lado_P / 2, altura)
        pp2 = FreeCAD.Vector(lado_P / 2, entre_caras_P / 2, altura)
        pp3 = FreeCAD.Vector(-lado_P / 2, entre_caras_P / 2, altura)
        pp4 = FreeCAD.Vector(-entre_caras_P / 2, lado_P / 2, altura)
        pp5 = FreeCAD.Vector(-entre_caras_P / 2, -lado_P / 2, altura)
        pp6 = FreeCAD.Vector(-lado_P / 2, -entre_caras_P / 2, altura)
        pp7 = FreeCAD.Vector(lado_P / 2, -entre_caras_P / 2, altura)
        pp8 = FreeCAD.Vector(entre_caras_P / 2, -lado_P / 2, altura)
        #  ---- Creamos lineas Polígono Grande
        lpg1 = Part.LineSegment(pg1, pg2)
        lpg2 = Part.LineSegment(pg2, pg3)
        lpg3 = Part.LineSegment(pg3, pg4)
        lpg4 = Part.LineSegment(pg4, pg5)
        lpg5 = Part.LineSegment(pg5, pg6)
        lpg6 = Part.LineSegment(pg6, pg7)
        lpg7 = Part.LineSegment(pg7, pg8)
        lpg8 = Part.LineSegment(pg8, pg1)
        #  ---- Creamos Cara Polígono Grande
        SG = Part.Shape([lpg1, lpg2, lpg3, lpg4, lpg5, lpg6, lpg7, lpg8])
        WG = Part.Wire(SG.Edges)
        FG = Part.Face(WG)
        #  ---- Creamos lineas Polígono Pequeño
        lpp1 = Part.LineSegment(pp1, pp2)
        lpp2 = Part.LineSegment(pp2, pp3)
        lpp3 = Part.LineSegment(pp3, pp4)
        lpp4 = Part.LineSegment(pp4, pp5)
        lpp5 = Part.LineSegment(pp5, pp6)
        lpp6 = Part.LineSegment(pp6, pp7)
        lpp7 = Part.LineSegment(pp7, pp8)
        lpp8 = Part.LineSegment(pp8, pp1)
        #  ---- Creamos Cara Polígono Pequeño
        SP = Part.Shape([lpp1, lpp2, lpp3, lpp4, lpp5, lpp6, lpp7, lpp8])
        WP = Part.Wire(SP.Edges)
        FP = Part.Face(WP)
        #  ---- Creamos lineas Caras inclinadas
        lincl1 = Part.LineSegment(pg1, pp1)
        lincl2 = Part.LineSegment(pg2, pp2)
        lincl3 = Part.LineSegment(pg3, pp3)
        lincl4 = Part.LineSegment(pg4, pp4)
        lincl5 = Part.LineSegment(pg5, pp5)
        lincl6 = Part.LineSegment(pg6, pp6)
        lincl7 = Part.LineSegment(pg7, pp7)
        lincl8 = Part.LineSegment(pg8, pp8)
        #  ---- Creamos Caras Inclinadas
        sincl1 = Part.Shape([lincl1, lpg1, lincl2, lpp1])
        wincl1 = Part.Wire(sincl1.Edges)
        fincl1 = Part.Face(wincl1)
        sincl2 = Part.Shape([lincl2, lpg2, lincl3, lpp2])
        wincl2 = Part.Wire(sincl2.Edges)
        fincl2 = Part.Face(wincl2)
        sincl3 = Part.Shape([lincl3, lpg3, lincl4, lpp3])
        wincl3 = Part.Wire(sincl3.Edges)
        fincl3 = Part.Face(wincl3)
        sincl4 = Part.Shape([lincl4, lpg4, lincl5, lpp4])
        wincl4 = Part.Wire(sincl4.Edges)
        fincl4 = Part.Face(wincl4)
        sincl5 = Part.Shape([lincl5, lpg5, lincl6, lpp5])
        wincl5 = Part.Wire(sincl5.Edges)
        fincl5 = Part.Face(wincl5)
        sincl6 = Part.Shape([lincl6, lpg6, lincl7, lpp6])
        wincl6 = Part.Wire(sincl6.Edges)
        fincl6 = Part.Face(wincl6)
        sincl7 = Part.Shape([lincl7, lpg7, lincl8, lpp7])
        wincl7 = Part.Wire(sincl7.Edges)
        fincl7 = Part.Face(wincl7)
        sincl8 = Part.Shape([lincl8, lpg8, lincl1, lpp8])
        wincl8 = Part.Wire(sincl8.Edges)
        fincl8 = Part.Face(wincl8)
        ###  ----- Hacemos cuerpo Sólido cone Central
        t_cone = Part.makeShell(
            [FG, fincl1, fincl2, fincl3, fincl4, fincl5, fincl6, fincl7, fincl8, FP]
        )
        #   ----  Junto las caras
        cone = Part.makeSolid(t_cone)
        #   ----  Genero agujeritos de r=1
        hole = Part.makeCylinder(1, 20, FreeCAD.Vector(-10, 0, 1.5675), FreeCAD.Vector(1, 0, 0))
        cone = cone.cut(hole)
        hole = Part.makeCylinder(1, 20, FreeCAD.Vector(0, -10, 1.5675), FreeCAD.Vector(0, 1, 0))
        cone = cone.cut(hole)
        return cone

    def add_cones(self, shape: Part.Shape):
        if self.connectors[0]:
            cone1 = self.create_cone()
            cone1.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 90)
            cone1.translate(FreeCAD.Vector(BU_FIVE_QUARTERS / 2, 0, 0))
            shape = shape.fuse(cone1)

        if self.connectors[1]:
            cone2 = self.create_cone()
            cone2.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), -90)
            cone2.translate(FreeCAD.Vector(0, BU_FIVE_QUARTERS / 2, 0))
            shape = shape.fuse(cone2)

        if self.connectors[2]:
            cone3 = self.create_cone()
            cone3.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), -90)
            cone3.translate(FreeCAD.Vector(-BU_FIVE_QUARTERS / 2, 0, 0))
            shape = shape.fuse(cone3)

        if self.connectors[3]:
            cone4 = self.create_cone()
            cone4.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 90)
            cone4.translate(FreeCAD.Vector(0, -BU_FIVE_QUARTERS / 2, 0))
            shape = shape.fuse(cone4)

        ###  ---- Hago los Agujeros centrales
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(0, -15, 0), FreeCAD.Vector(0, 1, 0))
        shape = shape.cut(Agujero)
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(-15, 0, 0), FreeCAD.Vector(1, 0, 0))
        shape = shape.cut(Agujero)
        # Refinamos el cuerpo
        # shape = shape.removeSplitter()
        return shape

    def execute(self, obj):
        obj.Code = self.code
        obj.Shape = self.add_cones(self.create_cube())


class TRH_H_BEM_SFT_1W(CONN):
    """Conector en 1 cara STEMFIE"""

    def __init__(self, obj):
        super().__init__(obj)
        obj.Proxy = self
        self.connectors = [True, False, False, False]
        self.code = "TRH_H_BEM_SFT_1W"


class TRH_H_BEM_SFT_2W_180(CONN):
    """Conector en 2 caras opuestas STEMFIE"""

    def __init__(self, obj):
        super().__init__(obj)
        obj.Proxy = self
        self.connectors = [True, False, True, False]
        self.code = "TRH_H_BEM_SFT_2W_180"


class TRH_H_BEM_SFT_2W_90(CONN):
    """Conector en 2 caras contiguas STEMFIE"""

    def __init__(self, obj):
        """Initialize connector object."""
        super().__init__(obj)
        obj.Proxy = self
        self.connectors = [True, True, False, False]
        self.code = "TRH_H_BEM_SFT_2W_90"


class TRH_H_BEM_SFT_3W(CONN):
    """Conector en 3 caras contiguas STEMFIE"""

    def __init__(self, obj):
        super().__init__(obj)
        obj.Proxy = self
        self.connectors = [True, True, True, False]
        self.code = "TRH_H_BEM_SFT_3W"


class TRH_H_BEM_SFT_4W(CONN):
    """Conector en las 4 caras STEMFIE"""

    def __init__(self, obj):
        super().__init__(obj)
        obj.Proxy = self
        self.connectors = [True, True, True, True]
        self.code = "TRH_H_BEM_SFT_4W"
