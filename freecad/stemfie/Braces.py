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
    SIN_45,
    make_chamfered_hole,
    make_slot_wire_rr,
    make_slot_wire_sr,
)

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP

simple_hole = Part.makeCylinder(
    HOLE_DIAMETER_STANDARD / 2, BLOCK_UNIT_QUARTER, Vector(0, 0, 0), Vector(0, 0, 1)
)
chamf_hole = make_hole(HOLE_DIAMETER_STANDARD, BLOCK_UNIT_QUARTER)

# NOTE: general approach is to generate a cheese wire (sketch with internal holes),
# then extrude it and simple shape is done; brace in a single step done.
# Detailed shape is done cutting the holes one by one.

# NOTE: To avoid breaking old files in some parts of the code first is checked if property
# exists and if it does it's deleted because we migrated from "App::PropertyInteger"
# to "App::PropertyIntegerConstraint". Values of properties are reset.


class BRACE:
    def __init__(self, obj):
        obj.Proxy = self  # Stores a reference to the Python instance in the FeaturePython object
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
        obj.addProperty(
            "App::PropertyBool",
            QT_TRANSLATE_NOOP("App::Property", "SimpleShape"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP(
                "App::Property",
                "Create simplified shape, holes are not chamfered and upper face is totally flush",
            ),
        ).SimpleShape = False

    def detail_face(
        self, shape: Part.Shape, inset_wire: Part.Shape, wire_holes: list
    ) -> Part.Shape:
        """
        Cut a thin slice on the upper face avoiding the holes and slots
        - shape: original shape
        - inset_wire: wire containing the shape to subtract
        - wire_holes: holes and slots to avoid cutting
        """
        inset_face = Part.Face([inset_wire] + wire_holes, "Part::FaceMakerCheese")
        inset_face.Placement = Placement(
            Vector(0, 0, BLOCK_UNIT_QUARTER - PLATE_UPPER_FACE_POCKET), Rotation()
        )
        upper_cut = inset_face.extrude((Vector(0, 0, PLATE_UPPER_FACE_POCKET)))
        return shape.cut(upper_cut)  # cut thin upper face with holes

    def make_brace_rr_wire(self, holes_size: int = 2) -> Part.Wire:
        """Create brace shape on X axis, size given by number of holes"""
        return make_slot_wire_rr((holes_size - 1) * BLOCK_UNIT, BLOCK_UNIT_HALF)

    def make_brace(self, holes: int = 2, ss: bool = False) -> Part.Shape:
        """Create brace shape on X axis, size given by number of holes"""
        w = self.make_brace_rr_wire(holes)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
        wire_holes = []
        #  ---- Creo la cara con el contorno
        f = Part.Face(w)
        #  ---- Le doy Volumen a la cara
        p = f.extrude(Vector(0, 0, BLOCK_UNIT_QUARTER))
        hole = simple_hole if ss else chamf_hole
        for x in range(holes):
            pos = Vector(x * BLOCK_UNIT, 0, 0)
            hole.Placement = Placement(pos, Rotation())
            p = p.cut(hole)
            circle = Part.Circle(
                pos, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
            )  # center, normal, radius
            wire_holes.append(Part.Wire(circle.toShape()))

        # FIXME: join inset faces before cutting upper face, looks cool though
        if not ss:
            p = self.detail_face(p, inset_wire, wire_holes)
        return p


class STR_STD_ERR(BRACE):
    """Brace - Straight - Ending Round Round


    Variables:
        Codigo          'Demoninacion'
        HolesNumber      'Numero Agujeros que contiene la pieza

    """

    #      _________________
    #     /                 \
    #    |   ()    ()    () |
    #    \ _______________ /
    #
    #         1     2     3
    #          --------->
    #           HolesNumber

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumber"):
            obj.removeProperty("HolesNumber")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumber"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes along the brace\nMinimum = 2"),
        ).HolesNumber = (
            3,
            2,
            50,
            1,
        )  # (Default, Minimum, Maximum, Step size)

    def execute(self, obj):
        #  ---- Bucle para agujeros
        p = self.make_brace(obj.HolesNumber, obj.SimpleShape)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = f"Brace STR STD ERR BU{obj.HolesNumber:02}x01x00.25"

        obj.Shape = p


class STR_STD_DBL_AZ(BRACE):
    """Brazo Angular STEMFIE"""

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
            QT_TRANSLATE_NOOP("App::Property", "Number of holes along the X axis\nMinimum = 2"),
        ).HolesNumberX = (
            3,
            2,
            50,
            1,
        )  # (Default, Minimum, Maximum, Step size)

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes along the Y axis\nMinimum = 2"),
        ).HolesNumberY = (2, 2, 50, 1)
        if not hasattr(obj, "Angle"):
            obj.addProperty(
                "App::PropertyAngle",
                QT_TRANSLATE_NOOP("App::Property", "Angle"),
                QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
                QT_TRANSLATE_NOOP("App::Property", "Angle\nMinimum = 60°\nMaximum = 180°"),
            ).Angle = 60

    def onChanged(self, obj, prop: str):
        # Compruebo Angulo entre 60° y 180°
        if prop == "Angle":
            if obj.Angle < 60:
                obj.Angle = 60
            if obj.Angle > 180:
                obj.Angle = 180

    def execute(self, obj):
        px = self.make_brace(obj.HolesNumberX, obj.SimpleShape)
        py = self.make_brace(obj.HolesNumberY, obj.SimpleShape)
        py.rotate(Vector(0, 0, 0), Vector(0, 0, 1), obj.Angle)
        p = px.fuse(py)

        sym = "SYM" if obj.HolesNumberX == obj.HolesNumberY else "ASYM"
        obj.Code = f"Brace STR STD DBL AZ {sym} ERR BU{obj.HolesNumberX:02}x{obj.HolesNumberY:02} {obj.Angle}"

        obj.Shape = p.removeSplitter()


class CRN_ERR_ASYM(STR_STD_DBL_AZ):
    """Brazo Angulo 90º STEMFIE"""

    def __init__(self, obj):
        super().__init__(obj)
        obj.removeProperty("Angle")

    def execute(self, obj):
        px = self.make_brace(obj.HolesNumberX, obj.SimpleShape)
        py = self.make_brace(obj.HolesNumberY, obj.SimpleShape)
        py.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 90)
        p = px.fuse(py)
        sym = "SYM" if obj.HolesNumberX == obj.HolesNumberY else "ASYM"
        obj.Code = f"Brace AGD 90 {sym} ERR BU{obj.HolesNumberX:02}x{obj.HolesNumberY:02}x01x00.25"

        obj.Shape = p.removeSplitter()


class STR_STD_SQR_AY(STR_STD_DBL_AZ):
    """Plancha Cuadrada STEMFIE con angulo en Y"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumberSloping"):
            obj.removeProperty("HolesNumberSloping")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberSloping"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes in sloping part\nMinimum 1"),
        ).HolesNumberSloping = (
            2,
            1,
            50,
            1,
        )  # (Default, Minimum, Maximum, Step size)
        obj.Angle = 135

    def onChanged(self, obj, prop: str):
        # Compruebo que Numero_Agujeros mayor de 1
        if prop == "Angle":
            if obj.Angle < 0:
                obj.Angle = 0
            if obj.Angle > 180:
                obj.Angle = 180

    def detail_face(
        self,
        shape: Part.Shape,
        inset_wire: Part.Shape,
        wire_holes: list,
        sloped_plate: bool = False,
    ) -> Part.Shape:
        """Cut a thin slice on the upper face avoiding the holes"""
        inset_face = Part.Face([inset_wire] + wire_holes, "Part::FaceMakerCheese")
        inset_face.Placement = Placement(Vector(0, 0, 0), Rotation())
        sign = -1 if sloped_plate else 1
        upper_cut = inset_face.extrude((Vector(0, 0, -sign * PLATE_UPPER_FACE_POCKET)))
        return shape.cut(upper_cut)  # cut thin upper face with holes

    def make_plate(
        self,
        holesX: int = 2,
        holesY: int = 2,
        ss: bool = False,
        angle: float = 0,
        sloped_plate: bool = False,
    ) -> Part.Shape:
        #  ---- Genero Cuerpo Horizontal
        pto1 = Vector(-BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF, 0)
        pto2 = Vector((holesX - 1) * BLOCK_UNIT, -BLOCK_UNIT_HALF, 0)

        pto3 = Vector(((holesX - 1) * BLOCK_UNIT) + BLOCK_UNIT_HALF, 0, 0)
        pto4 = Vector(((holesX - 1) * BLOCK_UNIT) + BLOCK_UNIT_HALF, (holesY - 1) * BLOCK_UNIT, 0)

        pto5 = Vector((holesX - 1) * BLOCK_UNIT, ((holesY - 1) * BLOCK_UNIT) + BLOCK_UNIT_HALF, 0)
        pto6 = Vector(-BLOCK_UNIT_HALF, ((holesY - 1) * BLOCK_UNIT) + BLOCK_UNIT_HALF, 0)

        #  ---- Genero puntos para círculos
        ptoc1 = Vector(
            ((holesX - 1) * BLOCK_UNIT) + (SIN_45 * BLOCK_UNIT_HALF), SIN_45 * -BLOCK_UNIT_HALF, 0
        )
        ptoc2 = Vector(
            ((holesX - 1) * BLOCK_UNIT) + SIN_45 * BLOCK_UNIT_HALF,
            ((holesY - 1) * BLOCK_UNIT) + SIN_45 * BLOCK_UNIT_HALF,
            0,
        )
        #  ---- Creamos lineas y arcos
        l1 = Part.LineSegment(pto1, pto2)
        c1 = Part.Arc(pto2, ptoc1, pto3)
        l2 = Part.LineSegment(pto3, pto4)
        c2 = Part.Arc(pto4, ptoc2, pto5)
        l3 = Part.LineSegment(pto5, pto6)
        l4 = Part.LineSegment(pto6, pto1)
        #  ---- Creo el contorno
        s = Part.Shape([l1, c1, l2, c2, l3, l4])
        w = Part.Wire(s.Edges)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
        wire_holes = []
        #  ---- Creo la cara con el contorno
        f = Part.Face(w)
        #  ---- Le doy Volumen a la cara
        sign = -1 if sloped_plate else 1
        p = f.extrude(Vector(0, 0, sign * -BLOCK_UNIT_QUARTER))
        #  ---- Bucle para agujeros
        hole = simple_hole if ss else chamf_hole

        def z(sign: int):
            return -(BLOCK_UNIT_QUARTER / 2) * (sign - 1) - BLOCK_UNIT_QUARTER

        for x in range(holesX):
            for y in range(holesY):
                pos = Vector(x * BLOCK_UNIT, y * BLOCK_UNIT, z(sign))
                pos2 = Vector(x * BLOCK_UNIT, y * BLOCK_UNIT, 0)
                hole.Placement = Placement(pos, Rotation())
                p = p.cut(hole)
                circle = Part.Circle(
                    pos2, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
                )  # center, normal, radius
                wire_holes.append(Part.Wire(circle.toShape()))

        if not ss:
            p = self.detail_face(p, inset_wire, wire_holes, sloped_plate)

        # Condicional para ángulo 180 no generar cilindros
        if angle != 180:
            # Tengo que meter un cuarto de cilindro y unirlo a P
            # Añado condicional para que sea en función del angulo
            ang = (180 - int(angle)) / 2
            Curva = Part.makeCylinder(
                BLOCK_UNIT_QUARTER,
                holesY * BLOCK_UNIT,
                Vector(sign * BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF, 0),
                Vector(0, 1, 0),
                ang,
            )  # radius, height, position, direction, angle

            if sloped_plate:
                Curva.rotate(
                    Vector(-BLOCK_UNIT_HALF, -BLOCK_UNIT_HALF, 0),
                    Vector(0, 1, 0),
                    -ang,
                )
            else:
                Curva.rotate(Vector(0, 0, 0), Vector(0, 1, 0), 180)
            p = p.fuse(Curva)
        return p

    def execute(self, obj):
        p = self.make_plate(obj.HolesNumberX, obj.HolesNumberY, obj.SimpleShape, 0)
        p_inc = self.make_plate(
            obj.HolesNumberSloping, obj.HolesNumberY, obj.SimpleShape, obj.Angle, True
        )
        # Giro en Y
        p_inc.rotate(Vector(-BLOCK_UNIT_HALF, 0, 0), Vector(0, 1, 0), -obj.Angle)
        # Junto los dos cuerpos
        p = p.fuse(p_inc)
        # Refinamos el cuerpo
        p = p.removeSplitter()

        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            f"Brace STR STD SQR AY BU{obj.HolesNumberX:02}x{obj.HolesNumberY:02}x{obj.HolesNumberSloping:02} "
            f"{obj.Angle}"
        )

        obj.Shape = p


# TODO: add chamfered slot cutter

# TODO: Braces - Straight - Slotted - Sequential - Round Ends


class STR_SLT_BE_SYM_ERR(BRACE):
    """Brazo STEMFIE con agujeros rasgados en extremos y simples en el centro"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumberTotal"):
            obj.removeProperty("HolesNumberTotal")
        if hasattr(obj, "HolesNumberSlotted"):
            obj.removeProperty("HolesNumberSlotted")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberTotal"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Total number of holes\nMinimum 5"),
        ).HolesNumberTotal = (
            5,
            5,
            50,
            1,
        )  # (Default, Minimum, Maximum, Step size)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberSlotted"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP(
                "App::Property", "Number of slotted holes\nSame on both sides\nMinimum 2"
            ),
        ).HolesNumberSlotted = (2, 2, 50, 1)

    def execute(self, obj):
        if (obj.HolesNumberSlotted * 2) + 1 > (obj.HolesNumberTotal):
            obj.HolesNumberTotal = (obj.HolesNumberSlotted * 2) + 1
        # ----------------------------
        #  ---- Genero Cuerpo exterior
        main_wire = self.make_brace_rr_wire(obj.HolesNumberTotal)
        slot_1 = make_slot_wire_rr(
            (obj.HolesNumberSlotted - 1) * BLOCK_UNIT, HOLE_DIAMETER_STANDARD / 2
        )
        slot_2 = make_slot_wire_rr(
            (obj.HolesNumberSlotted - 1) * BLOCK_UNIT, HOLE_DIAMETER_STANDARD / 2
        )
        slot2_place = Placement(
            Vector((obj.HolesNumberTotal - obj.HolesNumberSlotted) * BLOCK_UNIT, 0, 0), Rotation()
        )
        slot_2.Placement = slot2_place

        wire_holes = [slot_1, slot_2]

        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumberSlotted, obj.HolesNumberTotal - obj.HolesNumberSlotted, 1):
            pos = Vector(x * BLOCK_UNIT, 0, 0)
            circle = Part.Circle(
                pos, Vector(0, 0, 1), HOLE_DIAMETER_STANDARD / 2
            )  # center, normal, radius
            wire_holes.append(Part.Wire(circle.toShape()))

        face = Part.Face([main_wire] + wire_holes, "Part::FaceMakerCheese")
        p = face.extrude(Vector(0, 0, BLOCK_UNIT_QUARTER))

        if not obj.SimpleShape:
            inset_wire = main_wire.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
            slot1_up = make_slot_wire_rr(
                (obj.HolesNumberSlotted - 1) * BLOCK_UNIT, PLATE_UPPER_FACE_DIAMETER / 2
            )
            slot2_up = make_slot_wire_rr(
                (obj.HolesNumberSlotted - 1) * BLOCK_UNIT, PLATE_UPPER_FACE_DIAMETER / 2
            )
            slot2_up.Placement = slot2_place
            wire_holes_up = [slot1_up, slot2_up]

            hole = simple_hole if obj.SimpleShape else chamf_hole
            for x in range(
                obj.HolesNumberSlotted, obj.HolesNumberTotal - obj.HolesNumberSlotted, 1
            ):
                pos = Vector(x * BLOCK_UNIT, 0, 0)
                hole.Placement = Placement(pos, Rotation())
                p = p.cut(hole)
                circle1_up = Part.Circle(
                    pos, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
                )  # center, normal, radius
                wire_holes_up.append(Part.Wire(circle1_up.toShape()))

            p = self.detail_face(p, inset_wire, wire_holes_up)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = f"Brace STR SLT BE SYM ERR BU{obj.HolesNumberTotal:02}x01x00.25x{obj.HolesNumberSlotted:02}"

        obj.Shape = p


class STR_SLT_CNT_ERR(BRACE):
    """Brazo STEMFIE con agujeros rasgados en centro y simples en extremos"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumberTotal"):
            obj.removeProperty("HolesNumberTotal")
        if hasattr(obj, "HolesNumberSlotted"):
            obj.removeProperty("HolesNumberSlotted")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberTotal"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Total number of holes\nMinimum 4"),
        ).HolesNumberTotal = (4, 4, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberSlotted"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of slotted holes\nMinimum 2"),
        ).HolesNumberSlotted = (2, 2, 50, 1)

    def execute(self, obj):
        # Compruebo que HolesNumberTotal y HolesNumberSlotted
        if (obj.HolesNumberTotal < 4) or (
            obj.HolesNumberSlotted < 2
        ):  # Si alguno es menor no modificar pieza
            if obj.HolesNumberTotal < 4:  # si Numero Total de Agujeros es menor 4
                obj.HolesNumberTotal = 4  # dejarlo en 4
            else:  # si no
                obj.HolesNumberSlotted = 2  # dejar Numero Agujeros del coliso en 2
            # return
        # Ahora compuebo que la longitud total no sea menor de lo necesario
        if obj.HolesNumberSlotted + 2 > obj.HolesNumberTotal:
            obj.HolesNumberTotal = obj.HolesNumberSlotted + 2

        if ((obj.HolesNumberTotal - obj.HolesNumberSlotted) % 2) != 0:
            obj.HolesNumberTotal = (obj.HolesNumberTotal) + 1
        # ----------------------------
        main_wire = self.make_brace_rr_wire(obj.HolesNumberTotal)
        slot = make_slot_wire_rr(
            (obj.HolesNumberSlotted - 1) * BLOCK_UNIT, HOLE_DIAMETER_STANDARD / 2
        )
        slot_place = Placement(
            Vector((obj.HolesNumberTotal - obj.HolesNumberSlotted) / 2 * BLOCK_UNIT, 0, 0),
            Rotation(),
        )
        slot.Placement = slot_place
        wire_holes = [slot]

        #  ---- Bucle para agujeros
        for x in range(int((obj.HolesNumberTotal - obj.HolesNumberSlotted) / 2)):
            pos1 = Vector(x * BLOCK_UNIT, 0, 0)
            pos2 = Vector((obj.HolesNumberTotal - x - 1) * BLOCK_UNIT, 0, 0)
            circle1 = Part.Circle(
                pos1, Vector(0, 0, 1), HOLE_DIAMETER_STANDARD / 2
            )  # center, normal, radius
            circle2 = Part.Circle(
                pos2, Vector(0, 0, 1), HOLE_DIAMETER_STANDARD / 2
            )  # center, normal, radius
            wire_holes.append(Part.Wire(circle1.toShape()))
            wire_holes.append(Part.Wire(circle2.toShape()))

        face = Part.Face([main_wire] + wire_holes, "Part::FaceMakerCheese")
        p = face.extrude(Vector(0, 0, BLOCK_UNIT_QUARTER))

        if not obj.SimpleShape:
            inset_wire = main_wire.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
            slot_up = make_slot_wire_rr(
                (obj.HolesNumberSlotted - 1) * BLOCK_UNIT, PLATE_UPPER_FACE_DIAMETER / 2
            )
            slot_up.Placement = slot_place
            wire_holes_up = [slot_up]

            hole = simple_hole if obj.SimpleShape else chamf_hole
            for x in range(int((obj.HolesNumberTotal - obj.HolesNumberSlotted) / 2)):
                pos1 = Vector(x * BLOCK_UNIT, 0, 0)
                pos2 = Vector((obj.HolesNumberTotal - x - 1) * BLOCK_UNIT, 0, 0)
                hole.Placement = Placement(pos1, Rotation())
                p = p.cut(hole)
                hole.Placement = Placement(pos2, Rotation())
                p = p.cut(hole)
                circle1_up = Part.Circle(
                    pos1, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
                )  # center, normal, radius
                circle2_up = Part.Circle(
                    pos2, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
                )  # center, normal, radius
                wire_holes_up.append(Part.Wire(circle1_up.toShape()))
                wire_holes_up.append(Part.Wire(circle2_up.toShape()))

            p = self.detail_face(p, inset_wire, wire_holes_up)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = f"Brace STR SLT CNT ERR BU{obj.HolesNumberTotal:02}x01x00.25x{obj.HolesNumberSlotted:02}"

        obj.Shape = p


class STR_SLT_FL_ERR(BRACE):
    """Brazo STEMFIE rasgado en toda su extension"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumber"):
            obj.removeProperty("HolesNumber")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumber"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes\nMinimum 2"),
        ).HolesNumber = (4, 2, 50, 1)

    def execute(self, obj):
        main_wire = self.make_brace_rr_wire(obj.HolesNumber)
        slot = make_slot_wire_rr((obj.HolesNumber - 1) * BLOCK_UNIT, HOLE_DIAMETER_STANDARD / 2)
        face = Part.Face([main_wire, slot], "Part::FaceMakerCheese")
        p = face.extrude(Vector(0, 0, BLOCK_UNIT_QUARTER))

        if not obj.SimpleShape:
            inset_wire = main_wire.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
            wire_holes = [
                make_slot_wire_rr((obj.HolesNumber - 1) * BLOCK_UNIT, PLATE_UPPER_FACE_DIAMETER / 2)
            ]
            p = self.detail_face(p, inset_wire, wire_holes)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = f"Brace STR SLT FL ERR BU{obj.HolesNumber:02}x01x00.25"
        obj.Shape = p


class STR_SLT_SE_ERR(BRACE):
    """Brazo STEMFIE agujeros en un extremo y rasgado en el otro"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumber"):
            obj.removeProperty("HolesNumber")
        if hasattr(obj, "HolesNumberSlotted"):
            obj.removeProperty("HolesNumberSlotted")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumber"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of normal holes\nMinimum 1"),
        ).HolesNumber = (1, 1, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberSlotted"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP(
                "App::Property",
                "Slotted holes number\nMinimum 2",
            ),
        ).HolesNumberSlotted = (2, 2, 50, 1)

    def execute(self, obj):
        # Creo la variable de total agujeros
        HolesNumberTotal = obj.HolesNumber + obj.HolesNumberSlotted

        main_wire = self.make_brace_rr_wire(HolesNumberTotal)
        slot = make_slot_wire_rr(
            (obj.HolesNumberSlotted - 1) * BLOCK_UNIT, HOLE_DIAMETER_STANDARD / 2
        )
        slot.Placement = Placement(Vector(obj.HolesNumber * BLOCK_UNIT, 0, 0), Rotation())
        wire_holes = [slot]

        #  ---- Bucle para agujeros
        for x in range(obj.HolesNumber):
            pos = Vector(x * BLOCK_UNIT, 0, 0)
            circle = Part.Circle(
                pos, Vector(0, 0, 1), HOLE_DIAMETER_STANDARD / 2
            )  # center, normal, radius
            wire_holes.append(Part.Wire(circle.toShape()))

        face = Part.Face([main_wire] + wire_holes, "Part::FaceMakerCheese")
        p = face.extrude(Vector(0, 0, BLOCK_UNIT_QUARTER))

        if not obj.SimpleShape:
            inset_wire = main_wire.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
            slot_up = make_slot_wire_rr(
                (obj.HolesNumberSlotted - 1) * BLOCK_UNIT, PLATE_UPPER_FACE_DIAMETER / 2
            )
            slot_up.Placement = Placement(Vector(obj.HolesNumber * BLOCK_UNIT, 0, 0), Rotation())
            wire_holes_up = [slot_up]

            hole = simple_hole if obj.SimpleShape else chamf_hole
            for x in range(obj.HolesNumber):
                pos = Vector(x * BLOCK_UNIT, 0, 0)
                hole.Placement = Placement(pos, Rotation())
                p = p.cut(hole)
                circle_up = Part.Circle(
                    pos, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
                )  # center, normal, radius
                wire_holes_up.append(Part.Wire(circle_up.toShape()))

            p = self.detail_face(p, inset_wire, wire_holes_up)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            f"Brace STR SLT SE ERR BU{obj.HolesNumber:02}x01x00.25x{obj.HolesNumberSlotted:02}"
        )
        obj.Shape = p


class STR_STD_DBL_AY(BRACE):
    """Brazo STEMFIE angulo en Y Nº_Agujeros en horizontal y Nº agujeros en inclinada"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumberX"):
            obj.removeProperty("HolesNumberX")
        if hasattr(obj, "HolesNumberSloping"):
            obj.removeProperty("HolesNumberSloping")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberX"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes in horizontal bar\nMinimum 1"),
        ).HolesNumberX = (3, 1, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberSloping"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes in sloping part\nMinimum 1"),
        ).HolesNumberSloping = (2, 1, 50, 1)
        if not hasattr(obj, "Angle"):
            obj.addProperty(
                "App::PropertyAngle",
                QT_TRANSLATE_NOOP("App::Property", "Angle"),
                QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
                QT_TRANSLATE_NOOP("App::Property", "Angle\nMinimum = 0\nMaximum = 180"),
            ).Angle = 135

    def onChanged(self, obj, prop: str):
        if prop == "Angle":
            if obj.Angle < 0:
                obj.Angle = 0
            if obj.Angle > 180:
                obj.Angle = 180

    def detail_face(
        self,
        shape: Part.Shape,
        inset_wire: Part.Shape,
        wire_holes: list,
        sloped_plate: bool = False,
    ) -> Part.Shape:
        """Cut a thin slice on the upper face avoiding the holes"""
        inset_face = Part.Face([inset_wire] + wire_holes, "Part::FaceMakerCheese")
        inset_face.Placement = Placement(Vector(0, 0, 0), Rotation())
        sign = -1 if sloped_plate else 1
        upper_cut = inset_face.extrude((Vector(0, 0, -sign * PLATE_UPPER_FACE_POCKET)))
        return shape.cut(upper_cut)  # cut thin upper face with holes

    def make_brace_sr_wire(self, holes_size: int = 2) -> Part.Wire:
        """Create brace shape on X axis, size given by number of holes"""
        return make_slot_wire_sr(holes_size * BLOCK_UNIT - BLOCK_UNIT_HALF, BLOCK_UNIT_HALF)

    def make_brace_sr(
        self,
        holes: int = 2,
        ss: bool = False,
        angle: float = 0,
        sloped_plate: bool = False,
    ) -> Part.Shape:
        """Makes a brace with a square end and a round end"""
        #  ---- Genero Cuerpo Horizontal
        w = self.make_brace_sr_wire(holes)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
        wire_holes = []
        #  ---- Creo la cara con el contorno
        f = Part.Face(w)
        #  ---- Le doy Volumen a la cara
        sign = -1 if sloped_plate else 1
        p = f.extrude(Vector(0, 0, sign * -BLOCK_UNIT_QUARTER))
        # Hago los Agujeros de X
        hole = simple_hole if ss else chamf_hole

        def z(sign: int):
            return -(BLOCK_UNIT_QUARTER / 2) * (sign - 1) - BLOCK_UNIT_QUARTER

        for x in range(holes):
            for y in range(holes):
                pos = Vector(x * BLOCK_UNIT + BLOCK_UNIT_HALF, 0, z(sign))
                pos2 = Vector(x * BLOCK_UNIT + BLOCK_UNIT_HALF, y * BLOCK_UNIT, 0)
                hole.Placement = Placement(pos, Rotation())
                p = p.cut(hole)
                circle = Part.Circle(
                    pos2, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
                )  # center, normal, radius
                wire_holes.append(Part.Wire(circle.toShape()))

        if not ss:
            p = self.detail_face(p, inset_wire, wire_holes, sloped_plate)
        # Condicional para ángulo 180 no generar cilindros
        if angle != 180:
            # Tengo que meter un cuarto de cilindro y unirlo a P
            # Añado condicional para que sea en función del ángulo
            ang = (180 - int(angle)) / 2
            curva = Part.makeCylinder(
                BLOCK_UNIT_QUARTER,
                BLOCK_UNIT,
                Vector(0, -BLOCK_UNIT_HALF, 0),
                Vector(0, 1, 0),
                ang,
            )
            if sloped_plate:
                curva.rotate(Vector(0, 0, 0), Vector(0, 1, 0), -ang)
            else:
                curva.rotate(Vector(0, 0, 0), Vector(0, 1, 0), 180)
            p = p.fuse(curva)
        return p

    def execute(self, obj):
        p = self.make_brace_sr(obj.HolesNumberX, obj.SimpleShape, obj.Angle)
        p_inc = self.make_brace_sr(obj.HolesNumberSloping, obj.SimpleShape, obj.Angle, True)
        p_inc.rotate(Vector(0, 0, 0), Vector(0, 1, 0), obj.Angle * -1)
        p = p.fuse(p_inc)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = f"Brace STR_STD_DBL_AY BU{obj.HolesNumberX}x{obj.HolesNumberSloping} {obj.Angle}"
        #  ---- Añado emplazamiento al objeto
        obj.Shape = p.removeSplitter()


class STR_STD_TRPL_AZ(BRACE):
    """Brazo STEMFIE con brazos inclinados en extremos"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumberX"):
            obj.removeProperty("HolesNumberX")
        if hasattr(obj, "HolesNumberY1"):
            obj.removeProperty("HolesNumberY1")
        if hasattr(obj, "HolesNumberY2"):
            obj.removeProperty("HolesNumberY2")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberX"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes in central bar\nMinimum = 3"),
        ).HolesNumberX = (3, 3, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY1"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes in left vertical bar\nMinimum = 1"),
        ).HolesNumberY1 = (2, 1, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberY2"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP(
                "App::Property", "Number of holes in right vertical bar\nMinimum = 1"
            ),
        ).HolesNumberY2 = (2, 1, 50, 1)
        if not hasattr(obj, "Angle"):
            obj.addProperty(
                "App::PropertyAngle",
                QT_TRANSLATE_NOOP("App::Property", "Angle"),
                QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
                QT_TRANSLATE_NOOP("App::Property", "Angle\nMinimum = 90°\nMaximum = 180°"),
            ).Angle = 90

    def onChanged(self, obj, prop: str):
        if prop == "Angle":
            if obj.Angle < 90:
                obj.Angle = 90
            if obj.Angle > 180:
                obj.Angle = 180

    def execute(self, obj):
        px = self.make_brace(obj.HolesNumberX, obj.SimpleShape)
        py1 = self.make_brace(obj.HolesNumberY1, obj.SimpleShape)
        py1.rotate(Vector(0, 0, 0), Vector(0, 0, 1), obj.Angle)
        py2 = self.make_brace(obj.HolesNumberY2, obj.SimpleShape)
        py2.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 180 - int(obj.Angle))
        py2.translate(Vector((obj.HolesNumberX - 1) * BLOCK_UNIT, 0, 0))
        p = px.fuse(py1)
        p = p.fuse(py2)

        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            f"Brace STR_STD_TRPL_AZ BU{obj.HolesNumberY1}x{obj.HolesNumberX}"
            f"x{obj.HolesNumberY2} {obj.Angle}"
        )

        obj.Shape = p.removeSplitter()


class STR_STD_TRPL_AY(STR_STD_DBL_AY):
    """Brazo STEMFIE con brazos inclinados en extremos en eje Y"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        obj.removeProperty("HolesNumberSloping")
        if hasattr(obj, "HolesNumberSloping1"):
            obj.removeProperty("HolesNumberSloping1")
        if hasattr(obj, "HolesNumberSloping2"):
            obj.removeProperty("HolesNumberSloping2")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberSloping1"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes in left sloping part\nMinimum 1"),
        ).HolesNumberSloping1 = (2, 1, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberSloping2"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes in right sloping part\nMinimum 1"),
        ).HolesNumberSloping2 = (2, 1, 50, 1)

    def make_brace_ff(self, holes: int = 2, ss: bool = False, angle: float = 0) -> Part.Shape:
        """Makes a brace with a flat end and a round end"""
        #  ---- Genero Cuerpo Horizontal
        p1 = Vector(0, -BLOCK_UNIT_HALF, 0)
        p2 = Vector((holes * BLOCK_UNIT), -BLOCK_UNIT_HALF, 0)
        p3 = Vector((holes * BLOCK_UNIT), BLOCK_UNIT_HALF, 0)
        p4 = Vector(0, BLOCK_UNIT_HALF, 0)
        #  ---- Creamos lineas y arcos
        l1 = Part.LineSegment(p1, p2)
        l2 = Part.LineSegment(p2, p3)
        l3 = Part.LineSegment(p3, p4)
        l4 = Part.LineSegment(p4, p1)
        s = Part.Shape([l1, l2, l3, l4])
        w = Part.Wire(s.Edges)
        inset_wire = w.makeOffset2D(-PLATE_BORDER_OFFSET)  # Offset -1.1mm (inside)
        wire_holes = []
        #  ---- Creo la cara con el contorno
        f = Part.Face(w)
        #  ---- Le doy Volumen a la cara
        p = f.extrude(Vector(0, 0, -BLOCK_UNIT_QUARTER))
        # Hago los Agujeros de X
        hole = simple_hole if ss else chamf_hole

        for x in range(holes):
            for y in range(holes):
                pos = Vector(x * BLOCK_UNIT + BLOCK_UNIT_HALF, 0, -BLOCK_UNIT_QUARTER)
                pos2 = Vector(x * BLOCK_UNIT + BLOCK_UNIT_HALF, y * BLOCK_UNIT, 0)
                hole.Placement = Placement(pos, Rotation())
                p = p.cut(hole)
                circle = Part.Circle(
                    pos2, Vector(0, 0, 1), PLATE_UPPER_FACE_DIAMETER / 2
                )  # center, normal, radius
                wire_holes.append(Part.Wire(circle.toShape()))

        if not ss:
            p = self.detail_face(p, inset_wire, wire_holes)
        # Condicional para angulo 180 no generar cilindros

        # Tengo que meter dos cachos de cilindro en los extremos y unirlo a P
        # Añado condicional para que sea en funcion del angulo
        #  ---- Primer Cilindro
        if angle != 180:
            ang = (180 - int(angle)) / 2
            curva1 = Part.makeCylinder(
                BLOCK_UNIT_QUARTER,
                BLOCK_UNIT,
                Vector(0, -BLOCK_UNIT_HALF, 0),
                Vector(0, 1, 0),
                ang,
            )
            curva1.rotate(Vector(0, 0, 0), Vector(0, 1, 0), 180)
            p = p.fuse(curva1)
            #  ---- Segundo Cilindro
            curva2 = Part.makeCylinder(
                BLOCK_UNIT_QUARTER,
                BLOCK_UNIT,
                Vector(holes * BLOCK_UNIT, -BLOCK_UNIT_HALF, 0),
                Vector(0, 1, 0),
                ang,
            )
            curva2.rotate(
                Vector(holes * BLOCK_UNIT, 0, 0),
                Vector(0, 1, 0),
                180 - ang,
            )
            p = p.fuse(curva2)
        return p

    def execute(self, obj):
        p = self.make_brace_ff(obj.HolesNumberX, obj.SimpleShape, obj.Angle)
        p_inc1 = self.make_brace_sr(obj.HolesNumberSloping1, obj.SimpleShape, obj.Angle, True)
        p_inc2 = self.make_brace_sr(obj.HolesNumberSloping2, obj.SimpleShape, obj.Angle, True)
        p_inc1.rotate(Vector(0, 0, 0), Vector(0, 1, 0), -obj.Angle)
        p_inc2.rotate(Vector(0, 0, 0), Vector(0, 1, 0), -obj.Angle)
        p_inc2.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 180)
        p_inc2.translate(Vector(obj.HolesNumberX * BLOCK_UNIT, 0, 0))
        p = p.fuse(p_inc1)
        p = p.fuse(p_inc2)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        obj.Code = (
            f"Brace STR STD TRPL AY BU{obj.HolesNumberSloping1}x{obj.HolesNumberX}"
            f"x{obj.HolesNumberSloping2} {obj.Angle}"
        )

        obj.Shape = p


class STR_STD_CRS(BRACE):
    """Brazo STEMFIE Cruz con longitud de brazos independientes"""

    def __init__(self, obj):
        super().__init__(obj)
        # to update old unconstrained  property
        if hasattr(obj, "HolesNumberXPositive"):
            obj.removeProperty("HolesNumberXPositive")
        if hasattr(obj, "HolesNumberXNegative"):
            obj.removeProperty("HolesNumberXNegative")
        if hasattr(obj, "HolesNumberYPositive"):
            obj.removeProperty("HolesNumberYPositive")
        if hasattr(obj, "HolesNumberYNegative"):
            obj.removeProperty("HolesNumberYNegative")

        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberXPositive"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes along the X+ axis\nMinimum = 1"),
        ).HolesNumberXPositive = (3, 1, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberXNegative"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes along the X- axis\nMinimum = 1"),
        ).HolesNumberXNegative = (3, 1, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberYPositive"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes along the Y+ axis\nMinimum = 1"),
        ).HolesNumberYPositive = (2, 1, 50, 1)
        obj.addProperty(
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumberYNegative"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes along the Y- axis\nMinimum = 1"),
        ).HolesNumberYNegative = (2, 1, 50, 1)

    def execute(self, obj):
        px = self.make_brace(
            obj.HolesNumberXPositive + obj.HolesNumberXNegative + 1, obj.SimpleShape
        )
        py = self.make_brace(
            obj.HolesNumberYPositive + obj.HolesNumberYNegative + 1, obj.SimpleShape
        )
        px.translate(Vector(-obj.HolesNumberXNegative * BLOCK_UNIT, 0, 0))
        py.translate(Vector(-obj.HolesNumberYNegative * BLOCK_UNIT, 0, 0))
        py.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 90)
        p = px.fuse(py)
        #  ---- Ponemos Nombre a la pieza con las variables de la misma
        sym = (
            "SYM"
            if obj.HolesNumberXPositive == obj.HolesNumberXNegative
            and obj.HolesNumberYPositive == obj.HolesNumberYNegative
            else "ASYM"
        )
        obj.Code = (
            f"Brace CRS STD {sym} ERR BU{obj.HolesNumberXPositive:02}x{obj.HolesNumberXNegative:02}"
            f"x{obj.HolesNumberYPositive:02}x{obj.HolesNumberYNegative:02}"
        )

        obj.Shape = p.removeSplitter()
