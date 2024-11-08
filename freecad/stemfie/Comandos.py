# -*- coding: utf-8 -*-
import FreeCAD

translate = FreeCAD.Qt.translate


def ListadoPiezas():
    # FreeCAD.Console.PrintMessage("Esto se ejecuta\n")
    # List all objects of the document
    objs = FreeCAD.ActiveDocument.Objects

    piezas = {}

    """
        Con Listas
  """

    # Iniciacion de Variables
    ContenedorPiezas = []
    Pieza = []
    NoEsPiezaStemfie = []
    # Bucle Lectura objetos del dibujo
    for obj in objs:
        name = str(obj.Name)
        try:
            c = str(obj.Code)
            color = str(obj.ViewObject.ShapeColor)
            Pieza = list((1, c, color))
            ContenedorPiezas.append(Pieza)

        except:
            NoEsPiezaStemfie.append(str(name))

    ContenedorPiezas.sort()  # Ordena lista

    #   ----------------
    #   Quitar repetidos
    #   ----------------
    Contador = 1
    TemporalPiezas = []
    x = 0
    for Pieza in ContenedorPiezas:
        if x == 0:
            # Primer registro
            # Añado a Lista temporal la primera pieza
            TemporalPiezas.append(Pieza)
            # Tomo el valor de la pieza para comparar con la siguiente
            TemporalPieza = Pieza
            x += 1
        else:
            if TemporalPieza == Pieza:
                Contador += 1
            else:
                # Cambiar Nº piezas en la lista Temporal
                TempPieza = TemporalPiezas[-1]
                TempPieza[0] = Contador
                L = len(TemporalPiezas)
                TemporalPiezas[L - 1] = TempPieza

                # Añado pieza diferente a la anterior a la lista
                TemporalPiezas.append(Pieza)

                # Tomo el valor de la pieza para comparar con la siguiente
                TemporalPieza = Pieza
                # reseteo contador
                Contador = 1
    if len(TemporalPiezas) == 0:
        FreeCAD.Console.PrintMessage(translate("Log", "There are no STEMFIE parts on the tree.\n"))
        return

    # Cambiar Nº piezas a la ultima pieza
    TempPieza = TemporalPiezas[-1]
    TempPieza[0] = Contador
    L = len(TemporalPiezas)
    TemporalPiezas[L - 1] = TempPieza

    # Cambio Lista original por la que no tiene piezas repetidas
    ContenedorPiezas = TemporalPiezas

    # ------------------
    # Listado a Pantalla
    # ------------------
    FreeCAD.Console.PrintMessage(
        "\t\t\t**********************************************************\n"
    )
    FreeCAD.Console.PrintMessage(translate("Log", "\t\t\t    STEMFIE PARTS LIST\n"))
    FreeCAD.Console.PrintMessage("\t\t\t---------------------------------------------------\n")
    for x in ContenedorPiezas:
        print(x)
    FreeCAD.Console.PrintMessage(
        "\t\t\t**********************************************************\n"
    )

    return
