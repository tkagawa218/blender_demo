import bpy

class BatchRenamerOperator(bpy.types.Operator):
    bl_idname = "object.batch_rename"
    bl_label = "Batch Rename"
    bl_description = "Rename selected objects with prefix, suffix and numbering"
    bl_options = {'REGISTER', 'UNDO'}

    prefix: bpy.props.StringProperty(name="Prefix", default="Obj_")
    suffix: bpy.props.StringProperty(name="Suffix", default="")
    use_numbering: bpy.props.BoolProperty(name="Use Numbering", default=True)
    start_index: bpy.props.IntProperty(name="Start Index", default=1)

    def execute(self, context):
        selected = context.selected_objects
        for i, obj in enumerate(selected):
            new_name = self.prefix
            if self.use_numbering:
                new_name += str(i + self.start_index).zfill(3)
            obj.name = new_name + self.suffix
        return {'FINISHED'}

def register():
    bpy.utils.register_class(BatchRenamerOperator)

def unregister():
    bpy.utils.unregister_class(BatchRenamerOperator)

if __name__ == "__main__":
    register()
