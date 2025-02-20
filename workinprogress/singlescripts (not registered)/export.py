import bpy

class ApplyRenderEngineSettings(bpy.types.Operator):
    """Apply the selected render engine settings"""
    bl_idname = "render.apply_render_engine"
    bl_label = "Apply Render Engine Settings"

    def execute(self, context):
        if context.scene.render_engine == 'CYCLES':
            bpy.context.scene.render.engine = 'CYCLES'
            # Add your Cycles settings here
            bpy.context.scene.cycles.preview_samples = 1
            bpy.context.scene.cycles.diffuse_bounces = 3
            bpy.context.scene.cycles.glossy_bounces = 3
            bpy.context.scene.cycles.transmission_bounces = 3
            bpy.context.scene.cycles.volume_bounces = 3
            bpy.context.scene.cycles.max_bounces = 3
            bpy.context.scene.cycles.caustics_reflective = True
            bpy.context.scene.cycles.caustics_refractive = True
            bpy.context.scene.cycles.use_fast_gi = True
            bpy.context.scene.cycles.ao_bounces_render = 3
            bpy.context.scene.cycles.ao_bounces = 3
            bpy.context.scene.view_settings.view_transform = 'AgX'
            bpy.context.scene.view_settings.look = 'None'
            bpy.context.scene.cycles.device = 'GPU'

        elif context.scene.render_engine == 'BLENDER_EEVEE':
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
            # Add your Eevee settings here
            bpy.context.scene.eevee.use_gtao = True
            bpy.context.scene.eevee.use_bloom = True
            bpy.context.scene.eevee.use_ssr = True
            bpy.context.scene.eevee.use_motion_blur = True
            bpy.context.scene.eevee.use_volumetric_lights = True
            bpy.context.scene.eevee.use_volumetric_shadows = True
            bpy.context.scene.eevee.shadow_cube_size = '1024'
            bpy.context.scene.eevee.shadow_cascade_size = '2048'
            bpy.context.scene.eevee.use_shadow_high_bitdepth = True
            bpy.context.scene.view_settings.view_transform = 'AgX'
            bpy.context.scene.view_settings.look = 'None'

        return {'FINISHED'}

class ApplyExportSettings(bpy.types.Operator):
    """Apply the selected export settings"""
    bl_idname = "render.apply_export_settings"
    bl_label = "Apply Export Settings"

    def execute(self, context):
        # Apply export settings based on choice
        if context.scene.export_style == 'EXPORT_VIDEO':
            bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
            bpy.context.scene.render.ffmpeg.format = 'MPEG4'
            bpy.context.scene.render.use_stamp = False  # Disable stamp for video

        elif context.scene.export_style == 'EXPORT_SEQUENCE':
            bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR'
            bpy.context.scene.render.use_stamp = False  # Disable stamp for sequence

        elif context.scene.export_style == 'EXPORT_PREVIEW_VIDEO':
            bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
            bpy.context.scene.render.ffmpeg.format = 'MPEG4'
            bpy.context.scene.render.use_stamp = True  # Enable stamp for preview video
            bpy.context.scene.render.use_stamp_note = True
            bpy.context.scene.render.stamp_note_text = "eli_lab"
            bpy.context.scene.render.use_stamp_date = True
            bpy.context.scene.render.use_stamp_time = True

        return {'FINISHED'}

class NViewPanel(bpy.types.Panel):
    """Creates a Panel in the N-Panel of the 3D View"""
    bl_label = "Render Engine and Export Settings"
    bl_idname = "VIEW3D_PT_render_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Render Settings"

    def draw(self, context):
        layout = self.layout

        # Render Engine Selection
        layout.label(text="Select Render Engine:")
        layout.prop(context.scene, "render_engine", text="")
        layout.operator("render.apply_render_engine", text="Apply Render Engine")

        layout.separator()

        # Export Style Selection
        layout.label(text="Select Export Style:")
        layout.prop(context.scene, "export_style", text="")
        layout.operator("render.apply_export_settings", text="Apply Export Settings")

def register():
    bpy.utils.register_class(ApplyRenderEngineSettings)
    bpy.utils.register_class(ApplyExportSettings)
    bpy.utils.register_class(NViewPanel)
    
    bpy.types.Scene.render_engine = bpy.props.EnumProperty(
        name="Render Engine",
        description="Choose the render engine",
        items=[
            ('CYCLES', "Cycles", "Use Cycles rendering engine"),
            ('BLENDER_EEVEE', "Eevee", "Use Eevee rendering engine"),
        ],
        default='CYCLES',
    )

    bpy.types.Scene.export_style = bpy.props.EnumProperty(
        name="Export Style",
        description="Choose the export style",
        items=[
            ('EXPORT_VIDEO', "Export Video", "Export as video"),
            ('EXPORT_SEQUENCE', "Export Sequence", "Export as image sequence"),
            ('EXPORT_PREVIEW_VIDEO', "Export Preview Video", "Export as preview video"),
        ],
        default='EXPORT_VIDEO',
    )

def unregister():
    bpy.utils.unregister_class(NViewPanel)
    bpy.utils.unregister_class(ApplyExportSettings)
    bpy.utils.unregister_class(ApplyRenderEngineSettings)
    del bpy.types.Scene.render_engine
    del bpy.types.Scene.export_style

if __name__ == "__main__":
    register()

