import FreeCAD
import Part
from FreeCAD import Placement, Rotation, Vector

from freecad.stemfie.utils import (
    BLOCK_UNIT,
    BLOCK_UNIT_HALF,
    BLOCK_UNIT_QUARTER,
    HOLE_DIAMETER_STANDARD,
    PLATE_BORDER_OFFSET,
    PLATE_UPPER_FACE_DIAMETER,
    PLATE_UPPER_FACE_POCKET,
    make_chamfered_hole,
    make_slot_wire_rr,
    make_rectangle_wire,
    make_slot_wire_rs,
)

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP

simple_hole = Part.makeCylinder(
    HOLE_DIAMETER_STANDARD / 2, BLOCK_UNIT, Vector(0, 0, 0), Vector(0, 0, 1)
)
chamf_hole = make_chamfered_hole(HOLE_DIAMETER_STANDARD, BLOCK_UNIT)

# NOTE: general approach is to generate the base (box) shape with no holes.
# Simples and detailed shapes are done cutting the holes one by one.

# NOTE: To avoid breaking old files in some parts of the code first is checked if property
# exists and if it does it's deleted because we migrated from "App::PropertyInteger"
# to "App::PropertyIntegerConstraint". Values of properties are reset.


class BEAM:
    def __init__(self, obj):
        obj.Proxy = self  # Stores a reference to the Python instance in the FeaturePython object
        self.wire_holes = []
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
        obj.addProperty(
            "App::PropertyBool",
            QT_TRANSLATE_NOOP("App::Property", "SimpleShape"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP(
                "App::Property",
                "Create simplified shape, holes are not chamfered and upper face is totally flush",
            ),
        ).SimpleShape = False

    def make_beam_ss_wire(self, holesX: float, holesY: float) -> Part.Wire:
        """Create beam shape, size given by number of holes"""
        return make_rectangle_wire(
            holesX * BLOCK_UNIT, holesY * BLOCK_UNIT, -BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF
        )

    def make_beam(self, holes: int = 2, ss: bool = False) -> Part.Shape:
        w = self.make_beam_ss_wire(holes, 1)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
        self.wire_holes = []
        p = Part.makeBox(
            holes * BLOCK_UNIT,
            BLOCK_UNIT,
            BLOCK_UNIT,
            Vector(-BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF),
            Vector(0, 0, 1),
        )

        p = self.make_chamfered_holes_z(p, holes, ss)
        p = self.make_chamfered_holes_y(p, holes, ss)
        p = self.make_chamfered_holes_x(p, holes, ss)

        if not ss:
            p = self.detail_face(p, inset_wire, self.wire_holes)
        return p

    def make_beam_rr_wire(self, holes_size: int = 2) -> Part.Wire:
        """Create brace shape on X axis, size given by number of holes"""
        return make_slot_wire_rr((holes_size - 1) * BLOCK_UNIT, BLOCK_UNIT_HALF)

    def make_beam_rr(self, holes: int = 2, ss: bool = False) -> Part.Shape:
        """Create brace shape on X axis, size given by number of holes"""
        w = self.make_beam_rr_wire(holes)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
        wire_holes = []
        #  ---- Creo la cara con el contorno
        f = Part.Face(w)
        #  ---- Le doy Volumen a la cara
        p = f.extrude(Vector(0, 0, BLOCK_UNIT))
        p.translate(Vector(0, 0, -BLOCK_UNIT_HALF))
        hole = simple_hole if ss else chamf_hole
        for x in range(holes):
            pos = Vector(x * BLOCK_UNIT, 0, -BLOCK_UNIT_HALF)
            pos2 = Vector(x * BLOCK_UNIT, 0, 0)
            hole.Placement = Placement(pos, Rotation())
            p = p.cut(hole)
            circle = Part.Circle(
                pos2, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
            )  # center, normal, radius
            wire_holes.append(Part.Wire(circle.toShape()))

        if not ss:
            p = self.detail_face(p, inset_wire, wire_holes)
        return p

    def make_beam_rs_wire(self, holes_size: int = 2) -> Part.Wire:
        """Create RS beam shape on X axis, size given by number of holes"""
        return make_slot_wire_rs(holes_size * BLOCK_UNIT - BLOCK_UNIT_HALF, BLOCK_UNIT_HALF)

    def make_beam_rs(self, holes: int = 2) -> Part.Shape:
        """Makes a beam with a square end and a round end"""
        #  ---- Genero Cuerpo Horizontal
        w = self.make_beam_rs_wire(holes)
        self.inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
        wire_holes = []
        #  ---- Creo la cara con el contorno
        f = Part.Face(w)
        #  ---- Le doy Volumen a la cara
        p = f.extrude(Vector(0, 0, BLOCK_UNIT))
        p.translate(Vector(0, 0, -BLOCK_UNIT_HALF))
        return p

    def detail_face(
        self, shape: Part.Shape, inset_wire: Part.Shape, wire_holes: list, face_height: int = 1
    ) -> Part.Shape:
        """
        Cut a thin slice on the upper face avoiding the holes and slots
        - shape: original shape
        - inset_wire: wire containing the shape to subtract
        - wire_holes: holes and slots to avoid cutting
        """
        inset_face = Part.Face([inset_wire] + wire_holes, "Part::FaceMakerCheese")
        inset_face.Placement = Placement(
            Vector(0, 0, face_height * BLOCK_UNIT - BLOCK_UNIT_HALF - PLATE_UPPER_FACE_POCKET),
            Rotation(),
        )
        upper_cut = inset_face.extrude((Vector(0, 0, PLATE_UPPER_FACE_POCKET)))
        return shape.cut(upper_cut)  # cut thin upper face with holes

    def make_chamfered_holes_z(
        self, p: Part.Shape, holes: int, ss: bool = False, offset: float = 0
    ) -> Part.Shape:
        """Create a set of holes parallel to Z axis."""
        hole = simple_hole if ss else chamf_hole
        for x in range(holes):
            pos = Vector(x * BLOCK_UNIT + offset, 0, -BLOCK_UNIT_HALF)
            pos2 = Vector(x * BLOCK_UNIT + offset, 0, 0)
            hole.Placement = Placement(pos, Rotation())
            p = p.cut(hole)
            circle = Part.Circle(
                pos2, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
            )  # center, normal, radius
            self.wire_holes.append(Part.Wire(circle.toShape()))
        return p

    def make_chamfered_holes_y(
        self, p: Part.Shape, holes: int, ss: bool = False, offset: float = 0
    ) -> Part.Shape:
        """Create a set of holes parallel to Y axis."""
        hole = simple_hole if ss else chamf_hole
        for x in range(holes):
            pos = Vector(x * BLOCK_UNIT + offset, BLOCK_UNIT_HALF, 0)
            hole.Placement = Placement(pos, Rotation(Vector(1, 0, 0), 90))
            p = p.cut(hole)
        return p

    def make_chamfered_holes_x(
        self, p: Part.Shape, holes: int, ss: bool = False, offset: float = 0
    ) -> Part.Shape:
        """Create a single hole parallel to X axis."""
        if ss:
            hole = Part.makeCylinder(
                3.5, (holes * BLOCK_UNIT) + 25, Vector(-10, 0, 0), Vector(1, 0, 0)
            )
        else:
            hole = make_chamfered_hole(HOLE_DIAMETER_STANDARD, holes * BLOCK_UNIT)
            hole.Placement = Placement(
                Vector(-BLOCK_UNIT_HALF + offset, 0, 0), Rotation(Vector(0, 1, 0), 90)
            )
        return p.cut(hole)


class STR_ESS(BEAM):
    """Beam - Straight - Ending Square/Square
    Viga Simple STEMFIE"""

    def __init__(self, obj):
        super().__init__(obj)
        if hasattr(obj, "HolesNumber"):
            obj.removeProperty("HolesNumber")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumber"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number for part\nMinimum = 1"),
        ).HolesNumber = (
            4,
            1,
            50,
            1,
        )  # (Default, Minimum, Maximum, Step size)

    def execute(self, obj):
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = f"Beam STR STD ESS BU{obj.HolesNumber:02}x01x01"

        obj.Shape = self.make_beam(obj.HolesNumber, obj.SimpleShape)


class STR_ERR(BEAM):
    """Beam - Straight - Ending Round/Round


    Variables:
        Codigo          'Demoninacion'
        HolesNumber      'Numero Agujeros que contiene la pieza

    """

    #       ________________
    #      /                 \
    #     |   ()    ()    ()  |
    #      \ _______________ /
    #
    #          1     2     3
    #           --------->
    #            HolesNumber

    def __init__(self, obj):
        super().__init__(obj)
        if hasattr(obj, "HolesNumber"):
            obj.removeProperty("HolesNumber")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumber"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number for simple part\nMinimum = 3"),
        ).HolesNumber = (5, 3, 50, 1)

    def execute(self, obj):
        p = self.make_beam_rr(obj.HolesNumber, obj.SimpleShape)
        p = self.make_chamfered_holes_y(p, obj.HolesNumber - 2, obj.SimpleShape, BLOCK_UNIT)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = f"Beam STR ERR BU{obj.HolesNumber}x01x00.25"

        obj.Shape = p


class STR_BEM(STR_ESS):
    """Viga Cubo STEMFIE"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumberX"):
            obj.removeProperty("HolesNumberX")
        if hasattr(obj, "HolesNumberY"):
            obj.removeProperty("HolesNumberY")
        if hasattr(obj, "HolesNumberZ"):
            obj.removeProperty("HolesNumberZ")

        obj.removeProperty("HolesNumber")
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberX"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in X\nMinimum = 1"),
        ).HolesNumberX = (2, 1, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in Y\nMinimum = 1"),
        ).HolesNumberY = (2, 1, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberZ"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in Z\nMinimum = 1"),
        ).HolesNumberZ = (2, 1, 50, 1)

    def execute(self, obj):
        w = self.make_beam_ss_wire(obj.HolesNumberX, obj.HolesNumberY)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
        self.wire_holes = []
        # Genero el cuerpo exterior
        p = Part.makeBox(
            obj.HolesNumberX * BLOCK_UNIT,
            obj.HolesNumberY * BLOCK_UNIT,
            obj.HolesNumberZ * BLOCK_UNIT,
            Vector(-BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF),
            Vector(0, 0, 1),
        )
        #  ---- Bucle X,Y para agujeros en eje Z
        for x in range(obj.HolesNumberX):
            for y in range(obj.HolesNumberY):
                h1 = Part.makeCylinder(
                    HOLE_DIAMETER_STANDARD / 2,
                    (obj.HolesNumberZ * BLOCK_UNIT) + 20,
                    Vector(x * BLOCK_UNIT, y * BLOCK_UNIT, -10),
                    Vector(0, 0, 1),
                )
                h2 = make_chamfered_hole(HOLE_DIAMETER_STANDARD, obj.HolesNumberZ * BLOCK_UNIT)
                h2.Placement = Placement(
                    Vector(x * BLOCK_UNIT, y * BLOCK_UNIT, -BLOCK_UNIT_HALF),
                    Rotation(Vector(0, 0, 1), 0),
                )
                hole = h1 if obj.SimpleShape else h2
                p = p.cut(hole)
                pos2 = Vector(x * BLOCK_UNIT, y * BLOCK_UNIT, 0)
                circle = Part.Circle(
                    pos2, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
                )  # center, normal, radius
                self.wire_holes.append(Part.Wire(circle.toShape()))

        #  ---- Bucle X,Z para agujeros en eje Y
        for x in range(obj.HolesNumberX):
            for z in range(obj.HolesNumberZ):
                h1 = Part.makeCylinder(
                    HOLE_DIAMETER_STANDARD / 2,
                    (obj.HolesNumberY * BLOCK_UNIT) + 20,
                    Vector(x * BLOCK_UNIT, -10, z * BLOCK_UNIT),
                    Vector(0, 1, 0),
                )
                h2 = make_chamfered_hole(HOLE_DIAMETER_STANDARD, obj.HolesNumberY * BLOCK_UNIT)
                h2.Placement = Placement(
                    Vector(x * BLOCK_UNIT, -BLOCK_UNIT_HALF, z * BLOCK_UNIT),
                    Rotation(Vector(1, 0, 0), -90),
                )
                hole = h1 if obj.SimpleShape else h2
                p = p.cut(hole)

        #  ---- Bucle en Y,Z par agujeros en eje X
        for z in range(obj.HolesNumberZ):
            for y in range(obj.HolesNumberY):
                h1 = Part.makeCylinder(
                    HOLE_DIAMETER_STANDARD / 2,
                    (obj.HolesNumberX * BLOCK_UNIT) + 20,
                    Vector(-BLOCK_UNIT_HALF, y * BLOCK_UNIT, z * BLOCK_UNIT),
                    Vector(1, 0, 0),
                )
                h2 = make_chamfered_hole(HOLE_DIAMETER_STANDARD, obj.HolesNumberX * BLOCK_UNIT)
                h2.Placement = Placement(
                    Vector(-BLOCK_UNIT_HALF, y * BLOCK_UNIT, z * BLOCK_UNIT),
                    Rotation(Vector(0, 1, 0), 90),
                )
                hole = h1 if obj.SimpleShape else h2
                p = p.cut(hole)

        if not obj.SimpleShape:
            p = self.detail_face(p, inset_wire, self.wire_holes, obj.HolesNumberZ)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = f"Beam STR BEM BU{obj.HolesNumberX}x{obj.HolesNumberY}x{obj.HolesNumberZ}"

        obj.Shape = p


class AGD_USH_SYM_ESS(STR_ESS):
    """Viga STEMFIE con brazos a 90º en los extremos"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumberX"):
            obj.removeProperty("HolesNumberX")
        if hasattr(obj, "HolesNumberY1"):
            obj.removeProperty("HolesNumberY1")
        if hasattr(obj, "HolesNumberY2"):
            obj.removeProperty("HolesNumberY2")

        obj.removeProperty("HolesNumber")
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberX"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number for part in X\nMinimum = 3"),
        ).HolesNumberX = (3, 3, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY1"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in left vertical bar\nMinimum = 1"),
        ).HolesNumberY1 = (2, 1, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY2"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in right vertical bar\nMinimum = 1"),
        ).HolesNumberY2 = (2, 1, 50, 1)

    def execute(self, obj):
        # Genero el cuerpo exterior

        px = self.make_beam(obj.HolesNumberX, obj.SimpleShape)
        # NOTE: beams are overlap to avoid unwanted cuts at join planes
        py1 = self.make_beam(obj.HolesNumberY1 + 1, obj.SimpleShape)
        py1.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 90)
        py2 = self.make_beam(obj.HolesNumberY2 + 1, obj.SimpleShape)
        py2.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 90)
        py2.translate(Vector((obj.HolesNumberX - 1) * BLOCK_UNIT, 0, 0))
        p = px.fuse(py1)
        p = p.fuse(py2)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        sym = "SYM" if obj.HolesNumberY1 == obj.HolesNumberY2 else "ASYM"
        obj.Code = (
            f"Beam AGD USH {sym} ESS BU{obj.HolesNumberX:02}x{obj.HolesNumberY1:02}"
            f"x{obj.HolesNumberY2:02}x01"
        )

        obj.Shape = p.removeSplitter()


class STR_DBL(BEAM):
    """Viga Angular STEMFIE"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumberX"):
            obj.removeProperty("HolesNumberX")
        if hasattr(obj, "HolesNumberY"):
            obj.removeProperty("HolesNumberY")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberX"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number for part in X\nMinimum = 2"),
        ).HolesNumberX = (3, 2, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in angular bar\nMinimum = 1"),
        ).HolesNumberY = (2, 1, 50, 1)
        if not hasattr(obj, "Angle"):
            obj.addProperty(
                "App::PropertyAngle",
                QT_TRANSLATE_NOOP("App::Property", "Angle"),
                QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
                QT_TRANSLATE_NOOP("App::Property", "Angle\nMinimum = 90°\nMaximum = 180°"),
            ).Angle = 135

    def onChanged(self, obj, prop: str):
        if prop == "Angle":
            if obj.Angle < 90:
                obj.Angle = 90
            if obj.Angle > 180:
                obj.Angle = 180

    def execute(self, obj):
        w = self.make_beam_rs_wire(obj.HolesNumberX)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
        self.wire_holes = []
        # Genero el cuerpo exterior
        p = self.make_beam_rs(obj.HolesNumberX)
        p = self.make_chamfered_holes_z(p, obj.HolesNumberX, obj.SimpleShape)
        p = self.make_chamfered_holes_y(p, obj.HolesNumberX - 1, obj.SimpleShape, BLOCK_UNIT)
        if not obj.SimpleShape:
            p = self.detail_face(p, self.inset_wire, self.wire_holes)

        w = self.make_beam_ss_wire(obj.HolesNumberY + 1, 1)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
        self.wire_holes = []
        py = Part.makeBox(
            (obj.HolesNumberY + 1) * BLOCK_UNIT,
            BLOCK_UNIT,
            BLOCK_UNIT,
            Vector(-BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF),
            Vector(0, 0, 1),
        )
        py = py.cut(
            Part.makeBox(
                BLOCK_UNIT_HALF,
                BLOCK_UNIT,
                BLOCK_UNIT,
                Vector(-BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF),
                Vector(0, 0, 1),
            )
        )

        py = self.make_chamfered_holes_z(py, obj.HolesNumberY + 1, obj.SimpleShape)
        py = self.make_chamfered_holes_y(py, obj.HolesNumberY, obj.SimpleShape, BLOCK_UNIT)
        if not obj.SimpleShape:
            py = self.detail_face(py, inset_wire, self.wire_holes)
        #  Giro pieza
        # py.translate(Vector(-BLOCK_UNIT_HALF, 0, 0))
        py.rotate(Vector(0, 0, 0), Vector(0, 0, 1), obj.Angle)
        # Uno las dos partes
        p = p.fuse(py)

        #   TODO: chamfer X holes
        #   ----- Ahora que estan girados hago los circulos centrales y los resto
        #   ----- Agujero en X
        agujero1 = Part.makeCylinder(
            HOLE_DIAMETER_STANDARD / 2,
            (obj.HolesNumberX * BLOCK_UNIT) + ((obj.HolesNumberY + 1) * BLOCK_UNIT) + BLOCK_UNIT,
            Vector(((obj.HolesNumberY + 1) * -BLOCK_UNIT), 0, 0),
            Vector(1, 0, 0),
        )
        #   ----- Agujero en Inclinado
        agujero2 = Part.makeCylinder(
            HOLE_DIAMETER_STANDARD / 2,
            (obj.HolesNumberX + obj.HolesNumberY + 2) * BLOCK_UNIT,
            Vector(((obj.HolesNumberX + 1) * -BLOCK_UNIT), 0, 0),
            Vector(1, 0, 0),
        )
        agujero2.rotate(Vector(0, 0, 0), Vector(0, 0, 1), obj.Angle)

        p = p.cut(agujero1.fuse(agujero2))
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = f"Beam STR DBL BU{obj.HolesNumberX}x{obj.HolesNumberY} {obj.Angle}"

        obj.Shape = p.removeSplitter()


class STR_TRPL(STR_DBL):
    """Viga STEMFIE con brazos en los extremos Angulo variable"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumberY1"):
            obj.removeProperty("HolesNumberY1")
        if hasattr(obj, "HolesNumberY2"):
            obj.removeProperty("HolesNumberY2")

        obj.removeProperty("HolesNumberY")
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY1"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in left angular bar\nMinimum = 1"),
        ).HolesNumberY1 = (2, 1, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY2"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number in right angular bar\nMinimum = 1"),
        ).HolesNumberY2 = (2, 1, 50, 1)

    def execute(self, obj):
        w = self.make_beam_rr_wire(obj.HolesNumberX)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
        self.wire_holes = []
        # Genero el cuerpo exterior
        p = self.make_beam_rr(obj.HolesNumberX, obj.SimpleShape)
        p = self.make_chamfered_holes_z(p, obj.HolesNumberX, obj.SimpleShape)
        p = self.make_chamfered_holes_y(p, obj.HolesNumberX - 2, obj.SimpleShape, BLOCK_UNIT)
        if not obj.SimpleShape:
            p = self.detail_face(p, inset_wire, self.wire_holes)

        #  Genero cuerpo Izquierda
        w = self.make_beam_ss_wire(obj.HolesNumberY1 + 1, 1)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
        self.wire_holes = []
        py1 = Part.makeBox(
            (obj.HolesNumberY1 + 1) * BLOCK_UNIT,
            BLOCK_UNIT,
            BLOCK_UNIT,
            Vector(-BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF),
            Vector(0, 0, 1),
        )
        py1 = py1.cut(
            Part.makeBox(
                BLOCK_UNIT_HALF,
                BLOCK_UNIT,
                BLOCK_UNIT,
                Vector(-BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF),
                Vector(0, 0, 1),
            )
        )

        py1 = self.make_chamfered_holes_z(py1, obj.HolesNumberY1 + 1, obj.SimpleShape)
        py1 = self.make_chamfered_holes_y(py1, obj.HolesNumberY1, obj.SimpleShape, BLOCK_UNIT)
        if not obj.SimpleShape:
            py1 = self.detail_face(py1, inset_wire, self.wire_holes)
        py1.rotate(Vector(0, 0, 0), Vector(0, 0, 1), obj.Angle)
        p = p.fuse(py1)

        #  Genero cuerpo Derecha
        w = self.make_beam_ss_wire(obj.HolesNumberY2 + 1, 1)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
        self.wire_holes = []
        py2 = Part.makeBox(
            (obj.HolesNumberY2 + 1) * BLOCK_UNIT,
            BLOCK_UNIT,
            BLOCK_UNIT,
            Vector(-BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF),
            Vector(0, 0, 1),
        )
        py2 = py2.cut(
            Part.makeBox(
                BLOCK_UNIT_HALF,
                BLOCK_UNIT,
                BLOCK_UNIT,
                Vector(-BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF),
                Vector(0, 0, 1),
            )
        )

        py2 = self.make_chamfered_holes_z(py2, obj.HolesNumberY2 + 1, obj.SimpleShape)
        py2 = self.make_chamfered_holes_y(py2, obj.HolesNumberY2, obj.SimpleShape, BLOCK_UNIT)
        if not obj.SimpleShape:
            py2 = self.detail_face(py2, inset_wire, self.wire_holes)
        py2.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 180 - int(obj.Angle))
        py2.translate(Vector((obj.HolesNumberX - 1) * BLOCK_UNIT, 0, 0))
        p = p.fuse(py2)

        #   ----- Ahora que estan girados, hago los circulos centrales y los resto
        #   ----- Agujero en X
        agujero = Part.makeCylinder(
            HOLE_DIAMETER_STANDARD / 2,
            (obj.HolesNumberX + obj.HolesNumberY1 + obj.HolesNumberY2 + 2) * BLOCK_UNIT,
            Vector(((obj.HolesNumberY1 + 1) * -BLOCK_UNIT), 0, 0),
            Vector(1, 0, 0),
        )
        p = p.cut(agujero)
        #   ----- Agujero en Inclinado Y1
        agujero = Part.makeCylinder(
            HOLE_DIAMETER_STANDARD / 2,
            (obj.HolesNumberX + obj.HolesNumberY1 + 2) * BLOCK_UNIT,
            Vector(((obj.HolesNumberX + 1) * -BLOCK_UNIT), 0, 0),
            Vector(1, 0, 0),
        )
        agujero.rotate(Vector(0, 0, 0), Vector(0, 0, 1), obj.Angle)
        p = p.cut(agujero)
        #   ----- Agujero en Inclinado Y2
        agujero = Part.makeCylinder(
            HOLE_DIAMETER_STANDARD / 2,
            (obj.HolesNumberX + obj.HolesNumberY2 + 2) * BLOCK_UNIT,
            Vector(0, 0, 0),
            Vector(1, 0, 0),
        )
        agujero.rotate(
            Vector(((obj.HolesNumberX - 1) * BLOCK_UNIT), 0, 0),
            Vector(0, 0, 1),
            180 - int(obj.Angle),
        )
        p = p.cut(agujero)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            f"Beam STR TRPL {obj.HolesNumberY1}x{obj.HolesNumberX}x{obj.HolesNumberY2} {obj.Angle}"
        )

        obj.Shape = p.removeSplitter()


class STR_BXS_ESS_H(BEAM):
    """Viga hueca STEMFIE"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumber"):
            obj.removeProperty("HolesNumber")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumber"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number\nMinimum = 1"),
        ).HolesNumber = (1, 1, 50, 1)

    def execute(self, obj):
        p = Part.makeBox(
            obj.HolesNumber * BLOCK_UNIT,
            BLOCK_UNIT,
            BLOCK_UNIT,
            Vector(0, -BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF),
            Vector(0, 0, 1),
        )
        p = p.cut(
            Part.makeBox(
                ((obj.HolesNumber - 1) * BLOCK_UNIT) + BLOCK_UNIT_HALF,
                BLOCK_UNIT - BLOCK_UNIT_QUARTER,
                20,
                Vector(BLOCK_UNIT_QUARTER, -4.6875, -10),
                Vector(0, 0, 1),
            )
        )
        p = self.make_chamfered_holes_x(p, obj.HolesNumber, obj.SimpleShape, BLOCK_UNIT_HALF)

        obj.Code = f"Beam STR BXS ESS H BU{obj.HolesNumber}"

        obj.Shape = p


class STR_BXS_ESS_C(BEAM):
    """Viga hueca STEMFIE con dado en los extremos"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumber"):
            obj.removeProperty("HolesNumber")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumber"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Holes number\nMinimum = 3"),
        ).HolesNumber = (3, 3, 50, 1)

    def execute(self, obj):
        p = Part.makeBox(
            obj.HolesNumber * BLOCK_UNIT,
            BLOCK_UNIT,
            BLOCK_UNIT,
            Vector(0, -BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF),
            Vector(0, 0, 1),
        )
        p = p.cut(
            Part.makeBox(
                ((obj.HolesNumber - 2) * BLOCK_UNIT),
                BLOCK_UNIT - BLOCK_UNIT_QUARTER,
                20,
                Vector(BLOCK_UNIT, -4.6875, -10),
                Vector(0, 0, 1),
            )
        )
        # Holes at beginning
        p = self.make_chamfered_holes_z(p, 1, obj.SimpleShape, BLOCK_UNIT_HALF)
        p = self.make_chamfered_holes_y(p, 1, obj.SimpleShape, BLOCK_UNIT_HALF)
        # Holes at end
        p = self.make_chamfered_holes_z(
            p, 1, obj.SimpleShape, BLOCK_UNIT_HALF + (obj.HolesNumber - 1) * BLOCK_UNIT
        )
        p = self.make_chamfered_holes_y(
            p, 1, obj.SimpleShape, BLOCK_UNIT_HALF + (obj.HolesNumber - 1) * BLOCK_UNIT
        )
        p = self.make_chamfered_holes_x(p, obj.HolesNumber, obj.SimpleShape, BLOCK_UNIT_HALF)

        obj.Code = f"Beam STR BXS ESS C BU{obj.HolesNumber}"

        obj.Shape = p
