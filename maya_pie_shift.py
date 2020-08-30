import bpy
from bpy.types import Menu

# spawn an edit mode selection pie (run while object is in edit mode to get a valid output)
#https://blender.stackexchange.com/questions/45581/possible-to-combine-a-pie-operator-and-box-operator-together
bl_info = {
    "name": "Shade Menu: Key: 'L key'",
    "description": "View Modes",
    "author": "Pit Henrich",
    "version": (0, 1, 0),
    "blender": (2, 8, 0),
    "location": "L key",
    "warning": "",
    "wiki_url": "",
    "category": "3d View"
    }
    
class VIEW3D_MT_maya_shift(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Select Tool"

    def none(self, pie):
        pie.operator("transform.translate", text="", icon='PANEL_CLOSE')
    def knife(self, pie):
        pie.operator("mesh.knife_tool", text="Interactive Split Tool", icon='VERTEXSEL')
    def loop_cut(self, pie):
        pie.operator("mesh.loopcut_slide", text="Insert Edge Loop")
    def loop_cut_offset(self, pie):
        pie.operator("mesh.offset_edge_loops_slide", text="Offset Edge Loop")
    def extrude(self, pie):
        pie.operator("view3d.edit_mesh_extrude_move_normal", text="Extrude")
    def bevel(self, pie):
        pie.operator("mesh.bevel", text="Bevel")
    def collapse(self, pie):
        pie.operator("mesh.merge", text="Collapse").type='COLLAPSE'
    def delete_edge(self, pie):
        pie.operator("mesh.delete", text="Delete Edge").type='EDGE'
    def delete_vertex(self, pie):
        pie.operator("mesh.delete", text="Delete Vertex").type='VERT'
    def slide_edge(self, pie):
        pie.operator("transform.edge_slide", text="Slide Edge Tool")

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # operator_enum will just spread all available options
        # for the type enum of the operator on the pie
        #pie.operator_enum("mesh.select_mode", "type")
        #pie.operator('mesh.select_mode', "yaya",type="Edge")
        
        in_face_mode = tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True)
        in_edge_mode = tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, True, False)
        in_vertex_mode = tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False)
        if(bpy.context.object.mode == 'EDIT'):
            if in_face_mode:
                #LEFT
                #bpy.ops.mesh.knife_tool(use_occlude_geometry=True, only_selected=False)
                self.knife(pie)#LEFT
                self.none(pie) #RIGHT
                self.extrude(pie) #BOTTOM
                self.none(pie) #TOP
                self.none(pie) #TOP LEFT
                self.none(pie) #TOP RIGHT
                self.loop_cut(pie) #BOTTOM LEFT
                self.none(pie) #BOTTOM RIGHT
            
            if in_edge_mode:
                self.knife(pie)#LEFT
                self.bevel(pie) #RIGHT
                self.extrude(pie) #BOTTOM
                self.collapse(pie)#TOP
                self.none(pie) #TOP LEFT
                self.none(pie) #TOP RIGHT
                self.delete_edge(pie)#BOTTOM LEFT
                box = pie.box().column() #BOTTOM RIGHT
                self.slide_edge(box)
                self.loop_cut(box)
                self.loop_cut_offset(box)
            if in_vertex_mode:
                self.none(pie) #LEFT
                self.none(pie) #RIGHT
                self.none(pie) #BOTTOM
                self.collapse(pie) #TOP
                self.none(pie) #TOP LEFT
                self.none(pie) #TOP RIGHT
                self.delete_vertex(pie) #BOTTOM LEFT
                self.none(pie) #BOTTOM RIGHT

classes = (
    VIEW3D_MT_maya_shift,
)

addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        # Align
        km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'RIGHTMOUSE', 'PRESS', shift=True)
        kmi.properties.name = VIEW3D_MT_maya_shift.__name__
        addon_keymaps.append((km, kmi))

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
