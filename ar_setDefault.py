											#-----------------------------------------------------------------------------#
											# 	DESCRIPTION	: Main Python for Setting Default Values of Custom Attributes #	 																		   
											# 	AUTHOR 			: Arun . S - arunpillaii@gmail.com             								#                    												                       				                     
											# 	VERSION			: 1.00 , 26 November 2009                      								#
											#   Copyright (C) 2009.  All rights reserved.									 								#
											#-----------------------------------------------------------------------------#
#Imports
import maya.cmds as mc
import maya.OpenMaya as om

def ar_setDefault(objects = None):
	sel = objects if objects else mc.ls(sl=1)
	for ctrl in sel:
		attrB = []
		attrbKey = mc.listAttr(ctrl,k = 1,ud=1)
		attrNonKey = mc.listAttr(ctrl,cb = 1,ud=1,u =1)
		if attrbKey != None:attrB.extend(attrbKey)
		if attrNonKey != None:attrB.extend(attrNonKey)
		if len(attrB):
			for each in attrB:
				curAttr = mc.getAttr(ctrl + '.%s' % each)
				mc.addAttr((ctrl +'.%s'%each) ,e=1, dv=curAttr)
			om.MGlobal.displayInfo('The Current Values of %s are Set as Defaults!!' % ctrl)
			
#**************************************************END**************************************************#

