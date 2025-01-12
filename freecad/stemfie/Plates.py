import FreeCAD
import Part
from FreeCAD import Placement, Rotation, Vector

from freecad.stemfie.utils import (
    BLOCK_UNIT,
    BLOCK_UNIT_HALF,
    BLOCK_UNIT_QUARTER,
    COS_30,
    COS_60,
    FILLET_RADIUS,
    HOLE_DIAMETER_STANDARD,
    PLATE_BORDER_OFFSET,
    PLATE_UPPER_FACE_DIAMETER,
    PLATE_UPPER_FACE_POCKET,
    SIN_30,
    SIN_45,
    SIN_60,
    make_chamfered_hole,
)

translate = FreeCAD.Qt.translate
QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP

simple_hole = Part.makeCylinder(
    HOLE_DIAMETER_STANDARD / 2, BLOCK_UNIT_QUARTER, Vector(0, 0, 0), Vector(0, 0, 1)
)
chamf_hole = make_chamfered_hole(HOLE_DIAMETER_STANDARD, BLOCK_UNIT_QUARTER)

# NOTE: There is a migration code for files using old version of plate classes
# The migration method used is:
# "Method 3. Migration when restoring the document, manually handling the properties"
# from: https://wiki.freecad.org/Scripted_objects_migration

migration_msg = translate(
    "Log", "Plate migration was successful, using new constrained properties.\n"
)


class PLT:
    """Base class for all STEMFIE plates."""

    def __init__(self, obj):
        """
        Initialize the plate object.

        Args:
            obj: The FreeCAD object to which this connector is attached.
        """
        obj.Proxy = self  # Stores a reference to the Python instance in the FeaturePython object
        self.base_initialization(obj)

    def base_initialization(self, obj):
        self.inset_wire = None
        self.wire_holes = []
        obj.addProperty(
            "App::PropertyString",
            QT_TRANSLATE_NOOP("App::Property", "Code"),
            QT_TRANSLATE_NOOP("App::Property", "Designation"),
            QT_TRANSLATE_NOOP(
                "App::Property",
                "Unique identifier based on the features and dimensions of the part",
            ),
        )
        obj.setEditorMode("Code", 1)  # read only
        obj.addProperty(
            "App::PropertyBool",
            QT_TRANSLATE_NOOP("App::Property", "SimpleShape"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP(
                "App::Property",
                "Create simplified shape, holes are not chamfered and upper face is totally flush",
            ),
        ).SimpleShape = False

    def detail_face(self, shape: Part.Shape) -> Part.Shape:
        """Cut a thin slice on the upper face avoiding the holes."""
        inset_face = Part.Face([self.inset_wire] + self.wire_holes, "Part::FaceMakerCheese")
        inset_face.Placement = Placement(
            Vector(0, 0, BLOCK_UNIT_QUARTER - PLATE_UPPER_FACE_POCKET), Rotation()
        )
        upper_cut = inset_face.extrude((Vector(0, 0, PLATE_UPPER_FACE_POCKET)))
        return shape.cut(upper_cut)  # cut thin upper face with holes


class PLT_TRI(PLT):
    """Triangular Plate"""

    def __init__(self, obj):
        super().__init__(obj)
        self.tri_initialization(obj)

    def tri_initialization(self, obj):
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "RowsNumber"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of horizontal rows\nMinimum = 2"),
        ).RowsNumber = (
            3,
            2,
            50,
            1,
        )  # (Default, Minimum, Maximum, Step size)

    def onDocumentRestored(self, obj):
        """Implement migration for old version of shaft plain."""
        if not hasattr(obj, "SimpleShape"):  # old version
            old_props = dict()
            old_props["RowsNumber"] = obj.RowsNumber
            obj.removeProperty("Code")
            obj.removeProperty("RowsNumber")

            self.base_initialization(obj)
            self.tri_initialization(obj)
            obj.RowsNumber = old_props["RowsNumber"]
            FreeCAD.Console.PrintWarning(migration_msg)

    def execute(self, obj):
        #  ---- Genero puntos de los contornos, simetría en eje Y
        p1 = Vector(-(obj.RowsNumber - 1) * BLOCK_UNIT_HALF, 0, 0)
        p2 = Vector((obj.RowsNumber - 1) * BLOCK_UNIT_HALF, 0, 0)
        # angulo entre rectas sobre 2 -> 60°/2 = 30°
        p3 = Vector(
            (obj.RowsNumber - 1) * BLOCK_UNIT_HALF + FILLET_RADIUS * COS_30,
            FILLET_RADIUS * (1 + SIN_30),
            0,
        )
        p4 = Vector(
            FILLET_RADIUS * COS_30,
            (obj.RowsNumber - 1) * BLOCK_UNIT * SIN_60 + FILLET_RADIUS * (1 + SIN_30),
            0,
        )
        p5 = Vector(
            -FILLET_RADIUS * COS_30,
            (obj.RowsNumber - 1) * BLOCK_UNIT * SIN_60 + FILLET_RADIUS * (1 + SIN_30),
            0,
        )
        p6 = Vector(
            -(obj.RowsNumber - 1) * BLOCK_UNIT_HALF - FILLET_RADIUS * COS_30,
            FILLET_RADIUS * (1 + SIN_30),
            0,
        )
        #  ---- Genero puntos para circunferencias
        pc1 = Vector(
            (obj.RowsNumber - 1) * BLOCK_UNIT_HALF + FILLET_RADIUS * COS_30,
            FILLET_RADIUS * (1 - SIN_30),
            0,
        )
        pc2 = Vector(
            0, (obj.RowsNumber - 1) * BLOCK_UNIT * SIN_60 + FILLET_RADIUS * (1 + SIN_30 + COS_60), 0
        )
        pc3 = Vector(
            -(obj.RowsNumber - 1) * BLOCK_UNIT_HALF - FILLET_RADIUS * COS_30,
            FILLET_RADIUS * (1 - SIN_30),
            0,
        )
        #  ---- Creamos lineas y arcos
        l1 = Part.LineSegment(p1, p2)
        c1 = Part.Arc(p2, pc1, p3)
        l2 = Part.LineSegment(p3, p4)
        c2 = Part.Arc(p4, pc2, p5)
        l3 = Part.LineSegment(p5, p6)
        c3 = Part.Arc(p6, pc3, p1)

        #  ---- Creo el contorno
        s = Part.Shape([l1, c1, l2, c2, l3, c3])
        w = Part.Wire(s.Edges)
        self.inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)

        #  ---- Creo la cara con el contorno
        f = Part.Face(w)
        #  ---- Le doy Volumen a la cara
        p = f.extrude(Vector(0, 0, BLOCK_UNIT_QUARTER))

        x0 = -(obj.RowsNumber - 1) * BLOCK_UNIT_HALF
        y0 = BLOCK_UNIT_HALF
        self.wire_holes = []

        # NOTE: Imagine a lattice of equilateral triangles with l = BLOCK_UNIT
        # - Create ascending lines of holes at an angle of 60°,
        #     decreasing the holes number in one for the next lines.
        # - Cut the chamfered holes on the shape.
        # - Add circles to the `wire_holes` array to then create a "cheese" face.
        hole = simple_hole if obj.SimpleShape else chamf_hole
        for x in range(obj.RowsNumber):
            x1 = x0 + x * BLOCK_UNIT * COS_60
            for y in range(obj.RowsNumber - x):
                pos = Vector(x1 + x * BLOCK_UNIT * COS_60, y0 + y * BLOCK_UNIT * SIN_60, 0)
                hole.Placement = Placement(pos, Rotation())
                p = p.cut(hole)
                circle = Part.Circle(
                    pos, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
                )  # center, normal, radius
                self.wire_holes.append(Part.Wire(circle.toShape()))
                x1 += BLOCK_UNIT * COS_60

        if not obj.SimpleShape:
            p = self.detail_face(p)

        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = f"Plate TRI CRNR BU{obj.RowsNumber:02}x00.25"

        obj.Shape = p


# TODO: make version with sharp corners


class PLT_SQR(PLT):
    """Square/Rectangular plate"""

    def __init__(self, obj):
        super().__init__(obj)
        self.sqr_initialization(obj)

    def sqr_initialization(self, obj):
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberX"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP(
                "App::Property", "Number of holes in the X direction of the object\nMinimum = 2"
            ),
        ).HolesNumberX = (
            4,
            2,
            50,
            1,
        )  # (Default, Minimum, Maximum, Step size)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP(
                "App::Property", "Number of holes in the Y direction of the object\nMinimum = 2"
            ),
        ).HolesNumberY = (
            3,
            2,
            50,
            1,
        )  # (Default, Minimum, Maximum, Step size)

    def onDocumentRestored(self, obj):
        """Implement migration for old version of shaft plain."""
        if not hasattr(obj, "SimpleShape"):  # old version
            old_props = dict()
            old_props["HolesNumberX"] = obj.HolesNumberX
            old_props["HolesNumberY"] = obj.HolesNumberY
            obj.removeProperty("Code")
            obj.removeProperty("HolesNumberX")
            obj.removeProperty("HolesNumberY")

            self.base_initialization(obj)
            self.sqr_initialization(obj)
            obj.HolesNumberX = old_props["HolesNumberX"]
            obj.HolesNumberY = old_props["HolesNumberY"]
            FreeCAD.Console.PrintWarning(migration_msg)

    def execute(self, obj):
        #  ---- Genero puntos de los contornos
        p1 = Vector(0, -FILLET_RADIUS, 0)
        p2 = Vector((obj.HolesNumberX - 1) * BLOCK_UNIT, -FILLET_RADIUS, 0)

        p3 = Vector(((obj.HolesNumberX - 1) * BLOCK_UNIT) + FILLET_RADIUS, 0, 0)
        p4 = Vector(
            ((obj.HolesNumberX - 1) * BLOCK_UNIT) + FILLET_RADIUS,
            (obj.HolesNumberY - 1) * BLOCK_UNIT,
            0,
        )

        p5 = Vector(
            (obj.HolesNumberX - 1) * BLOCK_UNIT,
            ((obj.HolesNumberY - 1) * BLOCK_UNIT) + FILLET_RADIUS,
            0,
        )
        p6 = Vector(0, ((obj.HolesNumberY - 1) * BLOCK_UNIT) + FILLET_RADIUS, 0)

        p7 = Vector(-FILLET_RADIUS, ((obj.HolesNumberY - 1) * BLOCK_UNIT), 0)
        p8 = Vector(-FILLET_RADIUS, 0, 0)
        #  ---- Genero puntos para círculos, radio = FILLET_RADIUS
        pc1 = Vector(
            ((obj.HolesNumberX - 1) * BLOCK_UNIT) + (SIN_45 * FILLET_RADIUS),
            SIN_45 * -FILLET_RADIUS,
            0,
        )
        pc2 = Vector(
            ((obj.HolesNumberX - 1) * BLOCK_UNIT) + (SIN_45 * FILLET_RADIUS),
            ((obj.HolesNumberY - 1) * BLOCK_UNIT) + (SIN_45 * FILLET_RADIUS),
            0,
        )
        pc3 = Vector(
            (SIN_45 * FILLET_RADIUS) * -1,
            ((obj.HolesNumberY - 1) * BLOCK_UNIT) + (SIN_45 * FILLET_RADIUS),
            0,
        )
        pc4 = Vector((SIN_45 * FILLET_RADIUS) * -1, (SIN_45 * FILLET_RADIUS) * -1, 0)
        #  ---- Creamos lineas y arcos
        l1 = Part.LineSegment(p1, p2)
        c1 = Part.Arc(p2, pc1, p3)
        l2 = Part.LineSegment(p3, p4)
        c2 = Part.Arc(p4, pc2, p5)
        l3 = Part.LineSegment(p5, p6)
        c3 = Part.Arc(p6, pc3, p7)
        l4 = Part.LineSegment(p7, p8)
        c4 = Part.Arc(p8, pc4, p1)
        #  ---- Creo el contorno
        # W = Part.Wire([l1,c2,l3,c4])

        s = Part.Shape([l1, c1, l2, c2, l3, c3, l4, c4])
        w = Part.Wire(s.Edges)
        self.inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)

        #  ---- Creo la cara con el contorno
        f = Part.Face(w)
        #  ---- Le doy Volumen a la cara
        p = f.extrude(Vector(0, 0, BLOCK_UNIT_QUARTER))
        self.wire_holes = []

        #  ---- Bucle para agujeros
        hole = simple_hole if obj.SimpleShape else chamf_hole
        for x in range(obj.HolesNumberX):
            for y in range(obj.HolesNumberY):
                pos = Vector(x * BLOCK_UNIT, y * BLOCK_UNIT, 0)
                hole.Placement = Placement(pos, Rotation())
                p = p.cut(hole)
                circle = Part.Circle(
                    pos, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
                )  # center, normal, radius
                self.wire_holes.append(Part.Wire(circle.toShape()))

        if not obj.SimpleShape:
            p = self.detail_face(p)

        #  ---- Ponemos Nombre a la pieza con las variables de la misma

        obj.Code = f"Plate SQR RCT CRNR BU{obj.HolesNumberX:02}x{obj.HolesNumberY:02}x00.25"

        obj.Shape = p


class PLT_HEX(PLT):
    """Hexagonal Plate"""

    def __init__(self, obj):
        super().__init__(obj)
        self.hex_initialization(obj)

    def hex_initialization(self, obj):
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "RingsNumber"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP(
                "App::Property", "Number of rings around the central hole\nMinimum = 1"
            ),
        ).RingsNumber = (
            2,
            1,
            50,
            1,
        )  # (Default, Minimum, Maximum, Step size)

    def onDocumentRestored(self, obj):
        """Implement migration for old version of shaft plain."""
        if not hasattr(obj, "SimpleShape"):  # old version
            old_props = dict()
            old_props["RingsNumber"] = obj.RingsNumber
            obj.removeProperty("Code")
            obj.removeProperty("RingsNumber")

            self.base_initialization(obj)
            self.hex_initialization(obj)
            obj.RingsNumber = old_props["RingsNumber"]
            FreeCAD.Console.PrintWarning(migration_msg)

    def execute(self, obj):
        #  ---- Genero puntos de los contornos
        dx = obj.RingsNumber * BLOCK_UNIT * COS_60
        dy = obj.RingsNumber * BLOCK_UNIT * SIN_60 + BLOCK_UNIT_HALF

        p1 = Vector(-dx, -dy, 0)
        p2 = Vector(dx, -dy, 0)

        p3 = Vector(dx + FILLET_RADIUS * COS_30, -dy + FILLET_RADIUS * (1 - SIN_30), 0)
        p4 = Vector(
            obj.RingsNumber * BLOCK_UNIT + FILLET_RADIUS * COS_30, -FILLET_RADIUS * SIN_30, 0
        )

        p5 = Vector(
            obj.RingsNumber * BLOCK_UNIT + FILLET_RADIUS * COS_30, FILLET_RADIUS * SIN_30, 0
        )
        p6 = Vector(dx + FILLET_RADIUS * COS_30, dy - FILLET_RADIUS * (1 - SIN_30), 0)

        p7 = Vector(dx, dy, 0)
        p8 = Vector(-dx, dy, 0)

        p9 = Vector(-dx - FILLET_RADIUS * COS_30, dy - FILLET_RADIUS * (1 - SIN_30), 0)
        p10 = Vector(
            -obj.RingsNumber * BLOCK_UNIT - FILLET_RADIUS * COS_30, FILLET_RADIUS * SIN_30, 0
        )

        p11 = Vector(
            -obj.RingsNumber * BLOCK_UNIT - FILLET_RADIUS * COS_30, -FILLET_RADIUS * SIN_30, 0
        )
        p12 = Vector(-dx - FILLET_RADIUS * COS_30, -dy + FILLET_RADIUS * (1 - SIN_30), 0)

        #  ---- Genero puntos para circunferencias
        pc1 = Vector(dx + FILLET_RADIUS * COS_60, -dy + FILLET_RADIUS * (1 - SIN_60), 0)
        pc2 = Vector(obj.RingsNumber * BLOCK_UNIT + FILLET_RADIUS, 0, 0)
        pc3 = Vector(dx + FILLET_RADIUS * COS_60, dy - FILLET_RADIUS * (1 - SIN_60), 0)
        pc4 = Vector(-dx - FILLET_RADIUS * COS_60, dy - FILLET_RADIUS * (1 - SIN_60), 0)
        pc5 = Vector(-obj.RingsNumber * BLOCK_UNIT - FILLET_RADIUS, 0, 0)
        pc6 = Vector(-dx - FILLET_RADIUS * COS_60, -dy + FILLET_RADIUS * (1 - SIN_60), 0)

        #  ---- Creamos lineas y arcos
        l1 = Part.LineSegment(p1, p2)
        c1 = Part.Arc(p2, pc1, p3)
        l2 = Part.LineSegment(p3, p4)
        c2 = Part.Arc(p4, pc2, p5)
        l3 = Part.LineSegment(p5, p6)
        c3 = Part.Arc(p6, pc3, p7)
        l4 = Part.LineSegment(p7, p8)
        c4 = Part.Arc(p8, pc4, p9)
        l5 = Part.LineSegment(p9, p10)
        c5 = Part.Arc(p10, pc5, p11)
        l6 = Part.LineSegment(p11, p12)
        c6 = Part.Arc(p12, pc6, p1)

        #  ---- Creo el contorno
        s = Part.Shape([l1, c1, l2, c2, l3, c3, l4, c4, l5, c5, l6, c6])
        w = Part.Wire(s.Edges)
        self.inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)

        #  ---- Creo la cara con el contorno
        f = Part.Face(w)
        #  ---- Le doy Volumen a la cara
        p = f.extrude(Vector(0, 0, BLOCK_UNIT_QUARTER))

        x0 = -obj.RingsNumber * BLOCK_UNIT * (1 + COS_60)
        y0 = -obj.RingsNumber * BLOCK_UNIT * SIN_60
        self.wire_holes = []

        # NOTE: Imagine a lattice of equilateral triangles with l = BLOCK_UNIT
        # - Create ascending lines of holes at an angle of 60°,
        #     all the holes take rhomboid shape, there are more than needed
        # - Cut the chamfered holes on the shape.
        # - Add circles to the `wire_holes` array to then create a "cheese" face.
        hole = simple_hole if obj.SimpleShape else chamf_hole
        for x in range(obj.RingsNumber * 2 + 1):
            x1 = x0 + x * BLOCK_UNIT * COS_60
            for y in range(obj.RingsNumber * 2 + 1):
                pos = Vector(x1 + x * BLOCK_UNIT * COS_60, y0 + y * BLOCK_UNIT * SIN_60, 0)
                hole.Placement = Placement(pos, Rotation())
                p = p.cut(hole)
                circle = Part.Circle(
                    pos, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
                )  # center, normal, radius
                self.wire_holes.append(Part.Wire(circle.toShape()))
                x1 += BLOCK_UNIT * COS_60

        if not obj.SimpleShape:
            p = self.detail_face(p)

        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = f"Plate HEX CRNR BU{obj.RingsNumber*2+1:02}x00.25"

        obj.Shape = p
