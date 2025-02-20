# eli_lab Pipeline Hub

[![Blender Versions](https://img.shields.io/badge/Blender-3.0+-brightgreen.svg)](https://www.blender.org/)

A Blender addon that serves as a centralized hub for managing common pipeline tasks, automating repetitive actions, and providing quick access to essential tools, all tailored to your specific workflow needs. 
This pipeline-focused approach streamlines routine tasks and empowers you to focus on the creative aspects of your work.

**The goal is to create a seamless, user-friendly pipeline that significantly reduces the time spent on routine tasks, allowing artists to focus on creativity and less on administrative overhead.**

## Features

*   **Asset Management:** Easily import, export, and publish assets.
    *   Define custom asset paths.
    *   Select asset types (Model, Texture, Rig, Material).
*   **Scene Setup:** Quickly apply project presets and configure scenes.
    *   Manage project preset paths.
    *   Convert scene units.
    *   Setup collections.
*   **Linked Libraries:** Streamline library management with easy linking, updating, and relinking.
    *   Add, remove, and update linked libraries.
    *   Relink all libraries in a scene.
*   **Lighting & Rendering:** Manage lighting presets and render settings.
    *   Add, remove, and apply lighting presets.
*   **Data Export & Versioning:** Simplify data export and track scene versions.
    *   Export data in various formats (FBX, OBJ, GLB, USD, Alembic).
    *   Add comments to incremental saves.
*   **Scene Management:** Efficiently save, open, and version scenes.
    *   Save, open, and increment scene versions.
*   **Render Management:** Streamline render processes with queue management and output directory access.
    *   Start renders, manage render queues, and open output directories.
*   **Task Automation:** Automate batch operations and run custom scripts.
    *   Run predefined batch operations (e.g., import FBX, export OBJ).
    *   Execute custom Python scripts.
*   **Performance Optimization:** Optimize scene performance with cleanup tools.
    *   Remove unused data.
    *   Merge vertices by distance.
*   **Project Presets**: load blender files to serve as project presets to quickly set up projects

## Installation

1.  Download the latest release from the [Releases](https://github.com/ELIASADAMS/eli_lab_pipeline_hub/releases) page.
2.  In Blender, go to `Edit > Preferences > Add-ons`.
3.  Click the `Install...` button.
4.  Select the downloaded `.zip` file.~~~~
5.  Enable the addon by checking the box next to "eli_lab Pipeline Hub" in the list of addons.

## Usage

The "eli_lab Pipeline Hub" panel can be found in the 3D Viewport's sidebar (press `N` to toggle the sidebar).

### Detailed Descriptions of Each Module

#### Asset Management

*   **Asset Path:** Specifies the root directory for your assets. Click on the file icon to select a folder on your computer. This is where the addon will look for assets to import and where it will save exported assets.
*   **Asset Type:** Select the type of asset (Model, Texture, Rig, Material) you are working with. This helps to organize assets and apply specific import/export settings based on the asset type.
*   **Import Asset:** Imports an asset from the specified directory. The addon will look for files in the "Asset Path" directory, filtering by the "Asset Type" to show relevant files.
*   **Export Asset:** Exports the currently selected object(s) as an asset. The exported file will be saved in the "Asset Path" directory, and its file extension will be determined by the "Asset Type".
*   **Publish Asset:** Publishes the asset to the asset library.  *This step is crucial for making the asset readily available for use in other projects.  Implement functionality that copies the asset file to a designated "published" location.*

#### Scene Setup

*   **Project Presets Path:** Specifies the directory where your project preset files are stored. Project presets are `.blend` files containing pre-configured scene settings (units, render settings, etc.).
*   **Convert Units:** Opens a dialog to convert scene units to a preferred unit (Meters, Centimeters, Inches). *This will attempt to convert all the scene's measure to the selected one.*
*   **Setup Collections:** Creates a predefined set of collections in the scene. *This is useful for quickly organizing your scene's objects based on their type or function (e.g., "Characters," "Props," "Light").*

#### Linked Libraries

*   **Add Library:** Adds a new linked library to the list. *When clicked, a window will open to add the library location.*
*   **Remove Library:** Removes the selected linked library from the list.  *Careful! Objects will remain in the scene.*
*   **Update Library:** Updates the selected linked library. *This will attempt to get the newest version of the linked library.*
*   **Relink All Libraries:** Relinks all libraries in the scene. *Useful if your library files have been moved or renamed.*

#### Lighting & Rendering

*   **Add Preset:** Adds a new lighting preset. *Opens a new window to define the name for a new lighting setup.*
*   **Remove Preset:** Removes a lighting preset. *Careful! Lighting setup will be lost*
*   **Apply Preset:** Applies the selected lighting preset. *This loads the lighting settings from the preset file and applies them to the scene.*

#### Data Export & Versioning

*   **Export Path:** The directory where exported files will be saved. *Click the file icon to choose the folder for the exported files.*
*   **Export Format:** Choose the format for exporting data (FBX, OBJ, GLB, USD, Alembic). *Select the appropriate format based on compatibility with other software.*
*   **Incremental Save Comment:** Add a comment describing the changes before saving an incremental version. *Write short and clear comments for documentation.*
*   **Export Data:** Exports the selected data in the specified format. *Export the current scene.*
*   **Incremental Save Comment:** Save a comment with current scene *This will save the comment on the blender name version*

#### Scene Management

*   **Save Scene:** Saves the current scene. *Saves the active scene.*
*   **Open Scene:** Opens a scene from disk. *Opens the blender file browser for scene selection*
*   **Increment and Save:** Increments the scene version and saves the scene. *Saves a new file with a increment on the version number*
*   **Increment Version:** Increment the scene version without saving *Just increments the name version*
*   **Decrement Version:** Decrement the scene version *Decrements the number version of current name*

#### Render Management

*   **Start Render:** Starts the render process for the current scene. *Opens a blender window for rendering the scene.*
*   **Start Render Background:** Starts the render process in the background. *Starts the render process without a render window*
*   **Open Output Directory:** Opens the render output directory in your file explorer. *Opens the folder of the renders*
    *   **Render Queue:** Add to the Render Queue
    *   **Remove from Render Queue:** Remove from the Render Queue
    *   **Render Queue item setup**: Add blend file, Camera setup, resolution, samples

#### Task Automation

*   **Batch Operation:** Select a predefined batch operation. *Choose what batch operation to run*
*   **Custom Script:** Enter a custom Python script to run. *Add the script to the current scene, this script will run inside the current scene.*
*   **Run Batch Operation:** Runs the selected batch operation. *Starts a batch operation from the available operations.*
*   **Run Custom Script:** Executes the custom Python script. *Starts a Script written on custom script box.*

#### Performance Optimization

*   **Cleanup Unused Data:** Removes orphaned data blocks (materials, textures, etc.). *Removes the data not linked to the scene*
*   **Merge by Distance:** Removes duplicate vertices within a specified distance. *Removes doubles to optimize mesh performance.*

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bug fixes, new features, or improvements.

## License

This addon is released under the [GPLv3](LICENSE).

## Contact

[Ilya Minin (Eli)](https://t.me/eli_adams)