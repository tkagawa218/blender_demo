bl_info = {
    "name": "FBX出力支援ツール",
    "author": "あなたの名前",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3Dビュー > サイドバー > 出力",
    "description": "選択オブジェクトを個別にFBXでエクスポートします",
    "category": "Import-Export",
}

import bpy
import os
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper

class EXPORT_OT_fbx_selected(bpy.types.Operator, ExportHelper):
    bl_idname = "export_scene.fbx_selected"
    bl_label = "選択をFBX出力"
    bl_description = "選択中のオブジェクトを個別のFBXファイルでエクスポートします"

    filename_ext = ".fbx"
    use_filter_folder = True

    def execute(self, context):
        export_dir = os.path.dirname(self.filepath)
        selected_objects = context.selected_objects

        if not selected_objects:
            self.report({'WARNING'}, "何も選択されていません")
            return {'CANCELLED'}

        for obj in selected_objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj

            export_path = os.path.join(export_dir, f"{obj.name}.fbx")

            bpy.ops.export_scene.fbx(
                filepath=export_path,
                use_selection=True,
                global_scale=1.0,
                apply_unit_scale=True,
                bake_space_transform=True,
                object_types={'MESH'},
                use_mesh_modifiers=True,
                use_anim=False,
                axis_forward='-Z',
                axis_up='Y',
            )

            self.report({'INFO'}, f"出力: {export_path}")

        return {'FINISHED'}

class VIEW3D_PT_fbx_export_panel(bpy.types.Panel):
    bl_label = "FBX出力支援"
    bl_idname = "VIEW3D_PT_fbx_export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '出力'

    def draw(self, context):
        layout = self.layout
        layout.label(text="FBX個別出力")
        layout.operator("export_scene.fbx_selected", icon="EXPORT")

classes = [EXPORT_OT_fbx_selected, VIEW3D_PT_fbx_export_panel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
