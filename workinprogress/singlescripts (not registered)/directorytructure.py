import bpy
import os

def create_directory_structure(base_path):
    textures_path = os.path.join(base_path, "textures")
    meta_path = os.path.join(base_path, "meta")
    
    os.makedirs(textures_path, exist_ok=True)
    os.makedirs(meta_path, exist_ok=True)
    
    return textures_path, meta_path

# unpack images into material index subfolders
def unpack_images_to_folders(textures_path):
    for mat in bpy.data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    image = node.image
                    if image and image.packed_file:
                        # Create a subfolder for the material
                        material_folder = os.path.join(textures_path, mat.name)
                        os.makedirs(material_folder, exist_ok=True)

                        # Unpack the image to its original path
                        image.unpack(method='USE_ORIGINAL')

                        # Move the unpacked image to the material folder
                        original_image_path = bpy.path.abspath(image.filepath)
                        new_image_path = os.path.join(material_folder, os.path.basename(original_image_path))

                        # Only move if the file exists
                        if os.path.exists(original_image_path):
                            os.rename(original_image_path, new_image_path)
                            # Update the image path
                            node.image.filepath = new_image_path
                            image.save()  # Save the image with the new path

# gather metadata about the Blender file
def gather_metadata():
    metadata = {}

    # Basic file information
    metadata['File Name'] = bpy.data.filepath
    metadata['File Version'] = bpy.app.version_string
    metadata['Scene Name'] = bpy.context.scene.name

    # Collecting information about objects
    metadata['Objects'] = []
    for obj in bpy.data.objects:
        obj_info = {
            'Name': obj.name,
            'Type': obj.type,
            'Location': obj.location,
            'Rotation': obj.rotation_euler,
            'Scale': obj.scale,
        }
        metadata['Objects'].append(obj_info)

    # Collecting information about materials
    metadata['Materials'] = []
    for mat in bpy.data.materials:
        mat_info = {
            'Name': mat.name,
            'Use Nodes': mat.use_nodes,
        }
        metadata['Materials'].append(mat_info)

    # Collecting information about meshes
    metadata['Meshes'] = []
    for mesh in bpy.data.meshes:
        mesh_info = {
            'Name': mesh.name,
            'Vertex Count': len(mesh.vertices),
            'Face Count': len(mesh.polygons),
        }
        metadata['Meshes'].append(mesh_info)

    return metadata

# write metadata to a text file
def write_metadata_to_file(metadata, meta_path):
    output_file_path = os.path.join(meta_path, 'blender_file_metadata.txt')
    with open(output_file_path, 'w') as file:
        for key, value in metadata.items():
            file.write(f"{key}:\n")
            if isinstance(value, list):
                for item in value:
                    file.write(f"  - {item}\n")
            else:
                file.write(f"  {value}\n")
            file.write("\n")

# Main execute the workflow
def main():
    # Get the base path from the current Blender file
    base_path = bpy.path.abspath("//")
    if not base_path:
        print("Please save your Blender file before running this script.")
        return

    # Create the directory structure
    textures_path, meta_path = create_directory_structure(base_path)

    # Unpack images into folders
    unpack_images_to_folders(textures_path)

    # Gather metadata and write to file
    metadata = gather_metadata()
    write_metadata_to_file(metadata, meta_path)

    print(f"Project structure created at: {base_path}")
    print(f"Textures unpacked to: {textures_path}")
    print(f"Metadata saved at: {os.path.join(meta_path, 'blender_file_metadata.txt')}")

# Run
main()
