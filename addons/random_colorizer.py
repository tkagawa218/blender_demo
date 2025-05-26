bl_info = {
    "name": "ランダムカラー適用ツール",
    "author": "あなたの名前",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3Dビュー > サイドバー > ツール",
    "description": "選択オブジェクトにランダムなマテリアル色を適用する",
    "category": "Object",
}

import bpy
import random

def generate_random_color():
    return (random.random(), random.random(), random.random(), 1)

def assign_random_color(obj):
    mat = bpy.data.materials.new(name="Mat_" + obj.name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = generate_random_color()

    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

class OBJECT_OT_ApplyRandomColors(bpy.types.Operator):
    bl_idname = "object.apply_random_colors"
    bl_label = "ランダムカラー適用"
    bl_description = "各オブジェクトにランダムな色のマテリアルを割り当てます"

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                assign_random_color(obj)
        return {'FINISHED'}

class VIEW3D_PT_RandomColorPanel(bpy.types.Panel):
    bl_label = "ランダムカラー"
    bl_idname = "VIEW3D_PT_random_color"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ツール'

    def draw(self, context):
        layout = self.layout
        layout.label(text="オブジェクトにカラーを適用")
        layout.operator("object.apply_random_colors", icon="COLOR")

classes = [
    OBJECT_OT_ApplyRandomColors,
    VIEW3D_PT_RandomColorPanel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
