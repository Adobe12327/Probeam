import bpy

class SLOTS_UL_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.5)
        split.operator("slots.list_action", icon='RESTRICT_SELECT_OFF', text="").action = 'SELECT'
        split = layout.split(factor=0.3)
        split.label(text=item.type)

        split.label(text=item.default)

        split.label(text=item.description)

    def invoke(self, context, event):
        pass   

class SLOTMODIFIER_UL_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.5)
        split.operator("slotmodifier.list_action", icon='RESTRICT_SELECT_OFF', text="").action = 'SELECT'
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

class SLOTSMODIFIER_OT_actions(bpy.types.Operator):
    bl_idname = "slotmodifier.list_action"
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
        current_slot = bpy.context.active_object.data.jbeam.slots[bpy.context.active_object.data.jbeam.slots_index]
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

class SLOTS_OT_actions(bpy.types.Operator):
    bl_idname = "slots.list_action"
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
        idx = current_jbeam.slots_index

        try:
            item = current_jbeam.slots[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(current_jbeam.slots) - 1:
                item_next = current_jbeam.slots[idx+1].name
                current_jbeam.slots.move(idx, idx+1)
                current_jbeam.slots_index += 1

            elif self.action == 'UP' and idx >= 1:
                item_prev = current_jbeam.slots[idx-1].name
                current_jbeam.slots.move(idx, idx-1)
                current_jbeam.slots_index -= 1

            elif self.action == 'REMOVE':
                current_jbeam.slots_index -= 1
                current_jbeam.slots.remove(idx)

            elif self.action == 'SELECT':
                bpy.context.scene.jbeam.slots_type = item.type
                bpy.context.scene.jbeam.slots_default = item.default
                bpy.context.scene.jbeam.slots_description = item.description

                bpy.context.scene.jbeam.modifier_type = ""
                bpy.context.scene.jbeam.modifier_value_int = 0
                bpy.context.scene.jbeam.modifier_value_float = 0
                bpy.context.scene.jbeam.modifier_value_bool = True
                bpy.context.scene.jbeam.modifier_value_string = ""
                bpy.context.scene.jbeam.modifier_value_vector.x = 0
                bpy.context.scene.jbeam.modifier_value_vector.x = 0
                bpy.context.scene.jbeam.modifier_value_vector.x = 0

            elif self.action == 'EDIT':
                item.type = bpy.context.scene.jbeam.slots_type
                item.default = bpy.context.scene.jbeam.slots_default
                item.description = bpy.context.scene.jbeam.slots_description

        if self.action == 'ADD':
            item = current_jbeam.slots.add()
            item.type = bpy.context.scene.jbeam.slots_type
            item.default = bpy.context.scene.jbeam.slots_default
            item.description = bpy.context.scene.jbeam.slots_description
            current_jbeam.slots_index = len(current_jbeam.slots)-1
        return {"FINISHED"}

class  PANEL_PT_JBeamSlotTypePanel(bpy.types.Panel):
    bl_label = "Slot Type"
    bl_parent_id = "PANEL_PT_JBeamPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    def draw(self, context):
        self.layout.use_property_split = True
        self.layout.use_property_decorate = False
        flow = self.layout.column_flow()
        column = flow.column()
        column.prop(bpy.context.active_object.data.jbeam, "slot_type")


class  PANEL_PT_JBeamSlotPanel(bpy.types.Panel):
    bl_label = "Slots"
    bl_parent_id = "PANEL_PT_JBeamSlotTypePanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.prop(bpy.context.active_object.data.jbeam, "export_slots", text="")

    def draw(self, context):
        if not bpy.context.active_object.data.jbeam.export_slots:
            self.layout.active = False
        else:
            self.layout.use_property_split = True
            self.layout.use_property_decorate = False
            row = self.layout.row()
            row.template_list("SLOTS_UL_items", "", bpy.context.active_object.data.jbeam, "slots", bpy.context.active_object.data.jbeam, "slots_index", rows=2)
            column = row.column(align=True)
            column.operator("slots.list_action", icon='TRASH', text="").action = 'REMOVE'
            column.separator()
            column.operator("slots.list_action", icon='TRIA_UP', text="").action = 'UP'
            column.operator("slots.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
            column = self.layout.column_flow().column()
            column.prop(bpy.context.scene.jbeam, "slots_type")
            column.prop(bpy.context.scene.jbeam, "slots_default")
            column.prop(bpy.context.scene.jbeam, "slots_description")
            row = self.layout.row()
            row.operator("slots.list_action", icon='FILE_NEW', text="Add").action = 'ADD'
            row.operator("slots.list_action", icon='MODIFIER', text="Edit").action = 'EDIT'

class  PANEL_PT_JBeamSlotModifierPanel(bpy.types.Panel):
    bl_label = "Modifier"
    bl_parent_id = "PANEL_PT_JBeamSlotPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    def draw(self, context):
        row = self.layout.row()
        slot = bpy.context.active_object.data.jbeam.slots[bpy.context.active_object.data.jbeam.slots_index]
        row.template_list("SLOTMODIFIER_UL_items", "", slot, "modifier", slot, "modifier_index", rows=2)
        column = row.column(align=True)
        column.operator("slotmodifier.list_action", icon='TRASH', text="").action = 'REMOVE'
        column.separator()
        column.operator("slotmodifier.list_action", icon='TRIA_UP', text="").action = 'UP'
        column.operator("slotmodifier.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
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
        row.operator("slotmodifier.list_action", icon='FILE_NEW', text="Add").action = 'ADD'
        row.operator("slotmodifier.list_action", icon='MODIFIER', text="Edit").action = 'EDIT'