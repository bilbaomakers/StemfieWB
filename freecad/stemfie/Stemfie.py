import FreeCAD
import FreeCADGui

import os
import random
from freecad.stemfie import ICONPATH, Piezas, Plates, Shafts, get_icon_path

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP


class ViewProvider:
    def __init__(self, obj, icon_fn):
        obj.Proxy = self
        self._check_attr()
        if icon_fn[-3:].lower() != "svg":
            self.icon = get_icon_path("STEMFIE")
        else:
            self.icon_fn = icon_fn or get_icon_path("STEMFIE")

    def _check_attr(self):
        """Check for missing attributes."""

        if not hasattr(self, "icon_fn"):
            setattr(self, "icon_fn", get_icon_path("STEMFIE"))

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
        return {"Pixmap": self.pixmap, "MenuText": self.menutext, "ToolTip": self.tooltip}


# Beams
class STR_ESS(BaseCommand):
    NAME = "STR_ESS"
    FUNCTION = Piezas.STR_ESS
    pixmap = os.path.join(ICONPATH, "Beam STR ESS_icon.png")
    menutext = "STR ESS"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Beam_STR_ESS", "Beam - Straight - Ending Square Square")


class STR_ERR(BaseCommand):
    NAME = "STR_ERR"
    FUNCTION = Piezas.STR_ERR
    pixmap = os.path.join(ICONPATH, "Beam STR ERR_icon.png")
    menutext = "STR ERR"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Beam_STR_ERR", "Beam - Straight - End Round Round")


class STR_BEM(BaseCommand):
    NAME = "STR_BEM"
    FUNCTION = Piezas.STR_BEM
    pixmap = os.path.join(ICONPATH, "Beam STR BEM_icon.png")
    menutext = "STR BEM"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Beam_STR_BEM", "Beam - Straight")


class AGD_ESS_USH_SYM(BaseCommand):
    NAME = "AGD_ESS_USH_SYM"
    FUNCTION = Piezas.AGD_ESS_USH_SYM
    pixmap = os.path.join(ICONPATH, "Beam AGD ESS USH SYM_icon.png")
    menutext = "AGD ESS USH SYM"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Beam_AGD_ESS_USH_SYM", "Beam - Angled - End Square Square - U-shaped - Symmetric"
    )


class STR_BED(BaseCommand):
    NAME = "STR_BED"
    FUNCTION = Piezas.STR_BED
    pixmap = os.path.join(ICONPATH, "Beam STR BED_icon.png")
    menutext = "STR BED"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Beam_STR_BED", "Beam - Straight - BED")  # FIXME: BED?


class STR_BET(BaseCommand):
    NAME = "STR_BET"
    FUNCTION = Piezas.STR_BET
    pixmap = os.path.join(ICONPATH, "Beam STR BET_icon.png")
    menutext = "STR BET"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Beam_STR_BET", "Beam - Straight - BET")  # FIXME: BET?


class STR_BXS_ESS_H(BaseCommand):
    NAME = "STR_BXS_ESS_H"
    FUNCTION = Piezas.STR_BXS_ESS_H
    pixmap = os.path.join(ICONPATH, "Beam STR BXS ESS H_icon.png")
    menutext = "STR BXS ESS H"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Beam_STR_BXS_ESS_H", "Beam - Straight - Box-section - End Square Square - H"
    )


class STR_BXS_ESS_C(BaseCommand):
    NAME = "STR_BXS_ESS_C"
    FUNCTION = Piezas.STR_BXS_ESS_C
    pixmap = os.path.join(ICONPATH, "Beam STR BXS ESS C_icon.png")
    menutext = "STR BXS ESS C"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Beam_STR_BXS_ESS_C", "Beam - Straight - Box-section - End Square Square - C"
    )


# Braces
class STR_STD_ERR(BaseCommand):
    NAME = "STR_STD_ERR"
    FUNCTION = Piezas.STR_STD_ERR
    pixmap = os.path.join(ICONPATH, "Brace STR STD ERR_icon.png")
    menutext = "STR STD ERR"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_STD_ERR", "Brace - Straight - Standard - End Round Round"
    )


class STR_STD_BRD_AZ(BaseCommand):
    NAME = "STR_STD_BRD_AZ"
    FUNCTION = Piezas.STR_STD_BRD_AZ
    pixmap = os.path.join(ICONPATH, "Brace STR STD BRD AZ_icon.png")
    menutext = "STR STD BRD AZ"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_STD_BRD_AZ", "Brace - Straight - Standard - Barbed -  AZ"
    )


class CRN_ERR_ASYM(BaseCommand):
    NAME = "CRN_ERR_ASYM"
    FUNCTION = Piezas.CRN_ERR_ASYM
    pixmap = os.path.join(ICONPATH, "Brace CRN ERR ASYM_icon.png")
    menutext = "CRN ERR ASYM"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_CRN_ERR_ASYM", "Brace - Corner - End Round Round - Asymmetric"
    )


class STR_STD_BRM_AY(BaseCommand):
    NAME = "STR_STD_BRM_AY"
    FUNCTION = Piezas.STR_STD_BRM_AY
    pixmap = os.path.join(ICONPATH, "Brace STR STD BRM AY_icon.png")
    menutext = "STR STD BRM_AY"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_STD_BRM_AY", "Brace - Straight - Standard -  BRM_AY"
    )


class STR_SLT_BE_SYM_ERR(BaseCommand):
    NAME = "STR_SLT_BE_SYM_ERR"
    FUNCTION = Piezas.STR_SLT_BE_SYM_ERR
    pixmap = os.path.join(ICONPATH, "Brace STR SLT BE SYM ERR_icon.png")
    menutext = "STR SLT BE SYM ERR"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_SLT_BE_SYM_ERR",
        "Brace - Standard - Slotted - Both Ends - Symmetric - End Round Round",
    )


class STR_SLT_CNT_ERR(BaseCommand):
    NAME = "STR_SLT_CNT_ERR"
    FUNCTION = Piezas.STR_SLT_CNT_ERR
    pixmap = os.path.join(ICONPATH, "Brace STR SLT CNT ERR_icon.png")
    menutext = "STR SLT CNT ERR"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_SLT_CNT_ERR", "Brace - Straight - Slotted - Centered - End Round Round"
    )


class STR_SLT_FL_ERR(BaseCommand):
    NAME = "STR_SLT_FL_ERR"
    FUNCTION = Piezas.STR_SLT_FL_ERR
    pixmap = os.path.join(ICONPATH, "Brace STR SLT FL ERR_icon.png")
    menutext = "STR SLT FL ERR"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_SLT_FL_ERR", "Brace - Straight - Slotted - Full Length - End Round Round"
    )


class STR_SLT_SE_ERR(BaseCommand):
    NAME = "STR_SLT_SE_ERR"
    FUNCTION = Piezas.STR_SLT_SE_ERR
    pixmap = os.path.join(ICONPATH, "Brace STR SLT SE ERR_icon.png")
    menutext = "STR SLT SE ERR"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_SLT_SE_ERR", "Brace - Straight - Slotted - Single End - End Round Round"
    )


class STR_STD_BRD_AY(BaseCommand):
    NAME = "STR_STD_BRD_AY"
    FUNCTION = Piezas.STR_STD_BRD_AY
    pixmap = os.path.join(ICONPATH, "Brace STR STD BRD AY_icon.png")
    menutext = "STR STD BRD AY"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_STD_BRD_AY", "Brace - Straight - Standard - Barbed - AY"
    )  # FIXME: AY?


class STR_STD_BRT_AZ(BaseCommand):
    NAME = "STR_STD_BRT_AZ"
    FUNCTION = Piezas.STR_STD_BRT_AZ
    pixmap = os.path.join(ICONPATH, "Brace STR STD BRT AZ_icon.png")
    menutext = "STR STD BRT AZ"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_STD_BRT_AZ", "Brace Straight - Standard - BRT AZ"
    )  # FIXME: BRT AZ?


class STR_STD_BRT_AY(BaseCommand):
    NAME = "STR_STD_BRT_AY"
    FUNCTION = Piezas.STR_STD_BRT_AY
    pixmap = os.path.join(ICONPATH, "Brace STR STD BRT AY_icon.png")
    menutext = "STR STD BRT AY"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_STD_BRT_AY", "Brace - Straight - Standard - BRT AY"
    )  # FIXME: RT AY?


class STR_STD_CR(BaseCommand):
    NAME = "STR_STD_CR"
    FUNCTION = Piezas.STR_STD_CR
    pixmap = os.path.join(ICONPATH, "Brace STR STD CR_icon.png")
    menutext = "STR STD CR"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Brace_STR_STD_CR", "Brace - Straight - Standard - CR"
    )  # FIXME: CR? maybe CRN


#  Connectors
class TRH_H_BEM_SFT_1W(BaseCommand):
    NAME = "TRH_H_BEM_SFT_1W"
    FUNCTION = Piezas.TRH_H_BEM_SFT_1W
    pixmap = os.path.join(ICONPATH, "Conector THR H BEM SFT 1W_icon.png")
    menutext = "TRH-H BEM SFT 1W"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Connector_TRH_H_BEM_SFT_1W",
        "Connector - Through-Hole - Beam - Shaft - One-way",
    )


class TRH_H_BEM_SFT_2W_180(BaseCommand):
    NAME = "TRH_H_BEM_SFT_2W_180"
    FUNCTION = Piezas.TRH_H_BEM_SFT_2W_180
    pixmap = os.path.join(ICONPATH, "Conector THR H BEM SFT 2W 180_icon.png")
    menutext = "TRH-H BEM SFT 2W 180º"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Connector_TRH_H_BEM_SFT_2W_180",
        "Connector - Through-Hole - Beam - Shaft - Two-way - 180º",
    )


class TRH_H_BEM_SFT_2W_90(BaseCommand):
    NAME = "TRH_H_BEM_SFT_2W_90"
    FUNCTION = Piezas.TRH_H_BEM_SFT_2W_90
    pixmap = os.path.join(ICONPATH, "Conector THR H BEM SFT 2W 90_icon.png")
    menutext = "TRH-H BEM SFT 2W 90º"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Connector_TRH_H_BEM_SFT_2W_90",
        "Connector - Through-Hole - Beam - Shaft - Two-way - 90º",
    )


class TRH_H_BEM_SFT_3W(BaseCommand):
    NAME = "TRH_H_BEM_SFT_3W"
    FUNCTION = Piezas.TRH_H_BEM_SFT_3W
    pixmap = os.path.join(ICONPATH, "Conector THR H BEM SFT 3W_icon.png")
    menutext = "TRH-H BEM SFT 3W"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Connector_TRH_H_BEM_SFT_3W",
        "Connector - Through-Hole - Beam - Shaft - Three-way",
    )


class TRH_H_BEM_SFT_4W(BaseCommand):
    NAME = "TRH_H_BEM_SFT_4W"
    FUNCTION = Piezas.TRH_H_BEM_SFT_4W
    pixmap = os.path.join(ICONPATH, "Conector THR H BEM SFT 4W_icon.png")
    menutext = "TRH-H BEM SFT 4W"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Connector_TRH_H_BEM_SFT_4W",
        "Connector - Through-Hole - Beam - Shaft - Four-way",
    )


# Plates
class PLT_TRI(BaseCommand):
    NAME = "PLT_TRI"
    FUNCTION = Plates.PLT_TRI
    pixmap = os.path.join(ICONPATH, "Plate_TRI.svg")
    menutext = "PLT TRI"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Plate_TRI_PLT", "Plate - Triangular")


class PLT_SQR(BaseCommand):
    NAME = "PLT_SQR"
    FUNCTION = Plates.PLT_SQR
    pixmap = os.path.join(ICONPATH, "Plate_SQR.svg")
    menutext = "PLT SQR"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Plate_SQR", "Plate - Square")


class PLT_HEX(BaseCommand):
    NAME = "PLT_HEX"
    FUNCTION = Plates.PLT_HEX
    pixmap = os.path.join(ICONPATH, "Plate_HEX.svg")
    menutext = "PLT HEX"
    tooltip = QT_TRANSLATE_NOOP("STEMFIE_Plate_HEX", "Plate - Hexagonal")


# Shafts
class SFT_PLN(BaseCommand):
    NAME = "SFT_PLN"
    FUNCTION = Shafts.SFT_PLN
    pixmap = os.path.join(ICONPATH, "SFT_PLN.svg")
    menutext = "SFT PLN"
    tooltip = QT_TRANSLATE_NOOP(
        "STEMFIE_Shaft_SFT_PLN",
        "Shaft - Plain",
    )


#  Comandos
class Cmd_Listado:
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
            "MenuText": QT_TRANSLATE_NOOP("STEMFIE_Cmd_Listado", "Part list"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "STEMFIE_Cmd_Listado", "Print a list of the STEMFIE parts on the tree"
            ),
        }


# Beams
FreeCADGui.addCommand("STEMFIE_Beam_STR_ESS", STR_ESS())
FreeCADGui.addCommand("STEMFIE_Beam_STR_ERR", STR_ERR())
FreeCADGui.addCommand("STEMFIE_Beam_STR_BEM", STR_BEM())
FreeCADGui.addCommand("STEMFIE_Beam_AGD_ESS_USH_SYM", AGD_ESS_USH_SYM())
FreeCADGui.addCommand("STEMFIE_Beam_STR_BED", STR_BED())
FreeCADGui.addCommand("STEMFIE_Beam_STR_BET", STR_BET())
FreeCADGui.addCommand("STEMFIE_Beam_STR_BXS_ESS_H", STR_BXS_ESS_H())
FreeCADGui.addCommand("STEMFIE_Beam_STR_BXS_ESS_C", STR_BXS_ESS_C())
# Braces
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_ERR", STR_STD_ERR())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_BRD_AZ", STR_STD_BRD_AZ())
FreeCADGui.addCommand("STEMFIE_Brace_CRN_ERR_ASYM", CRN_ERR_ASYM())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_BRM_AY", STR_STD_BRM_AY())
FreeCADGui.addCommand("STEMFIE_Brace_STR_SLT_BE_SYM_ERR", STR_SLT_BE_SYM_ERR())
FreeCADGui.addCommand("STEMFIE_Brace_STR_SLT_CNT_ERR", STR_SLT_CNT_ERR())
FreeCADGui.addCommand("STEMFIE_Brace_STR_SLT_FL_ERR", STR_SLT_FL_ERR())
FreeCADGui.addCommand("STEMFIE_Brace_STR_SLT_SE_ERR", STR_SLT_SE_ERR())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_BRD_AY", STR_STD_BRD_AY())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_BRT_AZ", STR_STD_BRT_AZ())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_BRT_AY", STR_STD_BRT_AY())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_CR", STR_STD_CR())
# Connectors
FreeCADGui.addCommand("STEMFIE_Connector_TRH_H_BEM_SFT_1W", TRH_H_BEM_SFT_1W())
FreeCADGui.addCommand("STEMFIE_Connector_TRH_H_BEM_SFT_2W_180", TRH_H_BEM_SFT_2W_180())
FreeCADGui.addCommand("STEMFIE_Connector_TRH_H_BEM_SFT_2W_90", TRH_H_BEM_SFT_2W_90())
FreeCADGui.addCommand("STEMFIE_Connector_TRH_H_BEM_SFT_3W", TRH_H_BEM_SFT_3W())
FreeCADGui.addCommand("STEMFIE_Connector_TRH_H_BEM_SFT_4W", TRH_H_BEM_SFT_4W())
# Plates
FreeCADGui.addCommand("STEMFIE_Plate_TRI", PLT_TRI())
FreeCADGui.addCommand("STEMFIE_Plate_SQR", PLT_SQR())
FreeCADGui.addCommand("STEMFIE_Plate_HEX", PLT_HEX())
# Shafts
FreeCADGui.addCommand("STEMFIE_Shaft_SFT_PLN", SFT_PLN())
# Comandos
FreeCADGui.addCommand("STEMFIE_Cmd_Listado", Cmd_Listado())
