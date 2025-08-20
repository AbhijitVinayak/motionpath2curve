bl_info = {
    "name": "Motion Path to Curve",
    "author": "ABJVNK",
    "version": (1, 0),
    "blender": (4, 5, 1),
    "location": "Properties Editor > Object Properties > Motion Paths",
    "description": "Convert object motion path to Bezier curve",
    "category": "Object",
}

import bpy

class OBJECT_OT_motion_path_to_curve(bpy.types.Operator):
    """Convert motion path of selected object to Bezier curve"""
    bl_idname = "object.motion_path_to_curve"
    bl_label = "Convert to Curve"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ob = context.object
        mp = ob.motion_path if ob else None
        if not mp:
            self.report({'WARNING'}, "Select an object with a calculated motion path")
            return {'CANCELLED'}

        curve_data = bpy.data.curves.new('MotionCurve', 'CURVE')
        curve_obj = bpy.data.objects.new('MotionCurveObj', curve_data)
        context.scene.collection.objects.link(curve_obj)

        curve_data.dimensions = '3D'
        spline = curve_data.splines.new('BEZIER')
        spline.bezier_points.add(len(mp.points) - 1)

        for i, bp in enumerate(spline.bezier_points):
            bp.co = mp.points[i].co
            bp.handle_right_type = 'AUTO'
            bp.handle_left_type = 'AUTO'

        return {'FINISHED'}

# Extend the existing Motion Paths panel instead of creating a new one
def draw_motion_to_curve_button(self, context):
    layout = self.layout
    layout.operator(OBJECT_OT_motion_path_to_curve.bl_idname, icon='CURVE_PATH')

def register():
    bpy.utils.register_class(OBJECT_OT_motion_path_to_curve)
    # Append the button drawing to the existing Motion Paths panel
    from bpy.types import OBJECT_PT_motion_paths
    OBJECT_PT_motion_paths.append(draw_motion_to_curve_button)

def unregister():
    from bpy.types import OBJECT_PT_motion_paths
    OBJECT_PT_motion_paths.remove(draw_motion_to_curve_button)
    bpy.utils.unregister_class(OBJECT_OT_motion_path_to_curve)

if __name__ == "__main__":
    register()
