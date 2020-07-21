											#-----------------------------------------------------------#
											# 	DESCRIPTION	: Python Module for Rig Legs				#	 																		   
											# 	AUTHOR 		: Arun . S - arunpillaii@gmail.com			#                    												                       				                     
											# 	VERSION		: 2.00 , 17 October 2011		            #
											#   Copyright (C) 2011.  All rights reserved.				#
											#-----------------------------------------------------------#
#Imports!!
import maya.cmds as mc
import ar_rigTools as tools
import sk_ctrlCurves as ctrl
import ar_bendJointz as BJ

#def ar_rigLegs(LegStart,Heel,HeelExt,HeelInt,Side,bendOnOff,bendJnts,chrScale=1):
# method : 0 for normal and 1 for split knee

def ar_rigLegs(
	LegStart='RightUpLeg_CJ',
	Heel='RightHeel_CJ',
	HeelExt='RightHeelExt_CJ',
	HeelInt='RightHeelInt_CJ',
	Side='Right',
	bendOnOff=1,
	bendJnts=3,
	chrScale=1,
	method=0
):
    jntCount=5
    if method:jntCount=6
    hipJnt = mc.listRelatives(LegStart, p = True)
    legJnts  = mc.ls(LegStart , dag  = 1 , lf = 0)[:jntCount]
    ikJoints = []
    fkJoints = []

    #Creating IKFK joints
    ikJnts = mc.duplicate(legJnts[:jntCount],po = 1 ,rc = 1) 
    fkJnts = mc.duplicate(legJnts[:jntCount], po = 1 ,rc = 1)
    mc.parent(ikJnts[0],fkJnts[0], w = True)

    #Renaming IKFK Joints
    for i in range(len(ikJnts)):
        namepref = ikJnts[i].split('_CJ')
        ikJoints.append(mc.rename(ikJnts[i] ,  (namepref[0] + "_IK")))
        fkJoints.append(mc.rename(fkJnts[i] ,  (namepref[0] + "_FK")))
    mc.setAttr((ikJoints[-1] + '.jointOrient'), 0,0,0)
    mc.setAttr((fkJoints[-1] + '.jointOrient'), 0,0,0)
    #mc.setAttr((ikJoints[1] + ".preferredAngleY"), 90)

    ikKnee=ikJoints[1]
    if method:
        mc.setAttr((ikJoints[1] + ".preferredAngleY"), -90) # minus for reverse knee
        ikKnee=[ikJoints[1],ikJoints[2]]
        mc.setAttr((ikJoints[2] + ".preferredAngleY"), 45)

    #System and Main Group
    sysLeg = 'Sys_Legs'
    if not mc.objExists(sysLeg):
        mc.group(n = sysLeg, em = True)
    gIkFkJnts = mc.group(n = ('Sys_' + Side + 'LegIKFKJnts'), em = True, p = sysLeg)
    mc.delete(mc.parentConstraint(LegStart , gIkFkJnts))
    mc.parent(ikJoints[0] , fkJoints[0] , gIkFkJnts)
    mc.pointConstraint(LegStart, gIkFkJnts, mo = True)
    mc.orientConstraint(hipJnt, gIkFkJnts, mo = True)
    mc.scaleConstraint(hipJnt , gIkFkJnts, mo = True)
    legGrp = 'Grp_Legs'
    if not mc.objExists(legGrp):
        mc.group(n = legGrp, em = True)

    legCtrlsDic = {'Foot':("Ctrl_%sFoot" % Side),'Knee':("Ctrl_%sKnee" % Side),'LegIKFK':("Ctrl_%sLegIKFK" % Side),'FKLeg' : ('Ctrl_%sFKLeg' % Side),'FKKnee' : ('Ctrl_%sFKKnee' % Side),'FKAnkle' : ('Ctrl_%sFKAnkle' % Side),'FKToe' : ('Ctrl_%sFKToe' % Side)}
    legCtrlsGrpDic = {'FootGrp':("Grp_%sFoot" % Side),'KneeGrp':("Grp_%sKnee" % Side),'LegIKFKGrp' : ('Grp_%sLegIKFK' % Side),'FKLegGrp' : ('Grp_%sFKLeg' % Side),'FKKneeGrp' : ('Grp_%sFKKnee' % Side),'FKAnkleGrp' : ('Grp_%sFKAnkle' % Side),'FKToeGrp' : ('Grp_%sFKToe' % Side)}
    grpIKs = []

    inst = ctrl.Ctrlcurve(legCtrlsDic['Foot'], (1*chrScale))
    inst.foot(Side)
    grpIKs.append(mc.group(em = 1 , n = legCtrlsGrpDic['FootGrp']))
    mc.parent(legCtrlsDic['Foot'] , legCtrlsGrpDic['FootGrp'])
    mc.delete(mc.parentConstraint(Heel, legCtrlsGrpDic['FootGrp'])) 
    #mc.delete(mc.pointConstraint(Heel, legCtrlsGrpDic['FootGrp']))
    mc.delete(mc.pointConstraint(legJnts[-3], legCtrlsGrpDic['FootGrp']))

    mc.addAttr(legCtrlsDic['Foot'], ln = 'Stretch', at = 'bool', k = True , dv = 1)
    mc.setAttr(legCtrlsDic['Foot'] + '.Stretch' , k = False , cb = True,l = True)
    mc.addAttr(legCtrlsDic['Foot'], ln = 'AutoStretch', at = 'long', min = 0, max = 1, k = True)
    mc.addAttr(legCtrlsDic['Foot'], ln='UpperStretch' ,  at='double',min= -.9,dv = 0, k=True)
    mc.addAttr(legCtrlsDic['Foot'], ln='LowerStretch' ,  at='double',min= -.9,dv = 0, k=True)
    mc.addAttr(legCtrlsDic['Foot'], ln = 'KneePos', at = 'double',k = True)
    #
    mc.addAttr(legCtrlsDic['Foot'], ln = 'Pivots', at = 'bool', k = True , dv = 1)
    mc.setAttr(legCtrlsDic['Foot'] + '.Pivots' , k = False , cb = True,l = True)
    mc.addAttr(legCtrlsDic['Foot'], ln = 'FootRoll', at = 'double',k = True)
    mc.addAttr(legCtrlsDic['Foot'], ln = 'RollAngle', at = 'double',k = True,min = 0, max = 360)
    mc.addAttr(legCtrlsDic['Foot'], ln = 'ToeRoll', at = 'double',k = True)
    mc.addAttr(legCtrlsDic['Foot'], ln = 'FootLean', at = 'double',k = True)
    mc.addAttr(legCtrlsDic['Foot'], ln = 'HeelPivot', at = 'double',k = True)
    mc.addAttr(legCtrlsDic['Foot'], ln = 'ToePivot', at = 'double',k = True)

    mc.addAttr(legCtrlsDic['Foot'], ln = 'Xtras', at = 'bool', k = True , dv = 1)
    mc.setAttr(legCtrlsDic['Foot'] + '.Xtras' , k = False , cb = True,l = True)	
    mc.addAttr(legCtrlsDic['Foot'], ln = 'Twist', at = 'double',k = True)
    mc.addAttr(legCtrlsDic['Foot'], ln = 'KneeControl', at = 'bool', k = True , dv = 0)
    mc.setAttr(legCtrlsDic['Foot'] + '.KneeControl' , k = False , cb = True)

    inst = ctrl.Ctrlcurve(legCtrlsDic['Knee'], (.1*chrScale))
    inst.square()
    mc.setAttr((legCtrlsDic['Knee'] + ".rx"),90)
    mc.setAttr((legCtrlsDic['Knee'] + ".rz"),45)
    mc.makeIdentity(apply = True,r = 1)
    mc.addAttr(legCtrlsDic['Knee'] , ln='KneeLock' , min=0 , max=1 , k=True)
    grpIKs.append(mc.group(legCtrlsDic['Knee'] , n = legCtrlsGrpDic['KneeGrp']))
    mc.delete(mc.pointConstraint(ikKnee,legCtrlsGrpDic['KneeGrp']))

    # creating temp geometry for polvector alignment
    selPositions = [mc.xform(each, q=1, t=1, ws=1) for each in ikJoints[:3]]
    tempGeo, = mc.polyCreateFacet(ch=0,tx=1,p=selPositions)
    mc.delete(mc.normalConstraint(tempGeo,legCtrlsGrpDic['KneeGrp']),tempGeo)
    curValue =mc.xform(legCtrlsGrpDic['KneeGrp'],q=1, os = True, t = 1)
    curValue[-1] = curValue[-1] + 6
    mc.xform(legCtrlsGrpDic['KneeGrp'],os = True, t = curValue)
    # mc.setAttr((legCtrlsGrpDic['KneeGrp']+ ".tz"),2)
    #	mc.setAttr((legCtrlsGrpDic['KneeGrp']+ ".tz"),-2) # minus for reverse knee

    #Creating Knee Annotation Arrow
    locAnno = mc.spaceLocator(n = ("Loc_%sKneeArrow" % Side))
    mc.delete(mc.parentConstraint(legCtrlsDic['Knee'],locAnno[0]))
    mc.parent(locAnno[0],legCtrlsDic['Knee'])
    tmpAnno = mc.annotate(locAnno[0],tx = "")
    mc.rename(tmpAnno,(Side + "KneeAnnotationShape"))
    tranAnno = mc.listRelatives((Side + "KneeAnnotationShape"),p = 1)
    mc.rename(tranAnno[0],(Side + "KneeAnnotation"))
    mc.parentConstraint(ikKnee ,(Side + "KneeAnnotation"))
    mc.parent((Side + "KneeAnnotation"),locAnno[0])
    mc.setAttr((locAnno[0] + "Shape.v"),0)
    mc.setAttr((locAnno[0] + "Shape.v"),l = 1)
    mc.setAttr((Side + "KneeAnnotation.template"),1)

    inst = ctrl.Ctrlcurve(legCtrlsDic['LegIKFK'], (0.1*chrScale))
    inst.ikfk('Leg')
    grpIKs.append(mc.group(legCtrlsDic['LegIKFK'], n = legCtrlsGrpDic['LegIKFKGrp']))
    mc.xform(legCtrlsGrpDic['LegIKFKGrp'], os = True, piv = (0,0,0))
    mc.delete(mc.pointConstraint(legJnts[-3], legCtrlsGrpDic['LegIKFKGrp']))
    mc.parentConstraint(legJnts[-3], legCtrlsGrpDic['LegIKFKGrp'], mo = 1)
    valTx = 0.3
    if Side == 'Right': valTx = -0.3
    mc.setAttr((legCtrlsDic['LegIKFK'] + '.tx'), valTx)

    FKs = [('FKLeg','FKLegGrp'), ('FKKnee' , 'FKKneeGrp'), ('FKAnkle' , 'FKAnkleGrp') , ('FKToe','FKToeGrp')]
    grpFKs = []
    scaleVal = (0.3*chrScale)
    tmpLegJnts=list(legJnts)
    if method:tmpLegJnts.pop(2)
    for i in range(4):
        inst = ctrl.Ctrlcircle(legCtrlsDic[(FKs[i][0])], scaleVal,[1,0,0])
        inst.doubleshape()	
        scaleVal -= 0.05
        if i < 2:
            mc.addAttr(legCtrlsDic[FKs[i][0]], ln = 'Stretch', at = 'double', dv = 1, k = True)
        grpFKs.append(mc.group(legCtrlsDic[FKs[i][0]], n = legCtrlsGrpDic[FKs[i][1]]))
        mc.delete(mc.parentConstraint(tmpLegJnts[i] , legCtrlsGrpDic[FKs[i][1]]))

    ikFkVisCondition = mc.createNode('condition' , n = (Side + "LegIkFkVis_Con"))
    ikFkVisReverse = mc.createNode('reverse' , n = (Side + "LegIkFkVis_Rev"))
    mc.setAttr((ikFkVisCondition + '.secondTerm'), 1)
    mc.setAttr((ikFkVisCondition + '.colorIfTrueR'), 1)
    mc.connectAttr((legCtrlsDic['LegIKFK'] + '.IKFKControls'),(ikFkVisCondition + ".firstTerm"))
    mc.connectAttr((legCtrlsDic['LegIKFK'] + '.IKFK'),(ikFkVisCondition + ".colorIfFalseR"))
    mc.connectAttr((legCtrlsDic['LegIKFK'] + '.IKFK'),(ikFkVisCondition + ".colorIfFalseG"))
    mc.connectAttr((ikFkVisCondition + ".outColorG"),(ikFkVisReverse + ".inputX"))

    mc.connectAttr((ikFkVisCondition + ".outColorR"),(legCtrlsDic['FKLeg'] + ".v"))
    mc.connectAttr((ikFkVisCondition + ".outColorR"),(legCtrlsDic['FKKnee'] + ".v"))
    mc.connectAttr((ikFkVisCondition + ".outColorR"),(legCtrlsDic['FKAnkle'] + ".v"))
    mc.connectAttr((ikFkVisCondition + ".outColorR"),(legCtrlsDic['FKToe'] + ".v"))
    mc.connectAttr((ikFkVisReverse + ".outputX"),(legCtrlsDic['Knee'] + ".v"))
    mc.connectAttr((ikFkVisReverse + ".outputX"),(legCtrlsDic['Foot'] + ".v"))

    # IK Leg
    ankleIKHandle = mc.ikHandle(sj = ikJoints[0], ee = ikJoints[-3], sol = 'ikRPsolver', n = (Side + 'LegAnkle_IKHandle'))
    ballIKHandle = mc.ikHandle(sj = ikJoints[-3], ee = ikJoints[-2], sol = 'ikSCsolver', n = (Side + 'LegBall_IKHandle'))
    toeIKHandle = mc.ikHandle(sj = ikJoints[-2], ee = ikJoints[-1], sol = 'ikRPsolver', n = (Side + 'LegToe_IKHandle'))

    mc.select(cl = 1)
    revParents = [HeelExt , HeelInt , Heel , ikJoints[-1] , ikJoints[-2] , ikJoints[-3]]
    revJnts = []
    for each in revParents:
        jnt = mc.joint(n = (each[:-2] + 'INV'))
        mc.delete(mc.parentConstraint(each, jnt))
        if each == ikJoints[-1]:mc.setAttr((jnt + '.ty'), 0)
        revJnts.append(jnt)
    mc.makeIdentity(revJnts[0], apply = True)
    mc.select(cl = 1)
    mc.delete(Heel , HeelExt , HeelInt)
        
    inverseGrp = mc.group(em =  1, n = ('Grp_%sFootInverse' % Side))
    mc.setAttr((inverseGrp + '.v'), 0, lock = True)
    mc.delete(mc.parentConstraint(ikJoints[-3] , inverseGrp))	
    mc.parent(revJnts[0] , inverseGrp)
    inverseToeGrp = mc.group(em =  1, n = ('Grp_%sToeIkHandle' % Side) , p = revJnts[4])
    mc.parent(inverseToeGrp , revJnts[3])
    mc.parent(toeIKHandle[0] , inverseToeGrp)
    mc.parent(ballIKHandle[0] , revJnts[4])
    mc.parent(ankleIKHandle[0] , revJnts[5])
    mc.parent(inverseGrp , legCtrlsDic['Foot'])

    if Side == 'Right':
        mc.transformLimits(revJnts[0], rz = (0,360), erz = (1,0))
        mc.transformLimits(revJnts[1], rz = (-360,0), erz = (0,1))
    else:
        mc.transformLimits(revJnts[0], rz = (-360,0), erz = (0,1))
        mc.transformLimits(revJnts[1], rz = (0,360), erz = (1,0))
    mc.transformLimits(revJnts[2], rx = (-360,0), erx = (0,1))
    mc.transformLimits(revJnts[3], ry = (0,360), ery = (1,0))
    mc.transformLimits(revJnts[4], ry = (0,360), ery = (1,0))

    rollCondition = mc.createNode('condition' , n = (Side + "LegRoll_Con"))
    mc.setAttr(rollCondition+'.operation',4)
    rollPMA = mc.createNode('plusMinusAverage' , n = (Side + "LegRoll_PMA"))
    mc.setAttr(rollPMA+'.operation',2)

    mc.connectAttr((legCtrlsDic['Foot'] + '.FootLean'), (revJnts[0] + '.rz'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.FootLean'), (revJnts[1] + '.rz'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.HeelPivot'), (revJnts[2] + '.ry'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.ToePivot'), (revJnts[3] + '.rz'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.Twist'), (ankleIKHandle[0] + '.twist'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.FootRoll'), (revJnts[2] + '.rx'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.FootRoll'), (rollPMA + '.input1D[0]'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.RollAngle'), (rollPMA + '.input1D[1]'), f = True)
    mc.connectAttr((rollPMA + '.output1D'),(revJnts[3] + '.ry'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.FootRoll'), (rollCondition + '.firstTerm'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.FootRoll'), (rollCondition + '.colorIfTrueR'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.RollAngle'), (rollCondition + '.secondTerm'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.RollAngle'), (rollCondition + '.colorIfFalseR'), f = True)
    mc.connectAttr((rollCondition + '.outColorR'),(revJnts[4] + '.ry'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.ToeRoll'), (inverseToeGrp + '.ry'), f = True)

    # pole vector
    PoleLoc = (mc.spaceLocator(n = ('LOC_' + Side + 'LegPoleVector')))[0]
    PoleLocGrp = mc.group(PoleLoc, n = ('Grp_LOC' + Side + 'LegPoleVector'))
    mc.delete(mc.parentConstraint(revJnts[2], PoleLocGrp))
    #mc.delete(mc.parentConstraint(ikKnee, PoleLoc))
    #mc.setAttr((PoleLoc + '.tz'), 10)
    mc.delete(mc.parentConstraint(legCtrlsGrpDic['KneeGrp'], PoleLoc))

    mc.parent(PoleLocGrp, revJnts[2])
    PoleCstr1 = mc.group(n = (Side + 'LegPole_cstrn1'), em = True)
    PoleCstr1grp = mc.group(PoleCstr1, n = ('Grp_' + Side + 'LegPole_cstrn1'))
    PoleCstr2 = mc.group(n = (Side + 'LegPole_cstrn2'), em = True)
    PoleCstr2grp = mc.group(PoleCstr2, n = ('Grp_' + Side + 'LegPole_cstrn2'))
    mc.delete(mc.pointConstraint(ikJoints[0], PoleCstr1grp))
    mc.delete(mc.pointConstraint(ikJoints[-3] , PoleCstr2grp))
    mc.delete(mc.orientConstraint(legCtrlsDic['Foot'], PoleCstr1grp))
    mc.delete(mc.orientConstraint(legCtrlsDic['Foot'], PoleCstr2grp))
    mc.delete(mc.pointConstraint(PoleLoc, PoleCstr1))
    mc.delete(mc.pointConstraint(PoleLoc, PoleCstr2))
    PoleLocCon = (mc.pointConstraint(PoleCstr1, PoleCstr2, PoleLoc, mo = True))[0]
    mc.setAttr((PoleLocCon + '.' + PoleCstr1 + 'W0'), 0.5)
    mc.orientConstraint(PoleCstr1, PoleCstr2, PoleLoc, mo = True)
    mc.parent(PoleCstr1grp , hipJnt)
    mc.parent(PoleCstr2grp , legCtrlsDic['Foot'])
    poleVectorCons = mc.poleVectorConstraint(PoleLoc , legCtrlsDic['Knee'] , ankleIKHandle[0] , weight = 1)
    autoPoleRev = mc.createNode('reverse', name = (Side + 'AutoPoleReverse'))
    mc.connectAttr((legCtrlsDic['Foot'] + '.KneeControl') , (poleVectorCons[0] + '.%sW1' % legCtrlsDic['Knee']))
    mc.connectAttr(legCtrlsDic['Foot'] + '.KneeControl' , (autoPoleRev + '.inputX'))
    mc.connectAttr((autoPoleRev + '.outputX') , (poleVectorCons[0] + '.%sW0' % PoleLoc))
    mc.connectAttr((legCtrlsDic['Foot'] + '.KneeControl') , legCtrlsGrpDic['KneeGrp'] + '.v')

    #IK Stretching
    sysDim = 'Grp_LegDimentions'
    if not mc.objExists(sysDim):
        mc.group(n = sysDim, em = True , p = sysLeg)
    startLoc = mc.spaceLocator(n = Side + 'LegIKStrDim_StartLoc')
    endLoc = mc.spaceLocator(n = Side + 'LegIKStrDim_EndLoc')
    kneeLockLoc = mc.spaceLocator(n = Side + 'LegIKKneeLockDim_Loc')
    mc.parent(startLoc , endLoc , kneeLockLoc , sysDim)
    mc.pointConstraint(ikJoints[0] , startLoc)
    mc.pointConstraint(inverseGrp	, endLoc)
    mc.pointConstraint(legCtrlsDic['Knee'],kneeLockLoc)

    distMain = mc.createNode('distanceDimShape', n = Side + 'LegIKStrDistDimShape')
    distKneeLockUp = mc.createNode('distanceDimShape', n = Side + 'LegIKKneeUpDistDimShape')
    distKneeLockDn = mc.createNode('distanceDimShape', n = Side + 'LegIKKneeDnDistDimShape')
    mc.rename((mc.listRelatives(distMain, p = True)),  Side + 'LegIKStrDistDim')
    mc.rename((mc.listRelatives(distKneeLockUp, p = True)),  Side + 'LegIKKneeUpDistDim')
    mc.rename((mc.listRelatives(distKneeLockDn, p = True)),  Side + 'LegIKKneeDnDistDim')
    mc.parent(Side + 'LegIKStrDistDim' , Side + 'LegIKKneeUpDistDim' , Side + 'LegIKKneeDnDistDim' , sysDim)
    mc.connectAttr((startLoc[0] + 'Shape.worldPosition[0]'), (distMain + '.startPoint'), f = True)
    mc.connectAttr((endLoc[0] + 'Shape.worldPosition[0]'), (distMain + '.endPoint'), f = True)
    mc.connectAttr((startLoc[0] + 'Shape.worldPosition[0]'), (distKneeLockUp + '.startPoint'), f = True)
    mc.connectAttr((kneeLockLoc[0] + 'Shape.worldPosition[0]'), (distKneeLockUp + '.endPoint'), f = True)
    mc.connectAttr((kneeLockLoc[0] + 'Shape.worldPosition[0]'), (distKneeLockDn + '.startPoint'), f = True)
    mc.connectAttr((endLoc[0] + 'Shape.worldPosition[0]'), (distKneeLockDn + '.endPoint'), f = True)

    #Get input values for IK stretch
    lenghtMainDim = mc.getAttr(distMain + '.distance')
    getIKKneeTx = mc.getAttr(ikJoints[1] + '.tx')
    getIKAnklTx = mc.getAttr(ikJoints[-3] + '.tx')

    IKstretchMDs = {'scale':('pScale' + Side + 'IKLegStr_MD'),'kneeScale':('pScale' + Side + 'KneeLockUp_MD'),'ankleScale':('pScale' + Side + 'KneeLockDn_MD'),'kneeSwitch':(Side + 'KneeSwitch_MD'),'midPos':(Side + 'KneePos_MD'), 'div':(Side + 'IKLegScaleDiv_MD'), 'knee':(Side + 'KneeIKLeg_MD'), 'ankle':(Side + 'AnkleIKLeg_MD')}
    for each in IKstretchMDs.keys():
        mc.createNode('multiplyDivide', n = IKstretchMDs[each])
    limitCon = mc.createNode('condition', n = (Side + 'IKLegStrLimit_CD'))
    switchCon = mc.createNode('condition', n = (Side + 'IKLegStrSwitch CD'))
    midPosKneePMA = mc.createNode('plusMinusAverage' , n = (Side + "MidPosKnee_PMA"))
    midPosAnklePMA = mc.createNode('plusMinusAverage' , n = (Side + "MidPosAnkle_PMA"))

    upperSrtKneePMA = mc.createNode('plusMinusAverage' , n = (Side + "AddStrKnee_PMA"))
    mc.setAttr((upperSrtKneePMA+'.input1D[0]'),getIKKneeTx)
    mc.connectAttr((legCtrlsDic['Foot']+'.UpperStretch'),(upperSrtKneePMA+'.input1D[1]'))
    mc.connectAttr((upperSrtKneePMA+'.output1D'),(IKstretchMDs['knee'] + '.input1X'))
    lowerStrAnklePMA = mc.createNode('plusMinusAverage' , n = (Side + "AddStrAnkle_PMA"))
    mc.setAttr((lowerStrAnklePMA+'.input1D[0]'),getIKAnklTx)
    mc.connectAttr((legCtrlsDic['Foot']+'.LowerStretch'),(lowerStrAnklePMA+'.input1D[1]'))
    mc.connectAttr((lowerStrAnklePMA+'.output1D'),(IKstretchMDs['ankle'] + '.input1X'))

    addStrValPMA=mc.createNode('plusMinusAverage',n=(Side +'IKLegStrAdd_PMA'))
    mc.setAttr((addStrValPMA +'.input1D[0]'), lenghtMainDim)
    mc.connectAttr((legCtrlsDic['Foot']+'.UpperStretch'),(addStrValPMA+'.input1D[1]'))
    mc.connectAttr((legCtrlsDic['Foot']+'.LowerStretch'),(addStrValPMA+'.input1D[2]'))
    mc.connectAttr((addStrValPMA+'.output1D'),(IKstretchMDs['div'] + '.input2X'))

    kneeAttrBlend = mc.createNode('blendTwoAttr',n=(Side + 'kneeBlend_BTA'))
    ankleAttrBlend = mc.createNode('blendTwoAttr',n=(Side + 'AnkleBlend_BTA'))

    mc.setAttr((IKstretchMDs['scale'] + '.operation'), 2)
    mc.setAttr((IKstretchMDs['kneeScale'] + '.operation'), 2)
    mc.setAttr((IKstretchMDs['ankleScale'] + '.operation'), 2)
    mc.setAttr(midPosKneePMA+'.operation',1)
    mc.setAttr(midPosAnklePMA+'.operation',2)
    mc.setAttr((IKstretchMDs['midPos'] + '.operation'), 2)
    mc.setAttr((IKstretchMDs['midPos'] + '.input2X'), 10)
    if Side == 'Right':mc.setAttr((IKstretchMDs['midPos'] + '.input2X'), -10)
    mc.setAttr((IKstretchMDs['div'] + '.operation'), 2)

    mc.setAttr((limitCon+ '.operation'), 2)
    mc.setAttr((limitCon + '.secondTerm'), 1)
    mc.setAttr((switchCon+ '.secondTerm'), 1)

    mc.connectAttr((legCtrlsDic['Knee'] + '.KneeLock'), (IKstretchMDs['kneeSwitch'] + '.input1X'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.KneeControl'), (IKstretchMDs['kneeSwitch'] + '.input2X'), f = True)
    mc.connectAttr((distMain + '.distance'), (IKstretchMDs['scale'] + '.input1X'), f = True)
    mc.connectAttr((IKstretchMDs['scale'] + '.outputX'), (IKstretchMDs['div'] + '.input1X'), f = True)
    mc.connectAttr((IKstretchMDs['div'] + '.outputX'), (limitCon + '.firstTerm'), f = True)
    mc.connectAttr((IKstretchMDs['div'] + '.outputX'), (limitCon + '.colorIfTrueR'), f = True)
    mc.connectAttr((limitCon + '.outColorR'), (switchCon + '.colorIfTrueR'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.AutoStretch'), (switchCon + '.firstTerm'), f = True)
    mc.connectAttr((switchCon + '.outColorR'), (IKstretchMDs['knee'] + '.input2X'), f = True)
    mc.connectAttr((switchCon + '.outColorR'), (IKstretchMDs['ankle'] + '.input2X'), f = True)
    mc.connectAttr((IKstretchMDs['knee'] + '.outputX'), (midPosKneePMA +'.input1D[0]'), f = True)
    mc.connectAttr((IKstretchMDs['ankle'] + '.outputX'), (midPosAnklePMA +'.input1D[0]'), f = True)
    mc.connectAttr((legCtrlsDic['Foot'] + '.KneePos'), (IKstretchMDs['midPos'] + '.input1X'), f = True)
    mc.connectAttr((IKstretchMDs['midPos'] + '.outputX'),(midPosKneePMA +'.input1D[1]'), f = True)
    mc.connectAttr((IKstretchMDs['midPos'] + '.outputX'),(midPosAnklePMA +'.input1D[1]'), f = True)
    mc.connectAttr(((midPosKneePMA +'.output1D')), (kneeAttrBlend + '.input[0]'), f = True)
    mc.connectAttr(((midPosAnklePMA +'.output1D')), (ankleAttrBlend + '.input[0]'), f = True)
    mc.connectAttr((IKstretchMDs['kneeSwitch'] + '.outputX'), (kneeAttrBlend + '.attributesBlender'), f = True)
    mc.connectAttr((IKstretchMDs['kneeSwitch'] + '.outputX'), (ankleAttrBlend + '.attributesBlender'), f = True)
    mc.connectAttr((distKneeLockUp + '.distance'), (IKstretchMDs['kneeScale'] + '.input1X'), f = True)
    mc.connectAttr((distKneeLockDn + '.distance'), (IKstretchMDs['ankleScale'] + '.input1X'), f = True)
    mc.connectAttr((IKstretchMDs['kneeScale'] + '.outputX'), (kneeAttrBlend + '.input[1]'), f = True)
    mc.connectAttr((IKstretchMDs['ankleScale'] + '.outputX'), (ankleAttrBlend + '.input[1]'), f = True)
    mc.connectAttr((kneeAttrBlend + '.output'), (ikJoints[1] + '.tx'), f = True)
    mc.connectAttr((ankleAttrBlend + '.output'), (ikJoints[-3] + '.tx'), f = True)

    if Side == 'Right': # correcting knee lock problem
        valRevKneeLockUpMD = mc.createNode('multiplyDivide' , n = ("%sKneeLockRevUp_MD" % Side))
        mc.setAttr((valRevKneeLockUpMD + ".input2X"),-1)
        valRevKneeLockDnMD = mc.createNode('multiplyDivide' , n = ("%sKneeLockRevDn_MD" % Side))
        mc.setAttr((valRevKneeLockDnMD + ".input2X"),-1)
        
        mc.connectAttr((IKstretchMDs['kneeScale'] + '.outputX') ,  (valRevKneeLockUpMD + '.input1X'),f=True)
        mc.connectAttr((IKstretchMDs['ankleScale']+ '.outputX') ,  (valRevKneeLockDnMD + '.input1X'),f=True)
        mc.connectAttr((valRevKneeLockUpMD + '.outputX') , (kneeAttrBlend + '.input[1]'),f=True)
        mc.connectAttr((valRevKneeLockDnMD + '.outputX') , (ankleAttrBlend + '.input[1]'),f=True)
        
        # set operation values for right side manual stretch
        mc.setAttr((upperSrtKneePMA +'.operation'),2)
        mc.setAttr((lowerStrAnklePMA +'.operation'),2)

    # FK Leg
    legFKGrp = 'Grp_FKLegs'
    if not mc.objExists(legFKGrp):
        mc.group(n = legFKGrp, em = True , p = legGrp)
        mc.delete(mc.pointConstraint(hipJnt , legFKGrp))
    mc.parent(grpFKs , legFKGrp)
    mc.parentConstraint(hipJnt , legFKGrp , mo = 1)
    mc.scaleConstraint(hipJnt , legFKGrp)
    mc.parent(grpIKs , legGrp)

    tmpfkJnts=list(fkJoints)
    tmpIkJnts=list(ikJoints)
    if method:
        tmpfkJnts.pop(2)
        tmpIkJnts.pop(2)
    for i in range(len(tmpfkJnts)- 1):
        mc.orientConstraint(legCtrlsDic[(FKs[i][0])], tmpfkJnts[i], mo = True)
        if i > 0:
            mc.pointConstraint(tmpfkJnts[i], legCtrlsGrpDic[(FKs[i][1])], mo = True)
            mc.orientConstraint(legCtrlsDic[(FKs[i-1][0])], legCtrlsGrpDic[(FKs[i][1])], mo = True)
        if i == 1 or i == 2:
            getFKtx = mc.getAttr((tmpfkJnts[i] + '.tx'))
            fkStretchMulti = mc.createNode('multiplyDivide', n = (tmpfkJnts[i][:-3] + 'Stretch_MD'))
            mc.setAttr((fkStretchMulti + '.input1X'), getFKtx)
            mc.connectAttr((legCtrlsDic[(FKs[i-1][0])] + '.Stretch'), (fkStretchMulti + '.input2X'), f = True)
            mc.connectAttr((fkStretchMulti + '.outputX'), (tmpfkJnts[i] + '.tx'))
    #Snap Pivot for Ik
    snapGrp = mc.group(n =(Side + 'IKLegSnap_FK'),em=1,p=legCtrlsDic[FKs[2][0]])
    mc.delete(mc.parentConstraint(legCtrlsDic['Foot'],snapGrp))
            
    # Constraining IKFK Legs
    switchRevIKFK = mc.createNode('reverse' ,  n = Side + 'LegIKFK_Rev')
    mc.connectAttr((legCtrlsDic['LegIKFK'] + '.IKFK'), (switchRevIKFK + '.inputX'), f = True)
    for i in range(jntCount):
        switchCon = mc.orientConstraint(fkJoints[i], ikJoints[i], legJnts[i], mo = True)
        switchConTargets = mc.orientConstraint(switchCon[0], q = True, tl = True)
        mc.connectAttr((legCtrlsDic['LegIKFK'] + '.IKFK'), (switchCon[0] + '.' + switchConTargets[0] + 'W0'), f = True)
        mc.connectAttr((switchRevIKFK + '.outputX'),(switchCon[0] + '.' + switchConTargets[1] + 'W1'), f = True)
        tmpI=2
        if method:tmpI=3
        if i == 1 or i == tmpI:
            n=i
            if i==3:n=2
            print tmpLegJnts[n]
            print tmpIkJnts[n]
            legBlendColors = mc.createNode('blendColors' , n = (tmpLegJnts[n][:-3] + "_BC"))
            mc.connectAttr((tmpfkJnts[n] + '.tx'), (legBlendColors + '.color1R'))
            mc.connectAttr((tmpIkJnts[n] + '.tx'), (legBlendColors + '.color2R'))
            mc.connectAttr((legBlendColors + '.outputR'), (tmpLegJnts[n] + '.tx'))
            mc.connectAttr((legCtrlsDic['LegIKFK'] + '.IKFK') , (legBlendColors + '.blender'))
            
    #Parenting to Main Grp
    legCtrls = legCtrlsDic.values()
            
    #Bend Joint Creation
    if bendOnOff:
        if not mc.attributeQuery( 'BendControls', node= legCtrlsDic['LegIKFK'],ex=1):
            mc.addAttr(legCtrlsDic['LegIKFK'], ln ='BendControls', at = 'bool', k = False)
            mc.setAttr((legCtrlsDic['LegIKFK'] + '.BendControls'), cb = True)
        getUpBendGrps = BJ.ar_crtBendJntz(legJnts[0] , legJnts[1] , Side, 'Leg', 'Up' , bendJnts)
        getDnBendGrps = BJ.ar_crtBendJntz(legJnts[-4] , legJnts[-3] , Side, 'Leg', 'Dn' , bendJnts)
        mc.connectAttr((legCtrlsDic['LegIKFK'] + '.BendControls') , (getUpBendGrps[0] + '.v'))
        legCtrls +=  [getUpBendGrps[3],getDnBendGrps[3]]

    #add rightClick attributes
    for obj in legCtrls:
        mc.addAttr(obj , sn='IKFKpos' , at='message')
        mc.connectAttr(legCtrlsDic['LegIKFK'] + '.message' , obj + '.IKFKpos')
        if obj != legCtrlsDic['LegIKFK']:
            attrName = obj.split('_')[1].replace(Side,'')
            mc.addAttr(legCtrlsDic['LegIKFK'], sn=attrName , at='message')
            mc.connectAttr(obj + '.message' , legCtrlsDic['LegIKFK'] + '.%s' %attrName)

    snapObjs = ikJoints[:3] +[snapGrp]
    for each in snapObjs:
            attrName = each.split('_')[0].replace(Side,'')
            if each != snapGrp:attrName = attrName + 'Jnt'
            mc.addAttr(legCtrlsDic['LegIKFK'], sn=attrName , at='message')
            mc.connectAttr(each + '.message' , legCtrlsDic['LegIKFK'] + '.%s' %attrName)

    # Quick Selection Set		
    mc.sets(legCtrls, t = 'gCharacterSet', name = (Side + 'Leg_Sets'))

    # LocknHide Unused Attributes
    tools.lockhide(legCtrlsDic['Foot'],('sx', 'sy', 'sz', 'v'), 1)
    tools.lockhide(legCtrlsDic['Knee'],('tx' , 'ty' , 'tz'))
    tools.lockhide(legCtrlsDic['LegIKFK'],())
    for i in range(4):
        tools.lockhide((legCtrlsDic[(FKs[i][0])]),('rx', 'ry', 'rz'))

    ##########################################################################