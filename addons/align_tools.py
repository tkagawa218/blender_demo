import bpy

class OBJECT_OT_align_objects(bpy.types.Operator):
    bl_idname = "object.align_objects"
    bl_label = "Align Objects"
    bl_description = "Align selected objects along a chosen axis"

    axis: bpy.props.EnumProperty(
        name="Axis",
        items=[('X', "X Axis", ""), ('Y', "Y Axis", ""), ('Z', "Z Axis", "")],
        default='X'
    )

    def execute(self, context):
        selected = context.selected_objects
        if not selected:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}

        ref_location = selected[0].location
        for obj in selected[1:]:
            if self.axis == 'X':
                obj.location.x = ref_location.x
            elif self.axis == 'Y':
                obj.location.y = ref_location.y
            elif self.axis == 'Z':
                obj.location.z = ref_location.z

        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_align_objects)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_align_objects)

if __name__ == "__main__":
    register()
