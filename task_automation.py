import bpy
from bpy.types import Panel, Operator
from bpy.props import StringProperty, EnumProperty


class MY_PT_TaskAutomationPanel(Panel):
    bl_label = "Task Automation"
    bl_idname = "MY_PT_TaskAutomationPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "eli_lab Pipeline"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Batch Processing
        layout.label(text="Batch Processing:")
        layout.prop(scene, "eli_batch_operation", text="Operation")
        layout.operator("eli.run_batch_operation", text="Run Batch Operation")

        # Custom Scripts Integration
        layout.label(text="Custom Scripts:")
        layout.prop(scene, "eli_custom_script", text="Script")
        layout.operator("eli.run_custom_script", text="Run Custom Script")


class MY_OT_RunBatchOperation(Operator):
    bl_idname = "eli.run_batch_operation"
    bl_label = "Run Batch Operation"
    bl_description = "Runs a predefined batch operation."

    def execute(self, context):
        scene = context.scene
        batch_operation = scene.eli_batch_operation

        # Implement the batch operation logic here based on the selected operation.
        # Example:
        if batch_operation == "IMPORT_FBX":
            # Implement import FBX logic
            print("Importing FBX files in batch...")
            self.report({"INFO"}, "Importing FBX files in batch...")
        self.report({"INFO"}, f"Running batch operation: {batch_operation}")
        return {"FINISHED"}


class MY_OT_RunCustomScript(Operator):
    bl_idname = "eli.run_custom_script"
    bl_label = "Run Custom Script"
    bl_description = "Runs a custom Python script."

    def execute(self, context):
        scene = context.scene
        custom_script = scene.eli_custom_script

        try:
            # Execute the custom script using exec() or by importing the script as a module.
            # Implement this by using exec
            exec(custom_script, globals())
            print("Running custom script...")
            self.report({"INFO"}, "Running custom script...")

        except Exception as e:
            self.report({"ERROR"}, f"Error running custom script: {e}")

        return {"FINISHED"}

# --- Scene Properties ---
def register_scene_properties():
    bpy.types.Scene.eli_batch_operation = bpy.props.EnumProperty(
        name="Batch Operation",
        items=[
            ("IMPORT_FBX", "Import FBX", "Import multiple FBX files."),
            ("EXPORT_OBJ", "Export OBJ", "Export selected objects to OBJ format."),
            # Add more operations here
        ],
        description="Select a batch operation to perform."
    )
    bpy.types.Scene.eli_custom_script = bpy.props.StringProperty(
        name="Custom Script",
        default="",
        description="Enter a custom Python script to run."
    )
def unregister_scene_properties():
    del bpy.types.Scene.eli_batch_operation
    del bpy.types.Scene.eli_custom_script