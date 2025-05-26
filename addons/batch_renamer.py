bl_info = {
    "name": "一括リネームツール",
    "author": "あなたの名前",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3Dビュー > サイドバー > ツール",
    "description": "選択中のオブジェクトを一括でリネームするアドオン",
    "category": "Object",
}

import bpy

# プロパティグループ
class RenameToolProperties(bpy.types.PropertyGroup):
    prefix: bpy.props.StringProperty(name="Prefix", default="Obj_")
    suffix: bpy.props.StringProperty(name="Suffix", default="")
    use_numbering: bpy.props.BoolProperty(name="連番を付ける", default=True)
    start_index: bpy.props.IntProperty(name="開始番号", default=1, min=1)

# メイン処理
def batch_rename(props):
    selected = bpy.context.selected_objects
    existing_names = {obj.name for obj in bpy.data.objects}

    for i, obj in enumerate(selected):
        if props.use_numbering:
            base_name = f"{props.prefix}{str(i + props.start_index).zfill(3)}{props.suffix}"
        else:
            base_name = f"{props.prefix}{props.suffix}"

        new_name = base_name
        count = 1
        while new_name in existing_names:
            new_name = f"{base_name}_{count}"
            count += 1

        obj.name = new_name
        existing_names.add(new_name)

# ボタン押下時のオペレーター
class OBJECT_OT_BatchRename(bpy.types.Operator):
    bl_idname = "object.batch_rename"
    bl_label = "一括リネーム"
    bl_description = "選択中オブジェクトを指定パターンで一括リネーム"

    def execute(self, context):
        props = context.scene.rename_tool_props
        batch_rename(props)
        return {'FINISHED'}

# パネル表示
class VIEW3D_PT_BatchRenamePanel(bpy.types.Panel):
    bl_label = "一括リネームツール"
    bl_idname = "VIEW3D_PT_batch_rename"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ツール'

    def draw(self, context):
        layout = self.layout
        props = context.scene.rename_tool_props

        layout.prop(props, "prefix")
        layout.prop(props, "suffix")
        layout.prop(props, "use_numbering")
        layout.prop(props, "start_index")

        layout.operator("object.batch_rename", icon="FILE_REFRESH")

# 登録・解除
classes = [
    RenameToolProperties,
    OBJECT_OT_BatchRename,
    VIEW3D_PT_BatchRenamePanel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.rename_tool_props = bpy.props.PointerProperty(type=RenameToolProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.rename_tool_props

if __name__ == "__main__":
    register()
