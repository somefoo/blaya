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
    
class VIEW3D_MT_maya_ctrl(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Select Mode"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # operator_enum will just spread all available options
        # for the type enum of the operator on the pie
        #pie.operator_enum("mesh.select_mode", "type")
        #pie.operator('mesh.select_mode', "yaya",type="Edge")
        #LEFT
        pie.operator("mesh.select_mode", text="Vertex", icon='VERTEXSEL').type = 'VERT'
        
        #RIGHT
        pie.operator("transform.rotate", text="Rotate")
        
        #BOTTOM
        pie.operator("mesh.select_mode", text="Face", icon='FACESEL').type = 'FACE'
        
        #TOP
        pie.operator("mesh.select_mode", text="Edge", icon='EDGESEL').type = 'EDGE'
        
        #TOP LEFT
        pie.operator("transform.translate", text="Translate")
        
        #TOP RIGHT
        if(bpy.context.object.mode == 'OBJECT'):
            pie.operator("object.mode_set", text="Edit Mode").mode='EDIT'
        else:
            pie.operator("object.mode_set", text="Object Mode").mode='OBJECT'
        
        #BOTTOM LEFT
        pie.operator("mesh.loopcut_slide", text="Insert Edge Loop")
        
        
        #BOTTOM RIGHT
        pie.operator("transform.resize", text="Scale")


classes = (
    VIEW3D_MT_maya_ctrl,
)

addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        # Align
        km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'RIGHTMOUSE', 'PRESS', ctrl=True)
        kmi.properties.name = VIEW3D_MT_maya_ctrl.__name__
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

    bpy.ops.wm.call_menu_pie(name="VIEW3D_PIE_template")
