#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

import FreeCAD
import Part

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
from freecad.stemfie import BLOCK_UNIT, BLOCK_UNIT_HALF, BLOCK_UNIT_QUARTER
from pygears._functions import rotation, rotation3D

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP


# NOTE: To be able to generate gears using the Python classes
# from Gears WB we inherit from the original classes and perform
# some changes on the properties showed to users.


# TODO: Create hole according to gear size
stemfie_head = 0


def make_hole(obj) -> Part.Shape:
    if obj.num_teeth < 17:
        return Part.makeCylinder(
            1, BLOCK_UNIT_QUARTER, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1)
        )
    else:
        # TODO: replace boolean operation with single extrusion
        hole = Part.makeCylinder(
            BLOCK_UNIT_HALF + 0.1,
            BLOCK_UNIT_QUARTER,
            FreeCAD.Vector(0, 0, 0),
            FreeCAD.Vector(0, 0, 1),
        )  # radius, height, position, rotation
        hole = hole.cut(
            Part.makeCylinder(
                4.9, BLOCK_UNIT_QUARTER, FreeCAD.Vector(10, 0, 0), FreeCAD.Vector(0, 0, 1)
            )
        )
        hole = hole.cut(
            Part.makeCylinder(
                4.9, BLOCK_UNIT_QUARTER, FreeCAD.Vector(-10, 0, 0), FreeCAD.Vector(0, 0, 1)
            )
        )
        hole = hole.cut(
            Part.makeCylinder(
                4.9, BLOCK_UNIT_QUARTER, FreeCAD.Vector(0, 10, 0), FreeCAD.Vector(0, 0, 1)
            )
        )
        hole = hole.cut(
            Part.makeCylinder(
                4.9, BLOCK_UNIT_QUARTER, FreeCAD.Vector(0, -10, 0), FreeCAD.Vector(0, 0, 1)
            )
        )
    return hole


class InvoluteGear2(InvoluteGear):
    def __init__(self, obj):
        super().__init__(obj)
        # Make read-only some properties assigned on Gears WB
        for prop in ["height", "module"]:
            obj.setEditorMode(prop, 1)
        # Hide some properties assigned on Gears WB
        for prop in [
            "numpoints",
            "simple",
            "angular_backlash",
            "da",
            "df",
            "dw",  # pitch diameter
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

    # Override the original method to be able to modify the shape
    # - remove "simple shape" check
    def generate_gear_shape(self, obj):
        obj.gear.double_helix = obj.double_helix
        obj.gear.m_n = obj.module.Value
        obj.gear.undercut = obj.undercut
        obj.gear.shift = obj.shift
        obj.gear.pressure_angle = obj.pressure_angle.Value * np.pi / 180.0
        obj.gear.beta = obj.beta.Value * np.pi / 180
        obj.gear.clearance = obj.clearance
        obj.gear.backlash = obj.backlash.Value * (-obj.reversed_backlash + 0.5) * 2.0
        obj.gear.head = obj.head
        obj.gear.properties_from_tool = obj.properties_from_tool
        obj.gear.num_teeth = obj.num_teeth
        obj.height = str(BLOCK_UNIT_QUARTER) + "mm"

        obj.gear._update()
        self.compute_traverse_properties(obj)

        # Start chape creation
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

        # if obj.height.Value == 0: # not accessible, constant height
        #     return profile
        base = Part.Face(profile)
        if obj.beta.Value == 0:
            shape = base.extrude(FreeCAD.Vector(0, 0, obj.height.Value))
        else:
            twist_angle = obj.height.Value * np.tan(obj.gear.beta) * 2 / obj.gear.d
            shape = helical_extrusion(base, obj.height.Value, twist_angle, obj.double_helix)

        hole = make_hole(obj)
        # Now all gear shape has been created, now we add the hole
        return shape.cut(hole)


class BevelGear2(BevelGear):
    def __init__(self, obj):
        super().__init__(obj)
        # Hide some properties assigned on Gears WB
        for prop in [
            "numpoints",
            "angular_backlash",
            "dw",
            "backlash",
            "clearance",
            "version",
        ]:
            obj.setEditorMode(prop, 2)

    # The function is exactly the same as in original WB
    def generate_gear_shape(self, fp):
        fp.gear.z = fp.num_teeth
        fp.gear.module = fp.module.Value
        fp.gear.pressure_angle = (90 - fp.pressure_angle.Value) * np.pi / 180.0
        fp.gear.pitch_angle = fp.pitch_angle.Value * np.pi / 180
        max_height = fp.gear.module * fp.num_teeth / 2 / np.tan(fp.gear.pitch_angle)
        if fp.height >= max_height:
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
        for i in range(fp.num_teeth - 1):
            rotated_pts = list(map(rot, rotated_pts))
            pts.append(np.array([pts[-1][-1], rotated_pts[0][0]]))
            pts += rotated_pts
        pts.append(np.array([pts[-1][-1], pts[0][0]]))
        wires = []
        if not "version" in fp.PropertiesList:
            scale_0 = scale - fp.height.Value / 2
            scale_1 = scale + fp.height.Value / 2
        else:  # starting with version 0.0.2
            scale_0 = scale - fp.height.Value
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
        shape = Part.makeLoft(wires, True)
        if fp.reset_origin:
            mat = FreeCAD.Matrix()
            mat.A33 = -1
            mat.move(fcvec([0, 0, scale_1]))
            shape = shape.transformGeometry(mat)
        hole = make_hole(fp)
        return shape
        # return self.create_teeth(pts, pos1, fp.num_teeth)
