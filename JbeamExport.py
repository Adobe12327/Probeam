import itertools
import bpy

def FindNodeIndexById(id):
    for i, n in enumerate(bpy.context.active_object.data.jbeam.nodes):
        if n.id == id:
            return i

def export_jbeam(filepath):
    f = open(filepath, 'w')
    f.write('{\n')
    for obj in bpy.context.selected_objects:
        jbeam = obj.data.jbeam
        f.write(f'"{obj.name}":'+'{\n')


        if jbeam.export_information == True:
            f.write('\t"information":{\n')
            f.write(f'\t\t"authors":"{jbeam.authors}",\n')
            f.write(f'\t\t"name":"{jbeam.name}",\n')
            if jbeam.export_information_value == True:
                f.write(f'\t\t"value":{jbeam.value},\n')
            f.write('\t},\n')
        f.write(f'\t"slotType" : "{jbeam.slot_type}",\n')


        if jbeam.export_slots == True:
            f.write('\t"slots" : [\n')
            f.write('\t\t["type", "default", "description"],\n')
            for slot in jbeam.slots:
                f.write(f'\t\t["{slot.type}","{slot.default}","{slot.description}"],\n')
            f.write('\t],\n')

        if jbeam.export_flexbodies == True:
            f.write('\t"flexbodies": [\n')
            f.write('\t\t["mesh", "[group]:", "nonFlexMaterials"],\n')
            mods = {}
            node_table = {}
            currentdata = {}
            for n in jbeam.flexbodies:
                modifier = {}
                for m in n.modifier:
                    if m.value_type == 'INTEGER':
                        modifier[m.type] = m.value_int
                    if m.value_type == 'FLOAT':
                        modifier[m.type] = round(m.value_float, 3)
                    if m.value_type == 'BOOL':
                        res = str(m.value_bool).replace('True', 'true').replace('False', 'false')
                        modifier[m.type] = res
                    if m.value_type == 'STRING':
                        modifier[m.type] = f'"{m.value_string}"'
                    if m.value_type == 'VECTOR':
                        modifier[m.type] = [round(m.value_vector.x, 3), round(m.value_vector.y, 3), round(m.value_vector.z, 3)]
                towrite = []
                for m in modifier:
                    if not m in currentdata:
                        currentdata[m] = modifier[m]
                        towrite.append([m, modifier[m]])
                    else:
                        if not currentdata[m] == modifier[m]:
                            currentdata[m] = modifier[m]
                            towrite.append([m, modifier[m]])
                idx = len(mods)
                if len(towrite) != 0:
                    mods[str(len(node_table))] = towrite
                    idx = len(mods)
                    try:
                        ff = []
                        for d in n.group:
                            ff.append(d.data)
                        node_table[str(idx)].append([n.mesh, ff])
                    except KeyError:
                        node_table[str(idx)] = []
                        ff = []
                        for d in n.group:
                            ff.append(d.data)
                        node_table[str(idx)].append([n.mesh, ff])
                else:
                    if idx == 0:
                        idx = 1
                    try:
                        ff = []
                        for d in n.group:
                            ff.append(d.data)
                        node_table[str(idx-1)].append([n.mesh, ff])
                    except KeyError:
                        node_table[str(idx-1)] = []
                        ff = []
                        for d in n.group:
                            ff.append(d.data)
                        node_table[str(idx-1)].append([n.mesh, ff])
            for i in range(len(node_table)):
                if str(i) in mods:
                    for mm in mods[str(i)]:
                        f.write('\t\t{"'+mm[0]+'":'+str(mm[1])+'},\n')
                for n in node_table[str(i)]:
                    a = str(n[1]).replace("'", '"')
                    f.write(f'\t\t["{n[0]}",{a}],\n')
            f.write('\t\t{"deformGroup":""},\n')
            f.write('\t],\n')

        if jbeam.export_nodes == True:
            f.write('\t"nodes": [\n')
            f.write('\t\t["id", "posX", "posY", "posZ"],\n')
            mods = {}
            node_table = {}
            currentdata = {}
            for n in jbeam.nodes:
                modifier = {}
                for m in n.modifier:
                    if m.value_type == 'INTEGER':
                        modifier[m.type] = m.value_int
                    if m.value_type == 'FLOAT':
                        modifier[m.type] = round(m.value_float, 3)
                    if m.value_type == 'BOOL':
                        res = str(m.value_bool).replace('True', 'true').replace('False', 'false')
                        modifier[m.type] = res
                    if m.value_type == 'STRING':
                        modifier[m.type] = f'"{m.value_string}"'
                    if m.value_type == 'VECTOR':
                        modifier[m.type] = [round(m.value_vector.x, 3), round(m.value_vector.y, 3), round(m.value_vector.z, 3)]
                towrite = []
                for m in modifier:
                    if not m in currentdata:
                        currentdata[m] = modifier[m]
                        towrite.append([m, modifier[m]])
                    else:
                        if not currentdata[m] == modifier[m]:
                            currentdata[m] = modifier[m]
                            towrite.append([m, modifier[m]])
                idx = len(mods)
                if len(towrite) != 0:
                    mods[str(len(node_table))] = towrite
                    idx = len(mods)
                    try:
                        node_table[str(idx)].append(n.id)
                    except KeyError:
                        node_table[str(idx)] = []
                        node_table[str(idx)].append(n.id)
                else:
                    try:
                        node_table[str(idx-1)].append(n.id)
                    except KeyError:
                        node_table[str(idx-1)] = []
                        node_table[str(idx-1)].append(n.id)
            for i in range(len(node_table)):
                if str(i) in mods:
                    for mm in mods[str(i)]:
                        f.write('\t\t{"'+mm[0]+'":'+str(mm[1])+'},\n')
                for n in node_table[str(i)]:
                    coord = bpy.context.active_object.data.vertices[FindNodeIndexById(n)].co
                    f.write(f'\t\t["{n}",{round(coord.x,2)},{round(coord.y,2)},{round(coord.z,2)}],\n')
            f.write('\t\t{"group":""},\n')
            f.write('\t],\n')

        if jbeam.export_beams == True:
            f.write('\t"beams": [\n')
            f.write('\t\t["id1:", "id2:"],\n')
            mods = {}
            node_table = {}
            currentdata = {}
            for n in jbeam.beams:
                modifier = {}
                for m in n.modifier:
                    if m.value_type == 'INTEGER':
                        modifier[m.type] = m.value_int
                    if m.value_type == 'FLOAT':
                        modifier[m.type] = round(m.value_float, 3)
                    if m.value_type == 'BOOL':
                        res = str(m.value_bool).replace('True', 'true').replace('False', 'false')
                        modifier[m.type] = res
                    if m.value_type == 'STRING':
                        modifier[m.type] = f'"{m.value_string}"'
                    if m.value_type == 'VECTOR':
                        modifier[m.type] = [round(m.value_vector.x, 3), round(m.value_vector.y, 3), round(m.value_vector.z, 3)]
                towrite = []
                for m in modifier:
                    if not m in currentdata:
                        currentdata[m] = modifier[m]
                        towrite.append([m, modifier[m]])
                    else:
                        if not currentdata[m] == modifier[m]:
                            currentdata[m] = modifier[m]
                            towrite.append([m, modifier[m]])
                idx = len(mods)
                if len(towrite) != 0:
                    mods[str(len(node_table))] = towrite
                    idx = len(mods)
                    try:
                        node_table[str(idx)].append([n.id1, n.id2])
                    except KeyError:
                        node_table[str(idx)] = []
                        node_table[str(idx)].append([n.id1, n.id2])
                else:
                    try:
                        node_table[str(idx-1)].append([n.id1, n.id2])
                    except KeyError:
                        node_table[str(idx-1)] = []
                        node_table[str(idx-1)].append([n.id1, n.id2])
            for i in range(len(node_table)):
                if str(i) in mods:
                    for mm in mods[str(i)]:
                        f.write('\t\t{"'+mm[0]+'":'+str(mm[1])+'},\n')
                for n in node_table[str(i)]:
                    f.write(f'\t\t["{n[0]}","{n[1]}"],\n')
                
            f.write('\t],\n')

        if jbeam.export_triangles == True:
            f.write('\t"triangles": [\n')
            f.write('\t\t["id1:","id2:","id3:"],\n')
            mods = {}
            node_table = {}
            currentdata = {}
            for n in jbeam.triangles:
                modifier = {}
                for m in n.modifier:
                    if m.value_type == 'INTEGER':
                        modifier[m.type] = m.value_int
                    if m.value_type == 'FLOAT':
                        modifier[m.type] = round(m.value_float, 3)
                    if m.value_type == 'BOOL':
                        res = str(m.value_bool).replace('True', 'true').replace('False', 'false')
                        modifier[m.type] = res
                    if m.value_type == 'STRING':
                        modifier[m.type] = f'"{m.value_string}"'
                    if m.value_type == 'VECTOR':
                        modifier[m.type] = [round(m.value_vector.x, 3), round(m.value_vector.y, 3), round(m.value_vector.z, 3)]
                towrite = []
                for m in modifier:
                    if not m in currentdata:
                        currentdata[m] = modifier[m]
                        towrite.append([m, modifier[m]])
                    else:
                        if not currentdata[m] == modifier[m]:
                            currentdata[m] = modifier[m]
                            towrite.append([m, modifier[m]])
                idx = len(mods)
                if len(towrite) != 0:
                    mods[str(len(node_table))] = towrite
                    idx = len(mods)
                    try:
                        node_table[str(idx)].append([n.id1, n.id2, n.id3])
                    except KeyError:
                        node_table[str(idx)] = []
                        node_table[str(idx)].append([n.id1, n.id2, n.id3])
                else:
                    try:
                        node_table[str(idx-1)].append([n.id1, n.id2, n.id3])
                    except KeyError:
                        node_table[str(idx-1)] = []
                        node_table[str(idx-1)].append([n.id1, n.id2, n.id3])
            for i in range(len(node_table)):
                if str(i) in mods:
                    for mm in mods[str(i)]:
                        f.write('\t\t{"'+mm[0]+'":'+str(mm[1])+'},\n')
                for n in node_table[str(i)]:
                    f.write(f'\t\t["{n[0]}","{n[1]}","{n[2]}"],\n')
                
            f.write('\t],\n')


        f.write('},\n')
    f.write('}')