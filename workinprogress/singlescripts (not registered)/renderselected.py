import bpy

def some_function():
    print("Render selection executed.")
    
def batch_render_collections():
    """Renders selected objects in separate collections, one at a time, preserving existing collection visibility."""

    selected_objects = bpy.context.selected_objects
    if not selected_objects:
        print("No objects selected.")
        return

    original_hide_state = {}
    created_collections = []
    original_collection_exclude = {}  # Store original collection exclude state

    view_layer = bpy.context.view_layer
    scene = bpy.context.scene
    original_filepath = scene.render.filepath

    # 1. Create collections
    for obj in selected_objects:
        collection_name = f"{obj.name}_Collection"
        collection = bpy.data.collections.get(collection_name)

        if not collection:
            collection = bpy.data.collections.new(collection_name)
            bpy.context.scene.collection.children.link(collection)
        created_collections.append(collection)

        for c in list(obj.users_collection):
            c.objects.unlink(obj)
        collection.objects.link(obj)

        original_hide_state[obj] = obj.hide_viewport # Store initial hide state

    # 2. Store existing collection exclude state and exclude ONLY newly created collections
    for layer in view_layer.layer_collection.children:
        original_collection_exclude[layer.name] = layer.exclude #Store original excludes state
        if layer.name in [coll.name for coll in created_collections]:
            layer.exclude = True # Exclude newly created collection by default


    # 3. Batch Render
    try:
        for collection in created_collections:
            # Set render output path
            scene.render.filepath = f"{original_filepath}{collection.name}_"

            # Unexclude only the target collection
            layer_collection = view_layer.layer_collection.children[collection.name]
            layer_collection.exclude = False

            # Perform Render
            bpy.ops.render.render(write_still=True)
            print(f"Rendered collection: {collection.name}")

            #Exclude collection to default setup
            layer_collection.exclude = True

    finally:
        # Restore scene state (visibility, filepath)
        scene.render.filepath = original_filepath
        #Ensure that all objects hide state restores

        for obj in bpy.data.objects:
           if obj in original_hide_state:
               obj.hide_viewport = original_hide_state[obj]
        # Restore original collection exclude state

        for layer in view_layer.layer_collection.children:
            if layer.name in original_collection_exclude: #Check if layer in dictionary to avoid errors

                layer.exclude = original_collection_exclude[layer.name]



    print("Batch rendering complete.")

batch_render_collections()