#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import FreeCAD

from freecad.stemfie.utils import (
    BLOCK_UNIT,
    HOLE_DIAMETER_STANDARD,
    make_chamfered_ring,
)

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP


class SPACER:
    def __init__(self, obj):
        obj.Proxy = self  #  really needed
        obj.addProperty(
            "App::PropertyString",
            QT_TRANSLATE_NOOP("App::Property", "Code"),
            QT_TRANSLATE_NOOP("App::Property", "Designation"),
            QT_TRANSLATE_NOOP(
                "App::Property",
                "Unique identifier based on the features and dimensions of the part",
            ),
        )
        obj.setEditorMode("Code", 1)
        obj.addProperty(
            "App::PropertyFloatConstraint",
            QT_TRANSLATE_NOOP("App::Property", "Height"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP(
                "App::Property",
                "Create simplified shape, holes are not chamfered and upper face is totally flush",
            ),
        ).Height = (0.5, 0.25, 10, 0.25)


class FRE(SPACER):
    def __init__(self, obj):
        super().__init__(obj)

    # FIXME: include the internal sphere cuts
    def execute(self, obj):
        #  ---- Bucle para agujeros
        p = make_chamfered_ring(HOLE_DIAMETER_STANDARD, BLOCK_UNIT, obj.Height * BLOCK_UNIT)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = f"Spacer FRE BU01.00x{obj.Height:05.02}"

        obj.Shape = p

        obj.Shape = p
