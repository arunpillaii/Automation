											#-----------------------------------------------------------#
											# 	DESCRIPTION	: Python Module for Rig Arms				#	 																		   
											# 	AUTHOR 		: Arun . S - arunpillaii@gmail.com			#                    												                       				                     
											# 	VERSION		: 2.00 , 17 October 2011		            #
											#   Copyright (C) 2011.  All rights reserved.				#
											#-----------------------------------------------------------#

#importing Modules
import maya.cmds as mc
import maya.mel as mm
import sk_ctrlCurves as scc
import ar_rigTools as tools
import ar_bendJointz as BJ
import re
from ar_SDK import *

#def ar_rigArms(clavJnt = 'LeftClavicle_CJ' , side = 'Left',bendOnOff=1):
def ar_rigArms(clavJnt, side, bendOnOff, bendJnts, chrScale=1):

	mainprogressbar = mm.eval("global string $gMainProgressBar;string $tmp=$gMainProgressBar")
	mc.progressBar(mainprogressbar,edit=True,bp=True,isInterruptable=True,status=('Rigging %s Arms' % side))

	sel = mc.ls(clavJnt , dag = 1)
	armJnts = sel[0:4]
	spineJnt = mc.listRelatives(armJnts[0], p = True)
	ikJoints,fkJoints = [],[]
	
	#Creating IKFK joints
	ikJnts = mc.duplicate(armJnts[1:],po = 1 ,rc = 1)
	fkJnts = mc.duplicate(armJnts[1:], po = 1 ,rc = 1)
	mc.parent(ikJnts[0],fkJnts[0], w = True)
	
	#Renaming IKFK Joints
	for i in range(len(ikJnts)):
		namepref = ikJnts[i].split('_CJ')
		ikJoints.append(mc.rename(ikJnts[i] ,  (namepref[0] + "_IK")))
		fkJoints.append(mc.rename(fkJnts[i] ,  (namepref[0] + "_FK")))
	
	#setPreferredAngle to Ik Elbow joint
	mc.setAttr((ikJoints[1] + ".preferredAngleY"), -90)
	mc.progressBar(mainprogressbar,edit=True,step=10)

	#Creating System , main and Anchor group
	grpIKFK = mc.group(em = True,n = ("Sys_%sHdIkFkJnts" % side))
	mc.delete(mc.pointConstraint(armJnts[0],grpIKFK))
	mc.parentConstraint(armJnts[0],grpIKFK , mo  = 1)
	mc.scaleConstraint(armJnts[0],grpIKFK)
	mc.parent(ikJoints[0],fkJoints[0],grpIKFK)
	if mc.objExists("Sys_Arms"):
		sysGrp = "Sys_Arms"
	else:
		sysGrp = mc.group(em = True,n = "Sys_Arms")
	mc.parent(grpIKFK,sysGrp)
	
	if mc.objExists("Anchor_Torso"):
		anchorGrp = "Anchor_Torso"
	else:
		anchorGrp = mc.group(em = True,n = "Anchor_Torso")
		try:
			if len(spineJnt) != 0:
				mc.delete(mc.parentConstraint(spineJnt[0],anchorGrp))
				mc.parent(anchorGrp , spineJnt[0])
		except TypeError:
			pass
	if mc.objExists("Grp_Arms"):
		mainGrp = "Grp_Arms"
	else:
		mainGrp = mc.group(em = True,n = "Grp_Arms")
	
	#Control Creation
	armCtrlsDic = {
		'clavicle':("Ctrl_%sClavicle" % side),
		'shoulderFK':("Ctrl_%sShoulderFK" % side),
		'elbowFK':("Ctrl_%sElbowFK" % side),
		'wristFK':("Ctrl_%sWristFK" % side),
		'elbowPole':("Ctrl_%sElbowPole" % side),
		'arm':("Ctrl_%sArm" % side),
		'ArmIKFK' :("Ctrl_%sArmIKFK" % side),
		'gimbal':("Ctrl_%sHandGimbal" % side),
		'hand':("Ctrl_%sHand" % side)
	}
	armCtrlsGrpDic = {
		'clavicleGrp':("Grp_%sClavicle" % side),
		'shoulderFKGrp':("Grp_%sShoulderFK" % side),
		'elbowFKGrp':("Grp_%sElbowFK" % side),
		'wristFKGrp':("Grp_%sWristFK" % side),
		'elbowPoleGrp':("Grp_%sElbowPole" % side),
		'armGrp':("Grp_%sArm" % side),
		'ArmIKFKGrp' :("Grp_%sArmIKFK" % side),
		'gimbalGrp':("Grp_%sHandGimbal" % side),
		'handGrp':("Grp_%sHand" % side)
	}

	inst = scc.Ctrlcurve(armCtrlsDic['clavicle'], (.05*chrScale))
	inst.box()
	inst.rotorder()
	mc.group(armCtrlsDic['clavicle'] , n = armCtrlsGrpDic['clavicleGrp'])
	mc.addAttr(armCtrlsDic['clavicle'] , ln='AutoStretch' ,at = 'long', min=0 , max=1 , k=True)
	mc.delete(mc.pointConstraint(armJnts[1],armCtrlsGrpDic['clavicleGrp']))
	
	inst = scc.Ctrlcircle(armCtrlsDic['shoulderFK'],(.1*chrScale),[1,0,0])
	inst.doubleshape()
	inst.rotorder()
	mc.group(armCtrlsDic['shoulderFK'] , n = armCtrlsGrpDic['shoulderFKGrp'])
	mc.delete(mc.parentConstraint(armJnts[1],armCtrlsGrpDic['shoulderFKGrp']))
	
	inst = scc.Ctrlcircle(armCtrlsDic['elbowFK'],(.08*chrScale),[1,0,0])
	inst.doubleshape()
	inst.rotorder()
	mc.group(armCtrlsDic['elbowFK'] , n = armCtrlsGrpDic['elbowFKGrp'])
	mc.delete(mc.parentConstraint(armJnts[2],armCtrlsGrpDic['elbowFKGrp']))
	
	inst = scc.Ctrlcircle(armCtrlsDic['wristFK'],(.08*chrScale),[1,0,0])
	inst.doubleshape()
	inst.rotorder()
	mc.group(armCtrlsDic['wristFK'] , n = armCtrlsGrpDic['wristFKGrp'])
	mc.delete(mc.parentConstraint(armJnts[3],armCtrlsGrpDic['wristFKGrp']))
	
	inst = scc.Ctrlcurve(armCtrlsDic['elbowPole'], (.1*chrScale))
	inst.square()
	mc.setAttr((armCtrlsDic['elbowPole'] + ".rx"),90)
	mc.setAttr((armCtrlsDic['elbowPole'] + ".rz"),45)
	mc.makeIdentity(apply = True,r = 1)
	mc.addAttr(armCtrlsDic['elbowPole'] , ln='ElbowLock' , min=0 , max=1 , k=True)
	mc.group(armCtrlsDic['elbowPole'] , n = armCtrlsGrpDic['elbowPoleGrp'])
	mc.delete(mc.pointConstraint(armJnts[2],armCtrlsGrpDic['elbowPoleGrp']))
	mc.setAttr((armCtrlsGrpDic['elbowPoleGrp']+ ".tz"),(-4.5*chrScale))
	
	inst = scc.Ctrlcurve(armCtrlsDic['arm'], (.1*chrScale))
	inst.box()
	inst.rotorder()
	mc.group(armCtrlsDic['arm'] , n = armCtrlsGrpDic['armGrp'])
	mc.delete(mc.parentConstraint(armJnts[3],armCtrlsGrpDic['armGrp']))
	
	inst = scc.Ctrlcurve(armCtrlsDic['ArmIKFK'], (.08*chrScale))
	inst.ikfk()
	mc.setAttr(armCtrlsDic['ArmIKFK'] + '.tz' , -.5)
	mc.group(armCtrlsDic['ArmIKFK'] , n = armCtrlsGrpDic['ArmIKFKGrp'])
	mc.parentConstraint(armJnts[3],armCtrlsGrpDic['ArmIKFKGrp'])
	
	inst = scc.Ctrlcircle(armCtrlsDic['gimbal'],(.08*chrScale),[1,0,0])
	inst.rotorder()
	tmpcir1 = mc.circle(n = (armCtrlsDic['gimbal'] + '1'),nr = [0 , 1 , 0] , r =  .1 , ch = 0)
	tmpcir2 = mc.circle(n = (armCtrlsDic['gimbal'] + '2'),nr = [ 0 , 0 , 1] , r =  .1 , ch = 0)
	mc.parent((armCtrlsDic['gimbal'] + '1Shape') , (armCtrlsDic['gimbal'] + '2Shape') , armCtrlsDic['gimbal'], r = 1 , s = 1 )
	mc.delete(tmpcir1,tmpcir2)
	mc.group(armCtrlsDic['gimbal'] , n = armCtrlsGrpDic['gimbalGrp'])
	mc.pointConstraint(armJnts[3],armCtrlsGrpDic['gimbalGrp'])
	mc.orientConstraint(armCtrlsDic['gimbal'],armJnts[3])
	
	handSide = 0
	if side == 'Right':handSide = 1
	inst = scc.Ctrlcurve(armCtrlsDic['hand'], (1*chrScale))
	inst.hand(handSide)
	mc.group(armCtrlsDic['hand'] , n = armCtrlsGrpDic['handGrp'])
	mc.xform(armCtrlsGrpDic['handGrp'],os = 1, piv = [0,0,0])
	mc.parentConstraint(armJnts[3],armCtrlsGrpDic['handGrp'])
	mc.progressBar(mainprogressbar,edit=True,step=10)

	#Creating Elbow Annotation Arrow
	locAnno = mc.spaceLocator(n = ("Loc_%sElbowArrow" % side))
	mc.delete(mc.parentConstraint((armCtrlsDic['elbowPole'],locAnno[0])))
	mc.parent(locAnno[0],armCtrlsDic['elbowPole'])
	tmpAnno = mc.annotate(locAnno[0],tx = "")
	mc.rename(tmpAnno,(side + "ElbowAnnotationShape"))
	tranAnno = mc.listRelatives((side + "ElbowAnnotationShape"),p = 1)
	mc.rename(tranAnno[0],(side + "ElbowAnnotation"))
	mc.parentConstraint(ikJoints[1] ,(side + "ElbowAnnotation"))
	mc.parent((side + "ElbowAnnotation"),locAnno[0])
	mc.setAttr((locAnno[0] + "Shape.v"),0)
	mc.setAttr((locAnno[0] + "Shape.v"),l = 1)
	mc.setAttr((side + "ElbowAnnotation.template"),1)
	
	#Creating Clavicle and Arm IkHandles
	clavicleIkHandle = mc.ikHandle(sj = armJnts[0], ee = armJnts[1], sol = 'ikSCsolver', n = (side + 'ClavicleIkHandle') )
	mc.parent(clavicleIkHandle[0],armCtrlsDic['clavicle'])
	mc.setAttr((clavicleIkHandle[0] + '.v') , 0 )
	mc.setAttr((clavicleIkHandle[0] + '.v') , l = 1)
	
	#clavical stretch
	clavStretchStartLoc = mc.spaceLocator(n = ("Loc_%sClavDimStart" % side))
	clavStretchEndLoc = mc.spaceLocator(n = ("Loc_%sClavDimEnd" % side))
	mc.pointConstraint(armJnts[0],clavStretchStartLoc[0])
	mc.pointConstraint(armCtrlsDic['clavicle'],clavStretchEndLoc[0])
	dimensionShape = mc.createNode('distanceDimShape' , n = side + 'ClavDistDimShape')
	mc.rename((mc.listRelatives(dimensionShape, p = True)),  side + 'ClavDistDim')
	dimensionTrans = mc.listRelatives(dimensionShape , p = True)[0]
	mc.connectAttr((clavStretchStartLoc[0] + 'Shape.worldPosition[0]') ,(dimensionShape + '.startPoint'), f= True)
	mc.connectAttr((clavStretchEndLoc[0] + 'Shape.worldPosition[0]') ,(dimensionShape + '.endPoint'))
	
	strScaleClavMD = mc.createNode('multiplyDivide' , n = ("pScale_%sClav_MD" % side))
	mc.setAttr((strScaleClavMD + ".operation"), 2)

	strDivideClavMD = mc.createNode('multiplyDivide' , n = (side + 'ClavDivide_MD'))
	mc.setAttr((strDivideClavMD + ".operation"), 2)
	mc.setAttr((strDivideClavMD + ".input2X"), (mc.getAttr(dimensionShape + '.distance')))
	clavSwitchCD = mc.createNode('condition' , n = (side + 'ClavSwitch_Con'))
	mc.setAttr((clavSwitchCD + ".secondTerm"), 1)
	mc.setAttr((clavSwitchCD + '.colorIfFalseR'), 1)
	clavStrMD = mc.createNode('multiplyDivide' , n = (side + 'Clavicle_MD'))
	mc.setAttr((clavStrMD + ".input1X"), (mc.getAttr(armJnts[1] + '.tx')))

	mc.connectAttr((dimensionShape + '.distance') , (strScaleClavMD + '.input1X'))
	mc.connectAttr((strScaleClavMD + '.outputX') ,  (strDivideClavMD + '.input1X'))	
	
	mc.connectAttr((armCtrlsDic['clavicle'] + '.AutoStretch') , (clavSwitchCD + '.firstTerm'))
	mc.connectAttr((strDivideClavMD + '.outputX'), (clavSwitchCD + '.colorIfTrueR'))
	mc.connectAttr((clavSwitchCD + '.outColorR'), (clavStrMD + '.input2X'))

	mc.connectAttr((clavStrMD + '.outputX'), (armJnts[1] + '.tx'))

	if not mc.objExists('Grp_ArmDimensions'):
		grpDimensions = mc.group(em = 1 , p = sysGrp, n = 'Grp_ArmDimensions')
	else:
		grpDimensions = 'Grp_ArmDimensions'
	mc.parent(clavStretchStartLoc[0] , clavStretchEndLoc[0] , dimensionTrans , grpDimensions)
	
	armIkHandle = mc.ikHandle(sj = ikJoints[0], ee = ikJoints[2], sol = 'ikRPsolver' , n = (side + 'ArmIkHandle') )
	mc.parent(armIkHandle[0],armCtrlsDic['arm'])
	mc.setAttr((armIkHandle[0] + '.v') , 0 )
	mc.setAttr((armIkHandle[0] + '.v') , l = 1)
	mc.poleVectorConstraint((armCtrlsDic['elbowPole']),armIkHandle[0])
	mc.progressBar(mainprogressbar,edit=True,step=10)
	
	#Fk joints and Control Constraining
	mc.orientConstraint(armCtrlsDic['shoulderFK'],fkJoints[0])
	mc.pointConstraint(fkJoints[0],armCtrlsGrpDic['shoulderFKGrp'])
	mc.orientConstraint(anchorGrp,armCtrlsGrpDic['shoulderFKGrp'],mo = True)
	
	mc.orientConstraint(armCtrlsDic['elbowFK'],fkJoints[1])
	mc.pointConstraint(fkJoints[1],armCtrlsGrpDic['elbowFKGrp'])
	mc.orientConstraint(fkJoints[0],armCtrlsGrpDic['elbowFKGrp'],mo = True)

	mc.orientConstraint(armCtrlsDic['wristFK'],fkJoints[2])
	mc.pointConstraint(fkJoints[2],armCtrlsGrpDic['wristFKGrp'])
	mc.orientConstraint(fkJoints[1],armCtrlsGrpDic['wristFKGrp'],mo = True)
	
	#constrainting IKFK Joints to main joints and connecting controls
	mc.addAttr(armCtrlsDic['ArmIKFK'], ln ='GimbalControl', at = 'bool', k = False)
	mc.setAttr((armCtrlsDic['ArmIKFK'] + '.GimbalControl'), cb = True)
	mc.connectAttr((armCtrlsDic['ArmIKFK'] + '.GimbalControl') , (armCtrlsDic['gimbal'] + '.v'))
	IkFkReverse = mc.createNode('reverse' , n = (side + 'ArmIkFk_Rev'))
	mc.connectAttr((armCtrlsDic['ArmIKFK'] + '.IKFK'),(IkFkReverse + '.inputX'))
	
	#additional constraint for clavical stretch
	mc.pointConstraint(armJnts[1],ikJoints[0])
	mc.pointConstraint(armJnts[1],fkJoints[0])
	
	for i in range(3):
		constObject = armJnts[i+1]
		if i == 2:constObject = armCtrlsGrpDic['gimbalGrp']
		orintCon = mc.orientConstraint(fkJoints[i] , ikJoints[i] , constObject)
		targetList = mc.orientConstraint(orintCon[0] , q = True , tl = True)
		mc.connectAttr((armCtrlsDic['ArmIKFK'] + '.IKFK'),(orintCon[0] + '.%sW0'% targetList[0]))
		mc.connectAttr((IkFkReverse + '.outputX'),(orintCon[0] + '.%sW1'% targetList[1]))
	
	elbowBlendColors = mc.createNode('blendColors' , n = (side + "Elbow_BC"))
	mc.connectAttr((fkJoints[1] + '.tx'), (elbowBlendColors + '.color1R'))
	mc.connectAttr((ikJoints[1] + '.tx'), (elbowBlendColors + '.color2R'))
	mc.connectAttr((elbowBlendColors + '.outputR'), (armJnts[2] + '.tx'))
	mc.connectAttr((armCtrlsDic['ArmIKFK'] + '.IKFK') , (elbowBlendColors + '.blender'))
	
	wristBlendColors = mc.createNode('blendColors' , n = (side + "Wrist_BC"))
	mc.connectAttr((fkJoints[2] + '.tx'), (wristBlendColors + '.color1R'))
	mc.connectAttr((ikJoints[2] + '.tx'), (wristBlendColors + '.color2R'))
	mc.connectAttr((wristBlendColors + '.outputR'), (armJnts[3] + '.tx'))
	mc.connectAttr((armCtrlsDic['ArmIKFK'] + '.IKFK') , (wristBlendColors + '.blender'))
		
	ikFkVisCondition = mc.createNode('condition' , n = (side + "ArmIkFkVis_Con"))
	ikFkVisReverse = mc.createNode('reverse' , n = (side + "ArmIkFkVis_Rev"))
	mc.setAttr((ikFkVisCondition + '.secondTerm'), 1)
	mc.setAttr((ikFkVisCondition + '.colorIfTrueR'), 1)
	mc.connectAttr((armCtrlsDic['ArmIKFK'] + '.IKFKControls'),(ikFkVisCondition + ".firstTerm"))
	mc.connectAttr((armCtrlsDic['ArmIKFK'] + '.IKFK'),(ikFkVisCondition + ".colorIfFalseR"))
	mc.connectAttr((armCtrlsDic['ArmIKFK'] + '.IKFK'),(ikFkVisCondition + ".colorIfFalseG"))
	mc.connectAttr((ikFkVisCondition + ".outColorG"),(ikFkVisReverse + ".inputX"))
	
	mc.connectAttr((ikFkVisCondition + ".outColorR"),(armCtrlsDic['shoulderFK'] + ".v"))
	mc.connectAttr((ikFkVisCondition + ".outColorR"),(armCtrlsDic['elbowFK'] + ".v"))
	mc.connectAttr((ikFkVisCondition + ".outColorR"),(armCtrlsDic['wristFK'] + ".v"))
	mc.connectAttr((ikFkVisReverse + ".outputX"),(armCtrlsDic['elbowPole'] + ".v"))
	mc.connectAttr((ikFkVisReverse + ".outputX"),(armCtrlsDic['arm'] + ".v"))
	
	#Adding Extra attribute for Twist
	mc.addAttr(armCtrlsDic['arm'], ln='Twist',at='double',dv = 0,k=True)
	mc.connectAttr((armCtrlsDic['arm'] + ".Twist"),(armIkHandle[0] + ".twist"))
	
	#Creating IK AlignArm 
	mc.addAttr(armCtrlsDic['arm'],ln = 'ArmAlign' , k = 0, at = 'bool')
	mc.setAttr((armCtrlsDic['arm'] + '.ArmAlign') , e = True , cb = True)
	grgArmAlign = mc.group(em = True , n = ('g%sArmAlign' % side))
	mc.delete(mc.parentConstraint(armJnts[3],grgArmAlign))
	mc.parent(grgArmAlign , ikJoints[1])
	armAlignCon = mc.orientConstraint(grgArmAlign ,(armCtrlsDic['arm'],ikJoints[2]))	
	armAlignConTargets = mc.orientConstraint(armAlignCon[0], q = True , tl = True)
	armAlignReverse = mc.createNode('reverse' , n = (side + "ArmAlign_Rev"))
	mc.connectAttr((armCtrlsDic['arm'] + '.ArmAlign'),(armAlignReverse + '.inputX'))
	mc.connectAttr((armCtrlsDic['arm'] + '.ArmAlign'),(armAlignCon[0] + ".%sW0" % armAlignConTargets[0]))
	mc.connectAttr((armAlignReverse + '.outputX'),(armAlignCon[0] + ".%sW1" % armAlignConTargets[1]))
	mc.progressBar(mainprogressbar,edit=True,step=10)	

	#FK Stretching
	mc.addAttr(armCtrlsDic['shoulderFK'], k = 1 , ln = 'Stretch' , at = 'double', dv = 1)
	mc.addAttr(armCtrlsDic['elbowFK'], k = 1 , ln = 'Stretch' , at = 'double', dv = 1)
	
	sholuderFKstrMD = mc.createNode('multiplyDivide' , n = (side + 'shoulderFKStr_MD'))
	elbowTx = mc.getAttr((fkJoints[1] + '.tx'))
	mc.setAttr((sholuderFKstrMD + ".input1X"), elbowTx)
	mc.connectAttr((armCtrlsDic['shoulderFK'] + '.Stretch') , (sholuderFKstrMD + ".input2X"))
	mc.connectAttr((sholuderFKstrMD + ".outputX") , (fkJoints[1] + '.tx'))
	
	elbowFKstrMD = mc.createNode('multiplyDivide' , n = (side + 'elbowFKStr_MD'))
	wristTx = mc.getAttr((fkJoints[2] + '.tx'))
	mc.setAttr((elbowFKstrMD + ".input1X"), wristTx)
	mc.connectAttr((armCtrlsDic['elbowFK'] + '.Stretch') , (elbowFKstrMD + ".input2X"))
	mc.connectAttr((elbowFKstrMD + ".outputX") , (fkJoints[2] + '.tx'))
	
	#IK Stretching
	mc.addAttr(armCtrlsDic['arm'], k = 1 , ln = 'AutoStretch' , at = 'long', min = 0 , max = 1 , dv = 0)
	mc.addAttr(armCtrlsDic['arm'], ln='UpperStretch' ,  at='double',min= -.9,dv = 0, k=True)
	mc.addAttr(armCtrlsDic['arm'], ln='LowerStretch' ,  at='double',min= -.9,dv = 0, k=True)
	
	armStretchStartLoc = mc.spaceLocator(n = ("Loc_%sHandIKDimenStart" % side))
	armStretchEndLoc = mc.spaceLocator(n = ("Loc_%sHandIKDimenEnd" % side))
	elbowLockLoc = mc.spaceLocator(n =  "Loc_%sHandElbowLockDim_Loc" % side)
	mc.pointConstraint(ikJoints[0],armStretchStartLoc[0])
	mc.pointConstraint(armCtrlsDic['arm'],armStretchEndLoc[0])
	mc.pointConstraint(armCtrlsDic['elbowPole'],elbowLockLoc)
	dimensionShape = mc.createNode('distanceDimShape' , n = side + 'ArmIKStrDistDimShape')
	distElbowLockUp = mc.createNode('distanceDimShape', n = side + 'ArmElbowUpDistDimShape')
	distElbowLockDn = mc.createNode('distanceDimShape', n = side + 'ArmElbowDnDistDimShape')
	mc.rename((mc.listRelatives(dimensionShape, p = True)),  side + 'ArmIKStrDistDim')
	mc.rename((mc.listRelatives(distElbowLockUp, p = True)),  side + 'ArmElbowUpDistDim')
	mc.rename((mc.listRelatives(distElbowLockDn, p = True)),  side + 'ArmElbowDnDistDim')
	dimensionTrans = mc.listRelatives(dimensionShape , p = True)[0],mc.listRelatives(distElbowLockUp , p = True)[0],mc.listRelatives(distElbowLockDn , p = True)[0]
	mc.connectAttr((armStretchStartLoc[0] + 'Shape.worldPosition[0]') ,(dimensionShape + '.startPoint'), f= True)
	mc.connectAttr((armStretchEndLoc[0] + 'Shape.worldPosition[0]') ,(dimensionShape + '.endPoint'))
	mc.connectAttr((armStretchStartLoc[0] + 'Shape.worldPosition[0]'), (distElbowLockUp + '.startPoint'), f = True)
	mc.connectAttr((elbowLockLoc[0] + 'Shape.worldPosition[0]'), (distElbowLockUp + '.endPoint'), f = True)
	mc.connectAttr((elbowLockLoc[0] + 'Shape.worldPosition[0]'), (distElbowLockDn + '.startPoint'), f = True)
	mc.connectAttr((armStretchEndLoc[0] + 'Shape.worldPosition[0]'), (distElbowLockDn + '.endPoint'), f = True)
	
	
	strScaleIKArmMD = mc.createNode('multiplyDivide' , n = ("pScale_%sIKArm_MD" % side))
	mc.setAttr((strScaleIKArmMD + ".operation"), 2)
	strScaleElbowLockUpMD = mc.createNode('multiplyDivide' , n = ("pScale_%sElbowLockUp_MD" % side))
	mc.setAttr((strScaleElbowLockUpMD + ".operation"), 2)
	strScaleElbowLockDnMD = mc.createNode('multiplyDivide' , n = ("pScale_%sElbowLockDn_MD" % side))
	mc.setAttr((strScaleElbowLockDnMD + ".operation"), 2)
	
	strDivideIKArmMD = mc.createNode('multiplyDivide' , n = (side + 'IKArmDivide_MD'))
	mc.setAttr((strDivideIKArmMD + ".operation"), 2)
	#mc.setAttr((strDivideIKArmMD + ".input2X"), (mc.getAttr(dimensionShape + '.distance')))
	addmanStrValPMA=mc.createNode('plusMinusAverage',n=(side +'IKArmmanStrAdd_PMA'))
	mc.setAttr((addmanStrValPMA + ".input1D[0]"), (mc.getAttr(dimensionShape + '.distance')))
	mc.connectAttr((armCtrlsDic['arm']+'.UpperStretch'),(addmanStrValPMA+'.input1D[1]'))
	mc.connectAttr((armCtrlsDic['arm']+'.LowerStretch'),(addmanStrValPMA+'.input1D[2]'))
	mc.connectAttr((addmanStrValPMA+'.output1D'),(strDivideIKArmMD + ".input2X"))
	IKArmLimitCD = mc.createNode('condition' , n = (side + 'IKArmLimit_Con'))
	mc.setAttr((IKArmLimitCD + ".operation"), 2)
	mc.setAttr((IKArmLimitCD + ".secondTerm"), 1)
	IKArmSwitchCD = mc.createNode('condition' , n = (side + 'IKArmSwitch_Con'))
	mc.setAttr((IKArmSwitchCD + ".secondTerm"), 1)
	
	elbowIKArmStrAddPMA=mc.createNode('plusMinusAverage',n=(side +'IKArmElbowStrAdd_PMA'))
	mc.setAttr((elbowIKArmStrAddPMA + ".input1D[0]"), (mc.getAttr(ikJoints[1] + '.tx')))
	mc.connectAttr((armCtrlsDic['arm']+'.UpperStretch'),(elbowIKArmStrAddPMA+'.input1D[1]'))
	
	wristIKArmStrAddPMA=mc.createNode('plusMinusAverage',n=(side +'IKArmWristStrAdd_PMA'))
	mc.setAttr((wristIKArmStrAddPMA + ".input1D[0]"), (mc.getAttr(ikJoints[2] + '.tx')))
	mc.connectAttr((armCtrlsDic['arm']+'.LowerStretch'),(wristIKArmStrAddPMA+'.input1D[1]'))

	elbowIKArmMD = mc.createNode('multiplyDivide' , n = (side + 'IKArmElbow_MD'))
	#mc.setAttr((elbowIKArmMD + ".input1X"), (mc.getAttr(ikJoints[1] + '.tx')))
	wristIKArmMD = mc.createNode('multiplyDivide' , n = (side + 'IKArmWrist_MD'))
	#mc.setAttr((wristIKArmMD + ".input1X"), (mc.getAttr(ikJoints[2] + '.tx')))
	elbowBlend = mc.createNode('blendTwoAttr',n=(side + 'Elbow_BTA'))
	wristBlend = mc.createNode('blendTwoAttr',n=(side + 'Wrist_BTA'))

	mc.connectAttr((distElbowLockUp + '.distance') , (strScaleElbowLockUpMD + '.input1X'))
	mc.connectAttr((distElbowLockDn + '.distance') , (strScaleElbowLockDnMD + '.input1X'))
	mc.connectAttr((armCtrlsDic['elbowPole'] + '.ElbowLock') , (elbowBlend + '.attributesBlender'))
	mc.connectAttr((armCtrlsDic['elbowPole'] + '.ElbowLock') , (wristBlend + '.attributesBlender'))
	mc.connectAttr((strScaleElbowLockUpMD + '.outputX') ,  (elbowBlend + '.input[1]'))
	mc.connectAttr((strScaleElbowLockDnMD + '.outputX') ,  (wristBlend + '.input[1]'))
	
	if side == 'Right': # correcting elbow lock problem
		valRevElbowLockUpMD = mc.createNode('multiplyDivide' , n = ("%sElbowLockRevUp_MD" % side))
		mc.setAttr((valRevElbowLockUpMD + ".input2X"),-1)
		valRevElbowLockDnMD = mc.createNode('multiplyDivide' , n = ("%sElbowLockRevDn_MD" % side))
		mc.setAttr((valRevElbowLockDnMD + ".input2X"),-1)
		
		mc.connectAttr((strScaleElbowLockUpMD + '.outputX') ,  (valRevElbowLockUpMD + '.input1X'),f=True)
		mc.connectAttr((strScaleElbowLockDnMD + '.outputX') ,  (valRevElbowLockDnMD + '.input1X'),f=True)
		mc.connectAttr((valRevElbowLockUpMD + '.outputX') , (elbowBlend + '.input[1]'),f=True)
		mc.connectAttr((valRevElbowLockDnMD + '.outputX') , (wristBlend + '.input[1]'),f=True)
		
		#stretch add set value for right hand 
		mc.setAttr((elbowIKArmStrAddPMA + ".operation"),2)
		mc.setAttr((wristIKArmStrAddPMA + ".operation"),2)
	
	mc.connectAttr((dimensionShape + '.distance') , (strScaleIKArmMD + '.input1X'))
	mc.connectAttr((strScaleIKArmMD + '.outputX') ,  (strDivideIKArmMD + '.input1X'))
	mc.connectAttr((strDivideIKArmMD + '.outputX') , (IKArmLimitCD + '.firstTerm'))
	mc.connectAttr((strDivideIKArmMD + '.outputX') , (IKArmLimitCD + '.colorIfTrueR'))
	mc.connectAttr((IKArmLimitCD + '.outColorR'), (IKArmSwitchCD + '.colorIfTrueR'))
	mc.connectAttr((armCtrlsDic['arm'] + '.AutoStretch') , (IKArmSwitchCD + '.firstTerm'))
	mc.connectAttr((elbowIKArmStrAddPMA+'.output1D'),(elbowIKArmMD + ".input1X"))
	mc.connectAttr((wristIKArmStrAddPMA+'.output1D'),(wristIKArmMD + ".input1X"))
	mc.connectAttr((IKArmSwitchCD + '.outColorR'), (elbowIKArmMD + '.input2X'))
	mc.connectAttr((IKArmSwitchCD + '.outColorR'), (wristIKArmMD + '.input2X'))
	mc.connectAttr((elbowIKArmMD + '.outputX'), (elbowBlend + '.input[0]'))
	mc.connectAttr((wristIKArmMD + '.outputX'), (wristBlend + '.input[0]'))
	mc.connectAttr((elbowBlend + '.output'), (ikJoints[1] + '.tx'))
	mc.connectAttr((wristBlend + '.output'), (ikJoints[2] + '.tx'))

	if not mc.objExists('Grp_ArmDimensions'):
		grpDimensions = mc.group(em = 1 , p = sysGrp, n = 'Grp_ArmDimensions')
	else:
		grpDimensions = 'Grp_ArmDimensions'
	mc.parent(armStretchStartLoc[0] , armStretchEndLoc[0] , elbowLockLoc[0] , dimensionTrans , grpDimensions)
	mc.progressBar(mainprogressbar,edit=True,step=10)
	
	#Adding Aux Control
	AuxSwitch = 1
	if AuxSwitch:
		armCtrlsDic['aux'] = 'Ctrl_%sAux' % side
		inst = scc.Ctrlcurve(armCtrlsDic['aux'], (.1*chrScale))
		auxGrp = inst.grpTrans()
		auxCtrl = inst.flower()
		mc.delete(mc.parentConstraint(armJnts[3], auxGrp))
		mc.parent(auxGrp , mainGrp)
		mc.addAttr(armCtrlsDic['ArmIKFK'], ln ='AuxControl', at = 'bool', k = False)
		mc.setAttr((armCtrlsDic['ArmIKFK'] + '.AuxControl'), cb = True)
		mc.connectAttr((armCtrlsDic['ArmIKFK'] + '.AuxControl') , auxGrp + ('.v'))
		
	#Parenting to Main Grp
	armCtrls = armCtrlsDic.values()
	armCtrlsGrp = armCtrlsGrpDic.values()
	mc.parent(armCtrlsGrp,mainGrp)
	
	#Bend Joint Creation
	if bendOnOff:
		if not mc.attributeQuery( 'BendControls', node= armCtrlsDic['ArmIKFK'],ex=1):
			mc.addAttr(armCtrlsDic['ArmIKFK'], ln ='BendControls', at = 'bool', k = False)
			mc.setAttr((armCtrlsDic['ArmIKFK'] + '.BendControls'), cb = True)
		getUpBendGrps = BJ.ar_crtBendJntz(armJnts[1] , armJnts[2] , side, 'Arm', 'Up', bendJnts)
		getDnBendGrps = BJ.ar_crtBendJntz(armJnts[2] , armJnts[3] , side, 'Arm', 'Dn', bendJnts)
		mc.connectAttr((armCtrlsDic['ArmIKFK'] + '.BendControls') , (getUpBendGrps[0] + '.v'))
		armCtrls += [getUpBendGrps[3],getDnBendGrps[3]]
	
	#add rightClick attributes
	snapGrp = mc.group(em = True , n  = (side + 'IKElbowSnap_FK'),p=armCtrlsDic['shoulderFK'])
	mc.delete(mc.parentConstraint((armCtrlsDic['elbowPole']) , snapGrp))
	mc.makeIdentity(snapGrp , apply=True , t=1 , r=1 , s=1)

	for obj in armCtrls:
		mc.addAttr(obj , sn='IKFKpos' , at='message')
		mc.connectAttr(armCtrlsDic['ArmIKFK'] + '.message' , obj + '.IKFKpos')
		if obj != armCtrlsDic['ArmIKFK']:
			attrName = obj.split('_')[1].replace(side,'')
			mc.addAttr(armCtrlsDic['ArmIKFK'], sn=attrName , at='message')
			mc.connectAttr(obj + '.message' , armCtrlsDic['ArmIKFK'] + '.%s' %attrName)

	snapObjs = ikJoints[:3] +[snapGrp]
	for each in snapObjs:
			attrName = each.split('_')[0].replace(side,'')
			if each != snapGrp:attrName = attrName + 'Jnt'
			mc.addAttr(armCtrlsDic['ArmIKFK'], sn=attrName , at='message')
			mc.connectAttr(each + '.message' , armCtrlsDic['ArmIKFK'] + '.%s' %attrName)
			
	#Quick Selection sets
	quickSelSet = mc.sets(armCtrls, t = 'gCharacterSet', name = (side + 'Arm_Sets'))
	mc.progressBar(mainprogressbar,edit=True,step=10)
	
	#Lock n Hide Unused Attributs
	tools.lockhide(armCtrlsDic['ArmIKFK'], [])
	tools.lockhide(armCtrlsDic['arm'], ["tx", "ty", "tz", "rx", "ry", "rz"])
	tools.lockhide(armCtrlsDic['elbowPole'], ["tx", "ty", "tz"])
	tools.lockhide(armCtrlsDic['clavicle'], ["tx", "ty", "tz"])
	tools.lockhide(armCtrlsDic['shoulderFK'], ["rx", "ry", "rz"])
	tools.lockhide(armCtrlsDic['elbowFK'], ["rx", "ry", "rz"])
	tools.lockhide(armCtrlsDic['wristFK'], ["rx", "ry", "rz"])
	tools.lockhide(armCtrlsDic['gimbal'], ["rx", "ry", "rz"])
	tools.lockhide(armCtrlsDic['hand'], [])

	#Fingers Manual and custom attributes
	getfingJnts = mc.listRelatives(armJnts[3],c = True , type = 'joint')
	if getfingJnts:
		fingMainGrp = mc.group(em = 1 , n = ("Grp_%sFingers" % side),p=mainGrp)
		mc.connectAttr((armCtrlsDic['hand'] + '.FingerControl'),(fingMainGrp + '.v'))
		mc.parentConstraint(armJnts[3] , fingMainGrp)
		
		#Arranging the Finger Order
		fingOrder = ['Index','Middle','Ring','Pinky','Thumb']
		fingJnts = [each for obj in fingOrder for each in getfingJnts if obj in each]
		
		for obj in fingJnts:
			fingName = obj[:-4].replace(side,'')#Extracing the Name
			
			#Adding Curl and Spread Attribute
			mc.addAttr(armCtrlsDic['hand'], k = 1 , ln = (fingName + 'Curl') , at = 'double', min = -5 , max = 5 , dv = 0)
			mc.addAttr(armCtrlsDic['hand'], k = 1 , ln = (fingName + 'Spread') , at = 'double', dv = 0)	
			
			#Create Control for Each Joint
			childJnt = mc.ls(obj,dag=1, type='joint')
			for i  in range(len(childJnt)-1):
				fingCtrl = mc.circle (nr = [1 , 0 , 0] , r = .08 , ch = 0, n = ('Ctrl_%s' % (side + fingName + str(i))))
				fingSdkGrp = mc.group(fingCtrl[0] , n = ('g%s_sdk' % (side + fingName + str(i))))
				fingGrp = mc.group(fingSdkGrp , n = ('Grp_%s' % (side + fingName + str(i))))
				mc.delete(mc.parentConstraint(childJnt[i] ,fingGrp))
				mc.parentConstraint(fingCtrl[0],childJnt[i],mo=1)
				#mc.orientConstraint(fingCtrl[0],childJnt[i])
				if i != 0:
					mc.parentConstraint(('Ctrl_%s' % (side + fingName + str(i-1))) ,fingGrp , mo = True)#Constraint
				
				#Creating Extra Group For Cup
				if i == 0 and  (fingName == 'Index'  or fingName == 'Pinky' or fingName == 'Thumb'):
					fingCupSdkGrp = mc.group(n = ('Grp_%s_Cup' % (side + fingName)), em=1, p = fingMainGrp)
					mc.delete(mc.parentConstraint(armJnts[3] , fingCupSdkGrp))
					mc.makeIdentity(fingCupSdkGrp,a=1,t=1,r=1)
					mc.parentConstraint(fingCupSdkGrp , fingGrp , mo=1)
				
				#Parenting to Main Group
				mc.parent(fingGrp,fingMainGrp)
		
				tools.lockhide(fingCtrl[0], ["rx", "ry", "rz"])
				mc.sets(fingCtrl[0] , add = quickSelSet)
	
				mc.progressBar(mainprogressbar,edit=True,step=10)	 		
				#Adding SetDrivenKeys
				#Finger Curling
				if 'Thumb' in fingName: #For Thumb
					if i == 0: 
						val = [(50,48),(0,15),(0,-30)]
					elif i == 1:
						val = [(0,0),(0,0),(30,-100 )]
					else:
						val = [(0,0),(0,0),(30,-70)]
					ar_SDK((armCtrlsDic['hand'] + '.%sCurl' % fingName) , (fingSdkGrp + '.rx')  , [-5,0,5] , [val[0][0],0,val[0][1]])
					ar_SDK((armCtrlsDic['hand'] + '.%sCurl' % fingName) , (fingSdkGrp + '.ry')  , [-5,0,5] , [val[1][0],0,val[1][1]])
					ar_SDK((armCtrlsDic['hand'] + '.%sCurl' % fingName) , (fingSdkGrp + '.rz')  , [-5,0,5] , [val[2][0],0,val[2][1]])
					
				elif i >= 1: #For Other Finger
					if i == 1: 
						val = (25,-85)
					elif i == 2:
						val = (20,-105)
					else:
						val = (15,-55)
					ar_SDK((armCtrlsDic['hand'] + '.%sCurl' % fingName) , (fingSdkGrp + '.rz')  , [-5,0,5] , [val[0],0,val[1]])
					
				#Finger Spreading
				if 'Thumb' in fingName and i == 0: #For Thumb
					getKey = ar_SDK((armCtrlsDic['hand'] + '.%sSpread' % fingName) , (fingSdkGrp + '.ry')  , [-5,0,5] , [-5,0,5])
					mc.setAttr( (getKey[0] + '.preInfinity'), 1)
					mc.setAttr( (getKey[0] + '.postInfinity'), 1)
					mc.addAttr(armCtrlsDic['hand'], k = 1 , ln = (fingName + 'Reach') , at = 'double', dv = 0)	
					mc.addAttr(armCtrlsDic['hand'], k = 1 , ln = (fingName + 'Twist') , at = 'double', dv = 0)
					getKey = ar_SDK((armCtrlsDic['hand'] + '.%sReach' % fingName) , (fingSdkGrp + '.rz')  , [-5,0,5] , [-5,0,5])
					mc.setAttr( (getKey[0] + '.preInfinity'), 1)
					mc.setAttr( (getKey[0] + '.postInfinity'), 1)
					getKey = ar_SDK((armCtrlsDic['hand'] + '.%sTwist' % fingName) , (fingSdkGrp + '.rx')  , [-5,0,5] , [-5,0,5])
					mc.setAttr( (getKey[0] + '.preInfinity'), 1)
					mc.setAttr( (getKey[0] + '.postInfinity'), 1)
					
				elif not 'Thumb' in fingName and i == 1: #For Other Finger
					getKey = ar_SDK((armCtrlsDic['hand'] + '.%sSpread' % fingName) , (fingSdkGrp + '.ry')  , [-5,0,5] , [-5,0,5])
					mc.setAttr( (getKey[0] + '.preInfinity'), 1)
					mc.setAttr( (getKey[0] + '.postInfinity'), 1)
				
				#FingerCup
				if not mc.attributeQuery( 'Cup', node=(armCtrlsDic['hand']), ex=True):
					mc.addAttr(armCtrlsDic['hand'], k = 1 , ln = 'Cup' , at = 'double', min = -5 , max = 5 , dv = 0)	
				if i == 0 and  (fingName == 'Index'  or fingName == 'Pinky' or fingName == 'Thumb'):
					if 'Index' in fingName:val = (25,-25)
					if 'Pinky' in fingName:val = (-25,25)
					if 'Thumb' in fingName:val = (25,-25)
					ar_SDK((armCtrlsDic['hand'] + '.Cup') , (fingCupSdkGrp + '.rx')  , [-5,0,5] , [val[0],0,val[1]])
		
				#FingerFan
				if not mc.attributeQuery( 'Fan', node=(armCtrlsDic['hand']), ex=True):
					mc.addAttr(armCtrlsDic['hand'], k = 1 , ln = 'Fan' , at = 'double', min = -5 , max = 5 , dv = 0)	
				if fingName != 'Thumb' and i == 0:
					if 'Index' in fingName:val = (-20,20)
					if 'Middle' in fingName:val = (-5,5)
					if 'Ring' in fingName:val = (5,-5)	
					if 'Pinky' in fingName:val = (20,-20)
					ar_SDK((armCtrlsDic['hand'] + '.Fan') , (fingSdkGrp + '.rz')  , [-5,0,5] , [val[0],0,val[1]])
				
				#FingerRelax
				if not mc.attributeQuery( 'Relax', node=(armCtrlsDic['hand']), ex=True):
					mc.addAttr(armCtrlsDic['hand'], k = 1 , ln = 'Relax' , at = 'double', min = -5 , max = 5 , dv = 0)
				if (fingName == 'Thumb' and (i == 0 or i == 1)):
					if i == 0:
						valx = (0,-30)
						valy = (-20,12)
					else:
						valx = (0,40)
						valy = (0,42)
					ar_SDK((armCtrlsDic['hand'] + '.Relax') , (fingSdkGrp + '.rx')  , [-5,0,5] , [valx[0],0,valx[1]])
					ar_SDK((armCtrlsDic['hand'] + '.Relax') , (fingSdkGrp + '.ry')  , [-5,0,5] , [valy[0],0,valy[1]])
				elif (fingName != 'Thumb' and i == 1):
					if 'Index' in fingName:val = (-15,8)
					if 'Middle' in fingName:val = (0,0)
					if 'Ring' in fingName:val = (10,-5)	
					if 'Pinky' in fingName:val = (25,-3)
					ar_SDK((armCtrlsDic['hand'] + '.Relax') , (fingSdkGrp + '.ry')  , [-5,0,5] , [val[0],0,val[1]])
				
		#ReArrange Finger Attributes
		mc.progressBar(mainprogressbar,edit=True,step=10)
# 		for obj in fingJnts:
# 			fingName = obj[:-4].replace(side,'')
# 			mc.renameAttr((armCtrlsDic['hand'] + '.%sSpread_Ed' % fingName), (fingName + 'Spread') )
# 			if obj == fingJnts[len(fingJnts)-1]:
# 					mc.renameAttr((armCtrlsDic['hand'] + '.%sReach_Ed' % fingName), (fingName + 'Reach') )
# 					mc.renameAttr((armCtrlsDic['hand'] + '.%sTwist_Ed' % fingName), (fingName + 'Twist') )
# 					mc.renameAttr((armCtrlsDic['hand'] + '.Cup_Ed'), 'Cup')
# 					mc.renameAttr((armCtrlsDic['hand'] + '.Fan_Ed'), 'Fan')
# 					mc.renameAttr((armCtrlsDic['hand'] + '.Relax_Ed'), 'Relax')
	
	mc.progressBar(mainprogressbar,edit=True,endProgress=True)
	#return
	return mainGrp , sysGrp
	

#**************************************************END**************************************************#

#ar_rigArms()