import bpy

from .UI.JBEAM.Flexbody import *
from .UI.JBEAM.Triangles import *
from .UI.JBEAM.Beams import *
from .UI.JBEAM.Nodes import *
from .UI.JBEAM.Information import PANEL_PT_JBeamInformationPanel
from .UI.JBEAM.Slots import *
from .UI.ShowNodeID import ShowNodeID
from . import Operator
from .JbeamImport import *

bl_info = {
    "name": "Probeam | the jbeam blender addon",
    "author": "Adobe#7248",
    "description": "Probeam is an jbeam blender addon",
    "blender": (2, 93, 0),
    "version": (1, 0, 0),
    "location": "",
    "warning": "",
    "category": "Import-Export"
}


custom_property = [
    ("INTEGER", "Integer", "", 1),
    ("FLOAT", "Float", "", 2),
    ("BOOL", "Bool", "", 3),
    ("STRING", "String", "", 4),
    ("VECTOR", "Vector", "", 5)
]

class Vector(bpy.types.PropertyGroup):
    x : bpy.props.FloatProperty()
    y : bpy.props.FloatProperty()
    z : bpy.props.FloatProperty()

class Modifier(bpy.types.PropertyGroup):
    type: bpy.props.StringProperty()
    value_type : bpy.props.EnumProperty(items=custom_property)
    value_int : bpy.props.IntProperty()
    value_float : bpy.props.FloatProperty()
    value_bool : bpy.props.BoolProperty()
    value_string : bpy.props.StringProperty()
    value_vector : bpy.props.PointerProperty(type=Vector)

class Node(bpy.types.PropertyGroup):
    id : bpy.props.StringProperty(name="ID")
    co : bpy.props.PointerProperty(type=Vector)
    modifier : bpy.props.CollectionProperty(type=Modifier)
    modifier_index : bpy.props.IntProperty()

class Beam(bpy.types.PropertyGroup):
    id1 : bpy.props.StringProperty()
    id2 : bpy.props.StringProperty()
    modifier : bpy.props.CollectionProperty(type=Modifier)
    modifier_index : bpy.props.IntProperty()

class Triangle(bpy.types.PropertyGroup):
    id1 : bpy.props.StringProperty()
    id2 : bpy.props.StringProperty()
    id3 : bpy.props.StringProperty()
    modifier : bpy.props.CollectionProperty(type=Modifier)
    modifier_index : bpy.props.IntProperty()

class Slot(bpy.types.PropertyGroup):
    type : bpy.props.StringProperty()
    default: bpy.props.StringProperty()
    description : bpy.props.StringProperty()
    modifier : bpy.props.CollectionProperty(type=Modifier)
    modifier_index : bpy.props.IntProperty()

class Group(bpy.types.PropertyGroup):
    data : bpy.props.StringProperty()

class Flexbody(bpy.types.PropertyGroup):
    mesh : bpy.props.StringProperty()
    group : bpy.props.CollectionProperty(type=Group)
    group_index : bpy.props.IntProperty()
    modifier : bpy.props.CollectionProperty(type=Modifier)
    modifier_index : bpy.props.IntProperty()

class PROPERTIES_PG_jbeam_object(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name",description="",default="")
    authors: bpy.props.StringProperty(name="Authors",description="",default="")
    value: bpy.props.IntProperty(name="Value",description="", min=0)
    slot_type: bpy.props.StringProperty(name="Slot Type",description="",default="main")
    export_information : bpy.props.BoolProperty(default=True)
    export_information_value : bpy.props.BoolProperty(default=True)
    export_slots : bpy.props.BoolProperty(default=True)
    export_nodes : bpy.props.BoolProperty(default=True)
    export_beams : bpy.props.BoolProperty(default=True)
    export_triangles : bpy.props.BoolProperty(default=True)
    export_flexbodies : bpy.props.BoolProperty(default=True)
    slots : bpy.props.CollectionProperty(name="Slots", type=Slot)
    slots_index : bpy.props.IntProperty()
    nodes: bpy.props.CollectionProperty(name="Node", type=Node)
    nodes_index : bpy.props.IntProperty()
    beams : bpy.props.CollectionProperty(name="Beams", type=Beam)
    beams_index : bpy.props.IntProperty()
    triangles : bpy.props.CollectionProperty(name="Triangles", type=Triangle)
    triangles_index : bpy.props.IntProperty()
    flexbodies : bpy.props.CollectionProperty(name="Flexbodies", type=Flexbody)
    flexbodies_index : bpy.props.IntProperty()
    flexbody_group_data : bpy.props.StringProperty(name="Data")

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(Operator.ImportJbeam.bl_idname, text="BeamNG beam(.jbeam)")

def menu_func_export(self, context):
    self.layout.operator(Operator.ExportJbeam.bl_idname, text="BeamNG beam(.jbeam)")

class CurrentData(bpy.types.PropertyGroup):
    slots_type : bpy.props.StringProperty(name="Type")
    slots_default : bpy.props.StringProperty(name="Default")
    slots_description : bpy.props.StringProperty(name="Description")
    flexbodies_mesh :bpy.props.StringProperty(name="Mesh")
    flexbodies_group : bpy.props.CollectionProperty(name="Group", type=Group)
    flexbody_group_data : bpy.props.StringProperty(name="Data")
    modifier_type : bpy.props.StringProperty(name="Type")
    modifier_value_type : bpy.props.EnumProperty(name="Value Type", items=custom_property)
    modifier_value_int : bpy.props.IntProperty(name="Value")
    modifier_value_float : bpy.props.FloatProperty(name="Value")
    modifier_value_bool : bpy.props.BoolProperty(name="Value")
    modifier_value_string : bpy.props.StringProperty(name="Value")
    modifier_value_vector : bpy.props.PointerProperty(type=Vector)
    node_id : bpy.props.StringProperty(name="Node ID")
    nodename : bpy.props.StringProperty(name="Node Name")
    beams_id1 : bpy.props.StringProperty(name="ID1")
    beams_id2 : bpy.props.StringProperty(name="ID2")

classes = (
    Operator.ImportJbeam,
    Operator.ExportJbeam,
    Vector,
    Modifier,
    Beam,
    Node,
    Triangle,
    Slot,
    Group,
    Flexbody,
    PROPERTIES_PG_jbeam_object,
    PANEL_PT_JBeamPanel_Side,
    PANEL_PT_JBeamPanel_Side_Modifier,
    CopyNodeModifier,
    CopyBeamModifier,
    CopyTriangleModifier,
    RefreshAll,
    SelectOnList,
    ShowNodeID,
    PANEL_PT_JBeamPanel,
    PANEL_PT_JBeamInformationPanel,
    PANEL_PT_JBeamSlotTypePanel,
    PANEL_PT_JBeamSlotPanel,
    PANEL_PT_JBeamSlotModifierPanel,
    NODEMODIFIER_UL_items,
    SLOTMODIFIER_UL_items,
    SLOTS_UL_items,
    SLOTS_OT_actions,
    SLOTSMODIFIER_OT_actions,
    FLEXBODIES_UL_items,
    FLEXBODIESMODIFIER_UL_items,
    FLEXBODIESMODIFIER_OT_actions,
    Flexbodies_OT_actions,
    PANEL_PT_JBeamFlexbodiesPanel,
    PANEL_PT_JBeamFlexbodiesGroupPanel,
    PANEL_PT_JBeamFlexbodiesModifierPanel,
    CurrentData,
    NODES_OT_actions,
    NODES_UL_items,
    FLEXBODYGROUP_OT_actions,
    FLEXBODYGROUP_UL_items,
    NODESMODIFIER_OT_actions,
    PANEL_PT_JBeamNodesPanel,
    PANEL_PT_JBeamNodesModifierPanel,
    Beams_OT_actions,
    BEAMMODIFIER_UL_items,
    BEAMSMODIFIER_OT_actions,
    BEAMS_UL_items,
    PANEL_PT_JBeamBeamsPanel,
    PANEL_PT_JBeamBeamsModifierPanel,
    Triangles_OT_actions,
    TRIANGLEMODIFIER_UL_items,
    TRIANGLESMODIFIER_OT_actions,
    TRIANGLES_UL_items,
    PANEL_PT_JBeamTrianglesPanel,
    PANEL_PT_JBeamTrianglesModifierPanel,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Mesh.jbeam = bpy.props.PointerProperty(name="Jbeam settings", type=PROPERTIES_PG_jbeam_object)
    bpy.types.Scene.show_node_id = bpy.props.IntProperty(name="Show Node ID's")
    bpy.types.Scene.jbeam = bpy.props.PointerProperty(type=CurrentData)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Mesh.jbeam
    del bpy.types.Scene.show_node_id
    del bpy.types.Scene.jbeam
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
