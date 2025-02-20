import bpy
import os
from bpy.types import Panel, Operator


class MY_PT_SceneManagementPanel(Panel):
    bl_label = "Scene Management"
    bl_idname = "MY_PT_SceneManagementPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "eli_lab Pipeline"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Project Presets
        layout.label(text="Project Presets:")
        layout.prop(scene, "eli_project_presets_path", text="")
        layout.operator("eli.apply_project_preset", text="Apply Project Preset")

        # Hierarchy Management
        layout.label(text="Hierarchy Management:")
        layout.operator("eli.organize_hierarchy", text="Organize Hierarchy")

        # Naming Conventions
        layout.label(text="Naming Conventions:")
        layout.operator("eli.batch_rename", text="Batch Rename")

        # Scene Actions
        box = layout.box()
        box.label(text="Scene Actions")
        box.operator("eli.save_scene", text="Save Scene")
        box.operator("eli.open_scene", text="Open Scene")
        box.operator("eli.increment_save", text="Increment and Save")

        # Versioning UI elements
        layout.label(text="Scene Version:")
        layout.prop(scene, "eli_scene_version", text="")
        row = layout.row(align=True)
        row.operator("eli.increment_version", text="Increment", icon="TRIA_UP")
        row.operator("eli.decrement_version", text="Decrement", icon="TRIA_DOWN")


class MY_OT_ApplyProjectPreset(Operator):
    bl_idname = "eli.apply_project_preset"
    bl_label = "Apply Project Preset"
    bl_description = "Applies the settings from the project preset file."

    def execute(self, context):
        scene = context.scene
        filepath = scene.eli_project_presets_path
        if os.path.exists(filepath):
            try:
                bpy.ops.wm.open_mainfile(filepath=filepath)
                self.report({"INFO"}, f"Applied project preset: {filepath}")
            except Exception as e:
                self.report({"ERROR"}, f"Error applying project preset: {e}")
        else:
            self.report({"ERROR"}, f"Project preset file not found: {filepath}")
        return {"FINISHED"}


class MY_OT_OrganizeHierarchy(Operator):
    bl_idname = "eli.organize_hierarchy"
    bl_label = "Organize Hierarchy"
    bl_description = "Automatically organizes objects into collections based on rules."

    def execute(self, context):
        # Implement hierarchy organization logic here based on object type, material, name, etc.
        # Use bpy.data.collections and bpy.context.scene.collection.children.link(new_collection)
        # Example:
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                col = utils.create_collection_if_not_exists("Meshes")
                utils.safe_collection_link(obj, col)
        self.report({"INFO"}, "Organized hierarchy.")
        return {"FINISHED"}


class MY_OT_BatchRename(Operator):
    bl_idname = "eli.batch_rename"
    bl_label = "Batch Rename"
    bl_description = "Applies naming conventions to existing assets."

    def execute(self, context):
        # Implement batch renaming logic here based on naming templates
        # Example:
        for obj in bpy.context.selected_objects:
            obj.name = f"Renamed_{obj.name}"
        self.report({"INFO"}, "Batch renaming completed.")
        return {"FINISHED"}


class MY_OT_SaveScene(Operator):
    bl_label = "Save Scene"
    bl_idname = "eli.save_scene"
    bl_description = "Saves the current scene."

    def execute(self, context):
        print("Saving scene...")
        bpy.ops.wm.save_mainfile()
        self.report({"INFO"}, "Scene saved.")
        return {"FINISHED"}


class MY_OT_OpenScene(Operator):
    bl_label = "Open Scene"
    bl_idname = "eli.open_scene"
    bl_description = "Opens a scene from disk."

    def execute(self, context):
        print("Opening scene...")
        bpy.ops.wm.open_mainfile()
        self.report({"INFO"}, "Scene opened.")
        return {"FINISHED"}


class MY_OT_IncrementSave(Operator):
    bl_label = "Increment and Save"
    bl_idname = "eli.increment_save"
    bl_description = "Increment the scene version and save."

    def execute(self, context):
        scene = context.scene
        current_version = scene.eli_scene_version
        scene.eli_scene_version = current_version + 1
        bpy.ops.wm.save_mainfile()
        self.report({"INFO"}, f"Scene incremented to version {scene.eli_scene_version} and saved.")
        return {"FINISHED"}


class MY_OT_IncrementVersion(Operator):
    bl_label = "Increment Version"
    bl_idname = "eli.increment_version"
    bl_description = "Increment the scene version."

    def execute(self, context):
        scene = context.scene
        scene.eli_scene_version += 1
        return {"FINISHED"}


class MY_OT_DecrementVersion(Operator):
    bl_label = "Decrement Version"
    bl_idname = "eli.decrement_version"
    bl_description = "Decrement the scene version."

    def execute(self, context):
        scene = context.scene
        scene.eli_scene_version = max(0, scene.eli_scene_version - 1)
        return {"FINISHED"}