											#--------------------------------------------------------------#
											#		TOONZ ANIMATION INDIA Pvt Ltd - RIGGING DEPARTMENT	   #					
											#   --------------------------------------------------         #
											# 	DESCRIPTION	: Main Python Module for Right Click Menu      #	 																		   
											# 	AUTHOR 			: Arun . S - arunpillaii@gmail.com         #                    												                       				                     
											# 	VERSION			: 1.00 , 26 November 2009                  #
											#   Copyright (C) 2009.  All rights reserved.				   #
											#--------------------------------------------------------------#
											#    Revised by Stani. NS
											#    V2.0 , 10 Oct 2014  
#Imports
import maya.cmds as mc

#==============================================================================================================#
#Marking Menus For RightClickMenu
def ar_switchMenus(passObj):
	print 'passObj: %s' %passObj 
	if mc.objExists (passObj + ".IKFKpos"):
		getswitchCtrl = mc.listConnections(passObj + '.IKFKpos')[0]
		print 'getswitchCtrl: %s' %getswitchCtrl
		if 'ArmIKFK' in getswitchCtrl or 'LegIKFK' in getswitchCtrl:
			mc.menuItem(l = 'Switch IK <> FK' , c = lambda event:ar_snapIKFK(getswitchCtrl) , rp = 'NW' ,  bld = True ,  ecr = 1)
			mc.menuItem(l = 'Switch IK <> FK + Key' , c = lambda event:ar_snapIKFK(getswitchCtrl, key=True) , rp = 'NE' ,  bld = True ,  ecr = 1)
			mc.menuItem(l = 'Reverse Limb', c = lambda event:ar_reverseSide(getswitchCtrl) , en = 1 , rp = 'W',  bld = True ,  ecr = 1)
			mc.menuItem(l = 'Mirror Limb', c = lambda event:ar_mirrorCtrls(getswitchCtrl) , en = 1 , rp = 'E',  bld = True ,  ecr = 1)
			mc.menuItem(l = 'Reset', c = lambda event:ar_resetAttr(passObj) , en = 1 , rp = 'SE',  bld = True ,  ecr = 1)
			mc.menuItem(l = 'Reset All', c = lambda event:ar_resetAttr(passObj,1) , en = 1 , rp = 'SW',  bld = True ,  ecr = 1)
			if 'ArmIKFK' in getswitchCtrl and passObj == mc.listConnections(mc.listConnections(passObj + '.IKFKpos')[0] + '.ElbowPole')[0] :
				mc.menuItem(l = 'Toggle ElbowLock', c = lambda event:ar_ElKnLock(getswitchCtrl) , en = 1 , rp = 'NW',  bld = True ,  ecr = 1)	
			if 'LegIKFK' in getswitchCtrl and passObj == mc.listConnections(mc.listConnections(passObj + '.IKFKpos')[0] + '.Knee')[0]:
				mc.menuItem(l = 'Toggle KneeLock', c = lambda event:ar_ElKnLock(getswitchCtrl) , en = 1 , rp = 'NW',  bld = True ,  ecr = 1)	
	
	if mc.objExists (passObj + ".ParentBlend") or mc.objExists (passObj + ".Parent_RCD"):
		if mc.objExists (passObj + ".ParentBlend"):
			getEnum =  mc.attributeQuery('Parent0' , n = passObj , le = True)[0]
		elif mc.objExists (passObj + ".Parent_RCD"):
			getEnum =  mc.attributeQuery('Parent' , n = passObj , le = True)[0]
		getEnumAttrs = getEnum.split(':')
		mc.menuItem(l = 'Parent to' , sm = 1 , rp = 'S' ,  bld = True)
		for i in range(len(getEnumAttrs)):
			menuItemLine = 'mc.menuItem(("' + getEnumAttrs[i] + 'MI") , l = "' + getEnumAttrs[i] + '", c = \'import ar_menuScripts as ms;ms.ar_setDynParent(' + str(i) + ',"' + passObj + '")\' ,en = 1, ecr = 0)'
			eval(menuItemLine)

	if mc.objExists (passObj + ".Spine_RCDriver"):
		getswitchCtrl = mc.listConnections(passObj + '.Spine_RCDriver')[0]
		mc.menuItem(l = 'Reverse Spine' , c = lambda event:ar_reverseSide(getswitchCtrl) , rp = 'N' ,  bld = True ,  ecr = 1)
		mc.menuItem(l = 'Reset' , c = lambda event:ar_resetAttr(passObj) , rp = 'SE' ,  bld = True ,  ecr = 1)
		mc.menuItem(l = 'Reset All', c = lambda event:ar_resetAttr(passObj,1) , en = 1 , rp = 'SW',  bld = True ,  ecr = 1)

	if mc.objExists (passObj + ".Head_RCDriver"):
		getswitchCtrl = mc.listConnections(passObj + '.Head_RCDriver')[0]
		mc.menuItem(l = 'Reverse Head' , c = lambda event:ar_reverseSide(getswitchCtrl) , rp = 'N' ,  bld = True ,  ecr = 1)
		mc.menuItem(l = 'Reset' , c = lambda event:ar_resetAttr(passObj) , rp = 'SE' ,  bld = True ,  ecr = 1)
		mc.menuItem(l = 'Reset All', c = lambda event:ar_resetAttr(passObj,1) , en = 1 , rp = 'SW',  bld = True ,  ecr = 1)

	if mc.objExists (passObj + ".FingerPos"):
		getswitchCtrl = mc.listConnections(passObj + '.FingerPos')[0]
		print 'getswitchCtrl: %s' %getswitchCtrl 
		mc.menuItem(l = 'Mirror All' , c = lambda event:sn_mirrorFingers(getswitchCtrl) , rp = 'N' ,  bld = True ,  ecr = 1)
		#mc.menuItem(l = 'Mirror Ctrl', c = lambda event:ar_reverseSide(getswitchCtrl) , en = 1 , rp = 'W',  bld = True ,  ecr = 1)
		#mc.menuItem(l = 'Mirror Finger', c = lambda event:ar_mirrorCtrls(getswitchCtrl) , en = 1 , rp = 'E',  bld = True ,  ecr = 1)
		mc.menuItem(l = 'Reset', c = lambda event:ar_resetAttr(passObj) , en = 1 , rp = 'SE',  bld = True ,  ecr = 1)
		mc.menuItem(l = 'Reset All', c = lambda event:ar_resetAttr(passObj,1) , en = 1 , rp = 'SW',  bld = True ,  ecr = 1)		
		

#==============================================================================================================#


def sn_mirrorFingers(switchCtrl):
    mc.undoInfo( ock = True )
    #getIKFKVal = mc.getAttr((switchCtrl + '.IKFK'))
    print switchCtrl
    if 'Left' in switchCtrl:
        side = 'Left'
        swapSide = 'Right'
        swapCtrl = switchCtrl.replace('Left', 'Right')
    elif 'Right' in switchCtrl:
        side = 'Right'
        swapSide = 'Left'
        swapCtrl = switchCtrl.replace('Right', 'Left')		
    try:    
        mAttr = [i for i in mc.listAttr( switchCtrl, ud=1 ) if mc.attributeQuery( i, node=switchCtrl, at=1 )=='message']         
        print mAttr
        if 'FingerPos' in mAttr: mAttr.remove('FingerPos')
        kAttr = mc.listAttr( switchCtrl, ud=1, k=1 )
        for attr in kAttr:    mc.setAttr( '%s.%s' %(swapCtrl,attr), mc.getAttr( '%s.%s' %(switchCtrl,attr) )  )
        for attr in mAttr:
            srcObj = mc.listConnections( '%s.%s' %(switchCtrl,attr) )[0]
            t      = mc.getAttr( '%s.t' %srcObj )[0]
            r      = mc.getAttr( '%s.r' %srcObj )[0]
            s      = mc.getAttr( '%s.stretch' %srcObj )
            dstObj = mc.listConnections( '%s.%s' %(swapCtrl,attr) )[0]
            mc.setAttr( '%s.t' %dstObj, t[0]*-1,t[1]*-1,t[2]*-1 )
            mc.setAttr( '%s.r' %dstObj, r[0],r[1],r[2] )
            mc.setAttr( '%s.stretch' %dstObj, s )	    
    except:    pass
    mc.undoInfo(cck = True )

#'Ctrl_LeftHand'.replace('Left', 'Right')

#Mirror Contol Values to the Opposite Side
def ar_mirrorCtrls(switchCtrl):
	mc.undoInfo( ock = True )
	getIKFKVal = mc.getAttr((switchCtrl + '.IKFK'))
	if 'Left' in switchCtrl:
		side = 'Left'
		swapSide = 'Right'
	elif 'Right' in switchCtrl:
		side = 'Right'
		swapSide = 'Left'
	try:
		#----------------------------------------------------------------------------------------------------------#		
		#Mirror Control Values of Arm
		if 'ArmIKFK' in switchCtrl:
			if mc.attributeQuery( 'Clavicle', node=switchCtrl, ex=True ):
				getClavicle = mc.listConnections((switchCtrl + '.Clavicle'))
				if getClavicle:
					getClavicle=getClavicle[0]
					getClavicleTransVal = mc.getAttr((getClavicle + '.t'))
					getClaviclePBVal = mc.getAttr((getClavicle + '.ParentBlend'))
					getClavicleP0Val = mc.getAttr((getClavicle + '.Parent0'))
					getClavicleP1Val = mc.getAttr((getClavicle + '.Parent1'))
					mirrorClavicle = getClavicle.replace(side , swapSide)
					
					mc.setAttr((mirrorClavicle + '.t'),-getClavicleTransVal[0][0] , getClavicleTransVal[0][1] ,getClavicleTransVal[0][2])
					mc.setAttr((mirrorClavicle + '.ParentBlend'),getClaviclePBVal)
					mc.setAttr((mirrorClavicle + '.Parent0'),getClavicleP0Val)
					mc.setAttr((mirrorClavicle + '.Parent1'),getClavicleP1Val)
			
			#Cntrls = [mc.listConnections(switchCtrl + '.Hand')[0]]
			Cntrls = mc.listConnections(switchCtrl + '.Hand') 
			
			fingCntrlGrp = mc.listConnections(mc.listConnections(switchCtrl + '.Hand')[0] + '.FingerControl')[0]
			#fingCntrlGrp = mc.listConnections(Cntrls + '.FingerControl')

			Cntrls.extend([mc.listRelatives(obj , p = 1)[0] for obj in (mc.listRelatives(fingCntrlGrp , ad = 1 , type = 'nurbsCurve'))])
			print Cntrls
			for objc in Cntrls:
				mirrorCntrl = objc.replace(side , swapSide)
				getCB = mc.listAttr(objc , k = True ,  u = 1 , v = 1)
				for attr in getCB:
					val = mc.getAttr(objc + '.%s' % attr)
					mc.setAttr(mirrorCntrl + '.%s' % attr , val)
				
			if getIKFKVal == 0:
				mirrorIKFK = switchCtrl.replace(side , swapSide)
				getIKFKVal = mc.setAttr((mirrorIKFK + '.IKFK'), 0)
				
				getIKArm = mc.listConnections((switchCtrl + '.Arm'))[0]
				getIKArmTransVal = mc.getAttr((getIKArm + '.t'))
				getIKArmRotVal = mc.getAttr((getIKArm + '.r'))
				getIKArmStrVal = mc.getAttr((getIKArm + '.AutoStretch'))
				getIKArmAlignVal = mc.getAttr((getIKArm + '.ArmAlign'))
				getIKArmPBVal = mc.getAttr((getIKArm + '.ParentBlend'))
				getIKArmP0Val = mc.getAttr((getIKArm + '.Parent0'))
				getIKArmP1Val = mc.getAttr((getIKArm + '.Parent1'))
				mirrorIKArm = getIKArm.replace(side , swapSide)
			
				mc.setAttr((mirrorIKArm + '.t'), -getIKArmTransVal[0][0] , -getIKArmTransVal[0][1] ,-getIKArmTransVal[0][2])
				mc.setAttr((mirrorIKArm + '.r'), getIKArmRotVal[0][0] , getIKArmRotVal[0][1] ,getIKArmRotVal[0][2])
				mc.setAttr((mirrorIKArm + '.AutoStretch'),getIKArmStrVal)
				mc.setAttr((mirrorIKArm + '.ArmAlign'),getIKArmAlignVal)
				mc.setAttr((mirrorIKArm + '.ParentBlend'),getIKArmPBVal)
				mc.setAttr((mirrorIKArm + '.Parent0'),getIKArmP0Val)
				mc.setAttr((mirrorIKArm + '.Parent1'),getIKArmP1Val)
				
				getIKElbow = mc.listConnections((switchCtrl + '.ElbowPole'))[0]
				getIKElbowVal = mc.getAttr((getIKElbow + '.t'))
				getIKElbowPBVal = mc.getAttr((getIKElbow + '.ParentBlend'))
				getIKElbowP0Val = mc.getAttr((getIKElbow + '.Parent0'))
				getIKElbowP1Val = mc.getAttr((getIKElbow + '.Parent1'))
				mirrorIKElbow = getIKElbow.replace(side , swapSide)
				
				mc.setAttr((mirrorIKElbow + '.t'), -getIKElbowVal[0][0] , getIKElbowVal[0][1] ,getIKElbowVal[0][2])
				mc.setAttr((mirrorIKElbow + '.ParentBlend'),getIKElbowPBVal)
				mc.setAttr((mirrorIKElbow + '.Parent0'),getIKElbowP0Val)
				mc.setAttr((mirrorIKElbow + '.Parent1'),getIKElbowP1Val)
				
			if getIKFKVal == 1:
				mirrorIKFK = switchCtrl.replace(side , swapSide)
				getIKFKVal = mc.setAttr((mirrorIKFK + '.IKFK'), 1)
				
				getFKShoulder = mc.listConnections((switchCtrl + '.ShoulderFK'))[0]
				getFKShoulderRotVal = mc.getAttr((getFKShoulder + '.r'))
				getFKShoulderStrVal = mc.getAttr((getFKShoulder + '.Stretch'))
				mirrorFKShoulder = getFKShoulder.replace(side , swapSide)
				
				mc.setAttr((mirrorFKShoulder + '.r'), getFKShoulderRotVal[0][0] , getFKShoulderRotVal[0][1] ,getFKShoulderRotVal[0][2])
				mc.setAttr((mirrorFKShoulder + '.Stretch'),getFKShoulderStrVal)
				
				getFKElbow = mc.listConnections((switchCtrl + '.ElbowFK'))[0]
				getFKElbowRotVal = mc.getAttr((getFKElbow + '.r'))
				getFKElbowStrVal = mc.getAttr((getFKElbow + '.Stretch'))
				mirrorFKElbow = getFKElbow.replace(side , swapSide)
				
				mc.setAttr((mirrorFKElbow + '.r'), getFKElbowRotVal[0][0] , getFKElbowRotVal[0][1] ,getFKElbowRotVal[0][2])
				mc.setAttr((mirrorFKElbow + '.Stretch'),getFKElbowStrVal)
				
				getFKWrist = mc.listConnections((switchCtrl + '.WristFK'))[0]
				getFKWristRotVal = mc.getAttr((getFKWrist + '.r'))
				mirrorFKWrist = getFKWrist.replace(side , swapSide)
				
				mc.setAttr((mirrorFKWrist + '.r'), getFKWristRotVal[0][0] , getFKWristRotVal[0][1] ,getFKWristRotVal[0][2])
			# For Bend Controls
			if mc.attributeQuery('BendControls', typ=switchCtrl,ex=True ):
				getBendControlVal = mc.getAttr((switchCtrl + '.BendControls'))
				mirrorswitchCtrl = switchCtrl.replace(side , swapSide)
				if getBendControlVal:
					#Query Attributes
						getBendUp = mc.listConnections((switchCtrl + '.ArmBendUp'))[0]	
						mirrorBendUp = getBendUp.replace(side , swapSide)
						getBendUpTransVal = mc.getAttr((getBendUp + '.t'))
						getBendUpTwistUp = mc.getAttr((getBendUp + '.UpTwist'))
						getBendUpTwistDn = mc.getAttr((getBendUp + '.DnTwist'))
						getBendDn = mc.listConnections((switchCtrl + '.ArmBendDn'))[0]	
						mirrorBendDn = getBendDn.replace(side , swapSide)
						getBendDnTransVal = mc.getAttr((getBendDn + '.t'))
						getBendDnTwistUp = mc.getAttr((getBendDn + '.UpTwist'))
						getBendDnTwistDn = mc.getAttr((getBendDn + '.DnTwist'))
						
						#Set Attributes
						mc.setAttr((mirrorswitchCtrl + '.BendControls'),1)
						mc.setAttr((mirrorBendUp + '.t'), -getBendUpTransVal[0][0] , -getBendUpTransVal[0][1] ,-getBendUpTransVal[0][2])
						mc.setAttr((mirrorBendUp + '.UpTwist'),getBendUpTwistUp)
						mc.setAttr((mirrorBendUp + '.DnTwist'),getBendUpTwistDn)
						mc.setAttr((mirrorBendDn + '.t'), -getBendDnTransVal[0][0] , -getBendDnTransVal[0][1] ,-getBendDnTransVal[0][2])
						mc.setAttr((mirrorBendDn + '.UpTwist'),getBendDnTwistUp)
						mc.setAttr((mirrorBendDn + '.DnTwist'),getBendDnTwistDn)	
					
			getGimbalControlVal = mc.getAttr((switchCtrl + '.GimbalControl'))
			if getBendControlVal:
				#Query Attributes
				getGimbal = mc.listConnections((switchCtrl + '.HandGimbal'))[0]	
				mirrorGimbal = getGimbal.replace(side , swapSide)
				getGimbalRotVal = mc.getAttr((getGimbal + '.r'))
				
				#Set Attributes
				mc.setAttr((mirrorswitchCtrl + '.GimbalControl'),1)
				mc.setAttr((mirrorGimbal + '.r'), getGimbalRotVal[0][0] , getGimbalRotVal[0][1] ,getGimbalRotVal[0][2])
		#----------------------------------------------------------------------------------------------------------#	
		#Mirror Control Values of Leg
		#Leg Confirmation
		if 'LegIKFK' in switchCtrl:
			#For IK Mode
			if getIKFKVal == 0:
				mirrorIKFK = switchCtrl.replace(side , swapSide)# Swaping the Side
				mc.setAttr((mirrorIKFK + '.IKFK'), 0)
				
				#Query attibutes
				getIKLeg = mc.listConnections((switchCtrl + '.Foot'))[0]
				getIKLegTransVal = mc.getAttr((getIKLeg + '.t'))
				getIKLegRotVal = mc.getAttr((getIKLeg + '.r'))
				getIKLegStrVal = mc.getAttr((getIKLeg + '.AutoStretch'))
				getIKLegKneePosVal = mc.getAttr((getIKLeg + '.KneePos'))
				getIKLegFootRollVal = mc.getAttr((getIKLeg + '.FootRoll'))
				getIKLegFootAngleVal = mc.getAttr((getIKLeg + '.RollAngle'))
				getIKLegToeRollVal = mc.getAttr((getIKLeg + '.ToeRoll'))
				getIKLegFootLeanVal = mc.getAttr((getIKLeg + '.FootLean'))
				getIKLegHeelPivotVal = mc.getAttr((getIKLeg + '.HeelPivot'))
				getIKLegToePivotVal = mc.getAttr((getIKLeg + '.ToePivot'))
				getIKLegTwistVal = mc.getAttr((getIKLeg + '.Twist'))
				getIKLegKneeControlVal = mc.getAttr((getIKLeg + '.KneeControl'))
					
				#Set Attributes to the Opposite Side
				mirrorIKLeg = getIKLeg.replace(side , swapSide)
				mc.setAttr((mirrorIKLeg + '.t'), -getIKLegTransVal[0][0] , getIKLegTransVal[0][1] ,getIKLegTransVal[0][2])
				mc.setAttr((mirrorIKLeg + '.r'), getIKLegRotVal[0][0] , -getIKLegRotVal[0][1] ,-getIKLegRotVal[0][2])
				mc.setAttr((mirrorIKLeg + '.AutoStretch'),getIKLegStrVal)
				mc.setAttr((mirrorIKLeg + '.KneePos'),getIKLegKneePosVal)
				mc.setAttr((mirrorIKLeg + '.FootRoll'),getIKLegFootRollVal)
				mc.setAttr((mirrorIKLeg + '.RollAngle'),getIKLegFootAngleVal)
				mc.setAttr((mirrorIKLeg + '.ToeRoll'),getIKLegToeRollVal)
				mc.setAttr((mirrorIKLeg + '.FootLean'),-getIKLegFootLeanVal)
				mc.setAttr((mirrorIKLeg + '.HeelPivot'),-getIKLegHeelPivotVal)
				mc.setAttr((mirrorIKLeg + '.ToePivot'),getIKLegToePivotVal)
				mc.setAttr((mirrorIKLeg + '.Twist'),-getIKLegTwistVal)
				mc.setAttr((mirrorIKLeg + '.KneeControl'),getIKLegKneeControlVal)
				#For Knee Control
				if getIKLegKneeControlVal:
					getIKKnee = mc.listConnections((switchCtrl + '.Knee'))[0]
					getIKKneeTransVal = mc.getAttr((getIKKnee + '.t'))
					getIKKneeLockVal = mc.getAttr((getIKKnee + '.KneeLock'))
					mirrorIKKnee = getIKKnee.replace(side , swapSide)
					
					mc.setAttr((mirrorIKKnee + '.t'), -getIKKneeTransVal[0][0] , getIKKneeTransVal[0][1] ,getIKKneeTransVal[0][2])
					mc.setAttr((mirrorIKKnee + '.KneeLock'),getIKKneeLockVal)
			
			#For FK Mode	
			if getIKFKVal == 1:
				mirrorIKFK = switchCtrl.replace(side , swapSide)
				getIKFKVal = mc.setAttr((mirrorIKFK + '.IKFK'), 1)
				
				#FKLeg 
				getFKHip = mc.listConnections((switchCtrl + '.FKLeg'))[0]
				getFKHipRotVal = mc.getAttr((getFKHip + '.r'))
				getFKHipStrVal = mc.getAttr((getFKHip + '.Stretch'))
				mirrorFKHip = getFKHip.replace(side , swapSide)
				
				mc.setAttr((mirrorFKHip + '.r'), getFKHipRotVal[0][0] , getFKHipRotVal[0][1] ,getFKHipRotVal[0][2])
				mc.setAttr((mirrorFKHip + '.Stretch'),getFKHipStrVal)
				
				#FK Knee
				getFKKnee = mc.listConnections((switchCtrl + '.FKKnee'))[0]
				getFKKneeRotVal = mc.getAttr((getFKKnee + '.r'))
				getFKKneeStrVal = mc.getAttr((getFKKnee + '.Stretch'))
				mirrorFKKnee = getFKKnee.replace(side , swapSide)
				
				mc.setAttr((mirrorFKKnee + '.r'), getFKKneeRotVal[0][0] , getFKKneeRotVal[0][1] ,getFKKneeRotVal[0][2])
				mc.setAttr((mirrorFKKnee + '.Stretch'),getFKKneeStrVal)
				
			 	#FK Ankle
				getFKAnkle = mc.listConnections((switchCtrl + '.FKAnkle'))[0]
				getFKAnkleRotVal = mc.getAttr((getFKAnkle + '.r'))
				mirrorFKAnkle = getFKAnkle.replace(side , swapSide)
				
				mc.setAttr((mirrorFKAnkle + '.r'), getFKAnkleRotVal[0][0] , getFKAnkleRotVal[0][1] ,getFKAnkleRotVal[0][2])
				
				#FK Toe
				getFKBall = mc.listConnections((switchCtrl + '.FKToe'))[0]
				getFKBallRotVal = mc.getAttr((getFKBall + '.r'))
				mirrorFKBall = getFKBall.replace(side , swapSide)
				
				mc.setAttr((mirrorFKBall + '.r'), getFKBallRotVal[0][0] , getFKBallRotVal[0][1] ,getFKBallRotVal[0][2])
			
			# For Bend Controls
			getBendControlVal = mc.getAttr((switchCtrl + '.BendControls'))
			mirrorswitchCtrl = switchCtrl.replace(side , swapSide)
			if getBendControlVal:
				#Query Attributes
				getBendUp = mc.listConnections((switchCtrl + '.LegBendUp'))[0]	
				mirrorBendUp = getBendUp.replace(side , swapSide)
				getBendUpTransVal = mc.getAttr((getBendUp + '.t'))
				getBendUpTwistUp = mc.getAttr((getBendUp + '.UpTwist'))
				getBendUpTwistDn = mc.getAttr((getBendUp + '.DnTwist'))
				getBendDn = mc.listConnections((switchCtrl + '.LegBendDn'))[0]	
				mirrorBendDn = getBendDn.replace(side , swapSide)
				getBendDnTransVal = mc.getAttr((getBendDn + '.t'))
				getBendDnTwistUp = mc.getAttr((getBendDn + '.UpTwist'))
				getBendDnTwistDn = mc.getAttr((getBendDn + '.DnTwist'))
				
				#Set Attributes
				mc.setAttr((mirrorswitchCtrl + '.BendControls'),1)
				mc.setAttr((mirrorBendUp + '.t'), -getBendUpTransVal[0][0] , -getBendUpTransVal[0][1] ,-getBendUpTransVal[0][2])
				mc.setAttr((mirrorBendUp + '.UpTwist'),getBendUpTwistUp)
				mc.setAttr((mirrorBendUp + '.DnTwist'),getBendUpTwistDn)
				mc.setAttr((mirrorBendDn + '.t'), -getBendDnTransVal[0][0] , -getBendDnTransVal[0][1] ,-getBendDnTransVal[0][2])
				mc.setAttr((mirrorBendDn + '.UpTwist'),getBendDnTwistUp)
				mc.setAttr((mirrorBendDn + '.DnTwist'),getBendDnTwistDn)
	except (RuntimeError , TypeError):
				pass
	mc.undoInfo(cck = True )
	
#==============================================================================================================#

#Function For Swaping Left to Right and Right to Left
def ar_reverseSide(switchCtrl):
	mc.undoInfo( ock = True )
	if 'Left' in switchCtrl:
		side = 'Left'
		swapSide = 'Right'
	elif 'Right' in switchCtrl:
		side = 'Right'
		swapSide = 'Left'
	try:
		#----------------------------------------------------------------------------------------------------------#	
		#Arms
		if 'ArmIKFK' in switchCtrl:
			getIKFKVal = mc.getAttr((switchCtrl + '.IKFK'))
		
			getClavicle=[]
			if mc.attributeQuery( 'Clavicle', node=switchCtrl, ex=True ):
				getClavicle = mc.listConnections((switchCtrl + '.Clavicle'))
				if getClavicle:
					getClavicle=getClavicle[0]
					oppositeClavicle = getClavicle.replace(side , swapSide)
					getOppClavicleTransVal = mc.getAttr((oppositeClavicle + '.t'))
			
			getIKArm = mc.listConnections((switchCtrl + '.Arm'))[0]
			oppositeIKArm = getIKArm.replace(side , swapSide)
			getOppIKArmTransVal = mc.getAttr((oppositeIKArm + '.t'))
			getOppIKArmRotVal = mc.getAttr((oppositeIKArm + '.r'))
			getOppIKArmStrVal = mc.getAttr((oppositeIKArm + '.AutoStretch'))
	
			getIKElbow = mc.listConnections((switchCtrl + '.ElbowPole'))[0]
			oppositeIKElbow = getIKElbow.replace(side , swapSide)
			getOppIKElbowVal = mc.getAttr((oppositeIKElbow + '.t'))
			
			getFKShoulder = mc.listConnections((switchCtrl + '.ShoulderFK'))[0]
			OppositeFKShoulder = getFKShoulder.replace(side , swapSide)
			getOppFKShoulderRotVal = mc.getAttr((OppositeFKShoulder + '.r'))
			getOppFKShoulderStrVal = mc.getAttr((OppositeFKShoulder + '.Stretch'))
			
			getFKElbow = mc.listConnections((switchCtrl + '.ElbowFK'))[0]
			oppositFKElbow = getFKElbow.replace(side , swapSide)
			getOppFKElbowRotVal = mc.getAttr((oppositFKElbow + '.r'))
			getOppFKElbowStrVal = mc.getAttr((oppositFKElbow + '.Stretch'))
			
			getFKWrist = mc.listConnections((switchCtrl + '.WristFK'))[0]
			oppositeFKWrist = getFKWrist.replace(side , swapSide)
			getOppFKWristRotVal = mc.getAttr((oppositeFKWrist + '.r'))
			
			# For Bend Controls
			getBendControlVal = mc.getAttr((switchCtrl + '.BendControls'))
			if getBendControlVal:
			#Query Attributes
				getBendUp = mc.listConnections((switchCtrl + '.ArmBendUp'))[0]	
				mirrorBendUp = getBendUp.replace(side , swapSide)
				getBendUpTransVal = mc.getAttr((mirrorBendUp + '.t'))
				getBendUpTwistUp = mc.getAttr((mirrorBendUp + '.UpTwist'))
				getBendUpTwistDn = mc.getAttr((mirrorBendUp + '.DnTwist'))
				getBendDn = mc.listConnections((switchCtrl + '.ArmBendDn'))[0]	
				mirrorBendDn = getBendDn.replace(side , swapSide)
				getBendDnTransVal = mc.getAttr((mirrorBendDn + '.t'))
				getBendDnTwistUp = mc.getAttr((mirrorBendDn + '.UpTwist'))
				getBendDnTwistDn = mc.getAttr((mirrorBendDn + '.DnTwist'))
	
			ar_mirrorCtrls(switchCtrl)
			
			if getClavicle:
				mc.setAttr((getClavicle + '.t'),-getOppClavicleTransVal[0][0] , getOppClavicleTransVal[0][1] ,getOppClavicleTransVal[0][2])
			
			if getIKFKVal == 0:
				mc.setAttr((getIKArm + '.t'), -getOppIKArmTransVal[0][0] , -getOppIKArmTransVal[0][1] ,-getOppIKArmTransVal[0][2])
				mc.setAttr((getIKArm + '.r'), getOppIKArmRotVal[0][0] , getOppIKArmRotVal[0][1] ,getOppIKArmRotVal[0][2])
				mc.setAttr((getIKArm + '.AutoStretch'),getOppIKArmStrVal)
			
				mc.setAttr((getIKElbow + '.t'), -getOppIKElbowVal[0][0] , -getOppIKElbowVal[0][1] ,-getOppIKElbowVal[0][2])
			
			if getIKFKVal == 1:
				mc.setAttr((getFKShoulder + '.r'), getOppFKShoulderRotVal[0][0] , getOppFKShoulderRotVal[0][1] ,getOppFKShoulderRotVal[0][2])
				mc.setAttr((getFKShoulder + '.Stretch'),getOppFKShoulderStrVal)
				
				mc.setAttr((getFKElbow + '.r'), getOppFKElbowRotVal[0][0] , getOppFKElbowRotVal[0][1] ,getOppFKElbowRotVal[0][2])
				mc.setAttr((getFKElbow + '.Stretch'),getOppFKElbowStrVal)
			
				mc.setAttr((getFKWrist + '.r'), getOppFKWristRotVal[0][0] , getOppFKWristRotVal[0][1] ,getOppFKWristRotVal[0][2])
			
			#Set Bend Attributes
			if getBendControlVal:
				mc.setAttr((getBendUp + '.t'), -getBendUpTransVal[0][0] , -getBendUpTransVal[0][1] ,-getBendUpTransVal[0][2])
				mc.setAttr((getBendUp + '.UpTwist'),getBendUpTwistUp)
				mc.setAttr((getBendUp + '.DnTwist'),getBendUpTwistDn)
				mc.setAttr((getBendDn + '.t'), -getBendDnTransVal[0][0] , -getBendDnTransVal[0][1] ,-getBendDnTransVal[0][2])
				mc.setAttr((getBendDn + '.UpTwist'),getBendDnTwistUp)
				mc.setAttr((getBendDn + '.DnTwist'),getBendDnTwistDn)
		#----------------------------------------------------------------------------------------------------------#	
		#Legs
		if 'LegIKFK' in switchCtrl:
			getIKFKVal = mc.getAttr((switchCtrl + '.IKFK'))	
			
			#Query attibutes
			getIKLeg = mc.listConnections((switchCtrl + '.Foot'))[0]
			mirrorIKLeg = getIKLeg.replace(side , swapSide)
			getIKLegTransVal = mc.getAttr((mirrorIKLeg + '.t'))
			getIKLegRotVal = mc.getAttr((mirrorIKLeg + '.r'))
			getIKLegStrVal = mc.getAttr((mirrorIKLeg + '.AutoStretch'))
			getIKLegKneePosVal = mc.getAttr((mirrorIKLeg + '.KneePos'))
			getIKLegFootRollVal = mc.getAttr((mirrorIKLeg + '.FootRoll'))
			getIKLegFootAngleVal = mc.getAttr((mirrorIKLeg + '.RollAngle'))
			getIKLegToeRollVal = mc.getAttr((mirrorIKLeg + '.ToeRoll'))
			getIKLegFootLeanVal = mc.getAttr((mirrorIKLeg + '.FootLean'))
			getIKLegHeelPivotVal = mc.getAttr((mirrorIKLeg + '.HeelPivot'))
			getIKLegToePivotVal = mc.getAttr((mirrorIKLeg + '.ToePivot'))
			getIKLegTwistVal = mc.getAttr((mirrorIKLeg + '.Twist'))
			getIKLegKneeControlVal = mc.getAttr((mirrorIKLeg + '.KneeControl'))
			#For Knee Control
			if getIKLegKneeControlVal:
				getIKKnee = mc.listConnections((switchCtrl + '.Knee'))[0]
				mirrorIKKnee = getIKKnee.replace(side , swapSide)
				getIKKneeTransVal = mc.getAttr((mirrorIKKnee + '.t'))
				getIKKneeLockVal = mc.getAttr((mirrorIKKnee + '.KneeLock'))
	
			#FKLeg 
			getFKHip = mc.listConnections((switchCtrl + '.FKLeg'))[0]
			mirrorFKHip = getFKHip.replace(side , swapSide)
			getFKHipRotVal = mc.getAttr((mirrorFKHip + '.r'))
			getFKHipStrVal = mc.getAttr((mirrorFKHip + '.Stretch'))
		
			#FK Knee
			getFKKnee = mc.listConnections((switchCtrl + '.FKKnee'))[0]
			mirrorFKKnee = getFKKnee.replace(side , swapSide)
			getFKKneeRotVal = mc.getAttr((mirrorFKKnee + '.r'))
			getFKKneeStrVal = mc.getAttr((mirrorFKKnee + '.Stretch'))	
			
		 	#FK Ankle
			getFKAnkle = mc.listConnections((switchCtrl + '.FKAnkle'))[0]
			mirrorFKAnkle = getFKAnkle.replace(side , swapSide)
			getFKAnkleRotVal = mc.getAttr((mirrorFKAnkle + '.r'))
			
			#FK Toe
			getFKBall = mc.listConnections((switchCtrl + '.FKToe'))[0]
			mirrorFKBall = getFKBall.replace(side , swapSide)
			getFKBallRotVal = mc.getAttr((mirrorFKBall + '.r'))
			# For Bend Controls
			getBendControlVal = mc.getAttr((switchCtrl + '.BendControls'))
			if getBendControlVal:
			#Query Attributes
				getBendUp = mc.listConnections((switchCtrl + '.LegBendUp'))[0]	
				mirrorBendUp = getBendUp.replace(side , swapSide)
				getBendUpTransVal = mc.getAttr((mirrorBendUp + '.t'))
				getBendUpTwistUp = mc.getAttr((mirrorBendUp + '.UpTwist'))
				getBendUpTwistDn = mc.getAttr((mirrorBendUp + '.DnTwist'))
				getBendDn = mc.listConnections((switchCtrl + '.LegBendDn'))[0]	
				mirrorBendDn = getBendDn.replace(side , swapSide)
				getBendDnTransVal = mc.getAttr((mirrorBendDn + '.t'))
				getBendDnTwistUp = mc.getAttr((mirrorBendDn + '.UpTwist'))
				getBendDnTwistDn = mc.getAttr((mirrorBendDn + '.DnTwist'))
	
			ar_mirrorCtrls(switchCtrl)	
	
			if getIKFKVal == 0:
				#Set Attributes to the reverse Side
				mc.setAttr((getIKLeg + '.t'), -getIKLegTransVal[0][0] , getIKLegTransVal[0][1] ,getIKLegTransVal[0][2])
				mc.setAttr((getIKLeg + '.r'), getIKLegRotVal[0][0] , -getIKLegRotVal[0][1] ,-getIKLegRotVal[0][2])
				mc.setAttr((getIKLeg + '.AutoStretch'),getIKLegStrVal)
				mc.setAttr((getIKLeg + '.KneePos'),getIKLegKneePosVal)
				mc.setAttr((getIKLeg + '.FootRoll'),getIKLegFootRollVal)
				mc.setAttr((getIKLeg + '.RollAngle'),getIKLegFootAngleVal)
				mc.setAttr((getIKLeg + '.ToeRoll'),getIKLegToeRollVal)
				mc.setAttr((getIKLeg + '.FootLean'),-getIKLegFootLeanVal)
				mc.setAttr((getIKLeg + '.HeelPivot'),-getIKLegHeelPivotVal)
				mc.setAttr((getIKLeg + '.ToePivot'),getIKLegToePivotVal)
				mc.setAttr((getIKLeg + '.Twist'),-getIKLegTwistVal)
				mc.setAttr((getIKLeg + '.KneeControl'),getIKLegKneeControlVal)
				if getIKLegKneeControlVal:
					mc.setAttr((getIKKnee + '.t'), -getIKKneeTransVal[0][0] , getIKKneeTransVal[0][1] ,getIKKneeTransVal[0][2])
					mc.setAttr((getIKKnee + '.KneeLock'),getIKKneeLockVal)
			
			if getIKFKVal == 1:
				mc.setAttr((getFKHip + '.r'), getFKHipRotVal[0][0] , getFKHipRotVal[0][1] ,getFKHipRotVal[0][2])
				mc.setAttr((getFKHip + '.Stretch'),getFKHipStrVal)
				mc.setAttr((getFKKnee + '.r'), getFKKneeRotVal[0][0] , getFKKneeRotVal[0][1] ,getFKKneeRotVal[0][2])
				mc.setAttr((getFKKnee + '.Stretch'),getFKKneeStrVal)
				mc.setAttr((getFKAnkle + '.r'), getFKAnkleRotVal[0][0] , getFKAnkleRotVal[0][1] ,getFKAnkleRotVal[0][2])
				mc.setAttr((getFKBall + '.r'), getFKBallRotVal[0][0] , getFKBallRotVal[0][1] ,getFKBallRotVal[0][2])
			#Set Bend Attributes
			if getBendControlVal:
				mc.setAttr((getBendUp + '.t'), -getBendUpTransVal[0][0] , -getBendUpTransVal[0][1] ,-getBendUpTransVal[0][2])
				mc.setAttr((getBendUp + '.UpTwist'),getBendUpTwistUp)
				mc.setAttr((getBendUp + '.DnTwist'),getBendUpTwistDn)
				mc.setAttr((getBendDn + '.t'), -getBendDnTransVal[0][0] , -getBendDnTransVal[0][1] ,-getBendDnTransVal[0][2])
				mc.setAttr((getBendDn + '.UpTwist'),getBendDnTwistUp)
				mc.setAttr((getBendDn + '.DnTwist'),getBendDnTwistDn)
		#----------------------------------------------------------------------------------------------------------#			
		#Spine
		if 'Ctrl_Body' in switchCtrl:
			getBody = mc.listConnections((switchCtrl + '.Spine_RCDriver'))[0]
			getHip = mc.listConnections((switchCtrl + '.Hip'))[0]
			getSpine1 = mc.listConnections((switchCtrl + '.FKSpine1'))[0]
			getSpine2 = mc.listConnections((switchCtrl + '.FKSpine2'))[0]
			getTorso = mc.listConnections((switchCtrl + '.Torso'))[0]
			getShoulder = mc.listConnections((switchCtrl + '.Shoulder'))[0]
			allSpines = [getBody , getHip , getSpine1 ,getSpine2 , getTorso , getShoulder]
			for i in range (len(allSpines)):
				getRotSpine = mc.getAttr(allSpines[i] + '.r')
				mc.setAttr((allSpines[i] + '.r'),getRotSpine[0][0] , -getRotSpine[0][1] , -getRotSpine[0][2])
				if i == 0 or i == 1 or i == 4:
					getTrans = mc.getAttr(allSpines[i] + '.t')
					mc.setAttr((allSpines[i] + '.t'), -getTrans[0][0] , getTrans[0][1] ,getTrans[0][2])
	
		#----------------------------------------------------------------------------------------------------------#			
		#Head
		if mc.attributeQuery('Head_RCDriver',node = switchCtrl,ex=1):
			getHead = mc.listConnections((switchCtrl + '.Head'))[0]
			getNeck = mc.listConnections((switchCtrl + '.Neck'))[0]
			
			getNeckRot = mc.getAttr((getNeck + '.r'))
			getHeadTrans = mc.getAttr(getHead + '.t')
			getHeadRot = mc.getAttr(getHead + '.r')
			
			mc.setAttr((getNeck + '.r'),getNeckRot[0][0] , -getNeckRot[0][1] , -getNeckRot[0][2])
			mc.setAttr((getHead + '.t'), -getHeadTrans[0][0] , getHeadTrans[0][1] ,getHeadTrans[0][2])
			mc.setAttr((getHead + '.r'), getHeadRot[0][0] , -getHeadRot[0][1] ,-getHeadRot[0][2])
	except (RuntimeError):
		pass
	mc.undoInfo( cck = True )	
			
#==============================================================================================================#

#Function for Snaping IK to FK and vice versa    (Revised.1)
def ar_snapIKFK(switchCtrl, key=False):
    mc.undoInfo( ock = True )
    try:
        getIKFKVal = mc.getAttr((switchCtrl + '.IKFK'))#Query IKFK Mode
        #Check for Arm Control
        if 'ArmIKFK' in switchCtrl:		    
            #Query FK and IK Control Attributes
            IKFKObj = mc.listConnections(switchCtrl + '.IKFKpos')[0]
            IKArmObj = mc.listConnections(switchCtrl + '.Arm')[0]
            IKElbowObj = mc.listConnections(switchCtrl + '.ElbowPole')[0]
            FKShoulderObj = mc.listConnections(switchCtrl + '.ShoulderFK')[0]
            FKElbowObj = mc.listConnections(switchCtrl + '.ElbowFK')[0]
            FKWristObj = mc.listConnections(switchCtrl + '.WristFK')[0]
            snapIKElbowObj = mc.listConnections(switchCtrl + '.IKElbowSnap')[0]
            IKShoulderJnt = mc.listConnections(switchCtrl + '.ShoulderJnt')[0]
            IKElbJnt = mc.listConnections(switchCtrl + '.ElbowJnt')[0]
            IKWristJnt = mc.listConnections(switchCtrl + '.WristJnt')[0]
            gimbalObj = mc.listConnections(switchCtrl + '.HandGimbal')[0]
            #clavicleObj = mc.listConnections(switchCtrl + '.Clavicle')[0]
            handObj = mc.listConnections(switchCtrl + '.Hand')[0]
            armBendUpObj = mc.listConnections(switchCtrl + '.ArmBendUp')[0]
            armBendDnObj = mc.listConnections(switchCtrl + '.ArmBendDn')[0]

            if getIKFKVal == 0: # If Mode is IK
                preIKFK, curIKFK, preKeyObjs, curKeyObjs  =  0, 1, [IKArmObj, IKElbowObj], [FKShoulderObj, FKElbowObj, FKWristObj]  
                shlrVal = mc.xform(IKShoulderJnt ,r = 1 , q = 1 , ws = 1 , ro = 1)
                elbval = mc.xform(IKElbJnt , r = 1 , q = 1 , ws = 1 , ro = 1)
                wrstval = mc.xform(IKWristJnt , r = 1 , q = 1 , ws = 1 , ro = 1)
				
                #Setting IK Joint position to FK controls
                mc.xform(FKShoulderObj , ws = 1 , ro = [shlrVal[0] , shlrVal[1] ,shlrVal[2]])
                mc.xform(FKElbowObj , ws = 1 , ro = [elbval[0] , elbval[1] ,elbval[2]])
                mc.xform(FKWristObj , ws = 1 , ro = [wrstval[0] , wrstval[1] ,wrstval[2]])
				
                mc.setAttr((switchCtrl + '.IKFK') , 1)#Set Mode to FK
            else:#Mode is FK
                preIKFK, curIKFK, preKeyObjs, curKeyObjs = 1, 0, [FKShoulderObj, FKElbowObj, FKWristObj], [IKArmObj, IKElbowObj]
                IKHandTransVal = mc.xform(FKWristObj , q = 1 , r = 1 , ws = 1 , rp = 1)
                IKHandRotVal = mc.xform(FKWristObj , q = 1 , r = 1, ws = 1 , ro = 1)
                IKElbwTransVal = mc.xform(snapIKElbowObj , r = 1 ,q = 1 , ws = 1 , rp = 1)
                IKElbwRotVal = mc.xform(snapIKElbowObj , q = 1 , r = 1 , ws = 1 , ro = 1)
                #Setting FK's Position to IK Control
                mc.xform(IKArmObj ,a = 1 , ws = 1 , t = [IKHandTransVal[0] , IKHandTransVal[1] ,IKHandTransVal[2]])
                mc.xform(IKArmObj ,a = 1 , ws = 1 , ro = [IKHandRotVal[0] , IKHandRotVal[1] ,IKHandRotVal[2]])
                mc.xform(IKElbowObj ,a = 1 , ws = 1 , t = [IKElbwTransVal[0] , IKElbwTransVal[1] ,IKElbwTransVal[2]])
                
                mc.setAttr((switchCtrl + '.IKFK') , 0)#Set Mode to IK

		    		
	    #----------------------------------------------------------------------------------------------------------#	
	    #Check for Leg Control		
    	if 'LegIKFK' in switchCtrl:
    	    #Query FK and IK Control Attributes
    	    IKFKObj = mc.listConnections(switchCtrl + '.IKFKpos')[0]
    	    IKLegObj = mc.listConnections(switchCtrl + '.Foot')[0]
    	    IKKneeObj = mc.listConnections(switchCtrl + '.Knee')[0]
    	    FKHipObj = mc.listConnections(switchCtrl + '.FKLeg')[0]
    	    FKKneeObj = mc.listConnections(switchCtrl + '.FKKnee')[0]
    	    FKAnkleObj = mc.listConnections(switchCtrl + '.FKAnkle')[0]
    	    FKToeObj = mc.listConnections(switchCtrl + '.FKToe')[0]
    	    snapIKLegObj = mc.listConnections(switchCtrl + '.IKLegSnap')[0]
    	    IKHiprJnt = mc.listConnections(switchCtrl + '.UpLegJnt')[0]
    	    IKKneeJnt = mc.listConnections(switchCtrl + '.KneeJnt')[0]
    	    IKAnkleJnt = mc.listConnections(switchCtrl + '.AnkleJnt')[0]
	    
    	    if getIKFKVal == 0:#Mode is IK
    	        preIKFK, curIKFK, preKeyObjs, curKeyObjs  =  0, 1, [IKLegObj, IKKneeObj], [FKHipObj, FKKneeObj, FKAnkleObj, FKToeObj]
    	        #Query IK Controls Positon
    	        hipVal = mc.xform(IKHiprJnt ,r = 1 , q = 1 , ws = 1 , ro = 1)
    	        kneeval = mc.xform(IKKneeJnt , r = 1 , q = 1 , ws = 1 , ro = 1)
    	        ankleval = mc.xform(IKAnkleJnt , r = 1 , q = 1 , ws = 1 , ro = 1)
    	        
    	        #Setting IK's Position to FK Control
    	        mc.xform(FKHipObj , ws = 1 , ro = [hipVal[0] , hipVal[1] ,hipVal[2]])
    	        mc.xform(FKKneeObj , ws = 1 , ro = [kneeval[0] , kneeval[1] ,kneeval[2]])
    	        mc.xform(FKAnkleObj , ws = 1 , ro = [ankleval[0] , ankleval[1] ,ankleval[2]])
    	        
    	        mc.setAttr((switchCtrl + '.IKFK') , 1)#Set Mode to FK	
            else:#Mode is FK
                preIKFK, curIKFK, preKeyObjs, curKeyObjs  =  1, 0, [FKHipObj, FKKneeObj, FKAnkleObj, FKToeObj], [IKLegObj, IKKneeObj]
                #Query IK Controls Positon
                IKLegTransVal = mc.xform(snapIKLegObj , q = 1 , r = 1 , ws = 1 , rp = 1)
                IKLegRotVal = mc.xform(snapIKLegObj , q = 1 , r = 1, ws = 1 , ro = 1)	
                #Setting FK's Position to IK Control
                mc.xform(IKLegObj ,a = 1 , ws = 1 , t = [IKLegTransVal[0] , IKLegTransVal[1] ,IKLegTransVal[2]])
                mc.xform(IKLegObj ,a = 1 , ws = 1 , ro = [IKLegRotVal[0] , IKLegRotVal[1] ,IKLegRotVal[2]])
                
                mc.setAttr((switchCtrl + '.IKFK') , 0)#Set Mode to IK
        if key:
            curFrm = mc.currentTime(q=1)
            preFrm = mc.currentTime(q=1) - 1
            mc.setKeyframe( preKeyObjs, t=preFrm )
            mc.setKeyframe( curKeyObjs, t=curFrm )
            mc.setKeyframe( IKFKObj, t=preFrm, v=preIKFK, ott='step' )
            mc.setKeyframe( IKFKObj, t=curFrm, v=curIKFK, ott='step' )                
                
    except (RuntimeError , TypeError):
        pass
    mc.undoInfo( cck = True )

#==============================================================================================================#

#Function for Reseting Attributes to default Values
def ar_resetAttr(switchCtrl,mode = 0):
	mc.undoInfo( ock = True )
	if mode == 0:
		attrB = mc.listAttr(switchCtrl,k =1)
		nonKeyAttrb = mc.listAttr(switchCtrl,cb = 1,u =1)
		if nonKeyAttrb != None: attrB.extend(nonKeyAttrb)
		for each in attrB:
		 defAttr = mc.attributeQuery(each,n = switchCtrl,ld=True)
		 mc.setAttr(switchCtrl + '.%s' % each,defAttr[0])

	if mode == 1:
		if mc.objExists (switchCtrl + ".IKFKpos"):
			drvAttr = 'IKFKpos'
		elif mc.objExists (switchCtrl + ".Spine_RCDriver"):
			drvAttr = 'Spine_RCDriver'
		elif mc.objExists (switchCtrl + ".Head_RCDriver"):
			drvAttr = 'Head_RCDriver'
		elif mc.objExists (switchCtrl + ".FingerPos"):
			drvAttr = 'FingerPos'			
		
		getDriver = mc.listConnections((switchCtrl+'.%s'%drvAttr))[0]
		getCntrls = mc.listConnections(getDriver + '.message')
		for cntrl in getCntrls:
			ar_resetAttr(cntrl , 0)
	mc.undoInfo( cck = True)
	
#==============================================================================================================#

#Function for Changing the Parents with out  No movements
def ar_setDynParent(setVal , cntrl):
	mc.undoInfo( ock = True )
	isTran = mc.getAttr((cntrl + '.t') ,  se = 1)
	isRot = mc.getAttr((cntrl + '.r') ,  se = 1)
	
	getTransVal = mc.xform(cntrl , q = 1 , r = 1 , ws = 1 , rp = 1)
	getRotVal = mc.xform(cntrl , q = 1 , r = 1, ws = 1 , ro = 1)

	parAttr = 'Parent'
	if mc.objExists (cntrl + ".ParentBlend"):
		getPB = mc.getAttr(cntrl + ".ParentBlend")	
		parAttr = 'Parent%d' % getPB
	mc.setAttr((cntrl + '.%s' % parAttr) , setVal)
	
	if isTran and isRot :
		mc.xform(cntrl ,a = 1 , ws = 1 , t = [getTransVal[0] , getTransVal[1] ,getTransVal[2]])
		mc.xform(cntrl ,a = 1 , ws = 1 , ro = [getRotVal[0] , getRotVal[1] ,getRotVal[2]])
	elif isTran:
		mc.xform(cntrl ,a = 1 , ws = 1 , t = [getTransVal[0] , getTransVal[1] ,getTransVal[2]])
	else:
		mc.xform(cntrl ,a = 1 , ws = 1 , ro = [getRotVal[0] , getRotVal[1] ,getRotVal[2]])
	mc.undoInfo( cck = True)
	
#==============================================================================================================#

#Function for Enabling Elbow and Knee Locks
def ar_ElKnLock(switchCtrl):
	mc.undoInfo( ock = True )
	if 'ArmIKFK' in switchCtrl:		
		IKElbowObj = mc.listConnections(switchCtrl + '.ElbowPole')[0]
		IKElbJnt = mc.listConnections(switchCtrl + '.ElbowJnt')[0]
		if mc.getAttr(IKElbowObj + ".ElbowLock") == 0:
			elbval = mc.xform(IKElbJnt , r = 1 , q = 1 , ws = 1 , rp = 1)
			mc.xform(IKElbowObj ,a = 1 , ws = 1 , t = [elbval[0] , elbval[1] ,elbval[2]])
			mc.setAttr(IKElbowObj + ".ElbowLock" , 1)
		else:
			mc.setAttr(IKElbowObj + ".ElbowLock" , 0)
	#----------------------------------------------------------------------------------------------------------#	
	if 'LegIKFK' in switchCtrl:
		IKKnee = mc.listConnections(switchCtrl + '.Knee')[0]
		IKKneeJnt = mc.listConnections(switchCtrl + '.KneeJnt')[0]
		if mc.getAttr(IKKnee + ".KneeLock") == 0:
			kneeVal = mc.xform(IKKneeJnt , r = 1 , q = 1 , ws = 1 , rp = 1)
			mc.xform(IKKnee ,a = 1 , ws = 1 , t = [kneeVal[0] , kneeVal[1] ,kneeVal[2]])
			mc.setAttr(IKKnee + ".KneeLock" , 1)
		else:
			mc.setAttr(IKKnee + ".KneeLock" , 0)
	mc.undoInfo( cck = True )
		
#**************************************************END**************************************************#