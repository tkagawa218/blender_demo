import bpy
import random

class OBJECT_OT_random_color(bpy.types.Operator):
    bl_idname = "object.random_color"
    bl_label = "Apply Random Colors"
    bl_description = "Assign random colors to selected objects"

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                if not obj.data.materials:
                    mat = bpy.data.materials.new(name="RandomColor")
                    obj.data.materials.append(mat)
                else:
                    mat = obj.data.materials[0]

                mat.use_nodes = True
                bsdf = mat.node_tree.nodes.get("Principled BSDF")
                if bsdf:
                    color = (random.random(), random.random(), random.random(), 1)
                    bsdf.inputs['Base Color'].default_value = color
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_random_color)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_random_color)

if __name__ == "__main__":
    register()
