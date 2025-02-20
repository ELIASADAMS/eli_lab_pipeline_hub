bl_info = {
    "name": "Enhanced Camera manager with Real-Time Lens Control",
    "blender": (4, 0, 2),
    "category": "Object",
}

import bpy


def some_function():
    print("Camera Manager function executed.")


class CameramanagerPanel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport"""
    bl_label = "Camera manager"
    bl_idname = "OBJECT_PT_camera_manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Camera Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Dropdown menu for selecting cameras
        layout.prop(scene, "camera_manager", text="Select Camera")

        # Number box for adjusting camera lens
        layout.prop(scene, "camera_lens", text="Camera Lens")

        # Dropdown menu for selecting resolution modes
        layout.prop(scene, "resolution_mode", text="Resolution Mode")


class UpdateCameraList(bpy.types.Operator):
    """Updates the camera list"""
    bl_idname = "object.update_camera_list"
    bl_label = "Update Camera List"

    def execute(self, context):
        # Refresh the camera list
        cameras = [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == 'CAMERA']
        context.scene.camera_manager = cameras[0][0] if cameras else ""
        self.report({'INFO'}, "Camera list updated")
        return {'FINISHED'}


def update_camera(scene):
    """Update the active camera and lens when the selection changes"""
    camera_name = scene.camera_manager
    camera = bpy.data.objects.get(camera_name)
    if camera and camera.type == 'CAMERA':
        scene.camera = camera  # Set the active camera
        camera.data.lens = scene.camera_lens  # Set the lens value
        # Switch to camera view if necessary
        area = next((area for area in context.screen.areas if area.type == 'VIEW_3D'), None)
        if area:
            area.spaces.active.region_3d.view_perspective = 'CAMERA'
            area.spaces.active.region_3d.view_matrix = camera.matrix_world.inverted()


def update_camera_lens(scene):
    """Update the camera lens value and store it in the camera object"""
    camera_name = scene.camera_manager
    camera = bpy.data.objects.get(camera_name)
    if camera and camera.type == 'CAMERA':
        camera["lens_value"] = scene.camera_lens  # Store the lens value in the camera's custom property


def update_resolution(scene):
    """Update the render resolution based on the selected mode"""
    resolution_modes = {
        "1:1": (640, 640),
        "16:9": (1920, 1080),
        "4:3": (1024, 768),
        "2.35:1": (1920, 817)
    }
    resolution = resolution_modes.get(scene.resolution_mode, (1920, 1080))
    scene.render.resolution_x, scene.render.resolution_y = resolution


def get_camera_items(self, context):
    """Function to get camera items for the dropdown"""
    return [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == 'CAMERA']


def get_resolution_items(self, context):
    """Function to get resolution items for the dropdown"""
    return [
        ("1:1", "1:1", ""),
        ("16:9", "16:9", ""),
        ("4:3", "4:3", ""),
        ("2.35:1", "2.35:1", "")
    ]


def register():
    bpy.types.Scene.camera_manager = bpy.props.EnumProperty(
        name="Cameras",
        description="Select a camera to switch to",
        items=get_camera_items,
        update=lambda self, context: update_camera(context.scene)  # Call update function on change
    )

    bpy.types.Scene.camera_lens = bpy.props.FloatProperty(
        name="Lens",
        description="Set the camera lens focal length",
        default=50.0,  # Default focal length in mm
        min=1.0,  # Minimum lens value
        max=300.0,  # Maximum lens value
        step=1,  # Step size for the slider
        precision=1,  # Decimal precision
        update=lambda self, context: update_camera(context.scene)  # Call update function on change
    )

    bpy.types.Scene.resolution_mode = bpy.props.EnumProperty(
        name="Resolution Mode",
        description="Select the resolution mode",
        items=get_resolution_items,
        update=lambda self, context: update_resolution(context.scene)  # Call update function on change
    )

    bpy.utils.register_class(CameramanagerPanel)
    bpy.utils.register_class(UpdateCameraList)


def unregister():
    del bpy.types.Scene.camera_manager
    del bpy.types.Scene.camera_lens
    del bpy.types.Scene.resolution_mode
    bpy.utils.unregister_class(CameramanagerPanel)
    bpy.utils.unregister_class(UpdateCameraList)


if __name__ == "__main__":
    register()
