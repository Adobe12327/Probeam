import bpy
import blf
import mathutils

class ShowNodeID(bpy.types.Operator):
    """Shows Node ID"""
    bl_idname = "jbeam.show_node_id"
    bl_label = "Show Node ID's"

    _handle = None
    
    @classmethod
    def poll(cls, context):
        return context.mode=="EDIT_MESH"
    
    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        # removal of callbacks when operator is called again

        if context.scene.show_node_id == -1:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            context.scene.show_node_id = 0
            return {"CANCELLED"}
        
        return {"PASS_THROUGH"}
    
    def invoke(self, context, event):
        if context.area.type == "VIEW_3D":
            if context.scene.show_node_id < 1:
                # operator is called for the first time, start everything

                context.scene.show_node_id = 1
                self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px,
                    (self, context), 'WINDOW', 'POST_PIXEL')
                context.window_manager.modal_handler_add(self)
                return {"RUNNING_MODAL"}
            else:
                # operator is called again, stop displaying

                context.scene.show_node_id = -1
                return {'RUNNING_MODAL'}
        else:
            self.report({"WARNING"}, "View3D not found, can't run operator")
            return {"CANCELLED"}

def draw_callback_px(self, context):
    # polling

    region = context.region
    mid_x = region.width / 2
    mid_y = region.height / 2
    width = region.width
    height = region.height

    # get matrices

    view_mat = context.space_data.region_3d.perspective_matrix
    ob_mat = context.active_object.matrix_world
    total_mat = view_mat @ ob_mat

    blf.size(0, 13, 72)

    def draw_index(r, g, b, index, center):

        vec = total_mat @ center # order is important

        vec = mathutils.Vector((vec[0] / vec[3], vec[1] / vec[3], vec[2] / vec[3]))
        x = int(mid_x + vec[0] * width / 2)
        y = int(mid_y + vec[1] * height / 2)

        blf.color(0,1,1,1,1)
        blf.position(0, x, y, 0)
        if isinstance(index,float):
            blf.draw(0, '{:.2f}'.format(index))
        else:
            blf.draw(0, str(index))

    me = context.active_object.data

    me.update()

    for v in me.vertices:
        try:
            draw_index(1.0, 1.0, 1.0, me.jbeam.nodes[v.index].id, v.co.to_4d())
        except Exception as e:
            continue