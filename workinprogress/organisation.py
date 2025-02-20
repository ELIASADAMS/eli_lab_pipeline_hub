bl_info = {
    "name": "eli_lab pipeline",
    "blender": (4, 0, 2),
    "category": "3D View",
}

import bpy


def some_function():
    print("Organiser function executed.")


class OBJECTS_OT_organize(bpy.types.Operator):
    """Organize objects into collections"""
    bl_idname = "objects.organize"
    bl_label = "Organise Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Define collection names
        collection_names = ["Camera", "Mesh", "Light"]

        # Create collections if they do not exist
        collections = {}
        for name in collection_names:
            if name not in bpy.data.collections:
                collections[name] = bpy.data.collections.new(name)
                bpy.context.scene.collection.children.link(collections[name])
            else:
                collections[name] = bpy.data.collections[name]

        # Sort objects into the appropriate collections
        for obj in bpy.context.scene.objects:
            if obj.type == 'CAMERA':
                if obj.name not in collections["Camera"].objects:
                    collections["Camera"].objects.link(obj)
                    bpy.context.scene.collection.objects.unlink(obj)
            elif obj.type == 'MESH':
                if obj.name not in collections["Mesh"].objects:
                    collections["Mesh"].objects.link(obj)
                    bpy.context.scene.collection.objects.unlink(obj)
            elif obj.type == 'LIGHT':
                if obj.name not in collections["Light"].objects:
                    collections["Light"].objects.link(obj)
                    bpy.context.scene.collection.objects.unlink(obj)

        self.report({'INFO'}, "Collections created and objects sorted.")
        return {'FINISHED'}


class OBJECTS_OT_switch_textures(bpy.types.Operator):
    """Switch textures to PNG and purge unused data"""
    bl_idname = "objects.switch_textures"
    bl_label = "Switch Textures to PNG"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Loop through all images
        for img in bpy.data.images:
            # Change filepaths from different formats to .png
            if img.filepath.endswith(('.jpg', '.tga', '.exr', '.webp')):
                img.filepath = img.filepath.rsplit('.', 1)[0] + '.png'
                img.reload()  # Reload the image to apply changes

        self.report({'INFO'}, "Textures switched to PNG.")
        return {'FINISHED'}


class OBJECTS_OT_replace_interpolation(bpy.types.Operator):
    """Replace texture interpolation to Smart"""
    bl_idname = "objects.replace_interpolation"
    bl_label = "Replace Interpolation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            if obj.type == 'MESH':
                for mat_slot in obj.material_slots:
                    material = mat_slot.material
                    if material and material.use_nodes:
                        nodes = material.node_tree.nodes
                        for node in nodes:
                            if node.type == 'TEX_IMAGE':
                                node.interpolation = 'Smart'

        self.report({'INFO'}, "Texture interpolation replaced to Smart.")
        return {'FINISHED'}


class OBJECTS_OT_cleanup(bpy.types.Operator):
    """Cleanup unused data blocks"""
    bl_idname = "objects.cleanup"
    bl_label = "Cleanup Unused Data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # Cleanup unused data
        for action in bpy.data.actions:
            if action.users == 0 and not action.use_fake_user:
                bpy.data.actions.remove(action)

        for block in bpy.data.meshes:
            if block.users == 0:
                bpy.data.meshes.remove(block)

        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)

        for block in bpy.data.textures:
            if block.users == 0:
                bpy.data.textures.remove(block)

        for block in bpy.data.images:
            if block.users == 0:
                bpy.data.images.remove(block)

        for block in bpy.data.collections:
            if block.users == 0:
                bpy.data.collections.remove(block)

        for block in bpy.data.brushes:
            if block.users == 0:
                bpy.data.brushes.remove(block)

        for block in bpy.data.node_groups:
            if block.users == 0 and block.use_fake_user == 1:
                bpy.data.node_groups.remove(block)

        bpy.ops.outliner.orphans_purge(do_recursive=True)

        self.report({'INFO'}, "Cleanup completed.")
        return {'FINISHED'}


class VIEW3D_PT_organize_panel(bpy.types.Panel):
    """Creates a Panel in the 3D View"""
    bl_label = "Organize and Manage Assets"
    bl_idname = "VIEW3D_PT_organize"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Organize"

    def draw(self, context):
        layout = self.layout

        # Row for organizing objects
        row = layout.row()
        row.operator(OBJECTS_OT_organize.bl_idname)

        # Row for switching textures
        row = layout.row()
        row.operator(OBJECTS_OT_switch_textures.bl_idname)

        # Row for replacing interpolation
        row = layout.row()
        row.operator(OBJECTS_OT_replace_interpolation.bl_idname)

        # Row for cleanup
        row = layout.row()
        row.operator(OBJECTS_OT_cleanup.bl_idname)


def register():
    bpy.utils.register_class(OBJECTS_OT_organize)
    bpy.utils.register_class(OBJECTS_OT_switch_textures)
    bpy.utils.register_class(OBJECTS_OT_replace_interpolation)
    bpy.utils.register_class(OBJECTS_OT_cleanup)
    bpy.utils.register_class(VIEW3D_PT_organize_panel)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_organize_panel)
    bpy.utils.unregister_class(OBJECTS_OT_cleanup)
    bpy.utils.unregister_class(OBJECTS_OT_replace_interpolation)
    bpy.utils.unregister_class(OBJECTS_OT_switch_textures)
    bpy.utils.unregister_class(OBJECTS_OT_organize)


if __name__ == "__main__":
    register()
