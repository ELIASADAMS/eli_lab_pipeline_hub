import bpy
import os
import subprocess
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty, BoolProperty, IntProperty, EnumProperty, CollectionProperty

# --- Render Queue Item ---
class RenderQueueItem(PropertyGroup):
    scene_file: StringProperty(
        name="Scene File",
        subtype="FILE_PATH",
        description="Path to the Blender scene file to render"
    )
    camera_name: StringProperty(
        name="Camera",
        description="Name of the camera to use for rendering"
    )
    resolution_x: IntProperty(
        name="Resolution X",
        default=1920,
        description="Render resolution X"
    )
    resolution_y: IntProperty(
        name="Resolution Y",
        default=1080,
        description="Render resolution Y"
    )
    samples: IntProperty(
        name="Samples",
        default=64,
        description="Render samples"
    )
    output_path: StringProperty(
        name="Output Path",
        subtype="DIR_PATH",
        description="Path to save the rendered output"
    )
    render_engine: EnumProperty(
        name="Render Engine",
        items=[
            ("BLENDER_EEVEE", "Eevee", "Use the Eevee render engine"),
            ("CYCLES", "Cycles", "Use the Cycles render engine"),
        ],
        description="Render engine to use"
    )
# --- UI List ---
class UI_UL_render_queue(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name, icon='RENDER_ANIMATION') #Or other icon!

# --- Render Management Panel ---
class MY_PT_RenderManagementPanel(Panel):
    bl_label = "Render Management"
    bl_idname = "MY_PT_RenderManagementPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "eli_lab Pipeline"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Render Queue
        layout.label(text="Render Queue:")
        row = layout.row()
        row.template_list("UI_UL_render_queue", "Render Queue", scene, "eli_render_queue", scene, "eli_render_queue_index")
        #Render Queue Operations
        split = layout.split()
        col = split.column(align=True)
        col.operator("eli.add_render_queue_item", icon="ADD", text="")
        col.operator("eli.remove_render_queue_item", icon="REMOVE", text="")

        # Render Settings
        if scene.eli_render_queue_index >= 0 and scene.eli_render_queue:
            queue_item = scene.eli_render_queue[scene.eli_render_queue_index]
            box = layout.box()
            box.label(text="Queue Item Settings")
            box.prop(queue_item, "scene_file")
            box.prop(queue_item, "camera_name")
            box.prop(queue_item, "resolution_x")
            box.prop(queue_item, "resolution_y")
            box.prop(queue_item, "samples")
            box.prop(queue_item, "output_path")
            box.prop(queue_item, "render_engine")

        # Render Actions
        layout.label(text="Render Actions")
        layout.operator("eli.start_render_queue", text="Start Render Queue")
        layout.operator("eli.open_output_dir", text="Open Output Directory")
        layout.operator("eli.start_render", text="Start Render (Current Scene)") #Adding the option to render the current scene
        layout.operator("eli.start_render_background", text="Start Render Background") #Adding the option to render on background

# --- Operators ---
class MY_OT_AddRenderQueueItem(Operator):
    bl_idname = "eli.add_render_queue_item"
    bl_label = "Add Render Queue Item"
    bl_description = "Adds a new item to the render queue"

    def execute(self, context):
        scene = context.scene
        new_item = scene.eli_render_queue.add()
        new_item.name = f"Render Item {len(scene.eli_render_queue)}"
        return {"FINISHED"}

class MY_OT_RemoveRenderQueueItem(Operator):
    bl_idname = "eli.remove_render_queue_item"
    bl_label = "Remove Render Queue Item"
    bl_description = "Removes the selected item from the render queue"

    def execute(self, context):
        scene = context.scene
        index = scene.eli_render_queue_index
        scene.eli_render_queue.remove(index)
        scene.eli_render_queue_index = min(max(0, index - 1), len(scene.eli_render_queue) - 1) #Keep list index valid
        return {"FINISHED"}

class MY_OT_StartRenderQueue(Operator):
    bl_idname = "eli.start_render_queue"
    bl_label = "Start Render Queue"
    bl_description = "Starts rendering all scenes in the render queue"

    def execute(self, context):
        scene = context.scene
        for item in scene.eli_render_queue:
            print(f"Rendering: {item.scene_file}, Camera: {item.camera_name}, to: {item.output_path}")

            # Implement actual render logic here
            # 1. Load scene from item.scene_file
            # 2. Set render settings (resolution, samples, output path, etc.) from the item
            # 3. Set active camera to item.camera_name
            # 4. bpy.ops.render.render(write_still=True)
            # 5. Save the blend file or any changes, if any
            # Implement the logic to load a file and apply the render settings
            blend_file_path = item.scene_file

            try:
                bpy.ops.wm.open_mainfile(filepath=blend_file_path) #Opens the blend file
            except RuntimeError as err:
                self.report({'ERROR'}, "Error loading Blend File")

            bpy.context.scene.render.filepath = item.output_path #Applies the Output path from the list
            bpy.context.scene.render.engine = item.render_engine #Applies the Render engine

            self.report({'INFO'}, "Render Started")
            bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True)  # Renders the file and saves the render

        self.report({"INFO"}, "Render queue complete.")
        return {"FINISHED"}

class MY_OT_OpenOutputDir(Operator):
    bl_label = "Open Output Directory"
    bl_idname = "eli.open_output_dir"
    bl_description = "Opens the render output directory in the file explorer."

    def execute(self, context):
        output_path = bpy.context.scene.render.filepath
        if not output_path:
            output_path = bpy.utils.user_resource('CONFIG', path='renders')
            if not os.path.exists(output_path):
                os.makedirs(output_path)
        try:
            os.startfile(output_path)
        except OSError:  # Handle cases where startfile is not available (e.g., Linux)
            try:
                subprocess.Popen(['xdg-open', output_path])  # Linux
            except FileNotFoundError:
                try:
                    subprocess.Popen(['open', output_path])  # macOS
                except FileNotFoundError:
                    self.report({'ERROR'}, "Could not open output directory.")
                    return {'CANCELLED'}

        self.report({'INFO'}, f"Opening output directory: {output_path}")
        return {"FINISHED"}

class MY_OT_StartRender(Operator):
    bl_label = "Start Render (Current Scene)"
    bl_idname = "eli.start_render"
    bl_description = "Starts the render process for the current scene."

    def execute(self, context):
        # In a real implementation, this would start the render process.
        print("Starting render...")
        bpy.ops.render.render('INVOKE_DEFAULT')  # Start render
        self.report({"INFO"}, "Render started.")
        return {"FINISHED"}

class MY_OT_StartRenderBackground(Operator):
    bl_label = "Start Render Background"
    bl_idname = "eli.start_render_background"
    bl_description = "Starts the render process for the current scene."

    def execute(self, context):
        # Implement background rendering logic here.
        print("Starting render in background...")
        bpy.ops.render.render('INVOKE_DEFAULT', animation=True, write_still=False) #Changed to animation
        self.report({"INFO"}, "Render started in background.")
        return {"FINISHED"}