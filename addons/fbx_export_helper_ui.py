import bpy
import os

class EXPORT_OT_selected_fbx_adv(bpy.types.Operator):
    bl_idname = "export.selected_fbx_adv"
    bl_label = "Export Selected FBX (Advanced)"
    bl_description = "Export each selected object as FBX with options"
    bl_options = {'REGISTER', 'UNDO'}

    directory: bpy.props.StringProperty(
        name="Export Directory",
        description="Directory to export FBX files",
        subtype='DIR_PATH'
    )
    apply_unit_scale: bpy.props.BoolProperty(name="Apply Unit Scale", default=True)
    bake_space_transform: bpy.props.BoolProperty(name="Bake Space Transform", default=True)
    export_mesh: bpy.props.BoolProperty(name="Export Mesh", default=True)
    export_empty: bpy.props.BoolProperty(name="Export Empty", default=False)

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
            types = set()
            if self.export_mesh: types.add('MESH')
            if self.export_empty: types.add('EMPTY')

            bpy.ops.export_scene.fbx(
                filepath=export_path,
                use_selection=True,
                apply_unit_scale=self.apply_unit_scale,
                bake_space_transform=self.bake_space_transform,
                object_types=types
            )

        self.report({'INFO'}, f"Exported {len(selected_objects)} FBX files.")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class EXPORT_PT_fbx_export_ui(bpy.types.Panel):
    bl_label = "FBX Export Helper"
    bl_idname = "EXPORT_PT_fbx_export_ui"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Export Tools'

    def draw(self, context):
        layout = self.layout
        layout.operator("export.selected_fbx_adv")

def register():
    bpy.utils.register_class(EXPORT_OT_selected_fbx_adv)
    bpy.utils.register_class(EXPORT_PT_fbx_export_ui)

def unregister():
    bpy.utils.unregister_class(EXPORT_OT_selected_fbx_adv)
    bpy.utils.unregister_class(EXPORT_PT_fbx_export_ui)

if __name__ == "__main__":
    register()
