import bpy

class  PANEL_PT_JBeamInformationPanel(bpy.types.Panel):
    bl_label = "Information"
    bl_parent_id = "PANEL_PT_JBeamPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    def draw_header(self, context):
        self.layout.prop(bpy.context.active_object.data.jbeam, "export_information", text="")

    def draw(self, context):
        if not bpy.context.active_object.data.jbeam.export_information:
            self.layout.active = False
        else:
            self.layout.use_property_split = True
            self.layout.use_property_decorate = False
            flow = self.layout.column_flow()
            column = flow.column()
            column.prop(bpy.context.active_object.data.jbeam, "authors")
            column.prop(bpy.context.active_object.data.jbeam, "name")
            row = column.row()
            row.prop(bpy.context.active_object.data.jbeam, "export_information_value", text="")
            row.prop(bpy.context.active_object.data.jbeam, "value")