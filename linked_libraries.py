import bpy
from bpy.types import Panel, Operator, UIList
from bpy.props import StringProperty, CollectionProperty, IntProperty


class LinkedLibraryItem(bpy.types.PropertyGroup):
    name: StringProperty(name="Library Name")
    filepath: StringProperty(name="File Path", subtype='FILE_PATH')
    thumbnail: StringProperty(name="Thumbnail Path", subtype='FILE_PATH') # For visual preview

class UI_UL_linked_library_list(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Draw each item in the list
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon='OBJECT_DATA') # Or use a real icon
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='OBJECT_DATA') # Replace with thumbnail display


class MY_PT_LinkedLibrariesPanel(Panel):
    bl_label = "Linked Libraries"
    bl_idname = "MY_PT_LinkedLibrariesPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "eli_lab Pipeline"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # List of Linked Libraries
        layout.label(text="Linked Libraries:")
        row = layout.row()
        row.template_list(
            "UI_UL_linked_library_list",
            "Linked Libraries",
            scene,
            "eli_linked_libraries",
            scene,
            "eli_linked_libraries_index",
        )

        # Library Actions
        box = layout.box()
        box.label(text="Library Actions")
        col = box.column(align=True)
        col.operator("eli.add_linked_library", text="Add Library")
        col.operator("eli.remove_linked_library", text="Remove Library")
        col.operator("eli.update_linked_library", text="Update Library")
        col.operator("eli.relink_all_libraries", text="Relink All Libraries")

        # Display Thumbnail (Placeholder)
        if scene.eli_linked_libraries_index >= 0 and len(scene.eli_linked_libraries) > 0:
            library_item = scene.eli_linked_libraries[scene.eli_linked_libraries_index]
            if library_item.thumbnail:
                layout.label(text="Thumbnail Preview (Placeholder):")
                layout.label(text=f"Thumbnail Path: {library_item.thumbnail}")  # Replace with actual thumbnail display


class MY_OT_AddLinkedLibrary(Operator):
    bl_idname = "eli.add_linked_library"
    bl_label = "Add Library"
    bl_description = "Adds a new linked library to the list."

    def execute(self, context):
        scene = context.scene
        new_library = scene.eli_linked_libraries.add()
        new_library.name = "New Library"
        new_library.filepath = ""
        return {"FINISHED"}


class MY_OT_RemoveLinkedLibrary(Operator):
    bl_idname = "eli.remove_linked_library"
    bl_label = "Remove Library"
    bl_description = "Removes the selected linked library from the list."

    def execute(self, context):
        scene = context.scene
        list_index = scene.eli_linked_libraries_index
        if scene.eli_linked_libraries:
            scene.eli_linked_libraries.remove(list_index)
            scene.eli_linked_libraries_index = min(
                max(0, list_index - 1), len(scene.eli_linked_libraries) - 1
            )
        return {"FINISHED"}


class MY_OT_UpdateLinkedLibrary(Operator):
    bl_idname = "eli.update_linked_library"
    bl_label = "Update Library"
    bl_description = "Updates the linked library with the latest version."

    def execute(self, context):
        scene = context.scene
        if scene.eli_linked_libraries_index >= 0 and scene.eli_linked_libraries:
            selected_library = scene.eli_linked_libraries[scene.eli_linked_libraries_index]
            filepath = selected_library.filepath
            if os.path.exists(filepath):
                # Implement logic to update the linked library
                print(f"Updating library: {selected_library.name} from {filepath}")
                self.report({"INFO"}, f"Updating library: {selected_library.name}")
            else:
                self.report({"ERROR"}, f"Library file not found: {filepath}")
        return {"FINISHED"}


class MY_OT_RelinkAllLibraries(Operator):
    bl_idname = "eli.relink_all_libraries"
    bl_label = "Relink All Libraries"
    bl_description = "Relinks all linked libraries in the scene."

    def execute(self, context):
        scene = context.scene
        for library in scene.eli_linked_libraries:
            filepath = library.filepath
            if os.path.exists(filepath):
                # Implement logic to relink the library
                print(f"Relinking library: {library.name} from {filepath}")
                self.report({"INFO"}, f"Relinking library: {library.name}")
            else:
                self.report({"ERROR"}, f"Library file not found: {filepath}")
        return {"FINISHED"}