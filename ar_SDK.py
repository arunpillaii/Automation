											#--------------------------------------------------------------#
											# 	DESCRIPTION	: Module For SetDrivenKey									     #	 																		   
											#                 This will return SDK Node Name							 #
											# 	AUTHOR 			: Arun . S - arunpillaii@gmail.com             #                    												                       				                     
											# 	VERSION			: 1.00 , 15 Decembero 2009                     #
											#   Copyright (C) 2009.  All rights reserved.									 #
											#--------------------------------------------------------------#

import maya.cmds as mc
import sets
def ar_SDK(driver , driven  , drVals , dnVals):
	
	if not mc.listConnections(driven):#Nothing is Connected
		for i in range(len(drVals)):
			mc.setDrivenKeyframe(driven , cd = driver , dv = drVals[i] ,  v = dnVals[i] ,ib = True)
		getSDKnode = mc.listConnections(driven)
		return getSDKnode
	
	if mc.listConnections(driven,t='animCurveUA',scn=1) or mc.listConnections(driven,t='animCurveUL',scn=1) or mc.listConnections(driven,t='animCurveUU',scn=1):
		getOldSDK = mc.listConnections(driven,scn=1)
		for i in range(len(drVals)):
			mc.setDrivenKeyframe(driven , cd = driver , dv = drVals[i] ,  v = dnVals[i] ,ib = True)
		getBlendNode = mc.listConnections(driven , t = 'blendWeighted',scn=1)
		getSDKBlend = mc.listConnections(getBlendNode[0] + '.input',scn=1)
		getSDKnode = list(set(getSDKBlend).difference(set(getOldSDK)))
		return getSDKnode		
	
	if mc.listConnections(driven,t='blendWeighted',scn=1):
		getBlendNode = mc.listConnections(driven,scn=1)
		getOldSDKBlend = mc.listConnections(getBlendNode[0] + '.input',scn=1)
		for i in range(len(drVals)):
			mc.setDrivenKeyframe(driven , cd = driver , dv = drVals[i] ,  v = dnVals[i] ,ib = True)
		getSDKBlend = mc.listConnections(getBlendNode[0] + '.input',scn=1)
		getSDKnode = list(set(getSDKBlend).difference(set(getOldSDKBlend)))
		return getSDKnode
	

	
