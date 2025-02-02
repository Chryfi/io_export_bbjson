bl_info = {
    "name": "Blockbuster JSON export",
    "author": "McHorse",
    "version": (0, 1, 2),
    "blender": (2, 77, 0),
    "location": "File > Export",
    "description": "Exports JSON model out of Blender document for Blockbuster mod. Its main task is to create limbs and poses configuration to avoid doing it by hand.",
    "warning": "",
    "category": "Export"
}

import bpy

from bpy.props import (BoolProperty, StringProperty)
from bpy_extras.io_utils import (ExportHelper, path_reference_mode)

# Export panel
class ExportOBJ(bpy.types.Operator, ExportHelper):
    # Panel's information
    bl_idname = "export_scene.bbjson"
    bl_label = 'Export Blockbuster JSON'
    bl_options = {'PRESET'}

    # Panel's properties
    filename_ext = ".json"
    filter_glob = StringProperty(default="*.json", options={'HIDDEN'})
    use_selection = BoolProperty(name="Selection Only", description="Export selected objects only", default=False)
    export_parents = BoolProperty(name="Export parent names", description="Save the parent names of the limbs. If deactivated, an anchor limb will be used as parent for every limb.", default=False)
    provides_mtl = BoolProperty(name="Provides Materials", description="Mark 'provides_mtl' as True", default=False)
    path_mode = path_reference_mode
    check_extension = True

    def execute(self, context):
        from . import export
        
        keywords = self.as_keywords(ignore=("axis_forward", "axis_up", "check_existing", "filter_glob", "path_mode"))
        
        return export.save(context, **keywords)

# Register and stuff
def menu_func_export(self, context):
    self.layout.operator(ExportOBJ.bl_idname, text="Blockbuster JSON (.json)")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)