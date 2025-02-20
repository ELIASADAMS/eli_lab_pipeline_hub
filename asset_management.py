import bpy
from bpy.types import Panel, Operator


class MY_PT_AssetManagementPanel(Panel):
    bl_label = "Asset Management"
    bl_idname = "MY_PT_AssetManagement"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "eli_lab Pipeline"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Asset Path
        layout.label(text="Asset Path:")
        layout.prop(scene, "eli_asset_path", text="")

        # Asset Actions
        box = layout.box()
        box.label(text="Asset Actions")
        box.operator("eli.import_asset", text="Import Asset")
        box.operator("eli.export_asset", text="Export Asset")
        box.operator("eli.publish_asset", text="Publish Asset")
        box.operator("eli.replace_with_linked", text="Replace With Linked")  # NEW
        # Asset Type Dropdown
        layout.label(text="Asset Type:")
        layout.prop(scene, "eli_asset_type", text="")


class MY_OT_ImportAsset(Operator):
    bl_label = "Import Asset"
    bl_idname = "eli.import_asset"
    bl_description = "Imports an asset from the asset library."

    def execute(self, context):
        asset_path = context.scene.eli_asset_path
        asset_type = context.scene.eli_asset_type
        print(f"Importing asset from: {asset_path} of type: {asset_type}")
        self.report({"INFO"}, "Importing asset...")
        return {"FINISHED"}


class MY_OT_ExportAsset(Operator):
    bl_label = "Export Asset"
    bl_idname = "eli.export_asset"
    bl_description = "Exports the selected object as an asset."

    def execute(self, context):
        print("Exporting asset...")
        self.report({"INFO"}, "Exporting asset...")
        return {"FINISHED"}


class MY_OT_PublishAsset(Operator):
    bl_label = "Publish Asset"
    bl_idname = "eli.publish_asset"
    bl_description = "Publishes the current scene."

    def execute(self, context):
        # Implement logic to publish the asset (versioning, previews, etc.)
        print("Publishing asset...")
        self.report({"INFO"}, "Publishing asset...")
        return {"FINISHED"}


class MY_OT_ReplaceWithLinked(Operator):
    bl_idname = "eli.replace_with_linked"
    bl_label = "Replace With Linked"
    bl_description = "Replaces selected objects with linked assets from the library."

    def execute(self, context):
        # Implement the replace with linked functionality here

        # Get selected objects
        selected_objects = bpy.context.selected_objects
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}

        asset_path = context.scene.eli_asset_path

        # Check if the Library Exists

        # Iterate over all selected objects
        for obj in selected_objects:
            # Unlink the object
            bpy.data.objects.remove(obj)
            # Link the object into the scene
            bpy.ops.wm.link(filepath=asset_path)
        return {"FINISHED"}
