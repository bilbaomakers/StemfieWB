import os

import FreeCAD
import FreeCADGui as Gui
from FreeCADGui import Workbench
from freecad.stemfie import ICONPATH, TRANSLATIONSPATH

translate = FreeCAD.Qt.translate
QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP

# Add translations path
Gui.addLanguagePath(TRANSLATIONSPATH)
Gui.updateLocale()


class StemfieWorkbench(Workbench):
    MenuText = "STEMFIE"
    ToolTip = translate("Workbench", "Workbench for STEMFIE")
    Icon = os.path.join(ICONPATH, "STEMFIE.svg")

    def Initialize(self):
        from freecad.stemfie import Stemfie

        Gui.addIconPath(ICONPATH)

        self.list_beams = [
            "STEMFIE_Beam_STR_ESS",
            "STEMFIE_Beam_STR_ERR",
            "STEMFIE_Beam_STR_BEM",
            "STEMFIE_Beam_AGD_ESS_USH_SYM",
            "STEMFIE_Beam_STR_DBL",
            "STEMFIE_Beam_STR_TRPL",
            "STEMFIE_Beam_STR_BXS_ESS_H",
            "STEMFIE_Beam_STR_BXS_ESS_C",
        ]
        self.list_braces = [
            "STEMFIE_Brace_STR_STD_ERR",
            "STEMFIE_Brace_CRN_ERR_ASYM",
            "STEMFIE_Brace_STR_STD_SQR_AY",
            "STEMFIE_Brace_STR_SLT_BE_SYM_ERR",
            "STEMFIE_Brace_STR_SLT_CNT_ERR",
            "STEMFIE_Brace_STR_SLT_FL_ERR",
            "STEMFIE_Brace_STR_SLT_SE_ERR",
            "STEMFIE_Brace_STR_STD_DBL_AZ",
            "STEMFIE_Brace_STR_STD_DBL_AY",
            "STEMFIE_Brace_STR_STD_TRPL_AZ",
            "STEMFIE_Brace_STR_STD_TRPL_AY",
            "STEMFIE_Brace_STR_STD_CRS",
        ]
        self.list_connectors = [
            "STEMFIE_Connector_TRH_H_BEM_SFT_1W",
            "STEMFIE_Connector_TRH_H_BEM_SFT_2W_90",
            "STEMFIE_Connector_TRH_H_BEM_SFT_2W_180",
            "STEMFIE_Connector_TRH_H_BEM_SFT_3W",
            "STEMFIE_Connector_TRH_H_BEM_SFT_4W",
        ]
        self.list_fasteners = []
        self.list_plates = [
            "STEMFIE_Plate_TRI",
            "STEMFIE_Plate_SQR",
            "STEMFIE_Plate_HEX",
        ]
        self.list_shafts = ["STEMFIE_Shaft_SFT_PLN"]
        self.list_springs = []
        self.list_commands = ["STEMFIE_PartsList"]

        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "STEMFIE Beams"), self.list_beams)
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "STEMFIE Braces"), self.list_braces)
        self.appendToolbar(
            QT_TRANSLATE_NOOP("Workbench", "STEMFIE Connectors"), self.list_connectors
        )
        # self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "STEMFIE Fasteners"), self.list_fasteners)
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "STEMFIE Plates"), self.list_plates)
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "STEMFIE Shafts"), self.list_shafts)
        # self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "STEMFIE Springs"), self.list_springs)
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "STEMFIE Utilities"), self.list_commands)

        # Creamos menu
        self.appendMenu("STEMFIE", self.list_commands)
        # Creo submenus
        self.appendMenu(["STEMFIE", QT_TRANSLATE_NOOP("Workbench", "Beams")], self.list_beams)
        self.appendMenu(["STEMFIE", QT_TRANSLATE_NOOP("Workbench", "Braces")], self.list_braces)
        self.appendMenu(
            ["STEMFIE", QT_TRANSLATE_NOOP("Workbench", "Connectors")],
            self.list_connectors,
        )
        # self.appendMenu(
        #     ["STEMFIE", QT_TRANSLATE_NOOP("Workbench", "Fasteners")], self.list_fasteners
        # )
        self.appendMenu(["STEMFIE", QT_TRANSLATE_NOOP("Workbench", "Plates")], self.list_plates)
        self.appendMenu(["STEMFIE", QT_TRANSLATE_NOOP("Workbench", "Shafts")], self.list_shafts)
        # self.appendMenu(["STEMFIE", QT_TRANSLATE_NOOP("Workbench", "Springs")], self.list_springs)

    def Activated(self):
        """
        Code which should be computed when a user switch to this workbench.
        """
        # FreeCAD.Console.PrintMessage("Hola\n")
        pass

    def Deactivated(self):
        """
        Code which should be computed when this workbench is deactivated.
        """
        # FreeCAD.Console.PrintMessage("Adiós\n")
        pass

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    # def ContextMenu(self, recipient):
    #     """
    #     This is executed whenever the user right-clicks on screen
    #     "recipient" will be either "view" or "tree".
    #     """
    #
    #    self.appendContextMenu("STEMFIE",self.ListaBrazos)
    #
    #    import FreeCAD, FreeCADGui
    #     selection = [s  for s in FreeCADGui.Selection.getSelection() if s.Document == FreeCAD.ActiveDocument ]
    #     if len(selection) == 1:
    #         obj = selection[0]
    #         if 'sourceFile' in  obj.Content:
    #             self.appendContextMenu("STEMFIE", self.ListaBrazos )


Gui.addWorkbench(StemfieWorkbench())  # Carga las barras de herramientas que se denominen
