import bpy

def FindNodeIndexById(id):
    for i, n in enumerate(bpy.context.active_object.data.jbeam.nodes):
        if n.id == id:
            return i

class Beams_OT_actions(bpy.types.Operator):
    bl_idname = "beams.list_action"
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
        idx = current_jbeam.beams_index

        try:
            item = current_jbeam.beams[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(current_jbeam.beams) - 1:
                item_next = current_jbeam.beams[idx+1].name
                current_jbeam.beams.move(idx, idx+1)
                current_jbeam.beams_index += 1

            elif self.action == 'UP' and idx >= 1:
                item_prev = current_jbeam.beams[idx-1].name
                current_jbeam.beams.move(idx, idx-1)
                current_jbeam.beams_index -= 1

            elif self.action == 'REMOVE':
                try:
                    mode = bpy.context.object.mode
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_mode(type="VERT")
                    bpy.ops.mesh.select_all(action='DESELECT')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.context.active_object.data.vertices[FindNodeIndexById(item.id1)].select = True 
                    bpy.context.active_object.data.vertices[FindNodeIndexById(item.id2)].select = True 
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.delete(type='EDGE')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.mode_set(mode=mode)
                    current_jbeam.beams_index -= 1
                    current_jbeam.beams.remove(idx)
                except TypeError:
                        self.report({'ERROR'}, "One node is in other mesh!")

            elif self.action == 'SELECT':
                try:
                    bpy.ops.object.mode_set(mode = 'EDIT') 
                    bpy.ops.mesh.select_mode(type="VERT")
                    bpy.ops.mesh.select_all(action = 'DESELECT')
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    bpy.context.active_object.data.vertices[FindNodeIndexById(item.id1)].select = True 
                    bpy.context.active_object.data.vertices[FindNodeIndexById(item.id2)].select = True 
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.select_mode(type="EDGE")
                except TypeError:
                    self.report({'ERROR'}, "One node is in other mesh!")

                bpy.context.scene.jbeam.modifier_type = ""
                bpy.context.scene.jbeam.modifier_value_int = 0
                bpy.context.scene.jbeam.modifier_value_float = 0
                bpy.context.scene.jbeam.modifier_value_bool = True
                bpy.context.scene.jbeam.modifier_value_string = ""
                bpy.context.scene.jbeam.modifier_value_vector.x = 0
                bpy.context.scene.jbeam.modifier_value_vector.x = 0
                bpy.context.scene.jbeam.modifier_value_vector.x = 0

            elif self.action == 'EDIT':
                item.type = bpy.context.scene.jbeam.beams_type
                item.default = bpy.context.scene.jbeam.beams_default
                item.description = bpy.context.scene.jbeam.beams_description

        if self.action == 'ADD':
            item = current_jbeam.beams.add()
            item.type = bpy.context.scene.jbeam.beams_type
            item.default = bpy.context.scene.jbeam.beams_default
            item.description = bpy.context.scene.jbeam.beams_description
            current_jbeam.beams_index = len(current_jbeam.beams)-1
        return {"FINISHED"}

class BEAMMODIFIER_UL_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=1)
        split.operator("beammodifier.list_action", icon='RESTRICT_SELECT_OFF', text="").action = 'SELECT'
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

class BEAMSMODIFIER_OT_actions(bpy.types.Operator):
    bl_idname = "beammodifier.list_action"
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
        current_slot = bpy.context.active_object.data.jbeam.beams[bpy.context.active_object.data.jbeam.beams_index]
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

class BEAMS_UL_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=1)
        split.operator("beams.list_action", icon='RESTRICT_SELECT_OFF', text="").action = 'SELECT'
        split = layout.split(factor=0.3)

        split.label(text=item.id1)
        split.label(text=item.id2)

    def invoke(self, context, event):
        pass  

class PANEL_PT_JBeamBeamsPanel(bpy.types.Panel):
    bl_label = "Beams"
    bl_parent_id = "PANEL_PT_JBeamPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.prop(bpy.context.active_object.data.jbeam, "export_beams", text="")

    def draw(self, context):
        if not bpy.context.active_object.data.jbeam.export_beams:
            self.layout.active = False
        else:
            self.layout.use_property_split = True
            self.layout.use_property_decorate = False
            row = self.layout.row()
            row.template_list("BEAMS_UL_items", "", bpy.context.active_object.data.jbeam, "beams", bpy.context.active_object.data.jbeam, "beams_index", rows=2)
            col = row.column(align=True)
            col.operator("beams.list_action", icon='TRASH', text="").action = 'REMOVE'
            col.separator()
            col.operator("beams.list_action", icon='TRIA_UP', text="").action = 'UP'
            col.operator("beams.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
            # column = self.layout.column_flow().column()
            # beammesh = bpy.context.active_object.data.vertices[bpy.context.active_object.data.jbeam.beams_index]
            # beam = bpy.context.active_object.data.jbeam.beams[bpy.context.active_object.data.jbeam.beams_index]

class  PANEL_PT_JBeamBeamsModifierPanel(bpy.types.Panel):
    bl_label = "Modifier"
    bl_parent_id = "PANEL_PT_JBeamBeamsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    def draw(self, context):
        row = self.layout.row()
        beam = bpy.context.active_object.data.jbeam.beams[bpy.context.active_object.data.jbeam.beams_index]
        row.template_list("BEAMMODIFIER_UL_items", "", beam, "modifier", beam, "modifier_index", rows=2)
        col = row.column(align=True)
        col.operator("beammodifier.list_action", icon='TRASH', text="").action = 'REMOVE'
        col.separator()
        col.operator("beammodifier.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("beammodifier.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
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
        row.operator("beammodifier.list_action", icon='FILE_NEW', text="Add").action = 'ADD'
        row.operator("beammodifier.list_action", icon='MODIFIER', text="Edit").action = 'EDIT'