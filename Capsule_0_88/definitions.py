import bpy, bmesh, time
from math import *

#//////////////////////// - USER INTERFACE FUNCTIONS - ////////////////////////

def GenerateVisibilityList(self, context):
    smn = context.scene.GTSmn
    scn = context.scene.GTScn
    
    smn.scene_update_toggle = True
    
    print("Generating Visibility List")
        
    HP = smn.visibility_collection.add()
    HP.name = "High-Poly"
    HP.nameIcon = 1
    HP.type = scn.visibility_HP      
        
    LP = smn.visibility_collection.add()
    LP.name = "Low-Poly"
    LP.nameIcon = 1
    LP.type = scn.visibility_LP   
        
    CG = smn.visibility_collection.add()
    CG.name = "Cage"
    CG.nameIcon = 1
    CG.type = scn.visibility_CG 
        
    CX = smn.visibility_collection.add()
    CX.name = "Collision"
    CX.nameIcon = 1
    CX.type = scn.visibility_CX 
        
    BS = smn.visibility_collection.add()
    BS.name = "Parents"
    BS.nameIcon = 2
    BS.type = scn.visibility_base   
        
    CM = smn.visibility_collection.add()
    CM.name = "Children"
    CM.nameIcon = 2
    CM.type = scn.visibility_component
    
    FZ = smn.visibility_collection.add()
    FZ.name = "Freeze"
    FZ.nameIcon = 3
    FZ.type = scn.visibility_freeze
    
    smn.scene_update_toggle = False
    smn.vis_update_toggle = True
    
    
def ClearVisibilityList(self, context):
    smn = context.scene.GTSmn

    smn.visibility_collection.clear()
    # You can also use delete, but it didn't seem to clear everything, so this makes
    # sure everything in your collection is DEAD O_O
    
def GenerateComponentList(self, context):
    mnu = context.active_object.GTMnu
    obj = context.active_object
        
    for child in obj.children:
        GTObj = child.GTObj
        
        entry = mnu.component_collection.add()
        entry.name = GTObj.component_name
        entry.type = GTObj.visibility
        
        #print(int(GTObj.visibility))
        
    context.scene.GTSmn.component_update_toggle = True


    
def ClearComponentList(self, context):
    mnu = context.object.GTMnu

    mnu.component_collection.clear()
    
def GenerateFreezeList(self, context):
    mnu = context.active_object.GTMnu
    obj = context.active_object
        
    mnu.freeze_collection.clear()
    
    i = 0
        
    for item in bpy.data.objects:  
        if obj.GTObj.base_name == item.GTObj.base_name:
            if item.GTObj.is_frozen is True:
                if item.GTObj.object_type is "1":
                    print("FOUND A FREEZE OBJECT")
                    entry = mnu.freeze_collection.add()
                    entry.name = item.GTObj.freeze_name
                    entry.type = item.GTObj.freeze_type
                    entry.view = item.GTObj.freeze_hide
                    entry.index = i
                    item.GTObj.freeze_index = i
                    
                    i += 1
                
    context.scene.GTSmn.component_update_toggle = True
    
def ClearFreezeList(self, context):
    mnu = context.active_object.GTMnu
    
    mnu.freeze_collection.clear()
    

#//////////////////////// - GENERAL FUNCTIONS - ////////////////////////
            
def GenerateObjectShading(target, scn):
    
    obj = target.GTObj
    
    #Focus the object to ensure the values can be accessed at this stage if its hidden or unselectable.
    FocusObject(target )
    
    # First check that the visibility category that matches the object's type is
    # defined as object settings
    stageType = '1'
    objectType = '1'
    
    if int(obj.asset_type) is 1:
        stageType = scn.visibility_HP
    elif int(obj.asset_type) is 2:
        stageType = scn.visibility_LP
    elif int(obj.asset_type) is 3:
        stageType = scn.visibility_CG
    elif int(obj.asset_type) is 4:
        stageType = scn.visibility_CX
    
    if int(obj.object_type) is 1:
        objectType = scn.visibility_base
    elif int(obj.object_type) is 2:
        objectType = scn.visibility_component
        
    # If the object is frozen, we've got some other options to employ!
    if obj.is_frozen is True:
        
        target.hide_select = False
        
        if obj.freeze_hide is True:
            print("Starting to shade")
            type = scn.visibility_freeze
        
            if int(type) is 2:
                ShadeNormal(target) 
            elif int(type) is 3:
                ShadeBoxBounds(target)
            elif int(type) is 4:
                ShadeWireframe(target)
            elif int(type) is 5:
                ShadeWire(target)
            elif int(type) is 6:
                print("Hiding Frozen")
                ShadeHide(target)
        
        else:
            print("Freeze view is false, hiding")
            ShadeHide(target)
        
        target.hide_select = True
    
    # Now check to see whether either of them isnt 1.
    # If both of them arent 1, stage type takes precedent over object type
    elif int(stageType) != 1 and int(objectType) != 1 or int(stageType) != 1:
        
        #print("Shading stage type 1")
        
        if int(stageType) is 2:
            ShadeNormal(target) 
        elif int(stageType) is 3:
            ShadeBoxBounds(target)
        elif int(stageType) is 4:
            ShadeWireframe(target)
        elif int(stageType) is 5:
            ShadeWire(target)
        elif int(stageType) is 6:
            ShadeHide(target)
    
    elif int(objectType) != 1:
        
        #print("Shading stage type 2")
        
        if int(objectType) is 2:
            ShadeNormal(target) 
        elif int(objectType) is 3:
            ShadeBoxBounds(target)
        elif int(objectType) is 4:
            ShadeWireframe(target)
        elif int(objectType) is 5:
            ShadeWire(target)
        elif int(objectType) is 6:
            ShadeHide(target)
    
    # If were here, both object and stage types equal one, and we will use the object-defined vis settings
    else:
        type = obj.visibility
        
        #print("Shading object defined")
        
        if int(type) is 1:
            ShadeNormal(target)
        elif int(type) is 2:
            ShadeBoxBounds(target)
        elif int(type) is 3:
            ShadeWireframe(target)
        elif int(type) is 4:
            ShadeWire(target)
        elif int(type) is 5:
            ShadeHide(target)
            

#The top one kind of acts like a shading reset, the others perform more nuanced shading.
def ShadeNormal(target):
    #print("Shading Normal")
    FocusObject(target)
    target.draw_type = "TEXTURED"
    target.show_wire = False
    target.show_x_ray = False
    target.hide = False
    bpy.types.SpaceView3D.view_selected = "SOLID"
    
def ShadeBoxBounds(target):
    #print("Shading Box Bounds")
    ShadeNormal(target)
    target.draw_type = "BOUNDS"
    
def ShadeWireframe(target):
    #print("Shading Wireframe")
    ShadeNormal(target)
    target.draw_type = "WIRE"
    
def ShadeWire(target):
    #print("Shading Wire")
    ShadeNormal(target)
    target.show_wire = True
    
def ShadeTexture(target):
    #print("Shading Texture")
    ShadeNormal(target)
    bpy.types.SpaceView3D.view_selected = "TEXTURED"
    
def ShadeHide(target):
    #print("Hiding Object")
    ShadeNormal(target)
    target.hide = True
    
def SolidifyGroupShade(groupName):
    # For every object in the group, set it's shading to Solid
    if groupName in bpy.data.groups:
        group = bpy.data.groups[groupName]
        
        for object in group.objects:
            ShadeNormal(object)
    
def DefaultGroupShade(groupName, scn):
    
    # For every object in the group, call GenerateObjectShading
    if groupName in bpy.data.groups:
        group = bpy.data.groups[groupName]
        
        for object in group.objects:
            GenerateObjectShading(object, scn)
    
        
def FocusObject(target):
    
    # If the target isnt visible, MAKE IT FUCKING VISIBLE.
    if target.hide is True:
        target.hide = False
        
    if target.hide_select is True:
        target.hide_select = False
    
    #### Select and make target active
    bpy.ops.object.select_all(action='DESELECT')  
    bpy.context.scene.objects.active = bpy.data.objects[target.name]
    bpy.ops.object.select_pattern(pattern=target.name) 
    
def SelectObject(target):
    
    # If the target isnt visible, MAKE IT FUCKING VISIBLE.
    if target.hide is True:
        target.hide = False
        
    if target.hide_select is True:
        target.hide_select = False
    
    target.select = True
    
def ActivateObject(target):
    
    # If the target isnt visible, MAKE IT FUCKING VISIBLE.
    if target.hide is True:
        target.hide = False
        
    if target.hide_select is True:
        target.hide_select = False
    
    bpy.context.scene.objects.active = bpy.data.objects[target.name]
    
    
def DuplicateObject(target, targetLocation):
    
    #### Select and make target active
    bpy.ops.object.select_all(action='DESELECT')  
    bpy.context.scene.objects.active = bpy.data.objects[target.name]
    bpy.ops.object.select_pattern(pattern=target.name)
    
    # Duplicate the object
    bpy.ops.object.duplicate_move()
    
    # Now switch the active object to the duplicate
    duplicate = bpy.context.active_object
    
    # Now set the transform details
    duplicate.rotation_euler = target.rotation_euler
    duplicate.rotation_axis_angle = target.rotation_axis_angle
    
    # To preserve the scale, it has to be applied.  Sorreh!
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    
def MergeObject(target):
    
    # Ensure all modifiers on the stack are applied
    for modifier in target.modifiers:
        
        # First find if the modifier has a object
        print("GTMerge - Found modifier in base, applying")
        modObject = FindObjectInModifier(modifier)
        
        bpy.ops.object.select_all(action = 'DESELECT')
        SelectObject(base)
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
        
        # If it does, delete the object after applying the mod
        if modObject != None:
            print("GTMerge - Found object to delete.  BAI")
            FocusObject(modObject)
            bpy.ops.object.delete(use_global = False)
    
    if len(target.children) is not 0:    
        for child in target.children:
        
            print("GTMerge - Found modifier in component, applying")
            FocusObject(child)
        
            for modifier in child.modifiers:
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
        
    
    # Now select all the components
    for child in target.children:
        SelectObject(child)
    
    # Now make the base object active
    bpy.ops.object.select_pattern(pattern=target.name) 
    bpy.context.scene.objects.active = bpy.data.objects[target.name]
    
    # Now JOIN!
    bpy.ops.object.join()


def DeleteObject(target):
    
    # This needs proper data deletion, and all delete operations need to use this
    FocusObject(target)
    bpy.ops.object.delete()
    
    # Currently removing just in case...
    DeleteObjectByMemory(target)  
    
def DeleteObjectByMemory(target):
    
    try:
        ob = bpy.data.objects[target.name]
    
    except:
        ob = None
    
    if ob != None:
        ob.user_clear()
        bpy.data.objects.remove(ob) 
        
    return
    
def MoveObject(target, location):
    # Preserving the objects location has to happen again, e_e
    cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
    previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]
    
    # Move the cursor to the location
    bpy.data.scenes[bpy.context.scene.name].cursor_location = location
    
    # Focus the object
    FocusObject(target)
    
    # SNAP IT
    bpy.ops.view3D.snap_selected_to_cursor()
    
    # Restore the location
    bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc
    
def MoveObjectToObject(target, locationTarget):
    
    # Preserving the objects location has to happen again, e_e
    cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
    previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]

    # Focus the object
    FocusObject(locationTarget)
    bpy.ops.view3D.snap_cursor_to_selected()

    # SNAP IT
    FocusObject(target)
    bpy.ops.view3D.snap_selected_to_cursor()

    # Restore the location
    bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc
    
    
def AddToGroup(target, groupName):
    
    print("---Inside AddToGroup---")
    
    # Find and add the object to the group, and ensure everything runs smoothly
    if groupName in bpy.data.groups:
        print("O - Found the group in AddToGroup")
        
        group = bpy.data.groups[groupName]
        #print("Setting to group:")
        #print(group.name)
        
        for object in group.objects:
            print(object.name)
        
        # This is used to understand whether the component is alone, or whether 
        # as a base, if another base exists within the object
        if len(group.objects) is not 0:
            target.GTGrp.is_own_group = False
            
        else:
            target.GTGrp.is_own_group = True
            
        group.objects.link(target)
        
        
        
        if len(target.children) is not 0:
            for child in target.children:
                group = bpy.data.groups[groupName]
                group.objects.link(child)
        
        print("X - Exiting AddToGroup")
        return
        
    # Otherwise create a new group
    print("O - Creating new group")
    FocusObject(target)
    bpy.ops.group.create(name=groupName)
    group = bpy.data.groups[groupName]
    #group.objects.link(target)
    
    if len(target.children) is not 0:
        for child in target.children:
            FocusObject(child)
            group.objects.link(child)
            
    print("X - Exiting AddToGroup")
            
def AddToExistingGroup(target, destination):
    
    print("---Inside AddToExistingGroup---")
    
    groupName = destination.GTObj.asset_name
    
    # Find the group object specified
    if groupName in bpy.data.groups:
        print("O - Found group specified")
        group = bpy.data.groups[groupName]
        group.objects.link(target)
        
        if len(target.children) is not 0:
            for child in target.children:
                group.objects.link(child)
         
    else:
        print("! - Found no existing object")
        return False
            
def AddToNewGroup(target, groupName, increment):
    # This is exclusively for singular objects exiting groups or base parenting, that need
    # a group not inhabited by another object
    print("---Inside AddToNewGroup---")
    
    # Find the group object specified
    if groupName in bpy.data.groups:
        print("O - Found group specified")
        group = bpy.data.groups[groupName]
        
        #Now see if there are any objects in it
        if len(group.objects) is not 0:
            
            print("! - Group has objects, incrementing...")
            #If there is, increment the name and attempt adding again
            newGroupName = groupName + "0" + str(increment + 1)
            AddToNewGroup(target, newGroupName, increment + 1)
            
            return
          
        # If not, move in!  
        else:
            print("O - Group has no objects, adding...")
            group.objects.link(target)
            target.GTGrp.is_own_group = True
            
            if len(target.children) is not 0:
                for child in target.children:
                    group.objects.link(child)
            
            target.GTObj.old_asset_name = groupName
            target.GTObj.asset_name = groupName
            
            return
        
        return
        
    else:
        # Otherwise create a new group
        print("O - Creating new group")
        bpy.ops.group.create(name=groupName)
        group = bpy.data.groups[groupName]
        
        target.GTGrp.is_own_group = True
    
        if len(target.children) is not 0:
            #group.objects.link(target)
            for child in target.children:
                #group = bpy.data.groups[groupName]
                group.objects.link(child)
                
        # This is called after all objects are assigned, as it renames everything in the group
        target.GTObj.old_asset_name = groupName
        target.GTObj.asset_name = groupName
        
        print("# - New Asset Name:")
        print(target.GTObj.asset_name)
            
        return
        
def AddToMultiGroup(target, destination):
    
    print("---Inside AddToMultiGroup---")
    
    groupName = destination.GTObj.asset_name
    
    # Find and add the object to the group, and ensure everything runs smoothly
    # This adds extra functionality for if the object being joined has only one object
    if groupName in bpy.data.groups:
        print("O - Found the group in AddToGroup")
        
        group = bpy.data.groups[groupName]
        
        hasGroup = 0
        
        print("? - Counting number of objects in group that have a group")   
        # This is used to create a dummy object if only two main objects inhabit this 
        for object in group.objects:
            if object.GTGrp.has_group_object is True:
                hasGroup += 1
        
        print("# - hasGroup Total")   
        print(hasGroup)
        # If no objects in the group have a group, we need to set one up.    
        # Find the object that is it's own object and set it up there.
        alreadyDone = False
        
        if hasGroup == 0:
            print("? - No objects found, searching")   
            for object in group.objects:
                if alreadyDone == False:
                    if object.GTGrp.is_own_group is True:
                        print("> - Setting up Dummy")   
                    
                        # Create the dummy! owo
                        alreadyDone = True
                        CreateGroupDummy(object.GTObj.asset_name, '1')
                    
                        object.GTGrp.is_own_group = False
                        object.GTGrp.has_group_object = True
                    
                        AttachToDummy(object)
                    
                        if len(object.children) is not 0:
                            for child in object.children:
                                child.GTGrp.has_group_object = True


        print("> - Linking object to found group")      
        group.objects.link(target)
        target.GTGrp.is_own_group = False
        target.GTGrp.has_group_object = True
        
        target.GTObj.old_asset_name = groupName
        target.GTObj.asset_name = groupName
        
        if len(target.children) is not 0:
            for child in target.children:
                print("> - Linking children to found group")   
                #group = bpy.data.groups[groupName]
                group.objects.link(child)
                child.GTGrp.has_group_object = True
                child.GTObj.old_asset_name = groupName
                child.GTObj.asset_name = groupName
                
        AttachToDummy(target)
        
        print("X - Exiting AddToMultiGroup")
        
        return
        
    # Otherwise create a new group
    print("O - Creating new group")
    bpy.ops.group.create(name=groupName)
    group = bpy.data.groups[groupName]
    #group.objects.link(target)
    
    CreateGroupDummy(target.GTObj.asset_name, '1')
    target.GTGrp.has_group_object = True
    
    if len(target.children) is not 0:
        group.objects.link(target)
        
        for child in target.children:
            child.GTGrp.has_group_object = True
            #group.objects.link(child)
            
    print("X - Exiting AddToMultiGroup")
    
def FindInGroup(targetName, groupName):
    print("Rawr")
    
    # Find the object in the group, return a boolean as to whether it was found or not
    if groupName in bpy.data.groups:
        print("GroupName Found")
        group = bpy.data.groups[groupName]
        
        if target.name in group.objects:
            return True
            
        else:
            return False
        
    else:
        return False
        
    
def RemoveFromAllGroups(target):
    
    print("Inside Remove From All Groups")
    FocusObject(target)
    bpy.ops.group.objects_remove_all()
    
    if len(target.children) is not 0:
        for child in target.children:
            FocusObject(child)
            bpy.ops.group.objects_remove_all()
            
    # Temporary code to try and delete ghost objects
    # Doesn't currently work, exclude for now
    #if target.GTObj.asset_name in bpy.data.groups:
        #group = bpy.data.groups[target.GTObj.asset_name]
        
        #if len(group.objects) == 0:
            #bpy.ops.group.delete(target.GTObj.asset_name)
                
def SwitchToExistingGroup(target, destination):
    
    obj = target.GTObj
    grp = target.GTGrp
    oldAsset = obj.assetName
    FocusObject(target)
    
    print("---Inside SwitchToNewAsset---")
    
    # -------- FAILSAFES ------------
    if destination is None:
        print("! - HEY!  You didnt specify a destination!")
        return False
        
    if target is None:
        print("! - HEY!  You didnt specify a target!")
        return False
    
    # First off, if the target and destination are identical, tell the caller to fuck off.
    if target.name == destination.name:
        print("! - The target and destination are the same, fuck off o_o")
        return False
   
    # -------- DETACH ------------     
    # Now thats checked, remove the target from any group it was in
    RemoveFromAllGroups(target)
    
    # -------- PREPARATION ------------    
    # If this object has a parent, cut the ambilical cord
    if target.parent is not None:
        print("! - The target has a parent, cutting ambilical...")
        parent = target.parent
        ClearParent(target)
    
    # Now if this object was in a group previously, detach it from any dummy
    if grp.has_group_object is True:
        DetachFromDummy(target)
        grp.has_group_object = False
       
        # If a parent is flying, assign tags to the children
        if sel(target.children) is not 0:
            for child in target.children:
                child.GTGrp.has_group_object = False
                GenerateName(child)
            
    # -------- SWITCH ------------   
    AddToGroup(target, destination)
    
    # -------- CUSTOMS -----------
    CheckAsset(oldAsset)
    
    # Do a quick check to ensure this object is alone   
    obj.object_type = '1'
    
    GenerateName(target)
    
    return True
    
def SwitchToNewAsset(target, newAssetName):
    
    obj = target.GTObj
    grp = target.GTGrp
    oldAsset = obj.asset_name
    FocusObject(target)
    
    print("---Inside SwitchToNewAsset---")
    
    # -------- FAILSAFES ------------
    if target is None:
        print("! - HEY!  You didnt specify a target!")
        return False
        
    if newAssetName is "" or newAssetName is "None":
        print("! - HEY!  You didnt specify a proper asset name!")
        return False
   
    # -------- DETACH ------------     
    # Now thats checked, remove the target from any group it was in
    RemoveFromAllGroups(target)
    
    # -------- PREPARATION ------------    
    # If this object has a parent, cut the ambilical cord
    if target.parent is not None:
        print("! - The target has a parent, cutting ambilical...")
        parent = target.parent
        ClearParent(target)
    
    # Now if this object was in a group previously, detach it from any dummy
    if grp.has_group_object is True:
        DetachFromDummy(target)
        grp.has_group_object = False
       
        # If a parent is flying, assign tags to the children
        if len(target.children) is not 0:
            for child in target.children:
                child.GTGrp.has_group_object = False
                GenerateName(child)
            
    # -------- SWITCH ------------   
    AddToNewGroup(target, newAssetName, 0)
    
    # -------- CUSTOMS -----------
    CheckAsset(oldAsset)
    
    # Finally ensure the object is 'top-level', now it's alone     
    obj.object_type = '1'
    
    GenerateName(target)
    
    return True
    
def SwitchToGroupAsset(target, destination):
    
    obj = target.GTObj
    grp = target.GTGrp
    oldAsset = obj.asset_name
    oldObjectType = '1'
    FocusObject(target)
    
    print("---Inside SwitchToNewAsset---")
    
    # -------- FAILSAFES ------------
    if destination is None:
        print("! - HEY!  You didnt specify a destination!")
        return False
        
    if target is None:
        print("! - HEY!  You didnt specify a target!")
        return False
    
    # First off, if the target and destination are identical, tell the caller to fuck off.
    if target.name == destination.name:
        print("! - The target and destination are the same, fuck off o_o")
        return False
        
    # Additionally, if the object selected has any children for some reason, it cant be further
    # parented.    
    #if len(target.children) is not 0:
        #print("! - The target is already a parent, you cant currently parent a parent :/")
        #return False
        
    # -------- DETACH ------------     
    # Now thats checked, remove the target from any group it was in
    RemoveFromAllGroups(target)
   
    # -------- PREPARATION ------------    
    # If this object has a parent, cut the ambilical cord
    if target.parent is not None:
         print("! - The target has a parent, cutting ambilical...")
         parent = target.parent
         ClearParent(target)
   
    # Now if this object was in a group previously, detach it from any dummy
    if grp.has_group_object is True:
        DetachFromDummy(target)
        grp.has_group_object = False
           
    # -------- FLIGHT ------------   
    AddToMultiGroup(target, destination)
   
    # -------- CUSTOMS -----------
    # Ensure the target name doesn't clash with any other object name inside the group
    print("? - Checking the same base name isnt in the group:")
    if target.GTObj.object_type is '1':
        target.GTObj.base_name = target.GTObj.base_name
       
    else:
        target.GTObj.component_name = target.GTObj.component_name
   
    # Check the previously left asset to see if anything needs to be done
    CheckAsset(oldAsset)
   
    GenerateName(target)
   
    return True     
    
def SwitchToParentAsset(target, destination):
    
    obj = target.GTObj
    grp = target.GTGrp
    oldAsset = obj.asset_name
    oldObjectType = '1'
    FocusObject(target)
    
    print("---Inside SwitchToParentAsset---")
    
    # -------- FAILSAFES ------------
    if destination is None:
        print("! - HEY!  You didnt specify a destination!")
        return False
        
    if target is None:
        print("! - HEY!  You didnt specify a target!")
        return False
    
    # First off, if the target and destination are identical, tell the caller to fuck off.
    if target.name == destination.name:
        print("! - The target and destination are the same, fuck off o_o")
        return False
        
    # Additionally, if the object selected has any children for some reason, it cant be further
    # parented.    
    if len(target.children) is not 0:
        print("! - The target is already a parent, you cant currently parent a parent :/")
        return False
   
    # -------- DETACH ------------     
    # Now thats checked, remove the target from any group it was in
    RemoveFromAllGroups(target)
    
    # -------- PREPARATION ------------    
    # If this object has a parent, cut the ambilical cord
    # Also track whether the object was parented or not
    if target.parent is not None:
        print("! - The target has a parent, cutting ambilical...")
        parent = target.parent
        ClearParent(target)
        oldObjectType = '2'
        
    else:
        oldObjectType = '1'
    
    # Now if this object was in a group previously, detach it from any dummy
    if grp.has_group_object is True:
        DetachFromDummy(target)
        grp.has_group_object = False
            
    # -------- FLIGHT ------------   
    AddParent(target, destination)
    AddToExistingGroup(target, destination)
    
    # -------- CUSTOMS -----------
    # Make sure it's set to now have it's own group
    grp.is_own_group = False
    
    # If the object's new parent has a group, this object needs it to be added
    if target.parent.GTGrp.has_group_object is True:
        AttachToDummy(target)
        grp.has_group_object = True
        target.GTObj.old_asset_name = target.parent.GTObj.asset_name
        target.GTObj.asset_name = target.parent.GTObj.asset_name
    
    # Check the previously left asset to see if anything needs to be done
    CheckAsset(oldAsset)
    
    # Finally set the object as being a parent of another object 
    obj.old_object_type = oldObjectType
    obj.object_type = '2'
    
    GenerateName(target)
    GenerateName(destination)
    
    return True
    
def DetachParent(target):
    
    # So basically, all of the things from SwitchToNewAsset, without any of the parent or group detaching.
    obj = target.GTObj
    grp = target.GTGrp
    FocusObject(target)
    
    print("---Inside DetachParent---")
    
    # -------- FAILSAFES ------------
    if target is None:
        print("! - HEY!  You didnt specify a target!")
        return False

    if target.parent is None:
        print("! - HEY!  This asset doesn't have a parent, fuck off!")
        return False
        
    parent = target.parent
        
    # *sigh* , have to do this the hard way
    # First detach the parent from the dummy
    if grp.has_group_object is True:
        DetachFromDummy(target.parent)
    
    # NOW WE CAN CLEAR THE PARENT
    ClearParent(target)
    
    # Now if this object was in a group previously, attach it to the dummy
    if grp.has_group_object is True:
        AttachToDummy(target)
        grp.has_group_object = True
    
    # Used to ensure it doesnt increment anything when the child leaves the parent
    obj.update_toggle = True
    obj.base_name = "None"
    
    GenerateName(target)    
    AttachToDummy(parent)
    
    # Finally ensure the object is 'top-level', now it's alone     
    obj.object_type = '1'
    
    
    
    return True
    
    
def CheckAsset(groupName):
    
    # This function tries to refresh any settings for groups that have been edited, but are not
    # the focus of an operator
    
    # This code checks whether there's a multi-base asset
    # There may be an issue with this code as SwitchAsset is used by components as well as base objects they belong to.
    print("-"*40)
    print("---Inside CheckAsset---")
    print(groupName)
    
    if groupName in bpy.data.groups:
        group = bpy.data.groups[groupName]
        baseCount = 0
        compCount = 0
        hasGroup = 0
        finalCount = 0
        baseObject = None
        
        if len(group.objects) is not 0:
            for object in group.objects:
                if object.GTObj.object_type is '1':
                    if object.GTGrp.is_group_object is False and object.GTGrp.is_origin_point is False:
                        print(object.name)
                        baseObject = object
                        baseCount += 1
                        
                # If the object has no parent, we can determine it as having an attachment to the dummy
                elif object.parent is None:
                    print(object.name)
                    compCount += 1
                
                # If the group we left has a group object, count it up    
                if object.GTGrp.has_group_object is True:
                    print(object.name)
                    hasGroup += 1
                    
            finalCount = baseCount + compCount
            print("# - Final Count = ")
            print(finalCount)
            print("# - Has Group = ")
            print(finalCount)
            
            if finalCount == 1 or hasGroup == 1:
                print("! - The group only has one base or component, delete the dummy!")
                print("# - The group with one base or component is.....")
                print(group.name)
                emptyObject = None
                originObject = None
                normalObjects = []
                
                # Preserving the objects location has to happen again, e_e
                cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
                previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]
                
                # Sort through the objects we have to catch the empties and store the normal objects
                for object in group.objects:
                    if object.GTGrp.is_origin_point is True:
                        originObject = object
                    elif object.GTGrp.is_group_object is True:
                        emptyObject = object
                        
                    else:
                        normalObjects.append(object)
                        
                # If we didn't find an empty or origin object, we cant continue as theres
                # nothing to do.        
                if emptyObject is None or originObject is None:
                    return
                
                # Delete the empty objects, ensuring that normal objects are detached first   
                if originObject is not None:
                    DeleteObject(originObject)
                    
                if emptyObject is not None:
                    for object in normalObjects:
                        DetachFromDummy(object)
                        
                    DeleteObject(emptyObject) 
                
                # Now move the normal object out of the asset
                # We need to figure out if theres only one top-level object or not (AKA, the group
                # dissolved due to a parenting operation)
                
                multipleObjects = False
                
                if len(normalObjects) > 1:
                    multipleObjects = True
                
                for object in normalObjects:    
                    
                    if object.GTObj.object_type is '1':
                        print("> - Base found, switching to new asset")
                        print(object.name)
                        print(object.GTObj.base_name)
                        SwitchToNewAsset(object, object.GTObj.component_name)
                        
                    elif multipleObjects is True:
                        if object.parent is not None:
                            print("> - Child found, doing nothing")
                            
                    elif multipleObjects is False:
                        print("> - Component found, switching to new asset")
                        SwitchToNewAsset(object, object.GTObj.component_name)
                        
                        
                # Restore the cursor location a final time
                bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc
                        
                        
    print("-"*40)
                        
# Checks the name to see if anything is wrong, and fixes any issues with it.
def GenerateName(object):
    
    # New naming paradigm, component name is now the default name.
    #print("---Inside GenerateName---")
    
    if object.GTGrp.is_group_object is True:
        assetName = object.GTObj.asset_name
        object.name = assetName + "Dummy"
        return None
        
    elif object.GTGrp.is_origin_point is True:
        assetName = object.GTObj.asset_name
        object.name = assetName + "Origin"
        return None
        
    else:
        # Gather the object names
        stageEx = FindAssetTypeName(object)
    
        assetName = ""
        assetEx = ""
        if object.GTGrp.has_group_object is True:
            assetName = object.GTObj.asset_name
            assetEx = "_"
    
        baseName = ""
        baseEx = ""
        if object.GTObj.base_name != "None" or object.GTObj.base_name != "":
            if object.parent is not None:
                #print("> - Generating Parent Name")
                #print(object.GTObj.base_name)
                baseName = object.GTObj.base_name
                baseEx = "_"
    
        compName = ""
        compEx = ""
        if object.GTObj.component_name != "None" or object.GTObj.component_name != "":
            #print("> - Generating Object Name")
            #print(object.GTObj.component_name)
            compName = object.GTObj.component_name
            compEx = "_"
    
        freezeEx = ""    
        if object.GTObj.is_frozen is True:
            freezeEx = "_FZ"
        
        object.name = assetName + assetEx + baseName + baseEx + compName + compEx + stageEx + freezeEx
    
        return None
        
def CheckGroupName(target, name, increment):
    
    print("---Inside CheckGroupName---")
    print("# - Target:")
    print(target.name)
    print("# - Name Being Searched:")
    print(name)
    
    # This definition ensures the name currently set for the object group isn't taken by another group.
    
    if name in bpy.data.groups:
        print("! - Found group object")
        
        group = bpy.data.groups[name]
        
        print("# - Group name =")
        print(group.name)
        
        for object in group.objects:
            if object.name == target.name:
                print("> - We are in the group found, no need to change")
                return name
        
        #Now see if there are any objects in it
        if len(group.objects) >= 1:
            if group.objects[0].name != target.name:
                print("! - Group has objects, incrementing")
            
                #If there is, increment the name and attempt adding again
                newName = name + "0" + str(increment + 1)
                finalName = CheckGroupName(target, newName, (increment + 1))
            
                return finalName
            
        print("> - Group has no objects, leaving")
        # Othewrwise return the new name
            
        return name
        
    return name
    
def CheckObjectName(target, name, increment):
    
    obj = target.GTObj
    grp = target.GTGrp
    objects = []
    
    print("---Inside CheckObjectName---")
    print("# - Name to be searched for:")
    print(name)
    print(target.name)
    
    # This definition ensures the name currently set for the component isn't taken by another component in the same group.
    
    if obj.asset_name in bpy.data.groups:
        group = bpy.data.groups[obj.asset_name]
        
        print("# - Group name =")
        print(group.name)
        
        objects = FindDummyConstraintObjects(obj.asset_name)
        
        if target.parent is not None:
            for object in objects:
                if target.parent.name == object.name:
                    print("> - Group has no matches, leaving")
                    return name
                        
        for object in objects:
            print("# - Searching Object:")
            print(object.name)
            if object.GTObj.component_name == name or object.GTObj.base_name == name:
                print("! - Same component name")
                if object.name != target.name:
                    print("! - Identical Name Found, Incrementing...")
                    print("# - Object Name Found = ")
                    print(object.name)
                
                    #If there is, increment the name and attempt adding again
                    newName = name + "0" + str(increment + 1)
                    finalName = CheckObjectName(target, newName, (increment + 1))
                    
                    # In case the object being checked is already in the same group as the
                    # object found, the name need regenerating to avoid overlap
                    GenerateName(object)
            
                    return finalName
                
            
        print("> - Group has no matches, leaving")
        return name
        
    return name
    
def FindAssetTypeName(object):
    
    # Obtains the right asset type extension for the object.
    # Make a temp variable
    assetEx = "Temp"
    
    # Find the asset extension it needs
    if int(object.GTObj.asset_type) is 1:
        assetEx = "HP"
    if int(object.GTObj.asset_type) is 2:
        assetEx = "LP"  
    if int(object.GTObj.asset_type) is 3:
        assetEx = "CG"  
    if int(object.GTObj.asset_type) is 4:
        assetEx = "CX"  
    if int(object.GTObj.asset_type) is 5:
        assetEx = "SM"  
        
    return assetEx

    
def AddParent(child, parent):
    
    # I now have to add the cursor stuff here too, just in case...
    cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
    previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]
    FocusObject(child)
    bpy.ops.view3D.snap_cursor_to_selected()
    
    bpy.ops.object.select_all(action='DESELECT')
                
    SelectObject(parent)
    SelectObject(child)
                
    bpy.context.scene.objects.active = parent 
                
    bpy.ops.object.parent_set()
    
    # Now move the object
    FocusObject(child)
    bpy.ops.view3D.snap_selected_to_cursor()
    bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc
        

def ClearParent(child):
    # Prepare the 3D cursor so it can keep the object in it's current location
    # After it stops being a component
    cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
    previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]
    
    # Save the transform matrix before de-parenting
    matrixcopy = child.matrix_world.copy()
        
    # Move the cursor to the selected object
    FocusObject(child)
    bpy.ops.view3D.snap_cursor_to_selected()
    
    # Clear the parent
    bpy.ops.object.select_all(action='DESELECT')
    SelectObject(child)
    bpy.ops.object.parent_clear()
    
    # Now move the object
    bpy.ops.view3D.snap_selected_to_cursor()
    
    # Restore the original cursor location and matrix
    bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc
    child.matrix_world = matrixcopy
    
    
#This is used for searching through modifiers to find objects in them!
def SearchModifiers(target):
    
    object_list = []
    
    mod_types = {'ARRAY', 'BOOLEAN', 'MIRROR', 'SCREW', 'ARMATURE', 'CAST', 'CURVE', 'HOOK', 'LATTICE', 'MESH_DEFORM', 'SHRINKWRAP', 'SIMPLE_DEFORM', 'WARP', 'WAVE'}
        
    # This is used to define all modifiers that share the same object location
    mod_normal_types = {'BOOLEAN', 'SCREW', 'ARMATURE', 'CAST', 'CURVE', 'HOOK', 'LATTICE', 'MESH_DEFORM'}
        
    #Finds all the components in the object through modifiers that use objects
    for modifier in target.modifiers:
        
        print("GTFIND - Modifiers Found")
        if modifier.type in mod_types:
            print("GTFIND - Right Type Found")
                
            #Normal Object Types
            if modifier.type in mod_normal_types:
                print("GTFIND - Normal Object Found")
                if modifier.object is not None:
                    object_list.append(modifier.object)
                    
                    # If the modifier is a boolean, it should really have a specific default visibility option :P
                    if modifier.type  == 'BOOLEAN':
                        modifier.object.GTObj.visibility = '3'
        
            #Array
            elif modifier.type == 'ARRAY':
                if modifier.start_cap is not None:
                    object_list.append(modifier.start_cap)
    
            #Mirror
            elif modifier.type == 'MIRROR':
                print("GTFIND - Mirror Found")
                if modifier.mirror_object is not None:
                    object_list.append(modifier.mirror_object)
        
            #Shrinkwrap
            elif modifier.type == 'SHRINKWRAP':
                print("GTFIND - Boolean Found")
                if modifier.target is not None:
                    object_list.append(modifier.target)
        
            #Simple Deform
            elif modifier.type == 'SIMPLE_DEFORM':
                print("GTFIND - Boolean Found")
                if modifier.origin is not None:
                    object_list.append(modifier.origin)
        
            #Warp
            elif modifier.type == 'WARP':
                print("GTFIND - Boolean Found")
                if modifier.object_from is not None:
                    object_list.append(modifier.object_from)
                elif modifier.object_to is not None:
                    object_list.append(modifier.object_to)
    
            #Wave
            elif modifier.type == 'WAVE':
                print("GTFIND - Boolean Found")
                if modifier.start_position_object is not None:
                    object_list.append(modifier.start_position_object)
    
    
    return object_list

#This is used for searching through modifiers to find objects in them!
def FindObjectInModifier(modifier):
    
    return_object = None
    
    mod_types = {'ARRAY', 'BOOLEAN', 'MIRROR', 'SCREW', 'ARMATURE', 'CAST', 'CURVE', 'HOOK', 'LATTICE', 'MESH_DEFORM', 'SHRINKWRAP', 'SIMPLE_DEFORM', 'WARP', 'WAVE'}
        
    # This is used to define all modifiers that share the same object location
    mod_normal_types = {'BOOLEAN', 'SCREW', 'ARMATURE', 'CAST', 'CURVE', 'HOOK', 'LATTICE', 'MESH_DEFORM'}
        
    if modifier.type in mod_types:
        print("GTFIND - Right Type Found")
            
        #Normal Object Types
        if modifier.type in mod_normal_types:
            print("GTFIND - Boolean Found")
            if modifier.object is not None:
                return_object = modifier.object
        
        #Array
        elif modifier.type == 'ARRAY':
            if modifier.start_cap is not None:
                return_object = modifier.start_cap
    
        #Mirror
        elif modifier.type == 'MIRROR':
            print("GTFIND - Mirror Found")
            if modifier.mirror_object is not None:
                return_object = modifier.mirror_object
        
        #Shrinkwrap
        elif modifier.type == 'SHRINKWRAP':
            print("GTFIND - Boolean Found")
            if modifier.target is not None:
                return_object = modifier.target
        
        #Simple Deform
        elif modifier.type == 'SIMPLE_DEFORM':
            print("GTFIND - Boolean Found")
            if modifier.origin is not None:
                return_object = modifier.origin
        
        #Warp
        elif modifier.type == 'WARP':
            print("GTFIND - Boolean Found")
            if modifier.object_from is not None:
                return_object = modifier.object_from
            elif modifier.object_to is not None:
                return_object = modifier.object_to
    
        #Wave
        elif modifier.type == 'WAVE':
            print("GTFIND - Boolean Found")
            if modifier.start_position_object is not None:
                return_object = modifier.start_position_object
    
    print(return_object)
    return return_object
    
    
def LockTransform(objectName):
    
    bpy.data.objects[objectName].lock_location[0] = True
    bpy.data.objects[objectName].lock_location[1] = True
    bpy.data.objects[objectName].lock_location[2] = True
    
    bpy.data.objects[objectName].lock_rotation[0] = True
    bpy.data.objects[objectName].lock_rotation[1] = True
    bpy.data.objects[objectName].lock_rotation[2] = True
    
    bpy.data.objects[objectName].lock_scale[0] = True
    bpy.data.objects[objectName].lock_scale[1] = True
    bpy.data.objects[objectName].lock_scale[2] = True
    
def UnlockTransform(objectName):
    
    bpy.data.objects[objectName].lock_location[0] = False
    bpy.data.objects[objectName].lock_location[1] = False
    bpy.data.objects[objectName].lock_location[2] = False
    
    bpy.data.objects[objectName].lock_rotation[0] = False
    bpy.data.objects[objectName].lock_rotation[1] = False
    bpy.data.objects[objectName].lock_rotation[2] = False
    
    bpy.data.objects[objectName].lock_scale[0] = False
    bpy.data.objects[objectName].lock_scale[1] = False
    bpy.data.objects[objectName].lock_scale[2] = False
    
def FindHighestLocation(objects):
    
    print("Rawr")
    
    # Iterate through the objects, counting as we go along:
    i = -1
    highestZ = 0
    
    # First find the lowest Z value in the object
    for object in objects:
        i += 1
        
        if i == 0:
            highestZ = object.location[2]
        
        else:
            if object.location[2] > highestZ:
                highestZ = object.location[2]
    
    return highestZ
    
def FindLowestLocation(objects):
    
    # Iterate through the objects, counting as we go along:
    i = -1
    lowestZ = 0
    
    # First find the lowest Z value in the object
    for object in objects:
        i += 1
        
        if i == 0:
            lowestZ = object.location[2]
        
        else:
            if object.location[2] < lowestZ:
                lowestZ = object.location[2]
    
    return lowestZ
    
def FindMedianLocation(objects):
    
    print("Rawr")
    
    xTotal = 0
    yTotal = 0
    zTotal = 0
    count = 0
    
    # Iterate through the objects, counting as we go along:
    for object in objects:
        count += 1
        xTotal += object.location[0]
        yTotal += object.location[1]
        zTotal += object.location[2]
        
    # Now divide each value by the count
    xFinal = xTotal / count
    yFinal = yTotal / count
    zFinal = zTotal / count
    
    return [xFinal, yFinal, zFinal]
    
def CreateGroupDummy(groupName, dummyEnum):
    
    # Gather objects for placing the dummy location
    objects = FindDummyConstraintObjects(groupName)
            
    # Save the current cursor location
    cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
    previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]
            
    # Find the median point in the group objects
    dummyLocation = FindMedianLocation(objects)
    
    # Position the cursor to the location
    bpy.data.scenes[bpy.context.scene.name].cursor_location = dummyLocation
    
    # Generate the Group Dummy
    dummy = GenerateGroupDummy(dummyEnum)
    dummy.GTObj.old_asset_name = groupName
    dummy.GTObj.asset_name = groupName
    dummy.GTObj.is_GT_asset = True
    dummy.GTGrp.is_group_object = True
    
    # Lock scale and rotation
    bpy.data.objects[dummy.name].lock_rotation[0] = True
    bpy.data.objects[dummy.name].lock_rotation[1] = True
    bpy.data.objects[dummy.name].lock_rotation[2] = True
    
    bpy.data.objects[dummy.name].lock_scale[0] = True
    bpy.data.objects[dummy.name].lock_scale[1] = True
    bpy.data.objects[dummy.name].lock_scale[2] = True
    
    FocusObject(dummy)
    
    # Assign it to the group
    AddToGroup(dummy, groupName)
    
    # Position the cursor back to it's original location
    bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc
    
    # Generate the object name
    GenerateName(dummy)
    
    # Generate the origin
    GenerateOrigin(groupName)
    
    # Refocus the dummy
    FocusObject(dummy)
    
    
def GenerateGroupDummy(dummyEnum):
    
    bpy.ops.object.select_all(action='DESELECT')  
    bpy.ops.object.add(type='EMPTY')
    obj =  bpy.context.scene.objects.active
    
    if int(dummyEnum) is 1:
        obj.empty_draw_type = 'PLAIN_AXES'
        
    elif int(dummyEnum) is 2:
        obj.empty_draw_type = 'SINGLE_ARROW'
    
    elif int(dummyEnum) is 3:
        obj.empty_draw_type = 'CIRCLE'
        
    elif int(dummyEnum) is 4:
        obj.empty_draw_type = 'CUBE'
        
    elif int(dummyEnum) is 5:
        obj.empty_draw_type = 'CONE'
    
    return obj
    
def AttachToDummy(target):
    
    for constraint in target.constraints:
        #print("Found a constraint")
        if constraint.name == "Group Location":
            #print("The object already has the constraint, leaving...")
            return None
    
    #print("---Inside AttachToDummy---")
    #print("# - Target Object:")
    #print(target.name)
    dummy = None
    groupName = target.GTObj.asset_name
    
    # First find the dummy
    if groupName in bpy.data.groups:
        #print("O - GroupName Found")
        group = bpy.data.groups[groupName]
        
        for object in group.objects:
            #print(object.name)
            if object.GTGrp.is_group_object is True:
                #print("Dummy Found")
                dummy = object
                    
    if dummy is None:
        #print("Returning False")
        return None
        
    # Save the current cursor location
    cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
    previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]
    
    FocusObject(target)
    bpy.ops.view3D.snap_cursor_to_selected()
    
    # Add the child of constraint
    bpy.ops.object.constraint_add(type="CHILD_OF")
    constraint = target.constraints[0].name = "Group Location"
    target.constraints["Group Location"].target = dummy
    
    SelectObject(target)
    bpy.ops.view3D.snap_selected_to_cursor(use_offset=False)
    
    # Restore the cursor location a final time
    bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc
    
    #print("X - Exiting AttachToDummy")
    
def DetachFromDummy(target):
    
    #print("---Inside DetachFromDummy---")
    
    for constraint in target.constraints:
        #print("Found a constraint")
        if constraint.name == "Group Location":
            continue
        else:
            return None
            
    #print("O - Detaching dummy")
    groupName = target.GTObj.asset_name
    
    # Save the current cursor location
    cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
    previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]
    
    FocusObject(target)
    bpy.ops.view3D.snap_cursor_to_selected()
    
    for constraint in target.constraints:
        if constraint.name == "Group Location":
            target.constraints.remove(constraint)
            
    SelectObject(target)
    bpy.ops.view3D.snap_selected_to_cursor(use_offset=False)
    
    bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc
    
    #print("X - Exiting DetachFromDummy")
    
def UpdateDummyLocation(groupName, scene):
    
    # Allows the user to set the location of the dummy object
    empties = []
    empties = FindEmptyObjects(groupName)
    
    sel = empties[0]
    obj = sel.GTObj
    scn = scene.GTScn
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
    
def FindDummyConstraintObjects(groupName):
    
    objects = []
    
    # First gather all the objects in the group, minus the dummy
    if groupName in bpy.data.groups:
        group = bpy.data.groups[groupName]
        
        for object in group.objects:
            if object.GTGrp.is_group_object is False and object.GTGrp.is_origin_point is False:
                if object.GTObj.object_type == '1':
                    #print("Adding object")
                    #print(object.name)
                    objects.append(object)
                
                elif object.GTObj.object_type == '2':
                    if object.parent is None:
                        #print("Adding object")
                        #print(object.name)
                        objects.append(object)
    
    return objects
    
def FindEmptyObjects(groupName):
    
    objects = []
    emptyObject = None
    originObject = None
    
    # Get the group
    if groupName in bpy.data.groups:
        group = bpy.data.groups[groupName]
        
        for object in group.objects:
            if object.GTGrp.is_group_object is True:
                emptyObject = object
                
            elif object.GTGrp.is_origin_point is True:
                originObject = object
                
    # Now append them in order
    objects.append(emptyObject)
    objects.append(originObject)
    
    return objects
            
def GenerateOrigin(groupName):
    
    #Get the lowest point for the object group
    objects = FindDummyConstraintObjects(groupName)
    ZLocation = FindLowestLocation(objects)
    location = FindMedianLocation(objects)
    
    location[2] = ZLocation
    
    # Save the current cursor location and relocate it to a new position
    cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
    previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]
    
    bpy.data.scenes[bpy.context.scene.name].cursor_location = location
    
    # Generate the Origin Point
    bpy.ops.object.select_all(action='DESELECT')  
    bpy.ops.object.add(type='EMPTY')
    origin =  bpy.context.scene.objects.active
    origin.empty_draw_type = 'SPHERE'
    
    origin.GTGrp.is_origin_point = True
    origin.GTObj.old_asset_name = groupName
    origin.GTObj.asset_name = groupName
    origin.GTObj.is_GT_asset = True
    
    # Lock scale and rotation
    bpy.data.objects[origin.name].lock_rotation[0] = True
    bpy.data.objects[origin.name].lock_rotation[1] = True
    bpy.data.objects[origin.name].lock_rotation[2] = True
    
    AddToGroup(origin, groupName)
    AttachToDummy(origin)
    
def GenerateGroupPlinth(dummyEnum): 
    
    return None 
    
def SwitchStage(target):
    
    return None
    
def ChangeStageGroup(target, oldGroup, newGroup):
    
    return None
    
def ChangeStageComponentName(target):
    
    return None
    
def ChangeStageBaseName(target):
    
    return None

def ChangeStageAssetName(target):
    
    return None

def SetObjectOrigin(object, enum, context):
    
    print("Inside ASKETCH_SetObjectOrigin")
        
    # Set to Object Base
    if enum == 1:
        print("Setting to COM")
        
        # Enter the object!
        object_data = bpy.context.object.data
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.editmode_toggle()
        
        #Setup the correct tools to select vertices
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        sel_mode = context.tool_settings.mesh_select_mode
        context.tool_settings.mesh_select_mode = [True, False, False]
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        
        i = -1
        lowestZ = 0
        
        # First find the lowest Z value in the object
        for vertex in object_data.vertices:
            i += 1
            print (i)
            
            # Used to define a reference point for the first vertex, in case 0 is
            # lower than any vertex on the model.
            if i == 0:
                lowestZ = vertex.co.z
            
            else:
                if vertex.co.z < lowestZ:
                    lowestZ = vertex.co.z
        
        # Now select all vertices with lowestZ
        
        for vertex in object_data.vertices:
            if vertex.co.z == lowestZ:
                vertex.select = True
                print("Vertex Selected!")

        #Restore previous settings
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        context.tool_settings.mesh_select_mode = sel_mode
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                  
        
        # Saves the current cursor location
        cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
        previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]
        
        # Snap the cursor
        bpy.ops.object.editmode_toggle()
        bpy.ops.view3D.snap_cursor_to_selected()
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.editmode_toggle()
        
        # Set the origin
        FocusObject(object)
        bpy.ops.object.origin_set(type ='ORIGIN_CURSOR')
        
        # Restore the original cursor location
        bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc
        
    # Set to Absolute Lowest
    elif enum == 2:
        # Enter the object!
        object_data = bpy.context.object.data
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.editmode_toggle()
        
        #Setup the correct tools to select vertices
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        sel_mode = context.tool_settings.mesh_select_mode
        context.tool_settings.mesh_select_mode = [True, False, False]
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        
        i = -1
        lowestZ = 0
        
        # First find the lowest Z value in the object
        for vertex in object_data.vertices:
            i += 1
            print (i)
            
            # This code converts vertex coordinates from object space to world space.
            vertexWorld = object.matrix_world * vertex.co
            
            # Used to define a reference point for the first vertex, in case 0 is
            # lower than any vertex on the model.
            if i == 0:
                lowestZ = vertexWorld.z
            
            else:
                if vertexWorld.z < lowestZ:
                    lowestZ = vertexWorld.z
        
        # Now select all vertices with lowestZ
        
        for vertex in object_data.vertices:
            vertexWorld = object.matrix_world * vertex.co
            
            if vertexWorld.z == lowestZ:
                vertex.select = True
                print("Vertex Selected!")

        #Restore previous settings
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        context.tool_settings.mesh_select_mode = sel_mode
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                  
        
        # Saves the current cursor location
        cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
        previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]
        
        # Snap the cursor
        bpy.ops.object.editmode_toggle()
        bpy.ops.view3D.snap_cursor_to_selected()
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.editmode_toggle()
        
        # Set the origin
        FocusObject(object)
        bpy.ops.object.origin_set(type ='ORIGIN_CURSOR')
        
        # Restore the original cursor location
        bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc
                
    # Set to COM
    elif enum == 3:
        print("Setting to COM")
        
        # Set the origin
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        
    elif enum == 4:
        print("Setting to Vertex Group")
        
        # Enter the object!
        object_data = bpy.context.object.data
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.editmode_toggle()
        
        #Setup the correct tools to select vertices
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        sel_mode = context.tool_settings.mesh_select_mode
        context.tool_settings.mesh_select_mode = [True, False, False]
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        
        index = int(bpy.context.active_object.GTMnu.vertex_groups) - 1
        
        #Search through all vertices in the object to find the ones belonging to the
        #Selected vertex group
        for vertex in object_data.vertices:
            for group in vertex.groups:
                if group.group == index:
                    vertex.select = True
                    print("Vertex Selected!")
                    
        #Restore previous settings
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        context.tool_settings.mesh_select_mode = sel_mode
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                  
        
        # Saves the current cursor location
        cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
        previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]
        
        # Snap the cursor
        bpy.ops.object.editmode_toggle()
        bpy.ops.view3D.snap_cursor_to_selected()
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.editmode_toggle()
        
        # Set the origin
        FocusObject(object)
        bpy.ops.object.origin_set(type ='ORIGIN_CURSOR')
        
        # Restore the original cursor location
        bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc
        
def FindFreezeObject(target, index):
    
    # Inside the group, find an object with a matching name and a freeze tag
    groupName = target.GTObj.asset_name
    
    if groupName in bpy.data.groups:
        group = bpy.data.groups[groupName]
        
        for object in group.objects:
            if object.GTObj.base_name == target.GTObj.base_name:
                if object.GTObj.is_frozen is True:
                    if object.GTObj.freeze_index == index:
                        print("O - Object found, returning...")
                        return object
                        
    return None
                
            
    