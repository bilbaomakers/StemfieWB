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
    ToolTip = translate("Workbench", "Workbench for Stemfie")
    Icon = os.path.join(ICONPATH, "STEMFIE.svg")

    def Initialize(self):
        from freecad.stemfie import Stemfie

        #  Lista Brazos
        self.ListaBrazos = [
            "STEMFIE_Brace_STR_STD_ERR",
            "STEMFIE_Brace_STR_STD_BRD_AZ",
            "STEMFIE_Brace_CRN_ERR_ASYM",
            "STEMFIE_Brace_STR_STD_BRM_AY",
            "STEMFIE_Brace_STR_SLT_BE_SYM_ERR",
            "STEMFIE_Brace_STR_SLT_CNT_ERR",
            "STEMFIE_Brace_STR_SLT_FL_ERR",
            "STEMFIE_Brace_STR_SLT_SE_ERR",
            "STEMFIE_Brace_STR_STD_BRD_AY",
            "STEMFIE_Brace_STR_STD_BRT_AZ",
            "STEMFIE_Brace_STR_STD_BRT_AY",
            "STEMFIE_Brace_STR_STD_CR",
        ]
        self.appendToolbar(
            QT_TRANSLATE_NOOP("Workbench", "Stemfie Braces"), self.ListaBrazos
        )  # crea una barra de herramientas 'Stemfie Brace' con los iconos de los comandos

        #   Lista Vigas
        self.ListaVigas = [
            "STEMFIE_Beam_STR_ESS",
            "STEMFIE_Beam_STR_ERR",
            "STEMFIE_Beam_STR_BEM",
            "STEMFIE_Beam_AGD_ESS_USH_SYM",
            "STEMFIE_Beam_STR_BED",
            "STEMFIE_Beam_STR_BET",
            "STEMFIE_Beam_STR_BXS_ESS_H",
            "STEMFIE_Beam_STR_BXS_ESS_C",
        ]
        self.appendToolbar(
            QT_TRANSLATE_NOOP("Workbench", "Stemfie Beams"), self.ListaVigas
        )  # crea una barra de herramientas 'Stemfie Beam' con los iconos de los comandos

        # List of plates
        self.list_plates = [
            "STEMFIE_Plate_TRI",
            "STEMFIE_Plate_SQR",
            "STEMFIE_Plate_HEX",
        ]
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Stemfie Plates"), self.list_plates)

        #   Lista Conectores
        self.ListaConectores = [
            "STEMFIE_Connector_THR_H_BEM_SFT_1W",
            "STEMFIE_Connector_THR_H_BEM_SFT_2W_180",
            "STEMFIE_Connector_THR_H_BEM_SFT_2W_90",
            "STEMFIE_Connector_THR_H_BEM_SFT_3W",
            "STEMFIE_Connector_THR_H_BEM_SFT_4W",
        ]
        self.appendToolbar(
            QT_TRANSLATE_NOOP("Workbench", "Stemfie Conectors"), self.ListaConectores
        )  # crea una barra de herramientas 'Stemfie Conectores' con los iconos de los comandos

        #   Lista Comandos
        self.ListaComandos = ["STEMFIE_Cmd_Listado"]
        self.appendToolbar(
            QT_TRANSLATE_NOOP("Workbench", "Stemfie Tools"), self.ListaComandos
        )  # crea una barra de herramientas 'Stemfie Comandos' con los iconos de los comandos

        # Creamos menu
        self.appendMenu("Stemfie", self.ListaComandos)
        # Creo submenus
        self.appendMenu(["Stemfie", QT_TRANSLATE_NOOP("Workbench", "Braces")], self.ListaBrazos)
        self.appendMenu(["Stemfie", QT_TRANSLATE_NOOP("Workbench", "Beams")], self.ListaVigas)
        self.appendMenu(
            ["Stemfie", QT_TRANSLATE_NOOP("Workbench", "Connectors")], self.ListaConectores
        )

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
    #    self.appendContextMenu("Stemfie",self.ListaBrazos)
    #
    #    import FreeCAD, FreeCADGui
    #     selection = [s  for s in FreeCADGui.Selection.getSelection() if s.Document == FreeCAD.ActiveDocument ]
    #     if len(selection) == 1:
    #         obj = selection[0]
    #         if 'sourceFile' in  obj.Content:
    #             self.appendContextMenu("Stemfie", self.ListaBrazos )


Gui.addWorkbench(StemfieWorkbench())  # Carga las barras de herramientas que se denominen
