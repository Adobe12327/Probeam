import bpy

class FLEXBODIES_UL_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.5)
        split.operator("flexbodies.list_action", icon='RESTRICT_SELECT_OFF', text="").action = 'SELECT'
        split = layout.split(factor=0.3)
        split.label(text=item.mesh)


    def invoke(self, context, event):
        pass   

class FlexBodyGroup_Select(bpy.types.Operator):
    bl_idname = "flexbodygroup.select"
    bl_label = "List Actions"
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        current_jbeam = bpy.context.active_object.data.jbeam
        current_flexbody = current_jbeam.flexbodies[current_jbeam.flexbodies_index]
        item = current_flexbody.group[current_flexbody.group_index]
        bpy.context.scene.jbeam.flexbody_group_data = item.data

        return {"FINISHED"}

class FlexBodyGroup_Add(bpy.types.Operator):
    bl_idname = "flexbodygroup.select"
    bl_label = "List Actions"
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        current_jbeam = bpy.context.active_object.data.jbeam
        current_flexbody = current_jbeam.flexbodies[current_jbeam.flexbodies_index]
        item = current_flexbody.group[current_flexbody.group_index]
        bpy.context.scene.jbeam.flexbody_group_data = item.data

        return {"FINISHED"}

class FLEXBODYGROUP_UL_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.5)
        split.operator("flexbodygroup.list_action", icon='RESTRICT_SELECT_OFF', text="").action = 'SELECT'
        split = layout.split(factor=0.3)
        split.label(text=item.data)


    def invoke(self, context, event):
        pass   

class FLEXBODYGROUP_OT_actions(bpy.types.Operator):
    bl_idname = "flexbodygroup.list_action"
    bl_label = "List Actions"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", ""),
            ('SELECT', "Select", "")))

    def invoke(self, context, event):
        current_flexbodies = bpy.context.active_object.data.jbeam.flexbodies[bpy.context.active_object.data.jbeam.flexbodies_index]
        idx = current_flexbodies.group_index
        if self.action == 'SELECT':
            current_jbeam = bpy.context.active_object.data.jbeam
            current_flexbody = current_jbeam.flexbodies[current_jbeam.flexbodies_index]
            item = current_flexbody.group[current_flexbody.group_index]
            bpy.context.scene.jbeam.flexbody_group_data = item.data
        if self.action == 'ADD':
            item = current_flexbodies.group.add()
            item.data = bpy.context.scene.jbeam.flexbody_group_data
        elif self.action == 'REMOVE':
            current_flexbodies.group_index -= 1
            current_flexbodies.group.remove(idx)
        return {"FINISHED"}

class FLEXBODIESMODIFIER_UL_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=1)
        split.operator("flexbodiesmodifier.list_action", icon='RESTRICT_SELECT_OFF', text="").action = 'SELECT'
        split = layout.split()
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

class FLEXBODIESMODIFIER_OT_actions(bpy.types.Operator):
    bl_idname = "flexbodiesmodifier.list_action"
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
        current_flexbodies = bpy.context.active_object.data.jbeam.flexbodies[bpy.context.active_object.data.jbeam.flexbodies_index]
        idx = current_flexbodies.modifier_index

        try:
            item = current_flexbodies.modifier[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(current_flexbodies.modifier) - 1:
                item_next = current_flexbodies.modifier[idx+1].name
                current_flexbodies.modifier.move(idx, idx+1)
                current_flexbodies.modifier_index += 1

            elif self.action == 'UP' and idx >= 1:
                item_prev = current_flexbodies.modifier[idx-1].name
                current_flexbodies.modifier.move(idx, idx-1)
                current_flexbodies.modifier_index -= 1

            elif self.action == 'REMOVE':
                current_flexbodies.modifier_index -= 1
                current_flexbodies.modifier.remove(idx)

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
            item = current_flexbodies.modifier.add()
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
            current_flexbodies.modifier_index = len(current_flexbodies.modifier)-1
        return {"FINISHED"}

class Flexbodies_OT_actions(bpy.types.Operator):
    bl_idname = "flexbodies.list_action"
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
        idx = current_jbeam.flexbodies_index

        try:
            item = current_jbeam.flexbodies[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(current_jbeam.flexbodies) - 1:
                item_next = current_jbeam.flexbodies[idx+1].name
                current_jbeam.flexbodies.move(idx, idx+1)
                current_jbeam.flexbodies_index += 1

            elif self.action == 'UP' and idx >= 1:
                item_prev = current_jbeam.flexbodies[idx-1].name
                current_jbeam.flexbodies.move(idx, idx-1)
                current_jbeam.flexbodies_index -= 1

            elif self.action == 'REMOVE':
                current_jbeam.flexbodies_index -= 1
                current_jbeam.flexbodies.remove(idx)

            elif self.action == 'SELECT':
                bpy.context.scene.jbeam.flexbodies_mesh = item.mesh

            elif self.action == 'EDIT':
                item.mesh = bpy.context.scene.jbeam.flexbodies_mesh

        if self.action == 'ADD':
            item = current_jbeam.flexbodies.add()
            item.type = bpy.context.scene.jbeam.flexbodies_type
            item.default = bpy.context.scene.jbeam.flexbodies_default
            item.description = bpy.context.scene.jbeam.flexbodies_description
            current_jbeam.flexbodies_index = len(current_jbeam.flexbodies)-1
        return {"FINISHED"}

class  PANEL_PT_JBeamFlexbodiesPanel(bpy.types.Panel):
    bl_label = "Flexbodies"
    bl_space_type = "PROPERTIES"
    bl_parent_id = "PANEL_PT_JBeamPanel"
    bl_region_type = "WINDOW"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.prop(bpy.context.active_object.data.jbeam, "export_flexbodies", text="")

    def draw(self, context):
        if not bpy.context.active_object.data.jbeam.export_flexbodies:
            self.layout.active = False
        else:
            current_jbeam = bpy.context.active_object.data.jbeam
            self.layout.use_property_split = True
            self.layout.use_property_decorate = False
            row = self.layout.row()
            row.template_list("FLEXBODIES_UL_items", "", current_jbeam, "flexbodies", current_jbeam, "flexbodies_index", rows=2)
            column = row.column(align=True)
            column.operator("flexbodies.list_action", icon='TRASH', text="").action = 'REMOVE'
            column.separator()
            column.operator("flexbodies.list_action", icon='TRIA_UP', text="").action = 'UP'
            column.operator("flexbodies.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
            column = self.layout.column_flow().column()
            column.prop(bpy.context.scene.jbeam, "flexbodies_mesh")
            row = self.layout.row()
            row.operator("flexbodies.list_action", icon='FILE_NEW', text="Add").action = 'ADD'
            row.operator("flexbodies.list_action", icon='MODIFIER', text="Edit").action = 'EDIT'

class  PANEL_PT_JBeamFlexbodiesGroupPanel(bpy.types.Panel):
    bl_label = "Group"
    bl_parent_id = "PANEL_PT_JBeamFlexbodiesPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    def draw(self, context):
        current_jbeam = bpy.context.active_object.data.jbeam
        flexbody = current_jbeam.flexbodies[current_jbeam.flexbodies_index]
        row = self.layout.row()
        row.template_list("FLEXBODYGROUP_UL_items", "", flexbody, "group", flexbody, "group_index", rows=2)
        column = row.column(align=True)
        column.operator("flexbodygroup.list_action", icon='TRASH', text="").action = 'REMOVE'
        column = self.layout.column_flow().column()
        column.prop(bpy.context.scene.jbeam, "flexbody_group_data")
        row = self.layout.row()
        row.operator("flexbodygroup.list_action", icon='FILE_NEW', text="Add").action = 'ADD'

class  PANEL_PT_JBeamFlexbodiesModifierPanel(bpy.types.Panel):
    bl_label = "Modifier"
    bl_parent_id = "PANEL_PT_JBeamFlexbodiesPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    def draw(self, context):
        row = self.layout.row()
        flexbodies = bpy.context.active_object.data.jbeam.flexbodies[bpy.context.active_object.data.jbeam.flexbodies_index]
        row.template_list("FLEXBODIESMODIFIER_UL_items", "", flexbodies, "modifier", flexbodies, "modifier_index", rows=2)
        column = row.column(align=True)
        column.operator("flexbodiesmodifier.list_action", icon='TRASH', text="").action = 'REMOVE'
        column.separator()
        column.operator("flexbodiesmodifier.list_action", icon='TRIA_UP', text="").action = 'UP'
        column.operator("flexbodiesmodifier.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
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
        row.operator("flexbodiesmodifier.list_action", icon='FILE_NEW', text="Add").action = 'ADD'
        row.operator("flexbodiesmodifier.list_action", icon='MODIFIER', text="Edit").action = 'EDIT'