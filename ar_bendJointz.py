											#--------------------------------------------------------------#
											# 	DESCRIPTION	: Python Module for Creating Bend Joints       #	
											#									for Arms or Legs														 # 																		   
											# 	AUTHOR 			: Arun . S - arunpillaii@gmail.com             #                    												                       				                     
											# 	VERSION			: 1.00 , 10 November 2009                      #
											#   Copyright (C) 2011.  All rights reserved.									 #
											#--------------------------------------------------------------#
#Imports!					
import maya.cmds as mc
import maya.OpenMaya as om
import ar_rigTools as tools

# StBJ = StartJoint 
#  EnBJ = Endjoint 
# BJSide = Side (Left/Right) 
# BJlimb = Arm/Leg 
# BJpos = position of limb(Up/Dn)


def ar_crtBendJntz(StBJ , EnBJ , BJSide , BJlimb , BJpos , noJnts):
	selJnts = [StBJ , EnBJ]
	startEndJoints = mc.duplicate(selJnts[:3] , rc = True, po = True)
	mc.parent(startEndJoints[0] , w = True)
	
	#Creating 'n' number of joints between Start and end
	splitJoints = ar_splitJointz(startEndJoints[0] , startEndJoints[1] , noJnts)
	for i in range(len(splitJoints)): splitJoints[i] = mc.rename(splitJoints[i] , ((BJSide + BJlimb) +  BJpos + 'Bend%d_CJ' % i))
	tools.jnt_orient(splitJoints,'x','z','z')
	
#	splitJointsGrp = mc.group(em = 1 , n = ('g%sBend_CJ' % (BJSide + BJlimb) +  BJpos))
#	mc.delete(mc.parentConstraint(StBJ , splitJointsGrp))
#	mc.parent(splitJoints[0] , splitJointsGrp)
#	mc.parentConstraint(StBJ , splitJointsGrp)
#	mc.scaleConstraint(StBJ , splitJointsGrp)
	mc.parent(splitJoints[0] , StBJ)
	
	#Creating Ik Handle and Clusters
	bendIk = mc.ikHandle(n = ((BJSide + BJlimb) +  BJpos + 'BendIK'), sol = 'ikSplineSolver' , pcv = False , sj = splitJoints[0] , ee = splitJoints[(len(splitJoints) - 1)])
	bendIkCurve = mc.rename(bendIk[2] , ((BJSide + BJlimb) +  BJpos + 'BendIKCurve'))
	startCluster = mc.cluster((bendIkCurve + '.cv[0]') ,  n = ((BJSide + BJlimb) +  BJpos + 'BendSrtClu'))
	mc.setAttr((startCluster[1] + '.v') , 0 , l = 1)
	midCluster = mc.cluster((bendIkCurve + '.cv[1]') , (bendIkCurve + '.cv[2]') ,  n = ((BJSide + BJlimb) +  BJpos + 'BendMidClu'))
	mc.setAttr((midCluster[1] + '.v') , 0 , l = 1)
	endCluster = mc.cluster((bendIkCurve + '.cv[3]') ,  n = ((BJSide + BJlimb) +  BJpos + 'BendEndClu'))
	mc.setAttr((endCluster[1] + '.v') , 0 , l = 1)
	mc.parent(startCluster[1] , StBJ)
	mc.parent(endCluster[1] , EnBJ)
	mc.orientConstraint(EnBJ,splitJoints[len(splitJoints)-1], mo = 1)
	
	#Create and positioning Bend control
	bendCtrl = mc.circle(nr = [1 , 0 , 0] , r = .2 , d = 1 , ut = 0 , s = 8 , ch = 0 , n = ('Ctrl_%sBend' %  (BJSide + BJlimb) + BJpos))
	mc.addAttr(bendCtrl[0] , k = 1 , ln = 'UpTwist' , at = 'double')
	mc.addAttr(bendCtrl[0] , k = 1 , ln = 'DnTwist' , at = 'double')
	bendCtrlGrp = mc.group(bendCtrl[0] , n = ('Grp_%sBend' %  (BJSide + BJlimb) +  BJpos))
	mc.pointConstraint(StBJ , EnBJ , bendCtrlGrp)
	mc.orientConstraint(StBJ , bendCtrlGrp)
	mc.parent(midCluster[1] , bendCtrl[0])
	
	#Add Stretching to the Bend Joints	
	arclength = mc.arclen(bendIkCurve , ch = True)
	curveInfo = mc.rename(arclength , ((BJSide + BJlimb) +  BJpos + 'BdCurveInfo'))
	multiDiv01 = mc.createNode('multiplyDivide' , n = ('pScale%sMd01' % (BJSide + BJlimb) +  BJpos))
	multiDiv02 = mc.createNode('multiplyDivide' , n = ((BJSide + BJlimb) +  BJpos + 'MMd02'))
	multiDiv03 = mc.createNode('multiplyDivide' , n = ((BJSide + BJlimb) +  BJpos + 'MMd03'))
	mc.setAttr((multiDiv01 + ".operation") , 2)
	mc.setAttr((multiDiv02 + ".operation") , 2)
	mc.setAttr((multiDiv02 + ".input2X") , (mc.getAttr(curveInfo + '.arcLength')))
	mc.setAttr((multiDiv03 + ".input2X") , (mc.getAttr(splitJoints[1] + '.tx')))
	
	mc.connectAttr((curveInfo + ".arcLength") , (multiDiv01 + ".input1X"))
	mc.connectAttr((multiDiv01 + ".outputX") , (multiDiv02 + ".input1X"))
	mc.connectAttr((multiDiv02 + ".outputX") , (multiDiv03 + ".input1X"))
	for i in range(1,(len(splitJoints))):
		mc.connectAttr((multiDiv03 + ".outputX") , (splitJoints[i] + ".tx") )
	
	#Create locator for Up and Dn positions	
	if BJpos == 'Up':
		startLoc = mc.spaceLocator(n = ("Ctrl_%sTwistOff" % (BJSide + BJlimb) +  BJpos))
		mc.setAttr ((startLoc[0] + 'Shape.localScale') , .1 , .1 , .1)
		mc.setAttr ((startLoc[0] + '.v') , 0 , l = True)
		startLocGrp = mc.group(startLoc[0],n = ("Grp_%sTwistOff" % (BJSide + BJlimb) +  BJpos))
		mc.parentConstraint(StBJ ,startLocGrp)
		stLOC = startLoc[0]
		if BJlimb == 'Arm':
				clvCtrl = 'Ctrl_%sClavicle' % BJSide
				if mc.objExists(clvCtrl):
					mc.addAttr(clvCtrl,ln='ShoulderTwist',at='double')
					mc.setAttr(clvCtrl+'.ShoulderTwist',e=1,k=1)
					pmN=mc.createNode('plusMinusAverage',n=BJSide+'ShoulderTwistSum_PMA')
					mc.connectAttr(bendCtrl[0] + '.UpTwist',pmN+'.input1D[0]')
					mc.connectAttr(clvCtrl+'.ShoulderTwist',pmN+'.input1D[1]')
					mc.connectAttr(pmN+'.output1D',stLOC + '.rx')
		else:
			mc.connectAttr(bendCtrl[0] + '.UpTwist',stLOC + '.rx')
		
		sumPMA = mc.createNode('plusMinusAverage' , n = (BJSide + BJlimb + 'MidSun_PMA'))
		endLoc = ("Ctrl_%sMidTwistOff" % BJSide + BJlimb)
		edLOC = endLoc
		if not mc.objExists(endLoc):
			endLoc = mc.spaceLocator(n = ("Ctrl_%sMidTwistOff" % BJSide + BJlimb))
			mc.setAttr ((endLoc[0] + '.v') , 0 , l = True)
			mc.setAttr ((endLoc[0] + 'Shape.localScale') , .1 , .1 , .1)
			endLocGrp = mc.group(endLoc[0],n = ("Grp_%sMidTwistOff" % BJSide + BJlimb))
			mc.parentConstraint(EnBJ ,endLocGrp)
			edLOC = endLoc[0]
		mc.connectAttr(bendCtrl[0] + '.DnTwist', sumPMA + '.input1D[0]')
		mc.connectAttr(sumPMA + '.output1D' , edLOC + '.rx')
		
	if BJpos == 'Dn':	
		startLoc = ("Ctrl_%sMidTwistOff" % BJSide + BJlimb)
		stLOC = startLoc
		startLocGrp = ("Grp_%sTwistOff" % (BJSide + BJlimb) +  BJpos)
		if not mc.objExists(startLoc):
			startLoc = mc.spaceLocator(n = ("Ctrl_%sMidTwistOff" % BJSide + BJlimb))
			mc.setAttr ((startLoc[0] + 'Shape.localScale') , .1 , .1 , .1)
			mc.setAttr ((startLoc[0] + '.v') , 0 , l = True)
			startLocGrp = mc.group(startLoc[0],n = ("Grp_%sMidTwistOff" % BJSide + BJlimb))
			mc.parentConstraint(StBJ ,startLocGrp)
			stLOC = startLoc[0]
		lstCon = mc.listConnections(stLOC + '.rx' ,scn = True , type = 'plusMinusAverage')
		if lstCon :
			mc.connectAttr(bendCtrl[0] + '.UpTwist', lstCon[0] + '.input1D[1]')
			
		endLoc = mc.spaceLocator(n = ("Ctrl_%sTwistOff" % (BJSide + BJlimb) +  BJpos))
		mc.setAttr ((endLoc[0] + '.v') , 0 , l = True)
		mc.setAttr ((endLoc[0] + 'Shape.localScale') , .1 , .1 , .1)
		endLocGrp = mc.group(endLoc[0],n = ("Grp_%sTwistOff" % (BJSide + BJlimb) +  BJpos))
		mc.parentConstraint(EnBJ ,endLocGrp)
		edLOC = endLoc[0]
		mc.connectAttr(bendCtrl[0] + '.DnTwist',edLOC + '.rx')
	
	#connecting locator to 	ik handle and set attributes
	mc.setAttr((bendIk[0] + ".dTwistControlEnable") , 1)
	mc.setAttr((bendIk[0] + ".dWorldUpType") , 4)
	mc.connectAttr ((stLOC + ".worldMatrix[0]"), (bendIk[0] + ".dWorldUpMatrix"))
	mc.connectAttr ((edLOC + ".worldMatrix[0]"), (bendIk[0] + ".dWorldUpMatrixEnd"))
	
	#Lock n Hide Attributes
	tools.lockhide(stLOC, ["rx"])
	tools.lockhide(edLOC, ["rx"])
	tools.lockhide(bendCtrl[0], ["tx", "ty", "tz"])
	
	#Sys Group
	if not mc.objExists('Sys_%sBend' % (BJSide + BJlimb)): 
		mc.group(em = 1 ,  n = ('Sys_%sBend' % (BJSide + BJlimb)))
		mc.setAttr(('Sys_%sBend.v' % (BJSide + BJlimb)) , 0 , l = 1)
		mc.parent(('Sys_%sBend' % (BJSide + BJlimb)) , ('Sys_%ss' % BJlimb))
#	mc.parent(bendIk[0] , bendIkCurve , splitJointsGrp ,('Sys_%sBend' % (BJSide + BJlimb)))
	mc.parent(bendIk[0] , bendIkCurve , ('Sys_%sBend' % (BJSide + BJlimb)))
	
	#Control Group
	if not mc.objExists('Grp_%sBend' % (BJSide + BJlimb)): 
		mc.group(em = 1 ,  n = ('Grp_%sBend' % (BJSide + BJlimb)))
		mc.parent(('Grp_%sBend' % (BJSide + BJlimb)) , ('Grp_%ss' % BJlimb))
	mc.parent(startLocGrp , endLocGrp , bendCtrlGrp ,('Grp_%sBend' % (BJSide + BJlimb)))
	return ('Grp_%sBend' % (BJSide + BJlimb)),('Sys_%sBend' % (BJSide + BJlimb)) , splitJoints[0],bendCtrl[0]
	
#------------------------------------------------------------------------------------------------------------#
	
# def for creating split joints
def ar_splitJointz(startJnt,endJnt, divNo):
	if not endJnt in (mc.listRelatives(startJnt , c = True , ad = True)):
		om.MGlobal.displayError("Start joint and End Joint are not in  single Hieracy")
		return
	childJnt = mc.listRelatives(startJnt , c = 1 , type = 'joint')
	getTransVal = mc.getAttr(childJnt[0] + '.t')
	tranXVal = getTransVal[0][0] / (divNo + 1)
	tranYVal = getTransVal[0][1] / (divNo + 1)
	tranZVal = getTransVal[0][2] / (divNo + 1)
	joints =  [startJnt]
	for i in range(divNo):
		jnt = mc.duplicate(startJnt , po = 1 , n  = (startJnt + '_split%d' % (i + 1)))
		if i == 0 :
			mc.parent(jnt[0],startJnt)
		else:
			mc.parent(jnt[0] , joints[i])
		mc.setAttr((jnt[0] + '.t') , tranXVal , tranYVal , tranZVal)
		if i == (divNo - 1):
			mc.parent(childJnt[0] , jnt[0])
		joints.append(jnt[0])
	joints.append(endJnt)
	return joints

#**************************************************END**************************************************#
