import bpy
import bmesh

class NODES_OT_actions(bpy.types.Operator):
    bl_idname = "nodes.list_action"
    bl_label = "List Actions"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", ""),
            ('SELECT', "Select", ""),
            ("EDIT", "Edit", "")))

    def invoke(self, context, event):
        current_jbeam = bpy.context.active_object.data.jbeam
        idx = current_jbeam.nodes_index

        try:
            item = current_jbeam.nodes[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(current_jbeam.nodes) - 1:
                item_next = current_jbeam.nodes[idx+1].name
                mode = bpy.context.object.mode
                bpy.ops.object.mode_set(mode = 'EDIT') 
                bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
                vert_index = list(range(len(bm.verts)))
                ch1 = vert_index[idx]
                ch2 = vert_index[idx+1]
                vert_index[idx] = ch2
                vert_index[idx+1] = ch1
                for i, v in zip(vert_index, bm.verts):
                    v.index = i
                bm.verts.sort()
                bpy.ops.object.mode_set(mode = 'OBJECT') 
                bpy.ops.object.mode_set(mode = mode) 
                current_jbeam.nodes.move(idx, idx+1)
                current_jbeam.nodes_index += 1

            elif self.action == 'UP' and idx >= 1:
                item_prev = current_jbeam.nodes[idx-1].name
                mode = bpy.context.object.mode
                bpy.ops.object.mode_set(mode = 'EDIT') 
                bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
                vert_index = list(range(len(bm.verts)))
                ch1 = vert_index[idx]
                ch2 = vert_index[idx-1]
                vert_index[idx] = ch2
                vert_index[idx-1] = ch1
                for i, v in zip(vert_index, bm.verts):
                    v.index = i
                bm.verts.sort()
                bpy.ops.object.mode_set(mode = 'OBJECT') 
                bpy.ops.object.mode_set(mode = mode) 
                current_jbeam.nodes.move(idx, idx-1)
                current_jbeam.nodes_index -= 1

            elif self.action == 'REMOVE':
                for i, beam in enumerate(current_jbeam.beams):
                    if beam.id1 == item.id or beam.id2 == item.id:
                        current_jbeam.beams_index -= 1
                        current_jbeam.beams.remove(i)
                for i, triangle in enumerate(current_jbeam.triangles):
                    if triangle.id1 == item.id or triangle.id2 == item.id or triangle.id3 == item.id:
                        current_jbeam.triangles_index -= 1
                        current_jbeam.triangles.remove(i)
                mode = bpy.context.object.mode
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.context.active_object.data.vertices[idx].select = True
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.delete(type='VERT')
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.mode_set(mode=mode)
                current_jbeam.nodes_index -= 1
                current_jbeam.nodes.remove(idx)

            elif self.action == 'SELECT':
                bpy.ops.object.mode_set(mode = 'EDIT') 
                bpy.ops.mesh.select_mode(type="VERT")
                bpy.ops.mesh.select_all(action = 'DESELECT')
                bpy.ops.object.mode_set(mode = 'OBJECT')
                bpy.context.active_object.data.vertices[idx].select = True 
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.context.scene.jbeam.node_id = item.id

                bpy.context.scene.jbeam.modifier_type = ""
                bpy.context.scene.jbeam.modifier_value_int = 0
                bpy.context.scene.jbeam.modifier_value_float = 0
                bpy.context.scene.jbeam.modifier_value_bool = True
                bpy.context.scene.jbeam.modifier_value_string = ""
                bpy.context.scene.jbeam.modifier_value_vector.x = 0
                bpy.context.scene.jbeam.modifier_value_vector.x = 0
                bpy.context.scene.jbeam.modifier_value_vector.x = 0

            elif self.action == 'EDIT':
                tochange = bpy.context.scene.jbeam.node_id
                for beam in current_jbeam.beams:
                    if beam.id1 == item.id:
                        beam.id1 = tochange
                    elif beam.id2 == item.id:
                        beam.id2 = tochange
                for triangle in current_jbeam.triangles:
                    if triangle.id1 == item.id:
                        triangle.id1 = tochange
                    elif triangle.id2 == item.id:
                        triangle.id2 = tochange
                    elif triangle.id3 == item.id:
                        triangle.id3 = tochange
                item.id = bpy.context.scene.jbeam.node_id

        return {"FINISHED"}

class NODEMODIFIER_UL_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=1)
        split.operator("nodemodifier.list_action", icon='RESTRICT_SELECT_OFF', text="").action = 'SELECT'
        split = layout.split(factor=0.3)
        split.label(text=item.type)

        split.label(text=item.value_type)
        if item.value_type == 'INTEGER':
            split.label(text=str(item.value_int))
        if item.value_type == 'FLOAT':
            split.label(text=str(round(item.value_float, 2)))
        if item.value_type == 'BOOL':
            split.label(text=str(item.value_bool))
        if item.value_type == 'STRING':
            split.label(text=item.value_string)
        if item.value_type == 'VECTOR':
            split.label(text=f"{str(round(item.value_vector.x, 2))} {str(round(item.value_vector.y, 2))} {str(round(item.value_vector.z, 2))}")

    def invoke(self, context, event):
        pass   

class NODESMODIFIER_OT_actions(bpy.types.Operator):
    bl_idname = "nodemodifier.list_action"
    bl_label = "List Actions"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", ""),
            ('SELECT', "Select", ""),
            ("EDIT", "Edit", "")))

    def invoke(self, context, event):
        current_slot = bpy.context.active_object.data.jbeam.nodes[bpy.context.active_object.data.jbeam.nodes_index]
        idx = current_slot.modifier_index

        try:
            item = current_slot.modifier[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(current_slot.modifier) - 1:
                item_next = current_slot.modifier[idx+1].name
                current_slot.modifier.move(idx, idx+1)
                current_slot.modifier_index += 1

            elif self.action == 'UP' and idx >= 1:
                item_prev = current_slot.modifier[idx-1].name
                current_slot.modifier.move(idx, idx-1)
                current_slot.modifier_index -= 1

            elif self.action == 'REMOVE':
                current_slot.modifier_index -= 1
                current_slot.modifier.remove(idx)

            elif self.action == 'SELECT':
                bpy.context.scene.jbeam.modifier_type = item.type
                bpy.context.scene.jbeam.modifier_value_type = item.value_type
                if item.value_type == 'INTEGER':
                    bpy.context.scene.jbeam.modifier_value_int = item.value_int
                if item.value_type == 'FLOAT':
                    bpy.context.scene.jbeam.modifier_value_float = item.value_float
                if item.value_type == 'BOOL':
                    bpy.context.scene.jbeam.modifier_value_bool = item.value_bool
                if item.value_type == 'STRING':
                    bpy.context.scene.jbeam.modifier_value_string = item.value_string
                if item.value_type == 'VECTOR':
                    bpy.context.scene.jbeam.modifier_value_vector.x = item.value_vector.x
                    bpy.context.scene.jbeam.modifier_value_vector.y = item.value_vector.y
                    bpy.context.scene.jbeam.modifier_value_vector.z = item.value_vector.z

            elif self.action == 'EDIT':
                item.type = bpy.context.scene.jbeam.modifier_type
                item.value_type = bpy.context.scene.jbeam.modifier_value_type
                if item.value_type == 'INTEGER':
                    item.value_int = bpy.context.scene.jbeam.modifier_value_int
                if item.value_type == 'FLOAT':
                    item.value_float = bpy.context.scene.jbeam.modifier_value_float
                if item.value_type == 'BOOL':
                    item.value_bool = bpy.context.scene.jbeam.modifier_value_bool
                if item.value_type == 'STRING':
                    item.value_string = bpy.context.scene.jbeam.modifier_value_string
                if item.value_type == 'VECTOR':
                    item.value_vector.x = bpy.context.scene.jbeam.modifier_value_vector.x
                    item.value_vector.y = bpy.context.scene.jbeam.modifier_value_vector.y
                    item.value_vector.z = bpy.context.scene.jbeam.modifier_value_vector.z

        if self.action == 'ADD':
            item = current_slot.modifier.add()
            item.type = bpy.context.scene.jbeam.modifier_type
            item.value_type = bpy.context.scene.jbeam.modifier_value_type
            if item.value_type == 'INTEGER':
                item.value_int = bpy.context.scene.jbeam.modifier_value_int
            if item.value_type == 'FLOAT':
                item.value_float = bpy.context.scene.jbeam.modifier_value_float
            if item.value_type == 'BOOL':
                item.value_bool = bpy.context.scene.jbeam.modifier_value_bool
            if item.value_type == 'STRING':
                item.value_string = bpy.context.scene.jbeam.modifier_value_string
            if item.value_type == 'VECTOR':
                item.value_vector.x = bpy.context.scene.jbeam.modifier_value_vector.x
                item.value_vector.y = bpy.context.scene.jbeam.modifier_value_vector.y
                item.value_vector.z = bpy.context.scene.jbeam.modifier_value_vector.z
            current_slot.modifier_index = len(current_slot.modifier)-1
        return {"FINISHED"}

class NODES_UL_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=1)
        split.operator("nodes.list_action", icon='RESTRICT_SELECT_OFF', text="").action = 'SELECT'
        split = layout.split(factor=0.3)

        split.label(text=item.id)
        # custom_icon = "OUTLINER_OB_%s" % item.obj_type
        #split.prop(item, "name", text="", emboss=False, translate=False, icon=custom_icon)
        # split.label(text=item.name, icon=custom_icon)

    def invoke(self, context, event):
        pass  

class PANEL_PT_JBeamNodesPanel(bpy.types.Panel):
    bl_label = "Nodes"
    bl_parent_id = "PANEL_PT_JBeamPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.prop(bpy.context.active_object.data.jbeam, "export_nodes", text="")

    def draw(self, context):
        if not bpy.context.active_object.data.jbeam.export_nodes:
            self.layout.active = False
        else:
            self.layout.use_property_split = True
            self.layout.use_property_decorate = False
            row = self.layout.row()
            row.template_list("NODES_UL_items", "", bpy.context.active_object.data.jbeam, "nodes", bpy.context.active_object.data.jbeam, "nodes_index", rows=2)
            column = row.column(align=True)
            column.operator("nodes.list_action", icon='TRASH', text="").action = 'REMOVE'
            column.separator()
            column.operator("nodes.list_action", icon='TRIA_UP', text="").action = 'UP'
            column.operator("nodes.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
            column = self.layout.column_flow().column()
            column.prop(bpy.context.scene.jbeam, "node_id")
            row = self.layout.row()
            row.operator("nodes.list_action", icon='MODIFIER', text="Edit").action = 'EDIT'

class  PANEL_PT_JBeamNodesModifierPanel(bpy.types.Panel):
    bl_label = "Modifier"
    bl_parent_id = "PANEL_PT_JBeamNodesPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    def draw(self, context):
        row = self.layout.row()
        node = bpy.context.active_object.data.jbeam.nodes[bpy.context.active_object.data.jbeam.nodes_index]
        row.template_list("NODEMODIFIER_UL_items", "", node, "modifier", node, "modifier_index", rows=2)
        column = row.column(align=True)
        column.operator("nodemodifier.list_action", icon='TRASH', text="").action = 'REMOVE'
        column.separator()
        column.operator("nodemodifier.list_action", icon='TRIA_UP', text="").action = 'UP'
        column.operator("nodemodifier.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
        column = self.layout.column_flow().column()
        column.prop(bpy.context.scene.jbeam, "modifier_type")
        column.prop(bpy.context.scene.jbeam, "modifier_value_type")
        if bpy.context.scene.jbeam.modifier_value_type == 'INTEGER':
            column.prop(bpy.context.scene.jbeam, "modifier_value_int")
        if bpy.context.scene.jbeam.modifier_value_type == 'FLOAT':
            column.prop(bpy.context.scene.jbeam, "modifier_value_float")
        if bpy.context.scene.jbeam.modifier_value_type == 'BOOL':
            column.prop(bpy.context.scene.jbeam, "modifier_value_bool")
        if bpy.context.scene.jbeam.modifier_value_type == 'STRING':
            column.prop(bpy.context.scene.jbeam, "modifier_value_string")
        if bpy.context.scene.jbeam.modifier_value_type == 'VECTOR':
            column.prop(bpy.context.scene.jbeam.modifier_value_vector, "x")
            column.prop(bpy.context.scene.jbeam.modifier_value_vector, "y")
            column.prop(bpy.context.scene.jbeam.modifier_value_vector, "z")
        row = self.layout.row()
        row.operator("nodemodifier.list_action", icon='FILE_NEW', text="Add").action = 'ADD'
        row.operator("nodemodifier.list_action", icon='MODIFIER', text="Edit").action = 'EDIT'
