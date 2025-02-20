bl_info = {
    "name": "eli_lab Pipeline",
    "blender": (4, 0, 2),
    "category": "Object",
}

import bpy
from . import cameramanager
from . import organisation
from . import proxysystem
from . import scenechecker

class ELILabPipelinePanel(bpy.types.Panel):
    bl_label = "eli_lab Pipeline"
    bl_idname = "OBJECT_PT_eli_lab"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        
        # Create tabs for different categories
        layout.prop(context.scene, "eli_lab_tabs", text="")

        # Draw the sub-panel based on the selected tab
        if context.scene.eli_lab_tabs == 'CAMERA':
            self.draw_camera_tab(layout)
        elif context.scene.eli_lab_tabs == 'ORG':
            self.draw_organisation_tab(layout)
        elif context.scene.eli_lab_tabs == 'PROXY':
            self.draw_proxy_tab(layout)
        elif context.scene.eli_lab_tabs == 'SCENE':
            self.draw_scene_checker_tab(layout)

    def draw_camera_tab(self, layout):
        layout.label(text="Camera Switcher Operations:")
        layout.prop(context.scene, "eli_lab_operations", text="Select Operation")
        layout.operator("eli_lab.execute_operation")

    def draw_organisation_tab(self, layout):
        layout.label(text="Organisation Operations:")
        layout.prop(context.scene, "eli_lab_operations", text="Select Operation")
        layout.operator("eli_lab.execute_operation")

    def draw_proxy_tab(self, layout):
        layout.label(text="Proxy System Operations:")
        layout.prop(context.scene, "eli_lab_operations", text="Select Operation")
        layout.operator("eli_lab.execute_operation")

    def draw_scene_checker_tab(self, layout):
        layout.label(text="Scene Checker Operations:")
        layout.prop(context.scene, "eli_lab_operations", text="Select Operation")
        layout.operator("eli_lab.execute_operation")


class ExecuteOperation(bpy.types.Operator):
    bl_idname = "eli_lab.execute_operation"
    bl_label = "Execute Selected Operation"

    def execute(self, context):
        operation = context.scene.eli_lab_operations
        if operation == 'CAMERA_SWITCHER':
            cameramanager.some_function()  # Replace with the actual function
        elif operation == 'ORGANISATION':
            organisation.some_function()  # Replace with the actual function
        elif operation == 'PROXY_SYSTEM':
            proxysystem.some_function()  # Replace with the actual function
        elif operation == 'SCENE_CHECKER':
            scenechecker.some_function()  # Replace with the actual function
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ELILabPipelinePanel)

    # Unified Dropdown property
    bpy.types.Scene.eli_lab_operations = bpy.props.EnumProperty(
        items=[
            ('CAMERA_SWITCHER', "Camera Switcher", ""),
            ('ORGANISATION', "Organisation", ""),
            ('PROXY_SYSTEM', "Proxy System", ""),
            ('SCENE_CHECKER', "Scene Checker", ""),
        ],
        name="Operations",
        default='CAMERA_SWITCHER'
    )

    bpy.types.Scene.eli_lab_tabs = bpy.props.EnumProperty(
        items=[
            ('CAMERA', "Camera Switcher", ""),
            ('ORG', "Organisation", ""),
            ('PROXY', "Proxy System", ""),
            ('SCENE', "Scene Checker", ""),
        ],
        name="Tabs",
        default='CAMERA'
    )

    bpy.utils.register_class(ExecuteOperation)

    cameramanager.register()
    organisation.register()
    proxysystem.register()
    scenechecker.register()


def unregister():
    bpy.utils.unregister_class(ELILabPipelinePanel)
    del bpy.types.Scene.eli_lab_operations
    del bpy.types.Scene.eli_lab_tabs

    bpy.utils.unregister_class(ExecuteOperation)

    cameramanager.unregister()
    organisation.unregister()
    proxysystem.unregister()
    scenechecker.unregister()


if __name__ == "__main__":
    register()
