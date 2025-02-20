import bpy
from bpy.types import Panel, Operator, UIList
from bpy.props import StringProperty, CollectionProperty, IntProperty


class LightingPresetItem(bpy.types.PropertyGroup):
    name: StringProperty(name="Preset Name")
    filepath: StringProperty(name="File Path", subtype='FILE_PATH')
    # Add any other relevant lighting settings as properties here.

class UI_UL_lighting_preset_list(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Draw each item in the list
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon='LIGHT') # Or use a real icon
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='LIGHT')

class MY_PT_LightingRenderingPanel(Panel):
    bl_label = "Lighting & Rendering"
    bl_idname = "MY_PT_LightingRenderingPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "eli_lab Pipeline"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Lighting Presets
        layout.label(text="Lighting Presets:")
        row = layout.row()
        row.template_list(
            "UI_UL_lighting_preset_list",
            "Lighting Presets",
            scene,
            "eli_lighting_presets",
            scene,
            "eli_lighting_presets_index",
        )

        # Preset Actions
        box = layout.box()
        box.label(text="Preset Actions")
        col = box.column(align=True)
        col.operator("eli.add_lighting_preset", text="Add Preset")
        col.operator("eli.remove_lighting_preset", text="Remove Preset")
        col.operator("eli.apply_lighting_preset", text="Apply Preset")

        # Remove Render Queue Management from here
        #layout.label(text="Render Queue Management:")
        #layout.operator("eli.add_render_to_queue", text="Add to Render Queue")
        #layout.operator("eli.start_render_queue", text="Start Render Queue")


class MY_OT_AddLightingPreset(Operator):
    bl_idname = "eli.add_lighting_preset"
    bl_label = "Add Preset"
    bl_description = "Adds a new lighting preset to the list."

    def execute(self, context):
        scene = context.scene
        new_preset = scene.eli_lighting_presets.add()
        new_preset.name = "New Preset"
        new_preset.filepath = ""
        # You might also initialize other lighting settings here
        return {"FINISHED"}


class MY_OT_RemoveLightingPreset(Operator):
    bl_idname = "eli.remove_lighting_preset"
    bl_label = "Remove Preset"
    bl_description = "Removes the selected lighting preset from the list."

    def execute(self, context):
        scene = context.scene
        list_index = scene.eli_lighting_presets_index
        if scene.eli_lighting_presets:
            scene.eli_lighting_presets.remove(list_index)
            scene.eli_lighting_presets_index = min(
                max(0, list_index - 1), len(scene.eli_lighting_presets) - 1
            )
        return {"FINISHED"}


class MY_OT_ApplyLightingPreset(Operator):
    bl_idname = "eli.apply_lighting_preset"
    bl_label = "Apply Preset"
    bl_description = "Applies the selected lighting preset to the scene."

    def execute(self, context):
        scene = context.scene
        list_index = scene.eli_lighting_presets_index
        if scene.eli_lighting_presets:
            preset = scene.eli_lighting_presets[list_index]
            filepath = preset.filepath
            if filepath and bpy.data.filepath: #If loading from scene file
                try:

                    #This is just an example:
                    #load lights only:
                    with bpy.data.libraries.load(filepath, link=False, relative=False) as (data_from, data_to):
                        data_to.lights = data_from.lights
                        for light in data_to.lights:
                            bpy.context.collection.objects.link(light) #Link to scene
                        self.report({'INFO'}, f"Applied lighting preset: {preset.name}")
                except Exception as e:
                    self.report({"ERROR"}, f"Error applying lighting preset: {e}")
            else: #Loading from a blend file
                 self.report({"ERROR"}, f"Apply lighting preset: {preset.name}. No File Path")
        return {"FINISHED"}