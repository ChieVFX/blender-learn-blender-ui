# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
# <pep8 compliant>

import bpy
import re

bl_info = {
    "name" : "LearnBlenderUI",
    "author" : "ChieVFX",
    "description" : "\
        Helps you find python name for the UI elements\
        via fragments of labels or python names.",
    "version": (0, 5),
    "blender" : (2, 80, 0),
    "location" : "",
    "warning" : "",
    "wiki_url": "https://github.com/p2or/blender-viewport-rename",
    "tracker_url": "https://github.com/p2or/blender-viewport-rename/issues",
    "category" : "Development"
}

def get_ui_classes():
    ui = []
    headers = []
    menus = []
    operators = []
    panels = []
    ui_lists = []
    for clsName in dir(bpy.types):
        cls = getattr(bpy.types, clsName)
        # print("{} :: {}".format(clsName, cls))
        id_name = clsName
        if "_HT_" in id_name:
            ui.append(ClassContainer(cls, clsName))
            headers.append(ClassContainer(cls, clsName))
        if "_MT_" in clsName:
            ui.append(ClassContainer(cls, clsName))
            menus.append(ClassContainer(cls, clsName))
        if "_OT_" in clsName:
            ui.append(ClassContainer(cls, clsName))
            operators.append(ClassContainer(cls, clsName))
        if "_PT_" in clsName:
            ui.append(ClassContainer(cls, clsName))
            panels.append(ClassContainer(cls, clsName))
        if "_UL" in clsName:
            ui.append(ClassContainer(cls, clsName))
            ui_lists.append(ClassContainer(cls, clsName))
    
    return ui, headers, menus, operators, panels, ui_lists

class ClassContainer:
    def __init__(self, cls, idname):
        self.cls = cls
        self.label = ""
        if hasattr(cls, "bl_label"):
            self.label = cls.bl_label
        self.idname = idname
        if hasattr(cls, "bl_idname"):
            self.idname = cls.bl_idname
        else:
            class_name : [] = str(cls).replace("<class '", "").replace("'>", "").split('.')
            self.idname = class_name[len(class_name)-1]

def _on_value_updated(prop : bpy.types.Property, context):
    # user_input:str = self.label_fragment
    # classes = OpGetIdByLabel._get_classes_by_label(user_input)
        # self.report({'ERROR'}, info)

    context.area.tag_redraw()
    # for a in context.screen.areas:
    #     a.tag_redraw()
    
class OpGetIdByLabel(bpy.types.Operator):
    bl_idname = "learn_blender_ui.by_label"
    bl_label = "Learn ID by Label fragment"
    bl_description = "\
        By typing in a part of the label's text\
        you will get a list of ids for the ui elements that match"
    bl_options = {'REGISTER'}

    @staticmethod
    def _get_classes_by_label(label_fragment:str):
        result = []
        ui, headers, menus, operators, panels, ui_lists = get_ui_classes()
        label_fragment = label_fragment.lower()
        for class_container in ui:
            if not label_fragment:
                result.append(class_container)
                continue
            
            if label_fragment in class_container.label.lower():
                result.append(class_container)
        
        # print (">>>")
        # for class_container in result:
        #     print("{}: {}".format(class_container.idname, class_container.label))
        # print ("<<<")

        return result


    label_fragment : bpy.props.StringProperty(
        name="Label fragment",
        description="Part of the label that the search will be matching against",
        subtype='NONE',
        update=_on_value_updated
        )

    def execute(self, context):
        user_input = self.label_fragment

        classes = self._get_classes_by_label(user_input)
        if not len(classes):
            self.report({'INFO'}, "No matches found!")
            return {'FINISHED'}

        info = ""
        for class_container in classes:
            info += class_container.idname + "\n"
            # self.report({'ERROR'}, info)
        
        self._matches = classes
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        # self.label_fragment = ""
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "label_fragment")

        user_input = self.label_fragment
        classes = OpGetIdByLabel._get_classes_by_label(user_input)

        if not user_input:
            return

        is_overflowing = True
        max_i = 21
        if max_i > len(classes):
            max_i = len(classes)
            is_overflowing = False
        for i in range(0, max_i):
            layout.label(text=classes[i].idname)
        if is_overflowing:
            layout.label(text="...")

# class OpGetIdById(bpy.types.Operator):
#     bl_idname = "learn_blender_ui.by_id"
#     bl_label = "Learn ID by ID fragment"
#     bl_description = "\
#         By typing in a part of the bl_idname\
#         you will get a list of ids for the ui elements that match"
#     bl_options = {'REGISTER'}
#     label_fragment : bpy.props.StringProperty()
    
#     @staticmethod
#     def _get_classes_by_label(label_fragment:str):
#         result = []
#         label_fragment = label_fragment.lower()
#         print (">>>")
#         for clsName in dir(bpy.types):
#             try:
#                 cls = getattr(bpy.types, clsName)
#                 label:str = getattr(cls, 'bl_label').lower()
#                 if label_fragment in label.lower():
#                     result.append(cls)
#                     print("{}: {}".format(tName, label))
#                 # print(t.bl_idname)
#             except:
#                 pass
#         print ("<<<")

#         return result

#     def execute(self, context):
#         user_input = self.label_fragment
#         reverse = False

#         classes = self._get_classes_by_label(user_input)
#         if not len(classes):
#             bpy.window_manager.report('Info', "No matches found!")
#             return {'FINISHED'}



#         suff = re.findall("#+$", user_input)
#         if user_input and suff:
#             number = ('%0'+str(len(suff[0]))+'d', len(suff[0]))
#             real_name = re.sub("#", '', user_input)           

#             objs = context.selected_objects[::-1] if reverse else context.selected_objects
#             names_before = [n.name for n in objs]
#             for c, o in enumerate(objs, start=1):
#                 o.name = (real_name + (number[0] % c))
#                 if self.data_flag and o.data is not None:
#                     o.data.name = (real_name + (number[0] % c))
#             self.report({'INFO'}, "Renamed {}".format(", ".join(names_before)))
#             return {'FINISHED'}

#         elif user_input:
#             old_name = context.active_object.name
#             context.active_object.name = user_input
#             if self.data_flag and context.active_object.data is not None:
#                 context.active_object.data.name = user_input
#             self.report({'INFO'}, "{} renamed to {}".format(old_name, user_input))
#             return {'FINISHED'}

#         else:
#             self.report({'INFO'}, "No input, operation cancelled")
#             return {'CANCELLED'}

#     def invoke(self, context, event):
#         wm = context.window_manager
#         self.label_fragment = ""
#         return wm.invoke_props_dialog(self)

#     def draw(self, context):
#         row = self.layout
#         row.prop(self, "type", text="New Name")
#         row.prop(self, "data_flag", text="Rename Data-Block")


# ------------------------------------------------------------------------
#    register and unregister functions
# ------------------------------------------------------------------------

classes = [
    OpGetIdByLabel,
]

addon_keymaps = []

def register():
    from bpy.utils import register_class

    addon_keymaps.clear()
    for cls in classes:
        register_class(cls)
    # bpy.utils.register_module(__name__)

    # # handle the keymap
    # wm = bpy.context.window_manager
    # kc = wm.keyconfigs.addon
    # if kc:
    #     km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    #     kmi = km.keymap_items.new(ViewportRenameOperator.bl_idname, type='R', value='PRESS', ctrl=True)
    #     addon_keymaps.append((km, kmi))

def unregister():
    from bpy.utils import unregister_class

    # for km, kmi in addon_keymaps:
    #     km.keymap_items.remove(kmi)
    # addon_keymaps.clear()

    for cls in classes:
        unregister_class(cls)
    # bpy.utils.unregister_module(__name__)

# if __name__ == "__main__":
#     register()