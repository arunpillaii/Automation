											#--------------------------------------------------------------#
											# 	DESCRIPTION	: Python Module for Shape Editing(nurbsCurve)  #	 																		   
											# 	AUTHOR 			: Arun . S - arunpillaii@gmail.com         #                    												                       				                     
											# 	VERSION			: 1.00 , 20 November 2009                  #
											#   Copyright (C) 2009.  All rights reserved.				   #
											#--------------------------------------------------------------#
#imports!! 
import maya.cmds as mc

def ar_editShape(winReload = 0):
	
	# window exists check
	if mc.window('winEditShape',exists=1):mc.deleteUI('winEditShape' , window=1)
	if mc.windowPref('winEditShape' , exists=1) and winReload == 0:mc.windowPref('winEditShape' , remove=True)
	
	#Main window , Menu and layout Creation
	win = mc.window('winEditShape' , t="Control Editor" , menuBar=1 , s=0 , wh=(300,560))
	mc.menu(label="File")
	mc.menuItem(label="Refresh" , c =lambda event:ar_editShape(1))
	mc.menuItem(label="Close" , c="mc.deleteUI('winEditShape',window = 1)")
	
	#Main layout
	mc.columnLayout('maincolmlay_ES')
	mc.formLayout('formLay_ES')
	
	#Input Attributes for Translation
	mc.text('trans_TX' , l='[||||||||||||| TRANSLATION |||||||||||||] ' , w=300 , h=	24 , fn='boldLabelFont' , al='center')
	mc.radioButtonGrp('transSpace_RBG' , l=' Move Space -->>  ' , nrb=3 , sl=1 , cw4=[105,65,65,65] , la3=['World','Object','Local'])
	mc.floatSliderButtonGrp('transValue_FSBG' , label='Tran.Value' , f=1 , cw4=[65,35,158,50] , s=0.1 , bl='Rev' , bc=lambda :reverseFSBG("transValue_FSBG") , min=-100 , max=100 , v=0.25)
	mc.radioButtonGrp('transAxis_RBG' , l=' Axis -->>  ' , nrb=3 , sl=1 , cw4=[105,65,65,65] , la3=['X','Y','Z'])
	mc.button('trans_BT' , l='Translate' , bgc=[.6,.6,.6] , w=300 , c=lambda event:editShapeProc(0))
	mc.separator('sep_1' , w=300, style='double')
	
	#Input Attributes for Rotation
	mc.text('rot_TX' , l='[||||||||||||| ROTATION |||||||||||||] ' , w=300 ,h=24 , fn='boldLabelFont' , al='center')
	mc.radioButtonGrp('rotSpace_RBG' , l=' Rotate Space -->>  ',nrb=2 , sl=1 , cw3=[140,65,65] , la2=['World','Object'])
	mc.floatSliderButtonGrp('rotValue_FSBG' , label='Rot.Value' , f=1 , cw4=[65,35,158,50] , s=0.1 , bl='Rev' , bc=lambda :reverseFSBG("rotValue_FSBG") , min=-360 , max=360 , v=90)
	mc.radioButtonGrp('rotPivot_RBG' , l=' Pivot Position -->>  ',nrb=2 , sl=1 , cw3=[110,90,90] , la2=['Transform','Object Center'])
	mc.radioButtonGrp('rotAxis_RBG' , l=' Axis -->>  ' , nrb=3 , sl=1 , cw4=[105,65,65,65] , la3=['X','Y','Z'])
	mc.button('rot_BT' , l='Rotate' , bgc=[.6,.6,.6] , w=300 , c=lambda event:editShapeProc(1))
	mc.separator('sep_2' , w=300 , style='double')
	
	#Input Attributes for scaling
	mc.text('scale_TX' , l='[||||||||||||| SCALE |||||||||||||] ' , w=300 ,h=24 , fn='boldLabelFont' , al='center')
	mc.radioButtonGrp('scalePivot_RBG' ,l=' Pivot Position -->>  ',nrb=2 , sl=1 , cw3=[110,90,90] , la2=['Transform','Object Center'])
	mc.floatSliderButtonGrp('scaleValue_FSBG' , label='Scale.Value' , f=1 , cw4=[68,35,158,50] , s=0.1 , bl='Rev' , bc=lambda :reverseFSBG("scaleValue_FSBG") , min=-100 , max=100 , v=0.25)
	mc.checkBoxGrp('scaleAxis_CBG' , numberOfCheckBoxes=3, label='Axis -->>', cw4=[100,60,60,60] , labelArray3=['X', 'Y', 'Z'] , va3 = [1,1,1])
	mc.button('scale_BT' , l='Scale' , bgc=[.6,.6,.6] , w=300 , aop=True , c=lambda event:editShapeProc(2))
	mc.separator('sep_3' , w=300 , style='double')
	
	#Input Attributes for mirror
	mc.text( 'mirr_TX' , l='[||||||||||||| MIRROR |||||||||||||] ' , w=300 ,h=24 , fn='boldLabelFont' , al='center' )
	mc.textFieldGrp( 'searchTxt', cw2=(70,50), label='Search for:', tx='Left' )
	mc.textFieldGrp( 'replaceTxt', cw2=(80,50), label='Replace with:', tx='Right' )
	#mc.button( 'mirr_BT' , l='Mirror' , bgc=[.6,.6,.6] , w=292 , aop=True , c=lambda event:mirrorSelected() )
	mc.button( 'mirr_BT' , l='Mirror' , bgc=[.6,.6,.6] , w=300 , aop=True , c=lambda event:editShapeProc(3))
	
	
	mc.formLayout('formLay_ES' , edit = True , attachForm=[('transSpace_RBG', 'top', 25) , 	('transValue_FSBG', 'top', 50) ,
	('transAxis_RBG', 'top', 75) , ('trans_BT', 'top', 100) , ('sep_1', 'top', 130) , ('rot_TX', 'top', 135),('rotSpace_RBG', 'top', 160),
	 ('rotValue_FSBG', 'top', 185),('rotPivot_RBG', 'top', 212) , ('rotAxis_RBG', 'top', 235),('rot_BT', 'top', 260),('sep_2', 'top', 290),
	 ('scale_TX', 'top', 295),('scalePivot_RBG', 'top', 320),('scaleValue_FSBG', 'top', 345),('scaleAxis_CBG', 'top', 370),('scale_BT', 'top', 390),
	 ('sep_3', 'top', 420), ('mirr_TX', 'top', 425), ('searchTxt', 'top', 450), ('replaceTxt', 'top', 450), 
	 ('searchTxt', 'left', 10), ('replaceTxt', 'left', 150), ('mirr_BT', 'top', 480)])
	
	mc.showWindow('winEditShape')


#Value Reversing
def reverseFSBG(slider):
	getFSBGval = mc.floatSliderButtonGrp(slider , q=True , v=True)
	newValue = getFSBGval * -1
	mc.floatSliderButtonGrp(slider , e=True , v=newValue)

#Shape Editing	
def editShapeProc(procNo):
	mc.undoInfo( ock = True )
	sel=mc.ls(sl=1)
	for each in sel:
 		getShapes=mc.listRelatives(each , s=True , type='nurbsCurve')
 		for shape in getShapes:
			allVertex = []
 			spans=mc.getAttr(shape+'.spans')
 			degree=mc.getAttr(shape+'.degree')
 			form=mc.getAttr(shape+'.form')
 			if form==0: CVs=spans+degree
 			else: CVs=spans
 			for i in range(CVs):
 				allVertex.append(shape + '.cv[%d]' % i)
 			#Translation
			if procNo == 0:
				getTransSpace = mc.radioButtonGrp('transSpace_RBG' , q=True , sl=True)
				getTransValue = mc.floatSliderButtonGrp('transValue_FSBG' , q=True , v=True)
				getTransAxis = mc.radioButtonGrp('transAxis_RBG' , q=True , sl=True)
				transValue = [getTransValue,0,0]
				if getTransAxis==2:transValue=[0,getTransValue,0]
				elif getTransAxis==3:transValue=[0,0,getTransValue]
				spaceValue = [1,0,0]
				if getTransSpace==2:spaceValue=[0,1,0]
				elif getTransSpace==3:spaceValue=[0,0,1]
				mc.move(transValue[0] , transValue[1] , transValue[2] , allVertex, r=True, ws=spaceValue[0], os=spaceValue[1] , ls=spaceValue[2])
			#Rotation
 			if procNo == 1:
				getRotSpace = mc.radioButtonGrp('rotSpace_RBG' , q=True , sl=True)
				getRotValue = mc.floatSliderButtonGrp('rotValue_FSBG' , q=True , v=True)
				getRotPivot = mc.radioButtonGrp('rotPivot_RBG' , q=True , sl=True)
				getRotAxis = mc.radioButtonGrp('rotAxis_RBG' , q=True , sl=True)
				rotValue = [getRotValue,0,0]
				if getRotAxis==2:rotValue = [0,getRotValue,0]
				elif getRotAxis==3:rotValue = [0,0,getRotValue]
				spaceValue = [1,0]
				if getRotSpace==2:spaceValue=[0,1]
				rotPivot = 0
				if getRotPivot==2:rotPivot = 1
				mc.rotate(rotValue[0],rotValue[1],rotValue[2], allVertex , r=True , ws=spaceValue[0] , os=spaceValue[1] , ocp=rotPivot)
			#Scaling
			if procNo == 2:
				getScaleValue = mc.floatSliderButtonGrp('scaleValue_FSBG' , q=True , v=True)
				getScalePivot = mc.radioButtonGrp('scalePivot_RBG' , q=True , sl=True)
				getXAxis = mc.checkBoxGrp('scaleAxis_CBG' , q=True , v1=True)
				getYAxis = mc.checkBoxGrp('scaleAxis_CBG' , q=True , v2=True)
				getZAxis = mc.checkBoxGrp('scaleAxis_CBG' , q=True , v3=True)
				getTranScaleValue = mc.getAttr(each + '.scale')
				scaleValue = [(getTranScaleValue[0][0]+(getScaleValue*getXAxis)),(getTranScaleValue[0][1]+(getScaleValue*getYAxis)),(getTranScaleValue[0][2]+(getScaleValue*getZAxis))]
				scalePivot = 0
				if getScalePivot==2:scalePivot=1
				mc.scale(scaleValue[0],scaleValue[1],scaleValue[2], allVertex , r=True , ocp=scalePivot)
			#mirroring
			if procNo == 3:
				searchStr = mc.textFieldGrp( 'searchTxt', q=True, tx=True )
				replaceStr = mc.textFieldGrp( 'replaceTxt', q=True, tx=True )
				if not searchStr:	searchStr = 'Left'
				if not replaceStr:	replaceStr = 'Right'
				
				for i in range(len(allVertex)):
					oppVrtx = allVertex[i].replace(searchStr,replaceStr)
					getPos = mc.xform(allVertex[i],t =True,q=1,ws=1)
					mc.xform(oppVrtx,ws =True,t = [getPos[0]*-1,getPos[1],getPos[2]])
					
	mc.undoInfo( cck = True )				

#**************************************************END**************************************************#

