											#--------------------------------------------------------------#
											# 	DESCRIPTION	: Python Module for Creating Skeleton 				 #
											#									from Template	 															 #	 																		   
											# 	AUTHOR 			: Arun . S - arunpillaii@gmail.com             #                    												                       				                     
											# 	VERSION			: 1.00 , 17 November 2009                      #
											#   Copyright (C) 2009.  All rights reserved.									 #
											#--------------------------------------------------------------#

#imports!!
import maya.cmds as mc
import maya.OpenMaya as om
import ar_rigTools as tools

def ar_createSkeleton(Details , SpineJnts , BackUpTemOnOff):
	
	if not (mc.objExists('Root_Tmpl') or mc.objExists('Grp_Template')):
		om.MGlobal.displayError("Template Objects Need to create Skeleton is not Found!!!")
	else:
		# BAckUp Template
		if BackUpTemOnOff:
			path = mc.file(q = 1 , loc = 1)
			if path == 'unknown':
				mc.confirmDialog( title='Error', message='Current File is Not Exists or Not Saved !!', button=['OK'])
				return None
			else:
				fileDiretory = path.rsplit('/',1)[0]
				if mc.file((fileDiretory  + '/%s_RigTemplate.mb' % Details[0]) , q = True , ex = True):
					CF = mc.confirmDialog( title='File Exists', message='Template File Already Exists.Do You Want to Replace it?', button=['Yes','No'], defaultButton='Yes', cancelButton= 'No', dismissString='No' )
					if CF == 'No':
						return None
			mc.select('Grp_Template')
			mc.file((fileDiretory  + '/%s_RigTemplate.mb' % Details[0]) , type = "mayaBinary" , es = True)
			mc.select(cl = 1)
		
		#----------------------------------------SPINE----------------------------------------#
		
		objects = ['Root_Tmpl' , 'LowSpine_Tmpl' , 'MidSpine_Tmpl' , 'UpSpine_Tmpl' , 'Ribcage_Tmpl']
		spineJnts = tools.ar_jointsAlongCurve(objects , 'Spine' , SpineJnts)	
		rootJnt = mc.rename(spineJnts[0] , 'Root_CJ')	
		spineJnts[0] = rootJnt
		spineJnts.append(tools.ar_jointsAlongObjects(['Neck_Tmpl'] , 1 , 0)[0])
		mc.parent(spineJnts[len(spineJnts)-1] , spineJnts[len(spineJnts) - 2])
		
		#----------------------------------------LEGS----------------------------------------#
		# LeftLeg
		objects = ['LeftUpLeg_Tmpl' , 'LeftKnee_Tmpl' , 'LeftAnkle_Tmpl' , 'LeftBall_Tmpl', 'LeftToe_Tmpl']
		gety = mc.getAttr('LeftUpLeg_Tmpl.ry')
		mc.setAttr('LeftUpLeg_Tmpl.ry' , 0)
		LeftLegJnts = tools.ar_jointsAlongObjects(objects,0)
		mc.setAttr(LeftLegJnts[3] + '.jointOrientX' , 0 )
		tools.jnt_orient(LeftLegJnts,'x','z','z')
		
		objects = ['LeftHeelExt_Tmpl' , 'LeftHeelInt_Tmpl' , 'LeftHeel_Tmpl']
		LeftLegPvts = tools.ar_jointsAlongObjects(objects , 0 , 0, 1)
		mc.setAttr(LeftLegJnts[0] + '.jointOrientX', (gety*-1))
		mc.setAttr('LeftUpLeg_Tmpl.ry' , gety)
		mc.parent(LeftLegJnts[0] , spineJnts[0])
		tools.jnt_orient(LeftLegJnts[3:5],'x','z','y')
		
		# RightLeg
		objects = ['RightUpLeg_Tmpl' , 'RightKnee_Tmpl' , 'RightAnkle_Tmpl' , 'RightBall_Tmpl', 'RightToe_Tmpl']
		gety = mc.getAttr('RightUpLeg_Tmpl.ry')
		mc.setAttr('LeftUpLeg_Tmpl.ry' , 0)
		RightLegJnts = tools.ar_jointsAlongObjects(objects,0)
		mc.setAttr(RightLegJnts[3] + '.jointOrientX' , 0 )
		tools.jnt_orient(RightLegJnts,'-x','z','-z')
		
		objects = ['RightHeelExt_Tmpl' , 'RightHeelInt_Tmpl' , 'RightHeel_Tmpl']
		RightLegPvts = tools.ar_jointsAlongObjects(objects , 0 , 0, 1)
		mc.setAttr(RightLegJnts[0] + '.jointOrientX', (mc.getAttr(RightLegJnts[0] + '.jointOrientX') -(gety*-1)))
		mc.parent(RightLegJnts[0] , spineJnts[0])
		tools.jnt_orient(RightLegJnts[3:5],'-x','-z','y')
			
		#----------------------------------------ARMS----------------------------------------#
		
		objects = ['LeftClavicle_Tmpl' , 'LeftShoulder_Tmpl' , 'LeftElbow_Tmpl' , 'LeftWrist_Tmpl']
		LeftArmJnts = tools.ar_jointsAlongObjects(objects)
		tools.jnt_orient(LeftArmJnts,'x','z','z')
		getFingers = mc.listRelatives(objects[3], c = 1, ad = 1 , type = 'transform')
		getFingers.sort()
		fingers = tools.ar_jointsAlongObjects(getFingers , 1 , 0 , 1)
		mc.parent(LeftArmJnts[0] , spineJnts[len(spineJnts) - 2])
		tools.jnt_orient(fingers,'x','z','z')
		
		objects = ['RightClavicle_Tmpl' , 'RightShoulder_Tmpl' , 'RightElbow_Tmpl' , 'RightWrist_Tmpl']
		RightArmJnts = tools.ar_jointsAlongObjects(objects)
		tools.jnt_orient(RightArmJnts,'-x','z','-z')
		getFingers = mc.listRelatives(objects[3], c = 1, ad = 1 , type = 'transform')
		getFingers.sort()
		fingers = tools.ar_jointsAlongObjects(getFingers , 1 , 0 , 1)
		mc.parent(RightArmJnts[0] , spineJnts[len(spineJnts) - 2])	
		tools.jnt_orient(fingers,'-x','z','-z')
		#----------------------------------------HEAD----------------------------------------#
		
		objects = ['Head_Tmpl' , 'HeadEnd_Tmpl' , 'JawStart_Tmpl' , 'JawEnd_Tmpl' , 'LeftEye_Tmpl' , 'RightEye_Tmpl']
		headJnts = tools.ar_jointsAlongObjects(objects , 1 , 0 , 1)
		tools.jnt_orient((headJnts+spineJnts),'x','z','z')
		
		#Delete TemplateGroup
		mc.addAttr(rootJnt , ln = 'CharacterName' , dt = 'string')
		mc.setAttr((rootJnt + '.CharacterName') , Details[0] , type = 'string', l = True)
		mc.addAttr(rootJnt , ln = 'SkeletonBy' , dt = 'string')
		mc.setAttr((rootJnt + '.SkeletonBy') , Details[1],type = 'string', l = True)
		mc.delete('Grp_Template')
		mc.select(cl = True)



#**************************************************END**************************************************#