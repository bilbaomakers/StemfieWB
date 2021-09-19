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

# Brazos
class STR_STD_ERR:
    ''' Brace - Straight - Ending Round Round
       
        ________________
       /                 \_
      |   ()    ()    ()  |
       \ _______________ /
    
           1     2     3
            ---------> 
             N_Agujeros

        Variables:
            Codigo          'Demoninacion'
            N_Agujeros      'Numero Agujeros que contiene la pieza
    
    '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros","Valores Pieza","Nº Agujeros Pieza Simple\nMínimo = 1").N_Agujeros = 3
        

    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo que N_Agujeros mayor de 1
        if (obj.N_Agujeros < 1):
            obj.N_Agujeros = 1
        # En caso de 1 agujero seria una arandela y no tendria rectas
        elif (obj.N_Agujeros == 1):
            P = Part.makeCylinder(6.25, 3.5, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector(0, 0, -1), FreeCAD.Vector(0, 0, 1))
            P = P.cut (Agujero) 
        else:
            # Numero de agujeros mayor de 1
            #  ---- Genero puntos de los contornos
            P1 = FreeCAD.Vector(0,-6.25,0)
            P2 = FreeCAD.Vector((obj.N_Agujeros-1)*12.5,-6.25,0)
            P3 = FreeCAD.Vector((obj.N_Agujeros-1)*12.5,6.25,0)
            P4 = FreeCAD.Vector(0,6.25,0)
            #  ---- Genero puntos para circulos
            PC2 = FreeCAD.Vector(((obj.N_Agujeros-1)*12.5)+6.25,0,0)
            PC4 = FreeCAD.Vector(-6.25,0,0)
            #  ---- Creamos lineas y arcos
            L1 = Part.LineSegment(P1,P2) 
            C2 = Part.Arc(P2,PC2,P3)   
            L3 = Part.LineSegment(P3,P4)
            C4 = Part.Arc(P4,PC4,P1)
            #  ---- Creo el contorno
            S = Part.Shape([L1,C2,L3,C4])
            W = Part.Wire(S.Edges)
            #  ---- Creo la cara con el contorno
            F = Part.Face(W)
            #  ---- Le doy Volumen a la cara
            P = F.extrude (FreeCAD.Vector(0,0,3.125))
            #  ---- Bucle para agujeros
            for x in range(obj.N_Agujeros):
                Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( x*12.5, 0, -1), FreeCAD.Vector(0, 0, 1))
                if x == 0 : 
                    Agujeros = Agujero
                else:
                    Agujeros = Agujeros.fuse(Agujero)
            P = P.cut (Agujeros)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR STD ERR-BU" + str(obj.N_Agujeros) + "x01x00.25"

        P.Placement = obj.Placement
        obj.Shape = P

class STR_STD_BRD_AZ:
    ''' Brazo Angular Stemfie '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Piezas")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros_X","Valores Pieza","Número Agujeros en X\nMínimo = 2").N_Agujeros_X = 3
        obj.addProperty("App::PropertyInteger","N_Agujeros_Y","Valores Pieza","Número Agujeros en Y\nMínimo = 2").N_Agujeros_Y = 2
        obj.addProperty("App::PropertyAngle","Angulo","Valores Pieza","Ángulo\nMínimo = 60\nMáximo = 180").Angulo = 60

    def execute(self,obj):
        import Part,FreeCAD,FreeCADGui

        # Compruebo que Numero_Agujeros mayor de 2 y Angulo en 60 y 180
        if (obj.N_Agujeros_X < 2) or (obj.N_Agujeros_Y < 2) or (obj.Angulo < 60) or (obj.Angulo > 180):
            if (obj.N_Agujeros_X < 2) : obj.N_Agujeros_X = 2
            if (obj.N_Agujeros_Y < 2) : obj.N_Agujeros_Y = 2
            if (obj.Angulo < 60) : obj.Angulo = 60
            if (obj.Angulo > 180) : obj.Angulo = 180
        
        # Genero Pieza en X
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((obj.N_Agujeros_X-1)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((obj.N_Agujeros_X-1)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros_X-1)*12.5)+6.25,0,0)
        PC4 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        C4 = Part.Arc(P4,PC4,P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1,C2,L3,C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PX = F.extrude (FreeCAD.Vector(0,0,3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros_X):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( x*12.5, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x == 0 : 
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PX = PX.cut (Agujeros)
        # Genero Pieza en Y
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((obj.N_Agujeros_Y-1)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((obj.N_Agujeros_Y-1)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros_Y-1)*12.5)+6.25,0,0)
        PC4 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        C4 = Part.Arc(P4,PC4,P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1,C2,L3,C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PY = F.extrude (FreeCAD.Vector(0,0,3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros_Y):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector(x*12.5, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x == 0 : 
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PY = PY.cut (Agujeros)
        #  ---- Roto el brado inclinado
        PY.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),obj.Angulo)
        #  ---- Uno las piezas
        P = PX.fuse (PY)
        #  ---- Refino la pieza
        P = P.removeSplitter()

        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR STD BRD AZ-BU" + str(obj.N_Agujeros_X) + "x" + str(obj.N_Agujeros_Y) + " " + str(obj.Angulo)
        
        P.Placement = obj.Placement
        obj.Shape = P
        
class CRN_ERR_ASYM:
    ''' Brazo Angulo 90º Stemfie '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros_X","Valores Pieza","Número Agujeros en X\nMínimo = 2").N_Agujeros_X=3
        obj.addProperty("App::PropertyInteger","N_Agujeros_Y","Valores Pieza","Número Agujeros en Y\nMínimo = 2").N_Agujeros_Y=2

    def execute(self,obj):
        import Part,FreeCAD,FreeCADGui

        # Compruebo que Numero_Agujeros mayor de 2
        if (obj.N_Agujeros_X < 2) or (obj.N_Agujeros_Y < 2):
            if (obj.N_Agujeros_X < 2) : obj.N_Agujeros_X = 2
            if (obj.N_Agujeros_Y < 2) : obj.N_Agujeros_Y = 2
        
        # Genero Pieza en X
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((obj.N_Agujeros_X-1)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((obj.N_Agujeros_X-1)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros_X-1)*12.5)+6.25,0,0)
        PC4 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        C4 = Part.Arc(P4,PC4,P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1,C2,L3,C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PX = F.extrude (FreeCAD.Vector(0,0,3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros_X):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( x*12.5, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x == 0 : 
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PX = PX.cut (Agujeros)
        # Genero Pieza en Y
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((obj.N_Agujeros_Y-1)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((obj.N_Agujeros_Y-1)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros_Y-1)*12.5)+6.25,0,0)
        PC4 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        C4 = Part.Arc(P4,PC4,P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1,C2,L3,C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PY = F.extrude (FreeCAD.Vector(0,0,3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros_Y):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( x*12.5, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x == 0 : 
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        PY = PY.cut (Agujeros)
        #  ---- Giramos la pieza
        PY.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),90)
        #  ---- Unimos las piezas
        P = PX.fuse (PY)
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "CRN ERR ASYM-BU" + str(obj.N_Agujeros_X) + "x" + str(obj.N_Agujeros_Y) + "x0.25"

        P.Placement = obj.Placement
        obj.Shape = P
        
class STR_STD_BRM:
    ''' Plancha Cuadrada Stemfie '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros_X","Valores Pieza","Número Agujeros en X\nMínimo = 2").N_Agujeros_X=4
        obj.addProperty("App::PropertyInteger","N_Agujeros_Y","Valores Pieza","Número Agujeros en Y\nMínimo = 2").N_Agujeros_Y=3

    def execute(self,obj):
        import Part,FreeCAD
        import math

        # Compruebo que Numero_Agujeros mayor de 1
        if (obj.N_Agujeros_X < 2) or (obj.N_Agujeros_Y < 2):
            if (obj.N_Agujeros_X < 2) : obj.N_Agujeros_X = 2
            if (obj.N_Agujeros_Y < 2) : obj.N_Agujeros_Y = 2
        else:
            # Numero de agujeros mayor de 2
            #  ---- Genero puntos de los contornos
            Pto1 = FreeCAD.Vector(0,-6.25,0)
            Pto2 = FreeCAD.Vector((obj.N_Agujeros_X-1)*12.5,-6.25,0)

            Pto3 = FreeCAD.Vector(((obj.N_Agujeros_X-1)*12.5)+6.25,0,0)
            Pto4 = FreeCAD.Vector(((obj.N_Agujeros_X-1)*12.5)+6.25,(obj.N_Agujeros_Y-1)*12.5,0)

            Pto5 = FreeCAD.Vector((obj.N_Agujeros_X-1)*12.5,((obj.N_Agujeros_Y-1)*12.5)+6.25,0)
            Pto6 = FreeCAD.Vector(0,((obj.N_Agujeros_Y-1)*12.5)+6.25,0)

            Pto7 = FreeCAD.Vector(-6.25,((obj.N_Agujeros_Y-1)*12.5),0)
            Pto8 = FreeCAD.Vector(-6.25,0,0)
            #  ---- Genero puntos para circulos
            PtoC1 = FreeCAD.Vector(((obj.N_Agujeros_X-1)*12.5)+(math.sin(0.7854)*6.25),math.sin(0.7854)*-6.25,0)
            PtoC2 = FreeCAD.Vector(((obj.N_Agujeros_X-1)*12.5)+(math.sin(0.7854)*6.25),((obj.N_Agujeros_Y-1)*12.5)+(math.sin(0.7854)*6.25),0)
            PtoC3 = FreeCAD.Vector((math.sin(0.7854)*6.25)*-1,((obj.N_Agujeros_Y-1)*12.5)+(math.sin(0.7854)*6.25),0)
            PtoC4 = FreeCAD.Vector((math.sin(0.7854)*6.25)*-1,(math.sin(0.7854)*6.25)*-1,0) 
            #  ---- Creamos lineas y arcos
            L1 = Part.LineSegment(Pto1,Pto2) 
            C1 = Part.Arc(Pto2,PtoC1,Pto3)   
            L2 = Part.LineSegment(Pto3,Pto4)
            C2 = Part.Arc(Pto4,PtoC2,Pto5)
            L3 = Part.LineSegment(Pto5,Pto6)
            C3 = Part.Arc(Pto6,PtoC3,Pto7)
            L4 = Part.LineSegment(Pto7,Pto8)
            C4 = Part.Arc(Pto8,PtoC4,Pto1)
            #  ---- Creo el contorno
            #W = Part.Wire([L1,C2,L3,C4])

            S = Part.Shape([L1,C1,L2,C2,L3,C3,L4,C4])
            W = Part.Wire(S.Edges)
            
            #  ---- Creo la cara con el contorno
            F = Part.Face(W)
            #  ---- Le doy Volumen a la cara
            P = F.extrude (FreeCAD.Vector(0,0,3.125))
            #  ---- Bucle para agujeros
            for x in range(obj.N_Agujeros_X):
                for y in range(obj.N_Agujeros_Y):
                    Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( x*12.5, y*12.5, -1), FreeCAD.Vector(0, 0, 1))
                    if (x == 0) and (y == 0):
                        Agujeros = Agujero
                    else:
                        Agujeros = Agujeros.fuse(Agujero)
            P = P.cut (Agujeros)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR STD BRM-" + str(obj.N_Agujeros_X) + "x" + str(obj.N_Agujeros_Y)
        
        P.Placement = obj.Placement
        obj.Shape = P

class STR_STD_BRM_AY:
    ''' Plancha Cuadrada Stemfie con angulo en Y'''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros_X","Valores Pieza","Número Agujeros en X\nMínimo = 2").N_Agujeros_X=4
        obj.addProperty("App::PropertyInteger","N_Agujeros_Y","Valores Pieza","Número Agujeros en Y\nMínimo = 2").N_Agujeros_Y=3
        obj.addProperty("App::PropertyInteger","N_Agujeros_Inclinado","Valores Pieza","Nº Agujeros en parte inclinada\nMínimo 1").N_Agujeros_Inclinado = 2
        obj.addProperty("App::PropertyAngle","Angulo","Valores Pieza","Ángulo\nMínimo = 0\nMáximo = 180").Angulo = 135
 
    def execute(self,obj):
        import Part,FreeCAD
        import math

        # Compruebo que Numero_Agujeros mayor de 1
        if (obj.N_Agujeros_X < 2) or (obj.N_Agujeros_Y < 2) or (obj.N_Agujeros_Inclinado < 1) or (obj.Angulo < 0) or (obj.Angulo > 180):
            if (obj.N_Agujeros_X < 2) : obj.N_Agujeros_X = 2
            if (obj.N_Agujeros_Y < 2) : obj.N_Agujeros_Y = 2
            if (obj.N_Agujeros_Inclinado < 1) : obj.N_Agujeros_Inclinado = 1
            if (obj.Angulo < 0) : obj.Angulo = 0
            if (obj.Angulo > 180) : obj.Angulo = 180
        # ----------------------------
        #  ---- Genero Cuerpo Horizontal
        Pto1 = FreeCAD.Vector(-6.25,-6.25,0)
        Pto2 = FreeCAD.Vector((obj.N_Agujeros_X-1)*12.5,-6.25,0)

        Pto3 = FreeCAD.Vector(((obj.N_Agujeros_X-1)*12.5)+6.25,0,0)
        Pto4 = FreeCAD.Vector(((obj.N_Agujeros_X-1)*12.5)+6.25,(obj.N_Agujeros_Y-1)*12.5,0)

        Pto5 = FreeCAD.Vector((obj.N_Agujeros_X-1)*12.5,((obj.N_Agujeros_Y-1)*12.5)+6.25,0)
        Pto6 = FreeCAD.Vector(-6.25,((obj.N_Agujeros_Y-1)*12.5)+6.25,0)

        #Pto7 = FreeCAD.Vector(-6.25,((obj.N_Agujeros_Y-1)*12.5),0)
        #Pto8 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Genero puntos para circulos
        PtoC1 = FreeCAD.Vector(((obj.N_Agujeros_X-1)*12.5)+(math.sin(0.7854)*6.25),math.sin(0.7854)*-6.25,0)
        PtoC2 = FreeCAD.Vector(((obj.N_Agujeros_X-1)*12.5)+(math.sin(0.7854)*6.25),((obj.N_Agujeros_Y-1)*12.5)+(math.sin(0.7854)*6.25),0)
        #PtoC3 = FreeCAD.Vector((math.sin(0.7854)*6.25)*-1,((obj.N_Agujeros_Y-1)*12.5)+(math.sin(0.7854)*6.25),0)
        #PtoC4 = FreeCAD.Vector((math.sin(0.7854)*6.25)*-1,(math.sin(0.7854)*6.25)*-1,0) 
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(Pto1,Pto2) 
        C1 = Part.Arc(Pto2,PtoC1,Pto3)  
        L2 = Part.LineSegment(Pto3,Pto4)
        C2 = Part.Arc(Pto4,PtoC2,Pto5)
        L3 = Part.LineSegment(Pto5,Pto6)
        #C3 = Part.Arc(Pto6,PtoC3,Pto7)
        L4 = Part.LineSegment(Pto6,Pto1)
        #C4 = Part.Arc(Pto8,PtoC4,Pto1)
        #  ---- Creo el contorno
        S = Part.Shape([L1,C1,L2,C2,L3,L4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude (FreeCAD.Vector(0,0,-3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros_X):
            for y in range(obj.N_Agujeros_Y):
                Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( x*12.5, y*12.5, -5), FreeCAD.Vector(0, 0, 1))
                if (x == 0) and (y == 0):
                    Agujeros = Agujero
                else:
                    Agujeros = Agujeros.fuse(Agujero)
        P = P.cut (Agujeros)

        # Condicional para angulo 180 no generar cilindros
        if obj.Angulo != 180 :
            # Tengo que meter un cuarto de cilindro y unirlo a P
            # Añado condicional para que sea en funcion del angulo
            Ang = (180 - int(obj.Angulo)) / 2
            Curva = Part.makeCylinder(3.125, obj.N_Agujeros_Y*12.5, FreeCAD.Vector(6.25, -6.25, 0), FreeCAD.Vector(0, 1, 0),Ang)
            Curva.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),180)
            P = P.fuse (Curva)


        #  ---- Genero Cuerpo Inclinado
        #  ---- Genero puntos de los contornos
        Pto1 = FreeCAD.Vector(-6.25,-6.25,0)
        Pto2 = FreeCAD.Vector((obj.N_Agujeros_Inclinado-1)*12.5,-6.25,0)

        Pto3 = FreeCAD.Vector(((obj.N_Agujeros_Inclinado-1)*12.5)+6.25,0,0)
        Pto4 = FreeCAD.Vector(((obj.N_Agujeros_Inclinado-1)*12.5)+6.25,(obj.N_Agujeros_Y-1)*12.5,0)

        Pto5 = FreeCAD.Vector((obj.N_Agujeros_Inclinado-1)*12.5,((obj.N_Agujeros_Y-1)*12.5)+6.25,0)
        Pto6 = FreeCAD.Vector(-6.25,((obj.N_Agujeros_Y-1)*12.5)+6.25,0)

        #Pto7 = FreeCAD.Vector(-6.25,((obj.N_Agujeros_Y-1)*12.5),0)
        #Pto8 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Genero puntos para circulos
        PtoC1 = FreeCAD.Vector(((obj.N_Agujeros_Inclinado-1)*12.5)+(math.sin(0.7854)*6.25),math.sin(0.7854)*-6.25,0)
        PtoC2 = FreeCAD.Vector(((obj.N_Agujeros_Inclinado-1)*12.5)+(math.sin(0.7854)*6.25),((obj.N_Agujeros_Y-1)*12.5)+(math.sin(0.7854)*6.25),0)
        #PtoC3 = FreeCAD.Vector((math.sin(0.7854)*6.25)*-1,((obj.N_Agujeros_Y-1)*12.5)+(math.sin(0.7854)*6.25),0)
        #PtoC4 = FreeCAD.Vector((math.sin(0.7854)*6.25)*-1,(math.sin(0.7854)*6.25)*-1,0) 
        #  ---- Creamos lineas y arcos
        LInc1 = Part.LineSegment(Pto1,Pto2) 
        CInc1 = Part.Arc(Pto2,PtoC1,Pto3)   
        LInc2 = Part.LineSegment(Pto3,Pto4)
        CInc2 = Part.Arc(Pto4,PtoC2,Pto5)
        LInc3 = Part.LineSegment(Pto5,Pto6)
        #CInc3 = Part.Arc(Pto6,PtoC3,Pto7)
        LInc4 = Part.LineSegment(Pto6,Pto1)
        #CInc4 = Part.Arc(Pto8,PtoC4,Pto1)
        #  ---- Creo el contorno
        SInc = Part.Shape([LInc1,CInc1,LInc2,CInc2,LInc3,LInc4])
        WInc = Part.Wire(SInc.Edges)
            
        #  ---- Creo la cara con el contorno
        FInc = Part.Face(WInc)
        #  ---- Le doy Volumen a la cara
        PInc = FInc.extrude (FreeCAD.Vector(0,0,3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros_Inclinado):
            for y in range(obj.N_Agujeros_Y):
                Agujero = Part.makeCylinder(3.5, 10, FreeCAD.Vector( x*12.5, y*12.5, -5), FreeCAD.Vector(0, 0, 1))
                if (x == 0) and (y == 0):
                    Agujeros = Agujero
                else:
                    Agujeros = Agujeros.fuse(Agujero)
        PInc = PInc.cut (Agujeros)
        # Condicional para angulo 180 no generar cilindros
        if obj.Angulo != 180 :
            Curva = Part.makeCylinder(3.125, obj.N_Agujeros_Y*12.5, FreeCAD.Vector(-6.25,-6.25,0), FreeCAD.Vector(0, 1, 0),Ang)
            Curva.rotate(FreeCAD.Vector(-6.25,-6.25,0),FreeCAD.Vector(0,1,0),-Ang)
            PInc = PInc.fuse (Curva)
        # Giro en Y
        PInc.rotate(FreeCAD.Vector(-6.25,0,0),FreeCAD.Vector(0,1,0),obj.Angulo*-1)
        # Junto los dos cuerpos 
        P = P.fuse(PInc)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        



        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR STD BRM AY-" + str(obj.N_Agujeros_X) + "x" + str(obj.N_Agujeros_Y)

        
        P.Placement = obj.Placement
        obj.Shape = P

class STR_SLT_BE_SYM_ERR:
    ''' Brazo Stemfie con agujeros rasgados en extremos y simples en el centro '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros_T","Valores Pieza","Número Agujeros Total\nMínimo 5").N_Agujeros_T = 5
        obj.addProperty("App::PropertyInteger","N_Agujeros_R","Valores Pieza","Número Agujeros Rasgados\nIgual en ambos lados\nMínimo 2").N_Agujeros_R = 2

    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo que N_Agujeros_T y N_Agujeros_R
        if (obj.N_Agujeros_T < 5) or (obj.N_Agujeros_R < 2):    # Si alguno es menor no modificar pieza
            if (obj.N_Agujeros_T < 5) :                         # si Numero Total de Agujeros es menor 5 
                obj.N_Agujeros_T = 5                            # dejarlo en 5
            else:                                               # si no
                obj.N_Agujeros_R = 2                            # dejar Numero Agujeros del coliso en 2

        if (obj.N_Agujeros_R*2)+1 > (obj.N_Agujeros_T):
            obj.N_Agujeros_T = (obj.N_Agujeros_R*2)+1
        # ----------------------------
        #  ---- Genero Cuerpo exterior
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((obj.N_Agujeros_T-1)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((obj.N_Agujeros_T-1)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros_T-1)*12.5)+6.25,0,0)
        PC4 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        C4 = Part.Arc(P4,PC4,P1)
        S = Part.Shape([L1,C2,L3,C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude (FreeCAD.Vector(0,0,3.125))
        #  -----------------------------
        #  ---- Genero Cuerpos a restar 
        #  -----------------------------
        #  ---- Genero Cuerpos a restar de los dos extremos
        for x in range (2):
            if x == 0 :
                Desp = 0
            else:
                Desp = (((obj.N_Agujeros_T-(obj.N_Agujeros_R*2)) + obj.N_Agujeros_R))*12.5

            Pto01 = FreeCAD.Vector(0+Desp,-3.5,0)
            Pto02 = FreeCAD.Vector(((obj.N_Agujeros_R-1)*12.5)+Desp,-3.5,0)
            Pto03 = FreeCAD.Vector(((obj.N_Agujeros_R-1)*12.5)+Desp,3.5,0)
            Pto04 = FreeCAD.Vector(0+Desp,3.5,0)
            #  ---- Genero puntos para circulos
            PtoC2 = FreeCAD.Vector((((obj.N_Agujeros_R-1)*12.5)+3.5)+Desp,0,0)
            PtoC4 = FreeCAD.Vector(-3.5+Desp,0,0)
            #  ---- Creamos lineas y arcos
            LRest1 = Part.LineSegment(Pto01,Pto02) 
            CRest2 = Part.Arc(Pto02,PtoC2,Pto03)   
            LRest3 = Part.LineSegment(Pto03,Pto04)
            CRest4 = Part.Arc(Pto04,PtoC4,Pto01)
            SRest = Part.Shape([LRest1,CRest2,LRest3,CRest4])
            WRest = Part.Wire(SRest.Edges)
            #  ---- Creo la cara con el contorno
            FRest = Part.Face(WRest)
            PRest = FRest.extrude (FreeCAD.Vector(0,0,5))
            P = P.cut (PRest)

        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros_T-(obj.N_Agujeros_R*2)):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector((obj.N_Agujeros_R + x)*12.5, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x == 0 : 
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut (Agujeros)

        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR_SLT_BE_SYM_ERR-BU" + str(obj.N_Agujeros_T) + "x01x00.25x" + str(obj.N_Agujeros_R)

        P.Placement = obj.Placement
        obj.Shape = P

class STR_SLT_CNT_ERR:
    ''' Brazo Stemfie con agujeros rasgados en centro y simples en extremos '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros_T","Valores Pieza","Número Agujeros Total\nMínimo 4").N_Agujeros_T = 4
        obj.addProperty("App::PropertyInteger","N_Agujeros_R","Valores Pieza","Número Agujeros Rasgados\nMínimo 2").N_Agujeros_R = 2

    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo que N_Agujeros_T y N_Agujeros_R
        if (obj.N_Agujeros_T < 4) or (obj.N_Agujeros_R < 2): # Si alguno es menor no modificar pieza
            if (obj.N_Agujeros_T < 4) :                 # si Numero Total de Agujeros es menor 4
                obj.N_Agujeros_T = 4                    # dejarlo en 4
            else:                                       # si no
                obj.N_Agujeros_R = 2                    # dejar Numero Agujeros del coliso en 2
            #return
        # Ahora compuebo que la longitud total no sea menor de lo necesario
        if (obj.N_Agujeros_R+2 > obj.N_Agujeros_T) : obj.N_Agujeros_T = obj.N_Agujeros_R+2

        if ((obj.N_Agujeros_T-obj.N_Agujeros_R)%2) != 0 :
            obj.N_Agujeros_T = (obj.N_Agujeros_T)+1
        # ----------------------------
        #  ---- Genero Cuerpo exterior
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((obj.N_Agujeros_T-1)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((obj.N_Agujeros_T-1)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros_T-1)*12.5)+6.25,0,0)
        PC4 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        C4 = Part.Arc(P4,PC4,P1)
        S = Part.Shape([L1,C2,L3,C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude (FreeCAD.Vector(0,0,3.125))
        #  -----------------------------
        #  ---- Genero Cuerpos a restar 
        #  -----------------------------
        #  ---- Genero cilindros a restar de los dos extremos
        for x in range (2):
            if x == 0 :
                Desp = 0
            else:
                Desp = ( ( (obj.N_Agujeros_T - obj.N_Agujeros_R) / 2 ) + obj.N_Agujeros_R )*12.5
            #  ----  agujeros
            for y in range ( int( ( obj.N_Agujeros_T - obj.N_Agujeros_R ) / 2 ) ) :
                Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector((y*12.5)+Desp, 0, -1), FreeCAD.Vector(0, 0, 1))
                if y == 0 : 
                    Agujeros = Agujero
                else:
                    Agujeros = Agujeros.fuse(Agujero)
            P = P.cut (Agujeros)

        # Genero la forma central
        Desp = ((obj.N_Agujeros_T-obj.N_Agujeros_R)/2)*12.5       

        Pto01 = FreeCAD.Vector(0+Desp,-3.5,-1)
        Pto02 = FreeCAD.Vector(((obj.N_Agujeros_R-1)*12.5)+Desp,-3.5,-1)
        Pto03 = FreeCAD.Vector(((obj.N_Agujeros_R-1)*12.5)+Desp,3.5,-1)
        Pto04 = FreeCAD.Vector(0+Desp,3.5,-1)
        #  ---- Genero puntos para circulos
        PtoC2 = FreeCAD.Vector((((obj.N_Agujeros_R-1)*12.5)+3.5)+Desp,0,-1)
        PtoC4 = FreeCAD.Vector(-3.5+Desp,0,-1)
        #  ---- Creamos lineas y arcos
        LRest1 = Part.LineSegment(Pto01,Pto02) 
        CRest2 = Part.Arc(Pto02,PtoC2,Pto03)   
        LRest3 = Part.LineSegment(Pto03,Pto04)
        CRest4 = Part.Arc(Pto04,PtoC4,Pto01)
        SRest = Part.Shape([LRest1,CRest2,LRest3,CRest4])
        WRest = Part.Wire(SRest.Edges)
        #  ---- Creo la cara con el contorno
        FRest = Part.Face(WRest)
        PRest = FRest.extrude (FreeCAD.Vector(0,0,5))   # Extruyo 5
        P = P.cut (PRest)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR_SLT_CNT_ERR-BU" + str(obj.N_Agujeros_T) + "x01x00.25x" + str(obj.N_Agujeros_R)

        P.Placement = obj.Placement
        obj.Shape = P

class STR_SLT_FL_ERR:
    ''' Brazo Stemfie rasgado en toda su extension '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros","Valores Pieza","Número Agujeros\nMínimo 2").N_Agujeros = 4      

    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo que Numero_Agujeros
        if (obj.N_Agujeros < 2):obj.N_Agujeros = 2  # Si es menor dejar Numero Agujeros en 2
         
        # ----------------------------
        #  ---- Genero Cuerpo exterior
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((obj.N_Agujeros-1)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((obj.N_Agujeros-1)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros-1)*12.5)+6.25,0,0)
        PC4 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        C4 = Part.Arc(P4,PC4,P1)
        S = Part.Shape([L1,C2,L3,C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude (FreeCAD.Vector(0,0,3.125))
        
        #  ---- Genero el Cuerpo Interior a restar 
        #  -----------------------------
        Pto01 = FreeCAD.Vector(0,-3.5,-1)
        Pto02 = FreeCAD.Vector(((obj.N_Agujeros-1)*12.5),-3.5,-1)
        Pto03 = FreeCAD.Vector(((obj.N_Agujeros-1)*12.5),3.5,-1)
        Pto04 = FreeCAD.Vector(0,3.5,-1)
        #  ---- Genero puntos para circulos
        PtoC2 = FreeCAD.Vector((((obj.N_Agujeros-1)*12.5)+3.5),0,-1)
        PtoC4 = FreeCAD.Vector(-3.5,0,-1)
        #  ---- Creamos lineas y arcos
        LRest1 = Part.LineSegment(Pto01,Pto02) 
        CRest2 = Part.Arc(Pto02,PtoC2,Pto03)   
        LRest3 = Part.LineSegment(Pto03,Pto04)
        CRest4 = Part.Arc(Pto04,PtoC4,Pto01)
        SRest = Part.Shape([LRest1,CRest2,LRest3,CRest4])
        WRest = Part.Wire(SRest.Edges)
        #  ---- Creo la cara con el contorno
        FRest = Part.Face(WRest)
        PRest = FRest.extrude (FreeCAD.Vector(0,0,5))   # Extruyo 5
        P = P.cut (PRest)                               # Resto
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR_SLT_FL_ERR-" + str(obj.N_Agujeros)

        P.Placement = obj.Placement
        obj.Shape = P

class STR_SLT_SE_ERR:
    ''' Brazo Stemfie agujeros en un extremo y rasgado en el otro '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros","Valores Pieza","Nº Agujeros Sueltos\nMínimo 1").N_Agujeros = 1
        obj.addProperty("App::PropertyInteger","N_Agujeros_R","Valores Pieza","Nº Agujeros Rasgados\nIgual en ambos lados\nMínimo 2").N_Agujeros_R = 2
        
    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo que N_Agujeros y Numero_Agujeros_R
        if (obj.N_Agujeros < 1) or (obj.N_Agujeros_R < 2): # Si alguno es menor de lo permitido
            if (obj.N_Agujeros < 1) :                           # si Numero de Agujeros es menor 1
                obj.N_Agujeros = 1                              # dejarlo en 1
            else:                                               # si no a cambiado N_Agujeros, a sido Numero_Agujeros_R
                obj.N_Agujeros_R = 2                       # dejar Numero Agujeros del coliso en 2
         
        # Creo la variable de total agujeros 
        N_Agujeros_T = obj.N_Agujeros + obj.N_Agujeros_R
        # ----------------------------
        #  ---- Genero Cuerpo exterior
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((N_Agujeros_T-1)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((N_Agujeros_T-1)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((N_Agujeros_T-1)*12.5)+6.25,0,0)
        PC4 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        C4 = Part.Arc(P4,PC4,P1)
        S = Part.Shape([L1,C2,L3,C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude (FreeCAD.Vector(0,0,3.125))
        #  -----------------------------
        #  ---- Genero Cuerpos a restar 
        #  -----------------------------
        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( x*12.5, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x==0:
                Agujeros = Agujero
            else:
                Agujeros=Agujeros.fuse (Agujero)
        P = P.cut (Agujeros)
        #  ---- Genero Cuerpo del Agujero Rasgado
        #  ---- Calculo desplamiento para iniciar el coliso
        Desp = obj.N_Agujeros*12.5
        Pto01 = FreeCAD.Vector(0+Desp,-3.5,0)
        Pto02 = FreeCAD.Vector(((obj.N_Agujeros_R-1)*12.5)+Desp,-3.5,0)
        Pto03 = FreeCAD.Vector(((obj.N_Agujeros_R-1)*12.5)+Desp,3.5,0)
        Pto04 = FreeCAD.Vector(0+Desp,3.5,0)
        #  ---- Genero puntos para circulos
        PtoC2 = FreeCAD.Vector((((obj.N_Agujeros_R-1)*12.5)+3.5)+Desp,0,0)
        PtoC4 = FreeCAD.Vector(-3.5+Desp,0,0)
        #  ---- Creamos lineas y arcos
        LRest1 = Part.LineSegment(Pto01,Pto02) 
        CRest2 = Part.Arc(Pto02,PtoC2,Pto03)   
        LRest3 = Part.LineSegment(Pto03,Pto04)
        CRest4 = Part.Arc(Pto04,PtoC4,Pto01)
        SRest = Part.Shape([LRest1,CRest2,LRest3,CRest4])
        WRest = Part.Wire(SRest.Edges)
        #  ---- Creo la cara con el contorno
        FRest = Part.Face(WRest)
        PRest = FRest.extrude (FreeCAD.Vector(0,0,5))
        P = P.cut (PRest)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR_SLT_SE_ERR-BU" + str(obj.N_Agujeros) + "x01x00.25x" + str(obj.N_Agujeros_R)
        #  ---- Añado emplzamiento al objeto
        P.Placement = obj.Placement
        obj.Shape = P

class STR_STD_BRD_AY:
    ''' Brazo Stemfie angulo en Y Nº_Agureros en horizontal y Nº agujeros en inclinada '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros_X","Valores Pieza","Nº Agujeros en parte Horizontal\nMínimo 1")
        obj.N_Agujeros_X = 3
        obj.addProperty("App::PropertyInteger","N_Agujeros_Inclinado","Valores Pieza","Nº Agujeros en parte inclinada\nMínimo 1")
        obj.N_Agujeros_Inclinado = 2
        obj.addProperty("App::PropertyAngle","Angulo","Valores Pieza","Ángulo\nMínimo = 0\nMáximo = 180")
        obj.Angulo = 135
        
    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo que Numero_Agujeros mayor de 2 y Angulo en 60 y 180
        if (obj.N_Agujeros_X < 1) or (obj.N_Agujeros_Inclinado < 1) or (obj.Angulo < 0) or (obj.Angulo > 180):
            if (obj.N_Agujeros_X < 1) : obj.N_Agujeros_X = 1
            if (obj.N_Agujeros_Inclinado < 1) : obj.N_Agujeros_Inclinado = 1
            if (obj.Angulo < 0) : obj.Angulo = 0
            if (obj.Angulo > 180) : obj.Angulo = 180
        # ----------------------------
        #  ---- Genero Cuerpo Horizontal
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector( ((obj.N_Agujeros_X-1)*12.5)+6.25,-6.25,0 )
        P3 = FreeCAD.Vector( ((obj.N_Agujeros_X-1)*12.5)+6.25,6.25,0 )
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero punto para arco
        PC2 = FreeCAD.Vector(obj.N_Agujeros_X*12.5,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        L4 = Part.LineSegment(P4,P1)
        S = Part.Shape([L1,C2,L3,L4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude (FreeCAD.Vector(0,0,-3.125))
        # Hago los Agujeros de X
        for x in range(obj.N_Agujeros_X):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( (x*12.5)+6.25, 0, -5), FreeCAD.Vector(0, 0, 1))
            if x==0:
                Agujeros = Agujero
            else:
                Agujeros=Agujeros.fuse (Agujero)
        P = P.cut (Agujeros)
        # Condicional para angulo 180 no generar cilindros
        if obj.Angulo != 180 :
            # Tengo que meter un cuarto de cilindro y unirlo a P
            # Añado condicional para que sea en funcion del angulo
            Ang = (180 - int(obj.Angulo)) / 2
            Curva = Part.makeCylinder(3.125, 12.5, FreeCAD.Vector(0, -6.25, 0), FreeCAD.Vector(0, 1, 0),Ang)
            Curva.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),180)
            P = P.fuse (Curva)
        #  ---- Genero Cuerpo Inclinado
        Pto1 = FreeCAD.Vector(0,-6.25,0)
        Pto2 = FreeCAD.Vector( ((obj.N_Agujeros_Inclinado-1)*12.5)+6.25,-6.25,0 )
        Pto3 = FreeCAD.Vector( ((obj.N_Agujeros_Inclinado-1)*12.5)+6.25,6.25,0 )
        Pto4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero punto para arco
        PtoC2 = FreeCAD.Vector(obj.N_Agujeros_Inclinado*12.5,0,0)
        #  ---- Creamos lineas y arcos
        LInc1 = Part.LineSegment(Pto1,Pto2) 
        CInc2 = Part.Arc(Pto2,PtoC2,Pto3)   
        LInc3 = Part.LineSegment(Pto3,Pto4)
        LInc4 = Part.LineSegment(Pto4,Pto1)
        SInc = Part.Shape([LInc1,CInc2,LInc3,LInc4])
        WInc = Part.Wire(SInc.Edges)
        #  ---- Creo la cara con el contorno
        FInc = Part.Face(WInc)
        #  ---- Le doy Volumen a la cara
        PInc = FInc.extrude (FreeCAD.Vector(0,0,3.125))
        # Hago los Agujeros en el cuerpo inclinado
        for x in range(obj.N_Agujeros_Inclinado):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( (x*12.5)+6.25, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x==0:
                Agujeros = Agujero
            else:
                Agujeros=Agujeros.fuse (Agujero)
        PInc = PInc.cut (Agujeros)
        # Condicional para angulo 180 no generar cilindros
        if obj.Angulo != 180 :
            Curva = Part.makeCylinder(3.125, 12.5, FreeCAD.Vector(0, -6.25, 0), FreeCAD.Vector(0, 1, 0),Ang)
            Curva.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),-Ang)
            PInc = PInc.fuse (Curva)
        # Giro en Y
        PInc.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),obj.Angulo*-1)
        # Junto los dos cuerpos 
        P = P.fuse(PInc)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR_STD_BRD_AY-" + str(obj.N_Agujeros_X) + "x" + str(obj.N_Agujeros_Inclinado) + " " + str(obj.Angulo)
        #  ---- Añado emplazamiento al objeto
        P.Placement = obj.Placement
        obj.Shape = P

class STR_STD_BRT_AZ:
    ''' Brazo Stemfie con brazos inclinados en extremos '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros_X","Valores Pieza","Nº Agujeros en Barra Central\nMínimo = 3")
        obj.N_Agujeros_X = 3
        obj.addProperty("App::PropertyInteger","N_Agujeros_Y1","Valores Pieza","Nº Agujeros en Barra Vertical Izq\nMínimo = 1")
        obj.N_Agujeros_Y1=2
        obj.addProperty("App::PropertyInteger","N_Agujeros_Y2","Valores Pieza","Nº Agujeros en Barra Vertical Dch\nMínimo = 1")
        obj.N_Agujeros_Y2=2
        obj.addProperty("App::PropertyAngle","Angulo","Valores Pieza","Ángulo\nMínimo = 90\nMáximo = 180")
        obj.Angulo = 90

    def execute(self,obj):
        import Part,FreeCAD,FreeCADGui,math

        # Compruebo Valores
        if (obj.N_Agujeros_X < 3) or (obj.N_Agujeros_Y1 < 1)or (obj.N_Agujeros_Y2 < 1) or (obj.Angulo < 90) or (obj.Angulo > 180):
            if (obj.N_Agujeros_X < 3) : obj.N_Agujeros_X = 3
            if (obj.N_Agujeros_Y1 < 1) : obj.N_Agujeros_Y1 = 1
            if (obj.N_Agujeros_Y2 < 1) : obj.N_Agujeros_Y2 = 1
            if (obj.Angulo < 90) : obj.Angulo = 90
            if (obj.Angulo > 180) : obj.Angulo = 180
            #return
        
        # Genero Pieza en X
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((obj.N_Agujeros_X-1)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((obj.N_Agujeros_X-1)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros_X-1)*12.5)+6.25,0,0)
        PC4 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        C4 = Part.Arc(P4,PC4,P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1,C2,L3,C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PX = F.extrude (FreeCAD.Vector(0,0,3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros_X):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( x*12.5, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x==0:
                Agujeros = Agujero
            else:
                Agujeros=Agujeros.fuse (Agujero)
        PX = PX.cut (Agujeros)
        
        # Genero Piezas en Y1
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((obj.N_Agujeros_Y1)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((obj.N_Agujeros_Y1)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros_Y1)*12.5)+6.25,0,0)
        PC4 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        C4 = Part.Arc(P4,PC4,P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1,C2,L3,C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PY1 = F.extrude (FreeCAD.Vector(0,0,3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros_Y1+1):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector(x*12.5, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x==0:
                Agujeros = Agujero
            else:
                Agujeros=Agujeros.fuse (Agujero)
        PY1 = PY1.cut (Agujeros)

        PY1.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),obj.Angulo)

        P = PX.fuse (PY1)

        # Genero Piezas en Y2
        Desp = (obj.N_Agujeros_X-1)*12.5
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0+Desp,-6.25,0)
        P2 = FreeCAD.Vector(((obj.N_Agujeros_Y2)*12.5)+Desp,-6.25,0)
        P3 = FreeCAD.Vector(((obj.N_Agujeros_Y2)*12.5)+Desp,6.25,0)
        P4 = FreeCAD.Vector(0+Desp,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros_Y2)*12.5)+6.25+Desp,0,0)
        PC4 = FreeCAD.Vector(-6.25+Desp,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        C4 = Part.Arc(P4,PC4,P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1,C2,L3,C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PY2 = F.extrude (FreeCAD.Vector(0,0,3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros_Y2+1):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector(x*12.5+Desp, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x==0:
                Agujeros = Agujero
            else:
                Agujeros=Agujeros.fuse (Agujero)
        PY2 = PY2.cut (Agujeros)
        #  ---- giro parte Y 2 (restando de 180)----
        PY2.rotate(FreeCAD.Vector(Desp,0,0),FreeCAD.Vector(0,0,1),(180 - int(obj.Angulo)))

        P = P.fuse (PY2)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR_STD_BRT_AZ-" + str(obj.N_Agujeros_Y1) + "x" + str(obj.N_Agujeros_X) + "x" + str(obj.N_Agujeros_Y2) + " " + str(obj.Angulo)

        P.Placement = obj.Placement
        obj.Shape = P

class STR_STD_BRT_AY:
    ''' Brazo Stemfie con brazos inclinados en extremos en eje Y'''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros_X","Valores Pieza","Nº Agujeros en parte Horizontal\nMínimo 1").N_Agujeros_X = 3
        obj.addProperty("App::PropertyInteger","N_Agujeros_Inclinado_1","Valores Pieza","Nº Agujeros en parte inclinada Izq\nMínimo 1").N_Agujeros_Inclinado_1 = 2
        obj.addProperty("App::PropertyInteger","N_Agujeros_Inclinado_2","Valores Pieza","Nº Agujeros en parte inclinada Dch\nMínimo 1").N_Agujeros_Inclinado_2 = 2
        obj.addProperty("App::PropertyAngle","Angulo","Valores Pieza","Ángulo\nMínimo = 0\nMáximo = 180").Angulo = 135
        

    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo que Numero_Agujeros mayor de 2 y Angulo en 60 y 180
        if (obj.N_Agujeros_X < 1) or (obj.N_Agujeros_Inclinado_1 < 1) or (obj.N_Agujeros_Inclinado_2 < 1) or (obj.Angulo < 0) or (obj.Angulo > 180):
            if (obj.N_Agujeros_X < 1) : obj.N_Agujeros_X = 1
            if (obj.N_Agujeros_Inclinado_1 < 1) : obj.N_Agujeros_Inclinado_1 = 1
            if (obj.N_Agujeros_Inclinado_2 < 1) : obj.N_Agujeros_Inclinado_2 = 1
            if (obj.Angulo < 0) : obj.Angulo = 0
            if (obj.Angulo > 180) : obj.Angulo = 180
        # Limito nº agujeros en Inclinadas cuando angulo es 0
        if (obj.Angulo == 0):
            if (obj.N_Agujeros_Inclinado_1 > obj.N_Agujeros_X):
                obj.N_Agujeros_Inclinado_1 = obj.N_Agujeros_X
            if (obj.N_Agujeros_Inclinado_2 > obj.N_Agujeros_X):
                obj.N_Agujeros_Inclinado_2 = obj.N_Agujeros_X


        # ----------------------------
        #  ---- Genero Cuerpo Horizontal
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector( ((obj.N_Agujeros_X)*12.5),-6.25,0 )
        P3 = FreeCAD.Vector( ((obj.N_Agujeros_X)*12.5),6.25,0 )
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        L2 = Part.LineSegment(P2,P3)
        L3 = Part.LineSegment(P3,P4)
        L4 = Part.LineSegment(P4,P1)
        S = Part.Shape([L1,L2,L3,L4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude (FreeCAD.Vector(0,0,-3.125))
        # Hago los Agujeros de X
        for x in range(obj.N_Agujeros_X):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( (x*12.5)+6.25, 0, -5), FreeCAD.Vector(0, 0, 1))
            if x==0:
                Agujeros = Agujero
            else:
                Agujeros=Agujeros.fuse (Agujero)
        P = P.cut (Agujeros)

        # Condicional para angulo 180 no generar cilindros
        if obj.Angulo != 180 :
            # Tengo que meter dos cachos de cilindro en los extremos y unirlo a P
            # Añado condicional para que sea en funcion del angulo
            #  ---- Primer Cilindro
            Ang = (180 - int(obj.Angulo)) / 2
            Curva1 = Part.makeCylinder(3.125, 12.5, FreeCAD.Vector(0, -6.25, 0), FreeCAD.Vector(0, 1, 0),Ang)
            Curva1.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),180)
            P = P.fuse (Curva1)
            #  ---- Segundo Cilindro
            Curva2 = Part.makeCylinder(3.125, 12.5, FreeCAD.Vector(obj.N_Agujeros_X * 12.5, -6.25, 0), FreeCAD.Vector(0, 1, 0),Ang)
            Curva2.rotate(FreeCAD.Vector(obj.N_Agujeros_X * 12.5,0,0),FreeCAD.Vector(0,1,0),180-Ang)
            P = P.fuse (Curva2)

        #
        #  ---- Genero Cuerpo Inclinado_1 Izquierdo
        Pto1 = FreeCAD.Vector(0,-6.25,0)
        Pto2 = FreeCAD.Vector( ((obj.N_Agujeros_Inclinado_1-1)*12.5)+6.25,-6.25,0 )
        Pto3 = FreeCAD.Vector( ((obj.N_Agujeros_Inclinado_1-1)*12.5)+6.25,6.25,0 )
        Pto4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero punto para arco
        PtoC2 = FreeCAD.Vector(obj.N_Agujeros_Inclinado_1*12.5,0,0)
        #  ---- Creamos lineas y arcos
        LInc1 = Part.LineSegment(Pto1,Pto2) 
        CInc2 = Part.Arc(Pto2,PtoC2,Pto3)   
        LInc3 = Part.LineSegment(Pto3,Pto4)
        LInc4 = Part.LineSegment(Pto4,Pto1)
        SInc = Part.Shape([LInc1,CInc2,LInc3,LInc4])
        WInc = Part.Wire(SInc.Edges)
        #  ---- Creo la cara con el contorno
        FInc = Part.Face(WInc)
        #  ---- Le doy Volumen a la cara
        PInc = FInc.extrude (FreeCAD.Vector(0,0,3.125))
        # Hago los Agujeros en el cuerpo inclinado
        for x in range(obj.N_Agujeros_Inclinado_1):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( (x*12.5)+6.25, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x==0:
                Agujeros = Agujero
            else:
                Agujeros=Agujeros.fuse (Agujero)
        PInc = PInc.cut (Agujeros)
        # Condicional para angulo 180 no generar cilindros
        if obj.Angulo != 180 :
            # Curva
            Curva = Part.makeCylinder(3.125, 12.5, FreeCAD.Vector(0, -6.25, 0), FreeCAD.Vector(0, 1, 0),Ang)
            Curva.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),-Ang)
            PInc = PInc.fuse (Curva)
        # Giro en Y
        PInc.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),obj.Angulo*-1)
        # Junto los dos cuerpos 
        P = P.fuse(PInc)

        #  ---- Genero Cuerpo Inclinado_2 Izquierdo
        Desp = obj.N_Agujeros_X * 12.5
        Pto1 = FreeCAD.Vector(Desp,-6.25,0)
        Pto2 = FreeCAD.Vector( ((obj.N_Agujeros_Inclinado_2-1)*12.5)+6.25+Desp,-6.25,0 )
        Pto3 = FreeCAD.Vector( ((obj.N_Agujeros_Inclinado_2-1)*12.5)+6.25+Desp,6.25,0 )
        Pto4 = FreeCAD.Vector(Desp,6.25,0)
        #  ---- Genero punto para arco
        PtoC2 = FreeCAD.Vector((obj.N_Agujeros_Inclinado_2*12.5)+Desp,0,0)
        #  ---- Creamos lineas y arcos
        LInc1 = Part.LineSegment(Pto1,Pto2) 
        CInc2 = Part.Arc(Pto2,PtoC2,Pto3)   
        LInc3 = Part.LineSegment(Pto3,Pto4)
        LInc4 = Part.LineSegment(Pto4,Pto1)
        SInc = Part.Shape([LInc1,CInc2,LInc3,LInc4])
        WInc = Part.Wire(SInc.Edges)
        #  ---- Creo la cara con el contorno
        FInc = Part.Face(WInc)
        #  ---- Le doy Volumen a la cara
        PInc = FInc.extrude (FreeCAD.Vector(0,0,-3.125))
        # Hago los Agujeros en el cuerpo inclinado
        for x in range(obj.N_Agujeros_Inclinado_2):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( (x*12.5)+6.25+Desp, 0, -4), FreeCAD.Vector(0, 0, 1))
            if x==0:
                Agujeros = Agujero
            else:
                Agujeros=Agujeros.fuse (Agujero)
        PInc = PInc.cut (Agujeros)
        # Condicional para angulo 180 no generar cilindros
        if obj.Angulo != 180 :
            # Curva
            Curva = Part.makeCylinder(3.125, 12.5, FreeCAD.Vector(Desp, -6.25, 0), FreeCAD.Vector(0, 1, 0),Ang)
            Curva.rotate(FreeCAD.Vector(Desp,0,0),FreeCAD.Vector(0,1,0),180)
            PInc = PInc.fuse (Curva)
        # Giro en Y
        PInc.rotate(FreeCAD.Vector(Desp,0,0),FreeCAD.Vector(0,1,0),(180-int(obj.Angulo))*-1)
        # Junto los dos cuerpos 
        P = P.fuse(PInc)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR_STD_BRT_AY-" + str(obj.N_Agujeros_Inclinado_1) + "x" + str(obj.N_Agujeros_X) + "x" + str(obj.N_Agujeros_Inclinado_2) + " " + str(obj.Angulo)
        

        #  ---- Añado emplazamiento al objeto
        P.Placement = obj.Placement
        obj.Shape = P

class STR_STD_CR:
    ''' Brazo Stemfie Cruz con longitud de brazos independientes '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros_X_Positivo","Valores Pieza","Nº Agujeros en X +\nMínimo = 1").N_Agujeros_X_Positivo = 3
        obj.addProperty("App::PropertyInteger","N_Agujeros_X_Negativo","Valores Pieza","Nº Agujeros en X -\nMínimo = 1").N_Agujeros_X_Negativo = 3
        obj.addProperty("App::PropertyInteger","N_Agujeros_Y_Positivo","Valores Pieza","Nº Agujeros en Y +\nMínimo = 1").N_Agujeros_Y_Positivo = 2
        obj.addProperty("App::PropertyInteger","N_Agujeros_Y_Negativo","Valores Pieza","Nº Agujeros en Y -\nMínimo = 1").N_Agujeros_Y_Negativo = 2

    def execute(self,obj):
        import Part,FreeCAD,FreeCADGui

        # Compruebo que Numero_Agujeros mayor de 2
        if (obj.N_Agujeros_X_Positivo < 1) or (obj.N_Agujeros_X_Negativo < 1) or (obj.N_Agujeros_Y_Positivo < 1) or (obj.N_Agujeros_Y_Negativo < 1):
            if (obj.N_Agujeros_X_Positivo < 1) : obj.N_Agujeros_X_Positivo = 1
            if (obj.N_Agujeros_X_Negativo < 1) : obj.N_Agujeros_X_Negativo = 1
            if (obj.N_Agujeros_Y_Positivo < 1) : obj.N_Agujeros_Y_Positivo = 1
            if (obj.N_Agujeros_Y_Negativo < 1) : obj.N_Agujeros_Y_Negativo = 1
            #return
        
        # Genero Pieza en X+
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((obj.N_Agujeros_X_Positivo)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((obj.N_Agujeros_X_Positivo)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros_X_Positivo)*12.5)+6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        L4 = Part.LineSegment(P4,P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1,C2,L3,L4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PX = F.extrude (FreeCAD.Vector(0,0,3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros_X_Positivo+1):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( x*12.5, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x==0:
                Agujeros = Agujero
            else:
                Agujeros=Agujeros.fuse (Agujero)
        PX = PX.cut (Agujeros)
        P = PX
        # Genero Pieza en X-
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((obj.N_Agujeros_X_Negativo)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((obj.N_Agujeros_X_Negativo)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros_X_Negativo)*12.5)+6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        L4 = Part.LineSegment(P4,P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1,C2,L3,L4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PX = F.extrude (FreeCAD.Vector(0,0,3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros_X_Negativo+1):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( x*12.5, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x==0:
                Agujeros = Agujero
            else:
                Agujeros=Agujeros.fuse (Agujero)
        PX = PX.cut (Agujeros)
        PX.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),180)
        P = P.fuse(PX)
        # Genero Pieza en Y+
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((obj.N_Agujeros_Y_Positivo)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((obj.N_Agujeros_Y_Positivo)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros_Y_Positivo)*12.5)+6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        L4 = Part.LineSegment(P4,P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1,C2,L3,L4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PY = F.extrude (FreeCAD.Vector(0,0,3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros_Y_Positivo+1):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( x*12.5, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x==0:
                Agujeros = Agujero
            else:
                Agujeros=Agujeros.fuse (Agujero)
        PY = PY.cut (Agujeros)
        PY.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),90)
        P = P.fuse (PY)
        # Genero Pieza en Y-
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((obj.N_Agujeros_Y_Negativo)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((obj.N_Agujeros_Y_Negativo)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros_Y_Negativo)*12.5)+6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        L4 = Part.LineSegment(P4,P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1,C2,L3,L4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        PY = F.extrude (FreeCAD.Vector(0,0,3.125))
        #  ---- Bucle para agujeros
        for x in range(obj.N_Agujeros_Y_Negativo+1):
            Agujero = Part.makeCylinder(3.5, 5, FreeCAD.Vector( x*12.5, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x==0:
                Agujeros = Agujero
            else:
                Agujeros=Agujeros.fuse (Agujero)
        PY = PY.cut (Agujeros)
        PY.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),270)
        P = P.fuse (PY)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR_STD_CR-" + str(obj.N_Agujeros_X_Positivo) + "x" + str(obj.N_Agujeros_X_Negativo) + "x" + str(obj.N_Agujeros_Y_Positivo) +"x" + str(obj.N_Agujeros_Y_Negativo)

        P.Placement = obj.Placement
        obj.Shape = P

# Vigas
class STR_ESS:
    ''' Beam - Straight - Ending Square/Square
        Viga Simple Stemfie '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros","Valores Pieza","Nº Agujeros Pieza\nMínimo = 1").N_Agujeros = 4

    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo que Numero_Agujeros mayor de 1
        if (obj.N_Agujeros < 1):obj.N_Agujeros = 1

        # Genero el cuerpo exterior
        P = Part.makeBox((obj.N_Agujeros*12.5),12.5,12.5,FreeCAD.Vector(-6.25,-6.25,-6.25),FreeCAD.Vector(0,0,1))
        #  ---- Bucle para agujeros en X
        for x in range(obj.N_Agujeros):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( x*12.5, 0, -10), FreeCAD.Vector(0, 0, 1))
            if x == 0 : 
                Agujeros = Agujero
            else: 
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut (Agujeros)
        #  ---- Bucle para agujeros en Y
        for x in range(obj.N_Agujeros):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( x*12.5, -10, 0), FreeCAD.Vector(0, 1, 0))
            if x==0 : 
                Agujeros = Agujero
            else: 
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut (Agujeros)
        #  ---- Agujeros en Z
        Agujero = Part.makeCylinder(3.5, (obj.N_Agujeros*12.5) + 25, FreeCAD.Vector( -10, 0, 0), FreeCAD.Vector(1, 0, 0))
        P = P.cut (Agujero)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR_ESS_BU-" + str(obj.N_Agujeros) + "x01x01"
       
        P.Placement = obj.Placement
        obj.Shape = P

class STR_ERR:
    ''' Beam - Straight - Ending Round/Round
       
        ________________
       /                 \_
      |   ()    ()    ()  |
       \ _______________ /
    
           1     2     3
            ---------> 
             N_Agujeros

        Variables:
            Codigo          'Demoninacion'
            N_Agujeros      'Numero Agujeros que contiene la pieza
    
    '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros","Valores Pieza","Nº Agujeros Pieza Simple\nMínimo = 3").N_Agujeros = 5
        

    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo que N_Agujeros mayor de 3
        if (obj.N_Agujeros < 3): obj.N_Agujeros = 3
        
        
        #  ---- Genero puntos de los contornos
        P1 = FreeCAD.Vector(0,-6.25,0)
        P2 = FreeCAD.Vector((obj.N_Agujeros-1)*12.5,-6.25,0)
        P3 = FreeCAD.Vector((obj.N_Agujeros-1)*12.5,6.25,0)
        P4 = FreeCAD.Vector(0,6.25,0)
        #  ---- Genero puntos para circulos
        PC2 = FreeCAD.Vector(((obj.N_Agujeros-1)*12.5)+6.25,0,0)
        PC4 = FreeCAD.Vector(-6.25,0,0)
        #  ---- Creamos lineas y arcos
        L1 = Part.LineSegment(P1,P2) 
        C2 = Part.Arc(P2,PC2,P3)   
        L3 = Part.LineSegment(P3,P4)
        C4 = Part.Arc(P4,PC4,P1)
        #  ---- Creo el contorno
        S = Part.Shape([L1,C2,L3,C4])
        W = Part.Wire(S.Edges)
        #  ---- Creo la cara con el contorno
        F = Part.Face(W)
        #  ---- Le doy Volumen a la cara
        P = F.extrude (FreeCAD.Vector(0,0,12.5))
        #  ---- Bucle para agujeros superiores
        for x in range(obj.N_Agujeros):
            Agujero = Part.makeCylinder(3.5, 15, FreeCAD.Vector( x*12.5, 0, -1), FreeCAD.Vector(0, 0, 1))
            if x == 0 : 
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut (Agujeros)
        #  ---- Bucle para agujeros superiores
        for x in range(obj.N_Agujeros-2):
            Agujero = Part.makeCylinder(3.5, 15, FreeCAD.Vector( (x*12.5)+12.5, -7, 6.25), FreeCAD.Vector(0, 1, 0))
            if x == 0 : 
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut (Agujeros)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR ERR-BU" + str(obj.N_Agujeros) + "x01x00.25"

        P.Placement = obj.Placement
        obj.Shape = P

class STR_BEM:
    ''' Viga Cubo Stemfie '''
    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros_X","Valores Pieza","Nº Agujeros En X\nMínimo = 1")
        obj.N_Agujeros_X = 2
        obj.addProperty("App::PropertyInteger","N_Agujeros_Y","Valores Pieza","Nº Agujeros En Y\nMínimo = 1")
        obj.N_Agujeros_Y = 2
        obj.addProperty("App::PropertyInteger","N_Agujeros_Z","Valores Pieza","Nº Agujeros En Z\nMínimo = 1")
        obj.N_Agujeros_Z = 2

    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo que Numero_Agujeros mayor de 1
        if (obj.N_Agujeros_X < 1) or (obj.N_Agujeros_Y < 1) or (obj.N_Agujeros_Z < 1):
            if (obj.N_Agujeros_X < 1) : obj.N_Agujeros_X = 1
            if (obj.N_Agujeros_Y < 1) : obj.N_Agujeros_Y = 1
            if (obj.N_Agujeros_Z < 1) : obj.N_Agujeros_Z = 1

        # Genero el cuerpo exterior
        P = Part.makeBox((obj.N_Agujeros_X*12.5),(obj.N_Agujeros_Y*12.5),(obj.N_Agujeros_Z*12.5),FreeCAD.Vector(-6.25,-6.25,-6.25),FreeCAD.Vector(0,0,1))
        #  ---- Bucle para agujeros en X
        for x in range(obj.N_Agujeros_X):
            for y in range(obj.N_Agujeros_Y):
                Agujero = Part.makeCylinder(3.5, (obj.N_Agujeros_Z*12.5)+20, FreeCAD.Vector( x*12.5, y*12.5, -10), FreeCAD.Vector(0, 0, 1))
                if (y == 0) and (x == 0) : 
                    AgujerosX = Agujero
                else:
                    AgujerosX = AgujerosX.fuse(Agujero)
        
        #  ---- Bucle para agujeros en Y
        for x in range(obj.N_Agujeros_X):
            for z in range(obj.N_Agujeros_Z):
                Agujero = Part.makeCylinder(3.5, (obj.N_Agujeros_Y*12.5)+20, FreeCAD.Vector( x*12.5, -10, z*12.5), FreeCAD.Vector(0, 1, 0))
                if (z == 0) and (x == 0) : 
                    AgujerosY = Agujero
                else:
                    AgujerosY = AgujerosY.fuse(Agujero)

        #  ---- Agujeros en Z
        for z in range(obj.N_Agujeros_Z):
            for y in range(obj.N_Agujeros_Y):
                Agujero = Part.makeCylinder(3.5, (obj.N_Agujeros_X*12.5)+20, FreeCAD.Vector( -10, y*12.5, z*12.5), FreeCAD.Vector(1, 0, 0))
                if (y == 0) and (z == 0) : 
                    AgujerosZ = Agujero
                else:
                    AgujerosZ = AgujerosZ.fuse(Agujero)

        Agujeros = AgujerosX.fuse(AgujerosY)
        Agujeros = Agujeros.fuse(AgujerosZ)
        P = P.cut(Agujeros)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR_BEM-" + str(obj.N_Agujeros_X) + "x" + str(obj.N_Agujeros_Y) + "x" + str(obj.N_Agujeros_Z)
       
        P.Placement = obj.Placement
        obj.Shape = P

class AGD_ESS_USH_SYM:
    ''' Viga Stemfie con brazos a 90º en los estremos '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros_X","Valores Pieza","Nº Agujeros Pieza_X\nMínimo = 3")
        obj.N_Agujeros_X = 3
        obj.addProperty("App::PropertyInteger","N_Agujeros_Y1","Valores Pieza","Nº Agujeros en Barra Vertical Izq\nMínimo = 1")
        obj.N_Agujeros_Y1 = 2 
        obj.addProperty("App::PropertyInteger","N_Agujeros_Y2","Valores Pieza","Nº Agujeros en Barra Vertical Dch\nMínimo = 1")
        obj.N_Agujeros_Y2 = 2

    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo Valores
        if (obj.N_Agujeros_X < 3) or (obj.N_Agujeros_Y1 < 1)or (obj.N_Agujeros_Y2 < 1):
            if (obj.N_Agujeros_X < 3) : obj.N_Agujeros_X = 3
            if (obj.N_Agujeros_Y1 < 1) : obj.N_Agujeros_Y1 = 1
            if (obj.N_Agujeros_Y2 < 1) : obj.N_Agujeros_Y2 = 1

        # Genero el cuerpo exterior
        P = Part.makeBox((obj.N_Agujeros_X*12.5),12.5,12.5,FreeCAD.Vector(-6.25,-6.25,-6.25),FreeCAD.Vector(0,0,1))
        PY1 = Part.makeBox(12.5,((obj.N_Agujeros_Y1+1)*12.5),12.5,FreeCAD.Vector(-6.25,-6.25,-6.25),FreeCAD.Vector(0,0,1))
        PY2 = Part.makeBox(12.5,((obj.N_Agujeros_Y2+1)*12.5),12.5,FreeCAD.Vector(((obj.N_Agujeros_X-1)*12.5)-6.25,-6.25,-6.25),FreeCAD.Vector(0,0,1))
        P = P.fuse(PY1)
        P = P.fuse(PY2)

        #  Genero los agujeros de la parte central
        #  ---- Bucle para agujeros en cara X
        for x in range(obj.N_Agujeros_X):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( x*12.5, 0, -10), FreeCAD.Vector(0, 0, 1))
            if x==0:
                AgujerosX = Agujero
            else:
                AgujerosX = AgujerosX.fuse (Agujero)

        for y in range(obj.N_Agujeros_Y1):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( 0, (y*12.5)+12.5, -10), FreeCAD.Vector(0, 0, 1))
            if y==0:
                AgujerosY1 = Agujero
            else:
                AgujerosY1 = AgujerosY1.fuse (Agujero)
        
        for y in range(obj.N_Agujeros_Y2):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( ((obj.N_Agujeros_X-1)*12.5), (y*12.5)+12.5, -10), FreeCAD.Vector(0, 0, 1))
            if y==0:
                AgujerosY2 = Agujero
            else:
                AgujerosY2 = AgujerosY2.fuse (Agujero)

        Agujeros = AgujerosX.fuse(AgujerosY1)
        Agujeros = Agujeros.fuse(AgujerosY2)        
        P = P.cut (Agujeros)

        #  ---- Bucle para agujeros en cara Z
        for y in range(obj.N_Agujeros_X):
            if (y == 0): Longitud = (obj.N_Agujeros_Y1)*12.5
            if (y == obj.N_Agujeros_X-1): Longitud = (obj.N_Agujeros_Y2)*12.5
            if (y > 0) and (y < obj.N_Agujeros_X-1) : Longitud = 0

            Agujero = Part.makeCylinder(3.5, Longitud+20, FreeCAD.Vector( y*12.5, -10, 0), FreeCAD.Vector(0, 1, 0))
            if y==0 :
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut (Agujeros)
        #  ---- Bucle para agujeros en cara Y
        if (obj.N_Agujeros_Y1) >= (obj.N_Agujeros_Y2): 
            repeticion=(obj.N_Agujeros_Y1)
        else:
            repeticion=(obj.N_Agujeros_Y2)

        for x in range(repeticion+1):
            Agujero = Part.makeCylinder(3.5, (obj.N_Agujeros_X*12.5) + 25, FreeCAD.Vector( -10, (x*12.5), 0), FreeCAD.Vector(1, 0, 0))
            if x==0 :
                Agujeros = Agujero
            else:
                Agujeros = Agujeros.fuse(Agujero)
        P = P.cut (Agujeros)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "AGD_ESS_USH_SYM-" + str(obj.N_Agujeros_Y1) + "x" + str(obj.N_Agujeros_X) + "x" + str(obj.N_Agujeros_Y2)
       
        P.Placement = obj.Placement
        obj.Shape = P

class STR_BED:
    ''' Viga Angular Stemfie '''


    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros_X","Valores Pieza","Nº Agujeros Pieza_X\nMínimo = 2")
        obj.N_Agujeros_X = 3
        obj.addProperty("App::PropertyInteger","N_Agujeros_Y","Valores Pieza","Nº Agujeros en Barra Angular\nMínimo = 1")
        obj.N_Agujeros_Y = 2
        obj.addProperty("App::PropertyAngle","Angulo","Valores Pieza","Ángulo\nMínimo = 90\nMáximo = 180")
        obj.Angulo = 135
        

    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo Valores
        if (obj.N_Agujeros_X < 2) or (obj.N_Agujeros_Y < 1) or (obj.Angulo < 90) or (obj.Angulo > 180):
            if (obj.N_Agujeros_X < 2) : obj.N_Agujeros_X = 2
            if (obj.N_Agujeros_Y < 1) : obj.N_Agujeros_Y = 1
            if (obj.Angulo < 90) : obj.Angulo = 90
            if (obj.Angulo > 180) : obj.Angulo = 180

        # Genero el cuerpo exterior
        P = Part.makeBox(((obj.N_Agujeros_X-1)*12.5)+6.25,12.5,12.5,FreeCAD.Vector(0,-6.25,-6.25),FreeCAD.Vector(0,0,1))
        Curva = Part.makeCylinder(6.25, 12.5, FreeCAD.Vector( 0, 0, -6.25), FreeCAD.Vector(0, 0, 1))
        P = P.fuse(Curva)
 
        #  Genero los agujeros en el cuerpo principal
        #  ---- Bucle para agujeros en cara X
        for x in range(obj.N_Agujeros_X):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( x*12.5, 0, -10), FreeCAD.Vector(0, 0, 1))
            if x==0 :
                AgujerosX = Agujero
            else:
                AgujerosX = AgujerosX.fuse(Agujero)
        
        #  ---- Bucle para agujeros en cara Z
        for x in range(obj.N_Agujeros_X-1):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( (x*12.5)+12.5, -10, 0), FreeCAD.Vector(0, 1, 0))
            if x==0 :
                AgujerosY = Agujero
            else:
                AgujerosY = AgujerosY.fuse(Agujero)
        #  ---- Sumo los agujeros        
        Agujeros = AgujerosX.fuse(AgujerosY)
        #  ---- Se los resto al cuerpo
        P = P.cut (Agujeros)
        
        #  Genero cuerpo para luego girar
        PY1 = Part.makeBox(((obj.N_Agujeros_Y)*12.5)+6.25,12.5,12.5,FreeCAD.Vector(0,-6.25,-6.25),FreeCAD.Vector(0,0,1))
        #  Genero los agujeros en el cuerpo a girar
        #  ---- Bucle para agujeros en cara X
        for x in range(obj.N_Agujeros_Y+1):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( x*12.5, 0, -10), FreeCAD.Vector(0, 0, 1))
            if x==0 :
                AgujerosX = Agujero
            else:
                AgujerosX = AgujerosX.fuse(Agujero)
        
        #  ---- Bucle para agujeros en cara Z
        for x in range(obj.N_Agujeros_Y):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( (x*12.5)+12.5, -10, 0), FreeCAD.Vector(0, 1, 0))
            if x==0 :
                AgujerosY = Agujero
            else:
                AgujerosY = AgujerosY.fuse(Agujero)
        #  ---- Sumo los agujeros        
        Agujeros = AgujerosX.fuse(AgujerosY)
        #  ---- Se los resto al cuerpo
        PY1 = PY1.cut (Agujeros)
        #  Giro pieza
        PY1.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),obj.Angulo)
        # Uno las dos partes
        P = P.fuse(PY1)

        #   ----- Ahora que estan girados hago los circulos centrales y los resto
        #   ----- Agujero en X
        Agujero1 = Part.makeCylinder(3.5,(obj.N_Agujeros_X*12.5)+((obj.N_Agujeros_Y+1)*12.5)+12.5,FreeCAD.Vector( ((obj.N_Agujeros_Y+1)*-12.5),0,0), FreeCAD.Vector(1, 0, 0))
        #   ----- Agujero en Inclinado
        Agujero2 = Part.makeCylinder(3.5,(obj.N_Agujeros_X+obj.N_Agujeros_Y+2)*12.5,FreeCAD.Vector( ((obj.N_Agujeros_X+1)*-12.5),0,0), FreeCAD.Vector(1, 0, 0))
        Agujero2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),obj.Angulo)
        
        Agujeros = Agujero1.fuse (Agujero2)
        P = P.cut (Agujeros)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR_BED-" + str(obj.N_Agujeros_X) + "x" + str(obj.N_Agujeros_Y) + " " + str(obj.Angulo)
       
        P.Placement = obj.Placement
        obj.Shape = P
        
class STR_BET:
    ''' Viga Stemfie con brazos en los extremos Angulo variable'''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros_X","Valores Pieza","Nº Agujeros en Barra Central\nMínimo = 3")
        obj.N_Agujeros_X = 3
        obj.addProperty("App::PropertyInteger","N_Agujeros_Y1","Valores Pieza","Nº Agujeros en Barra Angular Izq\nMínimo = 1")
        obj.N_Agujeros_Y1 = 2
        obj.addProperty("App::PropertyInteger","N_Agujeros_Y2","Valores Pieza","Nº Agujeros en Barra Angular Dch\nMínimo = 1")
        obj.N_Agujeros_Y2 = 2
        obj.addProperty("App::PropertyAngle","Angulo","Valores Pieza","Ángulo\nMínimo = 90\nMáximo = 180")
        obj.Angulo = 135
        

    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo Valores
        if (obj.N_Agujeros_X < 3) or (obj.N_Agujeros_Y1 < 1) or (obj.N_Agujeros_Y2 < 1) or (obj.Angulo < 90) or (obj.Angulo > 180):
            if (obj.N_Agujeros_X < 3) : obj.N_Agujeros_X = 3
            if (obj.N_Agujeros_Y1 < 1) : obj.N_Agujeros_Y1 = 1
            if (obj.N_Agujeros_Y2 < 1) : obj.N_Agujeros_Y2 = 1
            if (obj.Angulo < 90) : obj.Angulo = 90
            if (obj.Angulo > 180) : obj.Angulo = 180

        # Genero el cuerpo exterior
        P = Part.makeBox(((obj.N_Agujeros_X-1)*12.5),12.5,12.5,FreeCAD.Vector(0,-6.25,-6.25),FreeCAD.Vector(0,0,1))
        Curva = Part.makeCylinder(6.25, 12.5, FreeCAD.Vector( 0, 0, -6.25), FreeCAD.Vector(0, 0, 1))
        P = P.fuse(Curva)
        Curva = Part.makeCylinder(6.25, 12.5,  FreeCAD.Vector( (obj.N_Agujeros_X-1)*12.5, 0, -6.25), FreeCAD.Vector(0, 0, 1))
        P = P.fuse(Curva)
 
        #  Genero los agujeros en el cuerpo principal
        #  ---- Bucle para agujeros en cara X
        for x in range(obj.N_Agujeros_X):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( x*12.5, 0, -10), FreeCAD.Vector(0, 0, 1))
            if x==0 :
                AgujerosX = Agujero
            else:
                AgujerosX = AgujerosX.fuse(Agujero)
        #  ---- Bucle para agujeros en cara Z
        for x in range(obj.N_Agujeros_X-2):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( (x*12.5)+12.5, -10, 0), FreeCAD.Vector(0, 1, 0))
            if x==0 :
                AgujerosY = Agujero
            else:
                AgujerosY = AgujerosY.fuse(Agujero)
        #  ---- Sumo los agujeros        
        Agujeros = AgujerosX.fuse(AgujerosY)
        #  ---- Se los resto al cuerpo
        P = P.cut (Agujeros)
        
        #  Genero cuerpo Izquierda
        PY1 = Part.makeBox(((obj.N_Agujeros_Y1)*12.5)+6.25,12.5,12.5,FreeCAD.Vector(0,-6.25,-6.25),FreeCAD.Vector(0,0,1))
        #  Genero los agujeros en el cuerpo a girar
        #  ---- Bucle para agujeros en cara X
        for x in range(obj.N_Agujeros_Y1+1):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( x*12.5, 0, -10), FreeCAD.Vector(0, 0, 1))
            if x==0 :
                AgujerosX = Agujero
            else:
                AgujerosX = AgujerosX.fuse(Agujero)
        #  ---- Bucle para agujeros en cara Z
        for x in range(obj.N_Agujeros_Y1):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( (x*12.5)+12.5, -10, 0), FreeCAD.Vector(0, 1, 0))
            if x==0 :
                AgujerosY = Agujero
            else:
                AgujerosY = AgujerosY.fuse(Agujero)
        #  ---- Sumo los agujeros        
        Agujeros = AgujerosX.fuse(AgujerosY)
        #  ---- Se los resto al cuerpo
        PY1 = PY1.cut (Agujeros)
        #  Giro pieza
        PY1.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),obj.Angulo)
        # Uno las dos partes
        P = P.fuse(PY1)
        #  Genero cuerpo Derecha
        PY2 = Part.makeBox(((obj.N_Agujeros_Y2)*12.5)+6.25,12.5,12.5,FreeCAD.Vector((obj.N_Agujeros_X-1)*12.5,-6.25,-6.25),FreeCAD.Vector(0,0,1))
        #  Genero los agujeros en el cuerpo a girar
        #  ---- Bucle para agujeros en cara X
        for x in range(obj.N_Agujeros_Y2+1):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( ((obj.N_Agujeros_X-1)*12.5)+x*12.5, 0, -10), FreeCAD.Vector(0, 0, 1))
            if x==0 :
                AgujerosX = Agujero
            else:
                AgujerosX = AgujerosX.fuse(Agujero)
        #  ---- Bucle para agujeros en cara Z
        for x in range(obj.N_Agujeros_Y2):
            Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( ((obj.N_Agujeros_X-1)*12.5)+(x*12.5)+12.5, -10, 0), FreeCAD.Vector(0, 1, 0))
            if x==0 :
                AgujerosY = Agujero
            else:
                AgujerosY = AgujerosY.fuse(Agujero)
        #  ---- Sumo los agujeros        
        Agujeros = AgujerosX.fuse(AgujerosY)
        #  ---- Se los resto al cuerpo
        PY2 = PY2.cut (Agujeros)
        #  Giro pieza
        PY2.rotate(FreeCAD.Vector(((obj.N_Agujeros_X-1)*12.5),0,0),FreeCAD.Vector(0,0,1),180-int(obj.Angulo))
        # Uno las dos partes
        P = P.fuse(PY2)

        #   ----- Ahora que estan girados, hago los circulos centrales y los resto
        #   ----- Agujero en X
        Agujero = Part.makeCylinder(3.5,(obj.N_Agujeros_X+obj.N_Agujeros_Y1+obj.N_Agujeros_Y2+2)*12.5,FreeCAD.Vector(((obj.N_Agujeros_Y1+1)*-12.5),0,0), FreeCAD.Vector(1, 0, 0))
        P=P.cut (Agujero)
        #   ----- Agujero en Inclinado Y1
        Agujero = Part.makeCylinder(3.5,(obj.N_Agujeros_X+obj.N_Agujeros_Y1+2)*12.5,FreeCAD.Vector( ((obj.N_Agujeros_X+1)*-12.5),0,0), FreeCAD.Vector(1, 0, 0))
        Agujero.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),obj.Angulo)
        P=P.cut (Agujero)
        #   ----- Agujero en Inclinado Y2
        Agujero = Part.makeCylinder(3.5,(obj.N_Agujeros_X+obj.N_Agujeros_Y2+2)*12.5,FreeCAD.Vector(0,0,0), FreeCAD.Vector(1, 0, 0))
        Agujero.rotate(FreeCAD.Vector(((obj.N_Agujeros_X-1)*12.5),0,0),FreeCAD.Vector(0,0,1),180-int(obj.Angulo))
        P=P.cut (Agujero)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR_BET-" + str(obj.N_Agujeros_Y1) + "x" + str(obj.N_Agujeros_X) + str(obj.N_Agujeros_Y2) + " " + str(obj.Angulo)

        P.Placement = obj.Placement
        obj.Shape = P
 
class STR_BXS_ESS_H:
    ''' Viga hueca Stemfie '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros","Valores Pieza","Nº Agujeros \nMínimo = 1")
        obj.N_Agujeros = 1
     
    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo Valores
        if (obj.N_Agujeros < 1): obj.N_Agujeros = 1

        # Genero el cuerpo exterior
        P = Part.makeBox(obj.N_Agujeros*12.5,12.5,12.5,FreeCAD.Vector(0,-6.25,-6.25),FreeCAD.Vector(0,0,1))
        
        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        Cubo = Part.makeBox(((obj.N_Agujeros-1)*12.5)+6.25,9.375,20,FreeCAD.Vector(3.125,-4.6875,-10),FreeCAD.Vector(0,0,1))
        P = P.cut (Cubo)
        #  ---- Agujero
        Agujero = Part.makeCylinder(3.5, (obj.N_Agujeros*12.5)+20, FreeCAD.Vector( -10, 0, 0), FreeCAD.Vector(1, 0, 0))
        P = P.cut (Agujero)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR_BXS_ESS_H-" + str(obj.N_Agujeros)

        P.Placement = obj.Placement
        obj.Shape = P
 
class STR_BXS_ESS_C:
    ''' Viga hueca Stemfie con dado en los extremos'''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        obj.addProperty("App::PropertyInteger","N_Agujeros","Valores Pieza","Nº Agujeros \nMínimo = 3")
        obj.N_Agujeros = 3
     

    def execute(self,obj):
        import Part,FreeCAD

        # Compruebo Valores
        if (obj.N_Agujeros < 3): obj.N_Agujeros = 3

        # Genero el cuerpo exterior
        P = Part.makeBox(obj.N_Agujeros*12.5,12.5,12.5,FreeCAD.Vector(0,-6.25,-6.25),FreeCAD.Vector(0,0,1))
        
        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        Cubo = Part.makeBox(((obj.N_Agujeros-2)*12.5),9.375,20,FreeCAD.Vector(12.5,-4.6875,-10),FreeCAD.Vector(0,0,1))
        P = P.cut (Cubo)
        #  ---- Agujero Longitudinal
        Agujero = Part.makeCylinder(3.5, (obj.N_Agujeros*12.5)+20, FreeCAD.Vector( -10, 0, 0), FreeCAD.Vector(1, 0, 0))
        P = P.cut (Agujero)
        #  ---- Agujero Cubo Inicio cara X
        Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( 6.25, -10, 0), FreeCAD.Vector(0, 1, 0))
        P = P.cut (Agujero)
        #  ---- Agujero Cubo Final cara X
        Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector(((obj.N_Agujeros-1)*12.5)+6.25, -10, 0), FreeCAD.Vector(0, 1, 0))
        P = P.cut (Agujero)
        #  ---- Agujero Cubo Inicio cara Z
        Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector( 6.25, 0, -10), FreeCAD.Vector(0, 0, 1))
        P = P.cut (Agujero)
        #  ---- Agujero Cubo Final cara Z
        Agujero = Part.makeCylinder(3.5, 20, FreeCAD.Vector(((obj.N_Agujeros-1)*12.5)+6.25, 0, -10), FreeCAD.Vector(0, 0, 1))
        P = P.cut (Agujero)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "STR_BXS_ESS_C-" + str(obj.N_Agujeros)

        P.Placement = obj.Placement
        obj.Shape = P
 
# Conectores
class THR_H_BEM_SFT_1W:
    ''' Conector en 1 cara Stemfie '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        

    def execute(self,obj):
        import Part,FreeCAD

        # Genero el cuerpo exterior
        P = Part.makeBox(15.625,15.625,12.5,FreeCAD.Vector(-7.8125,-7.8125,-6.25),FreeCAD.Vector(0,0,1))
        
        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        Cubo = Part.makeBox(12.9,12.9,20,FreeCAD.Vector(-6.45,-6.45,-10),FreeCAD.Vector(0,0,1))
        P = P.cut (Cubo)

        #  Genero el Cono
        #  Nombro Variables para Facilitar codigo
        LadoG = 4.9291
        EntreCarasG = 11.9
        LadoP = 3.7279
        EntreCarasP = 9
        Altura = 4.6875
        #  Puntos Poligono Grande
        PG1 = FreeCAD.Vector(EntreCarasG/2,LadoG/2,0)
        PG2 = FreeCAD.Vector(LadoG/2,EntreCarasG/2,0)
        PG3 = FreeCAD.Vector(-LadoG/2,EntreCarasG/2,0)
        PG4 = FreeCAD.Vector(-EntreCarasG/2,LadoG/2,0)
        PG5 = FreeCAD.Vector(-EntreCarasG/2,-LadoG/2,0)
        PG6 = FreeCAD.Vector(-LadoG/2,-EntreCarasG/2,0)
        PG7 = FreeCAD.Vector(LadoG/2,-EntreCarasG/2,0)
        PG8 = FreeCAD.Vector(EntreCarasG/2,-LadoG/2,0)
        #  Puntos Poligono Pequeño
        PP1 = FreeCAD.Vector(EntreCarasP/2,LadoP/2,Altura)
        PP2 = FreeCAD.Vector(LadoP/2,EntreCarasP/2,Altura)
        PP3 = FreeCAD.Vector(-LadoP/2,EntreCarasP/2,Altura)
        PP4 = FreeCAD.Vector(-EntreCarasP/2,LadoP/2,Altura)
        PP5 = FreeCAD.Vector(-EntreCarasP/2,-LadoP/2,Altura)
        PP6 = FreeCAD.Vector(-LadoP/2,-EntreCarasP/2,Altura)
        PP7 = FreeCAD.Vector(LadoP/2,-EntreCarasP/2,Altura)
        PP8 = FreeCAD.Vector(EntreCarasP/2,-LadoP/2,Altura)
        #  ---- Creamos lineas Poligono Grande
        LPG1 = Part.LineSegment(PG1,PG2)
        LPG2 = Part.LineSegment(PG2,PG3)
        LPG3 = Part.LineSegment(PG3,PG4)
        LPG4 = Part.LineSegment(PG4,PG5)
        LPG5 = Part.LineSegment(PG5,PG6)
        LPG6 = Part.LineSegment(PG6,PG7)
        LPG7 = Part.LineSegment(PG7,PG8)
        LPG8 = Part.LineSegment(PG8,PG1)
        #  ---- Creamos Cara Poligono Grande
        SG = Part.Shape([LPG1,LPG2,LPG3,LPG4,LPG5,LPG6,LPG7,LPG8])
        WG = Part.Wire(SG.Edges)
        FG = Part.Face(WG)
        #  ---- Creamos lineas Poligono Pequeño
        LPP1 = Part.LineSegment(PP1,PP2)
        LPP2 = Part.LineSegment(PP2,PP3)
        LPP3 = Part.LineSegment(PP3,PP4)
        LPP4 = Part.LineSegment(PP4,PP5)
        LPP5 = Part.LineSegment(PP5,PP6)
        LPP6 = Part.LineSegment(PP6,PP7)
        LPP7 = Part.LineSegment(PP7,PP8)
        LPP8 = Part.LineSegment(PP8,PP1)
        #  ---- Creamos Cara Poligono Pequeño
        SP = Part.Shape([LPP1,LPP2,LPP3,LPP4,LPP5,LPP6,LPP7,LPP8])
        WP = Part.Wire(SP.Edges)
        FP = Part.Face(WP)
        #  ---- Creamos lineas Caras inclinadas
        LIncl1 = Part.LineSegment(PG1,PP1)
        LIncl2 = Part.LineSegment(PG2,PP2)
        LIncl3 = Part.LineSegment(PG3,PP3)
        LIncl4 = Part.LineSegment(PG4,PP4)
        LIncl5 = Part.LineSegment(PG5,PP5)
        LIncl6 = Part.LineSegment(PG6,PP6)
        LIncl7 = Part.LineSegment(PG7,PP7)
        LIncl8 = Part.LineSegment(PG8,PP8)
        #  ---- Creamos Caras Inclinadas
        SIncl1 = Part.Shape([LIncl1,LPG1,LIncl2,LPP1])
        WIncl1 = Part.Wire(SIncl1.Edges)
        FIncl1 = Part.Face(WIncl1)
        SIncl2 = Part.Shape([LIncl2,LPG2,LIncl3,LPP2])
        WIncl2 = Part.Wire(SIncl2.Edges)
        FIncl2 = Part.Face(WIncl2)
        SIncl3 = Part.Shape([LIncl3,LPG3,LIncl4,LPP3])
        WIncl3 = Part.Wire(SIncl3.Edges)
        FIncl3 = Part.Face(WIncl3)
        SIncl4 = Part.Shape([LIncl4,LPG4,LIncl5,LPP4])
        WIncl4 = Part.Wire(SIncl4.Edges)
        FIncl4 = Part.Face(WIncl4)
        SIncl5 = Part.Shape([LIncl5,LPG5,LIncl6,LPP5])
        WIncl5 = Part.Wire(SIncl5.Edges)
        FIncl5 = Part.Face(WIncl5)
        SIncl6 = Part.Shape([LIncl6,LPG6,LIncl7,LPP6])
        WIncl6 = Part.Wire(SIncl6.Edges)
        FIncl6 = Part.Face(WIncl6)
        SIncl7 = Part.Shape([LIncl7,LPG7,LIncl8,LPP7])
        WIncl7 = Part.Wire(SIncl7.Edges)
        FIncl7 = Part.Face(WIncl7)
        SIncl8 = Part.Shape([LIncl8,LPG8,LIncl1,LPP8])
        WIncl8 = Part.Wire(SIncl8.Edges)
        FIncl8 = Part.Face(WIncl8)
        ###  ----- Hacemos cuerpo Solido Cono Central
        TCono = Part.makeShell([FG,FIncl1,FIncl2,FIncl3,FIncl4,FIncl5,FIncl6,FIncl7,FIncl8,FP])
        #   ----  Junto las caras
        Cono = Part.makeSolid(TCono)
        #   ----  Genero agujeritos de r=1
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(-10, 0, 1.5675), FreeCAD.Vector(1, 0, 0))
        Cono = Cono.cut (Agujero)
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(0, -10, 1.5675), FreeCAD.Vector(0, 1, 0))
        Cono = Cono.cut (Agujero)
        #   ----  muevo el cono a la cara
        Cono.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),90)
        Cono.translate(FreeCAD.Vector(7.8125,0,0))
        #   ----  Unimos cono al cuerpo
        P = P.fuse(Cono)
        ###  ---- Hago los Agujeros
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(0, -15, 0), FreeCAD.Vector(0, 1, 0))
        P = P.cut (Agujero)
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(-15, 0, 0), FreeCAD.Vector(1, 0, 0))
        P = P.cut (Agujero)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "THR_H_BEM_SFT_1W"

        P.Placement = obj.Placement
        obj.Shape = P

class THR_H_BEM_SFT_2W_180:
    ''' Conector en 2 caras opuestas Stemfie '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        
    def execute(self,obj):
        import Part,FreeCAD

        # Genero el cuerpo exterior
        P = Part.makeBox(15.625,15.625,12.5,FreeCAD.Vector(-7.8125,-7.8125,-6.25),FreeCAD.Vector(0,0,1))
        
        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        Cubo = Part.makeBox(12.9,12.9,20,FreeCAD.Vector(-6.45,-6.45,-10),FreeCAD.Vector(0,0,1))
        P = P.cut (Cubo)

        #  Genero el Cono
        #  Nombro Variables para Facilitar codigo
        LadoG = 4.9291
        EntreCarasG = 11.9
        LadoP = 3.7279
        EntreCarasP = 9
        Altura = 4.6875
        #  Puntos Poligono Grande
        PG1 = FreeCAD.Vector(EntreCarasG/2,LadoG/2,0)
        PG2 = FreeCAD.Vector(LadoG/2,EntreCarasG/2,0)
        PG3 = FreeCAD.Vector(-LadoG/2,EntreCarasG/2,0)
        PG4 = FreeCAD.Vector(-EntreCarasG/2,LadoG/2,0)
        PG5 = FreeCAD.Vector(-EntreCarasG/2,-LadoG/2,0)
        PG6 = FreeCAD.Vector(-LadoG/2,-EntreCarasG/2,0)
        PG7 = FreeCAD.Vector(LadoG/2,-EntreCarasG/2,0)
        PG8 = FreeCAD.Vector(EntreCarasG/2,-LadoG/2,0)
        #  Puntos Poligono Pequeño
        PP1 = FreeCAD.Vector(EntreCarasP/2,LadoP/2,Altura)
        PP2 = FreeCAD.Vector(LadoP/2,EntreCarasP/2,Altura)
        PP3 = FreeCAD.Vector(-LadoP/2,EntreCarasP/2,Altura)
        PP4 = FreeCAD.Vector(-EntreCarasP/2,LadoP/2,Altura)
        PP5 = FreeCAD.Vector(-EntreCarasP/2,-LadoP/2,Altura)
        PP6 = FreeCAD.Vector(-LadoP/2,-EntreCarasP/2,Altura)
        PP7 = FreeCAD.Vector(LadoP/2,-EntreCarasP/2,Altura)
        PP8 = FreeCAD.Vector(EntreCarasP/2,-LadoP/2,Altura)
        #  ---- Creamos lineas Poligono Grande
        LPG1 = Part.LineSegment(PG1,PG2)
        LPG2 = Part.LineSegment(PG2,PG3)
        LPG3 = Part.LineSegment(PG3,PG4)
        LPG4 = Part.LineSegment(PG4,PG5)
        LPG5 = Part.LineSegment(PG5,PG6)
        LPG6 = Part.LineSegment(PG6,PG7)
        LPG7 = Part.LineSegment(PG7,PG8)
        LPG8 = Part.LineSegment(PG8,PG1)
        #  ---- Creamos Cara Poligono Grande
        SG = Part.Shape([LPG1,LPG2,LPG3,LPG4,LPG5,LPG6,LPG7,LPG8])
        WG = Part.Wire(SG.Edges)
        FG = Part.Face(WG)
        #  ---- Creamos lineas Poligono Pequeño
        LPP1 = Part.LineSegment(PP1,PP2)
        LPP2 = Part.LineSegment(PP2,PP3)
        LPP3 = Part.LineSegment(PP3,PP4)
        LPP4 = Part.LineSegment(PP4,PP5)
        LPP5 = Part.LineSegment(PP5,PP6)
        LPP6 = Part.LineSegment(PP6,PP7)
        LPP7 = Part.LineSegment(PP7,PP8)
        LPP8 = Part.LineSegment(PP8,PP1)
        #  ---- Creamos Cara Poligono Pequeño
        SP = Part.Shape([LPP1,LPP2,LPP3,LPP4,LPP5,LPP6,LPP7,LPP8])
        WP = Part.Wire(SP.Edges)
        FP = Part.Face(WP)
        #  ---- Creamos lineas Caras inclinadas
        LIncl1 = Part.LineSegment(PG1,PP1)
        LIncl2 = Part.LineSegment(PG2,PP2)
        LIncl3 = Part.LineSegment(PG3,PP3)
        LIncl4 = Part.LineSegment(PG4,PP4)
        LIncl5 = Part.LineSegment(PG5,PP5)
        LIncl6 = Part.LineSegment(PG6,PP6)
        LIncl7 = Part.LineSegment(PG7,PP7)
        LIncl8 = Part.LineSegment(PG8,PP8)
        #  ---- Creamos Caras Inclinadas
        SIncl1 = Part.Shape([LIncl1,LPG1,LIncl2,LPP1])
        WIncl1 = Part.Wire(SIncl1.Edges)
        FIncl1 = Part.Face(WIncl1)
        SIncl2 = Part.Shape([LIncl2,LPG2,LIncl3,LPP2])
        WIncl2 = Part.Wire(SIncl2.Edges)
        FIncl2 = Part.Face(WIncl2)
        SIncl3 = Part.Shape([LIncl3,LPG3,LIncl4,LPP3])
        WIncl3 = Part.Wire(SIncl3.Edges)
        FIncl3 = Part.Face(WIncl3)
        SIncl4 = Part.Shape([LIncl4,LPG4,LIncl5,LPP4])
        WIncl4 = Part.Wire(SIncl4.Edges)
        FIncl4 = Part.Face(WIncl4)
        SIncl5 = Part.Shape([LIncl5,LPG5,LIncl6,LPP5])
        WIncl5 = Part.Wire(SIncl5.Edges)
        FIncl5 = Part.Face(WIncl5)
        SIncl6 = Part.Shape([LIncl6,LPG6,LIncl7,LPP6])
        WIncl6 = Part.Wire(SIncl6.Edges)
        FIncl6 = Part.Face(WIncl6)
        SIncl7 = Part.Shape([LIncl7,LPG7,LIncl8,LPP7])
        WIncl7 = Part.Wire(SIncl7.Edges)
        FIncl7 = Part.Face(WIncl7)
        SIncl8 = Part.Shape([LIncl8,LPG8,LIncl1,LPP8])
        WIncl8 = Part.Wire(SIncl8.Edges)
        FIncl8 = Part.Face(WIncl8)
        #   ----  Junto las caras
        TCono = Part.makeShell([FG,FIncl1,FIncl2,FIncl3,FIncl4,FIncl5,FIncl6,FIncl7,FIncl8,FP])
        #   ----  Hacemos 2 Conos Solidos con las caras
        Cono1 = Part.makeSolid(TCono)
        Cono2 = Part.makeSolid(TCono)
        #   ----  Genero agujeritos de r=1
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(-10, 0, 1.5675), FreeCAD.Vector(1, 0, 0))
        Cono1 = Cono1.cut(Agujero)
        Cono2 = Cono2.cut(Agujero)
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(0, -10, 1.5675), FreeCAD.Vector(0, 1, 0))
        Cono1 = Cono1.cut (Agujero)
        Cono2 = Cono2.cut(Agujero)
        #   ----  muevo el cono1 a la cara
        Cono1.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),90)
        Cono1.translate(FreeCAD.Vector(7.8125,0,0))
        #   ----  muevo el cono2 a la cara
        Cono2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),-90)
        Cono2.translate(FreeCAD.Vector(-7.8125,0,0))
        #   ----  Unimos conos al cuerpo
        P = P.fuse(Cono1)
        P = P.fuse(Cono2)
        ###  ---- Hago los Agujeros centrales
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(0, -15, 0), FreeCAD.Vector(0, 1, 0))
        P = P.cut (Agujero)
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(-15, 0, 0), FreeCAD.Vector(1, 0, 0))
        P = P.cut (Agujero)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "THR_H_BEM_SFT_2W_180"

        P.Placement = obj.Placement
        obj.Shape = P

class THR_H_BEM_SFT_2W_90:
    ''' Conector en 2 caras contiguas Stemfie '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        
    def execute(self,obj):
        import Part,FreeCAD

        # Genero el cuerpo exterior
        P = Part.makeBox(15.625,15.625,12.5,FreeCAD.Vector(-7.8125,-7.8125,-6.25),FreeCAD.Vector(0,0,1))
        
        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        Cubo = Part.makeBox(12.9,12.9,20,FreeCAD.Vector(-6.45,-6.45,-10),FreeCAD.Vector(0,0,1))
        P = P.cut (Cubo)

        #  Genero el Cono
        #  Nombro Variables para Facilitar codigo
        LadoG = 4.9291
        EntreCarasG = 11.9
        LadoP = 3.7279
        EntreCarasP = 9
        Altura = 4.6875
        #  Puntos Poligono Grande
        PG1 = FreeCAD.Vector(EntreCarasG/2,LadoG/2,0)
        PG2 = FreeCAD.Vector(LadoG/2,EntreCarasG/2,0)
        PG3 = FreeCAD.Vector(-LadoG/2,EntreCarasG/2,0)
        PG4 = FreeCAD.Vector(-EntreCarasG/2,LadoG/2,0)
        PG5 = FreeCAD.Vector(-EntreCarasG/2,-LadoG/2,0)
        PG6 = FreeCAD.Vector(-LadoG/2,-EntreCarasG/2,0)
        PG7 = FreeCAD.Vector(LadoG/2,-EntreCarasG/2,0)
        PG8 = FreeCAD.Vector(EntreCarasG/2,-LadoG/2,0)
        #  Puntos Poligono Pequeño
        PP1 = FreeCAD.Vector(EntreCarasP/2,LadoP/2,Altura)
        PP2 = FreeCAD.Vector(LadoP/2,EntreCarasP/2,Altura)
        PP3 = FreeCAD.Vector(-LadoP/2,EntreCarasP/2,Altura)
        PP4 = FreeCAD.Vector(-EntreCarasP/2,LadoP/2,Altura)
        PP5 = FreeCAD.Vector(-EntreCarasP/2,-LadoP/2,Altura)
        PP6 = FreeCAD.Vector(-LadoP/2,-EntreCarasP/2,Altura)
        PP7 = FreeCAD.Vector(LadoP/2,-EntreCarasP/2,Altura)
        PP8 = FreeCAD.Vector(EntreCarasP/2,-LadoP/2,Altura)
        #  ---- Creamos lineas Poligono Grande
        LPG1 = Part.LineSegment(PG1,PG2)
        LPG2 = Part.LineSegment(PG2,PG3)
        LPG3 = Part.LineSegment(PG3,PG4)
        LPG4 = Part.LineSegment(PG4,PG5)
        LPG5 = Part.LineSegment(PG5,PG6)
        LPG6 = Part.LineSegment(PG6,PG7)
        LPG7 = Part.LineSegment(PG7,PG8)
        LPG8 = Part.LineSegment(PG8,PG1)
        #  ---- Creamos Cara Poligono Grande
        SG = Part.Shape([LPG1,LPG2,LPG3,LPG4,LPG5,LPG6,LPG7,LPG8])
        WG = Part.Wire(SG.Edges)
        FG = Part.Face(WG)
        #  ---- Creamos lineas Poligono Pequeño
        LPP1 = Part.LineSegment(PP1,PP2)
        LPP2 = Part.LineSegment(PP2,PP3)
        LPP3 = Part.LineSegment(PP3,PP4)
        LPP4 = Part.LineSegment(PP4,PP5)
        LPP5 = Part.LineSegment(PP5,PP6)
        LPP6 = Part.LineSegment(PP6,PP7)
        LPP7 = Part.LineSegment(PP7,PP8)
        LPP8 = Part.LineSegment(PP8,PP1)
        #  ---- Creamos Cara Poligono Pequeño
        SP = Part.Shape([LPP1,LPP2,LPP3,LPP4,LPP5,LPP6,LPP7,LPP8])
        WP = Part.Wire(SP.Edges)
        FP = Part.Face(WP)
        #  ---- Creamos lineas Caras inclinadas
        LIncl1 = Part.LineSegment(PG1,PP1)
        LIncl2 = Part.LineSegment(PG2,PP2)
        LIncl3 = Part.LineSegment(PG3,PP3)
        LIncl4 = Part.LineSegment(PG4,PP4)
        LIncl5 = Part.LineSegment(PG5,PP5)
        LIncl6 = Part.LineSegment(PG6,PP6)
        LIncl7 = Part.LineSegment(PG7,PP7)
        LIncl8 = Part.LineSegment(PG8,PP8)
        #  ---- Creamos Caras Inclinadas
        SIncl1 = Part.Shape([LIncl1,LPG1,LIncl2,LPP1])
        WIncl1 = Part.Wire(SIncl1.Edges)
        FIncl1 = Part.Face(WIncl1)
        SIncl2 = Part.Shape([LIncl2,LPG2,LIncl3,LPP2])
        WIncl2 = Part.Wire(SIncl2.Edges)
        FIncl2 = Part.Face(WIncl2)
        SIncl3 = Part.Shape([LIncl3,LPG3,LIncl4,LPP3])
        WIncl3 = Part.Wire(SIncl3.Edges)
        FIncl3 = Part.Face(WIncl3)
        SIncl4 = Part.Shape([LIncl4,LPG4,LIncl5,LPP4])
        WIncl4 = Part.Wire(SIncl4.Edges)
        FIncl4 = Part.Face(WIncl4)
        SIncl5 = Part.Shape([LIncl5,LPG5,LIncl6,LPP5])
        WIncl5 = Part.Wire(SIncl5.Edges)
        FIncl5 = Part.Face(WIncl5)
        SIncl6 = Part.Shape([LIncl6,LPG6,LIncl7,LPP6])
        WIncl6 = Part.Wire(SIncl6.Edges)
        FIncl6 = Part.Face(WIncl6)
        SIncl7 = Part.Shape([LIncl7,LPG7,LIncl8,LPP7])
        WIncl7 = Part.Wire(SIncl7.Edges)
        FIncl7 = Part.Face(WIncl7)
        SIncl8 = Part.Shape([LIncl8,LPG8,LIncl1,LPP8])
        WIncl8 = Part.Wire(SIncl8.Edges)
        FIncl8 = Part.Face(WIncl8)
        #   ----  Junto las caras
        TCono = Part.makeShell([FG,FIncl1,FIncl2,FIncl3,FIncl4,FIncl5,FIncl6,FIncl7,FIncl8,FP])
        #   ----  Hacemos 2 Conos Solidos con las caras
        Cono1 = Part.makeSolid(TCono)
        Cono2 = Part.makeSolid(TCono)
        #   ----  Genero agujeritos de r=1
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(-10, 0, 1.5675), FreeCAD.Vector(1, 0, 0))
        Cono1 = Cono1.cut(Agujero)
        Cono2 = Cono2.cut(Agujero)
        Agujero = Part.makeCylinder(1, 20, FreeCAD.Vector(0, -10, 1.5675), FreeCAD.Vector(0, 1, 0))
        Cono1 = Cono1.cut (Agujero)
        Cono2 = Cono2.cut(Agujero)
        #   ----  muevo el cono1 a la cara
        Cono1.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),90)
        Cono1.translate(FreeCAD.Vector(7.8125,0,0))
        #   ----  muevo el cono2 a la cara
        Cono2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0),-90)
        Cono2.translate(FreeCAD.Vector(0,7.8125,0))
        #   ----  Unimos conos al cuerpo
        P = P.fuse(Cono1)
        P = P.fuse(Cono2)
        ###  ---- Hago los Agujeros centrales
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(0, -15, 0), FreeCAD.Vector(0, 1, 0))
        P = P.cut (Agujero)
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(-15, 0, 0), FreeCAD.Vector(1, 0, 0))
        P = P.cut (Agujero)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "THR_H_BEM_SFT_2W_90"

        P.Placement = obj.Placement
        obj.Shape = P

class THR_H_BEM_SFT_3W:
    ''' Conector en 3 caras contiguas Stemfie '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        
    def execute(self,obj):
        import Part,FreeCAD

        # Genero el cuerpo exterior
        P = Part.makeBox(15.625,15.625,12.5,FreeCAD.Vector(-7.8125,-7.8125,-6.25),FreeCAD.Vector(0,0,1))
        
        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        Cubo = Part.makeBox(12.9,12.9,20,FreeCAD.Vector(-6.45,-6.45,-10),FreeCAD.Vector(0,0,1))
        P = P.cut (Cubo)

        #  Genero el Cono
        #  Nombro Variables para Facilitar codigo
        LadoG = 4.9291
        EntreCarasG = 11.9
        LadoP = 3.7279
        EntreCarasP = 9
        Altura = 4.6875
        #  Puntos Poligono Grande
        PG1 = FreeCAD.Vector(EntreCarasG/2,LadoG/2,0)
        PG2 = FreeCAD.Vector(LadoG/2,EntreCarasG/2,0)
        PG3 = FreeCAD.Vector(-LadoG/2,EntreCarasG/2,0)
        PG4 = FreeCAD.Vector(-EntreCarasG/2,LadoG/2,0)
        PG5 = FreeCAD.Vector(-EntreCarasG/2,-LadoG/2,0)
        PG6 = FreeCAD.Vector(-LadoG/2,-EntreCarasG/2,0)
        PG7 = FreeCAD.Vector(LadoG/2,-EntreCarasG/2,0)
        PG8 = FreeCAD.Vector(EntreCarasG/2,-LadoG/2,0)
        #  Puntos Poligono Pequeño
        PP1 = FreeCAD.Vector(EntreCarasP/2,LadoP/2,Altura)
        PP2 = FreeCAD.Vector(LadoP/2,EntreCarasP/2,Altura)
        PP3 = FreeCAD.Vector(-LadoP/2,EntreCarasP/2,Altura)
        PP4 = FreeCAD.Vector(-EntreCarasP/2,LadoP/2,Altura)
        PP5 = FreeCAD.Vector(-EntreCarasP/2,-LadoP/2,Altura)
        PP6 = FreeCAD.Vector(-LadoP/2,-EntreCarasP/2,Altura)
        PP7 = FreeCAD.Vector(LadoP/2,-EntreCarasP/2,Altura)
        PP8 = FreeCAD.Vector(EntreCarasP/2,-LadoP/2,Altura)
        #  ---- Creamos lineas Poligono Grande
        LPG1 = Part.LineSegment(PG1,PG2)
        LPG2 = Part.LineSegment(PG2,PG3)
        LPG3 = Part.LineSegment(PG3,PG4)
        LPG4 = Part.LineSegment(PG4,PG5)
        LPG5 = Part.LineSegment(PG5,PG6)
        LPG6 = Part.LineSegment(PG6,PG7)
        LPG7 = Part.LineSegment(PG7,PG8)
        LPG8 = Part.LineSegment(PG8,PG1)
        #  ---- Creamos Cara Poligono Grande
        SG = Part.Shape([LPG1,LPG2,LPG3,LPG4,LPG5,LPG6,LPG7,LPG8])
        WG = Part.Wire(SG.Edges)
        FG = Part.Face(WG)
        #  ---- Creamos lineas Poligono Pequeño
        LPP1 = Part.LineSegment(PP1,PP2)
        LPP2 = Part.LineSegment(PP2,PP3)
        LPP3 = Part.LineSegment(PP3,PP4)
        LPP4 = Part.LineSegment(PP4,PP5)
        LPP5 = Part.LineSegment(PP5,PP6)
        LPP6 = Part.LineSegment(PP6,PP7)
        LPP7 = Part.LineSegment(PP7,PP8)
        LPP8 = Part.LineSegment(PP8,PP1)
        #  ---- Creamos Cara Poligono Pequeño
        SP = Part.Shape([LPP1,LPP2,LPP3,LPP4,LPP5,LPP6,LPP7,LPP8])
        WP = Part.Wire(SP.Edges)
        FP = Part.Face(WP)
        #  ---- Creamos lineas Caras inclinadas
        LIncl1 = Part.LineSegment(PG1,PP1)
        LIncl2 = Part.LineSegment(PG2,PP2)
        LIncl3 = Part.LineSegment(PG3,PP3)
        LIncl4 = Part.LineSegment(PG4,PP4)
        LIncl5 = Part.LineSegment(PG5,PP5)
        LIncl6 = Part.LineSegment(PG6,PP6)
        LIncl7 = Part.LineSegment(PG7,PP7)
        LIncl8 = Part.LineSegment(PG8,PP8)
        #  ---- Creamos Caras Inclinadas
        SIncl1 = Part.Shape([LIncl1,LPG1,LIncl2,LPP1])
        WIncl1 = Part.Wire(SIncl1.Edges)
        FIncl1 = Part.Face(WIncl1)
        SIncl2 = Part.Shape([LIncl2,LPG2,LIncl3,LPP2])
        WIncl2 = Part.Wire(SIncl2.Edges)
        FIncl2 = Part.Face(WIncl2)
        SIncl3 = Part.Shape([LIncl3,LPG3,LIncl4,LPP3])
        WIncl3 = Part.Wire(SIncl3.Edges)
        FIncl3 = Part.Face(WIncl3)
        SIncl4 = Part.Shape([LIncl4,LPG4,LIncl5,LPP4])
        WIncl4 = Part.Wire(SIncl4.Edges)
        FIncl4 = Part.Face(WIncl4)
        SIncl5 = Part.Shape([LIncl5,LPG5,LIncl6,LPP5])
        WIncl5 = Part.Wire(SIncl5.Edges)
        FIncl5 = Part.Face(WIncl5)
        SIncl6 = Part.Shape([LIncl6,LPG6,LIncl7,LPP6])
        WIncl6 = Part.Wire(SIncl6.Edges)
        FIncl6 = Part.Face(WIncl6)
        SIncl7 = Part.Shape([LIncl7,LPG7,LIncl8,LPP7])
        WIncl7 = Part.Wire(SIncl7.Edges)
        FIncl7 = Part.Face(WIncl7)
        SIncl8 = Part.Shape([LIncl8,LPG8,LIncl1,LPP8])
        WIncl8 = Part.Wire(SIncl8.Edges)
        FIncl8 = Part.Face(WIncl8)
        #   ----  Junto las caras
        TCono = Part.makeShell([FG,FIncl1,FIncl2,FIncl3,FIncl4,FIncl5,FIncl6,FIncl7,FIncl8,FP])
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
        Cono1.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),90)
        Cono1.translate(FreeCAD.Vector(7.8125,0,0))
        #   ----  muevo el cono2 a la cara
        Cono2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0),-90)
        Cono2.translate(FreeCAD.Vector(0,7.8125,0))
        #   ----  muevo el cono3 a la cara
        Cono3.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),-90)
        Cono3.translate(FreeCAD.Vector(-7.8125,0,0))
        #   ----  Unimos conos al cuerpo
        P = P.fuse(Cono1)
        P = P.fuse(Cono2)
        P = P.fuse(Cono3)
        ###  ---- Hago los Agujeros centrales
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(0, -15, 0), FreeCAD.Vector(0, 1, 0))
        P = P.cut (Agujero)
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(-15, 0, 0), FreeCAD.Vector(1, 0, 0))
        P = P.cut (Agujero)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "THR_H_BEM_SFT_3W"

        P.Placement = obj.Placement
        obj.Shape = P

class THR_H_BEM_SFT_4W:
    ''' Conector en las 4 caras Stemfie '''

    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyString","Codigo","Denominacion","Código Pieza")
        obj.setEditorMode("Codigo", 1)
        
    def execute(self,obj):
        import Part,FreeCAD

        # Genero el cuerpo exterior
        P = Part.makeBox(15.625,15.625,12.5,FreeCAD.Vector(-7.8125,-7.8125,-6.25),FreeCAD.Vector(0,0,1))
        
        #  Genero los cuerpos para restar del cuerpo exterior
        #  ---- Cubo central
        Cubo = Part.makeBox(12.9,12.9,20,FreeCAD.Vector(-6.45,-6.45,-10),FreeCAD.Vector(0,0,1))
        P = P.cut (Cubo)

        #  Genero el Cono
        #  Nombro Variables para Facilitar codigo
        LadoG = 4.9291
        EntreCarasG = 11.9
        LadoP = 3.7279
        EntreCarasP = 9
        Altura = 4.6875
        #  Puntos Poligono Grande
        PG1 = FreeCAD.Vector(EntreCarasG/2,LadoG/2,0)
        PG2 = FreeCAD.Vector(LadoG/2,EntreCarasG/2,0)
        PG3 = FreeCAD.Vector(-LadoG/2,EntreCarasG/2,0)
        PG4 = FreeCAD.Vector(-EntreCarasG/2,LadoG/2,0)
        PG5 = FreeCAD.Vector(-EntreCarasG/2,-LadoG/2,0)
        PG6 = FreeCAD.Vector(-LadoG/2,-EntreCarasG/2,0)
        PG7 = FreeCAD.Vector(LadoG/2,-EntreCarasG/2,0)
        PG8 = FreeCAD.Vector(EntreCarasG/2,-LadoG/2,0)
        #  Puntos Poligono Pequeño
        PP1 = FreeCAD.Vector(EntreCarasP/2,LadoP/2,Altura)
        PP2 = FreeCAD.Vector(LadoP/2,EntreCarasP/2,Altura)
        PP3 = FreeCAD.Vector(-LadoP/2,EntreCarasP/2,Altura)
        PP4 = FreeCAD.Vector(-EntreCarasP/2,LadoP/2,Altura)
        PP5 = FreeCAD.Vector(-EntreCarasP/2,-LadoP/2,Altura)
        PP6 = FreeCAD.Vector(-LadoP/2,-EntreCarasP/2,Altura)
        PP7 = FreeCAD.Vector(LadoP/2,-EntreCarasP/2,Altura)
        PP8 = FreeCAD.Vector(EntreCarasP/2,-LadoP/2,Altura)
        #  ---- Creamos lineas Poligono Grande
        LPG1 = Part.LineSegment(PG1,PG2)
        LPG2 = Part.LineSegment(PG2,PG3)
        LPG3 = Part.LineSegment(PG3,PG4)
        LPG4 = Part.LineSegment(PG4,PG5)
        LPG5 = Part.LineSegment(PG5,PG6)
        LPG6 = Part.LineSegment(PG6,PG7)
        LPG7 = Part.LineSegment(PG7,PG8)
        LPG8 = Part.LineSegment(PG8,PG1)
        #  ---- Creamos Cara Poligono Grande
        SG = Part.Shape([LPG1,LPG2,LPG3,LPG4,LPG5,LPG6,LPG7,LPG8])
        WG = Part.Wire(SG.Edges)
        FG = Part.Face(WG)
        #  ---- Creamos lineas Poligono Pequeño
        LPP1 = Part.LineSegment(PP1,PP2)
        LPP2 = Part.LineSegment(PP2,PP3)
        LPP3 = Part.LineSegment(PP3,PP4)
        LPP4 = Part.LineSegment(PP4,PP5)
        LPP5 = Part.LineSegment(PP5,PP6)
        LPP6 = Part.LineSegment(PP6,PP7)
        LPP7 = Part.LineSegment(PP7,PP8)
        LPP8 = Part.LineSegment(PP8,PP1)
        #  ---- Creamos Cara Poligono Pequeño
        SP = Part.Shape([LPP1,LPP2,LPP3,LPP4,LPP5,LPP6,LPP7,LPP8])
        WP = Part.Wire(SP.Edges)
        FP = Part.Face(WP)
        #  ---- Creamos lineas Caras inclinadas
        LIncl1 = Part.LineSegment(PG1,PP1)
        LIncl2 = Part.LineSegment(PG2,PP2)
        LIncl3 = Part.LineSegment(PG3,PP3)
        LIncl4 = Part.LineSegment(PG4,PP4)
        LIncl5 = Part.LineSegment(PG5,PP5)
        LIncl6 = Part.LineSegment(PG6,PP6)
        LIncl7 = Part.LineSegment(PG7,PP7)
        LIncl8 = Part.LineSegment(PG8,PP8)
        #  ---- Creamos Caras Inclinadas
        SIncl1 = Part.Shape([LIncl1,LPG1,LIncl2,LPP1])
        WIncl1 = Part.Wire(SIncl1.Edges)
        FIncl1 = Part.Face(WIncl1)
        SIncl2 = Part.Shape([LIncl2,LPG2,LIncl3,LPP2])
        WIncl2 = Part.Wire(SIncl2.Edges)
        FIncl2 = Part.Face(WIncl2)
        SIncl3 = Part.Shape([LIncl3,LPG3,LIncl4,LPP3])
        WIncl3 = Part.Wire(SIncl3.Edges)
        FIncl3 = Part.Face(WIncl3)
        SIncl4 = Part.Shape([LIncl4,LPG4,LIncl5,LPP4])
        WIncl4 = Part.Wire(SIncl4.Edges)
        FIncl4 = Part.Face(WIncl4)
        SIncl5 = Part.Shape([LIncl5,LPG5,LIncl6,LPP5])
        WIncl5 = Part.Wire(SIncl5.Edges)
        FIncl5 = Part.Face(WIncl5)
        SIncl6 = Part.Shape([LIncl6,LPG6,LIncl7,LPP6])
        WIncl6 = Part.Wire(SIncl6.Edges)
        FIncl6 = Part.Face(WIncl6)
        SIncl7 = Part.Shape([LIncl7,LPG7,LIncl8,LPP7])
        WIncl7 = Part.Wire(SIncl7.Edges)
        FIncl7 = Part.Face(WIncl7)
        SIncl8 = Part.Shape([LIncl8,LPG8,LIncl1,LPP8])
        WIncl8 = Part.Wire(SIncl8.Edges)
        FIncl8 = Part.Face(WIncl8)
        #   ----  Junto las caras
        TCono = Part.makeShell([FG,FIncl1,FIncl2,FIncl3,FIncl4,FIncl5,FIncl6,FIncl7,FIncl8,FP])
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
        Cono1.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),90)
        Cono1.translate(FreeCAD.Vector(7.8125,0,0))
        #   ----  muevo el cono2 a la cara
        Cono2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0),-90)
        Cono2.translate(FreeCAD.Vector(0,7.8125,0))
        #   ----  muevo el cono3 a la cara
        Cono3.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0),-90)
        Cono3.translate(FreeCAD.Vector(-7.8125,0,0))
        #   ----  muevo el cono4 a la cara
        Cono4.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0),90)
        Cono4.translate(FreeCAD.Vector(0,-7.8125,0))
        #   ----  Unimos conos al cuerpo
        P = P.fuse(Cono1)
        P = P.fuse(Cono2)
        P = P.fuse(Cono3)
        P = P.fuse(Cono4)
        ###  ---- Hago los Agujeros centrales
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(0, -15, 0), FreeCAD.Vector(0, 1, 0))
        P = P.cut (Agujero)
        Agujero = Part.makeCylinder(3.5, 30, FreeCAD.Vector(-15, 0, 0), FreeCAD.Vector(1, 0, 0))
        P = P.cut (Agujero)
        # Refinamos el cuerpo
        P = P.removeSplitter()
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Codigo = "THR_H_BEM_SFT_4W"

        P.Placement = obj.Placement
        obj.Shape = P
