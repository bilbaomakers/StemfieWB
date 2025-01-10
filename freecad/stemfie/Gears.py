from math import tan

import FreeCAD
import numpy as np
import Part
from pygears._functions import rotation, rotation3D

from freecad.gears.basegear import (
    fcvec,
    helical_extrusion,
    insert_fillet,
    make_bspline_wire,
    points_to_wire,
    rotate_tooth,
)
from freecad.gears.bevelgear import BevelGear
from freecad.gears.involutegear import InvoluteGear
from freecad.stemfie.utils import BLOCK_UNIT, make_stemfie_shape

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP


# NOTE: To be able to generate gears using the Python classes
# from Gears WB we inherit from the original classes and perform
# some changes on the properties showed to users.


def make_gear_hole(simple_hole, height, radius: float = 1) -> Part.Shape:
    """Create a simple/STEMFIE hole into a gear shape."""
    if simple_hole:
        return Part.makeCylinder(radius, height, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    else:
        return make_stemfie_shape(height)


class GWH(InvoluteGear):
    def __init__(self, obj):
        super().__init__(obj)
        # Make read-only some properties assigned on Gears WB
        obj.setEditorMode("module", 1)
        # Hide some properties assigned on Gears WB
        for prop in [
            "numpoints",
            "simple",
            "angular_backlash",
            "addendum_diameter",
            "root_diameter",
            "pitch_diameter",
            "transverse_pitch",
            "traverse_module",
            "backlash",
            "clearance",
            "head",
            "reversed_backlash",
            "head_fillet",
            "root_fillet",
            "undercut",
            "version",
        ]:
            obj.setEditorMode(prop, 2)

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
        # Override the original height property from Gears WB
        obj.removeProperty("height")
        obj.addProperty(
            "App::PropertyFloatConstraint",
            QT_TRANSLATE_NOOP("App::Property", "height"),
            "base",  # to be in the same group as in Gear WB
            QT_TRANSLATE_NOOP(
                "App::Property", "Gear height in terms of Block Units (BU)\n1 BU=12.5 mm"
            ),
        ).height = (0.5, 0.25, 1, 0.25)

    # Override the original method to be able to modify the shape
    # - remove "simple shape" check
    # - use new height definition
    def generate_gear_shape(self, obj):
        obj.gear.double_helix = obj.double_helix
        obj.gear.m_n = obj.module.Value
        obj.gear.undercut = obj.undercut
        obj.gear.shift = obj.shift
        obj.gear.pressure_angle = obj.pressure_angle.Value * np.pi / 180.0
        obj.gear.beta = obj.helix_angle.Value * np.pi / 180
        obj.gear.clearance = obj.clearance
        obj.gear.backlash = obj.backlash.Value * (-obj.reversed_backlash + 0.5) * 2.0
        obj.gear.head = obj.head
        obj.gear.properties_from_tool = obj.properties_from_tool
        obj.gear.num_teeth = obj.num_teeth

        obj.gear._update()
        self.compute_traverse_properties(obj)

        # Start shape creation
        pts = obj.gear.points(num=obj.numpoints)  # TODO: find a good value (20)
        rot = rotation(obj.gear.phipart)
        rotated_pts = list(map(rot, pts))
        pts.append([pts[-1][-1], rotated_pts[0][0]])
        pts += rotated_pts
        tooth = points_to_wire(pts)
        edges = tooth.Edges

        # head-fillet:
        r_head = float(obj.head_fillet * obj.module)
        r_root = float(obj.root_fillet * obj.module)
        if obj.undercut and r_root != 0.0:
            r_root = 0.0
            FreeCAD.Console.PrintWarning("root fillet is not allowed if undercut is computed")
        if len(tooth.Edges) == 11:
            pos_head = [1, 3, 9]
            pos_root = [6, 8]
            edge_range = [2, 12]
        else:
            pos_head = [0, 2, 6]
            pos_root = [4, 6]
            edge_range = [1, 9]

        for pos in pos_head:
            edges = insert_fillet(edges, pos, r_head)

        for pos in pos_root:
            try:
                edges = insert_fillet(edges, pos, r_root)
            except RuntimeError:
                edges.pop(8)
                edges.pop(6)
                edge_range = [2, 10]
                pos_root = [5, 7]
                for pos in pos_root:
                    edges = insert_fillet(edges, pos, r_root)
                break
        edges = edges[edge_range[0] : edge_range[1]]
        edges = [e for e in edges if e is not None]

        tooth = Part.Wire(edges)
        profile = rotate_tooth(tooth, obj.num_teeth)

        base = Part.Face(profile)
        if obj.gear.beta == 0:
            gear_shape = base.extrude(FreeCAD.Vector(0, 0, obj.height * BLOCK_UNIT))
        else:
            twist_angle = obj.height * BLOCK_UNIT * np.tan(obj.gear.beta) * 2 / obj.gear.d
            gear_shape = helical_extrusion(
                base, obj.height * BLOCK_UNIT, twist_angle, obj.double_helix
            )

        # Now all gear shape has been created, now we add the hole
        hole = make_gear_hole(obj.pitch_diameter.Value < 17, obj.height * BLOCK_UNIT)

        diam = "2.0mm" if obj.pitch_diameter.Value < 17 else "-STH"
        obj.Code = f"Gear Wheel PLN TTH{obj.num_teeth:02} BU{obj.height:05.02} SFT{diam}"

        return gear_shape.cut(hole)


class GRB(BevelGear):
    def __init__(self, obj):
        super().__init__(obj)
        # Make read-only some properties assigned on Gears WB
        obj.setEditorMode("module", 1)
        # Hide some properties assigned on Gears WB
        for prop in [
            "numpoints",
            "angular_backlash",
            "dw",  # pitch diameter
            "backlash",
            "clearance",
            "version",
        ]:
            obj.setEditorMode(prop, 2)

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
        # Override the original height property from Gears WB
        obj.removeProperty("height")
        obj.addProperty(
            "App::PropertyFloatConstraint",
            QT_TRANSLATE_NOOP("App::Property", "height"),
            "base",  # to be in the same group as in Gear WB
            QT_TRANSLATE_NOOP(
                "App::Property", "Gear height in terms of Block Units (BU)\n1 BU=12.5 mm"
            ),
        ).height = (0.5, 0.25, 1, 0.25)

    # NOTE: function must be named "generate_gear_shape" as is run in the
    # Gears WB execute() method

    # Override the original method to be able to modify the shape
    # - simplify scale
    # - use new height definition
    def generate_gear_shape(self, fp):
        fp.gear.z = fp.num_teeth
        fp.gear.module = fp.module.Value
        fp.gear.pressure_angle = (90 - fp.pressure_angle.Value) * np.pi / 180.0
        fp.gear.pitch_angle = fp.pitch_angle.Value * np.pi / 180
        max_height = fp.gear.module * fp.num_teeth / 2 / np.tan(fp.gear.pitch_angle)
        if fp.height * BLOCK_UNIT >= max_height:
            FreeCAD.Console.PrintWarning("height must be smaller than {}".format(max_height))
        fp.gear.backlash = fp.backlash.Value
        scale = fp.module.Value * fp.num_teeth / 2 / np.tan(fp.pitch_angle.Value * np.pi / 180)
        fp.gear.clearance = fp.clearance / scale
        fp.gear._update()
        pts = list(fp.gear.points(num=fp.numpoints))
        rot = rotation3D(-2 * np.pi / fp.num_teeth)
        # if fp.beta.Value != 0:
        #     pts = [np.array([self.spherical_rot(j, fp.beta.Value * np.pi / 180.) for j in i]) for i in pts]

        rotated_pts = pts
        for _ in range(fp.num_teeth - 1):
            rotated_pts = list(map(rot, rotated_pts))
            pts.append(np.array([pts[-1][-1], rotated_pts[0][0]]))
            pts += rotated_pts
        pts.append(np.array([pts[-1][-1], pts[0][0]]))
        wires = []

        # adapter from Gears WB
        scale_0 = scale - fp.height * BLOCK_UNIT
        scale_1 = scale

        if fp.beta.Value == 0:
            wires.append(make_bspline_wire([scale_0 * p for p in pts]))
            wires.append(make_bspline_wire([scale_1 * p for p in pts]))
        else:
            for scale_i in np.linspace(scale_0, scale_1, 20):
                # beta_i = (scale_i - scale_0) * fp.beta.Value * np.pi / 180
                # rot = rotation3D(- beta_i)
                # points = [rot(pt) * scale_i for pt in pts]
                angle = (
                    fp.beta.Value
                    * np.pi
                    / 180.0
                    * np.sin(np.pi / 4)
                    / np.sin(fp.pitch_angle.Value * np.pi / 180.0)
                )
                points = [
                    np.array([self.spherical_rot(p, angle) for p in scale_i * pt]) for pt in pts
                ]
                wires.append(make_bspline_wire(points))
                Part.show(make_bspline_wire(points))

        shape = Part.makeLoft(wires, True)
        if fp.reset_origin:
            mat = FreeCAD.Matrix()
            mat.A33 = -1
            mat.move(fcvec([0, 0, scale_1]))
            shape = shape.transformGeometry(mat)

        top_d = fp.dw.Value - 2 * fp.height * BLOCK_UNIT * tan(fp.pitch_angle.Value * np.pi / 180)
        if top_d > 4:  # only create hole if there is space
            hole = make_gear_hole(top_d < 16, fp.height * BLOCK_UNIT)
            shape = shape.cut(hole)

        diam = "2.0mm" if top_d < 16 else "-STH"
        fp.Code = f"Gear Bevel PLN TTH{fp.num_teeth:02} BU{fp.height:05.02} SFT{diam} {fp.pitch_angle.Value}°"

        return shape
