from .UI.ShowNodeID import ShowNodeID
from . import yaml
import bpy
import mathutils
import bmesh

class JBeam():
    def __init__(self):
        super().__init__()
        self.information = None #[]
        self.slotType = ""
        self.slots = None #[]
        self.flexbodies = None #[]
        self.nodes = None #[]
        self.beams = None #[]
        self.triangles = None #[]

class PANEL_PT_JBeamPanel(bpy.types.Panel):
    bl_label = "Jbeam"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    def draw(self, context):
        self.layout.use_property_split = True
        self.layout.use_property_decorate = False
    
# class GetNodeInfo(bpy.types.Operator):
#     """Get Node Info"""
#     bl_idname = "jbeam.get_node_info"
#     bl_label = "Get Selected Node Info"
    
#     @classmethod
#     def poll(cls, context):
#         return context.mode=="EDIT_MESH"
    
#     def invoke(self, context, event):
#         mode = bpy.context.active_object.mode
#         bpy.ops.object.mode_set(mode='OBJECT')
#         selected_vert = [v for v in bpy.context.active_object.data.vertices if v.select]
#         if len(selected_vert) != 0:
#             selected_vert = selected_vert[0]
#             bpy.ops.object.mode_set(mode=mode)
#             node = bpy.context.active_object.data.jbeam.nodes[selected_vert.index]
#             bpy.context.scene.jbeam.nodename = node.id
#         else:
#             bpy.ops.object.mode_set(mode=mode)
#             bpy.context.scene.jbeam.nodename = ""
        
#         return {"FINISHED"}

class CopyNodeModifier(bpy.types.Operator):
    """Copy Node Modifier"""
    bl_idname = "jbeam.copy_node_modifier"
    bl_label = "Copy Node Modifier"
    
    @classmethod
    def poll(cls, context):
        return context.mode=="EDIT_MESH"
    
    def invoke(self, context, event):
        bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
        nodes = bm.select_history
        if len(nodes) != 0:
            if type(nodes.active) == bmesh.types.BMVert:
                main_vert = nodes[0]
                node = bpy.context.active_object.data.jbeam.nodes[main_vert.index]
                modifier = node.modifier
                modifier_index = node.modifier_index
                for i in range(1, len(nodes), 1):
                    nodee = bpy.context.active_object.data.jbeam.nodes[nodes[i].index]
                    nodee.modifier.clear()
                    for mod in modifier:
                        modi = nodee.modifier.add()
                        modi.type = mod.type
                        modi.value_type = mod.value_type
                        modi.value_int = mod.value_int
                        modi.value_float = mod.value_float
                        modi.value_bool = mod.value_bool
                        modi.value_string = mod.value_string
                        modi.value_vector.x = mod.value_vector.x
                        modi.value_vector.y = mod.value_vector.y
                        modi.value_vector.z = mod.value_vector.z
                        modi.modifier_index = modifier_index
                self.report({'INFO'}, f"{len(nodee.modifier)} modifiers have copied to {len(nodes)-1} nodes")
        
        return {"FINISHED"}

class CopyBeamModifier(bpy.types.Operator):
    """Copy Beam Modifier"""
    bl_idname = "jbeam.copy_beam_modifier"
    bl_label = "Copy Beam Modifier"
    
    @classmethod
    def poll(cls, context):
        return context.mode=="EDIT_MESH"
    
    def invoke(self, context, event):
        bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
        beams = bm.select_history
        if len(beams) != 0:
            if type(beams.active) == bmesh.types.BMEdge:
                main_edge = beams[0]
                beam = bpy.context.active_object.data.jbeam.beams[FindBeamIndexbyIds(main_edge.verts[0].index, main_edge.verts[1].index)]
                modifier = beam.modifier
                modifier_index = beam.modifier_index
                for i in range(1, len(beams), 1):
                    beame = bpy.context.active_object.data.jbeam.beams[FindBeamIndexbyIds(beams[i].verts[0].index, beams[i].verts[1].index)]
                    beame.modifier.clear()
                    for mod in modifier:
                        modi = beame.modifier.add()
                        modi.type = mod.type
                        modi.value_type = mod.value_type
                        modi.value_int = mod.value_int
                        modi.value_float = mod.value_float
                        modi.value_bool = mod.value_bool
                        modi.value_string = mod.value_string
                        modi.value_vector.x = mod.value_vector.x
                        modi.value_vector.y = mod.value_vector.y
                        modi.value_vector.z = mod.value_vector.z
                        modi.modifier_index = modifier_index
                self.report({'INFO'}, f"{len(beame.modifier)} modifiers have copied to {len(beams)-1} beams")
        
        return {"FINISHED"}

class CopyTriangleModifier(bpy.types.Operator):
    """Copy triangle Modifier"""
    bl_idname = "jbeam.copy_triangle_modifier"
    bl_label = "Copy Triangle Modifier"
    
    @classmethod
    def poll(cls, context):
        return context.mode=="EDIT_MESH"
    
    def invoke(self, context, event):
        bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
        triangles = bm.select_history
        if len(triangles) != 0:
            if type(triangles.active) == bmesh.types.BMFace:
                main_edge = triangles[0]
                triangle = bpy.context.active_object.data.jbeam.triangles[FindTriangleIndexbyIds(main_edge.verts[0].index, main_edge.verts[1].index, main_edge.verts[2].index)]
                modifier = triangle.modifier
                modifier_index = triangle.modifier_index
                for i in range(1, len(triangles), 1):
                    trianglee = bpy.context.active_object.data.jbeam.triangles[FindTriangleIndexbyIds(triangles[i].verts[0].index, triangles[i].verts[1].index, triangles[i].verts[2].index)]
                    trianglee.modifier.clear()
                    for mod in modifier:
                        modi = trianglee.modifier.add()
                        modi.type = mod.type
                        modi.value_type = mod.value_type
                        modi.value_int = mod.value_int
                        modi.value_float = mod.value_float
                        modi.value_bool = mod.value_bool
                        modi.value_string = mod.value_string
                        modi.value_vector.x = mod.value_vector.x
                        modi.value_vector.y = mod.value_vector.y
                        modi.value_vector.z = mod.value_vector.z
                        modi.modifier_index = modifier_index
                self.report({'INFO'}, f"{len(trianglee.modifier)} modifiers have copied to {len(triangles)-1} triangles")
        
        return {"FINISHED"}

def FindNodeIndexById(id):
    for i, n in enumerate(bpy.context.active_object.data.jbeam.nodes):
        if n.id == id:
            return i

def FindNodeIdByIndex(index):
    return bpy.context.active_object.data.jbeam.nodes[index].id

def FindBeamIndexbyIds(id1, id2):
    for i, b in enumerate(bpy.context.active_object.data.jbeam.beams):
        if b.id1 == FindNodeIdByIndex(id1) and b.id2 == FindNodeIdByIndex(id2):
            return i
        elif b.id1 == FindNodeIdByIndex(id2) and b.id2 == FindNodeIdByIndex(id1):
            return i
    else:
        return None

def FindTriangleIndexbyIds(id1, id2, id3):
    id1 = FindNodeIdByIndex(id1)
    id2 = FindNodeIdByIndex(id2)
    id3 = FindNodeIdByIndex(id3)
    for i, t in enumerate(bpy.context.active_object.data.jbeam.triangles):
        if t.id1 == id1 and t.id2 == id2 and t.id3 == id3:
            return i
        if t.id1 == id1 and t.id2 == id3 and t.id3 == id2:
            return i
        if t.id1 == id2 and t.id2 == id3 and t.id3 == id1:
            return i
        if t.id1 == id2 and t.id2 == id1 and t.id3 == id3:
            return i
        if t.id1 == id3 and t.id2 == id1 and t.id3 == id2:
            return i
        if t.id1 == id3 and t.id2 == id2 and t.id3 == id1:
            return i
    else:
        return None

class RefreshAll(bpy.types.Operator):
    """Refresh All"""
    bl_idname = "jbeam.refresh_all"
    bl_label = "Refresh All"
    
    @classmethod
    def poll(cls, context):
        return context.mode=="EDIT_MESH"
    
    def invoke(self, context, event):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.mode_set(mode = 'EDIT') 
        for v in bpy.context.active_object.data.vertices:
            jbeam = bpy.context.active_object.data.jbeam
            try:
                node = bpy.context.active_object.data.jbeam.nodes[v.index]
            except IndexError:
                if v.co.x > 0:
                    if v.co.y > 0:
                        if v.co.x == 0:
                            add_node = jbeam.nodes.add()
                            add_node.id = f"r{v.index}"
                        else:
                            add_node = jbeam.nodes.add()
                            add_node.id = f"r{v.index}l"
                    else:
                        if v.co.x == 0:
                            add_node = jbeam.nodes.add()
                            add_node.id = f"f{v.index}"
                        else:
                            add_node = jbeam.nodes.add()
                            add_node.id = f"f{v.index}l"
                else:
                    if v.co.y > 0:
                        if v.co.x == 0:
                            add_node = jbeam.nodes.add()
                            add_node.id = f"r{v.index}"
                        else:
                            add_node = jbeam.nodes.add()
                            add_node.id = f"r{v.index}r"
                    else:
                        if v.co.x == 0:
                            add_node = jbeam.nodes.add()
                            add_node.id = f"f{v.index}"
                        else:
                            add_node = jbeam.nodes.add()
                            add_node.id = f"f{v.index}r"
                jbeam.nodes_index = len(jbeam.nodes)-1
        for e in bpy.context.active_object.data.edges:
            jbeam = bpy.context.active_object.data.jbeam
            id1 = e.vertices[0]
            id2 = e.vertices[1]
            if FindBeamIndexbyIds(id1, id2) == None:
                add_beam = jbeam.beams.add()
                add_beam.id1 = FindNodeIdByIndex(id1)
                add_beam.id2 = FindNodeIdByIndex(id2)
        for p in bpy.context.active_object.data.polygons:
            jbeam = bpy.context.active_object.data.jbeam
            id1 = p.vertices[0]
            id2 = p.vertices[1]
            id3 = p.vertices[2]
            if FindTriangleIndexbyIds(id1, id2, id3) == None:
                add_triangle = jbeam.triangles.add()
                add_triangle.id1 = FindNodeIdByIndex(id1)
                add_triangle.id2 = FindNodeIdByIndex(id2)
                add_triangle.id3 = FindNodeIdByIndex(id3)
        
        return {"FINISHED"}

class SelectOnList(bpy.types.Operator):
    """Select On List"""
    bl_idname = "jbeam.select_on_list"
    bl_label = "Select On List"
    
    @classmethod
    def poll(cls, context):
        return context.mode=="EDIT_MESH"

    def invoke(self, context, event):
        bpy.ops.object.mode_set(mode='OBJECT')
        face = [v for v in bpy.context.active_object.data.polygons if v.select]
        edge = [v for v in bpy.context.active_object.data.edges if v.select]
        vert = [v for v in bpy.context.active_object.data.vertices if v.select]
        bpy.ops.object.mode_set(mode='EDIT')
        if len(face) != 0:
            res = FindTriangleIndexbyIds(face[0].vertices[0], face[0].vertices[1], face[0].vertices[2])
            if res != None:
                bpy.context.active_object.data.jbeam.triangles_index = res
        elif len(edge) != 0:
            res = FindBeamIndexbyIds(edge[0].vertices[0], edge[0].vertices[1])
            if res != None:
                bpy.context.active_object.data.jbeam.beams_index = res
        elif len(vert) != 0:
            bpy.context.active_object.data.jbeam.nodes_index = vert[0].index
    
        return {"FINISHED"}

class PANEL_PT_JBeamPanel_Side_Modifier(bpy.types.Panel):
    bl_label = 'Copy Modifier'
    bl_parent_id = 'PANEL_PT_JBeamPanel_Side'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        column = self.layout.column()
        column.scale_y = 2
        column.operator(CopyNodeModifier.bl_idname, icon='VERTEXSEL')
        column.operator(CopyBeamModifier.bl_idname, icon='EDGESEL')
        column.operator(CopyTriangleModifier.bl_idname, icon='FACESEL')

class PANEL_PT_JBeamPanel_Side(bpy.types.Panel):
    bl_label = 'Jbeam'
    bl_category = 'Jbeam'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        column = self.layout.column()
        column.scale_y = 2
        column.operator(ShowNodeID.bl_idname, icon='HIDE_OFF')
        column.operator(RefreshAll.bl_idname, icon='FILE_REFRESH')
        column.operator(SelectOnList.bl_idname, icon='COLLAPSEMENU')

def modifier_write(obj, parent):
    for modifier in obj["modifier"]:
        obj_add = parent.modifier.add()
        obj_add.type = modifier
        if type(obj["modifier"][modifier]) == list:
            obj_add.value_type = "STRING"
            obj_add.value_string = str(obj["modifier"][modifier])
        elif type(obj["modifier"][modifier]) == bool:
            obj_add.value_type = "BOOL"
            obj_add.value_bool = obj["modifier"][modifier]
        elif type(obj["modifier"][modifier]) == int:
            obj_add.value_type = "INTEGER"
            obj_add.value_int = obj["modifier"][modifier]
        elif type(obj["modifier"][modifier]) == float:
            obj_add.value_type = "FLOAT"
            obj_add.value_float = obj["modifier"][modifier]
        elif type(obj["modifier"][modifier]) == str:
            obj_add.value_type = "STRING"
            obj_add.value_string = obj["modifier"][modifier]
        elif type(obj["modifier"][modifier]) == dict:
            obj_add.value_type = "VECTOR"
            obj_add.value_vector.x = obj["modifier"][modifier]['x']
            obj_add.value_vector.y = obj["modifier"][modifier]['y']
            obj_add.value_vector.z = obj["modifier"][modifier]['z']

# WRITE JBEAM
def write_jbeam(jbeam:JBeam):
    if jbeam.nodes != None:
        nodes = jbeam.nodes
        beams = jbeam.beams
        triangles = jbeam.triangles
        vertices_raw = {}
        if nodes != None:
            for i in range(len(nodes)):
                vertices_raw[nodes[i]["id"]] = [i, [nodes[i]["posX"], nodes[i]["posY"], nodes[i]["posZ"]]]
        edges_raw = []
        if beams != None:
            for i in range(len(beams)):
                edges_raw.append([beams[i]["id1:"], beams[i]["id2:"]])
        polygons_raw = []
        if triangles != None:
            for i in range(len(triangles)):
                polygons_raw.append([triangles[i]["id1:"], triangles[i]["id2:"], triangles[i]["id3:"]])
        vertices = []
        for v in vertices_raw:
            vertices.append(vertices_raw[v][1])
        edges = []
        for a, b in edges_raw:
            try:
                edges.append([vertices_raw[a][0], vertices_raw[b][0]])
            except:
                pass
        polygons = []
        for a, b, c in polygons_raw:
            try:
                polygons.append([vertices_raw[a][0], vertices_raw[b][0], vertices_raw[c][0]])
            except:
                pass
        mesh = bpy.data.meshes.new("mesh")
        mesh.from_pydata(vertices, edges, polygons)
        mesh.update()
        obj = bpy.data.objects.new(jbeam.slotType, mesh)

        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj

        obj.select_set(True)

        mesh.jbeam.slot_type = jbeam.slotType

        #information
        if jbeam.information == None:
            mesh.jbeam.export_information = False
        else:
            mesh.jbeam.name = jbeam.information["name"]
            mesh.jbeam.authors = jbeam.information["authors"]
            if not "value" in jbeam.information:
                mesh.jbeam.export_information_value = False
            else:
                mesh.jbeam.value = jbeam.information["value"]

        #slots
        if jbeam.slots == None:
            mesh.jbeam.export_slots = False
        else:
            for slot in jbeam.slots:
                slot_add = mesh.jbeam.slots.add()
                slot_add.type = slot["type"]
                slot_add.default = slot["default"]
                slot_add.description = slot["description"]
                if len(slot["modifier"]) != 0:
                    modifier_write(slot, slot_add)

        #flexbodies
        if jbeam.flexbodies == None:
            mesh.jbeam.export_flexbodies = False
        else:
            for flexbody in jbeam.flexbodies:
                flexbody_add = mesh.jbeam.flexbodies.add()
                flexbody_add.mesh = flexbody["mesh"]
                for g in flexbody["[group]:"]:
                    add_group = flexbody_add.group.add()
                    add_group.data = g
                if len(flexbody["modifier"]) != 0:
                    modifier_write(flexbody, flexbody_add)

        #nodes
        if jbeam.nodes == None:
            mesh.jbeam.export_nodes = False
        else:
            for node in nodes:
                node_add = mesh.jbeam.nodes.add()
                node_add.id = node["id"]
                node_add.co.posX = node["posX"]
                node_add.co.posY = node["posY"]
                node_add.co.posZ = node["posZ"]
                if len(node["modifier"]) != 0:
                    modifier_write(node, node_add)

        #beams
        if jbeam.beams == None:
            mesh.jbeam.export_beams = False
        else:
            for beam in jbeam.beams:
                beam_add = mesh.jbeam.beams.add()
                beam_add.id1 = beam["id1:"]
                beam_add.id2 = beam["id2:"]
                if len(beam["modifier"]) != 0:
                    modifier_write(beam, beam_add)

        #triangles
        if jbeam.triangles == None:
            mesh.jbeam.export_triangles = False
        else:
            for triangle in jbeam.triangles:
                triangle_add = mesh.jbeam.triangles.add()
                triangle_add.id1 = triangle["id1:"]
                triangle_add.id2 = triangle["id2:"]
                triangle_add.id3 = triangle["id3:"]
                if len(triangle["modifier"]) != 0:
                    modifier_write(triangle, triangle_add)


def read_jbeam(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    content = content.split("\n")
    for i in range(len(content)):
        if content[i].__contains__("//") == True:
            content[i] = content[i][:content[i].find("//")]
    dd = 0
    for i in range(len(content)):
        try:
            if content[i-dd].__contains__("/*") == True:
                d = i-dd
                for v in range(len(content)):
                    if content[v-dd].__contains__("*/") == True:
                        d2 = v-dd
                        del content[d:d2+2]
                        dd += d2-d
                        break
        except IndexError:
            pass
    content = "\n".join(content)
    content = content.replace("[]{", "[],{")
    content = content.replace('"\n', '",\n')
    content = content.replace('}\n', '},\n')
    content = content.replace(']\n', '],\n')
    content = content.replace(']"', '],"')
    content = content.replace("true", "True")
    content = content.replace("false", "False")
    content = yaml.load(content)
    objs = []
    for k in content:
        objs.append(k)
    jbeams = []
    global table
    global key
    for obj in objs:
        jbeam = JBeam()
        jbeam.information = content[obj]['information']
        jbeam.slotType = content[obj]["slotType"]
        if "slots" in content[obj]:
            slots_final = get_objs(content, obj, "slots")
            jbeam.slots = slots_final

        if "flexbodies" in content[obj]:
            flexbodies_final = get_objs(content, obj, "flexbodies")
            jbeam.flexbodies = flexbodies_final

        if "nodes" in content[obj]:
            nodes_final = get_objs(content, obj, "nodes")
            jbeam.nodes = nodes_final

        if "beams" in content[obj]:
            beams_final = get_objs(content, obj, "beams")
            jbeam.beams = beams_final

        if "triangles" in content[obj]:
            triangles_final = get_objs(content, obj, "triangles")
            jbeam.triangles = triangles_final

        jbeams.append(jbeam)
    for jb in jbeams:
            write_jbeam(jb)

def get_objs(content, obj, to_get):
    obj_data = content[obj][to_get]
    currentData = {}
    obj_data_final = []
    for i in range(len(obj_data)):
        if i == 0:
            table = obj_data[i]
        elif type(obj_data[i]) == dict:
            for k in obj_data[i]:
                currentData[k] = obj_data[i][k]
        elif type(obj_data[i]) == list:
            object = {}
            object["modifier"] = {}
            for v in range(len(table)):
                try:
                    object[table[v]] = obj_data[i][v]
                except:
                    pass
            for k in currentData:
                object["modifier"][k] = currentData[k]
            if len(obj_data[i]) > len(table):
                for k in obj_data[i][len(table)]:
                    object["modifier"][k] = obj_data[i][len(table)][k]
            obj_data_final.append(object)
    return obj_data_final