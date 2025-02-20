bl_info = {
    "name": "Debugger",
    "blender": (4, 0, 2),
    "category": "Object",
}

import bpy
import os
import time
import datetime

class OBJECT_OT_check_scene_issues(bpy.types.Operator):
    """Checks for common scene issues and logs them to a file"""
    bl_idname = "object.check_scene_issues"
    bl_label = "Check Scene Issues"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        filepath = bpy.data.filepath
        if not filepath:
            self.report({'ERROR'}, "Please save the Blender file first before running the check.")
            return {'CANCELLED'}

        # Create a timestamped log file name
        now = datetime.datetime.now()
        log_filename = os.path.splitext(filepath)[0] + f"_check_log_{now.strftime('%Y%m%d_%H%M%S')}.txt"

        with open(log_filename, "w") as log_file:
            log_file.write(f"Scene Check Log for: {filepath}\n")
            log_file.write(f"Date and Time: {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            log_file.write("--- Missing Textures ---\n")
            missing_textures = []
            for image in bpy.data.images:
                if image.filepath and not os.path.exists(bpy.path.abspath(image.filepath)):
                    missing_textures.append(image.name)

            if missing_textures:
                for texture_name in missing_textures:
                    log_file.write(f"  - Missing Texture: {texture_name}\n")
            else:
                log_file.write("  No missing textures found.\n")

            log_file.write("\n--- Unlinked Assets (Orphan Data) ---\n")
            unlinked_data = []

            # Iterate through different data types that can have orphans
            for data_collection_name in ['meshes', 'materials', 'textures', 'images', 'objects', 'armatures', 'actions', 'curves']:
                data_collection = getattr(bpy.data, data_collection_name, None)  # Use getattr and default None for compatibility
                if data_collection:
                    for item in data_collection:
                        if item.users == 0 and not item.name.startswith("Action"):  # Ignore default 'Action' object
                            unlinked_data.append((item.name, data_collection_name))
            if unlinked_data:
                for name, data_type in unlinked_data:
                    log_file.write(f"  - Orphaned {data_type[:-1]}: {name}\n")  # Remove plural from data_type for readability
            else:
                log_file.write("  No Unlinked data found.\n")

            log_file.write("\n--- Animation Errors ---\n")
            animation_errors = []
            for obj in bpy.data.objects:
                if obj.animation_data:
                    if not obj.animation_data.action:
                        animation_errors.append(obj.name)  # Object has animation data but no action

            if animation_errors:
                for obj_name in animation_errors:
                    log_file.write(f"  - Animation Error: Object {obj_name} has animation data, but no Action is assigned.\n")
            else:
                log_file.write("  No obvious animation errors found.\n")

            log_file.write("\n--- Estimated Render Time (Simple Test) ---\n")
            start_time = time.time()
            try:
                bpy.ops.render.render(write_still=False)  # Just render to memory
            except Exception as e:
                log_file.write(f"  Error during render time estimation: {e}\n")
                print(f"Error during render time estimation: {e}")  # also print to console for visibility
            end_time = time.time()
            render_time = end_time - start_time
            log_file.write(f"  Estimated render time for one frame (low sample): {render_time:.2f} seconds\n")

        self.report({'INFO'}, f"Scene check complete. Log file saved to: {log_filename}")
        return {'FINISHED'}


class VIEW3D_PT_scene_checker_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Scene Checker"
    bl_idname = "VIEW3D_PT_scene_checker"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Scene Check"

    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_check_scene_issues.bl_idname, text="Check Scene Issues")


def register():
   
    bpy.utils.register_class(OBJECT_OT_check_scene_issues)
    bpy.utils.register_class(VIEW3D_PT_scene_checker_panel)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_scene_checker_panel)
    bpy.utils.unregister_class(OBJECT_OT_check_scene_issues)


if __name__ == "__main__":
    register()