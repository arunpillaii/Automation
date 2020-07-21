											#--------------------------------------------------------------#
											# 	DESCRIPTION	: Python Module for Creating Spine Rig  			 #	 																		   
											# 	AUTHOR 			: Arun . S - arunpillaii@gmail.com             #                    												                       				                     
											# 	VERSION			: 1.00 , 16 November 2009                      #
											#   Copyright (C) 2009.  All rights reserved.									 #
											#--------------------------------------------------------------#
#Importing Modules
import maya.cmds as mc
import ar_rigTools as tools
import sk_ctrlCurves as ctrl

def ar_rigSpine(startSpine='Root_CJ',neck='Neck_CJ',fkControls=1,stretch=1,chrScale=1.0):
	
	endSpine = mc.listRelatives(neck , p = True)[0]
	#Declare Dictionary for Names
	Ctls = {'hip':'Ctrl_Hip', 'body':'Ctrl_Body', 'torso':'Ctrl_Torso', 'shoulder':'Ctrl_Shoulder'}
	ctrlGrps = {'hip':'Grp_Hip', 'body':'Grp_Body', 'torso':'Grp_Torso', 'shoulder':'Grp_Shoulder'}
	xtras = {'IKCurve':'curveMainIKSpline', 'spineSys':'Sys_Spine'}
	cntrls = Ctls.values()
	
	#IK Handle Creation	and Attribute SetUp
	spineIK = mc.ikHandle( n='mainIKSpline', sj=startSpine, ee=neck, sol='ikSplineSolver', scv=False)
	mc.setAttr((spineIK[0]+'.v'), 0, lock=True)
	spineJnts = mc.ikHandle(spineIK[0], query=True, jointList=True)
	mc.rename(spineIK[2], xtras['IKCurve'])
	mc.rebuildCurve(xtras['IKCurve'] , ch=0 , rpo=1 , rt=0 , end=1 , kr=1 , kcp=0 , kep=1 , kt=0 , s=0 , d=3 , tol=0.01)
	tmpCurve = mc.curve( d=1 , p=[mc.xform(endSpine , q=True, ws=True , t=True), mc.xform(neck , q=True, ws=True , t=True)])
	minusArcLen = (mc.arclen(xtras['IKCurve'])-mc.arclen(tmpCurve))
	mc.delete(tmpCurve)
	distDimension = mc.arcLengthDimension( xtras['IKCurve'] + '.u[%f]' % minusArcLen)
	
	#System Group	for Organising Untouchables
	if not(mc.objExists(xtras['spineSys'])):
		mc.group(name=xtras['spineSys'], empty=True)
	mc.parent(xtras['IKCurve'],spineIK[0], xtras['spineSys'])
	
	#joints for Spine curve
	curSkinJntPos = [(startSpine,endSpine , neck) , ('SpineLower_jnt' , 'SpineMid_jnt' , 'SpineUpper_jnt')]
	curSkinJnt = []
	for i in range(3):
		mc.select(cl=1)
		jnt = mc.joint(n=(curSkinJntPos[1][i]))
		mc.delete(mc.parentConstraint(curSkinJntPos[0][i] , jnt))
		mc.makeIdentity (jnt , a=True)
		mc.setAttr((jnt+'.v'),0, lock=True)
		curSkinJnt.append(jnt)
	mc.skinCluster(curSkinJnt, xtras['IKCurve'] , dr=4 , mi=2 , rui=1 , ibp=1)

	#Control Creation	
	Hip = ctrl.Ctrlcurve(Ctls['hip'], (0.4*chrScale))#Hip Control
	Hip.square()
	Hip.rect()
	Hip.rotorder()
	Hip.grpTrans()
	mc.delete(mc.pointConstraint(spineJnts[0] , ctrlGrps['hip'] ))
	Body = ctrl.Ctrlcurve(Ctls['body'], (0.5*chrScale))#Body Control
	Body.grpTrans()
	Body.square()
	Body.rect()
	Body.rotorder()
	mc.delete(mc.pointConstraint(spineJnts[0] , ctrlGrps['body'] ))
	Torso = ctrl.Ctrlcurve(Ctls['torso'], (0.35*chrScale))#Torso Control
	Torso.grpTrans()
	Torso.box(1)
	Torso.rotorder()
	mc.delete(mc.pointConstraint(spineJnts[len(spineJnts)-2] , ctrlGrps['torso'] ))
	Shoulder = ctrl.Ctrlcircle(Ctls['shoulder'], (0.75*chrScale))#Shoulder Control
	Shoulder.grpTrans()
	Shoulder.circsquare()
	Shoulder.rotorder()
	mc.delete(mc.pointConstraint(spineJnts[len(spineJnts)-1] , ctrlGrps['shoulder'] ))

	#constraint Controls and groups
	mc.parentConstraint(Ctls['body'] , ctrlGrps['hip'] , mo=1)
	mc.parentConstraint(Ctls['torso'] , ctrlGrps['shoulder'] , mo=1)

	#Parenting Joints
	mc.parent(curSkinJnt[0] , startSpine , Ctls['hip'])
	mc.parent(curSkinJnt[1] , Ctls['torso'])
	mc.parent(curSkinJnt[2] , Ctls['shoulder'])
	
	#Set Advanced Twist
	mc.setAttr(spineIK[0] + '.dTwistControlEnable' , 1)
	mc.setAttr(spineIK[0] + '.dWorldUpType' , 4)
	mc.setAttr(spineIK[0] + '.dWorldUpVectorX' , -1)
	mc.setAttr(spineIK[0] + '.dWorldUpVectorY' , 0)
	mc.setAttr(spineIK[0] + '.dWorldUpVectorEndX' , -1)
	mc.setAttr(spineIK[0] + '.dWorldUpVectorEndY' , 0)
	mc.connectAttr(Ctls['hip'] + '.worldMatrix[0]' , spineIK[0] + '.dWorldUpMatrix')
	mc.connectAttr(Ctls['shoulder'] + '.worldMatrix[0]' , spineIK[0] + '.dWorldUpMatrixEnd')
	
	#Spine Stretching
	if stretch:
		mc.addAttr(Ctls['torso'] , ln='AutoStretch',  at='long' ,min=0 , max=1 , k=1)
		spMulti1 = mc.createNode('multiplyDivide', n='pScaleSpineMD')
		mc.setAttr((spMulti1 + '.operation'), 2)
		mc.connectAttr((distDimension + '.arcLength'), (spMulti1 + '.input1X'), f=True)
		spMulti2 = mc.createNode('multiplyDivide', n='spineStrDivideMD')
		mc.setAttr((spMulti2 + '.operation'), 2)
		mc.connectAttr((spMulti1 + '.outputX'), (spMulti2 + '.input1X'), f=True)
		mc.setAttr((spMulti2 + '.input2X'), mc.getAttr(distDimension + '.arcLength'))
		spStrCon = mc.createNode('condition', n='spineStrSwitchCON')
		mc.setAttr((spStrCon + '.secondTerm'), 1)
		mc.connectAttr((Ctls['torso'] + '.AutoStretch'), (spStrCon + '.firstTerm'), f=True)
		mc.connectAttr((spMulti2 + '.outputX'), (spStrCon + '.colorIfTrueR'), f=True)
		for each in spineJnts[1:]:
			getJntTx = mc.getAttr((each + '.translateX'))
			spineJntMulti = mc.createNode('multiplyDivide', n=(each + 'SpStrMD'))
			mc.connectAttr((spStrCon + '.outColorR'), (spineJntMulti + '.input1X'), f=True)
			mc.setAttr((spineJntMulti + '.input2X'), getJntTx)
			mc.connectAttr((spineJntMulti + '.outputX'), (each + '.tx'))
		
	#Adding Additional FK Controls
	if fkControls:
		Ctls=dict(Ctls , fkSpine1='Ctrl_FKSpine1' , fkSpine2='Ctrl_FKSpine2')
		cntrls.append('Ctrl_FKSpine1')
		cntrls.append('Ctrl_FKSpine2')
		ctrlGrps=dict(ctrlGrps,fkSpine1='Grp_FKSpine1' , fkSpine2='Grp_FKSpine2')
		#Joints for FK Spine
		fkJnts = tools.ar_jointsAlongCurve(spineJnts[:len(spineJnts)-1] , 'FkSpine' , jntsNo=4 , chainSwitch=1)
		mc.setAttr((fkJnts[0] + '.v'), 0, lock=True)
	
		#Creating FK controls
		fk1 = ctrl.Ctrlcircle(Ctls['fkSpine2'])
		fk1.grpTrans()
		fk1.fkSpine()
		mc.delete(mc.pointConstraint(fkJnts[2] , ctrlGrps['fkSpine2']))
		fk2 = ctrl.Ctrlcircle(Ctls['fkSpine1'])
		fk2.grpTrans()
		fk2.fkSpine()
		mc.delete(mc.pointConstraint(fkJnts[1] , ctrlGrps['fkSpine1']))
		mc.parent(fkJnts[0] , Ctls['body'])
		
		#fkcontrols constrainting
		mc.parentConstraint(fkJnts[0] , ctrlGrps['fkSpine1'] , mo=1)
		mc.orientConstraint(Ctls['fkSpine1'] , fkJnts[1] , mo=1)
		mc.parentConstraint(fkJnts[1] , ctrlGrps['fkSpine2'] , mo=1)
		mc.orientConstraint(Ctls['fkSpine2'] , fkJnts[2] , mo=1)
		mc.parentConstraint(fkJnts[3] , ctrlGrps['torso'] , mo=1)
	else:
		mc.parentConstraint(Ctls['body'] , ctrlGrps['torso'] , mo=1)
		
	#creating main group
	mainGrp = mc.group(em=True,n='Grp_BODY')
	mc.parent(ctrlGrps.values(), mainGrp)
	
	#lock n hide unused attributes
	nlockAttrs = ([("tx", "ty", "tz", "rx", "ry", "rz")]*3 + [('rx' , 'ry' , 'rz')]*3)
	for i in range(len(cntrls)):
		tools.lockhide(cntrls[i] , nlockAttrs[i])

	#quick Selection set
	Controls = Ctls.values()
	mc.sets(Controls, t='gCharacterSet', name='Spine_Sets')
	
	#add rightClick attributes
	for obj in Ctls.values():
		mc.addAttr(obj , sn='Spine_RCDriver' , at='message')
		mc.connectAttr(Ctls['body'] + '.message' , obj + '.Spine_RCDriver')
		if obj != Ctls['body']:
			attrName = obj.split('_')[1]
			mc.addAttr(Ctls['body'], sn=attrName , at='message')
			mc.connectAttr(obj + '.message' , Ctls['body'] + '.%s' %attrName)
	mc.select(cl=True)

	#returns
	return mainGrp , xtras['spineSys']
	
#**************************************************END**************************************************#
