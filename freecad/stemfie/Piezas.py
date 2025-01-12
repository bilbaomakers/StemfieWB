#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# #####################################################################################
#         -------------    Piezas.py   ---------------------------
#  Este código contiene la geometría y propiedades de las piezas de Stemfie
#
#  Realizado por: Ander González
#  Socio BilbaoMaker #53
#  Fecha : 04-05-2021
#####################################################################################

import FreeCAD

from freecad.stemfie import Beams, Braces, Connectors

translate = FreeCAD.Qt.translate
QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP


# NOTE: Classes below this chunk are kept for migration purposes.
# The migration method used is "Method 2. Migration when restoring the document"
# from: https://wiki.freecad.org/Scripted_objects_migration
# The view provider is not changed.

msg = translate("Log", "Object migration was successful, using new proxy class.\n")


# NOTE: Beams-migration section


class STR_ESS:
    def onDocumentRestored(self, obj):
        Beams.STR_ESS(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_ERR:
    def onDocumentRestored(self, obj):
        Beams.STR_ERR(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_BEM:
    def onDocumentRestored(self, obj):
        Beams.STR_BEM(obj)
        FreeCAD.Console.PrintWarning(msg)


class AGD_ESS_USH_SYM:
    def onDocumentRestored(self, obj):
        Beams.AGD_USH_SYM_ESS(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_DBL:
    def onDocumentRestored(self, obj):
        Beams.STR_DBL(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_TRPL:
    def onDocumentRestored(self, obj):
        Beams.STR_TRPL(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_BXS_ESS_H:
    def onDocumentRestored(self, obj):
        Beams.STR_BXS_ESS_H(obj)
        FreeCAD.Console.PrintWarning(msg)


class STR_BXS_ESS_C:
    def onDocumentRestored(self, obj):
        Beams.STR_BXS_ESS_C(obj)
        FreeCAD.Console.PrintWarning(msg)


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
