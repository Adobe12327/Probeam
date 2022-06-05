import bpy
from . import JbeamImport
from . import JbeamExport

def import_jbeam(self, context, filepath):
    JbeamImport.read_jbeam(filepath)
    
    return {'FINISHED'}

def export_jbeam(self, context, filepath):
    JbeamExport.export_jbeam(filepath)
    
    return {'FINISHED'}



# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator


class ImportJbeam(Operator, ImportHelper):
    """Jbeam Import"""
    bl_idname = "import_jbeam.import"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import Jbeam"

    # ImportHelper mixin class uses this
    filename_ext = ".jbeam"

    filter_glob: StringProperty(
        default="*.jbeam",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        return import_jbeam(self, context, self.filepath)

class ExportJbeam(Operator, ImportHelper):
    """Jbeam Export"""
    bl_idname = "export_jbeam.import"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export jbeam"

    # ImportHelper mixin class uses this
    filename_ext = ".jbeam"

    filter_glob: StringProperty(
        default="*.jbeam",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        return export_jbeam(self, context, self.filepath)
