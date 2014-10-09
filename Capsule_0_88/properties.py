from .update import Update_VisibilityToggle, Update_ComponentToggle, Update_CompomentListType, Update_VisibilityListType, Update_FreezeList, Update_FreezeDelete, Update_FreezeView, Update_FreezeName, Update_Visibility, Update_ObjectOrigin, Update_ObjectVGOrigin, Update_AssetType, Update_ObjectType, Update_AssetName, Update_BaseName, Update_ComponentName, Update_HP_Visibility, Update_LP_Visibility, Update_CG_Visibility, Update_CG_Visibility, Update_CX_Visibility, Update_BaseVisibility, Update_ComponentVisibility, Update_FreezeVisibility, Update_DummyObject, Update_DummyPosition, Update_DummyLocation, Update_DummyOffset, Update_DummySize, Update_GroupOrigin, Update_XRay, Update_OriginSize

import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty, StringProperty, CollectionProperty

from bpy.types import PropertyGroup

# -------------OBJECT/SCENE PROPERTIES-------------------------------------------------------
# Defines scene preferences for the plugin
class GT_Scene_Preferences(PropertyGroup):
    
    engine_select = EnumProperty(
        name="Set Game Engine",
        items=(
        ('1', 'Unreal Engine 4', 'Configures UI and options for Unreal Engine 4 asset development.'),
        ('2', 'Unity', 'Configures UI and options for Unity asset development.'),    
        ('3', 'CryEngine 3', 'Configures UI and options for CryEngine 3 asset development.'),
        ),)
        
    new_asset_select = EnumProperty(
        name="Set Asset Type",
        items=(
        ('1', 'Set Asset Type', ''),
        ('2', 'High-Poly', 'Sets the object as a High-Resolution object.'),
        ('3', 'Low-Poly', 'Sets the object as a Low-Resolution object, which will be the mesh exported.'),
        ), )
        
    new_object_name = StringProperty(
        name="",
        description="The name of the asset selected",
        default="",)
        
    freeze_name = StringProperty(
        name="Freeze Name",
        description="The saved name of the Freeze state",
        default="None",)
        
    scene_visibility_category = EnumProperty(
        name="Switch Visibility List",
        items=(
        ('1', 'Asset Stage', 'Exports every GT asset in the scene'),
        ('2', 'Asset Type', 'Exports every selected, GT asset in the scene.'),
        ), )
        
    visibility_HP = EnumProperty(
        name="Visibility Options",
        items=(
        ('1', 'Object Settings', 'Preserves defined shading settings for that category.'),
        ('2', 'Normal', 'Shades everything normally'),
        ('3', 'Box Bounds', 'Changes the display to box bounds for all objects in this category'),   
        ('4', 'Wireframe', 'Changes the display to wireframe for all objects in this category'),
        ('5', 'Wire', 'Adds a wire display for all objects in this category'),
        ('6', 'Hide', 'Changes the display to hide all objects in this category'),
        ),
        default='1',
        update = Update_HP_Visibility)
        
    visibility_LP = EnumProperty(
        name="Visibility Options",
        items=(
        ('1', 'Object Settings', 'Preserves defined shading settings for that category.'),
        ('2', 'Normal', 'Shades everything normally'),
        ('3', 'Box Bounds', 'Changes the display to box bounds for all objects in this category'),   
        ('4', 'Wireframe', 'Changes the display to wireframe for all objects in this category'),
        ('5', 'Wire', 'Adds a wire display for all objects in this category'),
        ('6', 'Hide', 'Changes the display to hide all objects in this category'),
        ),
        default='1',
        update = Update_LP_Visibility)
        
    visibility_CG = EnumProperty(
        name="Visibility Options",
        items=(
        ('1', 'Object Settings', 'Preserves defined shading settings for that category.'),
        ('2', 'Normal', 'Shades everything normally'),
        ('3', 'Box Bounds', 'Changes the display to box bounds for all objects in this category'),   
        ('4', 'Wireframe', 'Changes the display to wireframe for all objects in this category'),
        ('5', 'Wire', 'Adds a wire display for all objects in this category'),
        ('6', 'Hide', 'Changes the display to hide all objects in this category'),
        ),
        default='1',
        update = Update_CG_Visibility)
        
    visibility_CX = EnumProperty(
        name="Visibility Options",
        items=(
        ('1', 'Object Settings', 'Preserves defined shading settings for that category.'),
        ('2', 'Normal', 'Shades everything normally'),
        ('3', 'Box Bounds', 'Changes the display to box bounds for all objects in this category'),   
        ('4', 'Wireframe', 'Changes the display to wireframe for all objects in this category'),
        ('5', 'Wire', 'Adds a wire display for all objects in this category'),
        ('6', 'Hide', 'Changes the display to hide all objects in this category'),
        ),
        default='1',
        update = Update_CX_Visibility)
        
    visibility_base = EnumProperty(
        name="Visibility Options",
        items=(
        ('1', 'Object Settings', 'Preserves defined shading settings for that category.'),
        ('2', 'Normal', 'Shades everything normally'),
        ('3', 'Box Bounds', 'Changes the display to box bounds for all objects in this category'),   
        ('4', 'Wireframe', 'Changes the display to wireframe for all objects in this category'),
        ('5', 'Wire', 'Adds a wire display for all objects in this category'),
        ('6', 'Hide', 'Changes the display to hide all objects in this category'),
        ),
        default='1',
        update = Update_BaseVisibility)
        
    visibility_component = EnumProperty(
        name="Visibility Options",
        items=(
        ('1', 'Object Settings', 'Preserves defined shading settings for that category.'),
        ('2', 'Normal', 'Shades everything normally'),
        ('3', 'Box Bounds', 'Changes the display to box bounds for all objects in this category'),   
        ('4', 'Wireframe', 'Changes the display to wireframe for all objects in this category'),
        ('5', 'Wire', 'Adds a wire display for all objects in this category'),
        ('6', 'Hide', 'Changes the display to hide all objects in this category'),
        ),
        default='1',
        update = Update_ComponentVisibility)
        
    visibility_freeze = EnumProperty(
        name="Visibility Options",
        items=(
        ('1', 'Object Settings', 'Preserves defined shading settings for that category.'),
        ('2', 'Normal', 'Shades everything normally'),
        ('3', 'Box Bounds', 'Changes the display to box bounds for all objects in this category'),   
        ('4', 'Wireframe', 'Changes the display to wireframe for all objects in this category'),
        ('5', 'Wire', 'Adds a wire display for all objects in this category'),
        ('6', 'Hide', 'Changes the display to hide all objects in this category'),
        ),
        default='4',
        update = Update_FreezeVisibility)
        
        
    export_scope = EnumProperty(
        name="Set Export Scope",
        items=(
        ('1', 'Export Scene', 'Exports every GT asset in the scene'),
        ('2', 'Export Selected', 'Exports every selected, GT asset in the scene.'),
        ('3', 'Export As Level', 'Exports the scene as a level (Unity Only).'),
        ('4', 'Export Tagged', 'Export all assets tagged for export'),
        ), )
    
    embed_textures = BoolProperty(
        name = "Embed Textures",
        description = "Toggles the embedding of textures for each object into the FBX file when exported",
        default = False)
    
    ue4_scale_100 = BoolProperty(
        name = "Scale 100x",
        description = "Toggles whether the asset will be scaled 100 times its current size in UE4.  This is due to Unreal Engine's unit conversion, which recognises 1m ad 1cm (ikr...).  Selecting this option will make your meshes appear normal in UE4, but may break Skeletal Meshes",
        default = False)
    
    export_destination = StringProperty(
        name = "", 
        description = "File path of the destination all assets will be exported to", 
        default = "None",
        #This is used as a special type to receive folder paths
        subtype = 'DIR_PATH')
        
    asset_update_loop = BoolProperty(
        name = "Asset Update Loop",
        description = "An internal variable designed to prevent the name update from looping on itself",
        default = True
    )   
    
    dummy_update_loop = BoolProperty(
        name="Dummy Update Loop",
        description = "Another one of those internal variables to prevent loops of oblivion",
        default=True)
        
    asset_group_exit = BoolProperty(
        name = "Use X-Ray",
        description = "Turns on X-Ray mode for the object, so it can be seen in front of all objects.",
        default = False)
        
# Defines individual object data for the plugin        
class GT_Object_Data(PropertyGroup):
    
    is_GT_asset = BoolProperty(
        name = "",
        description = "Determines whether this object is part of the GT system.  If not, only display the new asset UI",
        default = False)
    
    is_frozen = BoolProperty(
        name = "",
        description = "Determines whether this object is frozen.",
        default = False)
        
    freeze_hide = BoolProperty(
        name = "",
        description = "Determines whether this object is hidden regardless of the visibility options set",
        default = False)
        
    freeze_type = EnumProperty(
        name="Frozen Type",
        items=(
        ('1', 'Parent Only', 'Replaces the base it was frozen from'),   
        ('2', 'Parent and Children', 'Adds the frozen mesh as a duplicate to the object'),
        ('3', 'Merge', 'Duplicates the base as a low-poly object'),
        ),)
        
    freeze_name = StringProperty(
        name = "",
        description = "Internal value used to define the frozen object on the list",
        default = "None")
        
    update_toggle = BoolProperty(
        name = "",
        description = "This is an internal variable for bypassing the asset name failsafes, for entering a blank or 'none' name. False = Turned off, True = Turned on.",
        default = False)
    
    asset_name = StringProperty(
        name = "Object Name",
        description = "The name of the group this object belongs to",
        default = "None",
        update = Update_AssetName)
        
    old_asset_name = StringProperty(
        name = "Object Name",
        description = "The name of the group this object belongs to.    For internal use only.",
        default = "None",)

    base_name = StringProperty(
        name = "Base Name",
        description = "The name of the parent this object belongs to.",
        default = "None",
        update = Update_BaseName)
        
    old_base_name = StringProperty(
        name = "Base Name",
        description = "The name of the parent this object belongs to.",
        default = "None",)
        
    freeze_name = StringProperty(
        name="Freeze Name",
        description="The saved name of the Freeze state.  This is read and printed to the Freeze List.",
        default="None",)
        
    freeze_index = IntProperty(
        name="Freeze Index",
        description="A internal variable used for reading and writing to list entries",
        default = 0)
        
    component_name = StringProperty(
        name = "Component Name",
        description = "The name of the selected object.",
        default = "None",
        update = Update_ComponentName)
        
    old_component_name = StringProperty(
        name = "Component Name",
        description = "The name of the selected object.  For internal use only.",
        default = "None",)
      
    asset_type = EnumProperty(
        name="Set Asset Type",
        items=(
        ('1', 'High-Poly', 'Sets the object as a High-Resolution object, that will be exported'),
        ('2', 'Low-Poly', 'Sets the object as a Low-Resolution object.'),
        ('3', 'Cage', 'Sets the object as a cage object, for normal map baking.'),
        ('4', 'Collision', 'Sets the object as a collision object, for use in physics calculations.'),
        ('5', 'Skeletal Mesh', 'Sets the object as a skeletal mesh, for animation and posing.'),
        ), 
        update = Update_AssetType)
       
    object_type = EnumProperty(
        name="Set Object Type",
        items=(
        ('1', 'Base', 'A standard object type that is the foundation of any component'),
        ('2', 'Component', 'A part of a base object that adds additional detail to it'),
        ),
        update = Update_ObjectType)
        
    old_object_type = EnumProperty(
        name="Old Object Type",
        items=(
        ('1', 'Base', 'A standard object type that is the foundation of any component'),
        ('2', 'Component', 'A part of a base object that adds additional detail to it'),
        ),)

    origin_point = EnumProperty(
        name="Set Object Origin",
        items=(
        ('1', 'Origin to Object Base', 'Sets the origin to the lowest point of the object, disregarding object orientation.'),   
        ('2', 'Origin to Lowest Point', 'Sets the origin to the absolute lowest point of the object'),  
        ('3', 'Origin to Centre of Mass', 'Sets the origin using the objects centre of mass.'),
        ('4', 'Origin to Vertex Group', 'Sets the origin using a given vertex group'),
        ),
        update = Update_ObjectOrigin)
    
    mark_repto = BoolProperty(
        name = "Mark for Retopology",
        description = "Marks a component as requiring retopology.  This should only be necessary when the component is part of the object's silhouette and structure.",
        default = False)
        
    visibility = EnumProperty(
        name="Visibility Options",
        items=(
        ('1', 'Normal', 'Shades everything normally'),
        ('2', 'Box Bounds', 'Changes the display to box bounds for all objects in this category'),   
        ('3', 'Wireframe', 'Changes the display to wireframe for all objects in this category'),
        ('4', 'Wire', 'Adds a wire display for all objects in this category'),
        ('5', 'Hide', 'Changes the display to hide all objects in this category'),
        ),
        update = Update_Visibility)
        
def GetGroupOriginObjects(scene, context):
    items = [
        ("1", "None",  "", 0),
    ]

    sel = bpy.context.active_object
    obj = sel.GTObj
    u = 1
    
    if obj.asset_name in bpy.data.groups:
        group = bpy.data.groups[obj.asset_name]
        
        for i,x in enumerate(group.objects):
            
            if x.GTGrp.is_origin_point is False:
                items.append((str(i+1), x.name, x.name))

    return items
    
def GetGroupDummyObjects(scene, context):
    items = [
        ("1", "None",  "", 0),
    ]

    sel = bpy.context.active_object
    obj = sel.GTObj
    u = 1
    
    if obj.asset_name in bpy.data.groups:
        group = bpy.data.groups[obj.asset_name]
        
        for i,x in enumerate(group.objects):
            
            # Used to omit both the origin and dummy objects from the list
            if x.GTGrp.is_group_object is False and x.GTGrp.is_origin_point is False:
                items.append((str(i+1), x.name, x.name))

    return items
    
        
# Defines group data for the plugin         
class GT_Group_Data(PropertyGroup):
    
    group_dummy_object = EnumProperty(
        name="Set Dummy Object",
        items=(
        ('1', 'Plain Axes', 'Sets the dummy object as a Plain Axes.'),   
        ('2', 'Single Arrow', 'Sets the dummy object as a Single Arrow.'),
        ('3', 'Circle', 'Sets the dummy object as a Circle.'),
        ('4', 'Rectangle', 'Sets the dummy object as a Rectangle'),
        ),
        default = '1',
        update = Update_DummyObject)
        
    old_group_dummy_object = EnumProperty(
        name="Set Dummy Object",
        items=(
        ('1', 'Plain Axes', 'Sets the dummy object as a Plain Axes.'),   
        ('2', 'Single Arrow', 'Sets the dummy object as a Single Arrow.'),
        ('3', 'Circle', 'Sets the dummy object as a Circle.'),
        ('4', 'Rectangle', 'Sets the dummy object as a Rectangle'),
        ),
        default = '1')

    group_dummy_loc = EnumProperty(
        name="Set Dummy Position",
        items=(
        ('1', 'Above', 'Sets the dummy object above all base objects.'),   
        ('2', 'Below', 'Sets the dummy object above all base objects.'),
        ),
        update = Update_DummyPosition)
        
    group_dummy_location = EnumProperty(
        name="Set Dummy Location",
        items=(
        ('1', 'Auto-Update', 'Sets the dummy location automatically, based on object positions inside the group.'),   
        ('2', 'Freeform', 'Allows the user to position the dummy wherever they choose.'),
        ('3', 'Object', 'Sets the dummy location to the origin of a specific object.'),
        ),
        update = Update_DummyLocation)
    
    group_dummy_size = FloatProperty(
        name="Dummy Size",
        default = 1.0,
        update = Update_DummySize)
    
    group_dummy_offset = FloatProperty(
        name="Vertical Offset",
        default = 1.0,
        update = Update_DummyOffset)
    
    is_group_object = BoolProperty(
        name = "Group Object",
        description = "Well, is this object a group object?",
        default = False)  
        
    has_group_object = BoolProperty(
        name = "Group Object",
        description = "Well, do you have a group object?",
        default = False)
        
    is_own_group = BoolProperty(
        name = "Is Own Object",
        description = "Is this object not a dummy or origin, and is it's own group?"
    )
    
    hide_group = BoolProperty(
        name = "Hide Group Dummy",
        description = "Hides the group dummy from view so the model can be viewed without issue.",
        default = False)    
        
    is_origin_point = BoolProperty(
        name = "Is Origin Point",
        description = "Another internal variable, just in case",
        default = False)
        
    origin_location = EnumProperty(
        name = "Origin Location",
        description = "Snaps the origin to the chosen location",
        items=(
        ('1', 'Origin to Base Median', 'Sets the origin to the median point of all base and loose component objects.'),   
        ('2', 'Origin to Lowest Point', 'Sets the dummy to the median of the lowest origin points out of all objects in the group.'),
        ('3', 'Origin to Object', 'Sets the dummy object above all base objects.'),
        ),
        update = Update_GroupOrigin)
        
    origin_dummy_size = FloatProperty(
        name="Origin Size",
        default = 1.0,
        update = Update_OriginSize)
        
    dummy_object_select = EnumProperty(
        name="Select Object Origin",
        items=GetGroupDummyObjects,
        update=Update_DummyLocation)
        
    origin_object_select = EnumProperty(
        name="Select Object Origin",
        items=GetGroupOriginObjects,
        update=Update_GroupOrigin)
        
    x_ray_toggle = BoolProperty(
        name = "Use X-Ray",
        description = "Turns on X-Ray mode for the object, so it can be seen in front of all objects.",
        default = False,
        update = Update_XRay)
        
def GetVertexGroups(scene, context):
    items = [
        ("1", "None",  "", 0),
    ]

    ob = bpy.context.active_object
    u = 1
    #print(ob.vertex_groups.active)
    #print(ob.vertex_groups)
    
    for i,x in enumerate(ob.vertex_groups):
        
        # If you didn't want to append and just wanted to generate a list:
        #items = [(str(i+1),x.name,x.name) for i,x in enumerate(ob.vertex_groups)]
        
        items.append((str(i+1), x.name, x.name))

    return items

def GetFrozenItems(scene, context):
    items = [
    ]

    ob = bpy.context.active_object
    i = 0
    
    #Get the constraints
    for constraint in ob.constraints:
        
        #Find copy location constraints with a particular name :D
        if constraint.type is "COPY_LOCATION":
            if constraint.name.find("Freeze") == 1:
                items.append((str(i+1), constraint.name, constraint.name))
                i += 1

    return items

class FreezeList(PropertyGroup):
    name = StringProperty(
        name = "",
        default="",
        update = Update_FreezeName)
    type = EnumProperty(
        name="",
        items=(
        ('1', 'Single Object', 'Freezes just the object selected'),   
        ('2', 'Parent + Children', 'Freezes both the object selected, and its children'),
        ('3', 'Merge', 'Merges both the object selected, and its children'),
        ('4', 'Group', 'Freezes every object inside the selected group.')
        ),)
    delete = BoolProperty(
        default = True,
        update = Update_FreezeDelete)
    view = BoolProperty(
        default = True,
        update = Update_FreezeView)
        
    # This is used so freeze objects can properly read and write back to the list
    index = IntProperty()
    
class ComponentList(PropertyGroup):
    name = StringProperty()
    icon = IntProperty()
    type = EnumProperty(
        name="Visibility Options",
        items=(
        ('1', 'Normal', 'Doesnt do anything different'),
        ('2', 'Box Bounds', 'Changes the display to box bounds'),   
        ('3', 'Wireframe', 'Changes the display to wireframe'),
        ('4', 'Wire', 'Adds a wire display on top of normal shading'),
        ('5', 'Hide', 'Hides the object from view'),
        ),
        update = Update_CompomentListType)
        
    iconName = StringProperty()

class VisibilityList(PropertyGroup):
    name = StringProperty()
    nameIcon = IntProperty()
    type = EnumProperty(
        name="Visibility Options",
        items=(
        ('1', 'Object Settings', 'Uses already defined object settings'),
        ('2', 'Normal', 'Shades everything normally'),
        ('3', 'Box Bounds', 'Changes the display to box bounds for all objects in this category'),   
        ('4', 'Wireframe', 'Changes the display to wireframe for all objects in this category'),
        ('5', 'Wire', 'Adds a wire display for all objects in this category'),
        ('6', 'Hide', 'Changes the display to hide all objects in this category'),
        ),
        update=Update_VisibilityListType)
        
# Defines object-centric data generated specifically for menu operation
class GT_Object_Menu_Data(PropertyGroup):
    
    vertex_groups = EnumProperty(
        name="Select Vertex Group",
        items=GetVertexGroups,
        update=Update_ObjectVGOrigin)
        
    frozen_bases = EnumProperty(
        name="Select Frozen Base",
        items=GetFrozenItems)
        
    view_base_list = BoolProperty(
        name="View Parent List",
        description="Toggles the list of every base object in the model",
        default=False)
        
    view_freeze_list = BoolProperty(
        name="View Freeze List",
        description="Toggles the list of every freeze state this high-poly object has",
        default=False)
        
    view_component_list = BoolProperty(
        name="Show/Refresh Child List",
        description="Toggles the list of every component object the selected base has",
        default=False,
        update=Update_ComponentToggle)
        
    component_collection = CollectionProperty(
        name="Visibility Collection",
        description="Defines a list of components inside the base object",
        type=ComponentList)
        
    component_collection_index = IntProperty(
        name="Yoes",
        default=0)
        
    freeze_collection = CollectionProperty(
        name="Visibility Collection",
        description="Defines a list of frozen objects inside the base object",
        type=FreezeList)
        
    freeze_collection_index = IntProperty(
        name="Yoes",
        default=0)
        
        
class GT_Scene_Menu_Data(PropertyGroup):

    component_update_toggle = BoolProperty(
        name = "",
        description = "Another ugly internal variable used as a UI switch",
        default = False)
        
    component_generate_toggle = BoolProperty(
        name = "",
        description = "Yet another ugly internal variable used as a UI switch",
        default = False)
        
    vis_update_toggle = BoolProperty(
        name = "",
        description = "Another ugly internal variable used as a UI switch",
        default = False)
        
    vis_generate_toggle = BoolProperty(
        name = "",
        description = "Yet another ugly internal variable used as a UI switch",
        default = False)
    
    scene_visibility_toggle = BoolProperty(
        name="Show Visibility Options",
        description="Toggles a list of display options for various object categories in the scene",
        default=False,
        update=Update_VisibilityToggle)
        
    scene_update_toggle = BoolProperty(
        name="Internal Scene Update Toggle",
        description="Used to prevent the scene visibility updates from being called as the list is generated",
        default=False
    )
        
    freeze_toggle = BoolProperty(
        name="Show Freeze Options",
        description="Toggles the Freeze menu, used for asset versioning",
        update = Update_FreezeList,
        default=False)
        
    visibility_collection = CollectionProperty(
        name="Visibility Collection",
        description="Defines the object categories used in visibility changes",
        type=VisibilityList)
        
    visibility_collection_index = IntProperty(
        name="Yoes",
        default=0)
        
class GT_Update_Exits(PropertyGroup):
    base_group_exit = BoolProperty(
        name = "Use X-Ray",
        description = "Turns on X-Ray mode for the object, so it can be seen in front of all objects.",
        default = False)
        
    comp_group_exit = BoolProperty(
        name = "Use X-Ray",
        description = "Turns on X-Ray mode for the object, so it can be seen in front of all objects.",
        default = False)
        
    
        
        

# collection of property group classes that need to be registered on module startup
classes = (GT_Scene_Preferences, GT_Object_Data, GT_Group_Data, FreezeList, ComponentList, VisibilityList, GT_Object_Menu_Data, GT_Scene_Menu_Data, GT_Update_Exits)

def register():
    print("-"*40)
    print("Registering Properties")
    for cls in classes:
        bpy.utils.register_class(cls)
    
    #bpy.utils.register_module(__name__)

    # Add these properties to every object in the entire Blender system (muha-haa!!)
    bpy.types.Scene.GTScn = PointerProperty(type=GT_Scene_Preferences)
    bpy.types.Object.GTObj = PointerProperty(type=GT_Object_Data)
    bpy.types.Object.GTGrp = PointerProperty(type=GT_Group_Data)
    bpy.types.Object.GTMnu = PointerProperty(type=GT_Object_Menu_Data)
    bpy.types.Scene.GTSmn = PointerProperty(type=GT_Scene_Menu_Data)
    bpy.types.Object.GTExt = PointerProperty(type=GT_Update_Exits)

def unregister():
    print("-"*40)
    print("Unregistering Properties")
     
    del bpy.types.Scene.GTScn
    del bpy.types.Object.GTObj
    del bpy.types.Object.GTGrp
    del bpy.types.Object.GTMnu
    del bpy.types.Scene.GTSmn
    
    bpy.utils.unregister_class(GT_Scene_Preferences)
    bpy.utils.unregister_class(GT_Object_Data)
    bpy.utils.unregister_class(GT_Group_Data)
    bpy.utils.unregister_class(FreezeList)
    bpy.utils.unregister_class(ComponentList)
    bpy.utils.unregister_class(VisibilityList)
    bpy.utils.unregister_class(GT_Object_Menu_Data)
    bpy.utils.unregister_class(GT_Scene_Menu_Data)
    bpy.utils.unregister_class(GT_Update_Exits)
    
    #bpy.utils.unregister_module(__name__)
        
    
