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
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ##### END GPL LICENSE BLOCK #####


#//////////////////////////////// - AUTHORS YO - ///////////////////////////
# 99% of Everything (Design/Code) - Crocadillian/Takanu @ Polarised Games Ltd.
# Python Assistance - Atom, Linusy, Meta-Androcto, CoDEManX 


# Although GPL doesn't require any form of attribution (and i think this freedom is awesome, hence the 
# license choice), this was a huge timesink on my part, so some attribution would be nice 
# if you end up using this for anything cool.  I wanna know what people are using this for! :3



#This states the metadata for the plugin
bl_info = {
    "name": "Capsule 0.88",
    "author": "Crocadillian/Takanu @ Polarised Games, with assistance from Atom, Linusy, Meta-Androcto, CoDEManX",
    "version": (0,86),
    "blender": (2, 7, 1),
    "api": 39347,
    "location": "3D View > Object Mode > Tools > Capsule",
    "description": "Provides workflow tools for non-destructive, streamlined game and CG asset development",
    "warning": "Beta",
    "wiki_url": "",
    "category": "Object"}
    
    
    
# Start importing all the addon files
# The init file just gets things started, no code needs to be placed here.
import importlib


modules =  [ "properties", "user_interface", "update",
             "definitions", "operators"]


imported_modules = []


for m in modules:
    im =  importlib.import_module(".{}".format(m), __name__)
    imported_modules.append(im)


if "bpy" in locals():
    for im in imported_modules:
        importlib.reload(im)


import bpy


def register():
    for im in imported_modules:
        if hasattr(im, 'register'):
            im.register()


def unregister():
    for im in reversed(imported_modules):
        if hasattr(im, 'unregister'):
            im.unregister()

