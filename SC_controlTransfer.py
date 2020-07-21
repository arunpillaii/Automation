											#--------------------------------------------------------------#
											# 	DESCRIPTION	: Transfering curves vertex position			     #	 																		   
											# 	AUTHOR 			: Arun.S								            					 # 
											# 	VERSION			: 1.00 , 10 November 2009                      #
											#		MODIFIED		:	12 February 2010														 #
											#   Copyright (C) 2009.  All rights reserved.									 #
											#--------------------------------------------------------------#
#Imports!!
import maya.cmds as mc
import maya.OpenMaya as om
import re

#Procedure Interface
def SC_controlTransfer():
	contTrans = 'contTrans'
	if mc.window (contTrans, exists =1): mc.deleteUI (contTrans)
	if mc.windowPref (contTrans, exists = 1): mc.windowPref (contTrans, remove = 1)
		
	mc.window (contTrans,w =125,h =170,t ="ControlTransfer", titleBar= 1, mnb= 0, mxb= 0,mb= 0, tlb =1,sizeable =0)
	mc.columnLayout()
	mc.separator (h = 10,w =115,hr= 1,st= "none")
	mc.button (w= 115, h =40,l ="SaveControl",align= "center",c =lambda event:(mc.fileBrowserDialog (m =1,fc= savePose,ft ='.txt' ,an= 'Write_Controls')))
	mc.separator (h = 10,w =115,hr= 1,st= "none")
	mc.radioButtonGrp('rbgrpmode',numberOfRadioButtons= 2, cw3 =[10,40,60],sl =1,label ="",labelArray2 =["All","Select"])
	mc.separator (h =20,w =115, hr =1,st ="double")
	mc.button (w =115,h =40,l ="ReadControl",align= "center",c =lambda event:(mc.fileBrowserDialog (m =0,fc= readPose,ft ='.txt' ,an= 'Read_Controls')))
	mc.showWindow (contTrans)

#Procedure for Saving Control Position
def savePose(filename,ext):
	mode= mc.radioButtonGrp ('rbgrpmode',q=1,sl=1)
	if mode==1: 
		sel = mc.ls('Ctrl_*',type = "nurbsCurve")
	else: 
		sele=mc.ls(sl=1)
		sel=[]
		for each in sele:
			getShapes=mc.listRelatives(each,s=1,type='nurbsCurve')
			sel += getShapes
	control= []
	for n in range(0,len(sel)):
		spans  = mc.getAttr(sel[n]+'.spans')
		degree = mc.getAttr(sel[n]+'.degree')
		form   = mc.getAttr(sel[n]+'.form')
		
		if form == 0: clu = spans+degree
		else : clu = spans
			
		for i in range(0,clu,1):
			pos = mc.xform(sel[n]+'.cv['+str(i)+']',q=1,t=1)
			control.append( (sel[n] + ".cv[" + str(i) + "]")+ "\n" +str(pos[0]) + ',' + str(pos[1]) +',' + str(pos[2]) )
	
	fileid = open(filename, 'w')	
	for j in range(0,len(control),1):
		fileid.write(control[j]+'\n')
	fileid.close()
	om.MGlobal.displayInfo('The Controls Positions are Successfully Exported.......')
	
#Procedure for Reading Control Position
def readPose(filename,ext=None):
	mc.undoInfo( ock = True )
	fileid = open(filename, 'r')
	numline = (len(fileid.readlines()))/2
	fileid.seek(0)
	for i in range(0,numline,1):
		obj = fileid.readline()
		pos = fileid.readline()	
		pos = re.split('[,]+',pos)
		for j in range(0,3,1):
			pos[j] = float(pos[j])
		if mc.objExists(obj.split('.')[0]):
			mc.xform(obj,t=[pos[0],pos[1],pos[2]])
	fileid.close()
	om.MGlobal.displayInfo('The Controls Positions are Successfully Imported.......')
	mc.undoInfo(cck = True )
	
#**************************************************END**************************************************#