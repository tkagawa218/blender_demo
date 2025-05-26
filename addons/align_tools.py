bl_info = {
    "name": "配置支援ツール",
    "author": "あなたの名前",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3Dビュー > サイドバー > ツール",
    "description": "オブジェクトの整列・ランダム配置をサポートする",
    "category": "Object",
}

import bpy
import random

# プロパティ
class PlacementToolProperties(bpy.types.PropertyGroup):
    align_axis: bpy.props.EnumProperty(
        name="整列軸",
        items=[
            ('X', "X", ""),
            ('Y', "Y", ""),
            ('Z', "Z", "")
        ],
        default='X'
    )
    random_range: bpy.props.FloatProperty(
        name="ランダム範囲 (+/-)",
        default=1.0,
        min=0.0,
        description="ランダムに動かす範囲（中心からの±値）"
    )

# 整列処理
def align_objects(axis):
    selected = bpy.context.selected_objects
    if len(selected) < 2:
        return

    reference = selected[0]
    ref_pos = reference.location

    for obj in selected[1:]:
        loc = obj.location.copy()
        if axis == 'X':
            loc.x = ref_pos.x
        elif axis == 'Y':
            loc.y = ref_pos.y
        elif axis == 'Z':
            loc.z = ref_pos.z
        obj.location = loc

# ランダム配置処理
def randomize_positions(range_val):
    selected = bpy.context.selected_objects
    for obj in selected:
        obj.location.x += random.uniform(-range_val, range_val)
        obj.location.y += random.uniform(-range_val, range_val)
        obj.location.z += random.uniform(-range_val, range_val)

# オペレーター：整列
class OBJECT_OT_AlignObjects(bpy.types.Operator):
    bl_idname = "object.align_objects"
    bl_label = "整列"
    bl_description = "選択オブジェクトを基準オブジェクトに整列"

    def execute(self, context):
        props = context.scene.placement_tool_props
        align_objects(props.align_axis)
        return {'FINISHED'}

# オペレーター：ランダム配置
class OBJECT_OT_RandomizeObjects(bpy.types.Operator):
    bl_idname = "object.randomize_objects"
    bl_label = "ランダム配置"
    bl_description = "選択オブジェクトをランダムに移動"

    def execute(self, context):
        props = context.scene.placement_tool_props
        randomize_positions(props.random_range)
        return {'FINISHED'}

# UIパネル
class VIEW3D_PT_PlacementToolPanel(bpy.types.Panel):
    bl_label = "配置支援ツール"
    bl_idname = "VIEW3D_PT_placement_tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ツール'

    def draw(self, context):
        layout = self.layout
        props = context.scene.placement_tool_props

        layout.label(text="整列")
        layout.prop(props, "align_axis", expand=True)
        layout.operator("object.align_objects", icon="ALIGN_LEFT")

        layout.separator()
        layout.label(text="ランダム配置")
        layout.prop(props, "random_range")
        layout.operator("object.randomize_objects", icon="MOD_NOISE")

# 登録
classes = [
    PlacementToolProperties,
    OBJECT_OT_AlignObjects,
    OBJECT_OT_RandomizeObjects,
    VIEW3D_PT_PlacementToolPanel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.placement_tool_props = bpy.props.PointerProperty(type=PlacementToolProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.placement_tool_props

if __name__ == "__main__":
    register()
