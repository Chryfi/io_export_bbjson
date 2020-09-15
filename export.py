import os
import json
import ntpath

import bpy

from bpy_extras.wm_utils.progress_report import (
    ProgressReport,
    ProgressReportSubstep,
)

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

# Remove spaces from given string (so it would be spaceless)
def name_compat(name):
    return 'None' if name is None else name.replace(' ', '_')

def save(context, filepath, use_selection=True, provides_mtl=False):
    with ProgressReport(context.window_manager) as progress:
        scene = context.scene

        # Exit edit mode before exporting, so current object states are exported properly.
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT')

        objects = context.selected_objects if use_selection else scene.objects

        progress.enter_substeps(1)
        write_file(context, filepath, objects, scene, provides_mtl, progress)
        progress.leave_substeps()

    return {'FINISHED'}

def write_file(context, filepath, objects, scene, provides_mtl, progress=ProgressReport()):
    # bpy.ops.object.select_all(action='DESELECT')

    with ProgressReportSubstep(progress, 2, "JSON export path: %r" % filepath, "JSON export finished") as subprogress1:
        with open(filepath, "w", encoding="utf8", newline="\n") as f:
            limbs = {
                'anchor': {
                    'opacity': 0
                }
            }
            pose = {}

            for obj in objects:
                if obj.type != "MESH":
                    continue
                
                name1 = obj.name
                name2 = obj.data.name

                if name1 == name2:
                    name = name_compat(name1)
                else:
                    name = '%s_%s' % (name_compat(name1), name_compat(name2))
                
                cursor = obj.matrix_world.translation
                x = cursor[0]
                y = cursor[2]
                z = cursor[1]
                
                limb = { 
                    'origin': [x, y, -z],
                    'smooth': True,
                    'parent': 'anchor'
                }

                transform = {
                    'translate': [x * 16, y * 16, z * 16]
                }

                # Some automatic setup of limbs based on name
                if name1 == 'head':
                    limb['looking'] = True
                elif name1 == 'left_arm':
                    limb['holding'] = 'left'
                    limb['swinging'] = True
                    limb['idle'] = True
                    limb['invert'] = True
                elif name1 == 'right_arm':
                    limb['holding'] = 'right'
                    limb['swinging'] = True
                    limb['idle'] = True
                    limb['swiping'] = True
                elif name1 == 'right_leg':
                    limb['swinging'] = True
                    limb['invert'] = True
                elif name1 == 'left_leg':
                    limb['swinging'] = True
                
                limbs[name] = limb
                pose[name] = transform
            
            # Write JSON to the file
            pose = {
                'size': [0.6, 1.8, 0.6],
                'limbs': pose
            }
            
            data = {
                'scheme': "1.3",
                'providesObj': True,
                'providesMtl': provides_mtl,
                'name': path_leaf(filepath),
                'limbs': limbs,
                'poses': {
                    'standing': pose,
                    'sneaking': pose,
                    'sleeping': pose,
                    'flying': pose
                }
            }
            
            f.write(json.dumps(data, indent=4))

        subprogress1.step("Finished exporting JSON")