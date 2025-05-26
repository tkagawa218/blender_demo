import bpy
import os

class EXPORT_OT_selected_fbx(bpy.types.Operator):
    bl_idname = "export.selected_fbx"
    bl_label = "Export Selected FBX"
    bl_description = "Export each selected object to an individual FBX file"
    bl_options = {'REGISTER', 'UNDO'}

    directory: bpy.props.StringProperty(
        name="Export Directory",
        description="Directory to export FBX files",
        subtype='DIR_PATH'
    )

    def execute(self, context):
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}

        for obj in selected_objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj

            export_path = os.path.join(self.directory, f"{obj.name}.fbx")
            bpy.ops.export_scene.fbx(
                filepath=export_path,
                use_selection=True,
                apply_unit_scale=True,
                bake_space_transform=True,
                object_types={'MESH'}
            )

        self.report({'INFO'}, f"Exported {len(selected_objects)} FBX files to: {self.directory}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def register():
    bpy.utils.register_class(EXPORT_OT_selected_fbx)

def unregister():
    bpy.utils.unregister_class(EXPORT_OT_selected_fbx)

if __name__ == "__main__":
    register()
