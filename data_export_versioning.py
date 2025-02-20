import bpy
import os
from bpy.types import Panel, Operator


class MY_PT_DataExportVersioningPanel(Panel):
    bl_label = "Data Export & Versioning"
    bl_idname = "MY_PT_DataExportVersioningPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "eli_lab Pipeline"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Automated Export
        layout.label(text="Automated Export:")
        layout.prop(scene, "eli_export_path", text="")
        layout.prop(scene, "eli_export_format", text="Format")
        layout.operator("eli.export_data", text="Export Data")

        # Incremental Save with Comments
        layout.label(text="Incremental Save with Comments:")
        layout.prop(scene, "eli_save_comment", text="")
        layout.operator("eli.incremental_save_comment", text="Incremental Save")


class MY_OT_ExportData(Operator):
    bl_idname = "eli.export_data"
    bl_label = "Export Data"
    bl_description = "Exports the scene data to the specified format."

    def execute(self, context):
        scene = context.scene
        export_format = scene.eli_export_format
        export_path = scene.eli_export_path
        if not export_path:
            self.report({"ERROR"}, "Please specify an export path.")
            return {"CANCELLED"}
        # Implement export logic based on format
        if export_format == "FBX":
            bpy.ops.export_scene.fbx(filepath=export_path)
        elif export_format == "OBJ":
            bpy.ops.export_scene.gltf(filepath=export_path)
        elif export_format == "GLTF":
            bpy.ops.export_scene.usdc(filepath=export_path)
        elif export_format == "USD":
            bpy.ops.export_scene.obj(filepath=export_path)
        elif export_format == "ALEMBIC":
            bpy.ops.wm.alembic_export(
                filepath=export_path,
                start=bpy.context.scene.frame_start,
                end=bpy.context.scene.frame_end,
                selection_only=False,
            )  # Export everything!

        self.report({"INFO"}, f"Exported data to {export_path} in {export_format} format.")
        return {"FINISHED"}


class MY_OT_IncrementalSaveComment(Operator):
    bl_idname = "eli.incremental_save_comment"
    bl_label = "Incremental Save"
    bl_description = "Saves the scene with an incremented version number and prompts for a comment."

    def execute(self, context):
        scene = context.scene
        comment = scene.eli_save_comment
        # Increment version number
        current_version = scene.eli_scene_version
        scene.eli_scene_version = current_version + 1

        # Save the file with an incremented name
        filepath = bpy.data.filepath
        if not filepath:
            filepath = "untitled.blend"  # or generate a unique filename

        dir, filename = os.path.split(filepath)
        name, ext = os.path.splitext(filename)
        new_filepath = os.path.join(dir, f"{name}_v{scene.eli_scene_version:03d}{ext}")
        try:
            bpy.ops.wm.save_as_mainfile(filepath=new_filepath, copy=True)
            self.report({"INFO"}, f"Scene saved as {new_filepath} with comment: {comment}")
        except Exception as e:
            self.report({"ERROR"}, f"Error saving scene: {e}")
            return {"CANCELLED"}
        return {"FINISHED"}
