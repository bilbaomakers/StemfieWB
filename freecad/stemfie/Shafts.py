from math import sqrt

import FreeCAD
import Part
from FreeCAD import Vector

from freecad.stemfie.utils import (
    BLOCK_UNIT,
    BLOCK_UNIT_QUARTER,
    DOWEL_SHAFT_HOLE_DIAMETER,
    DOWEL_SHAFT_THICKNESS,
    make_hole,
)

translate = FreeCAD.Qt.translate
QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP


class SFT:
    """Base class for all STEMFIE shafts."""

    def __init__(self, obj):
        obj.Proxy = self  # Stores a reference to the Python instance in the FeaturePython object
        self._updating = False  # Reset the flag after the update is done
        if hasattr(obj, "HolesNumber"):  # migrating from old plain shaft
            old_props = dict()
            old_props["HolesNumber"] = obj.HolesNumber
            obj.removeProperty("Code")
            obj.removeProperty("HolesNumber")

            self.initialization(obj)
            obj.HolesNumber = old_props["HolesNumber"]
            obj.Label = "SFT_IDX"
        else:
            self.initialization(obj)

    def initialization(self, obj):
        self.hole = make_chamfered_hole(
            DOWEL_SHAFT_HOLE_DIAMETER, DOWEL_SHAFT_THICKNESS, -DOWEL_SHAFT_THICKNESS / 2
        )
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
            "App::PropertyIntegerConstraint",
            QT_TRANSLATE_NOOP("App::Property", "HolesNumber"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP("App::Property", "Number of holes along the shaft\nMinimum = 1"),
        ).HolesNumber = (
            3,
            1,
            1000,
            1,
        )  # (Default, Minimum, Maximum, Step size)
        obj.addProperty(
            "App::PropertyFloatConstraint",
            QT_TRANSLATE_NOOP("App::Property", "Length"),
            QT_TRANSLATE_NOOP("App::Property", "Part parameters"),
            QT_TRANSLATE_NOOP(
                "App::Property", "Shaft length in terms of Block Units (BU)\n1 BU=12.5 mm"
            ),
        ).Length = (0.75, 0.25, 1000, 0.25)

    def shaft_shape(self, length: float) -> Part.Shape:
        """Create a shaft shape with a specified length."""
        #  Profile symmetric to Y and Z axis
        dx = sqrt(BLOCK_UNIT_QUARTER**2 - (DOWEL_SHAFT_THICKNESS / 2) ** 2)
        p1 = Vector(0, -dx, -DOWEL_SHAFT_THICKNESS / 2)
        p2 = Vector(0, dx, -DOWEL_SHAFT_THICKNESS / 2)
        p3 = Vector(0, dx, DOWEL_SHAFT_THICKNESS / 2)
        p4 = Vector(0, -dx, DOWEL_SHAFT_THICKNESS / 2)
        #  Circumference points
        pc1 = Vector(0, BLOCK_UNIT_QUARTER, 0)
        pc2 = Vector(0, -BLOCK_UNIT_QUARTER, 0)
        #  ---- Creamos líneas y arcos
        l1 = Part.LineSegment(p1, p2)
        c1 = Part.Arc(p2, pc1, p3)
        l2 = Part.LineSegment(p3, p4)
        c2 = Part.Arc(p4, pc2, p1)

        s = Part.Shape([l1, c1, l2, c2])
        shaft_wire = Part.Wire(s.Edges)
        hole_wire = Part.Wire(
            Part.Circle(Vector(0, 0, 0), Vector(1, 0, 0), DOWEL_SHAFT_HOLE_DIAMETER / 2).toShape()
        )  # center, normal, radius

        f = Part.Face([shaft_wire, hole_wire], "Part::FaceMakerCheese")

        return f.extrude(Vector(length, 0, 0))


class SFT_IDX(SFT):
    """Shaft indexing: have holes from start to finish separated by 1/4 BU."""

    def __init__(self, obj):
        super().__init__(obj)

    def onChanged(self, obj, prop: str):
        """Update properties"""
        if hasattr(self, "_updating") and self._updating:
            return  # Prevent recursion if already updating

        # NOTE: At the very moment a property is changed either via user change or via code update,
        # a call to onChanged() is triggered. This is a problem when we want to update a property
        # based on another property that has changed. To avoid recursion we can use the
        # self._updating flag to block property-changing code execution.
        self._updating = True
        try:
            if prop == "HolesNumber" and hasattr(obj, "Length"):
                obj.Length = obj.HolesNumber * 0.25
            if prop == "Length":
                obj.Length = round(4 * obj.Length) / 4  # multiple of 0.25
                obj.HolesNumber = int(obj.Length * 4)
        finally:
            self._updating = False  # Reset the flag after the update is done

    def execute(self, obj):
        p = self.shaft_shape(obj.HolesNumber * BLOCK_UNIT_QUARTER)

        for x in range(obj.HolesNumber):
            self.hole.Placement = FreeCAD.Placement(
                Vector((x + 0.5) * BLOCK_UNIT_QUARTER, 0, -DOWEL_SHAFT_THICKNESS / 2),
                FreeCAD.Rotation(),
            )
            p = p.cut(self.hole)

        obj.Code = f"Shaft IDX BU{obj.Length:05.2f}"

        obj.Shape = p


class SFT_PLN(SFT):
    """Shaft plain: 2 holes at the start, 2 holes at the end, 1 hole in the middle."""

    def __init__(self, obj):
        super().__init__(obj)
        obj.HolesNumber = (3, 1, 5, 1)  # (def, min, max step)
        obj.Length = (1, 0.5, 1000, 0.25)

    def onDocumentRestored(self, obj):
        """Implement migration for old version of shaft plain."""
        if not hasattr(obj, "Length"):  # old version
            # NOTE: The old plain shaft was in reality a indexing shaft
            # The migration method used is:
            # "Method 3. Migration when restoring the document, manually handling the properties"
            # from: https://wiki.freecad.org/Scripted_objects_migration

            SFT_IDX(obj)
            FreeCAD.Console.PrintWarning(
                translate("Log", "Shaft migration was successful, using new proxy class.\n")
            )

    def onChanged(self, obj, prop: str):
        """Update properties"""
        if hasattr(self, "_updating") and self._updating:
            return  # Prevent recursion if already updating

        self._updating = True  #  update in progress
        try:
            if prop == "HolesNumber" and hasattr(obj, "Length"):
                obj.Length = (obj.HolesNumber + 1) / 4
            if prop == "Length":
                obj.Length = round(4 * obj.Length) / 4  # multiple of 0.25
                obj.HolesNumber = 1 + int(obj.Length * 4) if obj.Length <= 1.25 else 5
        finally:
            self._updating = False  # Reset the flag after the update is done

    def execute(self, obj):
        # NOTE: case when Length=0.25BU with 1 hole is not implemented
        p = self.shaft_shape(obj.Length * BLOCK_UNIT)

        if obj.HolesNumber < 5:
            offset = 1
            list = range(obj.HolesNumber)
        else:
            offset = 0
            list = [
                1,
                2,
                int(obj.Length * 4) / 2,
                int(obj.Length * 4) - 1,
                int(obj.Length * 4) - 2,
            ]  # put 2 holes at the start, one in the middle and 2 at the end
        for x in list:
            self.hole.Placement = FreeCAD.Placement(
                Vector((x + offset) * BLOCK_UNIT_QUARTER, 0, -DOWEL_SHAFT_THICKNESS / 2),
                FreeCAD.Rotation(),
            )
            p = p.cut(self.hole)

        obj.Code = f"Shaft PLN BU{obj.Length:05.2f}"

        obj.Shape = p
