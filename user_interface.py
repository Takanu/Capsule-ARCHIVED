from .operators import GT_Blank_Report, GT_Name_Report, GT_Update_Origin, GT_Assign_Base, GT_Remove_From_Base, GT_Select_Parent, GT_Select_Base, GT_Create_New_Asset, GT_Add_Components, GT_Find_Components, GT_Delete_Base, GT_Remove_Components, GT_Duplicate_Base, GT_Merge_Base, GT_Seperate_Object, GT_Duplicate_Group, GT_Freeze, GT_Multi_Freeze, GT_Unfreeze, GT_Create_Group, GT_Remove_From_Group, GT_Move_Dummy, GT_Create_Low_Poly_Base, GT_Create_Low_Poly_Component, GT_Create_Collision, GT_Create_Cage, GT_Group_Create_Collision, GT_Group_Create_Cage, GT_Check_Mesh, GT_Export_Assets

from .definitions import GenerateVisibilityList, ClearVisibilityList, GenerateComponentList, ClearComponentList, GenerateFreezeList

import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty
from bpy.types import Menu, Panel, AddonPreferences, PropertyGroup
from rna_prop_ui import PropertyPanel

class UI_Freeze_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
                
        tempText = "Base"
        
        if int(item.type) is 2:
            tempText = "Base + Comp"
        elif int(item.type) is 3:
            tempText = "Merge"
            
        tempView = "VISIBLE_IPO_OFF"
        
        if item.view is True:
            tempView = "VISIBLE_IPO_ON"
                
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            
            layout.prop(item, "name", text="", emboss=False)
            layout.label(tempText)
            layout.prop(item, "view", text="", icon=tempView, emboss=False)
            layout.prop(item, "delete", text="", icon="X", emboss=False)
            layout.separator()
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)
            
        
class UI_Visibility_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
            
        tempIcon = ""
            
        if item.nameIcon is 1:
            tempIcon = "OUTLINER_OB_MESH"
        elif item.nameIcon is 3:
            tempIcon = "PMARKER_ACT"
        else:
            tempIcon = "RETOPO"
            
        tempName = "OBJECT_DATA"
            
        if int(item.type) is 2:
            tempName = "SOLID"
        elif int(item.type) is 3:
            tempName = "GRID"
        elif int(item.type) is 4:
            tempName = "LATTICE_DATA"
        elif int(item.type) is 5:
            tempName = "WIRE"
        elif int(item.type) is 6:
            tempName = "X"
                
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            
            layout.prop(item, "name", text="", icon=tempIcon, emboss=False)
            layout.prop(item, "type", text="", icon=tempName)
            layout.separator()
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)
            
class UI_Component_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        
        tempName = "SOLID"
        
        if int(item.type) is 2:
            tempName = "GRID"
        elif int(item.type) is 3:
            tempName = "LATTICE_DATA"
        elif int(item.type) is 4:
            tempName = "WIRE"
        elif int(item.type) is 5:
            tempName = "X"
                
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            
            layout.prop(item, "name", text="", emboss=False)
            layout.prop(item, "type", text="", icon=tempName)
            layout.separator()
            
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


#//////////////////////// - USER INTERFACE - ////////////////////////

#Generates the UI panel inside the 3D view
class GT_Tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Global Tools"
    bl_category = "Capsule"
    
    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return True
                
        return False

    def draw(self, context):
        layout = self.layout
        
        scn = context.scene.GTScn
        ob = context.object.GTObj
        mnu = context.object.GTMnu
        smn = context.scene.GTSmn
        
        obj = context.object

        col_engine = layout.row(align=True)
        col_engine.alignment = 'EXPAND'
        row_engine = col_engine.row(align=True)
        row_engine.alignment = 'EXPAND'
        row_engine.prop(scn, "engine_select", text="", icon = "LOGIC")
        
        #layout.separator()
        
        layout.prop(smn, "scene_visibility_toggle")
        
        if smn.scene_visibility_toggle is True:
            
            layout.separator()
            
            layout.template_list("UI_Visibility_List", "default", smn, "visibility_collection", smn, "visibility_collection_index", rows=3, maxrows=6)
        # ARGUMENTS >>>>>>>> CLASS NAME >> LIST ID (n/a) >> dataptr >>>>>>>>> propname >>>>> active_dataptr >>>>>   
        
        #layout.separator()
        #layout.separator()
        
class GT_New_Asset(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "New Asset"
    bl_category = "Capsule"
    
    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            if context.active_object.GTObj.is_GT_asset is False:
                return True
                
        return False
    
    def draw(self, context):
        layout = self.layout
        
        scn = context.scene.GTScn
        ob = context.object.GTObj
        grp = context.object.GTGrp
        mnu = context.object.GTMnu
        
        #layout.label(text="Create Game Tools Asset")
        col_asset = layout.column(align=True)
        col_asset.alignment = 'EXPAND'
        col_asset.prop(scn, "new_object_name", text="Object Name", icon = "OBJECT_DATAMODE")
        
        layout.separator()
        
        col_asset = layout.column(align=True)
        col_asset.prop(scn, "new_asset_select", text="", icon = "OBJECT_DATAMODE")
        
        layout.separator()
        
        col_assign = layout.column(align=True)
        col_assign.alignment = 'EXPAND'
        col_assign.operator(GT_Assign_Base.bl_idname)
        col_assign.operator(GT_Create_New_Asset.bl_idname)
        
        layout.separator()
        
        
        
        
class GT_Object_Name(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Asset Details"
    bl_category = "Capsule"
    
    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            if context.active_object.GTObj.is_GT_asset is True:
                if context.active_object.GTGrp.is_group_object is False and  context.active_object.GTGrp.is_origin_point is False:
                    return True
                
        return False

    def draw(self, context):
        layout = self.layout
        
        scn = context.scene.GTScn
        ob = context.object.GTObj
        obj = context.active_object
        grp = context.object.GTGrp
        mnu = context.object.GTMnu
        

        if grp.is_group_object is False:
            #layout.label(text="Asset Type:", icon = "OBJECT_DATAMODE")
            #col_asset = layout.column(align=False)
            #col_asset.alignment = 'EXPAND'
            
            #col_asset.label(text=ob.asset_name, icon = "GROUP")
            
            if int(ob.object_type) is 1:
                if grp.has_group_object is True:
                    col_asset = layout.column(align=True)
                    col_asset.prop(ob, "asset_name", text="Group Name", icon = "GROUP")
                col_asset = layout.column(align=True)
                col_asset.prop(ob, "component_name", text="Object Name", icon = "OBJECT_DATAMODE")
                
            else:
                
                if grp.has_group_object is True:
                    col_asset = layout.column(align=True)
                    col_asset.prop(ob, "asset_name", text="Group Name", icon = "GROUP")
                if grp.is_own_group is False:
                    col_asset = layout.row(align=True)
                    col_asset.label(text="Parent Name")
                    col_asset.label(text=ob.base_name, icon = "RETOPO")
                col_asset = layout.column(align=True)
                col_asset.prop(ob, "component_name", text="Object Name", icon = "OBJECT_DATAMODE")
                
            layout.separator()
            col_asset = layout.column(align=True)
            #col_asset.operator(GT_Create_Group.bl_idname, icon = "ZOOMIN")
            #col_asset.operator(GT_Remove_From_Group.bl_idname, icon = "X")
            col_asset.operator(GT_Create_Group.bl_idname)
            col_asset.operator(GT_Remove_From_Group.bl_idname)
                
            
        
            
            
class GT_Object_Stage(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Object Stage"
    bl_category = "Capsule"
    
    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            if context.active_object.GTObj.is_GT_asset is True:
                if context.active_object.GTGrp.is_group_object is False and  context.active_object.GTGrp.is_origin_point is False:
                    return True
                
        return False
    
    def draw(self, context):
        layout = self.layout
        
        scn = context.scene.GTScn
        ob = context.object.GTObj
        obj = context.active_object
        grp = context.object.GTGrp
        mnu = context.object.GTMnu
        smn = context.scene.GTSmn
        
        col_asset = layout.column(align=True)
        col_asset.alignment = 'EXPAND'
        
        if grp.is_group_object is False:
        
            #col_asset.label(text="Asset Type:", icon = "OBJECT_DATAMODE")
            col_asset.prop(ob, "asset_type", text="", icon = "OUTLINER_OB_MESH")
        
            #Define Functions for Assets
            if int(ob.asset_type) is 1:
                row_asset = col_asset.row(align=True)
                #row_asset.prop(scn, "low_poly_base_options", text="")
                row_asset.operator_menu_enum(GT_Create_Low_Poly_Base.bl_idname, "low_poly_base_options")
                col_asset.operator(GT_Check_Mesh.bl_idname)
                col_asset.separator()
                col_asset.prop(ob, "mark_repto")
                col_asset.prop(smn, "freeze_toggle")
                
                if smn.freeze_toggle is True:
                    col_asset.separator()
                    col_asset.separator()
                
                    row_asset = col_asset.row(align=True)
                    col_asset.separator()
                    col_asset.prop(scn, "freeze_name", icon="PMARKER_ACT")
                    col_asset.separator()
                    col_asset.separator()
                    
                    row_asset = col_asset.row(align=True)
                    if context.selected_objects == 1 and obj.object_type is '1':
                        row_asset.operator_menu_enum(GT_Freeze.bl_idname, "freeze_options", icon="PMARKER_SEL")
                    else:
                        row_asset.operator_menu_enum(GT_Multi_Freeze.bl_idname, "freeze_options", icon="PMARKER_SEL")
                
                    row_asset = col_asset.row(align=True)
                    
                    row_asset = col_asset.row(align=True)
                    row_asset.operator_menu_enum(GT_Unfreeze.bl_idname, "unfreeze_options", icon="PMARKER")
                    row_asset = layout.row(align=True)
                    row_asset.template_list("UI_Freeze_List", "default", mnu, "freeze_collection", mnu, "freeze_collection_index", rows=2, maxrows=6)
                
            
            if int(ob.asset_type) is 2:
                col_asset.operator(GT_Create_Collision.bl_idname)
                col_asset.operator(GT_Create_Cage.bl_idname)


            
class GT_Object_Type(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Object Settings"
    bl_category = "Capsule"
    
    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            if context.active_object.GTObj.is_GT_asset is True:
                if context.active_object.GTGrp.is_group_object is False and  context.active_object.GTGrp.is_origin_point is False:
                    return True
                
        return False
    
    def draw(self, context):
        layout = self.layout
        
        scn = context.scene.GTScn
        ob = context.object.GTObj
        obj = context.active_object
        grp = context.object.GTGrp
        mnu = context.object.GTMnu
        
        col_object = layout.column(align=True)
        #col_object.alignment = 'EXPAND'
        
        #Define Functions for Base Objects
        if int(ob.object_type) is 1:
            #col_object.prop(ob, "object_type", text="", icon = "RETOPO")
            #col_object.label(text="Basic Tools")
            col_object.operator(GT_Duplicate_Base.bl_idname)
            col_object.operator(GT_Merge_Base.bl_idname)
            col_object.operator(GT_Seperate_Object.bl_idname)
            col_object.operator(GT_Delete_Base.bl_idname)
            col_object.operator(GT_Select_Base.bl_idname)
            
            layout.separator()
            
            col_object = layout.column(align=True)
            #col_object.label(text="Parenting Tools")
            col_object.operator(GT_Add_Components.bl_idname)
            col_object.operator(GT_Find_Components.bl_idname)
            col_object.operator(GT_Remove_Components.bl_idname)
            col_object = layout.column(align=True)
            col_object.prop(mnu, "view_component_list")
            
            # This code is for displaying the component object list
            if mnu.view_component_list is True:
                
                if len(obj.children) != 0:
                        
                    layout.template_list("UI_Component_List", "default", mnu, "component_collection", mnu, "component_collection_index", rows=3, maxrows=6)
                  
            layout.separator()

            col_object = layout.column(align=True)
            col_object.alignment = 'EXPAND'
            row_object = col_object.row(align=True)
            row_object.prop(ob, "origin_point", text="", icon = "CURSOR")
            row_object.operator("object.gt_update_origin", icon = "ROTATE")
            
            if int(ob.origin_point) is 4:
                row_object = layout.row(align=True)
                #col_object.operator_menu_enum(ShowVertexGroups.bl_idname, "select_objects", text=ShowVertexGroups.bl_label)
                row_object.prop(mnu, "vertex_groups",text = "",  icon = "GROUP_VERTEX")
            
        if int(ob.object_type) is 2:
            #col_object.prop(ob, "object_type", text="", icon = "RETOPO")
            
            col_object.operator(GT_Duplicate_Base.bl_idname)
            col_object.operator(GT_Merge_Base.bl_idname)
            col_object.operator(GT_Seperate_Object.bl_idname)
            col_object.operator(GT_Delete_Base.bl_idname)
            col_object.operator(GT_Select_Base.bl_idname)
            
            
            layout.separator()
            
            col_object = layout.column(align=True)
            col_object.operator(GT_Select_Parent.bl_idname)
            col_object.operator(GT_Remove_From_Base.bl_idname)
            
            layout.separator()
        
            col_base = layout.row(align=True)
            col_base.alignment = 'EXPAND'
            col_base.prop(ob, "origin_point", text="", icon = "CURSOR")
            col_base.operator("object.gt_update_origin", icon = "ROTATE")
            
                
            if int(ob.origin_point) is 4:
                col_base = layout.column(align=True)
                #col_base.operator_menu_enum("object.vertex_groups", "select_objects", text=ShowVertexGroups.bl_label)
                col_base.prop(mnu, "vertex_groups", text = "", icon = "GROUP_VERTEX")
            
            
class GT_Group_Details(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Group Details"
    bl_category = "Capsule"
    
    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            if context.active_object.GTObj.is_GT_asset is True:
                if context.active_object.GTGrp.is_group_object is True or context.active_object.GTGrp.is_origin_point is True:
                    return True
                
        return False
    
    def draw(self, context):
        layout = self.layout
        
        scn = context.scene.GTScn
        ob = context.object.GTObj
        obj = context.active_object
        grp = context.object.GTGrp
        mnu = context.object.GTMnu
        
        col_group = layout.column(align=True)
        col_group.alignment = 'EXPAND'
        col_group.prop(ob, "asset_name", text="Asset Name", icon = "GROUP")
        
        
        
        
class GT_Group_Object(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Origin Object"
    bl_category = "Capsule"
    
    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            if context.active_object.GTObj.is_GT_asset is True:
                if context.active_object.GTGrp.is_group_object is True:
                    return True
                
        return False
    
    def draw(self, context):
        layout = self.layout
        
        scn = context.scene.GTScn
        ob = context.object.GTObj
        obj = context.active_object
        grp = context.object.GTGrp
        mnu = context.object.GTMnu
        
        col_group = layout.row(align=True)
        col_group.alignment = 'EXPAND'
        
        #col_group.label(text="Group Object", icon = "OBJECT_DATAMODE")
        col_group.alignment = 'EXPAND'
        col_group.prop(grp, "x_ray_toggle")
        col_group = layout.row(align=True)
        col_group.prop(grp, "group_dummy_object", text="Dummy Object")
        col_group = layout.row(align=True)
        #col_group.prop(grp, "group_dummy_loc", text="Dummy Position")
        #col_group = layout.row(align=True)
        col_group.prop(grp, "group_dummy_location", text="Dummy Location")
        col_group = layout.column(align=True)
        
        col_group.separator()
        
        if int(grp.group_dummy_location) is 3:
            col_group.prop(grp, "dummy_object_select", text = "", icon = "OBJECT_DATAMODE")
            
        elif int(grp.group_dummy_location) is 2:
            col_group.operator(GT_Move_Dummy.bl_idname)
        
        col_group.prop(grp, "group_dummy_offset")
        col_group.prop(grp, "group_dummy_size")
        
        
        
class GT_Origin_Object(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Origin Object"
    bl_category = "Capsule"
    
    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            if context.active_object.GTObj.is_GT_asset is True:
                if context.active_object.GTGrp.is_origin_point is True:
                    return True
                
        return False
    
    def draw(self, context):
        layout = self.layout
        
        scn = context.scene.GTScn
        ob = context.object.GTObj
        obj = context.active_object
        grp = context.object.GTGrp
        mnu = context.object.GTMnu
        
        col_group = layout.column(align=True)
        col_group.alignment = 'EXPAND'
        
        col_group.prop(grp, "x_ray_toggle")
        col_group = layout.column(align=True)
        col_group.prop(grp, "origin_location", text="")
        
        if int(grp.origin_location) is 3:
            #col_group = layout.column(align=True)
            col_group.prop(grp, "origin_object_select", text = "", icon = "OBJECT_DATAMODE")
        
        #col_group = layout.column(align=True)
        col_group.prop(grp, "origin_dummy_size")   
        
        
                    
        
class GT_Export(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Export"
    bl_category = "Capsule"
    
    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            if context.active_object.GTObj.is_GT_asset is True:
                if context.active_object.GTGrp.is_group_object is True:
                    return False
                
        return False

    def draw(self, context):
        layout = self.layout
        
        scn = context.scene.GTScn
            
        col_export = layout.row(align=True)
        col_export.alignment = 'EXPAND'
        col_export.prop(scn, "export_destination", text="Export Destination", expand=True)
        
        layout.separator()
        
        col_export = layout.column(align=True)
        col_export.prop(scn, "embed_textures", expand=True)
        
        if int(scn.engine_select) is 1:
            col_export.prop(scn, "ue4_scale_100", expand=True)
            
        layout.separator()
            
        col_export = layout.row(align=True)
        col_export.prop(scn, "export_scope", text="",icon="FORWARD")
        col_export.operator("scene.gt_export_assets")
        
        layout.separator()

classes = (UI_Freeze_List, UI_Visibility_List, UI_Component_List, GT_Tools, GT_New_Asset, GT_Object_Name, GT_Object_Stage, GT_Object_Type, GT_Group_Details, GT_Group_Object, GT_Origin_Object, GT_Export)

def register():
    print("-"*40)
    print("Registering UI")
    
    for cls in classes:
        bpy.utils.register_class(cls)
    
    #bpy.utils.register_module(__name__)

def unregister():
    print("-"*40)
    print("Unregistering UI")
    
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    #bpy.utils.unregister_module(__name__)
    
    