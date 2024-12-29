import os
import random

import FreeCAD
import FreeCADGui

from freecad.stemfie import (
    ICONPATH,
    Braces,
    Connectors,
    Plates,
    Shafts,
    get_icon_path,
)

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP


class ViewProvider:
    def __init__(self, obj, icon_fn):
        obj.Proxy = self
        self._check_attr()
        self.icon_fn = get_icon_path(icon_fn or "STEMFIE")  # full path

    def _check_attr(self):
        """Check for missing attributes."""
        if not hasattr(self, "icon_fn"):
            setattr(self, "icon_fn", get_icon_path("STEMFIE"))  # full path

    def getIcon(self):
        """Returns the path to the SVG icon."""
        self._check_attr()
        return self.icon_fn


class BaseCommand:
    """Make commands unavailable when there is no active document"""

    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
            return False
        else:
            return True

    def Activated(self):
        FreeCADGui.doCommandGui("import freecad.stemfie.Stemfie")
        FreeCADGui.doCommandGui(
            "freecad.stemfie.Stemfie.{}.create()".format(self.__class__.__name__)
        )
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    @classmethod
    def create(cls):
        if FreeCAD.GuiUp:
            # borrowed from threaded profiles
            # puts the gear into an active container
            body = FreeCADGui.ActiveDocument.ActiveView.getActiveObject("pdbody")
            part = FreeCADGui.ActiveDocument.ActiveView.getActiveObject("part")

            if body:
                obj = FreeCAD.ActiveDocument.addObject("PartDesign::FeaturePython", cls.NAME)
            else:
                obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", cls.NAME)
            ViewProvider(obj.ViewObject, cls.pixmap)
            cls.FUNCTION(obj)

            if body:
                body.addObject(obj)
            elif part:
                part.Group += [obj]
        else:
            obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", cls.NAME)
            cls.FUNCTION(obj)

        obj.ViewObject.ShapeColor = tuple(random.random() for _ in range(3))

        return obj

    def GetResources(self):
        # We can use this without the full path because we used `FreeCADGui.addIconPath()`
        return {
            "Pixmap": self.pixmap,
            "MenuText": self.menutext,
            "ToolTip": self.tooltip,
        }


# Beams
class STR_ESS(BaseCommand):
    NAME = "STR_ESS"
    FUNCTION = Piezas.STR_ESS
    pixmap = "STR_ESS"
    menutext = "STR ESS"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Beam_STR_ESS", "Beam - Straight - End Square Square")


class STR_ERR(BaseCommand):
    NAME = "STR_ERR"
    FUNCTION = Piezas.STR_ERR
    pixmap = "STR_ERR"
    menutext = "STR ERR"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Beam_STR_ERR", "Beam - Straight - End Round Round")


class STR_BEM(BaseCommand):
    NAME = "STR_BEM"
    FUNCTION = Piezas.STR_BEM
    pixmap = "STR_BEM"
    menutext = "STR BEM"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Beam_STR_BEM", "Beam - Block")


class AGD_ESS_USH_SYM(BaseCommand):
    NAME = "AGD_ESS_USH_SYM"
    FUNCTION = Piezas.AGD_ESS_USH_SYM
    pixmap = "AGD_ESS_USH_SYM"
    menutext = "AGD ESS USH SYM"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Beam_AGD_ESS_USH_SYM", "Beam - Angled - End Square Square - U-shaped - Symmetric"
    )


class STR_DBL(BaseCommand):
    NAME = "STR_DBL"
    FUNCTION = Piezas.STR_DBL
    pixmap = "STR_DBL"
    menutext = "STR DBL"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Beam_STR_DBL", "Beam - Straight - Double")


class STR_TRPL(BaseCommand):
    NAME = "STR_TRPL"
    FUNCTION = Piezas.STR_TRPL
    pixmap = "STR_TRPL"
    menutext = "STR TRPL"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Beam_STR_TRPL", "Beam - Straight - Triple")


class STR_BXS_ESS_H(BaseCommand):
    NAME = "STR_BXS_ESS_H"
    FUNCTION = Piezas.STR_BXS_ESS_H
    pixmap = "STR_BXS_ESS_H"
    menutext = "STR BXS ESS H"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Beam_STR_BXS_ESS_H",
        "Beam - Straight - Box-section - End Square Square - Full Length",
    )


class STR_BXS_ESS_C(BaseCommand):
    NAME = "STR_BXS_ESS_C"
    FUNCTION = Piezas.STR_BXS_ESS_C
    pixmap = "STR_BXS_ESS_C"
    menutext = "STR BXS ESS C"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Beam_STR_BXS_ESS_C",
        "Beam - Straight - Box-section - End Square Square - Holes at ends",
    )


# Braces
class STR_STD_ERR(BaseCommand):
    NAME = "STR_STD_ERR"
    FUNCTION = Braces.STR_STD_ERR
    pixmap = "STR_STD_ERR"
    menutext = "STR STD ERR"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_STD_ERR", "Brace - Straight - Standard - End Round Round"
    )


class CRN_ERR_ASYM(BaseCommand):
    NAME = "CRN_ERR_ASYM"
    FUNCTION = Braces.CRN_ERR_ASYM
    pixmap = "CRN_ERR_ASYM"
    menutext = "CRN ERR ASYM"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_CRN_ERR_ASYM", "Brace - Corner - End Round Round - Asymmetric"
    )


class STR_STD_SQR_AY(BaseCommand):
    NAME = "STR_STD_SQR_AY"
    FUNCTION = Braces.STR_STD_SQR_AY
    pixmap = "STR_STD_SQR_AY"
    menutext = "STR STD SQR AY"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_STD_SQR_AY", "Brace - Straight - Standard - Square - Axis Y"
    )


# TODO: One slotted missing
class STR_SLT_BE_SYM_ERR(BaseCommand):
    NAME = "STR_SLT_BE_SYM_ERR"
    FUNCTION = Braces.STR_SLT_BE_SYM_ERR
    pixmap = "STR_SLT_BE_SYM_ERR"
    menutext = "STR SLT BE SYM ERR"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_SLT_BE_SYM_ERR",
        "Brace - Standard - Slotted - Both Ends - Symmetric - End Round Round",
    )


class STR_SLT_CNT_ERR(BaseCommand):
    NAME = "STR_SLT_CNT_ERR"
    FUNCTION = Braces.STR_SLT_CNT_ERR
    pixmap = "STR_SLT_CNT_ERR"
    menutext = "STR SLT CNT ERR"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_SLT_CNT_ERR", "Brace - Straight - Slotted - Centered - End Round Round"
    )


class STR_SLT_FL_ERR(BaseCommand):
    NAME = "STR_SLT_FL_ERR"
    FUNCTION = Braces.STR_SLT_FL_ERR
    pixmap = "STR_SLT_FL_ERR"
    menutext = "STR SLT FL ERR"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_SLT_FL_ERR", "Brace - Straight - Slotted - Full Length - End Round Round"
    )


class STR_SLT_SE_ERR(BaseCommand):
    NAME = "STR_SLT_SE_ERR"
    FUNCTION = Braces.STR_SLT_SE_ERR
    pixmap = "STR_SLT_SE_ERR"
    menutext = "STR SLT SE ERR"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_SLT_SE_ERR", "Brace - Straight - Slotted - Single End - End Round Round"
    )


class STR_STD_DBL_AZ(BaseCommand):
    NAME = "STR_STD_DBL_AZ"
    FUNCTION = Braces.STR_STD_DBL_AZ
    pixmap = "STR_STD_DBL_AZ"
    menutext = "STR STD DBL AZ"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_STD_DBL_AZ", "Brace - Straight - Standard - Double - Axis Z"
    )


class STR_STD_DBL_AY(BaseCommand):
    NAME = "STR_STD_DBL_AY"
    FUNCTION = Braces.STR_STD_DBL_AY
    pixmap = "STR_STD_DBL_AY"
    menutext = "STR STD DBL AY"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_STD_DBL_AY", "Brace - Straight - Standard - Double - Axis Y"
    )


class STR_STD_TRPL_AZ(BaseCommand):
    NAME = "STR_STD_TRPL_AZ"
    FUNCTION = Braces.STR_STD_TRPL_AZ
    pixmap = "STR_STD_TRPL_AZ"
    menutext = "STR STD TRPL AZ"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_STD_TRPL_AZ", "Brace - Straight - Standard - Triple - Axis Z"
    )


class STR_STD_TRPL_AY(BaseCommand):
    NAME = "STR_STD_TRPL_AY"
    FUNCTION = Braces.STR_STD_TRPL_AY
    pixmap = "STR_STD_TRPL_AY"
    menutext = "STR STD TRPL AY"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_STD_TRPL_AY", "Brace - Straight - Standard - Triple - Axis Y"
    )


class STR_STD_CRS(BaseCommand):
    NAME = "STR_STD_CRS"
    FUNCTION = Braces.STR_STD_CRS
    pixmap = "STR_STD_CRS"
    menutext = "STR STD CRS"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Brace_STR_STD_CRS", "Brace - Straight - Standard - Cross")


# NOTE: Connectors section


class BEM_TRH_H_SFT_1W(BaseCommand):
    NAME = "BEM_TRH_H_SFT_1W"
    FUNCTION = Connectors.BEM_TRH_H_SFT_1W
    pixmap = "TRH-H_BEM_SFT_1W"
    menutext = "BEM TRH-H SFT 1W"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Connector_TRH_H_BEM_SFT_1W",
        "Connector - Beam - Through-Hole - Shaft - One-way",
    )


class BEM_TRH_H_SFT_2W_90(BaseCommand):
    NAME = "BEM_TRH_H_SFT_2W_90"
    FUNCTION = Connectors.BEM_TRH_H_SFT_2W_90
    pixmap = "TRH-H_BEM_SFT_2W_90"
    menutext = "BEM TRH-H SFT 2W 90º"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Connector_BEM_TRH_H_SFT_2W_90",
        "Connector - Beam - Through-Hole - Shaft - Two-way - 90º",
    )


class BEM_TRH_H_SFT_2W_180(BaseCommand):
    NAME = "BEM_TRH_H_SFT_2W_180"
    FUNCTION = Connectors.BEM_TRH_H_SFT_2W_180
    pixmap = "TRH-H_BEM_SFT_2W_180"
    menutext = "BEM TRH-H SFT 2W 180º"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Connector_BEM_TRH_H_SFT_2W_180",
        "Connector - Beam - Through-Hole - Shaft - Two-way - 180º",
    )


class BEM_TRH_H_SFT_3W(BaseCommand):
    NAME = "BEM_TRH_H_SFT_3W"
    FUNCTION = Connectors.BEM_TRH_H_SFT_3W
    pixmap = "TRH-H_BEM_SFT_3W"
    menutext = "BEM TRH-H SFT 3W"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Connector_BEM_TRH_H_SFT_3W",
        "Connector - Beam - Through-Hole - Shaft - Three-way",
    )


class BEM_TRH_H_SFT_4W(BaseCommand):
    NAME = "BEM_TRH_H_SFT_4W"
    FUNCTION = Connectors.BEM_TRH_H_SFT_4W
    pixmap = "TRH-H_BEM_SFT_4W"
    menutext = "BEM TRH-H SFT 4W"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Connector_BEM_TRH_H_SFT_4W",
        "Connector - Beam - Through-Hole - Shaft - Four-way",
    )


# Plates
class PLT_TRI(BaseCommand):
    NAME = "PLT_TRI"
    FUNCTION = Plates.PLT_TRI
    pixmap = "Plate_TRI"
    menutext = "PLT TRI"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Plate_TRI", "Plate - Triangular")


class PLT_SQR(BaseCommand):
    NAME = "PLT_SQR"
    FUNCTION = Plates.PLT_SQR
    pixmap = "Plate_SQR"
    menutext = "PLT SQR"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Plate_SQR", "Plate - Square")


class PLT_HEX(BaseCommand):
    NAME = "PLT_HEX"
    FUNCTION = Plates.PLT_HEX
    pixmap = "Plate_HEX"
    menutext = "PLT HEX"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Plate_HEX", "Plate - Hexagonal")


# Shafts
class SFT_IDX(BaseCommand):
    NAME = "SFT_IDX"
    FUNCTION = Shafts.SFT_IDX
    pixmap = "SFT_IDX"
    menutext = "SFT IDX"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Shaft_SFT_IDX", "Shaft - Indexing")


class SFT_PLN(BaseCommand):
    NAME = "SFT_PLN"
    FUNCTION = Shafts.SFT_PLN
    pixmap = "SFT_PLN"
    menutext = "SFT PLN"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Shaft_SFT_PLN", "Shaft - Plain")


# Utilities
class PartsList:
    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
            return False
        else:
            return True

    def Activated(self):
        from freecad.stemfie import Comandos

        Comandos.ListadoPiezas()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "BoM.svg"),
            "MenuText": QT_TRANSLATE_NOOP("STEMFIE_PartsList", "Parts list"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "STEMFIE_PartsList", "Print a list of the STEMFIE parts on the tree to the console"
            ),
        }


# Beams
FreeCADGui.addCommand("STEMFIE_Beam_STR_ESS", STR_ESS())
FreeCADGui.addCommand("STEMFIE_Beam_STR_ERR", STR_ERR())
FreeCADGui.addCommand("STEMFIE_Beam_STR_BEM", STR_BEM())
FreeCADGui.addCommand("STEMFIE_Beam_AGD_ESS_USH_SYM", AGD_ESS_USH_SYM())
FreeCADGui.addCommand("STEMFIE_Beam_STR_DBL", STR_DBL())
FreeCADGui.addCommand("STEMFIE_Beam_STR_TRPL", STR_TRPL())
FreeCADGui.addCommand("STEMFIE_Beam_STR_BXS_ESS_H", STR_BXS_ESS_H())
FreeCADGui.addCommand("STEMFIE_Beam_STR_BXS_ESS_C", STR_BXS_ESS_C())
# Braces
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_ERR", STR_STD_ERR())
FreeCADGui.addCommand("STEMFIE_Brace_CRN_ERR_ASYM", CRN_ERR_ASYM())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_SQR_AY", STR_STD_SQR_AY())
FreeCADGui.addCommand("STEMFIE_Brace_STR_SLT_BE_SYM_ERR", STR_SLT_BE_SYM_ERR())
FreeCADGui.addCommand("STEMFIE_Brace_STR_SLT_CNT_ERR", STR_SLT_CNT_ERR())
FreeCADGui.addCommand("STEMFIE_Brace_STR_SLT_FL_ERR", STR_SLT_FL_ERR())
FreeCADGui.addCommand("STEMFIE_Brace_STR_SLT_SE_ERR", STR_SLT_SE_ERR())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_DBL_AZ", STR_STD_DBL_AZ())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_DBL_AY", STR_STD_DBL_AY())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_TRPL_AZ", STR_STD_TRPL_AZ())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_TRPL_AY", STR_STD_TRPL_AY())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_CRS", STR_STD_CRS())
# Connectors
FreeCADGui.addCommand("STEMFIE_Connector_TRH_H_BEM_SFT_1W", TRH_H_BEM_SFT_1W())
FreeCADGui.addCommand("STEMFIE_Connector_TRH_H_BEM_SFT_2W_90", TRH_H_BEM_SFT_2W_90())
FreeCADGui.addCommand("STEMFIE_Connector_TRH_H_BEM_SFT_2W_180", TRH_H_BEM_SFT_2W_180())
FreeCADGui.addCommand("STEMFIE_Connector_TRH_H_BEM_SFT_3W", TRH_H_BEM_SFT_3W())
FreeCADGui.addCommand("STEMFIE_Connector_TRH_H_BEM_SFT_4W", TRH_H_BEM_SFT_4W())
# Plates
FreeCADGui.addCommand("STEMFIE_Plate_TRI", PLT_TRI())
FreeCADGui.addCommand("STEMFIE_Plate_SQR", PLT_SQR())
FreeCADGui.addCommand("STEMFIE_Plate_HEX", PLT_HEX())
# Shafts
FreeCADGui.addCommand("STEMFIE_Shaft_SFT_PLN", SFT_PLN())
FreeCADGui.addCommand("STEMFIE_Shaft_SFT_IDX", SFT_IDX())
# Utilities
FreeCADGui.addCommand("STEMFIE_PartsList", PartsList())
