											#--------------------------------------------------------------#
											# 	DESCRIPTION	: Python Module for Creating a								 #
											#                  Default Template for Skeleton Creation			 #	 																		   
											# 	AUTHOR 			: Arun . S - arunpillaii@gmail.com             #                    												                       				                     
											# 	VERSION			: 1.00 , 17 November 2009                      #
											#   Copyright (C) 2009.  All rights reserved.									 #
											#--------------------------------------------------------------#
#imports!
import maya.cmds as mc
import ar_rigTools as tools

#Details = [character Name , Artist Name]
#Mirror = (On/Off)
#Fingers = (0-5)

def ar_Template(Details=['Test','Asd'] , Mirror=1 , Fingers=5 ):
	
	#Creating template groups
	if(mc.objExists('Grp_Template')):
		mc.delete('Grp_Template')
	grpRefObjs = mc.group(name = 'Grp_Template', empty = True)
	grpOthers = mc.group(name = 'Grp_Others', empty = True, p = grpRefObjs)
	
	#Spine Objects name and position
	SpGrps = [('Root_Tmpl',grpRefObjs), ('LowSpine_Tmpl','Root_Tmpl'),( 'MidSpine_Tmpl','LowSpine_Tmpl'),('UpSpine_Tmpl' ,'MidSpine_Tmpl'),	('Ribcage_Tmpl' , 'UpSpine_Tmpl'),('Neck_Tmpl' , 'Ribcage_Tmpl'),('Head_Tmpl', 'Neck_Tmpl'),('HeadEnd_Tmpl','Head_Tmpl'),	('JawStart_Tmpl','Head_Tmpl'),('JawEnd_Tmpl','JawStart_Tmpl'),('LeftEye_Tmpl','Head_Tmpl'),('RightEye_Tmpl','Head_Tmpl')]
	SpVals = [[0,3.1176,0.016], [0,3.3579,0.0258], [0,3.6226,0.0409], [0,3.8764,0.0406], [0,4.1842,0.0104], [0,4.9728,-0.0624], [0,5.1848,-0.0308], [0,6,0.0292], [0,5.2232,0.0748], [0,5.0468,0.3348], [0.1116,5.5284,0.2828], [-0.1116,5.5284,0.2828]]
	for i in range(len(SpGrps)):
		#spine template creation
		tools.rendbox(SpGrps[i][0] , SpVals[i][0] , SpVals[i][1],SpVals[i][2],SpGrps[i][1])
	
	#Legs and Arms name ,position and creation
	LegGrps = [('UpLeg_Tmpl','Root_Tmpl'),( 'Knee_Tmpl','UpLeg_Tmpl'),('Ankle_Tmpl','Knee_Tmpl'),('Ball_Tmpl','Ankle_Tmpl'),('Toe_Tmpl','Ball_Tmpl'),('Heel_Tmpl','Ankle_Tmpl'),('HeelExt_Tmpl','Ball_Tmpl'),('HeelInt_Tmpl','Ball_Tmpl')]
	LegVals = [[0.2816,2.9268,-0.0012], [0.2816,1.596,-0.0012], [0.2816,0.294,-0.0012], [0.2816,0.0804,0.4008], [0.2816,0.086,0.7308], [0.2816,0,-0.1284], [0.3812,0,0.4124], [0.1808,0,0.4124,0.05]]
	ArmGrps = [('Clavicle_Tmpl','Ribcage_Tmpl') , ('Shoulder_Tmpl','Clavicle_Tmpl') , ('Elbow_Tmpl','Shoulder_Tmpl') , ('Wrist_Tmpl','Elbow_Tmpl')]
	ArmVals = [(0.339,4.607,-0.089),(0.572,4.73,-0.089),(1.557,4.73,-0.089),(2.377,4.73,-0.089)]
	Mult = 1.0 
	for side in ['Left', 'Right']:
		for i in range(len(LegGrps)):
			LegParent = (side + LegGrps[i][1])
			if i == 0 : LegParent = 'Root_Tmpl'
			tools.rendbox((side + LegGrps[i][0]), (Mult * LegVals[i][0]), LegVals[i][1], LegVals[i][2], LegParent)
		for i in range(len(ArmGrps)):
			ArmParent = (side + ArmGrps[i][1])
			if i == 0 : ArmParent = 'Ribcage_Tmpl'
			tools.rendbox((side + ArmGrps[i][0]), (Mult * ArmVals[i][0]), ArmVals[i][1], ArmVals[i][2],ArmParent)

		#Fingers name and postion of template
		if Fingers:
			fingVal =[[[2.545,4.73,0.0],[2.723,4.73,0.0],[2.823,4.73,0.0],[2.923,4.73,0.0],[3.023,4.73,0.0]],
			[[2.48,4.73,-0.089],[2.741 ,4.73,-0.089],[2.841,4.73,-0.089],[2.941,4.73,-0.089],[3.041,4.73,-0.089]],
			[[2.475,4.73,-0.187],[2.714,4.73,-0.187],[2.814,4.73,-0.187],[2.914,4.73,-0.187],[3.014,4.73,-0.187]],
			[[2.511,4.73,-0.260],[2.672,4.73,-0.262],[2.772,4.73,-0.262],[2.872,4.73,-0.262],[2.972,4.73,-0.262]],
			[[2.461,4.73,0.024],[2.554,4.73,0.107],[2.645,4.73,0.207],[2.701,4.73,0.314]]]
			fingNames = ['Index','Middle','Ring','Pinky','Thumb']
			for i in range(Fingers):
				fingParent = (side + ArmGrps[3][0])
				fingCurObjs = [fingParent]
#				for j in range(1,6):
				for j in range(len(fingVal[i])):
					tools.rendbox((side + fingNames[i] + str(j) + '_Tmpl'), (Mult * fingVal[i][j][0]), fingVal[i][j][1], fingVal[i][j][2],fingParent)
					fingParent = (side + fingNames[i] + str(j) + '_Tmpl')
					fingCurObjs.append(fingParent)
				tools.crvfromobjs(fingCurObjs)
		
	#creating curves between templates of spine , legs and arms
		tools.crvfromobjs([SpGrps[4][0]] + [(side + each[0]) for each in ArmGrps])
		tools.crvfromobjs([SpGrps[0][0]] + [(side + each[0]) for each in LegGrps[:5]])
		tools.crvfromobjs([(side + LegGrps[2][0]),(side + LegGrps[5][0])])
		tools.crvfromobjs([(side + LegGrps[6][0]),(side + LegGrps[3][0]),(side + LegGrps[7][0])])
		Mult = -1.0
	curSpineObjs = [each[0] for each in SpGrps]
	curveObjts = (curSpineObjs[:8],[curSpineObjs[6],curSpineObjs[8],curSpineObjs[9]],[curSpineObjs[6],curSpineObjs[10]],[curSpineObjs[6],curSpineObjs[11]])
	for obj in curveObjts:
		tools.crvfromobjs(obj)
	
	#Connecting Left Template to Right
	if Mirror:
		leftobjs = mc.ls('Left*_Tmpl')
		for obj in leftobjs:
			rightObj = obj.replace('Left' , 'Right')
			mc.connectAttr((obj + '.ty'),(rightObj + '.ty'))
			mc.connectAttr((obj + '.tz'),(rightObj + '.tz'))
			mc.connectAttr((obj + '.rx'),(rightObj + '.rx'))
			mc.connectAttr((obj + '.scale'),(rightObj + '.scale'))
			mc.connectAttr((obj + 'Shape.size'),(rightObj + 'Shape.size'))
			reverseMD = mc.createNode('multiplyDivide')
			mc.setAttr((reverseMD + '.input2'), -1 , -1 , -1)
			mc.connectAttr((obj + '.tx'),(reverseMD + '.input1X'))
			mc.connectAttr((obj + '.ry'),(reverseMD + '.input1Y'))
			mc.connectAttr((obj + '.rz'),(reverseMD + '.input1Z'))
			mc.connectAttr((reverseMD + '.outputX'),(rightObj + '.tx'))
			mc.connectAttr((reverseMD + '.outputY'),(rightObj + '.ry'))
			mc.connectAttr((reverseMD + '.outputZ'),(rightObj + '.rz'))
			mc.setAttr((rightObj + '.overrideEnabled'),1)
			mc.setAttr((rightObj + '.overrideDisplayType'),2)
	mc.addAttr('Grp_Template' , ln = 'CharacterName' , dt = 'string')
	mc.setAttr('Grp_Template.CharacterName' , Details[0],type = 'string')
	mc.addAttr('Grp_Template' , ln = 'TemplateBy' , dt = 'string')
	mc.setAttr('Grp_Template.TemplateBy' , Details[1],type = 'string')
	mc.select(cl = True)

	#Fit all abjects in scene
	mc.viewFit( all=True )

#**************************************************END**************************************************#
