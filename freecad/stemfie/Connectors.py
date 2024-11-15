import FreeCAD
import Part
from FreeCAD import Vector

from freecad.stemfie.utils import (
    BLOCK_UNIT,
    BLOCK_UNIT_HALF,
)


# TODO: check if it's better to reduce from 5 commands to a single one
# advantage: you can change shape on the same object
# alternative: join 5 commands in a single drop-down icon on the toolbar

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP

BU_5_QTR = (5 / 4) * BLOCK_UNIT
lado_G = 4.9291
entre_caras_G = 11.9
lado_P = 3.7279
entre_caras_P = 9
altura = 4.6875


class CONN:
    """Base class for all STEMFIE connectors."""

    def __init__(self, obj):
        """
        Initialize the connector object.

        Args:
            obj: The FreeCAD object to which this connector is attached.
        """
        obj.Proxy = self  # Stores a reference to the Python instance in the FeaturePython object
        self.connectors = []
        self.code = ""
        # to update old unconstrained  property
        if hasattr(obj, "Code"):
            obj.removeProperty("Code")
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

    def create_cube(self) -> Part.Shape:
        """Create a cube shape with an internal hole for the connector base."""
        cube = Part.makeBox(
            BU_5_QTR,
            BU_5_QTR,
            BLOCK_UNIT,
            Vector(-BU_5_QTR / 2, -BU_5_QTR / 2, -BLOCK_UNIT_HALF),
            Vector(0, 0, 1),
        )

        # Generate the bodies to subtract from the outer body
        # ---- Central cube
        cube = cube.cut(Part.makeBox(12.9, 12.9, 20, Vector(-6.45, -6.45, -10), Vector(0, 0, 1)))
        return cube

    def create_cone(self) -> Part.Shape:
        """Create a cone shape for the connector sides."""
        # Points for the large polygon
        pg1 = Vector(entre_caras_G / 2, lado_G / 2, 0)
        pg2 = Vector(lado_G / 2, entre_caras_G / 2, 0)
        pg3 = Vector(-lado_G / 2, entre_caras_G / 2, 0)
        pg4 = Vector(-entre_caras_G / 2, lado_G / 2, 0)
        pg5 = Vector(-entre_caras_G / 2, -lado_G / 2, 0)
        pg6 = Vector(-lado_G / 2, -entre_caras_G / 2, 0)
        pg7 = Vector(lado_G / 2, -entre_caras_G / 2, 0)
        pg8 = Vector(entre_caras_G / 2, -lado_G / 2, 0)
        # Points for the small polygon
        pp1 = Vector(entre_caras_P / 2, lado_P / 2, altura)
        pp2 = Vector(lado_P / 2, entre_caras_P / 2, altura)
        pp3 = Vector(-lado_P / 2, entre_caras_P / 2, altura)
        pp4 = Vector(-entre_caras_P / 2, lado_P / 2, altura)
        pp5 = Vector(-entre_caras_P / 2, -lado_P / 2, altura)
        pp6 = Vector(-lado_P / 2, -entre_caras_P / 2, altura)
        pp7 = Vector(lado_P / 2, -entre_caras_P / 2, altura)
        pp8 = Vector(entre_caras_P / 2, -lado_P / 2, altura)
        # Create lines for the large polygon
        lpg1 = Part.LineSegment(pg1, pg2)
        lpg2 = Part.LineSegment(pg2, pg3)
        lpg3 = Part.LineSegment(pg3, pg4)
        lpg4 = Part.LineSegment(pg4, pg5)
        lpg5 = Part.LineSegment(pg5, pg6)
        lpg6 = Part.LineSegment(pg6, pg7)
        lpg7 = Part.LineSegment(pg7, pg8)
        lpg8 = Part.LineSegment(pg8, pg1)
        # Create face for the large polygon
        sg = Part.Shape([lpg1, lpg2, lpg3, lpg4, lpg5, lpg6, lpg7, lpg8])
        wg = Part.Wire(sg.Edges)
        fg = Part.Face(wg)
        # Create lines for the small polygon
        lpp1 = Part.LineSegment(pp1, pp2)
        lpp2 = Part.LineSegment(pp2, pp3)
        lpp3 = Part.LineSegment(pp3, pp4)
        lpp4 = Part.LineSegment(pp4, pp5)
        lpp5 = Part.LineSegment(pp5, pp6)
        lpp6 = Part.LineSegment(pp6, pp7)
        lpp7 = Part.LineSegment(pp7, pp8)
        lpp8 = Part.LineSegment(pp8, pp1)
        # Create face for the small polygon
        sp = Part.Shape([lpp1, lpp2, lpp3, lpp4, lpp5, lpp6, lpp7, lpp8])
        wp = Part.Wire(sp.Edges)
        fp = Part.Face(wp)
        # Create lines for the inclined faces
        lincl1 = Part.LineSegment(pg1, pp1)
        lincl2 = Part.LineSegment(pg2, pp2)
        lincl3 = Part.LineSegment(pg3, pp3)
        lincl4 = Part.LineSegment(pg4, pp4)
        lincl5 = Part.LineSegment(pg5, pp5)
        lincl6 = Part.LineSegment(pg6, pp6)
        lincl7 = Part.LineSegment(pg7, pp7)
        lincl8 = Part.LineSegment(pg8, pp8)
        # Create inclined faces
        sincl1 = Part.Shape([lincl1, lpg1, lincl2, lpp1])
        wincl1 = Part.Wire(sincl1.Edges)
        fincl1 = Part.Face(wincl1)
        sincl2 = Part.Shape([lincl2, lpg2, lincl3, lpp2])
        wincl2 = Part.Wire(sincl2.Edges)
        fincl2 = Part.Face(wincl2)
        sincl3 = Part.Shape([lincl3, lpg3, lincl4, lpp3])
        wincl3 = Part.Wire(sincl3.Edges)
        fincl3 = Part.Face(wincl3)
        sincl4 = Part.Shape([lincl4, lpg4, lincl5, lpp4])
        wincl4 = Part.Wire(sincl4.Edges)
        fincl4 = Part.Face(wincl4)
        sincl5 = Part.Shape([lincl5, lpg5, lincl6, lpp5])
        wincl5 = Part.Wire(sincl5.Edges)
        fincl5 = Part.Face(wincl5)
        sincl6 = Part.Shape([lincl6, lpg6, lincl7, lpp6])
        wincl6 = Part.Wire(sincl6.Edges)
        fincl6 = Part.Face(wincl6)
        sincl7 = Part.Shape([lincl7, lpg7, lincl8, lpp7])
        wincl7 = Part.Wire(sincl7.Edges)
        fincl7 = Part.Face(wincl7)
        sincl8 = Part.Shape([lincl8, lpg8, lincl1, lpp8])
        wincl8 = Part.Wire(sincl8.Edges)
        fincl8 = Part.Face(wincl8)
        # Create solid cone body
        t_cone = Part.makeShell(
            [fg, fincl1, fincl2, fincl3, fincl4, fincl5, fincl6, fincl7, fincl8, fp]
        )
        cone = Part.Shape(Part.makeSolid(t_cone))
        # Create small holes with radius 1
        hole = Part.makeCylinder(1, 20, Vector(-10, 0, 1.5675), Vector(1, 0, 0))
        cone = cone.cut(hole)
        hole = Part.makeCylinder(1, 20, Vector(0, -10, 1.5675), Vector(0, 1, 0))
        cone = cone.cut(hole)
        return cone

    def add_cones(self, shape: Part.Shape) -> Part.Shape:
        """Add cones to the given shape based on the connector configuration."""
        if self.connectors[0]:
            cone1 = self.create_cone()
            cone1.rotate(Vector(0, 0, 0), Vector(0, 1, 0), 90)
            cone1.translate(Vector(BU_5_QTR / 2, 0, 0))
            shape = shape.fuse(cone1)

        if self.connectors[1]:
            cone2 = self.create_cone()
            cone2.rotate(Vector(0, 0, 0), Vector(1, 0, 0), -90)
            cone2.translate(Vector(0, BU_5_QTR / 2, 0))
            shape = shape.fuse(cone2)

        if self.connectors[2]:
            cone3 = self.create_cone()
            cone3.rotate(Vector(0, 0, 0), Vector(0, 1, 0), -90)
            cone3.translate(Vector(-BU_5_QTR / 2, 0, 0))
            shape = shape.fuse(cone3)

        if self.connectors[3]:
            cone4 = self.create_cone()
            cone4.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 90)
            cone4.translate(Vector(0, -BU_5_QTR / 2, 0))
            shape = shape.fuse(cone4)

        # Create central holes
        agujero = Part.makeCylinder(3.5, 30, Vector(0, -15, 0), Vector(0, 1, 0))
        shape = shape.cut(agujero)
        agujero = Part.makeCylinder(3.5, 30, Vector(-15, 0, 0), Vector(1, 0, 0))
        shape = shape.cut(agujero)
        return shape

    def execute(self, obj):
        """
        Execute the creation of the connector shape.

        Args:
            obj: The FreeCAD object to which this connector is attached.
        """
        obj.Code = f"Connector {self.code}"
        obj.Shape = self.add_cones(self.create_cube())


class BEM_TRH_H_SFT_1W(CONN):
    """Connector on 1 face."""

    def __init__(self, obj):
        super().__init__(obj)
        self.connectors = [True, False, False, False]
        self.code = "BEM TRH-H SFT 1W"


class BEM_TRH_H_SFT_2W_90(CONN):
    """Connector on 2 contiguous faces."""

    def __init__(self, obj):
        super().__init__(obj)
        self.connectors = [True, True, False, False]
        self.code = "BEM TRH-H SFT 2W 90°"


class BEM_TRH_H_SFT_2W_180(CONN):
    """Connector on 2 opposite faces."""

    def __init__(self, obj):
        super().__init__(obj)
        self.connectors = [True, False, True, False]
        self.code = "BEM TRH-H SFT 2W 180°"


class BEM_TRH_H_SFT_3W(CONN):
    """Connector on 3 contiguous faces."""

    def __init__(self, obj):
        super().__init__(obj)
        self.connectors = [True, True, True, False]
        self.code = "BEM TRH-H SFT 3W"


class BEM_TRH_H_SFT_4W(CONN):
    """Connector on all 4 faces."""

    def __init__(self, obj):
        super().__init__(obj)
        self.connectors = [True, True, True, True]
        self.code = "BEM TRH-H SFT 4W"
