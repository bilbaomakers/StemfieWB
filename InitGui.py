import StemfieWb_locator
import os
global StemfieWBpath
global StemfieWB_icons_path
StemfieWBpath = os.path.dirname(StemfieWb_locator.__file__)
StemfieWB_icons_path = os.path.join( StemfieWBpath, 'Icons')

#global main_StemfieWB_Icon
#main_StemfieWB_Icon = os.path.join( StemfieWB_icons_path , 'Stemfie_-_Logo_48x48.png')

class StemfieWorkbench (Workbench): 
    MenuText = "STEMFIE"
    ToolTip = "Banco trabajo para Stemfie"
    Icon = ( StemfieWB_icons_path + "/Stemfie_-_Logo_48x48.png")

    def Initialize(self):
        import Stemfie                                  # Carga el modulo 'Stemfie.py'

        #  Lista Brazos
        self.ListaBrazos = [
            "Brace_STR_STD_ERR","Brace_STR_STD_BRD_AZ","Brace_CRN_ERR_ASYM","Brace_STR_STD_BRM","Brace_STR_STD_BRM_AY",
            "Brace_STR_SLT_BE_SYM_ERR","Brace_STR_SLT_CNT_ERR","Brace_STR_SLT_FL_ERR","Brace_STR_SLT_SE_ERR",
            "Brace_STR_STD_BRD_AY","Brace_STR_STD_BRT_AZ","Brace_STR_STD_BRT_AY","Brace_STR_STD_CR"
            ]                
        self.appendToolbar("Stemfie Brace",self.ListaBrazos) # crea una barra de herramientas 'Stemfie Brace' con los iconos de los comandos

        #   Lista Vigas
        self.ListaVigas = [
            "Beam_STR_ESS","Beam_STR_ERR","Beam_STR_BEM","Beam_AGD_ESS_USH_SYM","Beam_STR_BED","Beam_STR_BET",
            "Beam_STR_BXS_ESS_H","Beam_STR_BXS_ESS_C"
            ]                  
        self.appendToolbar("Stemfie Beam",self.ListaVigas)   # crea una barra de herramientas 'Stemfie Beam' con los iconos de los comandos
        
        #   Lista Conectores
        self.ListaConectores = [
            "Conector_THR_H_BEM_SFT_1W","Conector_THR_H_BEM_SFT_2W_180","Conector_THR_H_BEM_SFT_2W_90",
            "Conector_THR_H_BEM_SFT_3W","Conector_THR_H_BEM_SFT_4W"
            ]                 
        self.appendToolbar("Stemfie Conector",self.ListaConectores)  # crea una barra de herramientas 'Stemfie Conectores' con los iconos de los comandos

        #   Lista Comandos
        self.ListaComandos = ["Cmd_Listado"]
        self.appendToolbar("Comandos",self.ListaComandos)  # crea una barra de herramientas 'Stemfie Comandos' con los iconos de los comandos


        # Creamos menu 
        self.appendMenu("Stemfie",self.ListaComandos)
        # Creo submenus
        self.appendMenu(["Stemfie","Braces"],self.ListaBrazos)
        self.appendMenu(['Stemfie','Beams'],self.ListaVigas)
        self.appendMenu(['Stemfie','Connectors'],self.ListaConectores)

"""    def ContextMenu(self, recipient):
       
       self.appendContextMenu("Stemfie",self.ListaBrazos)
       
       import FreeCAD, FreeCADGui
        selection = [s  for s in FreeCADGui.Selection.getSelection() if s.Document == FreeCAD.ActiveDocument ]
        if len(selection) == 1:
            obj = selection[0]
            if 'sourceFile' in  obj.Content:
                self.appendContextMenu("Stemfie", self.ListaBrazos )

"""


Gui.addWorkbench(StemfieWorkbench())                # Carga las barras de herramientas que se denominen
