#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# #####################################################################################
#         -------------    Piezas.py   ---------------------------
#  Este codigo contiene la geometria y propiedades de las piezas de Stemfie
#
#  Realizado por: Ander González
#  Socio BilbaoMaker #53
#  Fecha : 04-05-2021
#####################################################################################

import FreeCAD
import Part

from freecad.stemfie import Braces, Connectors

translate = FreeCAD.Qt.translate
QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP


# Brazos


# Vigas
class STR_ESS:
    """Beam - Straight - Ending Square/Square
    Viga Simple Stemfie"""

    def __init__(self, obj):
        obj.Proxy = self
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
            QT_TRANSLATE_NOOP("App::Property", "Holes number for part\nMinimum = 1"),
        ).HolesNumber = 4

    def execute(self, obj):
        # Compruebo que Numero_Agujeros mayor de 1
        if obj.HolesNumber < 1:
            obj.HolesNumber = 1

        # Genero el cuerpo exterior
        P = Part.makeBox(
            (obj.HolesNumber * 12.5),
            12.5,
            12.5,
            FreeCAD.Vector(-6.25, -6.25, -6.25),
            FreeCAD.Vector(0, 0, 1),
        )
        #  ---- Bucle para agujeros en X
        for x in range(obj.HolesNumber):
            Agujero = Part.makeCylinder(
                3.5, 20, FreeCAD.Vector(x * 12.5, 0, -10), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut(Agujeros)
        #  ---- Bucle para agujeros en Y
        for x in range(obj.HolesNumber):
            Agujero = Part.makeCylinder(
                3.5, 20, FreeCAD.Vector(x * 12.5, -10, 0), FreeCAD.Vector(0, 1, 0)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut(Agujeros)
        #  ---- Agujeros en Z
        Agujero = Part.makeCylinder(
            3.5, (obj.HolesNumber * 12.5) + 25, FreeCAD.Vector(-10, 0, 0), FreeCAD.Vector(1, 0, 0)
        )
        P = P.cut(Agujero)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "STR_ESS_BU-" + str(obj.HolesNumber) + "x01x01"

        P.Placement = obj.Placement
        obj.Shape = P


class STR_ERR:
    """Beam - Straight - Ending Round/Round

      ________________
     /                 \_
    |   ()    ()    ()  |
     \ _______________ /

         1     2     3
          --------->
           HolesNumber

      Variables:
          Codigo          'Demoninacion'
          HolesNumber      'Numero Agujeros que contiene la pieza

    """

    def __init__(self, obj):
        obj.Proxy = self
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
            QT_TRANSLATE_NOOP("App::Property", "Holes number for simple part\nMinimum = 3"),
        ).HolesNumber = 5

    def execute(self, obj):
        # Compruebo que HolesNumber mayor de 3
        if obj.HolesNumber < 3:
            obj.HolesNumber = 3

        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector((obj.HolesNumber - 1) * 12.5, -6.25, 0)
        P3 = FreeCAD.Vector((obj.HolesNumber - 1) * 12.5, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.HolesNumber - 1) * 12.5) + 6.25, 0, 0)
        PC4 = FreeCAD.Vector(-6.25, 0, 0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1, P2)
        C2 = Part.Arc(P2, PC2, P3)
        L3 = Part.LineSegment(P3, P4)
        C4 = Part.Arc(P4, PC4, P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1, C2, L3, C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude(FreeCAD.Vector(0, 0, 12.5))
        #  ---- Bucle para agujeros superiores
        for x in range(obj.HolesNumber):
            Agujero = Part.makeCylinder(
                3.5, 15, FreeCAD.Vector(x * 12.5, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut(Agujeros)
        #  ---- Bucle para agujeros superiores
        for x in range(obj.HolesNumber - 2):
            Agujero = Part.makeCylinder(
                3.5, 15, FreeCAD.Vector((x * 12.5) + 12.5, -7, 6.25), FreeCAD.Vector(0, 1, 0)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut(Agujeros)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "STR ERR-BU" + str(obj.HolesNumber) + "x01x00.25"

        P.Placement = obj.Placement
        obj.Shape = P


class STR_BEM:
    """Viga Cubo Stemfie"""

    def __init__(self, obj):
        obj.Proxy = self
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
            QT_TRANSLATE_NOOP("App::Property", "Holes number in X\nMinimum = 1"),
        )
        obj.HolesNumberX = 2
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in Y\nMinimum = 1"),
        )
        obj.HolesNumberY = 2
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberZ"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in Z\nMinimum = 1"),
        )
        obj.HolesNumberZ = 2

    def execute(self, obj):
        # Compruebo que Numero_Agujeros mayor de 1
        if (obj.HolesNumberX < 1) or (obj.HolesNumberY < 1) or (obj.HolesNumberZ < 1):
            if obj.HolesNumberX < 1:
                obj.HolesNumberX = 1
            if obj.HolesNumberY < 1:
                obj.HolesNumberY = 1
            if obj.HolesNumberZ < 1:
                obj.HolesNumberZ = 1

        # Genero el cuerpo exterior
        P = Part.makeBox(
            (obj.HolesNumberX * 12.5),
            (obj.HolesNumberY * 12.5),
            (obj.HolesNumberZ * 12.5),
            FreeCAD.Vector(-6.25, -6.25, -6.25),
            FreeCAD.Vector(0, 0, 1),
        )
        #  ---- Bucle para agujeros en X
        for x in range(obj.HolesNumberX):
            for y in range(obj.HolesNumberY):
                Agujero = Part.makeCylinder(
                    3.5,
                    (obj.HolesNumberZ * 12.5) + 20,
                    FreeCAD.Vector(x * 12.5, y * 12.5, -10),
                    FreeCAD.Vector(0, 0, 1),
                )
                if (y == 0) and (x == 0):
                    AgujerosX = Agujero
                else:
                    AgujerosX = AgujerosX.fuse(Agujero)

        #  ---- Bucle para agujeros en Y
        for x in range(obj.HolesNumberX):
            for z in range(obj.HolesNumberZ):
                Agujero = Part.makeCylinder(
                    3.5,
                    (obj.HolesNumberY * 12.5) + 20,
                    FreeCAD.Vector(x * 12.5, -10, z * 12.5),
                    FreeCAD.Vector(0, 1, 0),
                )
                if (z == 0) and (x == 0):
                    AgujerosY = Agujero
                else:
                    AgujerosY = AgujerosY.fuse(Agujero)

        #  ---- Agujeros en Z
        for z in range(obj.HolesNumberZ):
            for y in range(obj.HolesNumberY):
                Agujero = Part.makeCylinder(
                    3.5,
                    (obj.HolesNumberX * 12.5) + 20,
                    FreeCAD.Vector(-10, y * 12.5, z * 12.5),
                    FreeCAD.Vector(1, 0, 0),
                )
                if (y == 0) and (z == 0):
                    AgujerosZ = Agujero
                else:
                    AgujerosZ = AgujerosZ.fuse(Agujero)

        Agujeros = AgujerosX.fuse(AgujerosY)
        Agujeros = Agujeros.fuse(AgujerosZ)
        P = P.cut(Agujeros)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            "STR_BEM-"
            + str(obj.HolesNumberX)
            + "x"
            + str(obj.HolesNumberY)
            + "x"
            + str(obj.HolesNumberZ)
        )

        P.Placement = obj.Placement
        obj.Shape = P


class AGD_ESS_USH_SYM:
    """Viga Stemfie con brazos a 90º en los estremos"""

    def __init__(self, obj):
        obj.Proxy = self
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
            QT_TRANSLATE_NOOP("App::Property", "Holes number for part in X\nMinimum = 3"),
        )
        obj.HolesNumberX = 3
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY1"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in left vertical bar\nMinimum = 1"),
        )
        obj.HolesNumberY1 = 2
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY2"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in right vertical bar\nMinimum = 1"),
        )
        obj.HolesNumberY2 = 2

    def execute(self, obj):
        # Compruebo Valores
        if (obj.HolesNumberX < 3) or (obj.HolesNumberY1 < 1) or (obj.HolesNumberY2 < 1):
            if obj.HolesNumberX < 3:
                obj.HolesNumberX = 3
            if obj.HolesNumberY1 < 1:
                obj.HolesNumberY1 = 1
            if obj.HolesNumberY2 < 1:
                obj.HolesNumberY2 = 1

        # Genero el cuerpo exterior
        P = Part.makeBox(
            (obj.HolesNumberX * 12.5),
            12.5,
            12.5,
            FreeCAD.Vector(-6.25, -6.25, -6.25),
            FreeCAD.Vector(0, 0, 1),
        )
        PY1 = Part.makeBox(
            12.5,
            ((obj.HolesNumberY1 + 1) * 12.5),
            12.5,
            FreeCAD.Vector(-6.25, -6.25, -6.25),
            FreeCAD.Vector(0, 0, 1),
        )
        PY2 = Part.makeBox(
            12.5,
            ((obj.HolesNumberY2 + 1) * 12.5),
            12.5,
            FreeCAD.Vector(((obj.HolesNumberX - 1) * 12.5) - 6.25, -6.25, -6.25),
            FreeCAD.Vector(0, 0, 1),
        )
        P = P.fuse(PY1)
        P = P.fuse(PY2)

        #  Genero los agujeros de la parte central
        #  ---- Bucle para agujeros en cara X
        for x in range(obj.HolesNumberX):
            Agujero = Part.makeCylinder(
                3.5, 20, FreeCAD.Vector(x * 12.5, 0, -10), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                AgujerosX = Agujero
            else:
                AgujerosX = AgujerosX.fuse(Agujero)

        for y in range(obj.HolesNumberY1):
            Agujero = Part.makeCylinder(
                3.5, 20, FreeCAD.Vector(0, (y * 12.5) + 12.5, -10), FreeCAD.Vector(0, 0, 1)
            )
            if y == 0:
                AgujerosY1 = Agujero
            else:
                AgujerosY1 = AgujerosY1.fuse(Agujero)

        for y in range(obj.HolesNumberY2):
            Agujero = Part.makeCylinder(
                3.5,
                20,
                FreeCAD.Vector(((obj.HolesNumberX - 1) * 12.5), (y * 12.5) + 12.5, -10),
                FreeCAD.Vector(0, 0, 1),
            )
            if y == 0:
                AgujerosY2 = Agujero
            else:
                AgujerosY2 = AgujerosY2.fuse(Agujero)

        Agujeros = AgujerosX.fuse(AgujerosY1)
        Agujeros = Agujeros.fuse(AgujerosY2)
        P = P.cut(Agujeros)

        #  ---- Bucle para agujeros en cara Z
        for y in range(obj.HolesNumberX):
            if y == 0:
                Longitud = (obj.HolesNumberY1) * 12.5
            if y == obj.HolesNumberX - 1:
                Longitud = (obj.HolesNumberY2) * 12.5
            if (y > 0) and (y < obj.HolesNumberX - 1):
                Longitud = 0

            Agujero = Part.makeCylinder(
                3.5, Longitud + 20, FreeCAD.Vector(y * 12.5, -10, 0), FreeCAD.Vector(0, 1, 0)
            )
            if y == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut(Agujeros)
        #  ---- Bucle para agujeros en cara Y
        if (obj.HolesNumberY1) >= (obj.HolesNumberY2):
            repeticion = obj.HolesNumberY1
        else:
            repeticion = obj.HolesNumberY2

        for x in range(repeticion + 1):
            Agujero = Part.makeCylinder(
                3.5,
                (obj.HolesNumberX * 12.5) + 25,
                FreeCAD.Vector(-10, (x * 12.5), 0),
                FreeCAD.Vector(1, 0, 0),
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut(Agujeros)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            "AGD_ESS_USH_SYM-"
            + str(obj.HolesNumberY1)
            + "x"
            + str(obj.HolesNumberX)
            + "x"
            + str(obj.HolesNumberY2)
        )

        P.Placement = obj.Placement
        obj.Shape = P


class STR_DBL:
    """Viga Angular Stemfie"""

    def __init__(self, obj):
        obj.Proxy = self
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
            QT_TRANSLATE_NOOP("App::Property", "Holes number for part in X\nMinimum = 2"),
        )
        obj.HolesNumberX = 3
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in angular bar\nMinimum = 1"),
        )
        obj.HolesNumberY = 2
        obj.addProperty(
            "App::PropertyAngle",
            QT_TRANSLATE_NOOP("App::Property", "Angle"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Angle\nMinimum = 90°\nMaximum = 180°"),
        )
        obj.Angle = 135

    def execute(self, obj):
        # Compruebo Valores
        if (
            (obj.HolesNumberX < 2)
            or (obj.HolesNumberY < 1)
            or (obj.Angle < 90)
            or (obj.Angle > 180)
        ):
            if obj.HolesNumberX < 2:
                obj.HolesNumberX = 2
            if obj.HolesNumberY < 1:
                obj.HolesNumberY = 1
            if obj.Angle < 90:
                obj.Angle = 90
            if obj.Angle > 180:
                obj.Angle = 180

        # Genero el cuerpo exterior
        P = Part.makeBox(
            ((obj.HolesNumberX - 1) * 12.5) + 6.25,
            12.5,
            12.5,
            FreeCAD.Vector(0, -6.25, -6.25),
            FreeCAD.Vector(0, 0, 1),
        )
        Curva = Part.makeCylinder(6.25, 12.5, FreeCAD.Vector(0, 0, -6.25), FreeCAD.Vector(0, 0, 1))
        P = P.fuse(Curva)

        #  Genero los agujeros en el cuerpo principal
        #  ---- Bucle para agujeros en cara X
        for x in range(obj.HolesNumberX):
            Agujero = Part.makeCylinder(
                3.5, 20, FreeCAD.Vector(x * 12.5, 0, -10), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                AgujerosX = Agujero
            else:
                AgujerosX = AgujerosX.fuse(Agujero)

        #  ---- Bucle para agujeros en cara Z
        for x in range(obj.HolesNumberX - 1):
            Agujero = Part.makeCylinder(
                3.5, 20, FreeCAD.Vector((x * 12.5) + 12.5, -10, 0), FreeCAD.Vector(0, 1, 0)
            )
            if x == 0:
                AgujerosY = Agujero
            else:
                AgujerosY = AgujerosY.fuse(Agujero)
        #  ---- Sumo los agujeros
        Agujeros = AgujerosX.fuse(AgujerosY)
        #  ---- Se los resto al cuerpo
        P = P.cut(Agujeros)

        #  Genero cuerpo para luego girar
        PY1 = Part.makeBox(
            ((obj.HolesNumberY) * 12.5) + 6.25,
            12.5,
            12.5,
            FreeCAD.Vector(0, -6.25, -6.25),
            FreeCAD.Vector(0, 0, 1),
        )
        #  Genero los agujeros en el cuerpo a girar
        #  ---- Bucle para agujeros en cara X
        for x in range(obj.HolesNumberY + 1):
            Agujero = Part.makeCylinder(
                3.5, 20, FreeCAD.Vector(x * 12.5, 0, -10), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                AgujerosX = Agujero
            else:
                AgujerosX = AgujerosX.fuse(Agujero)

        #  ---- Bucle para agujeros en cara Z
        for x in range(obj.HolesNumberY):
            Agujero = Part.makeCylinder(
                3.5, 20, FreeCAD.Vector((x * 12.5) + 12.5, -10, 0), FreeCAD.Vector(0, 1, 0)
            )
            if x == 0:
                AgujerosY = Agujero
            else:
                AgujerosY = AgujerosY.fuse(Agujero)
        #  ---- Sumo los agujeros
        Agujeros = AgujerosX.fuse(AgujerosY)
        #  ---- Se los resto al cuerpo
        PY1 = PY1.cut(Agujeros)
        #  Giro pieza
        PY1.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), obj.Angle)
        # Uno las dos partes
        P = P.fuse(PY1)

        #   ----- Ahora que estan girados hago los circulos centrales y los resto
        #   ----- Agujero en X
        Agujero1 = Part.makeCylinder(
            3.5,
            (obj.HolesNumberX * 12.5) + ((obj.HolesNumberY + 1) * 12.5) + 12.5,
            FreeCAD.Vector(((obj.HolesNumberY + 1) * -12.5), 0, 0),
            FreeCAD.Vector(1, 0, 0),
        )
        #   ----- Agujero en Inclinado
        Agujero2 = Part.makeCylinder(
            3.5,
            (obj.HolesNumberX + obj.HolesNumberY + 2) * 12.5,
            FreeCAD.Vector(((obj.HolesNumberX + 1) * -12.5), 0, 0),
            FreeCAD.Vector(1, 0, 0),
        )
        Agujero2.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), obj.Angle)

        Agujeros = Agujero1.fuse(Agujero2)
        P = P.cut(Agujeros)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            "STR_DBL-" + str(obj.HolesNumberX) + "x" + str(obj.HolesNumberY) + " " + str(obj.Angle)
        )

        P.Placement = obj.Placement
        obj.Shape = P


class STR_TRPL:
    """Viga Stemfie con brazos en los extremos Angulo variable"""

    def __init__(self, obj):
        obj.Proxy = self
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
            QT_TRANSLATE_NOOP("App::Property", "Holes number in central bar\nMinimum = 3"),
        )
        obj.HolesNumberX = 3
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY1"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in left angular bar\nMinimum = 1"),
        )
        obj.HolesNumberY1 = 2
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY2"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in right angular bar\nMinimum = 1"),
        )
        obj.HolesNumberY2 = 2
        obj.addProperty(
            "App::PropertyAngle",
            QT_TRANSLATE_NOOP("App::Property", "Angle"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Angle\nMinimum = 90°\nMaximum = 180°"),
        )
        obj.Angle = 135

    def execute(self, obj):
        # Compruebo Valores
        if (
            (obj.HolesNumberX < 3)
            or (obj.HolesNumberY1 < 1)
            or (obj.HolesNumberY2 < 1)
            or (obj.Angle < 90)
            or (obj.Angle > 180)
        ):
            if obj.HolesNumberX < 3:
                obj.HolesNumberX = 3
            if obj.HolesNumberY1 < 1:
                obj.HolesNumberY1 = 1
            if obj.HolesNumberY2 < 1:
                obj.HolesNumberY2 = 1
            if obj.Angle < 90:
                obj.Angle = 90
            if obj.Angle > 180:
                obj.Angle = 180

        # Genero el cuerpo exterior
        P = Part.makeBox(
            ((obj.HolesNumberX - 1) * 12.5),
            12.5,
            12.5,
            FreeCAD.Vector(0, -6.25, -6.25),
            FreeCAD.Vector(0, 0, 1),
        )
        Curva = Part.makeCylinder(6.25, 12.5, FreeCAD.Vector(0, 0, -6.25), FreeCAD.Vector(0, 0, 1))
        P = P.fuse(Curva)
        Curva = Part.makeCylinder(
            6.25,
            12.5,
            FreeCAD.Vector((obj.HolesNumberX - 1) * 12.5, 0, -6.25),
            FreeCAD.Vector(0, 0, 1),
        )
        P = P.fuse(Curva)

        #  Genero los agujeros en el cuerpo principal
        #  ---- Bucle para agujeros en cara X
        for x in range(obj.HolesNumberX):
            Agujero = Part.makeCylinder(
                3.5, 20, FreeCAD.Vector(x * 12.5, 0, -10), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                AgujerosX = Agujero
            else:
                AgujerosX = AgujerosX.fuse(Agujero)
        #  ---- Bucle para agujeros en cara Z
        for x in range(obj.HolesNumberX - 2):
            Agujero = Part.makeCylinder(
                3.5, 20, FreeCAD.Vector((x * 12.5) + 12.5, -10, 0), FreeCAD.Vector(0, 1, 0)
            )
            if x == 0:
                AgujerosY = Agujero
            else:
                AgujerosY = AgujerosY.fuse(Agujero)
        #  ---- Sumo los agujeros
        Agujeros = AgujerosX.fuse(AgujerosY)
        #  ---- Se los resto al cuerpo
        P = P.cut(Agujeros)

        #  Genero cuerpo Izquierda
        PY1 = Part.makeBox(
            ((obj.HolesNumberY1) * 12.5) + 6.25,
            12.5,
            12.5,
            FreeCAD.Vector(0, -6.25, -6.25),
            FreeCAD.Vector(0, 0, 1),
        )
        #  Genero los agujeros en el cuerpo a girar
        #  ---- Bucle para agujeros en cara X
        for x in range(obj.HolesNumberY1 + 1):
            Agujero = Part.makeCylinder(
                3.5, 20, FreeCAD.Vector(x * 12.5, 0, -10), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                AgujerosX = Agujero
            else:
                AgujerosX = AgujerosX.fuse(Agujero)
        #  ---- Bucle para agujeros en cara Z
        for x in range(obj.HolesNumberY1):
            Agujero = Part.makeCylinder(
                3.5, 20, FreeCAD.Vector((x * 12.5) + 12.5, -10, 0), FreeCAD.Vector(0, 1, 0)
            )
            if x == 0:
                AgujerosY = Agujero
            else:
                AgujerosY = AgujerosY.fuse(Agujero)
        #  ---- Sumo los agujeros
        Agujeros = AgujerosX.fuse(AgujerosY)
        #  ---- Se los resto al cuerpo
        PY1 = PY1.cut(Agujeros)
        #  Giro pieza
        PY1.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), obj.Angle)
        # Uno las dos partes
        P = P.fuse(PY1)
        #  Genero cuerpo Derecha
        PY2 = Part.makeBox(
            ((obj.HolesNumberY2) * 12.5) + 6.25,
            12.5,
            12.5,
            FreeCAD.Vector((obj.HolesNumberX - 1) * 12.5, -6.25, -6.25),
            FreeCAD.Vector(0, 0, 1),
        )
        #  Genero los agujeros en el cuerpo a girar
        #  ---- Bucle para agujeros en cara X
        for x in range(obj.HolesNumberY2 + 1):
            Agujero = Part.makeCylinder(
                3.5,
                20,
                FreeCAD.Vector(((obj.HolesNumberX - 1) * 12.5) + x * 12.5, 0, -10),
                FreeCAD.Vector(0, 0, 1),
            )
            if x == 0:
                AgujerosX = Agujero
            else:
                AgujerosX = AgujerosX.fuse(Agujero)
        #  ---- Bucle para agujeros en cara Z
        for x in range(obj.HolesNumberY2):
            Agujero = Part.makeCylinder(
                3.5,
                20,
                FreeCAD.Vector(((obj.HolesNumberX - 1) * 12.5) + (x * 12.5) + 12.5, -10, 0),
                FreeCAD.Vector(0, 1, 0),
            )
            if x == 0:
                AgujerosY = Agujero
            else:
                AgujerosY = AgujerosY.fuse(Agujero)
        #  ---- Sumo los agujeros
        Agujeros = AgujerosX.fuse(AgujerosY)
        #  ---- Se los resto al cuerpo
        PY2 = PY2.cut(Agujeros)
        #  Giro pieza
        PY2.rotate(
            FreeCAD.Vector(((obj.HolesNumberX - 1) * 12.5), 0, 0),
            FreeCAD.Vector(0, 0, 1),
            180 - int(obj.Angle),
        )
        # Uno las dos partes
        P = P.fuse(PY2)

        #   ----- Ahora que estan girados, hago los circulos centrales y los resto
        #   ----- Agujero en X
        Agujero = Part.makeCylinder(
            3.5,
            (obj.HolesNumberX + obj.HolesNumberY1 + obj.HolesNumberY2 + 2) * 12.5,
            FreeCAD.Vector(((obj.HolesNumberY1 + 1) * -12.5), 0, 0),
            FreeCAD.Vector(1, 0, 0),
        )
        P = P.cut(Agujero)
        #   ----- Agujero en Inclinado Y1
        Agujero = Part.makeCylinder(
            3.5,
            (obj.HolesNumberX + obj.HolesNumberY1 + 2) * 12.5,
            FreeCAD.Vector(((obj.HolesNumberX + 1) * -12.5), 0, 0),
            FreeCAD.Vector(1, 0, 0),
        )
        Agujero.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), obj.Angle)
        P = P.cut(Agujero)
        #   ----- Agujero en Inclinado Y2
        Agujero = Part.makeCylinder(
            3.5,
            (obj.HolesNumberX + obj.HolesNumberY2 + 2) * 12.5,
            FreeCAD.Vector(0, 0, 0),
            FreeCAD.Vector(1, 0, 0),
        )
        Agujero.rotate(
            FreeCAD.Vector(((obj.HolesNumberX - 1) * 12.5), 0, 0),
            FreeCAD.Vector(0, 0, 1),
            180 - int(obj.Angle),
        )
        P = P.cut(Agujero)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            "STR_TRPL-"
            + str(obj.HolesNumberY1)
            + "x"
            + str(obj.HolesNumberX)
            + str(obj.HolesNumberY2)
            + " "
            + str(obj.Angle)
        )

        P.Placement = obj.Placement
        obj.Shape = P


class STR_BXS_ESS_H:
    """Viga hueca Stemfie"""

    def __init__(self, obj):
        obj.Proxy = self
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
        )
        obj.HolesNumber = 1

    def execute(self, obj):
        # Compruebo Valores
        if obj.HolesNumber < 1:
            obj.HolesNumber = 1

        # Genero el cuerpo exterior
        P = Part.makeBox(
            obj.HolesNumber * 12.5,
            12.5,
            12.5,
            FreeCAD.Vector(0, -6.25, -6.25),
            FreeCAD.Vector(0, 0, 1),
        )

        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        Cubo = Part.makeBox(
            ((obj.HolesNumber - 1) * 12.5) + 6.25,
            9.375,
            20,
            FreeCAD.Vector(3.125, -4.6875, -10),
            FreeCAD.Vector(0, 0, 1),
        )
        P = P.cut(Cubo)
        #  ---- Agujero
        Agujero = Part.makeCylinder(
            3.5, (obj.HolesNumber * 12.5) + 20, FreeCAD.Vector(-10, 0, 0), FreeCAD.Vector(1, 0, 0)
        )
        P = P.cut(Agujero)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "STR_BXS_ESS_H-" + str(obj.HolesNumber)

        P.Placement = obj.Placement
        obj.Shape = P


class STR_BXS_ESS_C:
    """Viga hueca Stemfie con dado en los extremos"""

    def __init__(self, obj):
        obj.Proxy = self
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
            QT_TRANSLATE_NOOP("App::Property", "Holes number\nMinimum = 3"),
        )
        obj.HolesNumber = 3

    def execute(self, obj):
        # Compruebo Valores
        if obj.HolesNumber < 3:
            obj.HolesNumber = 3

        # Genero el cuerpo exterior
        P = Part.makeBox(
            obj.HolesNumber * 12.5,
            12.5,
            12.5,
            FreeCAD.Vector(0, -6.25, -6.25),
            FreeCAD.Vector(0, 0, 1),
        )

        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        Cubo = Part.makeBox(
            ((obj.HolesNumber - 2) * 12.5),
            9.375,
            20,
            FreeCAD.Vector(12.5, -4.6875, -10),
            FreeCAD.Vector(0, 0, 1),
        )
        P = P.cut(Cubo)
        #  ---- Agujero Longitudinal
        Agujero = Part.makeCylinder(
            3.5, (obj.HolesNumber * 12.5) + 20, FreeCAD.Vector(-10, 0, 0), FreeCAD.Vector(1, 0, 0)
        )
        P = P.cut(Agujero)
        #  ---- Agujero Cubo Inicio cara X
        Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector(6.25, -10, 0), FreeCAD.Vector(0, 1, 0))
        P = P.cut(Agujero)
        #  ---- Agujero Cubo Final cara X
        Agujero = Part.makeCylinder(
            3.5,
            20,
            FreeCAD.Vector(((obj.HolesNumber - 1) * 12.5) + 6.25, -10, 0),
            FreeCAD.Vector(0, 1, 0),
        )
        P = P.cut(Agujero)
        #  ---- Agujero Cubo Inicio cara Z
        Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector(6.25, 0, -10), FreeCAD.Vector(0, 0, 1))
        P = P.cut(Agujero)
        #  ---- Agujero Cubo Final cara Z
        Agujero = Part.makeCylinder(
            3.5,
            20,
            FreeCAD.Vector(((obj.HolesNumber - 1) * 12.5) + 6.25, 0, -10),
            FreeCAD.Vector(0, 0, 1),
        )
        P = P.cut(Agujero)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "STR_BXS_ESS_C-" + str(obj.HolesNumber)

        P.Placement = obj.Placement
        obj.Shape = P


# NOTE: Classes below this chunk are kept for migration purposes.
# The migration method used is "Method 2. Migration when restoring the document"
# from: https://wiki.freecad.org/Scripted_objects_migration
# The view provider is not changed.

msg = translate("Log", "Object migration was successful, using new proxy class.\n")

# Beams

# NOTE: Braces-migration section


class STR_STD_ERR:
    def onDocumentRestored(self, obj):
        Braces.STR_STD_ERR(obj)
        FreeCAD.Console.PrintWarning(msg)


class CRN_ERR_ASYM:
    def onDocumentRestored(self, obj):
        Braces.CRN_ERR_ASYM(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_STD_SQR_AY:
    def onDocumentRestored(self, obj):
        Braces.STR_STD_SQR_AY(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_SLT_BE_SYM_ERR:
    def onDocumentRestored(self, obj):
        Braces.STR_SLT_BE_SYM_ERR(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_SLT_CNT_ERR:
    def onDocumentRestored(self, obj):
        Braces.STR_SLT_CNT_ERR(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_SLT_FL_ERR:
    def onDocumentRestored(self, obj):
        Braces.STR_SLT_FL_ERR(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_SLT_SE_ERR:
    def onDocumentRestored(self, obj):
        Braces.STR_SLT_SE_ERR(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_STD_DBL_AZ:
    def onDocumentRestored(self, obj):
        Braces.STR_STD_DBL_AZ(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_STD_DBL_AY:
    def onDocumentRestored(self, obj):
        Braces.STR_STD_DBL_AY(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_STD_TRPL_AZ:
    def onDocumentRestored(self, obj):
        Braces.STR_STD_TRPL_AZ(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_STD_TRPL_AY:
    def onDocumentRestored(self, obj):
        Braces.STR_STD_TRPL_AY(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_STD_CRS:
    def onDocumentRestored(self, obj):
        Braces.STR_STD_CRS(obj)
        FreeCAD.Console.PrintWarning(msg)


# NOTE: Connectors-migration section


class TRH_H_BEM_SFT_1W:
    def onDocumentRestored(self, obj):
        Connectors.BEM_TRH_H_SFT_1W(obj)
        FreeCAD.Console.PrintWarning(msg)


class TRH_H_BEM_SFT_2W_90:
    def onDocumentRestored(self, obj):
        Connectors.BEM_TRH_H_SFT_2W_90(obj)
        FreeCAD.Console.PrintWarning(msg)


class TRH_H_BEM_SFT_2W_180:
    def onDocumentRestored(self, obj):
        Connectors.BEM_TRH_H_SFT_2W_180(obj)
        FreeCAD.Console.PrintWarning(msg)


class TRH_H_BEM_SFT_3W:
    def onDocumentRestored(self, obj):
        Connectors.BEM_TRH_H_SFT_3W(obj)
        FreeCAD.Console.PrintWarning(msg)


class TRH_H_BEM_SFT_4W:
    def onDocumentRestored(self, obj):
        Connectors.BEM_TRH_H_SFT_4W(obj)
        FreeCAD.Console.PrintWarning(msg)
