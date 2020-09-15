# Blockbuster JSON Blender exporter/generator script

This is resository is contains a Blender3d add-on that adds a menu item in the File > Export called `Blockbuster JSON`. With this add-on you can easily setup a Blockbuster mod custom model when exporting the OBJ file.

## How to install

Download this as zip, then in Blender's add-ons panel (File > User Preferences > Add-ons), click `Install from File...` and finally choose the downloaded zip. That should install this exporter script. 

Note: this branch of the script works Blender **2.8\***.

## How to use

Once you exported the OBJ/MTL file, you can use this add-ons' File > Export > `Blockbuster JSON (.json)` menu item to generate a JSON file with configured origin and default poses. Simply repeat same steps to export the OBJ file, but with this exporter, reload models in Blockbuster mod (by either pressing `B` key or `/model reload`, and it should work out).