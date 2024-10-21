import FreeCAD
import FreeCADGui

import os

from freecad.stemfie import ICONPATH, Piezas


# Brazos
class STR_STD_ERR_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_STD_ERR")
        Piezas.STR_STD_ERR(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Brace STR STD ERR_icon.png"),
            "MenuText": "STR STD ERR",
            "ToolTip": "Brace - Straight - Ending Round Round",
        }


class STR_STD_BRD_AZ_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_STD_BRD_AZ")
        # myObj = FreeCAD.ActiveDocument.addObject("Part::Refine","STR_STD_BRD_AZ")
        Piezas.STR_STD_BRD_AZ(myObj)
        myObj.ViewObject.Proxy = 0

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Brace STR STD BRD AZ_icon.png"),
            "MenuText": "STR STD BRD AZ",
            "ToolTip": "Brace STR STD BRD AZ",
        }


class CRN_ERR_ASYM_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "CRN_ERR_ASYM")
        Piezas.CRN_ERR_ASYM(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Brace CRN ERR ASYM_icon.png"),
            "MenuText": "CRN ERR ASYM",
            "ToolTip": "Brace CRN ERR ASYM",
        }


class STR_STD_BRM_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_STD_BRM")
        Piezas.STR_STD_BRM(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Brace STR STD BRM_icon.png"),
            "MenuText": "STR STD BRM",
            "ToolTip": "Brace STR STD BRM",
        }


class STR_STD_BRM_AY_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_STD_BRM_AY")
        Piezas.STR_STD_BRM_AY(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Brace STR STD BRM AY_icon.png"),
            "MenuText": "STR STD BRM_AY",
            "ToolTip": "Brace STR STD BRM_AY",
        }


class STR_SLT_BE_SYM_ERR_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_SLT_BE_SYM_ERR")
        Piezas.STR_SLT_BE_SYM_ERR(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Brace STR SLT BE SYM ERR_icon.png"),
            "MenuText": "STR SLT BE SYM ERR",
            "ToolTip": "Brace STR SLT BE SYM ERR",
        }


class STR_SLT_CNT_ERR_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_SLT_CNT_ERR")
        Piezas.STR_SLT_CNT_ERR(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Brace STR SLT CNT ERR_icon.png"),
            "MenuText": "STR SLT CNT ERR",
            "ToolTip": "Brace STR SLT CNT ERR",
        }


class STR_SLT_FL_ERR_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_SLT_FL_ERR")
        Piezas.STR_SLT_FL_ERR(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Brace STR SLT FL ERR_icon.png"),
            "MenuText": "STR SLT FL ERR",
            "ToolTip": "Brace - Straight - Slotted - Full Length - Ending Round Round",
        }


class STR_SLT_SE_ERR_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_SLT_SE_ERR")
        Piezas.STR_SLT_SE_ERR(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Brace STR SLT SE ERR_icon.png"),
            "MenuText": "STR SLT SE ERR",
            "ToolTip": "Brace - Straight - Slotted - Single End - Ending Round Round",
        }


class STR_STD_BRD_AY_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_STD_BRD_AY")
        Piezas.STR_STD_BRD_AY(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Brace STR STD BRD AY_icon.png"),
            "MenuText": "STR STD BRD AY",
            "ToolTip": "Brace STR STD BRD AY",
        }


class STR_STD_BRT_AZ_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_STD_BRT_AZ")
        Piezas.STR_STD_BRT_AZ(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Brace STR STD BRT AZ_icon.png"),
            "MenuText": "STR STD BRT AZ",
            "ToolTip": "Brace STR STD BRT AZ",
        }


class STR_STD_BRT_AY_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_STD_BRT_AY")
        Piezas.STR_STD_BRT_AY(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Brace STR STD BRT AY_icon.png"),
            "MenuText": "STR STD BRT AY",
            "ToolTip": "Brace STR STD BRT AY",
        }


class STR_STD_CR_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_STD_CR")
        Piezas.STR_STD_CR(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Brace STR STD CR_icon.png"),
            "MenuText": "STR STD CR",
            "ToolTip": "Brace STR STD CR",
        }


# Vigas
class STR_ESS_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_ESS")
        Piezas.STR_ESS(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Beam STR ESS_icon.png"),
            "MenuText": "STR ESS",
            "ToolTip": "Beam - Straight - Ending Square/Square",
        }


class STR_ERR_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_ERR")
        Piezas.STR_ERR(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Beam STR ERR_icon.png"),
            "MenuText": "STR ERR",
            "ToolTip": "Beam - Straight - Ending Round/Round",
        }


class STR_BEM_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_BEM")
        Piezas.STR_BEM(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Beam STR BEM_icon.png"),
            "MenuText": "STR BEM",
            "ToolTip": "Beam STR BEM",
        }


class AGD_ESS_USH_SYM_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "AGD_ESS_USH_SYM")
        Piezas.AGD_ESS_USH_SYM(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Beam AGD ESS USH SYM_icon.png"),
            "MenuText": "AGD ESS USH SYM",
            "ToolTip": "Beam AGD ESS USH SYM",
        }


class STR_BED_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_BED")
        Piezas.STR_BED(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Beam STR BED_icon.png"),
            "MenuText": "STR BED",
            "ToolTip": "Beam STR_BED",
        }


class STR_BET_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_BET")
        Piezas.STR_BET(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Beam STR BET_icon.png"),
            "MenuText": "STR BET",
            "ToolTip": "Beam STR_BET",
        }


class STR_BXS_ESS_H_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_BXS_ESS_H")
        Piezas.STR_BXS_ESS_H(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Beam STR BXS ESS H_icon.png"),
            "MenuText": "STR BXS ESS H",
            "ToolTip": "Beam STR BXS ESS H",
        }


class STR_BXS_ESS_C_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "STR_BXS_ESS_C")
        Piezas.STR_BXS_ESS_C(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Beam STR BXS ESS C_icon.png"),
            "MenuText": "STR BXS ESS C",
            "ToolTip": "Beam STR BXS ESS C",
        }


#  Conectores
class THR_H_BEM_SFT_1W_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "THR_H_BEM_SFT_1W")
        Piezas.THR_H_BEM_SFT_1W(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Conector THR H BEM SFT 1W_icon.png"),
            "MenuText": "THR H BEM SFT 1W",
            "ToolTip": "Conector THR H BEM SFT 1W",
        }


class THR_H_BEM_SFT_2W_180_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "THR_H_BEM_SFT_2W_180")
        Piezas.THR_H_BEM_SFT_2W_180(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Conector THR H BEM SFT 2W 180_icon.png"),
            "MenuText": "THR H BEM SFT 2W 180º",
            "ToolTip": "Conector THR H BEM SFT 2W 180º",
        }


class THR_H_BEM_SFT_2W_90_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "THR_H_BEM_SFT_2W_90")
        Piezas.THR_H_BEM_SFT_2W_90(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Conector THR H BEM SFT 2W 90_icon.png"),
            "MenuText": "THR H BEM SFT 2W 90º",
            "ToolTip": "Conector THR H BEM SFT 2W 90º",
        }


class THR_H_BEM_SFT_3W_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "THR_H_BEM_SFT_3W")
        Piezas.THR_H_BEM_SFT_3W(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Conector THR H BEM SFT 3W_icon.png"),
            "MenuText": "THR H BEM SFT 3W",
            "ToolTip": "Conector THR H BEM SFT 3W",
        }


class THR_H_BEM_SFT_4W_Icon:
    def Activated(self):
        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "THR_H_BEM_SFT_4W")
        Piezas.THR_H_BEM_SFT_4W(myObj)
        myObj.ViewObject.Proxy = 0  # this is mandatory unless we code the ViewProvider too

        FreeCAD.ActiveDocument.recompute()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Conector THR H BEM SFT 4W_icon.png"),
            "MenuText": "THR H BEM SFT 4W",
            "ToolTip": "Conector THR H BEM SFT 4W",
        }


#  Comandos
class Cmd_Listado_Icon:
    def Activated(self):
        import Comandos

        Comandos.ListadoPiezas()

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "Cmd_Listado_icon.png"),
            "MenuText": "Listado Piezas",
            "ToolTip": "Listado Piezas",
        }


# Brazos
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_ERR", STR_STD_ERR_Icon())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_BRD_AZ", STR_STD_BRD_AZ_Icon())
FreeCADGui.addCommand("STEMFIE_Brace_CRN_ERR_ASYM", CRN_ERR_ASYM_Icon())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_BRM", STR_STD_BRM_Icon())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_BRM_AY", STR_STD_BRM_AY_Icon())
FreeCADGui.addCommand("STEMFIE_Brace_STR_SLT_BE_SYM_ERR", STR_SLT_BE_SYM_ERR_Icon())
FreeCADGui.addCommand("STEMFIE_Brace_STR_SLT_CNT_ERR", STR_SLT_CNT_ERR_Icon())
FreeCADGui.addCommand("STEMFIE_Brace_STR_SLT_FL_ERR", STR_SLT_FL_ERR_Icon())
FreeCADGui.addCommand("STEMFIE_Brace_STR_SLT_SE_ERR", STR_SLT_SE_ERR_Icon())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_BRD_AY", STR_STD_BRD_AY_Icon())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_BRT_AZ", STR_STD_BRT_AZ_Icon())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_BRT_AY", STR_STD_BRT_AY_Icon())
FreeCADGui.addCommand("STEMFIE_Brace_STR_STD_CR", STR_STD_CR_Icon())
# Vigas
FreeCADGui.addCommand("STEMFIE_Beam_STR_ESS", STR_ESS_Icon())
FreeCADGui.addCommand("STEMFIE_Beam_STR_ERR", STR_ERR_Icon())
FreeCADGui.addCommand("STEMFIE_Beam_STR_BEM", STR_BEM_Icon())
FreeCADGui.addCommand("STEMFIE_Beam_AGD_ESS_USH_SYM", AGD_ESS_USH_SYM_Icon())
FreeCADGui.addCommand("STEMFIE_Beam_STR_BED", STR_BED_Icon())
FreeCADGui.addCommand("STEMFIE_Beam_STR_BET", STR_BET_Icon())
FreeCADGui.addCommand("STEMFIE_Beam_STR_BXS_ESS_H", STR_BXS_ESS_H_Icon())
FreeCADGui.addCommand("STEMFIE_Beam_STR_BXS_ESS_C", STR_BXS_ESS_C_Icon())
# Conectores
FreeCADGui.addCommand("STEMFIE_Conector_THR_H_BEM_SFT_1W", THR_H_BEM_SFT_1W_Icon())
FreeCADGui.addCommand("STEMFIE_Conector_THR_H_BEM_SFT_2W_180", THR_H_BEM_SFT_2W_180_Icon())
FreeCADGui.addCommand("STEMFIE_Conector_THR_H_BEM_SFT_2W_90", THR_H_BEM_SFT_2W_90_Icon())
FreeCADGui.addCommand("STEMFIE_Conector_THR_H_BEM_SFT_3W", THR_H_BEM_SFT_3W_Icon())
FreeCADGui.addCommand("STEMFIE_Conector_THR_H_BEM_SFT_4W", THR_H_BEM_SFT_4W_Icon())
# Comandos
FreeCADGui.addCommand("STEMFIE_Cmd_Listado", Cmd_Listado_Icon())


Icon = os.path.join(ICONPATH, "STEMFIE.svg")
