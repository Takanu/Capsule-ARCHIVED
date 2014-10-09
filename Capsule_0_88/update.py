from .definitions import GenerateObjectShading, ShadeNormal, ShadeBoxBounds, ShadeWireframe, ShadeWire, ShadeTexture, ShadeHide, SolidifyGroupShade, DefaultGroupShade, FocusObject, SelectObject, ActivateObject, DuplicateObject, DeleteObject, MoveObject, MoveObjectToObject, AddToGroup, FindInGroup, RemoveFromAllGroups, SwitchToExistingGroup, SwitchToNewAsset, SwitchToGroupAsset, SwitchToParentAsset, GenerateName, CheckGroupName, CheckObjectName, FindAssetTypeName, AddParent, ClearParent, SearchModifiers, FindObjectInModifier, AttachToDummy, FindFreezeObject

from .definitions import GenerateVisibilityList, ClearVisibilityList, GenerateComponentList, ClearComponentList, GenerateFreezeList, FindLowestLocation, FindHighestLocation, FindMedianLocation, AttachToDummy, DetachFromDummy, FindDummyConstraintObjects, SetObjectOrigin

import bpy, bmesh, time
from math import *

def Update_VisibilityToggle(self, context):
    
    active = None
    selected = []
    
    for sel in context.selected_objects:
        if sel.name != context.active_object.name:
            selected.append(sel)
            
    active = context.active_object
    
    print("---Inside Update_VisibilityToggle---")
    
    # Get the toggle and check whether it's on or off
    toggle = context.scene.GTSmn.scene_visibility_toggle
    smn = context.scene.GTSmn
    
    # If off, reset the visibility generation
    if toggle is False:
        ClearVisibilityList(self, context)
        smn.vis_generate_toggle = True
    
    # If on, create the list again
    elif toggle is True:
        if smn.vis_generate_toggle is True:
            print("> - Entering GenerateVisibilityList")
            GenerateVisibilityList(self, context)
            
    # Re-select the objects previously selected
    for sel in selected:
        SelectObject(sel)
        
    ActivateObject(active)
        
def Update_ComponentToggle(self, context):
    
    # Get the toggle and check whether it's on or off
    toggle = context.object.GTMnu.view_component_list
    smn = context.scene.GTSmn
    
    print("COMPONENT TOGGLE")
    print(self)
    
    smn.component_update_toggle = False
    
    # If off, reset the visibility generation
    if toggle is False:
        ClearComponentList(self, context)
        smn.component_generate_toggle = True
    
    # If on, create the list again
    elif toggle is True:
        if smn.component_generate_toggle is True:
            GenerateComponentList(self, context)
        
        
def Update_CompomentListType(self, context):
    
    # Pass the chosen data type to the actual visibility enum stored in the object
    sel = context.active_object
    obj = sel.GTObj
    
    for child in sel.children:
        if self.name == child.GTObj.component_name:
            child.GTObj.visibility = self.type
            print("COMPONENT LIST")
            print(self)
            
            # If we are permitted to change the UI symbol, change it!
            if context.scene.GTSmn.component_update_toggle is True:
                context.scene.GTSmn.component_generate_toggle = False
                child.GTMnu.view_component_list = False
                child.GTMnu.view_component_list = True
                
def Update_FreezeList(self, context):
    
    GenerateFreezeList(self, context)
                
            
def Update_VisibilityListType(self, context):
    
    # Pass the chosen data type to the actual visibility enum stored in the object
    obj = context.active_object
    scn = context.scene.GTScn
    smn = context.scene.GTSmn
    
    # Get the collection name to see what property needs updating
    if self.name == "High-Poly":
        scn.visibility_HP = self.type
        
    elif self.name == "Low-Poly":
        scn.visibility_LP = self.type
    
    elif self.name == "Cage":
        scn.visibility_CG = self.type
        
    elif self.name == "Collision":
        scn.visibility_CX = self.type
        
    elif self.name == "Parents":
        scn.visibility_base = self.type
        
    elif self.name == "Children":
        scn.visibility_component = self.type
        
    elif self.name == "Freeze":
        scn.visibility_freeze = self.type
    
            
    if smn.vis_update_toggle is True:
        smn.vis_update_toggle = False
        smn.scene_visibility_toggle = False
        smn.scene_visibility_toggle = True
                
                
def Update_FreezeDelete(self, context):
    
    # Just use self to delete the linked object and all it's children
    sel = context.active_object
    scn = context.scene.GTScn
    smn = context.scene.GTSmn
    
    # Apparently you need to also delete the mesh data, so this is currently on hold.
    print("PREPARING TO DELETE >:)")
    freeze = FindFreezeObject(sel, self.index)
    
    if freeze is not None:
        
        print("O - Freeze isn't none, yay!")
        
        if len(freeze.children) is not 0:
            for child in freeze.children:
                DeleteObject(child)
                
        print("> - Deleting parent...")    
        DeleteObject(freeze)
        
    else:
        print("!!! - Update_FreezeDelete failed.  No Freeze object available.")
        return
    
    # Regenerate the list to ensure it isnt displayed.
    DefaultGroupShade(sel.GTObj.asset_name, scn)
    FocusObject(sel)
    GenerateFreezeList(sel, context)
    
def Update_FreezeView(self, context):
    
    print("---Inside Update_FreezeView---")
    
    sel = context.active_object
    scn = context.scene.GTScn
    
    freeze = FindFreezeObject(sel, self.index)
    
    if freeze is not None:
        
        print("O - Found a freeze object")
        print(freeze.name)
        
        print("# - View being set:")
        print(self.view)
        
        # Set the freeze hide boolean
        freeze.GTObj.freeze_hide = self.view
        GenerateObjectShading(freeze, scn)  
        
        
        # Also set the children if there are any
        if len(freeze.children) is not 0:
            for child in freeze.children:
                child.GTObj.freeze_hide = self.view
                GenerateObjectShading(child, scn)
                
    FocusObject(sel)
        
def Update_FreezeName(self, context):
    
    print("---Inside Update_FreezeName---")
    sel = context.active_object
    freeze = None
    
    print("# - Object name being searched:")
    print(self.name)
    
    freeze = FindFreezeObject(sel, self.index)
    
    if freeze is not None:
        print("> - Assigning new name")
        freeze.GTObj.freeze_name = self.name
    
        
    
def Update_Visibility(self, context):
    
    selObj = context.active_object
    obj = context.active_object.GTObj
    scn = context.scene.GTScn
    print("Inside Visibility")
    print(self.component_name)
    
    # If the object has kids, and one of them is the visibility object being changed, use it!
    if obj.object_type is '1':
        
        # If the base has children that are the same name of self, we're dealing with a Component
        # List focused change.
        if len(selObj.children) != 0:
            for child in selObj.children:
                if child.GTObj.base_name == self.base_name and child.GTObj.component_name == self.component_name:
                    print("We made it!")
                    GenerateObjectShading(child, scn)
                    
        # Otherwise the base object is just being changed            
        else:
            GenerateObjectShading(selObj, scn)
            
            
    # If it's a component, just deal with it in a standard way
    elif obj.object_type is '2':
        GenerateObjectShading(selObj, scn)
                    
    
    FocusObject(selObj)
    


def Update_HP_Visibility(self, context):
    
    #Find all objects in the scene that are considered high-poly
    scn = context.scene.GTScn
    obj = context.active_object
    smn = context.scene.GTSmn
    type = scn.visibility_HP
    objectList = []
    
    # Used to prevent use during list generation
    if smn.scene_update_toggle == True:
        return None
        
    for item in bpy.data.objects:  
        if item.GTObj.is_GT_asset is True:
            if item.GTGrp.is_group_object is False and item.GTGrp.is_origin_point is False:
                if item.GTObj.asset_type is "1":
                    objectList.append(item)
                
    for object in objectList:
        GenerateObjectShading(object, scn)
    
    FocusObject(obj)
    
def Update_LP_Visibility(self, context):
    
    #Find all objects in the scene that are considered low-poly
    
    #Now find the type and give the objects that shading
    
    print("Rawr")
    
def Update_CG_Visibility(self, context):
    print("Rawr")
    
def Update_CX_Visibility(self, context):
    print("Rawr")
    
def Update_BaseVisibility(self, context):
    
    #Find all objects in the scene that are considered high-poly
    print("Inside BaseVisibility")
    scn = context.scene.GTScn
    obj = context.active_object
    smn = context.scene.GTSmn
    type = scn.visibility_base
    objectList = []
    
    # Used to prevent use during list generation
    if smn.scene_update_toggle == True:
        return None
        
    for item in bpy.data.objects:  
        if item.GTObj.is_GT_asset is True:
            if item.GTGrp.is_group_object is False and item.GTGrp.is_origin_point is False:
                if item.GTObj.object_type is "1":
                    print("Found Item O_O")
                    objectList.append(item)
                
    for object in objectList:
        GenerateObjectShading(object, scn)
    
    FocusObject(obj)
    
def Update_ComponentVisibility(self, context):
    
    #Find all objects in the scene that are considered high-poly
    scn = context.scene.GTScn
    obj = context.active_object
    smn = context.scene.GTSmn
    type = scn.visibility_component
    objectList = []
    
    # Used to prevent use during list generation
    if smn.scene_update_toggle == True:
        return None
        
    for item in bpy.data.objects:  
        if item.GTObj.is_GT_asset is True:
            if item.GTGrp.is_group_object is False and item.GTGrp.is_origin_point is False:
                if item.GTObj.object_type is "2":
                    objectList.append(item)
                
    for object in objectList:
        GenerateObjectShading(object, scn)
    
    FocusObject(obj)
    
def Update_FreezeVisibility(self, context):
    
    #Find all objects in the scene that are freeze objects
    print("Inside Update_FreezeVisibility")
    scn = context.scene.GTScn
    obj = context.active_object
    smn = context.scene.GTSmn
    type = scn.visibility_HP
    objectList = []
    
    # Used to prevent use during list generation
    if smn.scene_update_toggle == True:
        return None
        
    for item in bpy.data.objects:  
        if item.GTObj.is_GT_asset is True:
            if obj.GTObj.base_name == item.GTObj.base_name:
                if item.GTObj.is_frozen is True:
                    objectList.append(item)
    
    print(len(objectList))            
    for object in objectList:
        GenerateObjectShading(object, scn)
    
    FocusObject(obj)
            
        
def Update_ObjectOrigin(self, context):
    
    # Create an array to store all found objects
    objects_to_select = []
    
    sel = context.active_object
    
    print("---Inside Update_ObjectOrigin---")
    
    if sel.GTObj.update_toggle is False:
    
        # Store the active object
        active = context.active_object
            
        # Find all the selected objects in the scene and store them
        for object in context.selected_objects:
            if object.name != active.name:
                print("! - Found Selected Object")
                objects_to_select.append(object) 
                
        # First, we need to process the active object, as it already has the correct enum.
        print("# - Active Object Name")
        print(active)
        FocusObject(active) 
        
        # Get the origin point and call the respective def
        newInt = int(active.GTObj.origin_point)
        enum = active.GTObj.origin_point
        
        SetObjectOrigin(active, newInt, context)
            
        # Now were going to focus each selected object using the update loop, to prevent a recursion
        # loop
        for object in objects_to_select:
            object.GTObj.update_toggle = True
            FocusObject(object)
            object.GTObj.origin_point = enum
        
        active.GTObj.update_toggle = False
        FocusObject(active)
            
        # Now were at the end, re-select the objects in the correct order.  
        for object in objects_to_select:
            SelectObject(object)
            object.GTObj.update_toggle = False
            
        return None
        
    else:
        # Focus on the object
        print("# - Selected Object Name")
        FocusObject(sel) 
        print(sel.name)
        
        # Get the origin point and call the respective def
        newEnum = int(context.active_object.GTObj.origin_point)
        SetObjectOrigin(sel, newEnum, context)
        sel.GTObj.update_toggle = False
        
        return None
        
    
        
    return None 

def Update_ObjectVGOrigin(self, context):
    
    # Create an array to store all found objects
    objects_to_select = []
    objects_to_make_active = []
    
    print("Rawr?")
    
    # Store the active object
    objects_to_make_active.append(bpy.context.active_object)
            
    # Find all the selected objects in the scene and store them
    for object in context.selected_objects:
        objects_to_select.append(object)
        
    # Focus on the object with the newly selected vertex group
    FocusObject(bpy.context.active_object.object) 
        
    # Get the origin point and call the respective def
    newEnum = int(self.origin_point)
    VGSelect = int(bpy.context.active_object.GTMnu.vertex_groups)
    
    # If the index isnt one (which is the None selection), change the origin!)
    if VGSelect != 1:    
        SetObjectOrigin(object, newEnum, context)
        
    bpy.ops.object.select_all(action='DESELECT') 
        
    # Re-select all stored objects         
    for objectSelect in objects_to_select:
        bpy.ops.object.select_pattern(pattern=objectSelect.name)
             
    for objectActive in objects_to_make_active:
        bpy.ops.object.select_pattern(pattern=objectActive.name)
        bpy.context.scene.objects.active = objectActive
        
    return None 

def Update_AssetType(self, context):
    
    # Create a pop-up menu to prompt the user that if there are freeze states, they will be deleted
    # If the user pressed Yes, we are clear to proceed

    # Whatever its changing to, check visibility and freeze options to ensure its set properly
    
    # Now ensure the asset type for all it's components are changed
    
    # Get any name changes associated with it
    GenerateName(context.active_object)

    return None 

def Update_ObjectType(self, context):
    
    print("-"*40)
    print("---Inside Update_ObjectType---")
    
    sel = context.active_object
    obj = sel.GTObj
    grp = sel.GTGrp
    ext = sel.GTExt
    scn = context.scene
    
    print("# - Object being operated on:")
    print(sel.name)
    
    # If its changing to a base, remove it as a parent and clear any property relations
    if int(self.object_type) is 1:
        
        if obj.old_object_type == '1':
            print("X - Base Object stayed the same, doing nothing")
            return None
            
        print("> - Changing to Base")
        
        if grp.has_group_object is False:
            
            # This gives it some context methinks
            if grp.is_own_group is False:
                print("> - Switching asset again")
                SwitchToNewAsset(sel, obj.component_name)
        
        # New naming conventions, only the base name needs setting to "None", no other actions required.
        obj.update_toggle = True   
        obj.base_name = "None"
        
        if sel.parent is not None:
            ClearParent(sel)
            
        if grp.has_group_object is True:
            AttachToDummy(sel)
            
        obj.old_object_type = obj.object_type
        
        return None
        
    # If its changing to a component, make sure it loses it's children
    if int(self.object_type) is 2:
        
        if obj.old_object_type == '2':
            print("X - Component Object stayed the same, doing nothing")
            return None
        
        print("> - Changing to Component")
        print("> - Attempting to remove kids")
        
        for child in sel.children:
            
            # Now due to Mr.Multi-Asset, we have a more complex situation.  If it doesnt have a group, deal with it normally.  Otherwise, we don't 
            print(child.name)
            # Change the object focus so they can be altered
            FocusObject(child)
            print("O - Found a kid, killing...")
                
            child.GTObj.object_type = "1"
            
        FocusObject(sel)
        sel.GTObj.visibility = '1'
        
        # Switch and generate the name if theres no parent
        if sel.parent is None:
            print("> - Component has no parent, why the fuck are we here?")
            obj.update_toggle = True
            obj.base_name = "None"
            
        else:
            print("> - Component has a parent, proceeding...")
            # New naming convention, only the base name needs setting
            obj.base_name = sel.parent.GTObj.component_name
            print("> - Outside the NIGHTMARE LOOP")   
        
        print("> - Finishing ObjectType Update...")    
        GenerateName(sel)
        obj.old_object_type = obj.object_type
        
        return None 
            
    print("! - Exiting update, object type is neither")
    print("-"*40)
    return None 


def Update_AssetName(self, context):
    
    sel = context.active_object
    obj = sel.GTObj
    scn = context.scene.GTScn
    grp = sel.GTGrp
    ext = sel.GTExt
    
    #print("-"*40)
    #print("---Inside AssetName---")
    
    #if scn.asset_update_loop is True:
        #print("."*60)
        #print("! - First time inside AssetName, loop starting...")
        #print("."*60)
    
    # First check no bad names have been entered, if they haven't turned on the toggle, spit an error and return
    if obj.asset_name == "":
        if obj.update_toggle is False:
            obj.asset_name = obj.old_asset_name
            bpy.ops.object.gt_blank_report('INVOKE_DEFAULT')
            return None
    
    elif obj.asset_name == "None":
        if obj.update_toggle is False:
            obj.asset_name = obj.old_asset_name
            bpy.ops.object.gt_name_report('INVOKE_DEFAULT')
            return None
        
        
    # Now we can continue to the renaming process
    else:
        #print("> - Starting/Continuing the rename process")
        #print(scn.asset_update_loop)
        
        # For when an asset name is renamed directly from the UI
        # A check to ensure that it isnt named the same as another
        if scn.asset_update_loop is True:
            if grp.has_group_object is True:
                if grp.is_own_group is False:
                    if scn.asset_group_exit is False:
                        if sel.parent is None:
                            if grp.is_origin_point is False and grp.is_group_object is False:
                                if ext.base_group_exit is False and ext.comp_group_exit is False:
                                    #print("! - Checking Asset Name")
                                    scn.asset_update_loop = True
                
                                    checkedName = CheckGroupName(sel, obj.asset_name, 0)
                                    print(checkedName)
                
                                    scn.asset_group_exit = True
                                    obj.asset_name = checkedName
                
                                    scn.asset_group_exit = False    
                                    obj.update_toggle = False
                                    return None
                
            
        # Now for every object in the group, also rename the asset name
        
        if scn.asset_update_loop is True:
            scn.asset_update_loop = False
            #print("> - Entering AssetName Update Loop")
            
            if obj.old_asset_name in bpy.data.groups:
                #print("O - Found Old Asset name")
                group = bpy.data.groups[obj.old_asset_name]
                group.name = obj.asset_name
                #print(group.name)
                #print("? - Searching for objects in the Old Asset")
                    
                for object in group.objects:
                    FocusObject(object)
                    #print("O - Found object, renaming...")
                    #print(object.name)
                    object.GTObj.asset_name = obj.asset_name
                    
            scn.asset_update_loop = True
            DefaultGroupShade(obj.asset_name, scn)
            FocusObject(sel)
            
            #print("."*60)
            #print("! - Finished Recursive loop, leaving...")
            #print("."*60)
            
        #print("O - Renaming Asset")
        #print(sel.name)    
        FocusObject(sel)
        obj.old_asset_name = obj.asset_name
        
        # Change the name for the object
        GenerateName(sel)
        obj.update_toggle = False
    
        #print("---Exiting the AssetName Update Loop---")
        #print("*"*40)
        return None 

    #print("*"*40)

def Update_BaseName(self, context):
    
    sel = context.active_object
    obj = context.active_object.GTObj
    scn = context.scene.GTScn
    ext = sel.GTExt
    oldName = ""
    
    print("---Inside BaseName---")
    print(obj.base_name)
    print(sel.name)
     
    # First check no bad names have been entered, if they haven't turned on the toggle, spit an error and return
    if obj.base_name == "":
        if obj.update_toggle is False:
            print("! - Found a no name base name...")
            obj.base_name = obj.old_base_name
            bpy.ops.object.gt_blank_report('INVOKE_DEFAULT')
            return None
    
    elif obj.base_name == "None":
        if obj.update_toggle is False:
            print("! - Found a no name base name...")
            obj.base_name = obj.old_base_name
            bpy.ops.object.gt_name_report('INVOKE_DEFAULT')
            return None
        
        
    else:
        # If the object has no group object, also rename the asset name.
        if sel.GTGrp.is_own_group is True:
            if ext.base_group_exit is False:
                print("O - Updating Asset Name")
                scn.asset_update_loop = True
                
                checkedName = CheckGroupName(sel, obj.base_name, 0)
                print(checkedName)
                
                ext.base_group_exit = True
                obj.base_name = checkedName 
                
                if checkedName != obj.asset_name:
                    obj.asset_name = checkedName
                
                # Why is this here?
                #obj.asset_name = obj.base_name
                
                ext.base_group_exit = False    
                obj.update_toggle = False
                
                return None
        
        # If the object being renamed is in a group, ensure it isnt the same as another base object
        elif sel.GTGrp.has_group_object is True:
            if ext.base_group_exit is False:
                print("O - Updating Base Name")
                scn.asset_update_loop = True
                
                checkedName = CheckObjectName(sel, obj.base_name, 0)
                print(checkedName)
                
                ext.base_group_exit = True
                print(obj.base_name)
                obj.base_name = checkedName 
                ext.base_group_exit = False    
                
                return None
                
        # Change the name for the object
        print("O - Generating Base Name")
        GenerateName(sel)
        oldName = obj.old_base_name
        obj.old_base_name = obj.base_name
        print("? - Still here?")
        FocusObject(sel)
        
        # If the object we just renamed is a frozen object, we need to give it's item in the list
        # some new parameters
        #if sel.GTObj.is_frozen is True:
            #for item in sel.GTObj.freeze_collection:
                #if item.name == sel.GTObj.base_name:
                    
    
    # As a last thing, we need to rename any freeze objects :D
    if obj.object_type is '1':
        if obj.is_frozen is False:
            if obj.asset_name in bpy.data.groups:
                group = bpy.data.groups[obj.asset_name]
        
                print("? - Starting Freeze Search")
                
                for object in group.objects:
                    if object.name.find(oldName) != -1:
                        if object.name.find("_FZ") != -1:
                            print("Found Freeze Object")
                            print(object.name)
                            FocusObject(object)
                            object.GTObj.base_name = obj.base_name
    
    print("? - Final Preparation")            
    FocusObject(sel)

    obj.update_toggle = False
    
    DefaultGroupShade(obj.asset_name, scn)

    FocusObject(sel)
    
    print("X - Exiting Update_BaseName")
    
    return None 


def Update_ComponentName(self, context):
    
    sel = context.active_object
    obj = context.active_object.GTObj
    scn = context.scene.GTScn
    grp = sel.GTGrp
    ext = sel.GTExt
    
    print("---Entered ComponentName---")
    
    # First check no bad names have been entered, if they haven't turned on the toggle, spit an error and return
    if obj.component_name == "":
        if obj.update_toggle is False:
            obj.component_name = obj.old_component_name
            bpy.ops.object.gt_blank_report('INVOKE_DEFAULT')
            return None
    
    elif obj.component_name == "None":
        if obj.update_toggle is False:
            obj.component_name = obj.old_component_name
            bpy.ops.object.gt_name_report('INVOKE_DEFAULT')
            return None
            
    else:
        
        # If the object has no group object or parent objects, rename the asset name.
        if sel.GTGrp.is_own_group is True:
            print("> - Object is own group")
            if sel.parent is None:
                print("> - Object has no parent")
                if ext.comp_group_exit is False:
                    print("O - Updating Asset Name")
                    print(grp.is_own_group)
                    scn.asset_update_loop = True
                    
                    checkedName = CheckGroupName(sel, obj.component_name, 0)
                    print(checkedName)
                    ext.comp_group_exit = True
                    obj.component_name = checkedName 
                    
                    if checkedName != obj.asset_name:
                        obj.asset_name = checkedName
                    
                    # Why is this here?
                    #obj.asset_name = obj.component_name
                    
                    ext.comp_group_exit = False
                    obj.update_toggle = False
                    
                    return None
                    
        # If the object being renamed is in a group, ensure it isnt the same as another base object
        elif sel.GTGrp.has_group_object is True:
            if ext.comp_group_exit is False:
                print("O - Updating Component Name")
                scn.asset_update_loop = True
                
                checkedName = CheckObjectName(sel, obj.component_name, 0)
                print(checkedName)
                
                ext.comp_group_exit = True
                obj.component_name = checkedName 
                ext.comp_group_exit = False    
                
                return None
                    
        # Change the name for the object
        print("O - Generating Name")
        GenerateName(sel)
        obj.old_component_name = obj.component_name
        
        # Change the name for all parent objects
        for child in sel.children:
            FocusObject(child)
            print("> - Setting Base Name to Child")
            child.GTObj.base_name = obj.component_name
                    
    print("< - Exiting Loop")                
    ext.comp_group_exit = False    
    obj.update_toggle = False
    
    DefaultGroupShade(obj.asset_name, scn)
    
    FocusObject(sel)

    return None 
    
def Update_DummyObject(self, context):
    sel = context.active_object
    scn = context.scene.GTScn
    obj = sel.GTObj
    grp = sel.GTGrp
    
    emptyTypes = ['1', '2']
    meshTypes = ['3', '4', '5']
    objects = []
    originPoint = None
    newDummy = None
    
    wasEmpty = False
    wasMesh = False
    isEmpty = False
    isMesh = False
    
    if scn.dummy_update_loop is False:
        #print("Erm, the dummy update loop is False?")
        return None
        
    if grp.old_group_dummy_object in emptyTypes:
        #print("WAS AN EMPTY")
        wasEmpty = True
    else:
        #print("WAS A MESH")
        wasMesh = True
        
    if grp.group_dummy_object in emptyTypes:
        #print("IS A EMPTY")
        isEmpty = True
    else:
        #print("IS A MESH")
        isMesh = True
        
    if wasEmpty == True and isEmpty == True:
        #print("SWITCHING EMPTY")
        if grp.group_dummy_object is '1':
            sel.empty_draw_type = 'PLAIN_AXES'
            grp.old_group_dummy_object = grp.group_dummy_object
        elif grp.group_dummy_object is '2':
            sel.empty_draw_type = 'SINGLE_ARROW'
            grp.old_group_dummy_object = grp.group_dummy_object
        #print("Rawr")
        
    else:
        
        #print("Inside Empty Types")
        objects = FindDummyConstraintObjects(sel.GTObj.asset_name)
        
        # First detach all objects from the dummy
        for object in objects:
            DetachFromDummy(object)
            
        # Also detach the origin
        if obj.asset_name in bpy.data.groups:
            group = bpy.data.groups[obj.asset_name]
        
            for object in group.objects:
                if object.GTGrp.is_origin_point is True:
                    originPoint = object
                    DetachFromDummy(object)
        
        # Store the current cursor location before we start moving it
        FocusObject(sel)
        cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
        previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]
        bpy.ops.view3D.snap_cursor_to_selected()
        
        # Give it the has_group_object property
        scn.dummy_update_loop = False
        
        # Make a new dummy object depending on what type it is
        if grp.group_dummy_object is '1':
            bpy.ops.object.select_all(action='DESELECT')  
            bpy.ops.object.add(type='EMPTY')
            newDummy = context.active_object
            newDummy.empty_draw_type = 'PLAIN_AXES'
            newDummy.GTGrp.group_dummy_object = '1'
            
        elif grp.group_dummy_object is '2':
            bpy.ops.object.select_all(action='DESELECT')  
            bpy.ops.object.add(type='EMPTY')
            newDummy = context.active_object
            newDummy.empty_draw_type = 'SINGLE_ARROW'
            newDummy.GTGrp.group_dummy_object = '2'
            
        elif grp.group_dummy_object is '3':
            #print("ADDING CIRCLE PRIMITIVE")
            bpy.ops.mesh.primitive_circle_add()
            newDummy = context.active_object
            newDummy.GTGrp.group_dummy_object = '3'
            
        elif grp.group_dummy_object is '4':
            #print("ADDING PLANE PRIMITIVE")
            bpy.ops.mesh.primitive_plane_add()
            newDummy = context.active_object
            newDummy.GTGrp.group_dummy_object = '4'
            
        
        AddToGroup(newDummy, obj.asset_name)
        newDummy.GTObj.old_asset_name = obj.old_asset_name
        newDummy.GTObj.asset_name = obj.asset_name
        
        newDummy.GTGrp.is_group_object = True
        newDummy.GTObj.is_GT_asset = True
        newDummy.GTGrp.old_group_dummy_object = grp.group_dummy_object
            
        newDummy.GTGrp.group_dummy_loc = grp.group_dummy_loc
        newDummy.GTGrp.group_dummy_offset = grp.group_dummy_offset
        
        
        # Lock scale and rotation
        bpy.data.objects[newDummy.name].lock_rotation[0] = True
        bpy.data.objects[newDummy.name].lock_rotation[1] = True
        bpy.data.objects[newDummy.name].lock_rotation[2] = True
    
        bpy.data.objects[newDummy.name].lock_scale[0] = True
        bpy.data.objects[newDummy.name].lock_scale[1] = True
        bpy.data.objects[newDummy.name].lock_scale[2] = True
            
        # We no longer need this object!
        DeleteObject(sel)
        FocusObject(newDummy)
        GenerateName(newDummy)
        
        #print(newDummy.GTGrp.is_group_object)
        #print(newDummy.GTObj.is_GT_asset)
        
        # Reattach all objects to it
        for object in objects:
            AttachToDummy(object)
            
        # Also re-attach the origin
        AttachToDummy(originPoint)
        
        FocusObject(newDummy)
        scn.dummy_update_loop = True
        
    
def Update_DummyPosition(self, context):
    
    sel = context.active_object
    obj = sel.GTObj
    scn = context.scene.GTScn
    grp = sel.GTGrp
    
    ZLocation = 0
    offset = 0
    FinalZ = 0
    originPoint = None
    objects = []
    
    if scn.dummy_update_loop is False:
        return None
    
    objects = FindDummyConstraintObjects(sel.GTObj.asset_name)
    
    # Detach every found object from the dummy
    for object in objects:
        DetachFromDummy(object)
                        
    # Get the median point for X and Y positioning
    location = FindMedianLocation(objects) 
    
    # Find out whether it has been switched to be positioned above or below the object
    if grp.group_dummy_loc is '1':
        #print("Dummy Location is Above")
        ZLocation = FindHighestLocation(objects)
        offset = grp.group_dummy_offset 
        FinalZ = ZLocation + offset
        
    elif grp.group_dummy_loc is '2':
        #print("Dummy Location is Below")
        ZLocation = FindLowestLocation(objects)
        offset = grp.group_dummy_offset
        FinalZ = ZLocation - offset
        
    else:
        return
    
    # Offset that positively or negatively by the distance variable
    location[2] = FinalZ
    
    # Position and move the dummy
    FocusObject(sel)
    cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
    previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]
    
    bpy.data.scenes[bpy.context.scene.name].cursor_location = location
    
    bpy.ops.view3D.snap_selected_to_cursor(use_offset=False)
    
    # Reattach every object
    for object in objects:
        AttachToDummy(object)
        
    bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc
    FocusObject(sel)
    
    #print("Finished!")
    
    
def Update_DummyLocation(self, context):
    
    # Allows the user to set the location of the dummy object
    
    sel = context.active_object
    obj = sel.GTObj
    scn = context.scene.GTScn
    grp = sel.GTGrp
    
    objects = FindDummyConstraintObjects(sel.GTObj.asset_name)
    FinalZ = 0
    offset = 0
    location = []
    
    # Now we can start operating. 
    # If its the freeform option, we don't do anything here
    if sel.GTGrp.group_dummy_location is '2':
        return None
    
    # Detach every found object from the dummy
    for object in objects:
        DetachFromDummy(object)
    
    # Auto-Update Method, uses code pinched from Update_DummyPosition
    if sel.GTGrp.group_dummy_location is '1':
        
        # Get the median point for X and Y positioning
        location = FindMedianLocation(objects)
        
        # Find out whether it has been switched to be positioned above or below the object
        if grp.group_dummy_loc is '1':
            #print("Dummy Location is Above")
            ZLocation = FindHighestLocation(objects)
            offset = grp.group_dummy_offset 
            FinalZ = ZLocation + offset
        
        elif grp.group_dummy_loc is '2':
            #print("Dummy Location is Below")
            ZLocation = FindLowestLocation(objects)
            offset = grp.group_dummy_offset
            FinalZ = ZLocation - offset

    
        # Offset that positively or negatively by the distance variable
        location[2] = FinalZ
        
        MoveObject(sel, location)
    
    # Method for snapping the dummy to a object.
    elif sel.GTGrp.group_dummy_location is '3':
        
        # Get the selected object
        selEnum = int(grp.dummy_object_select)
        
        count = -1
        count += 1
        
        if obj.asset_name in bpy.data.groups:
            group = bpy.data.groups[obj.asset_name]
            
            for object in group.objects:
                count += 1
                
                if selEnum == count:
                    location = object.location
        
                    MoveObject(sel, location)
                    
                    # Any assignment to a location array caused the fucking object to move
                    # This is more complex than required because I had to work around it :/
                    offset = grp.group_dummy_offset
                    newLocation = location
                    z = newLocation[2]
                    z += offset
                    
                    MoveObject(sel, (newLocation[0], newLocation[1], z))
                    
    
    # Reattach every object
    for object in objects:
        AttachToDummy(object)
    
    FocusObject(sel)
    
    print("Rawr")
    
def Update_DummyOffset(self, context):
    
    sel = context.active_object
    scn = context.scene.GTScn
    grp = sel.GTGrp
    
    ZLocation = 0
    offset = 0
    FinalZ = 0
    objects = []
    
    if scn.dummy_update_loop is False:
        return None
    
    objects = FindDummyConstraintObjects(sel.GTObj.asset_name)
    
    # Detach every found object from the dummy
    for object in objects:
        DetachFromDummy(object)
                        
    # Get the median point for X and Y positioning
    # The location offset uses the selection location instead of re-calibrating it
    location = sel.location
    
    # Find out whether it has been switched to be positioned above or below the object
    if grp.group_dummy_loc is '1':
        #print("Dummy Location is Above")
        ZLocation = FindHighestLocation(objects)
        offset = grp.group_dummy_offset 
        FinalZ = ZLocation + offset
        
    elif grp.group_dummy_loc is '2':
        #print("Dummy Location is Below")
        ZLocation = FindLowestLocation(objects)
        offset = grp.group_dummy_offset
        FinalZ = ZLocation - offset
        
    else:
        return
    
    # Offset that positively or negatively by the distance variable
    location[2] = FinalZ
    
    # Position and move the dummy
    FocusObject(sel)
    cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
    previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]
    
    bpy.data.scenes[bpy.context.scene.name].cursor_location = location
    
    bpy.ops.view3D.snap_selected_to_cursor(use_offset=False)
    
    # Reattach every object
    for object in objects:
        AttachToDummy(object)
        
    bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc
    FocusObject(sel)
    
def Update_DummySize(self, context):
    sel = context.active_object
    scn = context.scene.GTScn
    obj = sel.GTObj
    grp = sel.GTGrp
        
    emptyTypes = ['1', '2']
    meshTypes = ['3', '4', '5']
    
    # If its a normal dummy object, just change the draw size.
    if grp.group_dummy_object in emptyTypes:
        sel.empty_draw_size = grp.group_dummy_size
        
    # Otherwise, were going to have to do a fucking detach/attach system
    else:
        objects = FindDummyConstraintObjects(sel.GTObj.asset_name)
        
        # First detach all objects from the dummy
        for object in objects:
            DetachFromDummy(object)
        
        # Now change the scale value
        sel.dimensions = [(grp.group_dummy_size * 2), (grp.group_dummy_size * 2), sel.dimensions[2]]
        FocusObject(sel)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Reattach all objects to it
        for object in objects:
            AttachToDummy(object)
        
        FocusObject(sel)
        
def Update_GroupOrigin(self, context):
    sel = context.active_object
    scn = context.scene.GTScn
    obj = sel.GTObj
    grp = sel.GTGrp
    
    location = [0, 0, 0]
    
    if grp.origin_location is '1':
        # Get the median and lowest Z position
        print("Inside Number 1!")
        objects = FindDummyConstraintObjects(obj.asset_name)
        
        for object in objects:
            if object.GTGrp.is_origin_point is True:
                objects.remove(object)
                
        # Iterate through the objects, counting as we go along:
        i = -1
        lowestObject = None
        lowestZ = 0
    
        # First find the lowest Z value in the object
        for object in objects:
            i += 1
            
            if i == 0:
                lowestObject = object
                lowestZ = object.location[2]
        
            else:
                if object.location[2] < lowestZ:
                    lowestObject = object
                    lowestZ = object.location[2]
                    
        location = FindMedianLocation(objects)
        location[2] = lowestZ
        
        # Now move the object
        MoveObject(sel, location)
    
    
    elif grp.origin_location is '2':
        print("Inside Number 2!")
        # Get the object with the lowest origin point
        objects = FindDummyConstraintObjects(obj.asset_name)
        
        for object in objects:
            if object.GTGrp.is_origin_point is True:
                objects.remove(object)
        
        # Iterate through the objects, counting as we go along:
        i = -1
        lowestObject = None
        lowestZ = 0
    
        # First find the lowest Z value in the object
        for object in objects:
            i += 1
            
            if i == 0:
                lowestObject = object
                lowestZ = object.location[2]
        
            else:
                if object.location[2] < lowestZ:
                    lowestObject = object
                    lowestZ = object.location[2]
        
        print(lowestObject.name)
        location = lowestObject.location
        
        # Now move the object
        MoveObjectToObject(sel, object)
        
    elif grp.origin_location is '3':
        # Get the selected object
        selEnum = int(grp.origin_object_select)
        
        count = -1
        count += 1
        
        if obj.asset_name in bpy.data.groups:
            group = bpy.data.groups[obj.asset_name]
            
            for object in group.objects:
                count += 1
                
                if selEnum == count:
                    MoveObjectToObject(sel, object)
                    
def Update_OriginSize(self, context):
    sel = context.active_object
    scn = context.scene.GTScn
    obj = sel.GTObj
    grp = sel.GTGrp
    
    # Just uses some code from the dummy update, but without some of the clutter.
    sel.empty_draw_size = grp.origin_dummy_size
    
        
def Update_XRay(self, context):
    sel = context.active_object
    scn = context.scene.GTScn
    obj = sel.GTObj
    grp = sel.GTGrp
    
    if grp.x_ray_toggle is True:
        sel.show_x_ray = True
        
    else:
        sel.show_x_ray = False
    
    
    print("Rawr")
    
    