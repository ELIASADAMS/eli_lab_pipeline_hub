bl_info = {
    "name": "Proxy System Creator",
    "blender": (4, 0, 2),
    "category": "Object",
}

import bpy


def some_function():
    print("Proxy function executed.")


class OBJECT_OT_create_proxy_system(bpy.types.Operator):
    """Creates a proxy system for selected high-res objects"""
    bl_idname = "object.create_proxy_system"
    bl_label = "Create Proxy System"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'WARNING'},
                        "No objects selected. Please select the high-resolution objects you want to create proxies for")
            return {'CANCELLED'}

        original_selection = selected_objects[:]  # Create a copy of the original selection

        for highres_obj in original_selection:

            # 1. Get or create a Low-Poly Object
            lowpoly_name = f"{highres_obj.name}_proxy"
            lowpoly_obj = bpy.data.objects.get(lowpoly_name)

            # Deselect all objects
            for obj in context.selected_objects:
                obj.select_set(False)

            if not lowpoly_obj:  # Lowpoly object doesn't exist
                # Create New Proxy
                context.view_layer.objects.active = highres_obj
                highres_obj.select_set(True)

                bpy.ops.object.duplicate(linked=False)

                lowpoly_obj = None

                for obj in context.selected_objects:
                    if obj != highres_obj and obj not in original_selection:
                        lowpoly_obj = obj
                        break

                if not lowpoly_obj:
                    self.report({'ERROR'}, f"Could not find low-poly object for {highres_obj.name}. Skipping")
                    continue

                lowpoly_obj.name = lowpoly_name

                context.view_layer.objects.active = lowpoly_obj  # Set active low poly
                lowpoly_obj.select_set(True)

                bpy.ops.object.modifier_add(type='DECIMATE')
                lowpoly_obj.modifiers["Decimate"].decimate_type = 'COLLAPSE'
                lowpoly_obj.modifiers["Decimate"].ratio = 0.1
                bpy.ops.object.modifier_apply(modifier=lowpoly_obj.modifiers["Decimate"].name)

            # 2. Parent the High-Res Model to the Low-Res Proxy
            context.view_layer.objects.active = lowpoly_obj  # set to proxy
            lowpoly_obj.select_set(True)
            highres_obj.select_set(True)

            bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

            # 3. Add Mesh Deform modifier to High poly
            context.view_layer.objects.active = highres_obj
            highres_obj.select_set(True)

            meshdeform_modifier = highres_obj.modifiers.new(name="Proxy_Deform", type='MESH_DEFORM')
            meshdeform_modifier.object = lowpoly_obj
            highres_obj.data.use_auto_smooth = False  # Disable autosmooth

            # Bind
            context.view_layer.objects.active = highres_obj
            highres_obj.select_set(True)
            lowpoly_obj.select_set(True)
            bpy.ops.object.meshdeform_bind(modifier=meshdeform_modifier.name)

            # 4. Set visibility: Low-Res Proxy Visible, High-Res Invisible in Viewport
            lowpoly_obj.hide_viewport = False
            lowpoly_obj.hide_render = True  # Disable in render

            # 5. Hide the High-Res Model in the viewport, but *not* in the render
            highres_obj.hide_viewport = True
            highres_obj.hide_render = False

            # Clear selection
            for obj in context.selected_objects:
                obj.select_set(False)

            self.report({'INFO'}, f"Proxy system created for {highres_obj.name}: Low-poly proxy is {lowpoly_name}")

        return {'FINISHED'}


class VIEW3D_PT_proxy_system_panel(bpy.types.Panel):
    """Panel in the Object properties window"""
    bl_label = "Proxy System"
    bl_idname = "VIEW3D_PT_proxy_system"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Proxy"

    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_create_proxy_system.bl_idname, text="Create Proxy System")


def register():
    bpy.utils.register_class(OBJECT_OT_create_proxy_system)
    bpy.utils.register_class(VIEW3D_PT_proxy_system_panel)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_proxy_system_panel)
    bpy.utils.unregister_class(OBJECT_OT_create_proxy_system)


if __name__ == "__main__":
    register()
