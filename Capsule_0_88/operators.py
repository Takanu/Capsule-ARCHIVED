from .definitions import GenerateObjectShading, ShadeNormal, ShadeBoxBounds, ShadeWireframe, ShadeWire, ShadeTexture, ShadeHide, SolidifyGroupShade, DefaultGroupShade, FocusObject, SelectObject, ActivateObject, DuplicateObject, MergeObject, DeleteObject, MoveObject, AddToGroup, FindInGroup, RemoveFromAllGroups, SwitchToExistingGroup, SwitchToNewAsset, SwitchToGroupAsset, SwitchToParentAsset, DetachParent, CheckAsset, GenerateName, CheckObjectName, FindAssetTypeName, AddParent, ClearParent, SearchModifiers, FindObjectInModifier, LockTransform, UnlockTransform, CreateGroupDummy, AttachToDummy, FindDummyConstraintObjects, AttachToDummy, DetachFromDummy, UpdateDummyLocation

from .definitions import GenerateVisibilityList, ClearVisibilityList, GenerateComponentList, ClearComponentList, GenerateFreezeList, ClearFreezeList

from .update import Update_ObjectOrigin

import bpy, bmesh, time
from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty
from math import *

#//////////////////////// - BASIC OPERATORS - ////////////////////////

class GT_Blank_Report(bpy.types.Operator):
    bl_idname = "object.gt_blank_report"
    bl_label = "Rawr"
    
    def execute(self, context):
        
        self.report({'WARNING'}, 
        'Please choose a name for the object.')
        return {'FINISHED'}
        
        
    
class GT_Name_Report(bpy.types.Operator):
    bl_idname = "object.gt_name_report"
    bl_label = ""
    
    def execute(self, context):
        
        self.report({'WARNING'}, 
        'You cant have None as a name, smartass O_O')
        return {'FINISHED'}

    
class GT_Update_Origin(bpy.types.Operator):
    """Updates the origin point based on the option selected, for all selected objects"""
    
    bl_idname = "object.gt_update_origin"
    bl_label = ""
    
    def execute(self, context):
        print(self)
        
        for sel in context.selected_objects:
        
            Update_ObjectOrigin(sel, context)
        
        # DefaultGroupShade has to happen in the update.
        
        return {'FINISHED'}
    
class GT_Assign_Base(bpy.types.Operator):
    """Assigns the object to an existing base."""
    
    bl_idname = "object.gt_assign_base"
    bl_label = "Assign to Base"
    
    def __init__(self):
        print("Start moving")
 
    def __del__(self):
        print("Rawr, im done now")

    def modal(self,context,event):
        # If escape is pressed, exit
        if event.type == 'ESC':
            return {'FINISHED'}
         
        if event.type == 'RET':
            return {'FINISHED'}

        # When an object is selected, set it as a child to the object, and finish.
        if event.type == 'TIMER':
            print('TIMER')
            
            # ALSO, check its not a dummy or origin object
            if context.scene.objects.active.GTGrp.is_origin_point is True or context.scene.objects.active.GTGrp.is_group_object is True:
                self.report({'WARNING'}, 
                'The object selected is a origin point or dummy object, and YOU CANT DO THAT O_O')
                FocusObject(self.childObj)
                return {'FINISHED'}
            
            if context.scene.objects.active is not None: 
                
                if context.scene.objects.active.name != self.childObj.name:
                    
                    # Also check that it's a GT asset.
                    if context.scene.objects.active.GTObj.is_GT_asset is True:
                        
                        if context.scene.objects.active.GTObj.object_type is '1':
                            
                            scn = context.scene.GTScn
                
                            # Lets set the component
                            print("new object found")
                            self.parentObj = context.scene.objects.active
                            print(self.childObj)
                            print(self.parentObj)
                            SwitchToParentAsset(self.childObj, self.parentObj)
                            
                            # Use Default Shading to ensure object shading is reset.
                            DefaultGroupShade(self.parentObj.GTObj.asset_name, scn)
                        
                            # Keep the original object selected as we exit.
                            FocusObject(self.childObj)
                            
                            return {'FINISHED'}
                            
                        else:
                            FocusObject(self.childObj)
                            self.report({'WARNING'}, 
                            'The object selected isnt a base.')
                            return {'FINISHED'}
                    
                    # Otherwise throw a warning :D
                    else:
                        self.report({'WARNING'}, 
                        'The object selected isnt a GT Object.')
                        return {'FINISHED'}
                        
                
        return {'PASS_THROUGH'}
    
    
    def execute(self, context):
        print("invoke!")
        print("Is this new?")
        
        # Deselect all objects, then go into the modal loop
        self.childObj = context.scene.objects.active
        print(self.childObj.name)
        print(context.scene.objects.active.name)
        
        # Add the modal handler and LETS GO!
        context.window_manager.modal_handler_add(self)
        
        # Add a timer to enable a search for a selected object
        self._timer = context.window_manager.event_timer_add(0.5, context.window)
        
        return {'RUNNING_MODAL'}
    
class GT_Remove_From_Base(bpy.types.Operator):
    """Detaches the child from the parent it currently belongs to."""
    
    bl_idname = "object.gt_remove_base"
    bl_label = "Detach from Parent"
    
    @classmethod
    def poll(cls, context):
        
        fail_test = True
        
        if len(context.selected_objects) > 1:
            fail_test = False
        
        return fail_test
    
    def execute(self, context):
        print(self)
        
        #Simply removes the component from the base
        sel = context.active_object
        grp = sel.GTGrp
        scn = context.scene.GTScn
        
        
        if grp.has_group_object is True:
            DetachParent(sel)
        
        else:
            SwitchToNewAsset(sel, sel.GTObj.component_name)
        
        # Use Default Shading to ensure object shading is reset.
        DefaultGroupShade(sel.GTObj.asset_name, scn)
        
        FocusObject(sel)
        
        return {'FINISHED'}

    
class GT_Select_Parent(bpy.types.Operator):
    """Selects the parent object"""
    
    bl_idname = "object.gt_select_parent"
    bl_label = "Select Parent"
    
    @classmethod
    def poll(cls, context):
        
        fail_test = True
        
        if len(context.selected_objects) > 1:
            fail_test = False
            
        if context.active_object.parent is None:
            fail_test = False
        
        return fail_test
    
    def execute(self, context):
        
        # And the award for simplest operator goes tooooo....
        sel = context.active_object
        
        FocusObject(sel.parent)
        
        return {'FINISHED'}
        
class GT_Select_Base(bpy.types.Operator):
    """Selects all the objects within a parent/child relationship"""
    
    bl_idname = "object.gt_select_base"
    bl_label = "Select All"
    
    def execute(self, context):
        
        print("---Inside GT_Select_Base---")
        
        sel = context.active_object
        scn = context.scene.GTScn
        parents = []
        children = []
        selection = []
        operators = []
        
        # First sort out all selected objects based on whether they are parents or children
        for object in context.selected_objects:
            print("> - Found selected object")
            if object.GTObj.object_type is '2':
                if object.parent is not None:
                    print("> - Adding Child to List")
                    children.append(object)
                    
            elif len(object.children) is not 0:
                print("> - Adding Parent to List")
                parents.append(object)
                
            else:
                selection.append(object)
                
        # Now try to match them together to remove the appearance of duplicate parent/child relationships
        # Find the parents of children selected, and if their parent is already in the list, remove them
        for child in children:
            for parent in parents:
                if child.parent.name == parent.name:
                    children.remove(child)
                    
        bpy.ops.object.select_all(action='DESELECT')  
            
        # Now you can select them! :D
        for parent in parents:
            print("> - Selecting Parent")
            SelectObject(parent)
            
            for child in parent.children:
                SelectObject(child)
                
        for child in children:
            print("> - Selecting Child")
            SelectObject(child.parent)
            
            for otherChild in child.parent.children:
                SelectObject(otherChild)
                
        for object in selection:
            SelectObject(object)
            
        ActivateObject(sel)
        
        return {'FINISHED'}
        
class GT_Create_New_Asset(bpy.types.Operator):
    """Assigns the object as a new Capsule asset.  This is required to use this object with the Capsule plugin."""
    
    bl_idname = "object.gt_new_asset"
    bl_label = "Create New Asset"
    
    def execute(self, context):
        print(self)
        
        obj = context.active_object
        scn = context.scene
        GTScn = scn.GTScn
        
        #If a correct enum hasnt been chosen, BYEBYE
        if int(scn.GTScn.new_asset_select) is 1:
            self.report({'WARNING'}, 
            'Please select the asset and object type!.')
            return {'FINISHED'}
        
        
        #If no name is found, LATERS
        if scn.GTScn.new_object_name == "":
            self.report({'WARNING'}, 
            'Please choose a name for the object.')
            return {'FINISHED'}
        
        if scn.GTScn.new_object_name == "None":
            self.report({'WARNING'}, 
            'Please choose a name for the object.')
            return {'FINISHED'}
        
        print("Creating New Object")
        print("-"*40)
        
        print("GTCREATE - Generating Object")
        obj.GTObj.component_name = scn.GTScn.new_object_name
        obj.GTObj.update_toggle = True
        obj.GTObj.base_name = "None"
        
        # Create the group
        bpy.ops.group.create(name=scn.GTScn.new_object_name)
        obj.GTObj.asset_name = scn.GTScn.new_object_name
        obj.GTGrp.is_own_group = True    
        
        print("GTCREATE - Assigning asset type")
        obj.GTObj.asset_type = str(int(scn.GTScn.new_asset_select) - 1) 
        obj.GTObj.old_object_type = '1'
        obj.GTObj.object_type = '1'
        
        #Reset the enums
        scn.GTScn.new_asset_select = "1"
        scn.GTScn.new_object_name = "None"
        
        #Setup the naming convention!
        GenerateName(obj)
        
        #Tick the object as now being in the system!
        obj.GTObj.is_GT_asset = True
        
        # Use Default Shading to ensure the object is shaded with the global settings, if any
        DefaultGroupShade(obj.GTObj.asset_name, GTScn)
        
        return {'FINISHED'}
    
class GT_Find_Components(bpy.types.Operator):
    """Finds and adds children to the selected object through target objects used in the modifier stack.  This is not recommended if youre utilising many object-centric modifiers, and don't want all of them to be a child of the selected object"""
    
    bl_idname = "object.gt_find_components"
    bl_label = "Find Children"
    
    @classmethod
    def poll(cls, context):
        
        fail_test = True
        
        if len(context.selected_objects) > 1:
            fail_test = False
        
        return fail_test
    
    def execute(self, context):
        print(self)
        
        print("GTFIND - Inside Find_Components")
        
        sel = context.active_object
        scn = context.scene.GTScn
        search_results = []
        
        search_results = SearchModifiers(sel)
        
        for result in search_results:
            
            # Check it's a GT Asset first.
            if result.GTObj.is_GT_asset is True:
                SwitchToParentAsset(result, sel)
                    
        FocusObject(sel)
        
        # Use Default Shading to ensure the object is shaded with the global settings, if any
        DefaultGroupShade(sel.GTObj.asset_name, scn)
        
        return {'FINISHED'}
    
class GT_Add_Components(bpy.types.Operator):
    """Once pressed, select the objects you want to attach to the active object as children.  Press enter when finished."""
    
    bl_idname = "object.gt_add_components"
    bl_label = "Add Children"
    
    @classmethod
    def poll(cls, context):
        
        fail_test = True
        
        if len(context.selected_objects) > 1:
            fail_test = False
        
        return fail_test
    
    def __init__(self):
        print("Start moving")
 
    def __del__(self):
        print("Rawr, im done now")

    def modal(self,context,event):
        # If escape is pressed, exit
        if event.type in {'ESC'}:
            print("Escape worked")
            return {'FINISHED'}
             
        if event.type in {'RET'}:
            print("Enter worked")
            scn = context.scene.GTScn
            
            for obj in context.selected_objects:
                error = False
                if obj.name != self.parentObj.name:
                    error = SwitchToParentAsset(obj, self.parentObj)
                    
                    if error == False:
                        self.report({'WARNING'}, 
                        'Something went wrong inside SwitchToParentAsset, please contact the creator for support >.>')
                        FocusObject(self.parentObj)
                        return {'FINISHED'}
                    
            # Use Default Shading to ensure object shading is reset.
            DefaultGroupShade(self.parentObj.GTObj.asset_name, scn)
                        
            # Keep the original object selected as we exit.
            FocusObject(self.parentObj)
            GenerateName(self.parentObj)
            
            return {'FINISHED'}

        # When an object is selected, set it as a child to the object, and finish.
        elif event.type == 'TIMER':
            print('TIMER')
            
            # ALSO, check its not a dummy or origin object
            if context.scene.objects.active.GTGrp.is_origin_point is True or context.scene.objects.active.GTGrp.is_group_object is True:
                self.report({'WARNING'}, 
                'The object selected is a origin point or dummy object, and YOU CANT DO THAT O_O')
                FocusObject(self.parentObj)
                return {'FINISHED'}
            
            if context.scene.objects.active is not None: 
                if context.scene.objects.active.name != self.parentObj.name:
                    
                    # Also check that it's a GT asset.
                    if context.scene.objects.active.GTObj.is_GT_asset is True:
                        
                        # ALSOALSO check its not a base object with children.
                        if len(context.scene.objects.active.children) == 0:
                        
                            # ALSO check were not already parented to it.
                            print("new object found")
                            self.childObj = context.scene.objects.active
                        
                            if self.childObj.parent is None:
                
                                print("new object found")
                                
                                # Select the object instead of add it to a list
                                # This is to easily prevent duplicates
                                SelectObject(self.childObj)
                                SelectObject(self.parentObj)
                                ActivateObject(self.parentObj)
                                #self.objList.append(context.scene.objects.active)
                                #FocusObject(self.parentObj)
                        
                            elif self.childObj.parent.name != self.parentObj.name:
                            
                                # Lets set the component
                                print("new object found")
                                #self.objList.append(context.scene.objects.active)
                                SelectObject(self.childObj)
                                SelectObject(self.parentObj)
                                ActivateObject(self.parentObj)
                                #FocusObject(self.parentObj)
                        
                            else:
                                self.report({'WARNING'}, 
                                'The object selected is already a component to this base object.')
                                FocusObject(self.parentObj)
                                return {'FINISHED'}
                        else:
                            self.report({'WARNING'}, 
                            'The object selected is a base object with components, no can do!')
                            FocusObject(self.parentObj)
                            return {'FINISHED'}
                    
                    # Otherwise throw a warning :D
                    else:
                        self.report({'WARNING'}, 
                        'The object selected isnt a GT Object.')
                        FocusObject(self.parentObj)
                        return {'FINISHED'}
                        
                
        return {'PASS_THROUGH'}
    
    
    def execute(self, context):
        print("invoke!")
        print("Is this new?")
        
        # Deselect all objects, then go into the modal loop
        self.parentObj = context.scene.objects.active
        print(self.parentObj.name)
        print(context.scene.objects.active.name)
        
        # Add the modal handler and LETS GO!
        context.window_manager.modal_handler_add(self)
        
        # Add a timer to enable a search for a selected object
        self._timer = context.window_manager.event_timer_add(0.5, context.window)
        
        return {'RUNNING_MODAL'}
    
    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
        return {'FINISHED'}
    
class GT_Delete_Base(bpy.types.Operator):
    """Deletes the selected objects."""
    
    bl_idname = "object.gt_delete_base"
    bl_label = "Delete"
    
    def execute(self, context):
        print(self)
        
        selected_objects = []
        
        for sel in context.selected_objects:
            
            if sel.GTGrp.is_group_object is True or sel.GTGrp.is_origin_point is True:
                self.report({'WARNING'}, 
                'You cant select a dummy or origin object for the Delete operation.')
                return {'FINISHED'}
            
            selected_objects.append(sel)
            
        for sel in selected_objects:
        
            scn = context.scene.GTScn
            obj = sel.GTObj
            assetName = sel.GTObj.asset_name
            children = []
            selType = '1'
        
            # If there are any children, de-parent them to ensure they stay in the same place when the object is deleted
            
            if obj.object_type is '1':
                if len(sel.children) is not 0:
                    for child in sel.children:
                        print("Removing Child")
                        print(child.name)
                        SwitchToNewAsset(child, child.GTObj.component_name)
                    
                # Now delete the object
                DeleteObject(sel)
            
                # Reshade every child that is hidden manually.
                DefaultGroupShade(assetName, scn)
                CheckAsset(assetName)
                
                bpy.ops.object.select_all(action = 'DESELECT')
                
            else:
                # Now delete the object
                DeleteObject(sel)
            
                # Reshade every child that is hidden manually.
                DefaultGroupShade(assetName, scn)
                CheckAsset(assetName)
                
                bpy.ops.object.select_all(action = 'DESELECT')
                
        
        return {'FINISHED'}
        
class GT_Remove_Components(bpy.types.Operator):
    """Removes all children attached to the selected parent"""
    
    bl_idname = "object.gt_remove_components"
    bl_label = "Remove All Children"
    
    @classmethod
    def poll(cls, context):
        
        fail_test = True
        
        if len(context.selected_objects) > 1:
            fail_test = False
        
        for sel in context.selected_objects:
            if len(sel.children) == 0:
                fail_test = False
        
        return fail_test
    
    def execute(self, context):
        sel = context.active_object
        scn = context.scene.GTScn
        
        print(self)
        
        #Filters through the object's parents, and removes them as components one by one!
        
        if len(sel.children) == 0:
            self.report({'WARNING'}, 
            'This base has no children, stop wasting my time... >_>')
            return {'FINISHED'}
        
        for child in sel.children:
            
            # Focuses the object to ensure the object type update changes
            # the right object.
            FocusObject(child)
            SwitchToNewAsset(child, child.GTObj.component_name)
            
        # Use Default Shading to ensure object shading is reset.
        DefaultGroupShade(sel.GTObj.asset_name, scn)
        GenerateName(sel)
        FocusObject(sel)
        
        return {'FINISHED'}

    
class GT_Duplicate_Base(bpy.types.Operator):
    """Duplicates the selected object.  MODE 1 - If one object with children is selected, it will duplicate both the parent and children.  MODE 2 - Selecting just children of a parent when duplicated will keep those duplicates parented.  MODE 3 - Any other selection mix will cause the duplicates to be seperated from any parent relations, unless a parent and at least one of it's children are selected."""
    
    bl_idname = "object.gt_duplicate_base"
    bl_label = "Duplicate"
    
    #@classmethod
    #def poll(cls, context):
        
        #fail_test = True
        
        #if len(context.selected_objects) > 1:
            #fail_test = False
        
        #return fail_test
    
    def execute(self, context):
        print(self)
        
        if len(context.selected_objects) > 0:
            
            # Now every object will be treated individually
            
            objects = []
            parents = []
            groups = []
            children = []
            
            
            for object in context.selected_objects:
                
                if object.GTGrp.is_group_object is True or object.GTGrp.is_origin_point is True:
                    self.report({'WARNING'}, 
                    'You cant select a dummy or origin object for the Duplicate operation.')
                    return {'FINISHED'}
                
                objects.append(object)
                
                if len(object.children) is not 0:
                    parents.append(object)
                    
                if object.parent is not None:
                    children.append(object)
                    
                    
            # Simply duplicate all selected objects, and check and generate their names.
            bpy.ops.object.duplicate_move()
            
            sel = context.active_object
            newObjects = []
            
            for object in context.selected_objects:
                newObjects.append(object)
                
                
            bpy.ops.object.select_all(action='DESELECT')  
            
            # Its not that simple, actually (to say this function is simple however is stupid >.>)
            # If all the selected objects are children, and all of them have the same parent, keep them parented.
            if len(children) == len(objects):
                
                for object in newObjects:
                    FocusObject(object)
                    newName = CheckObjectName(object, object.GTObj.component_name + "Dup", 0)
                    object.GTObj.component_name = newName
            
            else:    
                for object in newObjects:
                    newName = ""
                    nameSet = False
                    FocusObject(object)
                    
                    if object.GTGrp.has_group_object is False:
                        SwitchToNewAsset(object, object.GTObj.component_name)
                        object.GTObj.component_name = object.GTObj.asset_name
                        
                    elif object.parent is not None:
                        if object.parent not in newObjects:
                            print("> - Parent not in the object list, taking extra precautions")
                            parent = object.parent
                            parentName = object.parent.GTObj.component_name
                            print(parentName)
                        
                            DetachParent(object)
                        
                            newName = CheckObjectName(object, object.GTObj.component_name + "Dup", 0)
                            object.GTObj.old_asset_name = newName
                            object.GTObj.asset_name = newName
                            parent.GTObj.component_name = parentName
                            object.GTObj.component_name = newName
                        
                        else:
                            print("> - Parent is in the object list, taking no extra action")
                            newName = CheckObjectName(object, object.GTObj.component_name, 0)
                            object.GTObj.component_name = newName
                       
                    elif len(object.children) is 0:
                        print("> - This object has kids! D:")
                        newName = CheckObjectName(object, object.GTObj.component_name + "Dup", 0)
                        object.GTObj.component_name = newName
                    
                    else:
                        print("> - No parent, no children, no nothing.  Take no extra action")
                        newName = CheckObjectName(object, object.GTObj.component_name + "Dup", 0)
                        object.GTObj.component_name = newName
                        
                        
            # This is to ensure the naming of objects inside the groups were about to duplicate from is refreshed, to avoid incrementation issues
            for object in newObjects:
                if object.GTGrp.has_group_object is True:
                
                    if object.GTObj.asset_name in bpy.data.groups:
                        group = bpy.data.groups[object.GTObj.asset_name]
                
                        if object.GTObj.asset_name not in group:
                            groups.append(object)
                
            #Refresh naming for the source objects
            for object in objects:
                GenerateName(object)
            
            # Refresh naming for any group the objects currently belong in
            for groupObject in groups:
                if groupObject.GTObj.asset_name in bpy.data.groups:
                    
                    group = bpy.data.groups[groupObject.GTObj.asset_name]
                    
                    for object in group.objects:
                        GenerateName(object)
                
            bpy.ops.object.select_all(action='DESELECT')  
            
            # This needs to be done to ensure one object is active, so the origin point doesn't     screw up
            for object in newObjects: 
                SelectObject(object)
                    
            ActivateObject(sel)
                
            return {'FINISHED'}
                            
        
        elif len(context.selected_objects) == 1:
        
            # I made a ton of code when this is actually really simple
            # Select all the children
            base = context.active_object
        
            print("---Inside Duplicate_Base")
        
            for child in base.children:
                SelectObject(child)
            
                # Make the base the active object
                bpy.ops.object.select_pattern(pattern=base.name) 
                bpy.context.scene.objects.active = bpy.data.objects[base.name]
        
            # Now use the duplicate operator
            bpy.ops.object.duplicate_move()
        
            # Give the name some kind of increment
            newBase = context.active_object
            print("# - New Base Name:")
            print(newBase.name)
            
            FocusObject(newBase)
        
            if base.GTGrp.has_group_object is False:
            
                RemoveFromAllGroups(newBase)
            
                if len(newBase.children) is not 0:
                    for child in newBase.children:
                        RemoveFromAllGroups(child)  
                    
                newName = newBase.GTObj.component_name + "Dup"
            
                print("# - New Base Name:")
                print(newName)
            
                newBase.GTObj.old_asset_name = newName
                newBase.GTObj.asset_name = newName

                AddToGroup(newBase, newName) 
            
                newBase.GTObj.component_name = newName
            
                if len(newBase.children) is not 0:
                    for child in newBase.children:
                        child.GTObj.base_name = newName
                    
            else:
                newBase.GTObj.component_name = newBase.GTObj.component_name + "Dup"
        
            DefaultGroupShade(base.GTObj.asset_name, context.scene.GTScn)
            DefaultGroupShade(newBase.GTObj.asset_name, context.scene.GTScn)
        
            GenerateName(newBase)
            for child in newBase.children:
                GenerateName(child)
        
            GenerateName(base)
            for child in base.children:
                GenerateName(child)
            
            FocusObject(newBase)
        
            return {'FINISHED'}
    
    
class GT_Merge_Base(bpy.types.Operator):
    """Merges all selected objects into one object.  ALT MODE - If a single parent is selected for the merge operation, both the parent and it's children will be merged into one object."""
    
    bl_idname = "object.gt_merge_base"
    bl_label = "Merge"

    def execute(self, context):
        print(self)
        
        sel = context.active_object
        obj = sel.GTObj
        objects = []
        count = 0
        
        for object in context.selected_objects:
            
            if object.GTGrp.is_group_object is True or object.GTGrp.is_origin_point is True:
                self.report({'WARNING'}, 
                'You cant select a dummy or origin object for the Merge operation.')
                return {'FINISHED'}
            
            objects.append(object)
            print("FINALLY")
            
            if object.name != sel.name:
                count += 1
                
        print(len(objects))
            
        
        if count is 0:
            print("> - Using the single-object merge code")
            # Ensure all modifiers on the stack are applied
            for modifier in sel.modifiers:
            
                # First find if the modifier has a object
                print("GTMerge - Found modifier in base, applying")
                print(modifier.name)
                modObject = FindObjectInModifier(modifier)
            
                bpy.ops.object.select_all(action = 'DESELECT')
                FocusObject(sel)
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
            
                # If it does, delete the object after applying the mod
                if modObject != None:
                    print("GTMerge - Found object to delete.  BAI")
                    FocusObject(modObject)
                    bpy.ops.object.delete(use_global = False)
            
            # Currently this doesn't support modifier objects attached to the child, which is a must for Array Sketch support.
            for child in sel.children:
            
                print("GTMerge - Found modifier in component, applying")
                FocusObject(child)
            
                for modifier in child.modifiers:
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
            
        
            # Now select all the components
            for child in sel.children:
                SelectObject(child)
        
            # Now make the base object active
            bpy.ops.object.select_pattern(pattern=sel.name) 
            bpy.context.scene.objects.active = bpy.data.objects[sel.name]
        
            # Now JOIN!
            bpy.ops.object.join()
            
        else:
            print("> - Using the multi-object merge code")
            
            bpy.ops.object.select_all(action='DESELECT')  
            
            print("? - Finding any modifiers")
            for object in objects:
                print("? - Searching Object...")
                
                FocusObject(object)
                
                for modifier in object.modifiers:
            
                    # First find if the modifier has a object
                    print("GTMerge - Found modifier in base, applying")
                    print(modifier.name)
                    modObject = FindObjectInModifier(modifier)
            
                    bpy.ops.object.select_all(action = 'DESELECT')
                    FocusObject(object)
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
            
                    # If it does, delete the object after applying the mod
                    if modObject != None:
                        print("GTMerge - Found object to delete.  BAI")
                        FocusObject(modObject)
                        bpy.ops.object.delete(use_global = False)
                        
            bpy.ops.object.select_all(action='DESELECT')     
            
            for object in objects:
                if object.parent is not None:
                    print("! - Found parented object, removing parent")   
                    DetachParent(sel)  
                    
                elif len(object.children) is not 0:
                    for child in object.children:
                        print("! - Found modifier in child, applying")
                        FocusObject(child)
                        objects.append(child)
            
                        for modifier in child.modifiers:
                            bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
                    
            for object in objects:
                print("! - Selecting Object")   
                SelectObject(object)
                
            ActivateObject(sel)
            
            # Now JOIN!
            bpy.ops.object.join()
            
        
        # Use Default Shading to ensure object shading is reset.
        DefaultGroupShade(sel.GTObj.asset_name, context.scene.GTScn)
        
        FocusObject(sel)
                
        return {'FINISHED'}
        
class GT_Seperate_Object(bpy.types.Operator):
    
    """Seperates all selected objects from their current groups and parents."""
    
    bl_idname = "object.gt_seperate_object"
    bl_label = "Seperate"
    
    def execute(self, context):
        print(self)
        
        selected_objects = []
        
        for sel in context.selected_objects:
            
            if sel.GTGrp.is_group_object is True or sel.GTGrp.is_origin_point is True:
                self.report({'WARNING'}, 
                'You cant select a dummy or origin object for the Seperate operation.')
                return {'FINISHED'}
            
            selected_objects.append(sel)
            
        for sel in selected_objects:
            SwitchToNewAsset(sel, sel.GTObj.component_name)
            
        return {'FINISHED'}
    
class GT_Duplicate_Group(bpy.types.Operator):
    
    """Duplicates the selected group."""
    
    bl_idname = "object.gt_duplicate_group"
    bl_label = "Duplicate Group"
    
    def execute(self, context):
        print(self)
        
        return {'FINISHED'}
    
    
class GT_Freeze(bpy.types.Operator):
    
    """Stores and hides the selected objects in their current state.  This function can be used for asset versioning, as well as saving a low-poly version of an asset for later use."""
    
    bl_idname = "object.gt_freeze"
    bl_label = "Freeze Version"
        
    freeze_options = EnumProperty(
        name="",
        items=(
        ('1', 'Parent Only', 'Only freezes the parent object.'),   
        ('2', 'Parent and Children', 'Freezes both the parent and all its children.'),
        ('3', 'Merge', 'Freezes and merges the parent and its children.'),
        ),)
    
    def execute(self, context):
        print(self)

        base = context.active_object
        scn = context.scene.GTScn
        freeze_items = []
        
        # Make sure a valid freeze name is provided
        if scn.freeze_name == "None" or scn.freeze_name == "":
            self.report({'WARNING'}, 
            'Give the freeze object a valid name, no None or Blanks!')
            return {'FINISHED'}
        
        for child in base.children:
            # Give them the freeze tag and select them
            SelectObject(child)
            
        # Make the base the active object
        bpy.ops.object.select_pattern(pattern=base.name) 
        bpy.context.scene.objects.active = bpy.data.objects[base.name]
        
        # Now use the duplicate operator
        bpy.ops.object.duplicate_move()
        
        # Create a list of selected items
        for object in context.selected_objects:
            freeze_items.append(object)
            
        print("Objects to freeze:")
        print(len(freeze_items))
            
        newBase = context.active_object
        
        for object in freeze_items:
            if object.name == newBase.name:
                freeze_items.remove(newBase)
        
        print("Objects to freeze after checks:")
        print(len(freeze_items))
        
        if self.freeze_options != '3':
            print("Freeze type isnt Merge")
            
            ## Give all components the freeze!
            if self.freeze_options == '2':
                print("Freeze type is Base+Components")
                
                for object in freeze_items:
            
                    FocusObject(object)
                    
                    # Assign the object the frozen tag
                    object.GTObj.is_frozen = True
                    
                    # Ensure the object cant be further trandformed, and generate it's shading
                    LockTransform(object.name)
                    GenerateObjectShading(object, scn)
                    GenerateName(object)
                    #object.hide_select = True
            
            else:
                print("Freeze type is Base")
                for child in freeze_items:
                    SwitchToNewAsset(child, child.GTObj.component_name)
                    DeleteObject(child)
                    
            
            # Give the base object the freeze name
            newBase.GTObj.freeze_name = scn.freeze_name
            scn.freeze_name = "None"
        
            # Clear the freeze list for re-generation
            FocusObject(newBase)
            ClearFreezeList(self, context)
            newBase.GTObj.is_frozen = True
        
            # Add a location constraint to the base to ensure it continues tracking the active objects
            # location.
            FocusObject(newBase)
            bpy.ops.object.constraint_add(type="COPY_LOCATION")
            constraint = newBase.constraints[0].name = "Freeze Location"
            newBase.constraints["Freeze Location"].target = base
            bpy.ops.object.hide_view_set(unselected=False)
        
            # Generate the new shading, that will hide the objects from view.
            LockTransform(newBase.name)
            GenerateObjectShading(newBase, scn)
            GenerateName(newBase)
            #newBase.hide_select = True
            
            
        # If were here, the frozen mesh will be a merge type
        else:
            print("Freeze type is Merge")
            
            MergeObject(newBase)
            merge = context.active_object
            
            FocusObject(merge)
            ClearFreezeList(self, context)
            merge.GTObj.is_frozen = True
            merge.GTObj.freeze_name = scn.freeze_name
            scn.freeze_name = "None"
        
            FocusObject(merge)
            bpy.ops.object.constraint_add(type="COPY_LOCATION")
            constraint = merge.constraints[0].name = "Freeze Location"
            merge.constraints["Freeze Location"].target = base
            bpy.ops.object.hide_view_set(unselected=False)
        
            LockTransform(merge.name)
            GenerateObjectShading(merge, scn)
            GenerateName(merge)
            #merge.hide_select = True
            
            
        FocusObject(base)
    
        # Set the freeze type
        newBase.GTObj.freeze_type = self.freeze_options
    
        #Re-generate the Freeze List
        GenerateFreezeList(self, context)
        
        DefaultGroupShade(base.GTObj.asset_name, scn)
        
        FocusObject(base)
        
        return {'FINISHED'}

    
    
    
class GT_Multi_Freeze(bpy.types.Operator):
    
    """Stores and hides the selected objects in their current state.  This function can be used for asset versioning, as well as saving a low-poly version of an asset for later use."""
    
    freeze_options = EnumProperty(
        name="",
        items=(
        ('1', 'All Selected', 'Freezes all selected objects.'),   
        ('2', 'Active', 'Freezes only the active object.'),
        ('3', 'Merge', 'Freezes and merges all selected objects.'),
        ),)
    
    bl_idname = "object.gt_multi_freeze"
    bl_label = "Freeze Version"

    def execute(self, context):
        print(self)

        sel = context.active_object
        scn = context.scene.GTScn
        selected_items = []
        freeze_items = []
        
        # Need to keep a hold of the old objects, so their lists can be generated.
        for object in context.selected_objects:
            selected_items.append(object)
        
        # Make sure a valid freeze name is provided
        if scn.freeze_name == "None" or scn.freeze_name == "":
            self.report({'WARNING'}, 
            'Give the freeze object a valid name, no None or Blanks!')
            return {'FINISHED'}
        
        # Now use the duplicate operator
        bpy.ops.object.duplicate_move()
        
        # Create a list of selected items
        for object in context.selected_objects:
            freeze_items.append(object)
            
            
        newSel = context.active_object
        
        # Use a index to obtain the corresponding selected object
        i = 0
        
        for object in freeze_items:
            
            # Perform the operations just for the freeze object
            FocusObject(object)
            
            # Assign the object the frozen tag
            object.GTObj.is_frozen = True
            
            # Ensure the object cant be further trandformed, and generate it's shading
            LockTransform(object.name)
            GenerateObjectShading(object, scn)
            GenerateName(object)
            
            #Obtain the selected object the freeze state belongs to
            original = selected_items(i)
        
            # Clear the freeze list for re-generation
            FocusObject(original)
            ClearFreezeList(self, context)
        
            # Add a location constraint to the object to ensure it continues tracking the original objects
            # location.
            FocusObject(object)
            bpy.ops.object.constraint_add(type="COPY_LOCATION")
            constraint = object.constraints[0].name = "Freeze Location"
            object.constraints["Freeze Location"].target = original
            bpy.ops.object.hide_view_set(unselected=False)
        
            # Generate the new shading, that will hide the objects from view.
            LockTransform(object.name)
            GenerateObjectShading(object, scn)
            GenerateName(object)
            
            FocusObject(original)
    
            # Set the freeze type
            object.GTObj.freeze_type = self.freeze_options
    
            #Re-generate the Freeze List
            GenerateFreezeList(self, context)
        
            DefaultGroupShade(original.GTObj.asset_name, scn)
        
            #Increment the index
            i += 1
        
        # Finish by re-selecting the original objects    
        for object in selected_items:
            SelectObject(object)
        
        FocusObject(sel)
        
        return {'FINISHED'}
    
    
class GT_Unfreeze(bpy.types.Operator):
    
    """Unfreezes and un-hides the selected, frozen object from the list, making it usable."""
    
    bl_idname = "object.gt_unfreeze"
    bl_label = "Unfreeze Selected Version"
    
    unfreeze_options = EnumProperty(
        name="",
        items=(
        ('1', 'Replace Parent', 'Replaces the currently selected parent with the currently selected freeze state.'),   
        ('2', 'Duplicate as New', 'Adds the selected freeze state as a duplicate into the scene.'),
        ('3', 'Duplicate as Low-Poly', 'Duplicates the selected freeze state as a low-poly stage.  If a low-poly stage already exists, it must be deleted first.'),
        ),)
    
    def execute(self, context):
        print(self)
        
        return {'FINISHED'}
    
class GT_Create_Group(bpy.types.Operator):
    
    """Attach one object to another to form an asset comprising of multiple parents and/or objects.  This should be used for complex assets for which parent/child relationships don't provide enough structure."""
    
    bl_idname = "scene.gt_create_group"
    bl_label = "Create/Add To Group"
        
    def __init__(self):
        print("Start moving")
 
    def __del__(self):
        print("Rawr, im done now")

    def modal(self,context,event):
        # If escape is pressed, exit
        if event.type == 'ESC':
            return {'FINISHED'}
         
        if event.type == 'RET':
            print("Enter worked")
            scn = context.scene.GTScn
            error = False
            
            multiAssetObjects = 0
            multi_asset_objects = []
            parent_objects = []
            child_objects = []
            objects_to_process = []
            active = self.currentObj
            target = None
            
            print("*"*40)
            print("---Inside Add To Group Operator---")
            print("*"*40)
            
            print("# - Active Object:")
            print(active.name)
            
            #self.currentObj.select = False
            
            # SO, WE HAVE TO RECONFIGURE HOW THIS WORKS, YAAAAAAY
            # First, check if any selected objects are in a group of their own
            # Then we have to check that out of all selected objects, what ones that have been selected
            # are in the same group.  We only need to deal with objects that have their own group.
            
            for object in context.selected_objects:
                if object.GTGrp.has_group_object is True:
                    print("O - Found object with a group object")
                    objects_to_process.append(object)
                    multiAssetObjects += 1
                    multi_asset_objects.append(object)
                    
                # Then we have to check that out of all selected objects, what ones that have been
                # selected are in the same group.
                # objects that have their own group.    
                elif object.GTGrp.is_own_group is True:
                    print("O - Found object who is its own group")
                    objects_to_process.append(object) 
                    
                # If we dont have an object selected that is in it's own group, we need to ensure the
                # object that is the group owner is added.
                # We can assume it's a component, and add it's parent to the list
                else:
                    objects_to_process.append(object.parent)
                        
                    
            #self.currentObj.select = True
                    
            if multiAssetObjects == 1:
                print("O - One multiasset found, setting as target")
                target = multi_asset_objects[0]
                objects_to_process.remove(target)
                print(target.name)
                
            else:
                print("O - Setting Active Object as Target")
                target = active
                objects_to_process.remove(target)
                print(target.name)
                
            print("# - Target Object:")
            print(target.name)
            
            FocusObject(target)
                    
            # Now we have the objects collected, the algorithm either needs to either create a new group
            # If the current object isnt in one, or add selected objects to a group if there is.
            
            # As objects can now not be processed, the program needs to check if any have been operated on.  If so, the empty location can be updated.
            objectsProcessed = 0
            
            for object in objects_to_process:
                print(object.name)
                error = True
                
                if target.GTObj.asset_name == object.GTObj.asset_name:
                    self.report({'WARNING'}, 
                    'One of the objects selected was in the same group as another selected object. :P')
                    error = True
                
                elif target.GTObj.asset_name != object.GTObj.asset_name:
                    error = SwitchToGroupAsset(object, target)
                    objectsProcessed += 1
                
                if error == False:
                    self.report({'WARNING'}, 
                    'Something went wrong inside SwitchToParentAsset, please contact the creator for support >.>')
                    FocusObject(self.currentObj)
                    return {'FINISHED'}
                
                
            # The CreateGroupDummy setup only accounts for one object, and not the others being added to it.  UPDATE THE POSITION!
            if objectsProcessed != 0:
                
                UpdateDummyLocation(target.GTObj.asset_name, context.scene)
                
            # Use Default Shading to ensure object shading is reset.
            DefaultGroupShade(self.currentObj.GTObj.asset_name, scn)
                
            FocusObject(self.currentObj)
                
            print("*"*40)
            
            return {'FINISHED'}

        # When an object is selected, set it as a child to the object, and finish.
        if event.type == 'TIMER':
            print('TIMER')
            
            # ALSO, check its not a dummy or origin object
            if context.scene.objects.active.GTGrp.is_origin_point is True or context.scene.objects.active.GTGrp.is_group_object is True:
                self.report({'WARNING'}, 
                'The object selected is a origin point or dummy object, and YOU CANT DO THAT O_O')
                FocusObject(self.currentObj)
                return {'FINISHED'}
            
            if context.scene.objects.active is not None: 
                
                if context.scene.objects.active.name != self.currentObj.name:
                    
                    # Also check that it's a GT asset.
                    if context.scene.objects.active.GTObj.is_GT_asset is True:
                
                        # Select the object, and keep the parent active
                        self.targetObj = context.active_object
                        print("new object found")
                        print(self.currentObj)
                        print(self.targetObj)
                        
                        bpy.ops.object.select_pattern(pattern=self.currentObj.name) 
                        bpy.ops.object.select_pattern(pattern=self.targetObj.name) 
                        bpy.context.scene.objects.active = bpy.data.objects[self.currentObj.name]
                            
                    
                    # Otherwise throw a warning :D
                    else:
                        self.report({'WARNING'}, 
                        'The object selected isnt a GT Object.')
                        return {'FINISHED'}
                        
                
        return {'PASS_THROUGH'}
    
    
    def execute(self, context):
        print("invoke!")
        print("Is this new?")
        
        # Deselect all objects, then go into the modal loop
        self.currentObj = context.scene.objects.active
        
        # Add the modal handler and LETS GO!
        context.window_manager.modal_handler_add(self)
    
        # Add a timer to enable a search for a selected object
        self._timer = context.window_manager.event_timer_add(0.5, context.window)
        
        return {'RUNNING_MODAL'}
        
    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
            
        return {'FINISHED'}
        

class GT_Remove_From_Group(bpy.types.Operator):
    
    """Removes the selected from the current group.  If more than one object is selected, it will remove each object into a seperate asset.  If only one object is left in the group being operated on, it will dissolve."""
    
    bl_idname = "scene.gt_remove_from_group"
    bl_label = "Remove From Group"
    
    @classmethod
    def poll(cls, context):
        
        fail_test = True
        
        if len(context.selected_objects) > 1:
            fail_test = False
        
        for sel in context.selected_objects:
            if sel.GTGrp.has_group_object is False:
                fail_test = False
        
        return fail_test
    
    def execute(self, context):
        print(self)
        sel = context.active_object
        obj = context.active_object.GTObj
        grp = context.active_object.GTGrp
        scn = context.scene.GTScn
        oldGroup = obj.asset_name
        
        print("OBject being removed from the group:")
        print(sel.name)
        
        if grp.has_group_object is True:
            print("Object is in a group")
            
            if obj.object_type is '1':
                
                print("Removing base from group")
                # Switch the grouping
                # If the base name has the same name as the group its under, append it to avoid clashes
                SwitchToNewAsset(sel, obj.component_name)
        
                FocusObject(sel)
                
                DefaultGroupShade(oldGroup, scn)
                DefaultGroupShade(obj.asset_name, scn)
        
                FocusObject(sel)
                
                return {'FINISHED'}
            
            else:
                print("Removing component from group")
                RemoveComponent(sel)
                SwitchToNewAsset(sel, obj.component_name)
                FocusObject(sel)
                
                DefaultGroupShade(obj.asset_name, scn)
                DefaultGroupShade(oldGroup, scn)
        
                FocusObject(sel)
                
                return {'FINISHED'}
                
        
        # This is a more manual method for removing objects tied to groups that aren't multi-asset, such as duplicates created through Shift+D.    
        else:
            RemoveFromAllGroups(sel)
            
            if len(sel.children) is not 0:
                for child in sel.children:
                    RemoveFromGroup(child, obj.asset_name)  
                    
            obj.old_asset_name = obj.component_name + "Dup"
            obj.asset_name = obj.component_name + "Dup"
            
            if len(sel.children) is not 0:
                for child in sel.children:
                    child.GTObj.old_asset_name = child.GTObj.component_name + "Dup"
                    child.GTObj.asset_name = child.GTObj.component_name + "Dup"
                    
            AddToGroup(sel, obj.component_name + "Dup") 
            
            obj.component_name = obj.asset_name
            
            DefaultGroupShade(obj.asset_name, scn)
            DefaultGroupShade(oldGroup, scn)
        
            FocusObject(sel)
        
            return {'FINISHED'}
            
class GT_Move_Dummy(bpy.types.Operator):
    """Allows you to freely move the dummy object without the groups objects moving with it."""
    
    bl_idname = "object.gt_move_dummy"
    bl_label = "Move Dummy Object"
    
        
    def __init__(self):
        print("Start moving")
 
    def __del__(self):
        print("Rawr, im done now")

    def modal(self,context,event):
        if event.type == 'ESC':
            
            # Were going to restore the dummy location to it's original location
            MoveObject(self.currentObj, (self.oldLocationX, self.oldLocationY, self.oldLocationZ))
            
            objects = FindDummyConstraintObjects(self.currentObj.GTObj.asset_name)
        
            for object in objects:
                AttachToDummy(object)
                
            FocusObject(self.currentObj)
            
            return {'FINISHED'}
         
        if event.type == 'RET':
            print("Enter worked")
            
            #We dont need to here, just re-attach all objects
            objects = FindDummyConstraintObjects(self.currentObj.GTObj.asset_name)
        
            for object in objects:
                AttachToDummy(object)
                
            FocusObject(self.currentObj)
                
            return {'FINISHED'}
                
        # When an object is selected, set it as a child to the object, and finish.
        if event.type == 'TIMER':
            print('TIMER')
            
            if context.active_object.name != self.currentObj.name or len(context.selected_objects) > 1:
                # Were going to restore the dummy location to it's original location
                MoveObject(self.currentObj, (self.oldLocationX, self.oldLocationY, self.oldLocationZ))
                
                objects = FindDummyConstraintObjects(self.currentObj.GTObj.asset_name)
        
                for object in objects:
                    AttachToDummy(object)
                    
                FocusObject(self.currentObj)
                    
                return {'FINISHED'}
                
        return {'PASS_THROUGH'}

        
    def execute(self, context):
        print("invoke!")
        print("Is this new?")
        
        sel = context.active_object
        
        # Deselect all objects, then go into the modal loop
        self.currentObj = sel
        
        # Have to do this to avoid retrieving a data pointer... x_x
        self.oldLocationX = sel.location[0]
        self.oldLocationY = sel.location[1]
        self.oldLocationZ = sel.location[2]
        
        # Detach all current objects from the dummy so it can be moved
        objects = FindDummyConstraintObjects(sel.GTObj.asset_name)
        
        for object in objects:
            DetachFromDummy(object)
            
        FocusObject(sel)
        
        # Add the modal handler and LETS GO!
        context.window_manager.modal_handler_add(self)
        
        # Add a timer to enable a search for a selected object
        self._timer = context.window_manager.event_timer_add(0.1, context.window)
        
        return {'RUNNING_MODAL'}
        
    
class GT_Create_Low_Poly_Base(bpy.types.Operator):
    
    """Creates a low-poly stage for the selected asset.  This will be the mesh used for the export, and for the game engine of your choice."""
    
    bl_idname = "object.gt_create_low_poly_base"
    bl_label = "Create Low-Poly"
    
    low_poly_base_options = EnumProperty(
        name="",
        items=(
        ('1', 'Use Base', 'Duplicate the base object as a low-poly object.'),   
        ('2', 'Use Base and Components', 'Duplicate the base and components as a low-poly object.'),
        ('3', 'Use Repto', 'Duplicate the base and marked components as a low-poly object.'),
        ),)
    
    def execute(self, context):
        print(self)
        
        return {'FINISHED'}
        
    
class GT_Create_Low_Poly_Component(bpy.types.Operator):
    
    """Updates the origin point based on the option selected, for all selected objects"""
    
    bl_idname = "object.gt_create_low_poly_comp"
    bl_label = "Create Low-Poly"
    
    low_poly_component_options = EnumProperty(
        name="",
        items=(
        ('1', 'Base Only', 'Replaces the base it was frozen from'),   
        ('2', 'Base and Components', 'Adds the frozen mesh as a duplicate to the object'),
        ('3', 'Merge', 'Duplicates the base as a low-poly object'),
        ),)
    
    def execute(self, context):
        print(self)
        
        return {'FINISHED'}
    
class GT_Create_Collision(bpy.types.Operator):
    """Updates the origin point based on the option selected, for all selected objects"""
    
    bl_idname = "object.gt_create_collision"
    bl_label = "Create Collision"
    
    def execute(self, context):
        print(self)
        
        return {'FINISHED'}
    
class GT_Create_Cage(bpy.types.Operator):
    """Updates the origin point based on the option selected, for all selected objects"""
    
    bl_idname = "object.gt_create_group"
    bl_label = "Create Cage"
    
    def execute(self, context):
        print(self)
        
        return {'FINISHED'}

class GT_Group_Create_Collision(bpy.types.Operator):
    """Updates the origin point based on the option selected, for all selected objects"""
    
    bl_idname = "object.gt_group_create_collision"
    bl_label = "Create Collision"
    
    def execute(self, context):
        print(self)
        
        return {'FINISHED'}
    
class GT_Group_Create_Cage(bpy.types.Operator):
    """Super rawr."""
    
    bl_idname = "scene.gt_group_create_group"
    bl_label = "Create Cage"
    
    def execute(self, context):
        print(self)
        
        return {'FINISHED'}
        
        
    
class GT_Check_Mesh(bpy.types.Operator):
    """Updates the origin point based on the option selected, for all selected objects"""
    
    bl_idname = "object.gt_check_mesh"
    bl_label = "Check Mesh"
    
    def execute(self, context):
        print(self)
        
        return {'FINISHED'}
        
        
#//////////////////////// - COMPLEX OPERATORS - ////////////////////////
class GT_Export_Assets(bpy.types.Operator):
    """Updates the origin point based on the option selected, for all selected objects"""
    
    bl_idname = "scene.gt_export_assets"
    bl_label = "Export Assets"
    
    def execute(self, context):
        print(self)
        
        # Create defaults of variables that need changing and change em
        objectScale = 1
        
        if context.GT_ue4_scale_100 is True:
            objectScale = 100
            
        embedTextures = False
        
        if context.GT_embed_textures is True:
            embedTextures = True
            
        # Check if we have a valid (or any) filepath
        
        # Start duplicating and merging all targeted assets for export
        # Put all duplicated objects inside exportObjects so they can be iterated through and
        # deleted at the end
        exportedObjects = []
        exportObjects = []
        originLocations = []
        
        
        # Run through each object
        
        # Set the origin of each object to the origin locations
        
        # Export them!
        bpy.ops.export_scene.fbx(check_existing=True, 
        filepath="", 
        filter_glob="*.fbx", 
        version='BIN7400', 
        use_selection=False, 
        global_scale=1.0, 
        axis_forward='-Z', 
        axis_up='Y', 
        bake_space_transform=False, 
        object_types={'EMPTY', 'ARMATURE', 'LAMP', 'CAMERA', 'MESH'}, 
        use_mesh_modifiers=True, 
        mesh_smooth_type='FACE', 
        use_mesh_edges=False, 
        use_tspace=False, 
        use_custom_properties=False, 
        use_armature_deform_only=False, 
        bake_anim=True, 
        bake_anim_use_nla_strips=True, 
        bake_anim_step=1.0, 
        bake_anim_simplify_factor=1.0, 
        use_anim=True, 
        use_anim_action_all=True, 
        use_default_take=True, 
        use_anim_optimize=True, 
        anim_optimize_precision=6.0, 
        path_mode='AUTO', 
        embed_textures=False, 
        batch_mode='OFF', 
        use_batch_own_dir=True, 
        use_metadata=True)
        
        # Delete all the temporary objects
        
        # Generate names for all the objects exported to avoid the .001 extension
        
        return {'FINISHED'}
        
classes = (GT_Blank_Report, GT_Name_Report, GT_Update_Origin, GT_Assign_Base, GT_Remove_From_Base, GT_Select_Parent, GT_Select_Base, GT_Create_New_Asset, GT_Add_Components, GT_Find_Components, GT_Delete_Base, GT_Remove_Components, GT_Duplicate_Base, GT_Merge_Base, GT_Seperate_Object, GT_Duplicate_Group, GT_Freeze, GT_Multi_Freeze, GT_Unfreeze, GT_Create_Group, GT_Remove_From_Group, GT_Move_Dummy, GT_Create_Low_Poly_Base, GT_Create_Low_Poly_Component, GT_Create_Collision, GT_Create_Cage, GT_Group_Create_Collision, GT_Group_Create_Cage, GT_Check_Mesh, GT_Export_Assets)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    print("-"*40)
    print("Registering Operators")
    
    #bpy.utils.register_module(__name__)

def unregister():
    
    print("-"*40)
    print("Unregistering Operators")
    
    
    bpy.utils.unregister_class(GT_Blank_Report)
    bpy.utils.unregister_class(GT_Name_Report)
    bpy.utils.unregister_class(GT_Update_Origin)
    bpy.utils.unregister_class(GT_Assign_Base)
    bpy.utils.unregister_class(GT_Remove_From_Base)
    bpy.utils.unregister_class(GT_Select_Parent)
    bpy.utils.unregister_class(GT_Select_Base)
    bpy.utils.unregister_class(GT_Create_New_Asset)
    bpy.utils.unregister_class(GT_Add_Components)
    bpy.utils.unregister_class(GT_Find_Components)
    bpy.utils.unregister_class(GT_Delete_Base)
    bpy.utils.unregister_class(GT_Remove_Components)
    bpy.utils.unregister_class(GT_Duplicate_Base)
    bpy.utils.unregister_class(GT_Merge_Base)
    bpy.utils.unregister_class(GT_Seperate_Object)
    bpy.utils.unregister_class(GT_Duplicate_Group)
    bpy.utils.unregister_class(GT_Freeze)
    bpy.utils.unregister_class(GT_Multi_Freeze)
    bpy.utils.unregister_class(GT_Unfreeze)
    bpy.utils.unregister_class(GT_Create_Group)
    bpy.utils.unregister_class(GT_Remove_From_Group)
    bpy.utils.unregister_class(GT_Move_Dummy)
    bpy.utils.unregister_class(GT_Create_Low_Poly_Base)
    bpy.utils.unregister_class(GT_Create_Low_Poly_Component)
    bpy.utils.unregister_class(GT_Create_Collision)
    bpy.utils.unregister_class(GT_Create_Cage)
    bpy.utils.unregister_class(GT_Group_Create_Collision)
    bpy.utils.unregister_class(GT_Group_Create_Cage)
    bpy.utils.unregister_class(GT_Check_Mesh)
    bpy.utils.unregister_class(GT_Export_Assets)
        
    #bpy.utils.unregister_module(__name__)
    