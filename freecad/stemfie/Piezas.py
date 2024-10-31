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


translate = FreeCAD.Qt.translate
QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP


# Brazos
class STR_STD_ERR:
    """Brace - Straight - Ending Round Round

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
            QT_TRANSLATE_NOOP("App::Property", "Holes number for simple part\nMinimum = 1"),
        ).HolesNumber = 3

    def execute(self, obj):
        # Compruebo que HolesNumber mayor de 1
        if obj.HolesNumber < 1:
            obj.HolesNumber = 1
        # En caso de 1 agujero seria una arandela y no tendria rectas
        elif obj.HolesNumber == 1:
            P = Part.makeCylinder(6.25, 3.5, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector(0, 0, -1), FreeCAD.Vector(0, 0, 1))
            P = P.cut(Agujero)
        else:
            # Numero de agujeros mayor de 1
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
            P = F.extrude(FreeCAD.Vector(0, 0, 3.125))
            #  ---- Bucle para agujeros
            for x in range(obj.HolesNumber):
                Agujero = Part.makeCylinder(
                    3.5, 5, FreeCAD.Vector(x * 12.5, 0, -1), FreeCAD.Vector(0, 0, 1)
                )
                if x == 0:
                    Agujeros = Agujero
                else:
                    Agujeros = Agujeros.fuse(Agujero)
            P = P.cut(Agujeros)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "STR STD ERR-BU" + str(obj.HolesNumber) + "x01x00.25"

        P.Placement = obj.Placement
        obj.Shape = P


class STR_STD_BRD_AZ:
    """Brazo Angular Stemfie"""

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
            QT_TRANSLATE_NOOP("App::Property", "Holes number in X\nMinimum = 2"),
        ).HolesNumberX = 3
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in Y\nMinimum = 2"),
        ).HolesNumberY = 2
        obj.addProperty(
            "App::PropertyAngle",
            QT_TRANSLATE_NOOP("App::Property", "Angle"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Angle\nMinimum = 60°\nMaximum = 180°"),
        ).Angle = 60

    def execute(self, obj):
        # Compruebo que Numero_Agujeros mayor de 2 y Angulo en 60 y 180
        if (
            (obj.HolesNumberX < 2)
            or (obj.HolesNumberY < 2)
            or (obj.Angle < 60)
            or (obj.Angle > 180)
        ):
            if obj.HolesNumberX < 2:
                obj.HolesNumberX = 2
            if obj.HolesNumberY < 2:
                obj.HolesNumberY = 2
            if obj.Angle < 60:
                obj.Angle = 60
            if obj.Angle > 180:
                obj.Angle = 180

        # Genero Pieza en X
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector((obj.HolesNumberX - 1) * 12.5, -6.25, 0)
        P3 = FreeCAD.Vector((obj.HolesNumberX - 1) * 12.5, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.HolesNumberX - 1) * 12.5) + 6.25, 0, 0)
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
        PX = F.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberX):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector(x * 12.5, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PX = PX.cut(Agujeros)
        # Genero Pieza en Y
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector((obj.HolesNumberY - 1) * 12.5, -6.25, 0)
        P3 = FreeCAD.Vector((obj.HolesNumberY - 1) * 12.5, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.HolesNumberY - 1) * 12.5) + 6.25, 0, 0)
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
        PY = F.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberY):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector(x * 12.5, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PY = PY.cut(Agujeros)
        #  ---- Roto el brado inclinado
        PY.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), obj.Angle)
        #  ---- Uno las piezas
        P = PX.fuse(PY)
        #  ---- Refino la pieza
        P = P.removeSplitter()

        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            "STR STD BRD AZ-BU"
            + str(obj.HolesNumberX)
            + "x"
            + str(obj.HolesNumberY)
            + " "
            + str(obj.Angle)
        )

        P.Placement = obj.Placement
        obj.Shape = P


class CRN_ERR_ASYM:
    """Brazo Angulo 90º Stemfie"""

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
            QT_TRANSLATE_NOOP("App::Property", "Holes number in X\nMinimum = 2"),
        ).HolesNumberX = 3
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in Y\nMinimum = 2"),
        ).HolesNumberY = 2

    def execute(self, obj):
        # Compruebo que Numero_Agujeros mayor de 2
        if (obj.HolesNumberX < 2) or (obj.HolesNumberY < 2):
            if obj.HolesNumberX < 2:
                obj.HolesNumberX = 2
            if obj.HolesNumberY < 2:
                obj.HolesNumberY = 2

        # Genero Pieza en X
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector((obj.HolesNumberX - 1) * 12.5, -6.25, 0)
        P3 = FreeCAD.Vector((obj.HolesNumberX - 1) * 12.5, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.HolesNumberX - 1) * 12.5) + 6.25, 0, 0)
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
        PX = F.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberX):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector(x * 12.5, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PX = PX.cut(Agujeros)
        # Genero Pieza en Y
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector((obj.HolesNumberY - 1) * 12.5, -6.25, 0)
        P3 = FreeCAD.Vector((obj.HolesNumberY - 1) * 12.5, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.HolesNumberY - 1) * 12.5) + 6.25, 0, 0)
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
        PY = F.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberY):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector(x * 12.5, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PY = PY.cut(Agujeros)
        #  ---- Giramos la pieza
        PY.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 90)
        #  ---- Unimos las piezas
        P = PX.fuse(PY)
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "CRN ERR ASYM-BU" + str(obj.HolesNumberX) + "x" + str(obj.HolesNumberY) + "x0.25"

        P.Placement = obj.Placement
        obj.Shape = P


class STR_STD_BRM:
    """Plancha Cuadrada Stemfie"""

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
            QT_TRANSLATE_NOOP("App::Property", "Holes number in X\nMinimum = 2"),
        ).HolesNumberX = 4
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in Y\nMinimum = 2"),
        ).HolesNumberY = 3

    def execute(self, obj):
        import math

        # Compruebo que Numero_Agujeros mayor de 1
        if (obj.HolesNumberX < 2) or (obj.HolesNumberY < 2):
            if obj.HolesNumberX < 2:
                obj.HolesNumberX = 2
            if obj.HolesNumberY < 2:
                obj.HolesNumberY = 2
        else:
            # Numero de agujeros mayor de 2
            #  ---- Genero puntos de los contornos
            Pto1 = FreeCAD.Vector(0, -6.25, 0)
            Pto2 = FreeCAD.Vector((obj.HolesNumberX - 1) * 12.5, -6.25, 0)

            Pto3 = FreeCAD.Vector(((obj.HolesNumberX - 1) * 12.5) + 6.25, 0, 0)
            Pto4 = FreeCAD.Vector(
                ((obj.HolesNumberX - 1) * 12.5) + 6.25, (obj.HolesNumberY - 1) * 12.5, 0
            )

            Pto5 = FreeCAD.Vector(
                (obj.HolesNumberX - 1) * 12.5, ((obj.HolesNumberY - 1) * 12.5) + 6.25, 0
            )
            Pto6 = FreeCAD.Vector(0, ((obj.HolesNumberY - 1) * 12.5) + 6.25, 0)

            Pto7 = FreeCAD.Vector(-6.25, ((obj.HolesNumberY - 1) * 12.5), 0)
            Pto8 = FreeCAD.Vector(-6.25, 0, 0)
            #  ---- Genero puntos para circulos
            PtoC1 = FreeCAD.Vector(
                ((obj.HolesNumberX - 1) * 12.5) + (math.sin(0.7854) * 6.25),
                math.sin(0.7854) * -6.25,
                0,
            )
            PtoC2 = FreeCAD.Vector(
                ((obj.HolesNumberX - 1) * 12.5) + (math.sin(0.7854) * 6.25),
                ((obj.HolesNumberY - 1) * 12.5) + (math.sin(0.7854) * 6.25),
                0,
            )
            PtoC3 = FreeCAD.Vector(
                (math.sin(0.7854) * 6.25) * -1,
                ((obj.HolesNumberY - 1) * 12.5) + (math.sin(0.7854) * 6.25),
                0,
            )
            PtoC4 = FreeCAD.Vector(
                (math.sin(0.7854) * 6.25) * -1, (math.sin(0.7854) * 6.25) * -1, 0
            )
            #  ---- Creamos lineas y arcos
            L1 = Part.LineSegment(Pto1, Pto2)
            C1 = Part.Arc(Pto2, PtoC1, Pto3)
            L2 = Part.LineSegment(Pto3, Pto4)
            C2 = Part.Arc(Pto4, PtoC2, Pto5)
            L3 = Part.LineSegment(Pto5, Pto6)
            C3 = Part.Arc(Pto6, PtoC3, Pto7)
            L4 = Part.LineSegment(Pto7, Pto8)
            C4 = Part.Arc(Pto8, PtoC4, Pto1)
            #  ---- Creo el contorno
            # W = Part.Wire([L1,C2,L3,C4])

            S = Part.Shape([L1, C1, L2, C2, L3, C3, L4, C4])
            W = Part.Wire(S.Edges)

            #  ---- Creo la cara con el contorno
            F = Part.Face(W)
            #  ---- Le doy Volumen a la cara
            P = F.extrude(FreeCAD.Vector(0, 0, 3.125))
            #  ---- Bucle para agujeros
            for x in range(obj.HolesNumberX):
                for y in range(obj.HolesNumberY):
                    Agujero = Part.makeCylinder(
                        3.5, 5, FreeCAD.Vector(x * 12.5, y * 12.5, -1), FreeCAD.Vector(0, 0, 1)
                    )
                    if (x == 0) and (y == 0):
                        Agujeros = Agujero
                    else:
                        Agujeros = Agujeros.fuse(Agujero)
            P = P.cut(Agujeros)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "STR STD BRM-" + str(obj.HolesNumberX) + "x" + str(obj.HolesNumberY)

        P.Placement = obj.Placement
        obj.Shape = P


class STR_STD_BRM_AY:
    """Plancha Cuadrada Stemfie con angulo en Y"""

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
            QT_TRANSLATE_NOOP("App::Property", "Holes number in X\nMinimum = 2"),
        ).HolesNumberX = 4
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in Y\nMinimum = 2"),
        ).HolesNumberY = 3
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberSloping"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in sloping part\nMinimum 1"),
        ).HolesNumberSloping = 2
        obj.addProperty(
            "App::PropertyAngle",
            QT_TRANSLATE_NOOP("App::Property", "Angle"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Angle\nMinimum = 0\nMaximum = 180"),
        ).Angle = 135

    def execute(self, obj):
        import math

        # Compruebo que Numero_Agujeros mayor de 1
        if (
            (obj.HolesNumberX < 2)
            or (obj.HolesNumberY < 2)
            or (obj.HolesNumberSloping < 1)
            or (obj.Angle < 0)
            or (obj.Angle > 180)
        ):
            if obj.HolesNumberX < 2:
                obj.HolesNumberX = 2
            if obj.HolesNumberY < 2:
                obj.HolesNumberY = 2
            if obj.HolesNumberSloping < 1:
                obj.HolesNumberSloping = 1
            if obj.Angle < 0:
                obj.Angle = 0
            if obj.Angle > 180:
                obj.Angle = 180
        # ----------------------------
        #  ---- Genero Cuerpo Horizontal
        Pto1 = FreeCAD.Vector(-6.25, -6.25, 0)
        Pto2 = FreeCAD.Vector((obj.HolesNumberX - 1) * 12.5, -6.25, 0)

        Pto3 = FreeCAD.Vector(((obj.HolesNumberX - 1) * 12.5) + 6.25, 0, 0)
        Pto4 = FreeCAD.Vector(
            ((obj.HolesNumberX - 1) * 12.5) + 6.25, (obj.HolesNumberY - 1) * 12.5, 0
        )

        Pto5 = FreeCAD.Vector(
            (obj.HolesNumberX - 1) * 12.5, ((obj.HolesNumberY - 1) * 12.5) + 6.25, 0
        )
        Pto6 = FreeCAD.Vector(-6.25, ((obj.HolesNumberY - 1) * 12.5) + 6.25, 0)

        # Pto7 = FreeCAD.Vector(-6.25,((obj.HolesNumberY-1)*12.5),0)
        # Pto8 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Genero puntos para circulos
        PtoC1 = FreeCAD.Vector(
            ((obj.HolesNumberX - 1) * 12.5) + (math.sin(0.7854) * 6.25), math.sin(0.7854) * -6.25, 0
        )
        PtoC2 = FreeCAD.Vector(
            ((obj.HolesNumberX - 1) * 12.5) + (math.sin(0.7854) * 6.25),
            ((obj.HolesNumberY - 1) * 12.5) + (math.sin(0.7854) * 6.25),
            0,
        )
        # PtoC3 = FreeCAD.Vector((math.sin(0.7854)*6.25)*-1,((obj.HolesNumberY-1)*12.5)+(math.sin(0.7854)*6.25),0)
        # PtoC4 = FreeCAD.Vector((math.sin(0.7854)*6.25)*-1,(math.sin(0.7854)*6.25)*-1,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(Pto1, Pto2)
        C1 = Part.Arc(Pto2, PtoC1, Pto3)
        L2 = Part.LineSegment(Pto3, Pto4)
        C2 = Part.Arc(Pto4, PtoC2, Pto5)
        L3 = Part.LineSegment(Pto5, Pto6)
        # C3 = Part.Arc(Pto6,PtoC3,Pto7)
        L4 = Part.LineSegment(Pto6, Pto1)
        # C4 = Part.Arc(Pto8,PtoC4,Pto1)
        #  ---- Creo el contorno
        S = Part.Shape([L1, C1, L2, C2, L3, L4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude(FreeCAD.Vector(0, 0, -3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberX):
            for y in range(obj.HolesNumberY):
                Agujero = Part.makeCylinder(
                    3.5, 5, FreeCAD.Vector(x * 12.5, y * 12.5, -5), FreeCAD.Vector(0, 0, 1)
                )
                if (x == 0) and (y == 0):
                    Agujeros = Agujero
                else:
                    Agujeros = Agujeros.fuse(Agujero)
        P = P.cut(Agujeros)

        # Condicional para angulo 180 no generar cilindros
        if obj.Angle != 180:
            # Tengo que meter un cuarto de cilindro y unirlo a P
            # Añado condicional para que sea en funcion del angulo
            Ang = (180 - int(obj.Angle)) / 2
            Curva = Part.makeCylinder(
                3.125,
                obj.HolesNumberY * 12.5,
                FreeCAD.Vector(6.25, -6.25, 0),
                FreeCAD.Vector(0, 1, 0),
                Ang,
            )
            Curva.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 180)
            P = P.fuse(Curva)

        #  ---- Genero Cuerpo Inclinado
        #  ---- Genero puntos de los contornos
        Pto1 = FreeCAD.Vector(-6.25, -6.25, 0)
        Pto2 = FreeCAD.Vector((obj.HolesNumberSloping - 1) * 12.5, -6.25, 0)

        Pto3 = FreeCAD.Vector(((obj.HolesNumberSloping - 1) * 12.5) + 6.25, 0, 0)
        Pto4 = FreeCAD.Vector(
            ((obj.HolesNumberSloping - 1) * 12.5) + 6.25, (obj.HolesNumberY - 1) * 12.5, 0
        )

        Pto5 = FreeCAD.Vector(
            (obj.HolesNumberSloping - 1) * 12.5, ((obj.HolesNumberY - 1) * 12.5) + 6.25, 0
        )
        Pto6 = FreeCAD.Vector(-6.25, ((obj.HolesNumberY - 1) * 12.5) + 6.25, 0)

        # Pto7 = FreeCAD.Vector(-6.25,((obj.HolesNumberY-1)*12.5),0)
        # Pto8 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Genero puntos para circulos
        PtoC1 = FreeCAD.Vector(
            ((obj.HolesNumberSloping - 1) * 12.5) + (math.sin(0.7854) * 6.25),
            math.sin(0.7854) * -6.25,
            0,
        )
        PtoC2 = FreeCAD.Vector(
            ((obj.HolesNumberSloping - 1) * 12.5) + (math.sin(0.7854) * 6.25),
            ((obj.HolesNumberY - 1) * 12.5) + (math.sin(0.7854) * 6.25),
            0,
        )
        # PtoC3 = FreeCAD.Vector((math.sin(0.7854)*6.25)*-1,((obj.HolesNumberY-1)*12.5)+(math.sin(0.7854)*6.25),0)
        # PtoC4 = FreeCAD.Vector((math.sin(0.7854)*6.25)*-1,(math.sin(0.7854)*6.25)*-1,0)
        #  ---- Creamos lineas y arcos
        LInc1 = Part.LineSegment(Pto1, Pto2)
        CInc1 = Part.Arc(Pto2, PtoC1, Pto3)
        LInc2 = Part.LineSegment(Pto3, Pto4)
        CInc2 = Part.Arc(Pto4, PtoC2, Pto5)
        LInc3 = Part.LineSegment(Pto5, Pto6)
        # CInc3 = Part.Arc(Pto6,PtoC3,Pto7)
        LInc4 = Part.LineSegment(Pto6, Pto1)
        # CInc4 = Part.Arc(Pto8,PtoC4,Pto1)
        #  ---- Creo el contorno
        SInc = Part.Shape([LInc1, CInc1, LInc2, CInc2, LInc3, LInc4])
        WInc = Part.Wire(SInc.Edges)

        #  ---- Creo la cara con el contorno
        FInc = Part.Face(WInc)
        #  ---- Le doy Volumen a la cara
        PInc = FInc.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberSloping):
            for y in range(obj.HolesNumberY):
                Agujero = Part.makeCylinder(
                    3.5, 10, FreeCAD.Vector(x * 12.5, y * 12.5, -5), FreeCAD.Vector(0, 0, 1)
                )
                if (x == 0) and (y == 0):
                    Agujeros = Agujero
                else:
                    Agujeros = Agujeros.fuse(Agujero)
        PInc = PInc.cut(Agujeros)
        # Condicional para angulo 180 no generar cilindros
        if obj.Angle != 180:
            Curva = Part.makeCylinder(
                3.125,
                obj.HolesNumberY * 12.5,
                FreeCAD.Vector(-6.25, -6.25, 0),
                FreeCAD.Vector(0, 1, 0),
                Ang,
            )
            Curva.rotate(FreeCAD.Vector(-6.25, -6.25, 0), FreeCAD.Vector(0, 1, 0), -Ang)
            PInc = PInc.fuse(Curva)
        # Giro en Y
        PInc.rotate(FreeCAD.Vector(-6.25, 0, 0), FreeCAD.Vector(0, 1, 0), obj.Angle * -1)
        # Junto los dos cuerpos
        P = P.fuse(PInc)
        # Refinamos el cuerpo
        P = P.removeSplitter()

        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            "STR STD BRM AY-"
            + str(obj.HolesNumberX)
            + "x"
            + str(obj.HolesNumberY)
            + "x"
            + str(obj.HolesNumberSloping)
            + " "
            + str(obj.Angle)
        )

        P.Placement = obj.Placement
        obj.Shape = P


class STR_SLT_BE_SYM_ERR:
    """Brazo Stemfie con agujeros rasgados en extremos y simples en el centro"""

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
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberTotal"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Total number of holes\nMinimum 5"),
        ).HolesNumberTotal = 5
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberSlotted"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP(
                "App::Property", "Slotted holes number\nSame on both sides\nMinimum 2"
            ),
        ).HolesNumberSlotted = 2

    def execute(self, obj):
        # Compruebo que HolesNumberTotal y HolesNumberSlotted
        if (obj.HolesNumberTotal < 5) or (
            obj.HolesNumberSlotted < 2
        ):  # Si alguno es menor no modificar pieza
            if obj.HolesNumberTotal < 5:  # si Numero Total de Agujeros es menor 5
                obj.HolesNumberTotal = 5  # dejarlo en 5
            else:  # si no
                obj.HolesNumberSlotted = 2  # dejar Numero Agujeros del coliso en 2

        if (obj.HolesNumberSlotted * 2) + 1 > (obj.HolesNumberTotal):
            obj.HolesNumberTotal = (obj.HolesNumberSlotted * 2) + 1
        # ----------------------------
        #  ---- Genero Cuerpo exterior
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector((obj.HolesNumberTotal - 1) * 12.5, -6.25, 0)
        P3 = FreeCAD.Vector((obj.HolesNumberTotal - 1) * 12.5, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.HolesNumberTotal - 1) * 12.5) + 6.25, 0, 0)
        PC4 = FreeCAD.Vector(-6.25, 0, 0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1, P2)
        C2 = Part.Arc(P2, PC2, P3)
        L3 = Part.LineSegment(P3, P4)
        C4 = Part.Arc(P4, PC4, P1)
        S = Part.Shape([L1, C2, L3, C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  -----------------------------
        #  ---- Genero Cuerpos a restar
        #  -----------------------------
        #  ---- Genero Cuerpos a restar de los dos extremos
        for x in range(2):
            if x == 0:
                Desp = 0
            else:
                Desp = (
                    (obj.HolesNumberTotal - (obj.HolesNumberSlotted * 2)) + obj.HolesNumberSlotted
                ) * 12.5

            Pto01 = FreeCAD.Vector(0 + Desp, -3.5, 0)
            Pto02 = FreeCAD.Vector(((obj.HolesNumberSlotted - 1) * 12.5) + Desp, -3.5, 0)
            Pto03 = FreeCAD.Vector(((obj.HolesNumberSlotted - 1) * 12.5) + Desp, 3.5, 0)
            Pto04 = FreeCAD.Vector(0 + Desp, 3.5, 0)
            #  ---- Genero puntos para circulos
            PtoC2 = FreeCAD.Vector((((obj.HolesNumberSlotted - 1) * 12.5) + 3.5) + Desp, 0, 0)
            PtoC4 = FreeCAD.Vector(-3.5 + Desp, 0, 0)
            #  ---- Creamos lineas y arcos
            LRest1 = Part.LineSegment(Pto01, Pto02)
            CRest2 = Part.Arc(Pto02, PtoC2, Pto03)
            LRest3 = Part.LineSegment(Pto03, Pto04)
            CRest4 = Part.Arc(Pto04, PtoC4, Pto01)
            SRest = Part.Shape([LRest1, CRest2, LRest3, CRest4])
            WRest = Part.Wire(SRest.Edges)
            #  ---- Creo la cara con el contorno
            FRest = Part.Face(WRest)
            PRest = FRest.extrude(FreeCAD.Vector(0, 0, 5))
            P = P.cut(PRest)

        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberTotal - (obj.HolesNumberSlotted * 2)):
            Agujero = Part.makeCylinder(
                3.5,
                5,
                FreeCAD.Vector((obj.HolesNumberSlotted + x) * 12.5, 0, -1),
                FreeCAD.Vector(0, 0, 1),
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut(Agujeros)

        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            "STR_SLT_BE_SYM_ERR-BU"
            + str(obj.HolesNumberTotal)
            + "x01x00.25x"
            + str(obj.HolesNumberSlotted)
        )

        P.Placement = obj.Placement
        obj.Shape = P


class STR_SLT_CNT_ERR:
    """Brazo Stemfie con agujeros rasgados en centro y simples en extremos"""

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
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberTotal"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Total number of holes\nMinimum 4"),
        ).HolesNumberTotal = 4
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberSlotted"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of slotted holes\nMinimum 2"),
        ).HolesNumberSlotted = 2

    def execute(self, obj):
        # Compruebo que HolesNumberTotal y HolesNumberSlotted
        if (obj.HolesNumberTotal < 4) or (
            obj.HolesNumberSlotted < 2
        ):  # Si alguno es menor no modificar pieza
            if obj.HolesNumberTotal < 4:  # si Numero Total de Agujeros es menor 4
                obj.HolesNumberTotal = 4  # dejarlo en 4
            else:  # si no
                obj.HolesNumberSlotted = 2  # dejar Numero Agujeros del coliso en 2
            # return
        # Ahora compuebo que la longitud total no sea menor de lo necesario
        if obj.HolesNumberSlotted + 2 > obj.HolesNumberTotal:
            obj.HolesNumberTotal = obj.HolesNumberSlotted + 2

        if ((obj.HolesNumberTotal - obj.HolesNumberSlotted) % 2) != 0:
            obj.HolesNumberTotal = (obj.HolesNumber_T) + 1
        # ----------------------------
        #  ---- Genero Cuerpo exterior
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector((obj.HolesNumberTotal - 1) * 12.5, -6.25, 0)
        P3 = FreeCAD.Vector((obj.HolesNumberTotal - 1) * 12.5, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.HolesNumberTotal - 1) * 12.5) + 6.25, 0, 0)
        PC4 = FreeCAD.Vector(-6.25, 0, 0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1, P2)
        C2 = Part.Arc(P2, PC2, P3)
        L3 = Part.LineSegment(P3, P4)
        C4 = Part.Arc(P4, PC4, P1)
        S = Part.Shape([L1, C2, L3, C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  -----------------------------
        #  ---- Genero Cuerpos a restar
        #  -----------------------------
        #  ---- Genero cilindros a restar de los dos extremos
        for x in range(2):
            if x == 0:
                Desp = 0
            else:
                Desp = (
                    ((obj.HolesNumberTotal - obj.HolesNumberSlotted) / 2) + obj.HolesNumberSlotted
                ) * 12.5
            #  ----  agujeros
            for y in range(int((obj.HolesNumberTotal - obj.HolesNumberSlotted) / 2)):
                Agujero = Part.makeCylinder(
                    3.5, 5, FreeCAD.Vector((y * 12.5) + Desp, 0, -1), FreeCAD.Vector(0, 0, 1)
                )
                if y == 0:
                    Agujeros = Agujero
                else:
                    Agujeros = Agujeros.fuse(Agujero)
            P = P.cut(Agujeros)

        # Genero la forma central
        Desp = ((obj.HolesNumberTotal - obj.HolesNumberSlotted) / 2) * 12.5

        Pto01 = FreeCAD.Vector(0 + Desp, -3.5, -1)
        Pto02 = FreeCAD.Vector(((obj.HolesNumberSlotted - 1) * 12.5) + Desp, -3.5, -1)
        Pto03 = FreeCAD.Vector(((obj.HolesNumberSlotted - 1) * 12.5) + Desp, 3.5, -1)
        Pto04 = FreeCAD.Vector(0 + Desp, 3.5, -1)
        #  ---- Genero puntos para circulos
        PtoC2 = FreeCAD.Vector((((obj.HolesNumberSlotted - 1) * 12.5) + 3.5) + Desp, 0, -1)
        PtoC4 = FreeCAD.Vector(-3.5 + Desp, 0, -1)
        #  ---- Creamos lineas y arcos
        LRest1 = Part.LineSegment(Pto01, Pto02)
        CRest2 = Part.Arc(Pto02, PtoC2, Pto03)
        LRest3 = Part.LineSegment(Pto03, Pto04)
        CRest4 = Part.Arc(Pto04, PtoC4, Pto01)
        SRest = Part.Shape([LRest1, CRest2, LRest3, CRest4])
        WRest = Part.Wire(SRest.Edges)
        #  ---- Creo la cara con el contorno
        FRest = Part.Face(WRest)
        PRest = FRest.extrude(FreeCAD.Vector(0, 0, 5))  # Extruyo 5
        P = P.cut(PRest)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            "STR_SLT_CNT_ERR-BU"
            + str(obj.HolesNumberTotal)
            + "x01x00.25x"
            + str(obj.HolesNumberSlotted)
        )

        P.Placement = obj.Placement
        obj.Shape = P


class STR_SLT_FL_ERR:
    """Brazo Stemfie rasgado en toda su extension"""

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
            QT_TRANSLATE_NOOP("App::Property", "Holes number\nMinimum 2"),
        ).HolesNumber = 4

    def execute(self, obj):
        # Compruebo que Numero_Agujeros
        if obj.HolesNumber < 2:
            obj.HolesNumber = 2  # Si es menor dejar Numero Agujeros en 2

        # ----------------------------
        #  ---- Genero Cuerpo exterior
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
        S = Part.Shape([L1, C2, L3, C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude(FreeCAD.Vector(0, 0, 3.125))

        #  ---- Genero el Cuerpo Interior a restar
        #  -----------------------------
        Pto01 = FreeCAD.Vector(0, -3.5, -1)
        Pto02 = FreeCAD.Vector(((obj.HolesNumber - 1) * 12.5), -3.5, -1)
        Pto03 = FreeCAD.Vector(((obj.HolesNumber - 1) * 12.5), 3.5, -1)
        Pto04 = FreeCAD.Vector(0, 3.5, -1)
        #  ---- Genero puntos para circulos
        PtoC2 = FreeCAD.Vector((((obj.HolesNumber - 1) * 12.5) + 3.5), 0, -1)
        PtoC4 = FreeCAD.Vector(-3.5, 0, -1)
        #  ---- Creamos lineas y arcos
        LRest1 = Part.LineSegment(Pto01, Pto02)
        CRest2 = Part.Arc(Pto02, PtoC2, Pto03)
        LRest3 = Part.LineSegment(Pto03, Pto04)
        CRest4 = Part.Arc(Pto04, PtoC4, Pto01)
        SRest = Part.Shape([LRest1, CRest2, LRest3, CRest4])
        WRest = Part.Wire(SRest.Edges)
        #  ---- Creo la cara con el contorno
        FRest = Part.Face(WRest)
        PRest = FRest.extrude(FreeCAD.Vector(0, 0, 5))  # Extruyo 5
        P = P.cut(PRest)  # Resto
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "STR_SLT_FL_ERR-" + str(obj.HolesNumber)

        P.Placement = obj.Placement
        obj.Shape = P


class STR_SLT_SE_ERR:
    """Brazo Stemfie agujeros en un extremo y rasgado en el otro"""

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
            QT_TRANSLATE_NOOP("App::Property", "Number of slotted holes\nMinimum 1"),
        ).HolesNumber = 1
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberSlotted"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP(
                "App::Property",
                "Slotted holes number\nSame on both sides\nMinimum 2",
            ),
        ).HolesNumberSlotted = 2

    def execute(self, obj):
        # Compruebo que HolesNumber y Numero_Agujeros_R
        if (obj.HolesNumber < 1) or (
            obj.HolesNumberSlotted < 2
        ):  # Si alguno es menor de lo permitido
            if obj.HolesNumber < 1:  # si Numero de Agujeros es menor 1
                obj.HolesNumber = 1  # dejarlo en 1
            else:  # si no a cambiado HolesNumber, a sido Numero_Agujeros_R
                obj.HolesNumberSlotted = 2  # dejar Numero Agujeros del coliso en 2

        # Creo la variable de total agujeros
        HolesNumberTotal = obj.HolesNumber + obj.HolesNumberSlotted
        # ----------------------------
        #  ---- Genero Cuerpo exterior
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector((HolesNumberTotal - 1) * 12.5, -6.25, 0)
        P3 = FreeCAD.Vector((HolesNumberTotal - 1) * 12.5, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((HolesNumberTotal - 1) * 12.5) + 6.25, 0, 0)
        PC4 = FreeCAD.Vector(-6.25, 0, 0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1, P2)
        C2 = Part.Arc(P2, PC2, P3)
        L3 = Part.LineSegment(P3, P4)
        C4 = Part.Arc(P4, PC4, P1)
        S = Part.Shape([L1, C2, L3, C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  -----------------------------
        #  ---- Genero Cuerpos a restar
        #  -----------------------------
        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumber):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector(x * 12.5, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut(Agujeros)
        #  ---- Genero Cuerpo del Agujero Rasgado
        #  ---- Calculo desplamiento para iniciar el coliso
        Desp = obj.HolesNumber * 12.5
        Pto01 = FreeCAD.Vector(0 + Desp, -3.5, 0)
        Pto02 = FreeCAD.Vector(((obj.HolesNumberSlotted - 1) * 12.5) + Desp, -3.5, 0)
        Pto03 = FreeCAD.Vector(((obj.HolesNumberSlotted - 1) * 12.5) + Desp, 3.5, 0)
        Pto04 = FreeCAD.Vector(0 + Desp, 3.5, 0)
        #  ---- Genero puntos para circulos
        PtoC2 = FreeCAD.Vector((((obj.HolesNumberSlotted - 1) * 12.5) + 3.5) + Desp, 0, 0)
        PtoC4 = FreeCAD.Vector(-3.5 + Desp, 0, 0)
        #  ---- Creamos lineas y arcos
        LRest1 = Part.LineSegment(Pto01, Pto02)
        CRest2 = Part.Arc(Pto02, PtoC2, Pto03)
        LRest3 = Part.LineSegment(Pto03, Pto04)
        CRest4 = Part.Arc(Pto04, PtoC4, Pto01)
        SRest = Part.Shape([LRest1, CRest2, LRest3, CRest4])
        WRest = Part.Wire(SRest.Edges)
        #  ---- Creo la cara con el contorno
        FRest = Part.Face(WRest)
        PRest = FRest.extrude(FreeCAD.Vector(0, 0, 5))
        P = P.cut(PRest)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            "STR_SLT_SE_ERR-BU" + str(obj.HolesNumber) + "x01x00.25x" + str(obj.HolesNumberSlotted)
        )
        #  ---- Añado emplzamiento al objeto
        P.Placement = obj.Placement
        obj.Shape = P


class STR_STD_BRD_AY:
    """Brazo Stemfie angulo en Y Nº_Agujeros en horizontal y Nº agujeros en inclinada"""

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
            QT_TRANSLATE_NOOP("App::Property", "Holes number in horizontal bar\nMinimum 1"),
        )
        obj.HolesNumberX = 3
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberSloping"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in sloping part\nMinimum 1"),
        )
        obj.HolesNumberSloping = 2
        obj.addProperty(
            "App::PropertyAngle",
            QT_TRANSLATE_NOOP("App::Property", "Angle"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Angle\nMinimum = 0\nMaximum = 180"),
        )
        obj.Angle = 135

    def execute(self, obj):
        # Compruebo que Numero_Agujeros mayor de 2 y Angulo en 60 y 180
        if (
            (obj.HolesNumberX < 1)
            or (obj.HolesNumberSloping < 1)
            or (obj.Angle < 0)
            or (obj.Angle > 180)
        ):
            if obj.HolesNumberX < 1:
                obj.HolesNumberX = 1
            if obj.HolesNumberSloping < 1:
                obj.HolesNumberSloping = 1
            if obj.Angle < 0:
                obj.Angle = 0
            if obj.Angle > 180:
                obj.Angle = 180
        # ----------------------------
        #  ---- Genero Cuerpo Horizontal
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector(((obj.HolesNumberX - 1) * 12.5) + 6.25, -6.25, 0)
        P3 = FreeCAD.Vector(((obj.HolesNumberX - 1) * 12.5) + 6.25, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero punto para arco
        PC2 = FreeCAD.Vector(obj.HolesNumberX * 12.5, 0, 0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1, P2)
        C2 = Part.Arc(P2, PC2, P3)
        L3 = Part.LineSegment(P3, P4)
        L4 = Part.LineSegment(P4, P1)
        S = Part.Shape([L1, C2, L3, L4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude(FreeCAD.Vector(0, 0, -3.125))
        # Hago los Agujeros de X
        for x in range(obj.HolesNumberX):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector((x * 12.5) + 6.25, 0, -5), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut(Agujeros)
        # Condicional para angulo 180 no generar cilindros
        if obj.Angle != 180:
            # Tengo que meter un cuarto de cilindro y unirlo a P
            # Añado condicional para que sea en funcion del angulo
            Ang = (180 - int(obj.Angle)) / 2
            Curva = Part.makeCylinder(
                3.125, 12.5, FreeCAD.Vector(0, -6.25, 0), FreeCAD.Vector(0, 1, 0), Ang
            )
            Curva.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 180)
            P = P.fuse(Curva)
        #  ---- Genero Cuerpo Inclinado
        Pto1 = FreeCAD.Vector(0, -6.25, 0)
        Pto2 = FreeCAD.Vector(((obj.HolesNumberSloping - 1) * 12.5) + 6.25, -6.25, 0)
        Pto3 = FreeCAD.Vector(((obj.HolesNumberSloping - 1) * 12.5) + 6.25, 6.25, 0)
        Pto4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero punto para arco
        PtoC2 = FreeCAD.Vector(obj.HolesNumberSloping * 12.5, 0, 0)
        #  ---- Creamos lineas y arcos
        LInc1 = Part.LineSegment(Pto1, Pto2)
        CInc2 = Part.Arc(Pto2, PtoC2, Pto3)
        LInc3 = Part.LineSegment(Pto3, Pto4)
        LInc4 = Part.LineSegment(Pto4, Pto1)
        SInc = Part.Shape([LInc1, CInc2, LInc3, LInc4])
        WInc = Part.Wire(SInc.Edges)
        #  ---- Creo la cara con el contorno
        FInc = Part.Face(WInc)
        #  ---- Le doy Volumen a la cara
        PInc = FInc.extrude(FreeCAD.Vector(0, 0, 3.125))
        # Hago los Agujeros en el cuerpo inclinado
        for x in range(obj.HolesNumberSloping):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector((x * 12.5) + 6.25, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PInc = PInc.cut(Agujeros)
        # Condicional para angulo 180 no generar cilindros
        if obj.Angle != 180:
            Curva = Part.makeCylinder(
                3.125, 12.5, FreeCAD.Vector(0, -6.25, 0), FreeCAD.Vector(0, 1, 0), Ang
            )
            Curva.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), -Ang)
            PInc = PInc.fuse(Curva)
        # Giro en Y
        PInc.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), obj.Angle * -1)
        # Junto los dos cuerpos
        P = P.fuse(PInc)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            "STR_STD_BRD_AY-"
            + str(obj.HolesNumberX)
            + "x"
            + str(obj.HolesNumberSloping)
            + " "
            + str(obj.Angle)
        )
        #  ---- Añado emplazamiento al objeto
        P.Placement = obj.Placement
        obj.Shape = P


class STR_STD_BRT_AZ:
    """Brazo Stemfie con brazos inclinados en extremos"""

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
        obj.addProperty(
            "App::PropertyAngle",
            QT_TRANSLATE_NOOP("App::Property", "Angle"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Angle\nMinimum = 90°\nMaximum = 180°"),
        )
        obj.Angle = 90

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
            # return

        # Genero Pieza en X
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector((obj.HolesNumberX - 1) * 12.5, -6.25, 0)
        P3 = FreeCAD.Vector((obj.HolesNumberX - 1) * 12.5, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.HolesNumberX - 1) * 12.5) + 6.25, 0, 0)
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
        PX = F.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberX):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector(x * 12.5, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PX = PX.cut(Agujeros)

        # Genero Piezas en Y1
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector((obj.HolesNumberY1) * 12.5, -6.25, 0)
        P3 = FreeCAD.Vector((obj.HolesNumberY1) * 12.5, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.HolesNumberY1) * 12.5) + 6.25, 0, 0)
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
        PY1 = F.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberY1 + 1):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector(x * 12.5, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PY1 = PY1.cut(Agujeros)

        PY1.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), obj.Angle)

        P = PX.fuse(PY1)

        # Genero Piezas en Y2
        Desp = (obj.HolesNumberX - 1) * 12.5
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0 + Desp, -6.25, 0)
        P2 = FreeCAD.Vector(((obj.HolesNumberY2) * 12.5) + Desp, -6.25, 0)
        P3 = FreeCAD.Vector(((obj.HolesNumberY2) * 12.5) + Desp, 6.25, 0)
        P4 = FreeCAD.Vector(0 + Desp, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.HolesNumberY2) * 12.5) + 6.25 + Desp, 0, 0)
        PC4 = FreeCAD.Vector(-6.25 + Desp, 0, 0)
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
        PY2 = F.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberY2 + 1):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector(x * 12.5 + Desp, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PY2 = PY2.cut(Agujeros)
        #  ---- giro parte Y 2 (restando de 180)----
        PY2.rotate(FreeCAD.Vector(Desp, 0, 0), FreeCAD.Vector(0, 0, 1), (180 - int(obj.Angle)))

        P = P.fuse(PY2)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            "STR_STD_BRT_AZ-"
            + str(obj.HolesNumberY1)
            + "x"
            + str(obj.HolesNumberX)
            + "x"
            + str(obj.HolesNumberY2)
            + " "
            + str(obj.Angle)
        )

        P.Placement = obj.Placement
        obj.Shape = P


class STR_STD_BRT_AY:
    """Brazo Stemfie con brazos inclinados en extremos en eje Y"""

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
            QT_TRANSLATE_NOOP("App::Property", "Holes number in horizontal part\nMinimum 1"),
        ).HolesNumberX = 3
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberSloping1"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in left sloping part\nMinimum 1"),
        ).HolesNumberSloping1 = 2
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberSloping2"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in right sloping part\nMinimum 1"),
        ).HolesNumberSloping2 = 2
        obj.addProperty(
            "App::PropertyAngle",
            QT_TRANSLATE_NOOP("App::Property", "Angle"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Angle\nMinimum = 0\nMaximum = 180"),
        ).Angle = 135

    def execute(self, obj):
        # Compruebo que Numero_Agujeros mayor de 2 y Angulo en 60 y 180
        if (
            (obj.HolesNumberX < 1)
            or (obj.HolesNumberSloping1 < 1)
            or (obj.HolesNumberSloping2 < 1)
            or (obj.Angle < 0)
            or (obj.Angle > 180)
        ):
            if obj.HolesNumberX < 1:
                obj.HolesNumberX = 1
            if obj.HolesNumberSloping1 < 1:
                obj.HolesNumberSloping1 = 1
            if obj.HolesNumberSloping2 < 1:
                obj.HolesNumberSloping2 = 1
            if obj.Angle < 0:
                obj.Angle = 0
            if obj.Angle > 180:
                obj.Angle = 180
        # Limito nº agujeros en Inclinadas cuando angulo es 0
        if obj.Angle == 0:
            if obj.HolesNumberSloping1 > obj.HolesNumberX:
                obj.HolesNumberSloping1 = obj.HolesNumberX
            if obj.HolesNumberSloping2 > obj.HolesNumberX:
                obj.HolesNumberSloping2 = obj.HolesNumberX

        # ----------------------------
        #  ---- Genero Cuerpo Horizontal
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector(((obj.HolesNumberX) * 12.5), -6.25, 0)
        P3 = FreeCAD.Vector(((obj.HolesNumberX) * 12.5), 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1, P2)
        L2 = Part.LineSegment(P2, P3)
        L3 = Part.LineSegment(P3, P4)
        L4 = Part.LineSegment(P4, P1)
        S = Part.Shape([L1, L2, L3, L4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude(FreeCAD.Vector(0, 0, -3.125))
        # Hago los Agujeros de X
        for x in range(obj.HolesNumberX):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector((x * 12.5) + 6.25, 0, -5), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut(Agujeros)

        # Condicional para angulo 180 no generar cilindros
        if obj.Angle != 180:
            # Tengo que meter dos cachos de cilindro en los extremos y unirlo a P
            # Añado condicional para que sea en funcion del angulo
            #  ---- Primer Cilindro
            Ang = (180 - int(obj.Angle)) / 2
            Curva1 = Part.makeCylinder(
                3.125, 12.5, FreeCAD.Vector(0, -6.25, 0), FreeCAD.Vector(0, 1, 0), Ang
            )
            Curva1.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 180)
            P = P.fuse(Curva1)
            #  ---- Segundo Cilindro
            Curva2 = Part.makeCylinder(
                3.125,
                12.5,
                FreeCAD.Vector(obj.HolesNumberX * 12.5, -6.25, 0),
                FreeCAD.Vector(0, 1, 0),
                Ang,
            )
            Curva2.rotate(
                FreeCAD.Vector(obj.HolesNumberX * 12.5, 0, 0), FreeCAD.Vector(0, 1, 0), 180 - Ang
            )
            P = P.fuse(Curva2)

        #
        #  ---- Genero Cuerpo Inclinado_1 Izquierdo
        Pto1 = FreeCAD.Vector(0, -6.25, 0)
        Pto2 = FreeCAD.Vector(((obj.HolesNumberSloping1 - 1) * 12.5) + 6.25, -6.25, 0)
        Pto3 = FreeCAD.Vector(((obj.HolesNumberSloping1 - 1) * 12.5) + 6.25, 6.25, 0)
        Pto4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero punto para arco
        PtoC2 = FreeCAD.Vector(obj.HolesNumberSloping1 * 12.5, 0, 0)
        #  ---- Creamos lineas y arcos
        LInc1 = Part.LineSegment(Pto1, Pto2)
        CInc2 = Part.Arc(Pto2, PtoC2, Pto3)
        LInc3 = Part.LineSegment(Pto3, Pto4)
        LInc4 = Part.LineSegment(Pto4, Pto1)
        SInc = Part.Shape([LInc1, CInc2, LInc3, LInc4])
        WInc = Part.Wire(SInc.Edges)
        #  ---- Creo la cara con el contorno
        FInc = Part.Face(WInc)
        #  ---- Le doy Volumen a la cara
        PInc = FInc.extrude(FreeCAD.Vector(0, 0, 3.125))
        # Hago los Agujeros en el cuerpo inclinado
        for x in range(obj.HolesNumberSloping1):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector((x * 12.5) + 6.25, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PInc = PInc.cut(Agujeros)
        # Condicional para angulo 180 no generar cilindros
        if obj.Angle != 180:
            # Curva
            Curva = Part.makeCylinder(
                3.125, 12.5, FreeCAD.Vector(0, -6.25, 0), FreeCAD.Vector(0, 1, 0), Ang
            )
            Curva.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), -Ang)
            PInc = PInc.fuse(Curva)
        # Giro en Y
        PInc.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), obj.Angle * -1)
        # Junto los dos cuerpos
        P = P.fuse(PInc)

        #  ---- Genero Cuerpo Inclinado_2 Izquierdo
        Desp = obj.HolesNumberX * 12.5
        Pto1 = FreeCAD.Vector(Desp, -6.25, 0)
        Pto2 = FreeCAD.Vector(((obj.HolesNumberSloping2 - 1) * 12.5) + 6.25 + Desp, -6.25, 0)
        Pto3 = FreeCAD.Vector(((obj.HolesNumberSloping2 - 1) * 12.5) + 6.25 + Desp, 6.25, 0)
        Pto4 = FreeCAD.Vector(Desp, 6.25, 0)
        #  ---- Genero punto para arco
        PtoC2 = FreeCAD.Vector((obj.HolesNumberSloping2 * 12.5) + Desp, 0, 0)
        #  ---- Creamos lineas y arcos
        LInc1 = Part.LineSegment(Pto1, Pto2)
        CInc2 = Part.Arc(Pto2, PtoC2, Pto3)
        LInc3 = Part.LineSegment(Pto3, Pto4)
        LInc4 = Part.LineSegment(Pto4, Pto1)
        SInc = Part.Shape([LInc1, CInc2, LInc3, LInc4])
        WInc = Part.Wire(SInc.Edges)
        #  ---- Creo la cara con el contorno
        FInc = Part.Face(WInc)
        #  ---- Le doy Volumen a la cara
        PInc = FInc.extrude(FreeCAD.Vector(0, 0, -3.125))
        # Hago los Agujeros en el cuerpo inclinado
        for x in range(obj.HolesNumberSloping2):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector((x * 12.5) + 6.25 + Desp, 0, -4), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PInc = PInc.cut(Agujeros)
        # Condicional para angulo 180 no generar cilindros
        if obj.Angle != 180:
            # Curva
            Curva = Part.makeCylinder(
                3.125, 12.5, FreeCAD.Vector(Desp, -6.25, 0), FreeCAD.Vector(0, 1, 0), Ang
            )
            Curva.rotate(FreeCAD.Vector(Desp, 0, 0), FreeCAD.Vector(0, 1, 0), 180)
            PInc = PInc.fuse(Curva)
        # Giro en Y
        PInc.rotate(
            FreeCAD.Vector(Desp, 0, 0), FreeCAD.Vector(0, 1, 0), (180 - int(obj.Angle)) * -1
        )
        # Junto los dos cuerpos
        P = P.fuse(PInc)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            "STR_STD_BRT_AY-"
            + str(obj.HolesNumberSloping1)
            + "x"
            + str(obj.HolesNumberX)
            + "x"
            + str(obj.HolesNumberSloping2)
            + " "
            + str(obj.Angle)
        )

        #  ---- Añado emplazamiento al objeto
        P.Placement = obj.Placement
        obj.Shape = P


class STR_STD_CR:
    """Brazo Stemfie Cruz con longitud de brazos independientes"""

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
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberXPositive"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in X +\nMinimum = 1"),
        ).HolesNumberXPositive = 3
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberXNegative"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in X -\nMinimum = 1"),
        ).HolesNumberXNegative = 3
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberYPositive"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in Y +\nMinimum = 1"),
        ).HolesNumberYPositive = 2
        obj.addProperty(
            "App::PropertyInteger",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberYNegative"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in Y -\nMinimum = 1"),
        ).HolesNumberYNegative = 2

    def execute(self, obj):
        # Compruebo que Numero_Agujeros mayor de 2
        if (
            (obj.HolesNumberXPositive < 1)
            or (obj.HolesNumberXNegative < 1)
            or (obj.HolesNumberYPositive < 1)
            or (obj.HolesNumberYNegative < 1)
        ):
            if obj.HolesNumberXPositive < 1:
                obj.HolesNumberXPositive = 1
            if obj.HolesNumberXNegative < 1:
                obj.HolesNumberXNegative = 1
            if obj.HolesNumberYPositive < 1:
                obj.HolesNumberYPositive = 1
            if obj.HolesNumberYNegative < 1:
                obj.HolesNumberYNegative = 1
            # return

        # Genero Pieza en X+
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector((obj.HolesNumberXPositive) * 12.5, -6.25, 0)
        P3 = FreeCAD.Vector((obj.HolesNumberXPositive) * 12.5, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.HolesNumberXPositive) * 12.5) + 6.25, 0, 0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1, P2)
        C2 = Part.Arc(P2, PC2, P3)
        L3 = Part.LineSegment(P3, P4)
        L4 = Part.LineSegment(P4, P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1, C2, L3, L4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PX = F.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberXPositive + 1):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector(x * 12.5, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PX = PX.cut(Agujeros)
        P = PX
        # Genero Pieza en X-
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector((obj.HolesNumberXNegative) * 12.5, -6.25, 0)
        P3 = FreeCAD.Vector((obj.HolesNumberXNegative) * 12.5, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.HolesNumberXNegative) * 12.5) + 6.25, 0, 0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1, P2)
        C2 = Part.Arc(P2, PC2, P3)
        L3 = Part.LineSegment(P3, P4)
        L4 = Part.LineSegment(P4, P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1, C2, L3, L4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PX = F.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberXNegative + 1):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector(x * 12.5, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PX = PX.cut(Agujeros)
        PX.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 180)
        P = P.fuse(PX)
        # Genero Pieza en Y+
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector((obj.HolesNumberYPositive) * 12.5, -6.25, 0)
        P3 = FreeCAD.Vector((obj.HolesNumberYPositive) * 12.5, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.HolesNumberYPositive) * 12.5) + 6.25, 0, 0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1, P2)
        C2 = Part.Arc(P2, PC2, P3)
        L3 = Part.LineSegment(P3, P4)
        L4 = Part.LineSegment(P4, P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1, C2, L3, L4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PY = F.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberYPositive + 1):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector(x * 12.5, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PY = PY.cut(Agujeros)
        PY.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 90)
        P = P.fuse(PY)
        # Genero Pieza en Y-
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0, -6.25, 0)
        P2 = FreeCAD.Vector((obj.HolesNumberYNegative) * 12.5, -6.25, 0)
        P3 = FreeCAD.Vector((obj.HolesNumberYNegative) * 12.5, 6.25, 0)
        P4 = FreeCAD.Vector(0, 6.25, 0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.HolesNumberYNegative) * 12.5) + 6.25, 0, 0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1, P2)
        C2 = Part.Arc(P2, PC2, P3)
        L3 = Part.LineSegment(P3, P4)
        L4 = Part.LineSegment(P4, P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1, C2, L3, L4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PY = F.extrude(FreeCAD.Vector(0, 0, 3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberYNegative + 1):
            Agujero = Part.makeCylinder(
                3.5, 5, FreeCAD.Vector(x * 12.5, 0, -1), FreeCAD.Vector(0, 0, 1)
            )
            if x == 0:
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PY = PY.cut(Agujeros)
        PY.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 270)
        P = P.fuse(PY)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            "STR_STD_CR-"
            + str(obj.HolesNumberXPositive)
            + "x"
            + str(obj.HolesNumberXNegative)
            + "x"
            + str(obj.HolesNumberYPositive)
            + "x"
            + str(obj.HolesNumberYNegative)
        )

        P.Placement = obj.Placement
        obj.Shape = P


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


class STR_BED:
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
            "STR_BED-" + str(obj.HolesNumberX) + "x" + str(obj.HolesNumberY) + " " + str(obj.Angle)
        )

        P.Placement = obj.Placement
        obj.Shape = P


class STR_BET:
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
            "STR_BET-"
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
            QT_TRANSLATE_NOOP("App::Property", "Holes number \nMinimum = 1"),
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
            QT_TRANSLATE_NOOP("App::Property", "Holes number \nMinimum = 3"),
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


# Conectores
class TRH_H_BEM_SFT_1W:
    """Conector en 1 cara Stemfie"""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyString",
            QT_TRANSLATE_NOOP("App::Property", "Code"),
            QT_TRANSLATE_NOOP("App::Property", "Designation"),
            QT_TRANSLATE_NOOP("App::Property", "STEMFIE part number"),
        )
        obj.setEditorMode("Code", 1)

    def execute(self, obj):
        # Genero el cuerpo exterior
        P = Part.makeBox(
            15.625, 15.625, 12.5, FreeCAD.Vector(-7.8125, -7.8125, -6.25), FreeCAD.Vector(0, 0, 1)
        )

        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        Cubo = Part.makeBox(
            12.9, 12.9, 20, FreeCAD.Vector(-6.45, -6.45, -10), FreeCAD.Vector(0, 0, 1)
        )
        P = P.cut(Cubo)

        #  Genero el Cono
        #  Nombro Variables para Facilitar codigo
        LadoG = 4.9291
        EntreCarasG = 11.9
        LadoP = 3.7279
        EntreCarasP = 9
        Altura = 4.6875
        #  Puntos Poligono Grande
        PG1 = FreeCAD.Vector(EntreCarasG / 2, LadoG / 2, 0)
        PG2 = FreeCAD.Vector(LadoG / 2, EntreCarasG / 2, 0)
        PG3 = FreeCAD.Vector(-LadoG / 2, EntreCarasG / 2, 0)
        PG4 = FreeCAD.Vector(-EntreCarasG / 2, LadoG / 2, 0)
        PG5 = FreeCAD.Vector(-EntreCarasG / 2, -LadoG / 2, 0)
        PG6 = FreeCAD.Vector(-LadoG / 2, -EntreCarasG / 2, 0)
        PG7 = FreeCAD.Vector(LadoG / 2, -EntreCarasG / 2, 0)
        PG8 = FreeCAD.Vector(EntreCarasG / 2, -LadoG / 2, 0)
        #  Puntos Poligono Pequeño
        PP1 = FreeCAD.Vector(EntreCarasP / 2, LadoP / 2, Altura)
        PP2 = FreeCAD.Vector(LadoP / 2, EntreCarasP / 2, Altura)
        PP3 = FreeCAD.Vector(-LadoP / 2, EntreCarasP / 2, Altura)
        PP4 = FreeCAD.Vector(-EntreCarasP / 2, LadoP / 2, Altura)
        PP5 = FreeCAD.Vector(-EntreCarasP / 2, -LadoP / 2, Altura)
        PP6 = FreeCAD.Vector(-LadoP / 2, -EntreCarasP / 2, Altura)
        PP7 = FreeCAD.Vector(LadoP / 2, -EntreCarasP / 2, Altura)
        PP8 = FreeCAD.Vector(EntreCarasP / 2, -LadoP / 2, Altura)
        #  ---- Creamos lineas Poligono Grande
        LPG1 = Part.LineSegment(PG1, PG2)
        LPG2 = Part.LineSegment(PG2, PG3)
        LPG3 = Part.LineSegment(PG3, PG4)
        LPG4 = Part.LineSegment(PG4, PG5)
        LPG5 = Part.LineSegment(PG5, PG6)
        LPG6 = Part.LineSegment(PG6, PG7)
        LPG7 = Part.LineSegment(PG7, PG8)
        LPG8 = Part.LineSegment(PG8, PG1)
        #  ---- Creamos Cara Poligono Grande
        SG = Part.Shape([LPG1, LPG2, LPG3, LPG4, LPG5, LPG6, LPG7, LPG8])
        WG = Part.Wire(SG.Edges)
        FG = Part.Face(WG)
        #  ---- Creamos lineas Poligono Pequeño
        LPP1 = Part.LineSegment(PP1, PP2)
        LPP2 = Part.LineSegment(PP2, PP3)
        LPP3 = Part.LineSegment(PP3, PP4)
        LPP4 = Part.LineSegment(PP4, PP5)
        LPP5 = Part.LineSegment(PP5, PP6)
        LPP6 = Part.LineSegment(PP6, PP7)
        LPP7 = Part.LineSegment(PP7, PP8)
        LPP8 = Part.LineSegment(PP8, PP1)
        #  ---- Creamos Cara Poligono Pequeño
        SP = Part.Shape([LPP1, LPP2, LPP3, LPP4, LPP5, LPP6, LPP7, LPP8])
        WP = Part.Wire(SP.Edges)
        FP = Part.Face(WP)
        #  ---- Creamos lineas Caras inclinadas
        LIncl1 = Part.LineSegment(PG1, PP1)
        LIncl2 = Part.LineSegment(PG2, PP2)
        LIncl3 = Part.LineSegment(PG3, PP3)
        LIncl4 = Part.LineSegment(PG4, PP4)
        LIncl5 = Part.LineSegment(PG5, PP5)
        LIncl6 = Part.LineSegment(PG6, PP6)
        LIncl7 = Part.LineSegment(PG7, PP7)
        LIncl8 = Part.LineSegment(PG8, PP8)
        #  ---- Creamos Caras Inclinadas
        SIncl1 = Part.Shape([LIncl1, LPG1, LIncl2, LPP1])
        WIncl1 = Part.Wire(SIncl1.Edges)
        FIncl1 = Part.Face(WIncl1)
        SIncl2 = Part.Shape([LIncl2, LPG2, LIncl3, LPP2])
        WIncl2 = Part.Wire(SIncl2.Edges)
        FIncl2 = Part.Face(WIncl2)
        SIncl3 = Part.Shape([LIncl3, LPG3, LIncl4, LPP3])
        WIncl3 = Part.Wire(SIncl3.Edges)
        FIncl3 = Part.Face(WIncl3)
        SIncl4 = Part.Shape([LIncl4, LPG4, LIncl5, LPP4])
        WIncl4 = Part.Wire(SIncl4.Edges)
        FIncl4 = Part.Face(WIncl4)
        SIncl5 = Part.Shape([LIncl5, LPG5, LIncl6, LPP5])
        WIncl5 = Part.Wire(SIncl5.Edges)
        FIncl5 = Part.Face(WIncl5)
        SIncl6 = Part.Shape([LIncl6, LPG6, LIncl7, LPP6])
        WIncl6 = Part.Wire(SIncl6.Edges)
        FIncl6 = Part.Face(WIncl6)
        SIncl7 = Part.Shape([LIncl7, LPG7, LIncl8, LPP7])
        WIncl7 = Part.Wire(SIncl7.Edges)
        FIncl7 = Part.Face(WIncl7)
        SIncl8 = Part.Shape([LIncl8, LPG8, LIncl1, LPP8])
        WIncl8 = Part.Wire(SIncl8.Edges)
        FIncl8 = Part.Face(WIncl8)
        ###  ----- Hacemos cuerpo Solido Cono Central
        TCono = Part.makeShell(
            [FG, FIncl1, FIncl2, FIncl3, FIncl4, FIncl5, FIncl6, FIncl7, FIncl8, FP]
        )
        #   ----  Junto las caras
        Cono = Part.makeSolid(TCono)
        #   ----  Genero agujeritos de r=1
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(-10, 0, 1.5675), FreeCAD.Vector(1, 0, 0))
        Cono = Cono.cut(Agujero)
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(0, -10, 1.5675), FreeCAD.Vector(0, 1, 0))
        Cono = Cono.cut(Agujero)
        #   ----  muevo el cono a la cara
        Cono.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 90)
        Cono.translate(FreeCAD.Vector(7.8125, 0, 0))
        #   ----  Unimos cono al cuerpo
        P = P.fuse(Cono)
        ###  ---- Hago los Agujeros
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(0, -15, 0), FreeCAD.Vector(0, 1, 0))
        P = P.cut(Agujero)
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(-15, 0, 0), FreeCAD.Vector(1, 0, 0))
        P = P.cut(Agujero)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "TRH_H_BEM_SFT_1W"

        P.Placement = obj.Placement
        obj.Shape = P


class TRH_H_BEM_SFT_2W_180:
    """Conector en 2 caras opuestas Stemfie"""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyString",
            QT_TRANSLATE_NOOP("App::Property", "Code"),
            QT_TRANSLATE_NOOP("App::Property", "Designation"),
            QT_TRANSLATE_NOOP("App::Property", "STEMFIE part number"),
        )
        obj.setEditorMode("Code", 1)

    def execute(self, obj):
        # Genero el cuerpo exterior
        P = Part.makeBox(
            15.625, 15.625, 12.5, FreeCAD.Vector(-7.8125, -7.8125, -6.25), FreeCAD.Vector(0, 0, 1)
        )

        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        Cubo = Part.makeBox(
            12.9, 12.9, 20, FreeCAD.Vector(-6.45, -6.45, -10), FreeCAD.Vector(0, 0, 1)
        )
        P = P.cut(Cubo)

        #  Genero el Cono
        #  Nombro Variables para Facilitar codigo
        LadoG = 4.9291
        EntreCarasG = 11.9
        LadoP = 3.7279
        EntreCarasP = 9
        Altura = 4.6875
        #  Puntos Poligono Grande
        PG1 = FreeCAD.Vector(EntreCarasG / 2, LadoG / 2, 0)
        PG2 = FreeCAD.Vector(LadoG / 2, EntreCarasG / 2, 0)
        PG3 = FreeCAD.Vector(-LadoG / 2, EntreCarasG / 2, 0)
        PG4 = FreeCAD.Vector(-EntreCarasG / 2, LadoG / 2, 0)
        PG5 = FreeCAD.Vector(-EntreCarasG / 2, -LadoG / 2, 0)
        PG6 = FreeCAD.Vector(-LadoG / 2, -EntreCarasG / 2, 0)
        PG7 = FreeCAD.Vector(LadoG / 2, -EntreCarasG / 2, 0)
        PG8 = FreeCAD.Vector(EntreCarasG / 2, -LadoG / 2, 0)
        #  Puntos Poligono Pequeño
        PP1 = FreeCAD.Vector(EntreCarasP / 2, LadoP / 2, Altura)
        PP2 = FreeCAD.Vector(LadoP / 2, EntreCarasP / 2, Altura)
        PP3 = FreeCAD.Vector(-LadoP / 2, EntreCarasP / 2, Altura)
        PP4 = FreeCAD.Vector(-EntreCarasP / 2, LadoP / 2, Altura)
        PP5 = FreeCAD.Vector(-EntreCarasP / 2, -LadoP / 2, Altura)
        PP6 = FreeCAD.Vector(-LadoP / 2, -EntreCarasP / 2, Altura)
        PP7 = FreeCAD.Vector(LadoP / 2, -EntreCarasP / 2, Altura)
        PP8 = FreeCAD.Vector(EntreCarasP / 2, -LadoP / 2, Altura)
        #  ---- Creamos lineas Poligono Grande
        LPG1 = Part.LineSegment(PG1, PG2)
        LPG2 = Part.LineSegment(PG2, PG3)
        LPG3 = Part.LineSegment(PG3, PG4)
        LPG4 = Part.LineSegment(PG4, PG5)
        LPG5 = Part.LineSegment(PG5, PG6)
        LPG6 = Part.LineSegment(PG6, PG7)
        LPG7 = Part.LineSegment(PG7, PG8)
        LPG8 = Part.LineSegment(PG8, PG1)
        #  ---- Creamos Cara Poligono Grande
        SG = Part.Shape([LPG1, LPG2, LPG3, LPG4, LPG5, LPG6, LPG7, LPG8])
        WG = Part.Wire(SG.Edges)
        FG = Part.Face(WG)
        #  ---- Creamos lineas Poligono Pequeño
        LPP1 = Part.LineSegment(PP1, PP2)
        LPP2 = Part.LineSegment(PP2, PP3)
        LPP3 = Part.LineSegment(PP3, PP4)
        LPP4 = Part.LineSegment(PP4, PP5)
        LPP5 = Part.LineSegment(PP5, PP6)
        LPP6 = Part.LineSegment(PP6, PP7)
        LPP7 = Part.LineSegment(PP7, PP8)
        LPP8 = Part.LineSegment(PP8, PP1)
        #  ---- Creamos Cara Poligono Pequeño
        SP = Part.Shape([LPP1, LPP2, LPP3, LPP4, LPP5, LPP6, LPP7, LPP8])
        WP = Part.Wire(SP.Edges)
        FP = Part.Face(WP)
        #  ---- Creamos lineas Caras inclinadas
        LIncl1 = Part.LineSegment(PG1, PP1)
        LIncl2 = Part.LineSegment(PG2, PP2)
        LIncl3 = Part.LineSegment(PG3, PP3)
        LIncl4 = Part.LineSegment(PG4, PP4)
        LIncl5 = Part.LineSegment(PG5, PP5)
        LIncl6 = Part.LineSegment(PG6, PP6)
        LIncl7 = Part.LineSegment(PG7, PP7)
        LIncl8 = Part.LineSegment(PG8, PP8)
        #  ---- Creamos Caras Inclinadas
        SIncl1 = Part.Shape([LIncl1, LPG1, LIncl2, LPP1])
        WIncl1 = Part.Wire(SIncl1.Edges)
        FIncl1 = Part.Face(WIncl1)
        SIncl2 = Part.Shape([LIncl2, LPG2, LIncl3, LPP2])
        WIncl2 = Part.Wire(SIncl2.Edges)
        FIncl2 = Part.Face(WIncl2)
        SIncl3 = Part.Shape([LIncl3, LPG3, LIncl4, LPP3])
        WIncl3 = Part.Wire(SIncl3.Edges)
        FIncl3 = Part.Face(WIncl3)
        SIncl4 = Part.Shape([LIncl4, LPG4, LIncl5, LPP4])
        WIncl4 = Part.Wire(SIncl4.Edges)
        FIncl4 = Part.Face(WIncl4)
        SIncl5 = Part.Shape([LIncl5, LPG5, LIncl6, LPP5])
        WIncl5 = Part.Wire(SIncl5.Edges)
        FIncl5 = Part.Face(WIncl5)
        SIncl6 = Part.Shape([LIncl6, LPG6, LIncl7, LPP6])
        WIncl6 = Part.Wire(SIncl6.Edges)
        FIncl6 = Part.Face(WIncl6)
        SIncl7 = Part.Shape([LIncl7, LPG7, LIncl8, LPP7])
        WIncl7 = Part.Wire(SIncl7.Edges)
        FIncl7 = Part.Face(WIncl7)
        SIncl8 = Part.Shape([LIncl8, LPG8, LIncl1, LPP8])
        WIncl8 = Part.Wire(SIncl8.Edges)
        FIncl8 = Part.Face(WIncl8)
        #   ----  Junto las caras
        TCono = Part.makeShell(
            [FG, FIncl1, FIncl2, FIncl3, FIncl4, FIncl5, FIncl6, FIncl7, FIncl8, FP]
        )
        #   ----  Hacemos 2 Conos Solidos con las caras
        Cono1 = Part.makeSolid(TCono)
        Cono2 = Part.makeSolid(TCono)
        #   ----  Genero agujeritos de r=1
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(-10, 0, 1.5675), FreeCAD.Vector(1, 0, 0))
        Cono1 = Cono1.cut(Agujero)
        Cono2 = Cono2.cut(Agujero)
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(0, -10, 1.5675), FreeCAD.Vector(0, 1, 0))
        Cono1 = Cono1.cut(Agujero)
        Cono2 = Cono2.cut(Agujero)
        #   ----  muevo el cono1 a la cara
        Cono1.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 90)
        Cono1.translate(FreeCAD.Vector(7.8125, 0, 0))
        #   ----  muevo el cono2 a la cara
        Cono2.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), -90)
        Cono2.translate(FreeCAD.Vector(-7.8125, 0, 0))
        #   ----  Unimos conos al cuerpo
        P = P.fuse(Cono1)
        P = P.fuse(Cono2)
        ###  ---- Hago los Agujeros centrales
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(0, -15, 0), FreeCAD.Vector(0, 1, 0))
        P = P.cut(Agujero)
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(-15, 0, 0), FreeCAD.Vector(1, 0, 0))
        P = P.cut(Agujero)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "TRH_H_BEM_SFT_2W_180"

        P.Placement = obj.Placement
        obj.Shape = P


class TRH_H_BEM_SFT_2W_90:
    """Conector en 2 caras contiguas Stemfie"""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyString",
            QT_TRANSLATE_NOOP("App::Property", "Code"),
            QT_TRANSLATE_NOOP("App::Property", "Designation"),
            QT_TRANSLATE_NOOP("App::Property", "STEMFIE part number"),
        )
        obj.setEditorMode("Code", 1)

    def execute(self, obj):
        # Genero el cuerpo exterior
        P = Part.makeBox(
            15.625, 15.625, 12.5, FreeCAD.Vector(-7.8125, -7.8125, -6.25), FreeCAD.Vector(0, 0, 1)
        )

        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        Cubo = Part.makeBox(
            12.9, 12.9, 20, FreeCAD.Vector(-6.45, -6.45, -10), FreeCAD.Vector(0, 0, 1)
        )
        P = P.cut(Cubo)

        #  Genero el Cono
        #  Nombro Variables para Facilitar codigo
        LadoG = 4.9291
        EntreCarasG = 11.9
        LadoP = 3.7279
        EntreCarasP = 9
        Altura = 4.6875
        #  Puntos Poligono Grande
        PG1 = FreeCAD.Vector(EntreCarasG / 2, LadoG / 2, 0)
        PG2 = FreeCAD.Vector(LadoG / 2, EntreCarasG / 2, 0)
        PG3 = FreeCAD.Vector(-LadoG / 2, EntreCarasG / 2, 0)
        PG4 = FreeCAD.Vector(-EntreCarasG / 2, LadoG / 2, 0)
        PG5 = FreeCAD.Vector(-EntreCarasG / 2, -LadoG / 2, 0)
        PG6 = FreeCAD.Vector(-LadoG / 2, -EntreCarasG / 2, 0)
        PG7 = FreeCAD.Vector(LadoG / 2, -EntreCarasG / 2, 0)
        PG8 = FreeCAD.Vector(EntreCarasG / 2, -LadoG / 2, 0)
        #  Puntos Poligono Pequeño
        PP1 = FreeCAD.Vector(EntreCarasP / 2, LadoP / 2, Altura)
        PP2 = FreeCAD.Vector(LadoP / 2, EntreCarasP / 2, Altura)
        PP3 = FreeCAD.Vector(-LadoP / 2, EntreCarasP / 2, Altura)
        PP4 = FreeCAD.Vector(-EntreCarasP / 2, LadoP / 2, Altura)
        PP5 = FreeCAD.Vector(-EntreCarasP / 2, -LadoP / 2, Altura)
        PP6 = FreeCAD.Vector(-LadoP / 2, -EntreCarasP / 2, Altura)
        PP7 = FreeCAD.Vector(LadoP / 2, -EntreCarasP / 2, Altura)
        PP8 = FreeCAD.Vector(EntreCarasP / 2, -LadoP / 2, Altura)
        #  ---- Creamos lineas Poligono Grande
        LPG1 = Part.LineSegment(PG1, PG2)
        LPG2 = Part.LineSegment(PG2, PG3)
        LPG3 = Part.LineSegment(PG3, PG4)
        LPG4 = Part.LineSegment(PG4, PG5)
        LPG5 = Part.LineSegment(PG5, PG6)
        LPG6 = Part.LineSegment(PG6, PG7)
        LPG7 = Part.LineSegment(PG7, PG8)
        LPG8 = Part.LineSegment(PG8, PG1)
        #  ---- Creamos Cara Poligono Grande
        SG = Part.Shape([LPG1, LPG2, LPG3, LPG4, LPG5, LPG6, LPG7, LPG8])
        WG = Part.Wire(SG.Edges)
        FG = Part.Face(WG)
        #  ---- Creamos lineas Poligono Pequeño
        LPP1 = Part.LineSegment(PP1, PP2)
        LPP2 = Part.LineSegment(PP2, PP3)
        LPP3 = Part.LineSegment(PP3, PP4)
        LPP4 = Part.LineSegment(PP4, PP5)
        LPP5 = Part.LineSegment(PP5, PP6)
        LPP6 = Part.LineSegment(PP6, PP7)
        LPP7 = Part.LineSegment(PP7, PP8)
        LPP8 = Part.LineSegment(PP8, PP1)
        #  ---- Creamos Cara Poligono Pequeño
        SP = Part.Shape([LPP1, LPP2, LPP3, LPP4, LPP5, LPP6, LPP7, LPP8])
        WP = Part.Wire(SP.Edges)
        FP = Part.Face(WP)
        #  ---- Creamos lineas Caras inclinadas
        LIncl1 = Part.LineSegment(PG1, PP1)
        LIncl2 = Part.LineSegment(PG2, PP2)
        LIncl3 = Part.LineSegment(PG3, PP3)
        LIncl4 = Part.LineSegment(PG4, PP4)
        LIncl5 = Part.LineSegment(PG5, PP5)
        LIncl6 = Part.LineSegment(PG6, PP6)
        LIncl7 = Part.LineSegment(PG7, PP7)
        LIncl8 = Part.LineSegment(PG8, PP8)
        #  ---- Creamos Caras Inclinadas
        SIncl1 = Part.Shape([LIncl1, LPG1, LIncl2, LPP1])
        WIncl1 = Part.Wire(SIncl1.Edges)
        FIncl1 = Part.Face(WIncl1)
        SIncl2 = Part.Shape([LIncl2, LPG2, LIncl3, LPP2])
        WIncl2 = Part.Wire(SIncl2.Edges)
        FIncl2 = Part.Face(WIncl2)
        SIncl3 = Part.Shape([LIncl3, LPG3, LIncl4, LPP3])
        WIncl3 = Part.Wire(SIncl3.Edges)
        FIncl3 = Part.Face(WIncl3)
        SIncl4 = Part.Shape([LIncl4, LPG4, LIncl5, LPP4])
        WIncl4 = Part.Wire(SIncl4.Edges)
        FIncl4 = Part.Face(WIncl4)
        SIncl5 = Part.Shape([LIncl5, LPG5, LIncl6, LPP5])
        WIncl5 = Part.Wire(SIncl5.Edges)
        FIncl5 = Part.Face(WIncl5)
        SIncl6 = Part.Shape([LIncl6, LPG6, LIncl7, LPP6])
        WIncl6 = Part.Wire(SIncl6.Edges)
        FIncl6 = Part.Face(WIncl6)
        SIncl7 = Part.Shape([LIncl7, LPG7, LIncl8, LPP7])
        WIncl7 = Part.Wire(SIncl7.Edges)
        FIncl7 = Part.Face(WIncl7)
        SIncl8 = Part.Shape([LIncl8, LPG8, LIncl1, LPP8])
        WIncl8 = Part.Wire(SIncl8.Edges)
        FIncl8 = Part.Face(WIncl8)
        #   ----  Junto las caras
        TCono = Part.makeShell(
            [FG, FIncl1, FIncl2, FIncl3, FIncl4, FIncl5, FIncl6, FIncl7, FIncl8, FP]
        )
        #   ----  Hacemos 2 Conos Solidos con las caras
        Cono1 = Part.makeSolid(TCono)
        Cono2 = Part.makeSolid(TCono)
        #   ----  Genero agujeritos de r=1
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(-10, 0, 1.5675), FreeCAD.Vector(1, 0, 0))
        Cono1 = Cono1.cut(Agujero)
        Cono2 = Cono2.cut(Agujero)
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(0, -10, 1.5675), FreeCAD.Vector(0, 1, 0))
        Cono1 = Cono1.cut(Agujero)
        Cono2 = Cono2.cut(Agujero)
        #   ----  muevo el cono1 a la cara
        Cono1.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 90)
        Cono1.translate(FreeCAD.Vector(7.8125, 0, 0))
        #   ----  muevo el cono2 a la cara
        Cono2.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), -90)
        Cono2.translate(FreeCAD.Vector(0, 7.8125, 0))
        #   ----  Unimos conos al cuerpo
        P = P.fuse(Cono1)
        P = P.fuse(Cono2)
        ###  ---- Hago los Agujeros centrales
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(0, -15, 0), FreeCAD.Vector(0, 1, 0))
        P = P.cut(Agujero)
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(-15, 0, 0), FreeCAD.Vector(1, 0, 0))
        P = P.cut(Agujero)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "TRH_H_BEM_SFT_2W_90"

        P.Placement = obj.Placement
        obj.Shape = P


class TRH_H_BEM_SFT_3W:
    """Conector en 3 caras contiguas Stemfie"""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyString",
            QT_TRANSLATE_NOOP("App::Property", "Code"),
            QT_TRANSLATE_NOOP("App::Property", "Designation"),
            QT_TRANSLATE_NOOP("App::Property", "STEMFIE part number"),
        )
        obj.setEditorMode("Code", 1)

    def execute(self, obj):
        # Genero el cuerpo exterior
        P = Part.makeBox(
            15.625, 15.625, 12.5, FreeCAD.Vector(-7.8125, -7.8125, -6.25), FreeCAD.Vector(0, 0, 1)
        )

        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        Cubo = Part.makeBox(
            12.9, 12.9, 20, FreeCAD.Vector(-6.45, -6.45, -10), FreeCAD.Vector(0, 0, 1)
        )
        P = P.cut(Cubo)

        #  Genero el Cono
        #  Nombro Variables para Facilitar codigo
        LadoG = 4.9291
        EntreCarasG = 11.9
        LadoP = 3.7279
        EntreCarasP = 9
        Altura = 4.6875
        #  Puntos Poligono Grande
        PG1 = FreeCAD.Vector(EntreCarasG / 2, LadoG / 2, 0)
        PG2 = FreeCAD.Vector(LadoG / 2, EntreCarasG / 2, 0)
        PG3 = FreeCAD.Vector(-LadoG / 2, EntreCarasG / 2, 0)
        PG4 = FreeCAD.Vector(-EntreCarasG / 2, LadoG / 2, 0)
        PG5 = FreeCAD.Vector(-EntreCarasG / 2, -LadoG / 2, 0)
        PG6 = FreeCAD.Vector(-LadoG / 2, -EntreCarasG / 2, 0)
        PG7 = FreeCAD.Vector(LadoG / 2, -EntreCarasG / 2, 0)
        PG8 = FreeCAD.Vector(EntreCarasG / 2, -LadoG / 2, 0)
        #  Puntos Poligono Pequeño
        PP1 = FreeCAD.Vector(EntreCarasP / 2, LadoP / 2, Altura)
        PP2 = FreeCAD.Vector(LadoP / 2, EntreCarasP / 2, Altura)
        PP3 = FreeCAD.Vector(-LadoP / 2, EntreCarasP / 2, Altura)
        PP4 = FreeCAD.Vector(-EntreCarasP / 2, LadoP / 2, Altura)
        PP5 = FreeCAD.Vector(-EntreCarasP / 2, -LadoP / 2, Altura)
        PP6 = FreeCAD.Vector(-LadoP / 2, -EntreCarasP / 2, Altura)
        PP7 = FreeCAD.Vector(LadoP / 2, -EntreCarasP / 2, Altura)
        PP8 = FreeCAD.Vector(EntreCarasP / 2, -LadoP / 2, Altura)
        #  ---- Creamos lineas Poligono Grande
        LPG1 = Part.LineSegment(PG1, PG2)
        LPG2 = Part.LineSegment(PG2, PG3)
        LPG3 = Part.LineSegment(PG3, PG4)
        LPG4 = Part.LineSegment(PG4, PG5)
        LPG5 = Part.LineSegment(PG5, PG6)
        LPG6 = Part.LineSegment(PG6, PG7)
        LPG7 = Part.LineSegment(PG7, PG8)
        LPG8 = Part.LineSegment(PG8, PG1)
        #  ---- Creamos Cara Poligono Grande
        SG = Part.Shape([LPG1, LPG2, LPG3, LPG4, LPG5, LPG6, LPG7, LPG8])
        WG = Part.Wire(SG.Edges)
        FG = Part.Face(WG)
        #  ---- Creamos lineas Poligono Pequeño
        LPP1 = Part.LineSegment(PP1, PP2)
        LPP2 = Part.LineSegment(PP2, PP3)
        LPP3 = Part.LineSegment(PP3, PP4)
        LPP4 = Part.LineSegment(PP4, PP5)
        LPP5 = Part.LineSegment(PP5, PP6)
        LPP6 = Part.LineSegment(PP6, PP7)
        LPP7 = Part.LineSegment(PP7, PP8)
        LPP8 = Part.LineSegment(PP8, PP1)
        #  ---- Creamos Cara Poligono Pequeño
        SP = Part.Shape([LPP1, LPP2, LPP3, LPP4, LPP5, LPP6, LPP7, LPP8])
        WP = Part.Wire(SP.Edges)
        FP = Part.Face(WP)
        #  ---- Creamos lineas Caras inclinadas
        LIncl1 = Part.LineSegment(PG1, PP1)
        LIncl2 = Part.LineSegment(PG2, PP2)
        LIncl3 = Part.LineSegment(PG3, PP3)
        LIncl4 = Part.LineSegment(PG4, PP4)
        LIncl5 = Part.LineSegment(PG5, PP5)
        LIncl6 = Part.LineSegment(PG6, PP6)
        LIncl7 = Part.LineSegment(PG7, PP7)
        LIncl8 = Part.LineSegment(PG8, PP8)
        #  ---- Creamos Caras Inclinadas
        SIncl1 = Part.Shape([LIncl1, LPG1, LIncl2, LPP1])
        WIncl1 = Part.Wire(SIncl1.Edges)
        FIncl1 = Part.Face(WIncl1)
        SIncl2 = Part.Shape([LIncl2, LPG2, LIncl3, LPP2])
        WIncl2 = Part.Wire(SIncl2.Edges)
        FIncl2 = Part.Face(WIncl2)
        SIncl3 = Part.Shape([LIncl3, LPG3, LIncl4, LPP3])
        WIncl3 = Part.Wire(SIncl3.Edges)
        FIncl3 = Part.Face(WIncl3)
        SIncl4 = Part.Shape([LIncl4, LPG4, LIncl5, LPP4])
        WIncl4 = Part.Wire(SIncl4.Edges)
        FIncl4 = Part.Face(WIncl4)
        SIncl5 = Part.Shape([LIncl5, LPG5, LIncl6, LPP5])
        WIncl5 = Part.Wire(SIncl5.Edges)
        FIncl5 = Part.Face(WIncl5)
        SIncl6 = Part.Shape([LIncl6, LPG6, LIncl7, LPP6])
        WIncl6 = Part.Wire(SIncl6.Edges)
        FIncl6 = Part.Face(WIncl6)
        SIncl7 = Part.Shape([LIncl7, LPG7, LIncl8, LPP7])
        WIncl7 = Part.Wire(SIncl7.Edges)
        FIncl7 = Part.Face(WIncl7)
        SIncl8 = Part.Shape([LIncl8, LPG8, LIncl1, LPP8])
        WIncl8 = Part.Wire(SIncl8.Edges)
        FIncl8 = Part.Face(WIncl8)
        #   ----  Junto las caras
        TCono = Part.makeShell(
            [FG, FIncl1, FIncl2, FIncl3, FIncl4, FIncl5, FIncl6, FIncl7, FIncl8, FP]
        )
        #   ----  Hacemos 3 Conos Solidos con las caras
        Cono1 = Part.makeSolid(TCono)
        Cono2 = Part.makeSolid(TCono)
        Cono3 = Part.makeSolid(TCono)
        #   ----  Genero agujeritos de r=1
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(-10, 0, 1.5675), FreeCAD.Vector(1, 0, 0))
        Cono1 = Cono1.cut(Agujero)
        Cono2 = Cono2.cut(Agujero)
        Cono3 = Cono3.cut(Agujero)
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(0, -10, 1.5675), FreeCAD.Vector(0, 1, 0))
        Cono1 = Cono1.cut(Agujero)
        Cono2 = Cono2.cut(Agujero)
        Cono3 = Cono3.cut(Agujero)
        #   ----  muevo el cono1 a la cara
        Cono1.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 90)
        Cono1.translate(FreeCAD.Vector(7.8125, 0, 0))
        #   ----  muevo el cono2 a la cara
        Cono2.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), -90)
        Cono2.translate(FreeCAD.Vector(0, 7.8125, 0))
        #   ----  muevo el cono3 a la cara
        Cono3.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), -90)
        Cono3.translate(FreeCAD.Vector(-7.8125, 0, 0))
        #   ----  Unimos conos al cuerpo
        P = P.fuse(Cono1)
        P = P.fuse(Cono2)
        P = P.fuse(Cono3)
        ###  ---- Hago los Agujeros centrales
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(0, -15, 0), FreeCAD.Vector(0, 1, 0))
        P = P.cut(Agujero)
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(-15, 0, 0), FreeCAD.Vector(1, 0, 0))
        P = P.cut(Agujero)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "TRH_H_BEM_SFT_3W"

        P.Placement = obj.Placement
        obj.Shape = P


class TRH_H_BEM_SFT_4W:
    """Conector en las 4 caras Stemfie"""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyString",
            QT_TRANSLATE_NOOP("App::Property", "Code"),
            QT_TRANSLATE_NOOP("App::Property", "Designation"),
            QT_TRANSLATE_NOOP("App::Property", "STEMFIE part number"),
        )
        obj.setEditorMode("Code", 1)

    def execute(self, obj):
        # Genero el cuerpo exterior
        P = Part.makeBox(
            15.625, 15.625, 12.5, FreeCAD.Vector(-7.8125, -7.8125, -6.25), FreeCAD.Vector(0, 0, 1)
        )

        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        Cubo = Part.makeBox(
            12.9, 12.9, 20, FreeCAD.Vector(-6.45, -6.45, -10), FreeCAD.Vector(0, 0, 1)
        )
        P = P.cut(Cubo)

        #  Genero el Cono
        #  Nombro Variables para Facilitar codigo
        LadoG = 4.9291
        EntreCarasG = 11.9
        LadoP = 3.7279
        EntreCarasP = 9
        Altura = 4.6875
        #  Puntos Poligono Grande
        PG1 = FreeCAD.Vector(EntreCarasG / 2, LadoG / 2, 0)
        PG2 = FreeCAD.Vector(LadoG / 2, EntreCarasG / 2, 0)
        PG3 = FreeCAD.Vector(-LadoG / 2, EntreCarasG / 2, 0)
        PG4 = FreeCAD.Vector(-EntreCarasG / 2, LadoG / 2, 0)
        PG5 = FreeCAD.Vector(-EntreCarasG / 2, -LadoG / 2, 0)
        PG6 = FreeCAD.Vector(-LadoG / 2, -EntreCarasG / 2, 0)
        PG7 = FreeCAD.Vector(LadoG / 2, -EntreCarasG / 2, 0)
        PG8 = FreeCAD.Vector(EntreCarasG / 2, -LadoG / 2, 0)
        #  Puntos Poligono Pequeño
        PP1 = FreeCAD.Vector(EntreCarasP / 2, LadoP / 2, Altura)
        PP2 = FreeCAD.Vector(LadoP / 2, EntreCarasP / 2, Altura)
        PP3 = FreeCAD.Vector(-LadoP / 2, EntreCarasP / 2, Altura)
        PP4 = FreeCAD.Vector(-EntreCarasP / 2, LadoP / 2, Altura)
        PP5 = FreeCAD.Vector(-EntreCarasP / 2, -LadoP / 2, Altura)
        PP6 = FreeCAD.Vector(-LadoP / 2, -EntreCarasP / 2, Altura)
        PP7 = FreeCAD.Vector(LadoP / 2, -EntreCarasP / 2, Altura)
        PP8 = FreeCAD.Vector(EntreCarasP / 2, -LadoP / 2, Altura)
        #  ---- Creamos lineas Poligono Grande
        LPG1 = Part.LineSegment(PG1, PG2)
        LPG2 = Part.LineSegment(PG2, PG3)
        LPG3 = Part.LineSegment(PG3, PG4)
        LPG4 = Part.LineSegment(PG4, PG5)
        LPG5 = Part.LineSegment(PG5, PG6)
        LPG6 = Part.LineSegment(PG6, PG7)
        LPG7 = Part.LineSegment(PG7, PG8)
        LPG8 = Part.LineSegment(PG8, PG1)
        #  ---- Creamos Cara Poligono Grande
        SG = Part.Shape([LPG1, LPG2, LPG3, LPG4, LPG5, LPG6, LPG7, LPG8])
        WG = Part.Wire(SG.Edges)
        FG = Part.Face(WG)
        #  ---- Creamos lineas Poligono Pequeño
        LPP1 = Part.LineSegment(PP1, PP2)
        LPP2 = Part.LineSegment(PP2, PP3)
        LPP3 = Part.LineSegment(PP3, PP4)
        LPP4 = Part.LineSegment(PP4, PP5)
        LPP5 = Part.LineSegment(PP5, PP6)
        LPP6 = Part.LineSegment(PP6, PP7)
        LPP7 = Part.LineSegment(PP7, PP8)
        LPP8 = Part.LineSegment(PP8, PP1)
        #  ---- Creamos Cara Poligono Pequeño
        SP = Part.Shape([LPP1, LPP2, LPP3, LPP4, LPP5, LPP6, LPP7, LPP8])
        WP = Part.Wire(SP.Edges)
        FP = Part.Face(WP)
        #  ---- Creamos lineas Caras inclinadas
        LIncl1 = Part.LineSegment(PG1, PP1)
        LIncl2 = Part.LineSegment(PG2, PP2)
        LIncl3 = Part.LineSegment(PG3, PP3)
        LIncl4 = Part.LineSegment(PG4, PP4)
        LIncl5 = Part.LineSegment(PG5, PP5)
        LIncl6 = Part.LineSegment(PG6, PP6)
        LIncl7 = Part.LineSegment(PG7, PP7)
        LIncl8 = Part.LineSegment(PG8, PP8)
        #  ---- Creamos Caras Inclinadas
        SIncl1 = Part.Shape([LIncl1, LPG1, LIncl2, LPP1])
        WIncl1 = Part.Wire(SIncl1.Edges)
        FIncl1 = Part.Face(WIncl1)
        SIncl2 = Part.Shape([LIncl2, LPG2, LIncl3, LPP2])
        WIncl2 = Part.Wire(SIncl2.Edges)
        FIncl2 = Part.Face(WIncl2)
        SIncl3 = Part.Shape([LIncl3, LPG3, LIncl4, LPP3])
        WIncl3 = Part.Wire(SIncl3.Edges)
        FIncl3 = Part.Face(WIncl3)
        SIncl4 = Part.Shape([LIncl4, LPG4, LIncl5, LPP4])
        WIncl4 = Part.Wire(SIncl4.Edges)
        FIncl4 = Part.Face(WIncl4)
        SIncl5 = Part.Shape([LIncl5, LPG5, LIncl6, LPP5])
        WIncl5 = Part.Wire(SIncl5.Edges)
        FIncl5 = Part.Face(WIncl5)
        SIncl6 = Part.Shape([LIncl6, LPG6, LIncl7, LPP6])
        WIncl6 = Part.Wire(SIncl6.Edges)
        FIncl6 = Part.Face(WIncl6)
        SIncl7 = Part.Shape([LIncl7, LPG7, LIncl8, LPP7])
        WIncl7 = Part.Wire(SIncl7.Edges)
        FIncl7 = Part.Face(WIncl7)
        SIncl8 = Part.Shape([LIncl8, LPG8, LIncl1, LPP8])
        WIncl8 = Part.Wire(SIncl8.Edges)
        FIncl8 = Part.Face(WIncl8)
        #   ----  Junto las caras
        TCono = Part.makeShell(
            [FG, FIncl1, FIncl2, FIncl3, FIncl4, FIncl5, FIncl6, FIncl7, FIncl8, FP]
        )
        #   ----  Hacemos 3 Conos Solidos con las caras
        Cono1 = Part.makeSolid(TCono)
        Cono2 = Part.makeSolid(TCono)
        Cono3 = Part.makeSolid(TCono)
        Cono4 = Part.makeSolid(TCono)
        #   ----  Genero agujeritos de r=1
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(-10, 0, 1.5675), FreeCAD.Vector(1, 0, 0))
        Cono1 = Cono1.cut(Agujero)
        Cono2 = Cono2.cut(Agujero)
        Cono3 = Cono3.cut(Agujero)
        Cono4 = Cono4.cut(Agujero)
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(0, -10, 1.5675), FreeCAD.Vector(0, 1, 0))
        Cono1 = Cono1.cut(Agujero)
        Cono2 = Cono2.cut(Agujero)
        Cono3 = Cono3.cut(Agujero)
        Cono4 = Cono4.cut(Agujero)
        #   ----  muevo el cono1 a la cara
        Cono1.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 90)
        Cono1.translate(FreeCAD.Vector(7.8125, 0, 0))
        #   ----  muevo el cono2 a la cara
        Cono2.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), -90)
        Cono2.translate(FreeCAD.Vector(0, 7.8125, 0))
        #   ----  muevo el cono3 a la cara
        Cono3.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), -90)
        Cono3.translate(FreeCAD.Vector(-7.8125, 0, 0))
        #   ----  muevo el cono4 a la cara
        Cono4.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 90)
        Cono4.translate(FreeCAD.Vector(0, -7.8125, 0))
        #   ----  Unimos conos al cuerpo
        P = P.fuse(Cono1)
        P = P.fuse(Cono2)
        P = P.fuse(Cono3)
        P = P.fuse(Cono4)
        ###  ---- Hago los Agujeros centrales
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(0, -15, 0), FreeCAD.Vector(0, 1, 0))
        P = P.cut(Agujero)
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(-15, 0, 0), FreeCAD.Vector(1, 0, 0))
        P = P.cut(Agujero)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = "TRH_H_BEM_SFT_4W"

        P.Placement = obj.Placement
        obj.Shape = P
