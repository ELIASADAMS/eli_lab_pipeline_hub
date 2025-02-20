import bpy
from bpy.types import Panel, Operator, UIList


class UI_UL_list(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name)


class MY_PT_SceneSetupPanel(Panel):
    bl_label = "Scene Setup"
    bl_idname = "MY_PT_SceneSetupPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "eli_lab Pipeline"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Project Presets
        layout.label(text="Project Presets:")
        layout.prop(scene, "eli_project_presets_path", text="")

        # Preset List
        layout.label(text="Available Presets:")
        row = layout.row()
        row.template_list(
            "UI_UL_list",
            "Project Presets",
            scene,
            "eli_project_presets",
            scene,
            "eli_project_presets_index",
        )

        # Preset Actions
        box = layout.box()
        box.label(text="Preset Actions")
        col = box.column(align=True)
        col.operator("eli.add_project_preset", text="Add Preset")
        col.operator("eli.remove_project_preset", text="Remove Preset")
        col.operator("eli.apply_project_preset", text="Apply Preset")

        # Unit Conversion
        layout.label(text="Unit Conversion:")
        layout.prop(scene, "eli_preferred_units", text="")
        layout.operator("eli.convert_units", text="Convert Units")

        # Collection Setup
        layout.label(text="Collection Setup:")
        layout.operator("eli.setup_collections", text="Setup Collections")


class MY_OT_AddProjectPreset(Operator):
    bl_idname = "eli.add_project_preset"
    bl_label = "Add Project Preset"
    bl_description = "Adds a new project preset to the list."

    def execute(self, context):
        scene = context.scene
        new_item = scene.eli_project_presets.add()
        new_item.name = "New Preset"
        new_item.filepath = ""
        return {"FINISHED"}


class MY_OT_RemoveProjectPreset(Operator):
    bl_idname = "eli.remove_project_preset"
    bl_label = "Remove Project Preset"
    bl_description = "Removes the selected project preset from the list."

    def execute(self, context):
        scene = context.scene
        list_index = scene.eli_project_presets_index
        if scene.eli_project_presets:
            scene.eli_project_presets.remove(list_index)
            scene.eli_project_presets_index = min(
                max(0, list_index - 1), len(scene.eli_project_presets) - 1
            )
        return {"FINISHED"}


class MY_OT_ApplyProjectPreset(Operator):
    bl_idname = "eli.apply_project_preset"
    bl_label = "Apply Project Preset"
    bl_description = "Applies the settings from the selected project preset."

    def execute(self, context):
        scene = context.scene
        list_index = scene.eli_project_presets_index
        if scene.eli_project_presets:
            preset = scene.eli_project_presets[list_index]
            filepath = preset.filepath
            if os.path.exists(filepath):
                try:
                    bpy.ops.wm.open_mainfile(filepath=filepath)
                    self.report({"INFO"}, f"Applied preset: {preset.name}")
                except Exception as e:
                    self.report({"ERROR"}, f"Error applying preset: {e}")
            else:
                self.report({"ERROR"}, f"Preset file not found: {filepath}")
        return {"FINISHED"}


class MY_OT_ConvertUnits(Operator):
    bl_idname = "eli.convert_units"
    bl_label = "Convert Units"
    bl_description = "Converts scene units to the preferred standard."

    def execute(self, context):
        scene = context.scene
        preferred_units = scene.eli_preferred_units
        # Implement unit conversion logic based on preferred_units
        if preferred_units == "METERS":
            bpy.context.scene.unit_settings.system = "METRIC"
            bpy.context.scene.unit_settings.scale_length = 1.0
        elif preferred_units == "CENTIMETERS":
            bpy.context.scene.unit_settings.system = "METRIC"
            bpy.context.scene.unit_settings.scale_length = 0.01
        elif preferred_units == "INCHES":
            bpy.context.scene.unit_settings.system = "IMPERIAL"  # Closest equivalent

        self.report({"INFO"}, f"Converted units to {preferred_units}")
        return {"FINISHED"}


class MY_OT_SetupCollections(Operator):
    bl_idname = "eli.setup_collections"
    bl_label = "Setup Collections"
    bl_description = "Sets up standard collections with predefined naming conventions."

    def execute(self, context):
        # Define standard collection names
        collection_names = ["Camera", "Mesh", "Light", "Rig", "Environment", "FX"]

        # Create collections if they don't exist
        for name in collection_names:
            if name not in bpy.data.collections:
                new_collection = bpy.data.collections.new(name)
                bpy.context.scene.collection.children.link(new_collection)

        self.report({"INFO"}, "Setup standard collections.")
        return {"FINISHED"}
