											#--------------------------------------------------------------#
											# 	DESCRIPTION	: Python Module for Creating Proxy Geometry		 #	 																		   
											# 	AUTHOR 			: Arun . S - arunpillaii@gmail.com             #                    												                       				                     
											# 	VERSION			: 1.00 , 17 November 2009                      #
											#   Copyright (C) 2009.  All rights reserved.									 #
											#--------------------------------------------------------------#
											
#Imports!
import maya.cmds as mc , math ,maya.OpenMaya as om

#calling procedure
def ar_proxy():
	sel = mc.ls(sl=1)
	if len(sel)==0:
		raise Exception('No Objects are Selected..........')#Selection Error
		return 
	for each in sel:
		if mc.nodeType(each) != 'joint':#Object Matching Error
			continue
		getRet = ar_buildProxy(each)#Main Procedure 
	mc.select(sel)
	om.MGlobal.displayInfo("Proxy Objects Created Successfully.........")
	return getRet

#Proxt Creation Procedure
def ar_buildProxy(rootJoint='Root_SJ'):
	try:
		childJnts = mc.listRelatives(rootJoint,c=True,type='joint')#Finding Child joints
		mainGrp = 'PROXY'
		if not mc.objExists(mainGrp):#Main Group Creation
			mc.group(n=mainGrp,em=True)
			if mc.objExists('Ctrl_ROOT') and mc.attributeQuery('Display', n='Ctrl_ROOT', ex=1):
				proxyCon = mc.createNode('condition',n = 'Display_Proxy')
				mc.connectAttr('Ctrl_ROOT.Display', proxyCon + '.firstTerm')
				mc.setAttr(proxyCon + '.colorIfTrue', 1,1,1)
				mc.setAttr(proxyCon + '.colorIfFalse', 0,0,0)
				mc.connectAttr(proxyCon + '.outColor.outColorR', mainGrp + '.v')
		for jnt in childJnts:
			parentPos = mc.xform(rootJoint,q=True,t=True, ws=True)#query Parent Position
			childPos  = mc.xform(jnt,q=True,t=True , ws=True)#query Child Position
			vectVal = [(parentPos[0]-childPos[0]),(parentPos[1]-childPos[1]),(parentPos[2]-childPos[2])]
			jntLength = abs(math.sqrt(vectVal[0]**2 + vectVal[1]**2 + vectVal[2]**2))#get Distance
			radius = jntLength * 0.20
			getIndex = childJnts.index(jnt)
			name = rootJoint.split('_')[0] + '_%iProxy' % getIndex #get Name
			proxy = mc.polyCylinder(n=name ,r=radius , h=jntLength, sx=8 , sy=1 , sz=0 , ax=[0,1,0] , ch=1)#Geometry Creation
			mc.parent(proxy[0],mainGrp)
			mc.delete(mc.parentConstraint(rootJoint,jnt,proxy[0]))
			mc.delete(mc.aimConstraint(jnt,proxy[0],aim=[0,1,0]))
			mc.parentConstraint(rootJoint,proxy[0],mo=True)
			mc.scaleConstraint(rootJoint,proxy[0],mo=True)
			mc.refresh(cv=True)#Refresh View
			ar_buildProxy(jnt)
		return mainGrp
	except TypeError:#Error
		return None
		
#**************************************************END**************************************************#

