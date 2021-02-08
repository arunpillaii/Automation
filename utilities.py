""" Rigging automation utilities
"""

import maya.cmds as mc
import pymel.core as pm

def place_polevector(start, mid, end, offset_value=None):
    
	postions = [each.getTranslation(space="world") for each in (start, mid, end)]
	poly_plane = pm.polyCreateFacet( p=postions, ch=0)[0]

	loc = pm.spaceLocator()
	pm.pointConstraint(mid, loc)
	pm.normalConstraint(poly_plane, loc)

	pm.delete(poly_plane)


def create_skinjnts():
	selJnts = mc.ls(sl=1, type="joint")
	for selJnt in selJnts:
		mc.select(cl=1)
		for eachjnt in mc.ls(selJnt,dag=1,type="joint"):
			if not eachjnt.endswith("_CJ"):
				continue
			jntName = eachjnt.replace('_CJ' , '_SJ')
			jnt = mc.joint(n = jntName, rad = 0.5)
			mc.delete(mc.parentConstraint(eachjnt , jnt))
			mc.makeIdentity(jnt , apply = True , t = 1 , r = 1 , s = 1)
			mc.parentConstraint(eachjnt , jnt)
			mc.scaleConstraint(eachjnt , jnt)	
			cjParent = mc.listRelatives(eachjnt , p = True)
			if cjParent and not mc.listRelatives(jnt,p=1):
					mc.parent(jnt , cjParent[0].replace('_CJ' , '_SJ'))


import pymel.core as pm
from maya import OpenMaya
import re
import os

def file_save():
	file_path = pm.system.sceneName()
	if not file_path:
    		return
	file_dir, file_name = os.path.split(file_path)

	confirm_ver = pm.confirmDialog(
		title='Choose an option to save.',
		message="Click one option below.",
		button=['File-Version','Folder-Version', "Cancel"],
		defaultButton='Cancel',
		cancelButton='Cancel',
		dismissString='Cancel'
	)
	new_file_path = None
	if confirm_ver == "File-Version":
		path, ext = os.path.splitext(file_name)
		path_split = path.split("_")
		search_result = re.search(r'\d+', path_split[-1])
		if search_result:
			version_number = search_result.group()
			increment_number = str(int(version_number)+1).zfill(len(version_number))
			path_split[-1] = path_split[-1].replace(version_number, increment_number)
			new_name = "{}{}".format("_".join(path_split), ext)
			new_file_path = os.path.join(file_dir, new_name)
	elif confirm_ver == "Folder-Version":
		file_path = pm.system.sceneName()
		file_dir, file_name = os.path.split(file_path)
		dir_split = file_dir.split("/")
		search_result = re.search(r'\d+', dir_split[-1])
		new_dir = None
		if search_result:
			version_number = search_result.group()
			increment_number = str(int(version_number)+1).zfill(len(version_number))
			dir_split[-1] = dir_split[-1].replace(version_number, increment_number)
			new_dir = os.path.join(*dir_split)
			if not os.path.exists(new_dir):
					os.makedirs(new_dir)
			new_file_path = os.path.join(new_dir, file_name)

	if new_file_path:
		confirm_save = pm.confirmDialog(
			title='Confirm save.',
			message="File will be saved as: %s" % new_file_path, 
			button=['Yes', "Cancel"]
		)
		if confirm_save != "Yes":
			return
		
		pm.system.saveAs(new_file_path, force=True)
		OpenMaya.MGlobal.displayInfo("File saved as: %s" % new_file_path)

# file_save()

import pymel.core as pm
from automation import sk_ctrlCurves as scc
reload(scc)


`def facial_ctrls():
	selections = pm.ls(sl=True)
	for selection in selections:
		sel_name = selection.replace("_CJ", "")
		ctrl_name = "%s_Ctrl" % sel_name
		grp_name = "%s_Grp" % sel_name
		inst = scc.Ctrlcurve(ctrl_name)
		inst.sphere()
		inst.grpTrans(name=grp_name)
		pm.delete(pm.parentConstraint(selection, grp_name))
		pm.parentConstraint(ctrl_name, selection, mo=True)
		input_parent = selection.getParent()
		if input_parent:
			pm.parentConstraint(input_parent, grp_name, mo=True)
			

		# if 
facial_ctrls()`
