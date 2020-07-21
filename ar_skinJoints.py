											#--------------------------------------------------------------#
											# 	DESCRIPTION	: Python Module for Skinning Joints 		   #
											# 	AUTHOR 			: Arun . S - arunpillaii@gmail.com         #
											# 	VERSION			: 1.00 , 17 November 2009                  #
											#   Copyright (C) 2009.  All rights reserved.				   #
											#--------------------------------------------------------------#
#Imports!
import maya.cmds as mc

def ar_skinJoints(root_jnt='Root_CJ', exclude_jnts=[]):
	mc.select(cl = True)
	mc.addAttr('Systems' , ln = 'Skeleton_SJ' , at = 'bool', k = True , h = False)
	mc.setAttr('Systems.Skeleton_SJ', 1 , k = False , cb = True)
	allCJjnts = mc.ls(root_jnt,dag=1,type="joint")
	
	mc.select(cl = True)
	allSJjnts = []
	for eachjnt in allCJjnts:
		if eachjnt in exclude_jnts:
			continue
		sjJntName = replace_jnt(eachjnt)
		jnt = mc.joint(n = sjJntName, rad = 0.5)
		mc.delete(mc.parentConstraint(eachjnt , jnt))
		mc.makeIdentity(jnt , apply = True , t = 1 , r = 1 , s = 1)
		mc.parentConstraint(eachjnt , jnt)
		mc.scaleConstraint(eachjnt , jnt)

		cjParent = mc.listRelatives(eachjnt , p = True)
		if cjParent and mc.objExists(replace_jnt(eachjnt)):
			cjtosjParent = replace_jnt(cjParent[0])
			mc.parent(jnt , cjtosjParent)
		else:
			allSJjnts.append(jnt)
		mc.select(cl = True)

	for i in range(len(allSJjnts)):
		sjtocj = replace_jnt(allSJjnts[i], '_SJ' , '_CJ')
		cjParent = mc.listRelatives(sjtocj , p = True)[0]
		cjtosjParent = replace_jnt(cjParent)
		mc.parent(allSJjnts[i] , cjtosjParent)
	
	for side in ['Left' , 'Right']:
		if mc.objExists(side + 'ArmUpBend0_SJ'):
			mc.parent((side + 'ArmUpBend0_SJ') , (side + 'Clavicle_SJ'))
			bendUpChilds = mc.listRelatives((side + 'ArmUpBend0_SJ') , type = 'joint' , ad = True)
			mc.parent((side + 'ArmDnBend0_SJ') , bendUpChilds[1])
			bendDnChilds = mc.listRelatives((side + 'ArmDnBend0_SJ') , type = 'joint' , ad = True)
			wristChilds = mc.listRelatives((side + 'Wrist_SJ') , type = 'joint' , c = True)
			mc.parent(wristChilds , bendDnChilds[0])
			mc.delete(bendUpChilds[0] , (side + 'Shoulder_SJ'))
		
		if mc.objExists(side + 'LegUpBend0_SJ'):
			mc.parent((side + 'LegUpBend0_SJ') , 'Root_SJ')
			bendUpChilds = mc.listRelatives((side + 'LegUpBend0_SJ') , type = 'joint' , ad = True)
			mc.parent((side + 'LegDnBend0_SJ') , bendUpChilds[1])
			bendDnChilds = mc.listRelatives((side + 'LegDnBend0_SJ') , type = 'joint' , ad = True)
			ankleChilds = mc.listRelatives((side + 'Ankle_SJ') , type = 'joint' , c = True)
			mc.parent(ankleChilds , bendDnChilds[0])
			mc.delete(bendUpChilds[0] , (side + 'UpLeg_SJ'))
	mc.select(cl = True)

	root_sj = replace_jnt(root_jnt)
	if mc.objExists(root_sj):
		mc.parent(root_sj ,'CENTER')
		mc.connectAttr('Systems.Skeleton_SJ', "%s.v" % root_sj)


def replace_jnt(jnt_name, input_str='_CJ', output_str='_SJ'):
	return jnt_name.replace(input_str , output_str)
