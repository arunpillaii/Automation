											#--------------------------------------------------------------#
											# 	DESCRIPTION	: Supporting Scripts for AutoRigging Tool      #                    												                       				                     
											# 	VERSION			: 1.00 , 20 November 2009                      #
											#   Copyright (C) 2009.  All rights reserved.									 #
											#--------------------------------------------------------------#
#Imports!
import maya.cmds as mc
import maya.mel as mel
import ar_rigTools as tools

#	Description -- Lock And Hide Unused Attributes 
#	skObject -- Source Object (Single / Array)
#	skAttrs -- Input Attibutes
#	skMode -- 0 : Lock and Hide all attibutes exclude input attributes , 1 : Lock and Hide input attributes
def lockhide(skObject, skAttrs, skMode=0):
	skAllAttrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
	for attrs in skAttrs:
		skAllAttrs.remove(attrs)
	if skMode == 0 :
		for attr in skAllAttrs:
			mc.setAttr((skObject + '.' + attr), lock=1, keyable=0)
	else:
		for attr in skAttrs:
			mc.setAttr((skObject + '.' + attr), lock=1, keyable=0)
#-------------------------------------------------------------------------------------------------#
#	Description -- Reverse the constraints of object with two constraints with reverse node
# skConstr -- input object
def revcnstr(skConstr):
	skConType = mc.nodeType(skConstr)
	if skConType == 'parentConstraint' or skConType == 'pointConstraint' or skConType == 'orientConstraint':
		skTargs = mel.eval(skConType + ' -q -tl ' + skConstr)
		if len(skTargs) == 2:
			skRev = mc.createNode('reverse', name=(skConstr + 'Reverse'))
			skClamp = mc.createNode('clamp', name=(skConstr + 'Clamp'))
			mc.connectAttr((skConstr + '.' + skTargs[0] + 'W0'), (skRev + '.inputX'))
			mc.connectAttr((skRev + '.outputX'), (skConstr + '.' + skTargs[1] + 'W1'))
			mc.setAttr((skClamp + '.maxR'), 1)
			mc.connectAttr((skClamp + '.outputR'), (skConstr + '.' + skTargs[0] + 'W0'))
			return skClamp
		else:
			return 'Too many constraint parents'
	else:
		return 'Not a constraint'
#-------------------------------------------------------------------------------------------------#
#	Description -- Creating a render box on input position and parent that object under input object
# skBoxName -- Input Name for Render Box
# skPosX, skPosY, skPosZ -- X, Y , Z position of render Box
# parentObj -- render box parent under this object 
def rendbox(skBoxName , skPosX , skPosY , skPosZ , parentObj = None):
	skBoxShape = mc.createNode('renderBox')
	mc.setAttr((skBoxShape + '.size'), 0.05, 0.05, 0.05)
	skBox = mc.listRelatives(skBoxShape, parent=True)
	mc.setAttr((skBox[0] + '.displayRotatePivot'), 1)
	mc.setAttr((skBox[0] + '.translate'), skPosX, skPosY, skPosZ)
	skBoxFnlName = mc.rename(skBox[0], skBoxName)
	try:
		if len(parentObj): mc.parent(skBoxFnlName , parentObj)
	except TypeError:
		pass
	return skBoxFnlName

#-------------------------------------------------------------------------------------------------#
#	Description -- Creating a curve throught objects
def crvfromobjs(skObjs):
	skCrvPos = []
	for skO in skObjs:
		skPos = mc.xform(skO, query=True, worldSpace=True, translation=True)
		skCrvPos.append(tuple(skPos))
	skCrvGrp = 'Grp_Curves_Tmpl'
	skClusGrp = 'GrpCluster_Tmpl'
	if mc.objExists(skCrvGrp) != True:
		mc.group(name = skCrvGrp, empty=True)
		mc.setAttr((skCrvGrp + '.template'), 1, lock=True)
	skCurv = mc.curve(p=skCrvPos, degree=1)
	mc.parent(skCurv, skCrvGrp)
	skCurvShp = mc.listRelatives(skCurv, children=True, shapes=True)
	skSpan = mc.getAttr((skCurvShp[0] + '.spans'))
	if mc.objExists(skClusGrp) != True:
		mc.group(name = skClusGrp, empty=True)
		mc.setAttr((skClusGrp + '.template'), 1, lock=True)
		mc.setAttr((skClusGrp + '.v'), 0, lock=True)
	skClus = []
	mc.select(clear=True)
	for i in range(skSpan + 1):
		skClusTmp = mc.cluster((skCurv + '.cv[' + str(i) + ']'), relative=True)
		skClus.append(skClusTmp[1])
		mc.parent(skClus[i], skClusGrp)
		mc.parentConstraint(skObjs[i], skClusTmp[1], mo = True)
	if mc.objExists('Grp_Others') != True:
		mc.group(name = 'Grp_Others', empty = True)
	if mc.listRelatives(skCrvGrp, parent = True) != ['Grp_Others']:
		mc.parent(skCrvGrp, 'Grp_Others')
	if mc.listRelatives(skClusGrp, parent = True) != ['Grp_Others']:
		mc.parent(skClusGrp, 'Grp_Others')

#-------------------------------------------------------------------------------------------------#		
#	Description -- This will return the Name of Skin Cluster
def idsknclus(skObject):
	skHistory = mc.listHistory(skObject)
	for i in range(len(skHistory)):
		if mc.nodeType(skHistory[i]) == 'skinCluster':
			return skHistory[i]
			break
	return 'None'
	
#-------------------------------------------------------------------------------------------------#
#	Description -- This will Flatten the selection of an Array
def flatten(skList):
	skSeled = mc.ls(sl = True)
	mc.select(skList, replace = True)
 	skNewList = mc.ls(sl = True, fl = True)
	mc.select(skSeled, r = True)
	return skNewList
	
#-------------------------------------------------------------------------------------------------#
#	Description -- Joint Orient
def jnt_orient(joints,aimAxisD,upAxisD,upDire):
	
	dic = {'x':(1,0,0),'y':(0,1,0),'z':(0,0,1),'-x':(-1,0,0),'-y':(0,-1,0),'-z':(0,0,-1)}
	aimAxis = dic[aimAxisD]
	upAxis  = dic[upAxisD]
	upDir   = dic[upDire]
	njnt    = len(joints)
	prevUp  = [0,0,0]
	childs  =[]
	parentlist = []
	
	### Orient each joint ###
	for i in range(0,njnt,1):
		child  = mc.listRelatives (joints[i],children=True,type=('transform','joint'))
		if child != None:
			childs.append(child)
			if len(childs)>0:
				parents = mc.listRelatives (joints[i], parent = True)
				parentlist.append(parents)
				child = mc.parent (child, w=True)
				parent = parentlist[0]
			for childl in childs:
				if mc.nodeType(childl[0])=='joint':
					aimTgt = childl[0]
			if aimTgt != '':
				upVec = upDir
				aCons = mc.aimConstraint (aimTgt,joints[i],
								aim =(aimAxis[0],aimAxis[1],aimAxis[2]),
								upVector =(upAxis[0],upAxis[1],upAxis[2]),
								worldUpVector =(upVec[0],upVec[1],upVec[2]),worldUpType='vector')
				mc.delete (aCons)	
				mag   = pow((upVec[0]*upVec[0]+upVec[1]*upVec[1]+upVec[2]*upVec[2]),0.5)
				curUpr = (upVec[0]/mag,upVec[1]/mag,upVec[2]/mag)
				dotlist = []
				for j in range(0,3,1):
					dot	=  curUpr[j]*prevUp[j]
					dotlist.append(dot)
					prevUp[j] = upVec[j]
				if i > 0 and dotlist[0]== 0 and dotlist[1]== 0 and dotlist[2]== 0 :
						mc.xform (joints[i],r=True,os=True,ra= ((aimAxis[0]*180),(aimAxis[1]*180),(aimAxis[2]*180)))
						for t in range(0,3,1): prevUp[t] *= -1.0
				mc.joint (joints[i],e =True,zso=True)
				mc.makeIdentity (joints[i],a=True)
			elif parent != '':
				oCons = mc.orientConstraint (parent,joints[i],weight=1.0)
				mc.delete(oCons)
				mc.joint (joints[i],e =True,zso=True)
				mc.makeIdentity (joints[i],a=True)
			if len(childs) >0:
				mc.parent (child,joints[i])
		else :
			mc.joint (joints[i],e =True,zso=True)
			mc.makeIdentity (joints[i],a=True)
			mc.setAttr(joints[i]+'.jointOrient',0,0,0)

#----------------------------------------------------------------------------------------------------#
#	Description -- This will Create Joints Along the selected Objects
def ar_jointsAlongObjects(objects , orientationSwitch = 1,chainSwitch = 1,parent = 0):
	mc.select(cl = True)
	JntList = []
	for i in range(len(objects)):
		jntName = objects[i].replace('_Tmpl','_CJ')
		if chainSwitch == 0:mc.select(cl = True)
		if parent:
			parentTmpl = mc.listRelatives(objects[i], p = True)[0].replace('_Tmpl','_CJ')
			jnt = mc.joint(n = jntName)
			mc.parent(jnt , parentTmpl)
		else:
			jnt = mc.joint(n = jntName)
		mc.delete(mc.pointConstraint(objects[i],jnt))
		JntList.append(jnt)
		if i >= 1:
			mc.joint(JntList[i - 1] , edit = True , zso = True , oj = 'xyz' , sao = 'yup')
	if orientationSwitch :
		if 'Right' in JntList[0]:
			tools.jnt_orient(JntList,'-x','-z','z')
		else:
			tools.jnt_orient(JntList,'x','z','z')
	return JntList

#----------------------------------------------------------------------------------------------------#
#	Description -- This will Create Joints Along a Curve
def ar_jointsAlongCurve(objects , name , jntsNo = 7 , chainSwitch = 1):
	jntArray = []
	curPos = []
	for obj in objects:
		queryPosition = mc.xform(obj , q = True ,t = 1, ws = 1)
		curPos.append(tuple(queryPosition))
	cur = mc.curve( p = curPos , d = 2)
	pathVal = 1.00/(jntsNo - 1)
	for i in range(jntsNo):
		mc.cycleCheck(e = 0)
		if i == 0 or chainSwitch == 0 :mc.select(cl = 1)	
		jnt = mc.joint(n = (name + '%d_CJ' % i))
		jntArray.append(jnt)
		tmpLoc = mc.spaceLocator()
		mPath = mc.pathAnimation(tmpLoc[0] ,c = cur, fractionMode = True , follow =  False , followAxis = 'x' , upAxis = 'y' , worldUpType = "vector" , worldUpVector = [0,1,0])
		mc.cutKey(mPath , cl = True , at = "u")
		mc.setAttr((mPath + '.uValue'), (pathVal * i))
		mc.delete(mc.pointConstraint(tmpLoc[0] , jnt) , mPath , tmpLoc[0] )
		mc.select(jnt)
	mc.delete(cur)
	tools.jnt_orient(jntArray,'x','z','z')
	return jntArray
	
#**************************************************END**************************************************#