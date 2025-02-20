import bpy
import subprocess
import sys
import os
from . import (
    asset_management,
    scene_setup,
    linked_libraries,
    lighting_rendering,
    data_export_versioning,
    scene_management,
    render_management,
    publish,
    task_automation,
    performance_optimization,
    utils,
)

bl_info = {
    "name": "eli_lab Pipeline Hub",
    "author": "Ilya Minin (Eli)",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "description": "A centralized hub for managing pipeline tasks.",
    "category": "Pipeline",
}


classes = (
    utils.ProjectPresetItem,
    utils.LinkedLibraryItem,
    lighting_rendering.LightingPresetItem,
    lighting_rendering.UI_UL_lighting_preset_list,
    asset_management.MY_PT_AssetManagementPanel,
    scene_setup.MY_PT_SceneSetupPanel,
    linked_libraries.MY_PT_LinkedLibrariesPanel,
    lighting_rendering.MY_PT_LightingRenderingPanel,
    data_export_versioning.MY_PT_DataExportVersioningPanel,
    scene_management.MY_PT_SceneManagementPanel,
    render_management.MY_PT_RenderManagementPanel,
    publish.MY_PT_PublishPanel,
    linked_libraries.UI_UL_linked_library_list,
    scene_setup.UI_UL_list,
    scene_setup.MY_OT_AddProjectPreset,
    scene_setup.MY_OT_RemoveProjectPreset,
    scene_setup.MY_OT_ApplyProjectPreset,
    scene_setup.MY_OT_ConvertUnits,
    scene_setup.MY_OT_SetupCollections,
    linked_libraries.MY_OT_AddLinkedLibrary,
    linked_libraries.MY_OT_RemoveLinkedLibrary,
    linked_libraries.MY_OT_UpdateLinkedLibrary,
    linked_libraries.MY_OT_RelinkAllLibraries,
    data_export_versioning.MY_OT_ExportData,
    data_export_versioning.MY_OT_IncrementalSaveComment,
    asset_management.MY_OT_ImportAsset,
    asset_management.MY_OT_ExportAsset,
    asset_management.MY_OT_PublishAsset,
    scene_management.MY_OT_SaveScene,
    scene_management.MY_OT_OpenScene,
    scene_management.MY_OT_IncrementSave,
    scene_management.MY_OT_IncrementVersion,
    scene_management.MY_OT_DecrementVersion,
    render_management.MY_OT_StartRender,
    render_management.MY_OT_StartRenderBackground,
    render_management.MY_OT_OpenOutputDir,
    publish.MY_OT_Publish,
    lighting_rendering.MY_OT_AddLightingPreset,
    lighting_rendering.MY_OT_RemoveLightingPreset,
    lighting_rendering.MY_OT_ApplyLightingPreset,
    task_automation.MY_PT_TaskAutomationPanel,
    task_automation.MY_OT_RunBatchOperation,
    performance_optimization.MY_PT_PerformanceOptimizationPanel,
    performance_optimization.MY_OT_CleanupUnusedData,
    performance_optimization.MY_OT_MergeByDistance,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Scene Properties Registration
    bpy.types.Scene.eli_asset_path = bpy.props.StringProperty(
        name="Asset Path",
        default=utils._asset_path,
        description="Path to the asset library",
    )
    bpy.types.Scene.eli_project_presets_path = bpy.props.StringProperty(
        name="Project Presets Path",
        default=utils._project_presets_path,
        description="Path to project preset files.",
    )
    bpy.types.Scene.eli_asset_type = bpy.props.EnumProperty(
        name="Asset Type",
        items=[
            ("MODEL", "Model", "A 3D model asset"),
            ("TEXTURE", "Texture", "A texture asset"),
            ("RIG", "Rig", "A character rig asset"),
            ("MATERIAL", "Material", "A Blender Material"),
        ],
        description="Type of asset.",
    )
    bpy.types.Scene.eli_scene_version = bpy.props.IntProperty(
        name="Scene Version", default=1, description="Scene version number"
    )
    bpy.types.Scene.eli_render_resolution_x = bpy.props.IntProperty(
        name="Resolution X", default=1920, description="Render resolution X"
    )
    bpy.types.Scene.eli_render_resolution_y = bpy.props.IntProperty(
        name="Resolution Y", default=1080, description="Render resolution Y"
    )
    bpy.types.Scene.eli_render_samples = bpy.props.IntProperty(
        name="Samples", default=64, description="Render samples"
    )
    bpy.types.Scene.eli_publish_description = bpy.props.StringProperty(
        name="Description", default="", description="Publish description"
    )
    bpy.types.Scene.eli_publish_create_thumbnail = bpy.props.BoolProperty(
        name="Create Thumbnail", default=True, description="Create a thumbnail during publish"
    )
    bpy.types.Scene.eli_project_presets = bpy.props.CollectionProperty(type=utils.ProjectPresetItem)
    bpy.types.Scene.eli_project_presets_index = bpy.props.IntProperty()
    bpy.types.Scene.eli_preferred_units = bpy.props.EnumProperty(
        name="Preferred Units",
        items=[
            ("METERS", "Meters", "Use meters as the scene unit"),
            ("CENTIMETERS", "Centimeters", "Use centimeters as the scene unit"),
            ("INCHES", "Inches", "Use inches as the scene unit (approximation with Imperial)"),
        ],
        description="Preferred units for the scene.",
    )
    bpy.types.Scene.eli_linked_libraries = bpy.props.CollectionProperty(type=utils.LinkedLibraryItem)
    bpy.types.Scene.eli_linked_libraries_index = bpy.props.IntProperty()
    bpy.types.Scene.eli_export_path = bpy.props.StringProperty(
        name="Export Path",
        default=utils._export_path,
        description="Path to export the data to.",
        subtype="DIR_PATH",
    )
    bpy.types.Scene.eli_export_format = bpy.props.EnumProperty(
        name="Export Format",
        items=[
            ("FBX", "FBX", "Export to FBX format"),
            ("OBJ", "OBJ", "Export to OBJ format"),
            ("ALEMBIC", "Alembic", "Export to Alembic format"),
        ],
        description="Export format",
    )
    bpy.types.Scene.eli_save_comment = bpy.props.StringProperty(
        name="Save Comment", default="", description="Comment describing the changes in this save."
    )

    bpy.types.Scene.eli_lighting_presets = bpy.props.CollectionProperty(
        type=lighting_rendering.LightingPresetItem
    )
    bpy.types.Scene.eli_lighting_presets_index = bpy.props.IntProperty()

    task_automation.register_scene_properties()  # NEW CALL
    performance_optimization.register_scene_properties()  # NEW CALL


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # Scene Properties Unregistration
    del bpy.types.Scene.eli_asset_path
    del bpy.types.Scene.eli_project_presets_path
    del bpy.types.Scene.eli_asset_type
    del bpy.types.Scene.eli_scene_version
    del bpy.types.Scene.eli_render_resolution_x
    del bpy.types.Scene.eli_render_resolution_y
    del bpy.types.Scene.eli_render_samples
    del bpy.types.Scene.eli_publish_description
    del bpy.types.Scene.eli_publish_create_thumbnail
    del bpy.types.Scene.eli_project_presets
    del bpy.types.Scene.eli_project_presets_index
    del bpy.types.Scene.eli_preferred_units
    del bpy.types.Scene.eli_linked_libraries
    del bpy.types.Scene.eli_linked_libraries_index
    del bpy.types.Scene.eli_export_path
    del bpy.types.Scene.eli_export_format
    del bpy.types.Scene.eli_save_comment

    del bpy.types.Scene.eli_lighting_presets
    del bpy.types.Scene.eli_lighting_presets_index

    task_automation.unregister_scene_properties()  # NEW CALL
    performance_optimization.unregister_scene_properties()  # NEW CALL


if __name__ == "__main__":
    register()