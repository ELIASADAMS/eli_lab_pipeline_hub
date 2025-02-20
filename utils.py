import bpy
from bpy.props import StringProperty
import os

_asset_path = "//assets/"  # Default asset path
_project_presets_path = "//presets/"
_export_path = "//exports/"


class ProjectPresetItem(bpy.types.PropertyGroup):
    name: StringProperty(name="Preset Name")
    filepath: StringProperty(name="Preset Filepath", subtype="FILE_PATH")


class LinkedLibraryItem(bpy.types.PropertyGroup):
    name: StringProperty(name="Library Name")
    filepath: StringProperty(name="File Path", subtype="FILE_PATH")
    thumbnail: StringProperty(name="Thumbnail Path", subtype="FILE_PATH")  # For visual preview

def create_collection_if_not_exists(collection_name):
    """Creates a collection if it doesn't exist."""
    if collection_name not in bpy.data.collections:
        new_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(new_collection)  # Link to main scene
        return new_collection
    return bpy.data.collections[collection_name]

def safe_collection_link(obj, col):
    """
    Safely links an object to a collection, handling potential errors.
    """
    try:
        col.objects.link(obj)
    except RuntimeError:
        # Object may already be in collection
        pass

def load_blend_file(filepath, link=False, relative=False, lights=False, objects=False):
    """Helper function to load objects or lights from a blend file safely."""
    try:
        with bpy.data.libraries.load(filepath, link=link, relative=relative) as (data_from, data_to):
            if lights:
                data_to.lights = data_from.lights
            if objects:
                data_to.objects = data_from.objects

            if not any([data_to.lights, data_to.objects]):
                print("Warning: No lights or objects to load.")
                return None, None #Or return empty lists depending upon the call

        return data_to.lights if lights else [], data_to.objects if objects else []
    except Exception as e:
        print(f"Error loading blend file: {e}")
        return None, None