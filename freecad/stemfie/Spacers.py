#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import FreeCAD

from freecad.stemfie.utils import (
    BLOCK_UNIT,
    BLOCK_UNIT_HALF,
    BLOCK_UNIT_QUARTER,
    HOLE_DIAMETER_STANDARD,
    make_chamfered_ring,
    make_stemfie_shape,
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


class BUD_FRE(SPACER):
    def __init__(self, obj):
        super().__init__(obj)
        self.valid_values = [
            BLOCK_UNIT + 0.8,
            BLOCK_UNIT + BLOCK_UNIT_QUARTER,
            BLOCK_UNIT + BLOCK_UNIT_HALF,
            2 * BLOCK_UNIT - BLOCK_UNIT_QUARTER,
            2 * BLOCK_UNIT,
        ]
        obj.addProperty(
            "App::PropertyEnumeration",
            QT_TRANSLATE_NOOP("App::Property", "ExternalDiameter"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "External diameter of the spacer"),
        ).ExternalDiameter = self.valid_values
        # obj.ExternalDiameter = valid_values[0]

    def execute(self, obj):
        #  ---- Bucle para agujeros
        p = make_chamfered_ring(
            BLOCK_UNIT, float(obj.ExternalDiameter), obj.Height * BLOCK_UNIT, 0.1
        )
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        ext_d = (
            f"{obj.ExternalDiameter}+0.8mm"
            if obj.Height == self.valid_values[0]
            else f"{obj.ExternalDiameter}"
        )
        obj.Code = f"Spacer BUD FRE PLN BU{ext_d}x{obj.Height:07.02}"

        obj.Shape = p


class FXD(SPACER):
    def __init__(self, obj):
        super().__init__(obj)

    def execute(self, obj):
        #  ---- Bucle para agujeros
        p = make_stemfie_shape(obj.Height * BLOCK_UNIT)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = f"Spacer FXD BU01.00x{obj.Height:05.02}"

        obj.Shape = p
