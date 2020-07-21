											#--------------------------------------------------------------#
											# 	DESCRIPTION	: Python Module For Rig Head          	       #                    												                       				                     
											# 	VERSION			: 1.00 , 20 November 2009                      #
											#   Copyright (C) 2009.  All rights reserved.									 #
											#--------------------------------------------------------------#
#Imports!
import maya.cmds as mc
import sk_ctrlCurves as scc
import ar_rigTools as tools

def ar_rigHead(NeckJnt,HeadStart, HeadEnd,Stretch = 1,NeckMethod = 1,EyeOnOff = 0,chrScale=1):
		
	#Control Creation and grouping
	headCntrl = 'Ctrl_Head'
	neckCntrl = 'Ctrl_Neck'
	jawCntrl = 'Ctrl_Jaw'
	allCntrls = [headCntrl,neckCntrl,jawCntrl]
	inst = scc.Ctrlcurve(headCntrl , (.3*chrScale))
	inst.head()
	headCntrlGrp = mc.group(headCntrl , n = 'Grp_HeadCtrl')
	mc.delete(mc.pointConstraint(HeadStart , headCntrlGrp))
	inst = scc.Ctrlcircle(neckCntrl,(.3*chrScale) ,[0,1,0 ])
	neckGrp = mc.group(neckCntrl , n = 'Grp_Neck')
	mc.delete(mc.pointConstraint(NeckJnt , neckGrp))
	
	headNeckGrp = mc.group(em = True, n = 'Grp_HeadNeck')
	mc.parent(neckGrp,headCntrlGrp , headNeckGrp)
	mc.parentConstraint(neckCntrl , headCntrlGrp , mo = 1)
	
	#Creating Jaw control
	jawStrJnt='JawStart_CJ'
	if mc.objExists(jawStrJnt):
		inst = scc.Ctrlcurve(jawCntrl , (.2*chrScale))
		jawGrp=inst.grpTrans()
		inst.jaw()
		mc.delete(mc.parentConstraint(jawStrJnt, jawGrp))
		mc.parentConstraint(jawCntrl,jawStrJnt,mo=1)
		mc.parentConstraint(HeadStart,jawGrp,mo=1)
		mc.parent(jawGrp, headNeckGrp)

	#Creating anchor group
	anchorGrp = mc.group(em = True , n = 'AnchorNeckHead')
	mc.delete(mc.pointConstraint(NeckJnt , anchorGrp))
	mc.parent(anchorGrp, (mc.listRelatives(NeckJnt , p = True)[0]))
	
	#Constraiting and connecting Head neck groups
	mc.parentConstraint(anchorGrp , neckGrp)
	
	#IK Handle Creation
	neckHeadIK = mc.ikHandle(sj = NeckJnt , ee = HeadStart , sol = 'ikSCsolver' , n = 'HeadIKHandle' )
	mc.setAttr((neckHeadIK[0] + '.v') , 0 , l = True)
	mc.pointConstraint(headCntrl , neckHeadIK[0])
	mc.parent(neckHeadIK[0] , headCntrlGrp)
	headEndIK = mc.ikHandle(sj = HeadStart , ee = HeadEnd , sol = 'ikSCsolver' , n = 'HeadEndIKHandle' )
	mc.setAttr((headEndIK[0] + '.v') , 0 , l = True)
	mc.parent(headEndIK[0] , headCntrl)
	
	#Neck Stretching
	dimStartLoc  = mc.spaceLocator(n = 'Loc HeadDimStart')
	dimEndLoc  = mc.spaceLocator(n = 'Loc HeadDimEnd')
	mc.pointConstraint(NeckJnt , dimStartLoc[0])
	mc.pointConstraint(headCntrl , dimEndLoc[0])
	disDimension = mc.createNode('distanceDimShape')
	transDim = mc.rename((mc.listRelatives(disDimension , p = True)[0]), 'Head_DistanceDimension')
	mc.connectAttr((dimStartLoc[0] + "Shape.worldPosition[0]") , (transDim + "Shape.startPoint"))
	mc.connectAttr((dimEndLoc[0] + "Shape.worldPosition[0]") , (transDim + "Shape.endPoint"))
	scaleHeadMD = mc.createNode('multiplyDivide' , n = 'pScaleHeadMD')
	divideHeadMD = mc.createNode('multiplyDivide' , n = 'HeadDivideMD')
	HeadlimitCondition = mc.createNode('condition' , n = 'HeadLimitStrCON')
	HeadSwitchCondition = mc.createNode('condition' , n = 'HeadSwitchCON')
	headMultiTx = mc.createNode('multiplyDivide' , n = 'HeadStretchMD')
	
	dimgrp = mc.group(em = 1 ,  n = 'Grp_HeadDimentions')
	mc.parent(dimStartLoc, dimEndLoc , transDim , dimgrp)
	sysgrp = mc.group(em  = True , n = 'Sys_Head')
	mc.parent(dimgrp , sysgrp)
	
	mc.setAttr((scaleHeadMD + ".operation"), 2)
	mc.setAttr((divideHeadMD + ".operation"), 2)
	mc.setAttr((HeadlimitCondition + ".operation"), 2)
	mc.setAttr((HeadlimitCondition + ".secondTerm"), 1)
	mc.setAttr((HeadSwitchCondition + ".secondTerm"), 1)
	mc.setAttr((divideHeadMD + ".input2X") ,(mc.getAttr(transDim + "Shape.distance")))
	mc.setAttr((headMultiTx + ".input1X") ,(mc.getAttr(HeadStart + ".tx")))
	
	mc.connectAttr((transDim + "Shape.distance") , (scaleHeadMD + ".input1X"))
	mc.connectAttr((scaleHeadMD + ".outputX") , (divideHeadMD + ".input1X"))
	mc.connectAttr((divideHeadMD + ".outputX") , (HeadlimitCondition + ".firstTerm"))
	mc.connectAttr((divideHeadMD + ".outputX"), (HeadlimitCondition + ".colorIfTrueR"))
	mc.connectAttr((HeadlimitCondition + ".outColorR") , (HeadSwitchCondition + ".colorIfTrueR"))
	mc.connectAttr((headCntrl + '.AutoStretch') ,(HeadSwitchCondition + ".firstTerm"))
	mc.connectAttr((HeadSwitchCondition + ".outColorR"), (headMultiTx + ".input2X"))
	mc.connectAttr((headMultiTx + ".outputX") ,(HeadStart + ".tx"))
		
	#Eyes Rig
	if EyeOnOff:
		eyeJnts = mc.ls('*Eye_CJ')
		cntrlEye = 'Ctrl_Eye'
		EyeCntrls = [cntrlEye]
		inst = scc.Ctrlcircle(cntrlEye ,(.55*chrScale) , (0,0,1))
		inst.circsquare()
		mc.setAttr((cntrlEye + '.sx') , .2)
		mc.makeIdentity(cntrlEye ,apply = True)
		eyeMainGrp = mc.group(cntrlEye , n = 'Grp_Eye')
		mc.delete(mc.parentConstraint(eyeJnts[0] , eyeMainGrp , st = 'x'))
		mc.setAttr(eyeMainGrp + '.tz' , (1*chrScale))
		mc.parentConstraint(HeadStart , eyeMainGrp , mo = True)
		mc.parent(eyeMainGrp , headNeckGrp)
		
		for jnt in eyeJnts:
			ctrlName = 'Ctrl_%s' % jnt.split('_')[0]
			circMain = mc.circle(name = ctrlName, c = (0,0,0), nr = (1,0,0), sw = 360, ch = 0 , r = .039)
			circ1 = mc.circle(name = ctrlName , c = (0,0,0), nr = (0,1,0), sw = 360, ch = 0 , r = .039)
			circ2 = mc.circle(name = ctrlName , c = (0,0,0), nr = (0,0,1), sw = 360, ch = 0 , r = .039)
			mc.parent(mc.listRelatives(circ1[0], c = 1 , s = 1)[0],mc.listRelatives(circ2[0], c = 1 , s = 1)[0],circMain[0],r = 1 , s = 1)
			eyeGrp = mc.group(ctrlName , n = ('Grp_%s' % jnt.split('_')[0]))
			mc.delete(circ1[0],circ2[0],mc.parentConstraint(jnt , eyeGrp))
			mc.setAttr(eyeGrp + '.tz' , (1*chrScale))
			mc.parent(eyeGrp , cntrlEye)
			mc.aimConstraint(ctrlName , jnt ,  mo  = 1 , w  = 1 , aim = (0,0,1) , u = (0,1,0) , wut = 'object' , wuo = HeadStart )
			EyeCntrls.append(ctrlName)
		for cntrl in EyeCntrls:
			tools.lockhide(cntrl,('tx', 'ty', 'tz'))
		allCntrls += EyeCntrls
	
	#add rightClick attributes
	for each in [headCntrl , neckCntrl]:
		mc.addAttr(each, sn='Head_RCDriver' , at='message')
		mc.connectAttr(headCntrl + '.message' , each + '.Head_RCDriver')
	mc.addAttr(headCntrl, sn='Head' , at='message')
	mc.connectAttr(headCntrl + '.message' , headCntrl + '.Head')
	mc.addAttr(headCntrl, sn='Neck' , at='message')
	mc.connectAttr(neckCntrl + '.message' , headCntrl + '.Neck')
	
	#QuickSelection Set
	mc.sets(allCntrls , n = 'Head_Sets' , t = 'gCharacterSet')
			
	# LocknHide Unused Attributes
	tools.lockhide(headCntrl,('sx', 'sy', 'sz', 'v'), 1)
	tools.lockhide(neckCntrl,('rx', 'ry', 'rz'))
	tools.lockhide(jawCntrl,('rx', 'ry', 'rz'))

		
#**************************************************END**************************************************#
