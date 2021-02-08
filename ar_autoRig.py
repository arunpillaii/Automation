											#---------------------------------------------------------------#
											# 	DESCRIPTION	: Main Python Module for Auto Rigging tool     	#	 																		   
											# 	AUTHOR 			: Arun . S - arunpillaii@gmail.com         	#                    												                       				                     
											# 	VERSION			: 2.00 , 17 October 2011	            	#
											#   Copyright (C) 2011.  All rights reserved.					#
											#---------------------------------------------------------------#
# imports!!
import maya.cmds as mc
import maya.mel as mm
import os
import ar_rigTemplate as RT;reload(RT)
import ar_createSkeleton as CS;reload(CS)
import ar_rigSpine as RS;reload(RS)
import ar_rigArms as RA;reload(RA)
import ar_dynParent as DP;reload(DP)
import ar_rigLeg as RL;reload(RL)
import ar_rigHead as RH;reload(RH)
import ar_menuScripts as MS;reload(MS)
import ar_rigHierarchy as BH;reload(BH)
import ar_skinJoints as SJ;reload(SJ)
import ar_setDefault as SD;reload(SD)
import SC_controlTransfer as CT;reload(CT)
import ar_createProxy as CP;reload(CP)

def ar_autoRig(loadEvent = 0):
	# UI exists check
	if mc.window('winAutoRig',exists = 1):
		mc.deleteUI('winAutoRig',window = 1)
	if mc.windowPref('winAutoRig',exists = 1)and loadEvent == 0:
		mc.windowPref('winAutoRig',remove = True)

	# Server Path for listing character names
	serverPath = 'Z:/Production/WIP/RiggingWIP/CHARACTERS'

	# Main window and Menu Creation
	win = mc.window('winAutoRig',t = "AutoRiggingTool" ,menuBar  = 1 ,s = 1 ,wh = (450,597))
	mc.menu(label = "File")
	mc.menuItem(label = "Refresh",c = ("import ar_autoRig as AR;AR.ar_autoRig(1)"))
	mc.menuItem(label = "Close",c = "mc.deleteUI('winAutoRig',window = 1)")
	mc.menu(label = "Help")
	mc.menuItem(label = "Help.." ,c = "")
	mc.menuItem(label = "About!",c = "")
	mc.columnLayout('maincolmlay')
	userName=os.getenv('USERNAME')
	imageFolder= os.path.dirname(RA.__file__)
	mc.image(image=(imageFolder +'/icons/BanerNew.jpg'),h = 75 )
	mc.separator(style = 'none' , h = 10)
	mc.rowColumnLayout(nc = 2 , cw = ([1 , 150], [2 ,250]))
	mc.text(l = 'Character Name  :> ' , al = 'center' , fn = 'boldLabelFont' )
	mc.textField('CharName' , w = 50)
	mc.popupMenu()
	if os.path.exists(serverPath):
		characters = os.listdir(serverPath )	
		if len(characters):
			for i in range(len(characters)):
				mc.menuItem(('menuitemCharTF%d' % i),l = characters[i] ,c = ('ar_autoRig.mc.textField("CharName" , e = True , tx = \'%s\')' % characters[i]) )	
	mc.setParent('..')
	mc.separator(style = 'none' , h = 15)
	mc.rowColumnLayout(nc = 2 , cw = ([1 , 225], [2 ,225]), co = ([1 , 'left' , 20] , [2 , 'left' , 20]))
	mc.textFieldGrp('userName' , l = 'Rigged By  : ' , cw2 = [75 , 100] , ed = 0 , tx = (os.getenv('username')))
	mc.optionMenu( label=' Character Type :' , h = 25)
	for obj in ['Main' , 'Secondary' , 'Incidental']:mc.menuItem( label = obj )
	mc.setParent('..')
	mc.separator(style = 'out' , h = 10, w = 450)
	mainTabLay = mc.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
	
	# QuickRig Layout
	GeneralFL = mc.frameLayout(l = '  Quick Rig  ' , h = 350 , w = 450 , labelAlign = "center" , li = 155 , borderStyle = "etchedIn", p = mainTabLay)
	mc.formLayout('generalFoL')
	mc.rowColumnLayout('genRCL' , nc = 2 , cw = ([1 , 250], [2 ,200]), co = ([1 , 'left' , 60] , [2 , 'left' , 40]))
	fingerOM = mc.optionMenu('fingerOM' , label=' No of Fingers :' , w = 50)
	for i in range(6):mc.menuItem( label = i )
	mc.optionMenu(fingerOM ,  edit = True, v = 5)
	mirrorCB = mc.checkBox('mirrorCB' , l = 'Mirror?' , v = 1, h = 25)
	mc.setParent('..')
	tempScaleFSL = mc.floatSliderGrp('tempScaleFSL' , field=True, label='Character Scale -->', minValue= .1, maxValue=10, value=1 )
	mc.button('btnCrtTem',l = 'Create Template' , c = lambda event:ar_btnCmds(0) , w = 350)
	mc.separator('sepFl1',style = 'in' , h = 10 , w = 426)
	noSpineISL = mc.intSliderGrp('noSpineISL' , field=True, label='Spine Joints -->', minValue= 3, maxValue=25, value=7 )
	backUpTpltCB = mc.checkBox('backUpTpltCB' , l = 'BackUp Template?' , v = 0, h = 25)
	#noTongueISL = mc.intSliderGrp('noTongueISL' , field=True, label='Tongue Joints :>>', minValue= 3, maxValue=25, value=6 )
	mc.button('btnCrtSkele',l = 'Create Skeleton' , c = lambda event:ar_btnCmds(1) , w = 350)
	mc.separator('sepFl2',style = 'in' , h = 10 , w = 426)
	
	bendRigTXT = mc.text('bendRigTXT',l='Bend Rig',fn='smallBoldLabelFont',w=75)
	mc.rowColumnLayout('bendJntsRCL' , nc = 3 , cw = ([1 , 150], [2 ,125],[3,50]), co = ([1 , 'left' , 90] , [2 , 'left' , 40]))
	armsBendCB = mc.checkBox('armsBendCB' , l = 'Arms ?' , v = 1, h = 25)
	mc.text('armBendTXT', l='No of Joints   >>')
	armBendJntsIF=mc.intField('armBendJntsIF',min = 1,v=7,ed = 1,ann = "Right Click Here")
	mc.popupMenu('armsBendPPM')
	for i in range(3,11):
		mc.menuItem(('menuitarmBendIF%d' % i),l = i ,c = "mc.intField('%s' ,e = 1, v =  %d" % (armBendJntsIF,i) + ")" )
		
	legsBendCB = mc.checkBox('legsBendCB' , l = 'Legs ?' , v = 1, h = 25)
	mc.text('legBendTXT',l='No of Joints   >>')
	legBendJntsIF=mc.intField('legBendJntsIF',min = 1,v=7,ed = 1,ann = "Right Click Here")
	mc.popupMenu('legsBendPPM')
	for i in range(3,11):
		mc.menuItem(('menuitlegBendIF%d' % i),l = i ,c = "mc.intField('%s' ,e = 1, v =  %d" % (legBendJntsIF,i) + ")" )
	mc.setParent('..')
	
	mc.checkBox(armsBendCB, e = 1, onc=("mc.intField('armBendJntsIF',e=1, ed = 1),mc.text('armBendTXT',e=1,en=1)"),
	ofc=("mc.intField('armBendJntsIF',e=1, ed = 0),mc.text('armBendTXT',e=1,en=0)"))
	mc.checkBox(legsBendCB, e = 1, onc=("mc.intField('legBendJntsIF',e=1, ed = 1),mc.text('legBendTXT',e=1,en=1)"),
	ofc=("mc.intField('legBendJntsIF',e=1, ed = 0),mc.text('legBendTXT',e=1,en=0)"))
	
	mc.separator('sepFl3',style = 'in' , h = 5 , w = 325)
	mc.rowColumnLayout('wholeRCL' , nc = 3 , cw = ([1 , 150], [2 ,150],[3,150]), co = ([1 , 'left' , 60] , [2 , 'left' , 40]))
	sjCB = mc.checkBox('sjCB' , l = 'Skin Joints ?' , v = 1, h = 25)
	proxyCB = mc.checkBox('proxyCB' , l = 'Proxy ?' , v = 0, h = 25)
	rigEyeCB = mc.checkBox('rigEyeCB' , l = 'EyeRig ?' , v = 1, h = 25)
	mc.setParent('..')	
	
	mc.button('btnRigWhole',l = '*** RIG THE WHOLE CHARACTER ***' ,c = lambda event:ar_btnCmds(2), h = 35 , w = 375)
	
	# QuickRig layout Edit
	mc.formLayout('generalFoL' , edit = True , attachForm=[('genRCL', 'top', 5) ,('tempScaleFSL', 'top', 35),('btnCrtTem', 'top', 65) ,
	('btnCrtTem', 'left', 35),('sepFl1', 'top', 87),(noSpineISL , 'top', 100),('backUpTpltCB' , 'top', 120),('backUpTpltCB', 'left', 150),
	('btnCrtSkele', 'top', 145),('btnCrtSkele', 'left', 35),('sepFl2', 'top', 167),('bendRigTXT', 'top', 175),('bendRigTXT', 'left', 175),
	('bendJntsRCL', 'top', 193),('sepFl3', 'top', 248),('sepFl3', 'left', 50),('wholeRCL', 'top', 258),('btnRigWhole', 'top', 290),
	('btnRigWhole', 'left', 25)])
	mc.setParent('..')
	
# 	# SpineRig Layout
# 	RigSpineFL = mc.frameLayout(l = ' SetUp Spine ' , h = 250 , w = 425 , labelAlign = "center" , li = 155 , borderStyle = "etchedIn", p = mainTabLay)
# 	mc.formLayout('RigSpineFoL', vis=0)
# 	HipJntTFBG = mc.textFieldButtonGrp(l = 'Hip Joint  -->>' , bl = '      Select      ' , bc = '' , w = 425 ,cw3 = [95 , 175 ,100], cat = [3 , 'left' , 15])
# 	NeckJntTFBG = mc.textFieldButtonGrp(l = 'Neck Joint  -->>' , bl = '      Select      ' , bc = '' , w = 425 ,cw3 = [95 , 175 ,100], cat = [3 , 'left' , 15])
# 	spineMtdRBG = mc.radioButtonGrp(nrb=2, sl =1 , l = 'FK Controls  :', labelArray2=['On', 'Off'], cw3 = [100 , 75 , 75])
# 	mc.button('btnRigspine',l = '** RIG SPINE **' , h = 30 , w = 375)
# 	
# 	# SpineRig Layout Edit
# 	mc.formLayout('RigSpineFoL' , edit = True , attachForm=[(HipJntTFBG, 'top', 15), (HipJntTFBG, 'left', 30),
# 	(NeckJntTFBG, 'top', 50), (NeckJntTFBG, 'left', 30),(spineMtdRBG, 'top', 95), (spineMtdRBG, 'left', 85),
# 	('btnRigspine', 'top', 180),('btnRigspine', 'left', 25)])
# 	mc.setParent('..')
# 
# 	# ArmRig Layout
# 	RigArmsFL = mc.frameLayout(l = ' SetUp Arms ' , h = 250 , w = 425 , labelAlign = "center" , li = 150 , borderStyle = "etchedIn", p = mainTabLay)
# 	mc.formLayout('RigArmFoL' , vis=0)
# 	ClavicleTFBG = mc.textFieldButtonGrp(l = 'Clavicle Jnt  -->> ' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [95 , 175 ,100], cat = [3 , 'left' , 15])
# 	ShoulderTFBG = mc.textFieldButtonGrp(l = 'Shoulder Jnt  -->>' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [95 , 175 ,100], cat = [3 , 'left' , 15])
# 	ElbowTFBG = mc.textFieldButtonGrp(l = 'Elbow Jnt  -->>    ' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [95 , 175 ,100], cat = [3 , 'left' , 15])
# 	WristTFBG = mc.textFieldButtonGrp(l = 'Wrist Jnt -->>      ' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [95 , 175 ,100], cat = [3 , 'left' , 15])
# 	ArmSideRBG = mc.radioButtonGrp(nrb=2, sl = 1 , l = 'Side  :', labelArray2=['Left', 'Right'], cw3 = [120 , 75 , 75] )
# 	ArmOptCBG = mc.checkBoxGrp(ncb = 3 ,labelArray3 = ['Stretch' , 'Bend' , 'IKFK AutoSnap'], cw3 = [125 , 125 , 125], va3 = [1 , 1 , 1])
# 	ArmMtdRBG = mc.radioButtonGrp(nrb=3, sl = 3 , l = 'Rig Method  :', labelArray3=['IK', 'FK', 'Both'], cw4 = [120 , 75 , 75 ,75] )
# 	mc.button('btnRigArms',l = '** RIG ARM **' , h = 30 , w = 375)
# 	
# 	# ArmRig Layout Edit
# 	mc.formLayout('RigArmFoL' , edit = True , attachForm=[(ClavicleTFBG, 'top', 10), (ClavicleTFBG, 'left', 30),
# 	(ShoulderTFBG, 'top', 37), (ShoulderTFBG, 'left', 30),(ElbowTFBG, 'top', 63), (ElbowTFBG, 'left', 30),
# 	(WristTFBG, 'top', 89), (WristTFBG, 'left', 30),(ArmSideRBG, 'top', 120),(ArmSideRBG, 'left', 30),
# 	(ArmOptCBG, 'top', 145),(ArmOptCBG, 'left', 45),	(ArmMtdRBG, 'top', 170),(ArmMtdRBG, 'left', 30),
# 	('btnRigArms', 'top', 200),('btnRigArms', 'left', 30)])
# 	mc.setParent('..')
# 	
# 	# LegRig Layout
# 	RigLegsFL = mc.frameLayout(l = ' SetUp Legs ' , h = 250 , w = 425 , labelAlign = "center" , li = 150 , borderStyle = "etchedIn", p = mainTabLay)
# 	mc.formLayout('RigLegFoL', vis=0)
# 	HipTFBG = mc.textFieldButtonGrp(l = 'Hip Jnt  -->> ' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [95 , 175 ,100], cat = [3 , 'left' , 15])
# 	KneeTFBG = mc.textFieldButtonGrp(l = 'Knee Jnt  -->> ' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [95 , 175 ,100], cat = [3 , 'left' , 15])
# 	AnkleTFBG = mc.textFieldButtonGrp(l = 'Ankle Jnt  -->> ' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [95 , 175 ,100], cat = [3 , 'left' , 15])
# 	BallTFBG = mc.textFieldButtonGrp(l = 'Ball Jnt -->> ' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [95 , 175 ,100], cat = [3 , 'left' , 15])
# 	ToeTFBG = mc.textFieldButtonGrp(l = 'Toe Jnt -->> ' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [95 , 175 ,100], cat = [3 , 'left' , 15])
# 	LegSideRBG = mc.radioButtonGrp(nrb=2, sl = 1 , l = 'Side  :', labelArray2=['Left', 'Right'], cw3 = [120 , 75 , 75] )
# 	LegOptCBG = mc.checkBoxGrp(ncb = 2 ,labelArray2 = ['Stretch' , 'Bend'], cw2 = [125 , 125], va2 = [1 , 1 ])
# 	LegMtdRBG = mc.radioButtonGrp(nrb=3, sl = 3 , l = 'Rig Method  :', labelArray3=['IK', 'FK', 'Both'], cw4 = [120 , 75 , 75 ,75] )
# 	mc.button('btnRigLeg',l = '** RIG LEG **' , h = 30 , w = 375)
# 
# 	# LegRig Layout Edit
# 	mc.formLayout('RigLegFoL' , edit = True , attachForm=[(HipTFBG, 'top', 5), (HipTFBG, 'left', 30),
# 	(KneeTFBG, 'top', 30), (KneeTFBG, 'left', 30),(AnkleTFBG, 'top', 55), (AnkleTFBG, 'left', 30),
# 	(BallTFBG, 'top', 80), (BallTFBG, 'left', 30),(ToeTFBG, 'top', 105),(ToeTFBG, 'left', 30),
# 	(LegSideRBG, 'top', 132),(LegSideRBG, 'left', 45),	(LegOptCBG, 'top', 153),(LegOptCBG, 'right', 50),
# 	(LegMtdRBG, 'top', 175),(LegMtdRBG, 'left', 30),('btnRigLeg', 'top', 200),('btnRigLeg', 'left', 30)])
# 	mc.setParent('..')
# 	
# 	# HeadRig Layout
# 	RigHeadFL = mc.frameLayout(l = ' SetUp Head and Neck ' , h = 250 , w = 425 , labelAlign = "center" , li = 150 , borderStyle = "etchedIn", p = mainTabLay)
# 	mc.formLayout('RigHeadFoL', vis=0)
# 	NeckTFBG = mc.textFieldButtonGrp(l = 'Neck Jnt  -->> ' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [100 , 175 ,100], cat = [3 , 'left' , 15])
# 	HeadStartTFBG = mc.textFieldButtonGrp(l = 'HeadStart  -->> ' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [100 , 175 ,100], cat = [3 , 'left' , 15])
# 	HeadEndTFBG = mc.textFieldButtonGrp(l = 'HeadEnd  -->> ' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [100 , 175 ,100], cat = [3 , 'left' , 15])
# 	NeckMthdRBG = mc.radioButtonGrp(nrb=2, sl = 1 , l = 'Neck Rig Method  :', labelArray2=['Single Joint', 'Multi Joint'], cw3 = [120 , 120 , 120] )
# 	NeckStretchCB = mc.checkBox(l = 'Stretch' , v = 1)
# 	mc.button('btnHeadRig',l = '** RIG NECK  n  HEAD **' , h = 30 , w = 375)
# 
# 	# HeadRig Layout Edit
# 	mc.formLayout('RigHeadFoL' , edit = True , attachForm=[(NeckTFBG, 'top', 20), (NeckTFBG, 'left', 30),
# 	(HeadStartTFBG, 'top', 55), (HeadStartTFBG, 'left', 30),(HeadEndTFBG, 'top', 90), (HeadEndTFBG, 'left', 30),
# 	(NeckMthdRBG, 'top', 135),(NeckMthdRBG, 'left', 45),(NeckStretchCB , 'top', 170),(NeckStretchCB , 'left', 175),
# 	('btnHeadRig', 'top', 200),('btnHeadRig', 'left', 30)])
# 	mc.setParent('..')
# 	
# 	# HeirarchyRig Layout
# 	BasicHierarchyFL = mc.frameLayout(l = ' Basic Hierarchy ' , h = 250 , w = 425 , labelAlign = "center" , li = 150 , borderStyle = "etchedIn", p = mainTabLay)
# 	mc.formLayout('BasicHierarchyFoL', vis=0)
# 	NeckTFBG = mc.textFieldButtonGrp(l = 'Neck Jnt  -->> ' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [100 , 175 ,100], cat = [3 , 'left' , 15])
# 	HeadStartTFBG = mc.textFieldButtonGrp(l = 'HeadStart  -->> ' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [100 , 175 ,100], cat = [3 , 'left' , 15])
# 	HeadEndTFBG = mc.textFieldButtonGrp(l = 'HeadEnd  -->> ' , bl = '    Select    ' , bc = '' , w = 425 ,cw3 = [100 , 175 ,100], cat = [3 , 'left' , 15])
# 	NeckMthdRBG = mc.radioButtonGrp(nrb=2, sl = 1 , l = 'Neck Rig Method  :', labelArray2=['Single Joint', 'Multi Joint'], cw3 = [120 , 120 , 120] )
# 	NeckStretchCB = mc.checkBox(l = 'Stretch' , v = 1)
# 	mc.button('btnHeadRig',l = '** RIG NECK  n  HEAD **' , h = 30 , w = 375)
# 
# 	# Hierarchy Layout Edit
# 	mc.formLayout('BasicHierarchyFoL' , edit = True , attachForm=[(NeckTFBG, 'top', 20), (NeckTFBG, 'left', 30),
# 	(HeadStartTFBG, 'top', 55), (HeadStartTFBG, 'left', 30),(HeadEndTFBG, 'top', 90), (HeadEndTFBG, 'left', 30),
# 	(NeckMthdRBG, 'top', 135),(NeckMthdRBG, 'left', 45),(NeckStretchCB , 'top', 170),(NeckStretchCB , 'left', 175),
# 	('btnHeadRig', 'top', 200),('btnHeadRig', 'left', 30)])
# 	mc.setParent('..')
#   
# 	#Extras layout
# 	ToolsFL = mc.frameLayout(l = ' Supporting Tools ' , h = 250 , w = 425 , labelAlign = "center" , li = 150 , borderStyle = "etchedOut", p = mainTabLay)
# 	mc.formLayout('ToolsFoL')
# 	mc.button('btnShapeEdit' , l='ShapeEditor' , w = 75,c = lambda event:SE.ar_editShape())
# 	mc.button('btnSetDefault' , l='Set Defaults' , w = 75,c = lambda event:SD.ar_setDefault())
# 	mc.button('btnCtrlTransfer',  l='Wt/Rd Ctrls' , w = 75,c = lambda event:CT.SC_controlTransfer())
# 	mc.button('ToolsBtn4', w = 75)
# 
# 	# Extras layout Edit
# 	mc.formLayout('ToolsFoL' , edit = True, af = [('btnShapeEdit' , 'left'  , 25),('btnShapeEdit' , 'top'  , 10),
# 	('btnSetDefault' , 'left'  , 125),('btnSetDefault' , 'top'  , 10),('btnCtrlTransfer' , 'left'  , 225),('btnCtrlTransfer' , 'top'  , 10),
# 	('ToolsBtn4' , 'left'  , 325),('ToolsBtn4' , 'top'  , 10)] )
# 	mc.setParent('..')
#   	
# 	# Main TabLayout Edit
# 	mc.tabLayout( mainTabLay, edit=True, tabLabel=((GeneralFL , ' Skeleton '),
# 	(RigSpineFL , 'Rig Spine'),(RigArmsFL ,'Rig Arms'),	(RigLegsFL , 'Rig Legs'),
# 	(RigHeadFL , 'Rig Head'),(BasicHierarchyFL , 'Basic Hierarchy'), (ToolsFL , ' Xtra Tools ')), sti = 1 )

#	mc.tabLayout( mainTabLay, edit=True, tabLabel=((GeneralFL , ' Skeleton '),(ToolsFL , ' Xtra Tools ')), sti = 1 )
	mc.tabLayout( mainTabLay, edit=True, tabLabel=(GeneralFL , ' Skeleton '))
	mc.showWindow('winAutoRig')
	# if mc.dockControl('autoDock',exists=1):
	# 	mc.deleteUI('autoDock')
	# mc.dockControl('autoDock',a='right',label='Auto-Rigging Tool',content='winAutoRig',allowedArea= "all")
# Button Commands	
def ar_btnCmds(callProc):
	
	# Rig Details
	charaName = mc.textField('CharName' , q = True , tx = True) 
	userName = mc.textFieldGrp('userName' , q = True , tx = True)
	
#	# get Character Scale
	if mc.objExists('HeadEnd_CJ'):
		tmpLoc=mc.spaceLocator()	
		mc.delete(mc.pointConstraint('HeadEnd_CJ',tmpLoc,mo=0,skip=('x','z')))
		locVal=mc.getAttr(tmpLoc[0]+'.ty')
		charScale=locVal/6.0
		print charScale
		mc.delete(tmpLoc)
		
	#charScale = mc.floatSliderGrp('tempScaleFSL',q=True,value=1)
	
	
	
	if not charaName:
		mc.confirmDialog( title='Name Error', message='Enter Character Name', button=['OK'])
		return None
	details = [charaName , userName]
	
	# Button Commands
	if callProc == 0: # Template
		queryfingerOM = int(mc.optionMenu('fingerOM' , q = True , v = True))
		querymirrorCB = mc.checkBox('mirrorCB' , q = True , v = True)
		RT.ar_Template(details , querymirrorCB , queryfingerOM)
	
	if callProc == 1: # Skeleton	
		querynoSpineISL = mc.intSliderGrp('noSpineISL' , query = True , value = True )
		queryTempBackUp = mc.checkBox('backUpTpltCB' , q = True , v = True)
		CS.ar_createSkeleton(details , querynoSpineISL , queryTempBackUp)
		
	if callProc == 2: # Rig Whole		
   
		#Spine
		startSpine = 'Root_CJ'
		neck = 'Neck_CJ'
		retSpine = RS.ar_rigSpine(startSpine,neck,charScale)

		#Legs & Arms
		for Side in ['Left' , 'Right']:

			#Initialising Joint Names for Leg
			LegStart = Side + 'UpLeg_CJ'
			Heel = Side + 'Heel_CJ'
			HeelExt = Side + 'HeelExt_CJ'
			HeelInt = Side + 'HeelInt_CJ'
			querylegsBendCB = mc.checkBox('legsBendCB' ,q = True , v = True)
			querylegBendJntsIF=mc.intField('legBendJntsIF',q = True,v=True)
			retlegs = RL.ar_rigLegs(LegStart,Heel,HeelExt,HeelInt,Side,querylegsBendCB,querylegBendJntsIF,charScale)
			
			#Initialising Joint Names for Arm
			clavJnt = Side + 'Clavicle_CJ'
			queryarmsBendCB = mc.checkBox('armsBendCB' ,q = True , v = True)
			queryarmBendJntsIF=mc.intField('armBendJntsIF',q=True,v=True)
			retarms = RA.ar_rigArms(clavJnt , Side , queryarmsBendCB,queryarmBendJntsIF,charScale)
	
		#Neck
		NeckJnt = 'Neck_CJ'
		HeadStart = 'Head_CJ'
		HeadEnd = 'HeadEnd_CJ'
		queryrigEyeCB = mc.checkBox('rigEyeCB' , q = True , v = True)
		RH.ar_rigHead(NeckJnt,HeadStart,HeadEnd,1,1,queryrigEyeCB,charScale)
		
		#Hierarchy
		mainGrp = BH.ar_rigHierarchy(charaName,details)
		
		#Dynamic Parenting
		sourceObj = ['Ctrl_LeftArm' , 'Ctrl_RightArm' , 'Ctrl_LeftElbowPole','Ctrl_RightElbowPole','Ctrl_LeftClavicle' ,
		'Ctrl_RightClavicle','Ctrl_LeftFoot','Ctrl_RightFoot','Ctrl_LeftAux','Ctrl_RightAux','Ctrl_Head','Ctrl_LeftKnee','Ctrl_RightKnee']
		targets = [('Ctrl_LeftClavicle','Ctrl_Head' , 'Ctrl_Torso' , 'Ctrl_Body' ,'Ctrl_LeftAux', 'Ctrl_PLACE' , 'Ctrl_ROOT'),
		('Ctrl_RightClavicle','Ctrl_Head' , 'Ctrl_Torso' , 'Ctrl_Body' ,'Ctrl_RightAux', 'Ctrl_PLACE' , 'Ctrl_ROOT') ,
		('Ctrl_Shoulder','Ctrl_LeftArm','Ctrl_PLACE'),
		('Ctrl_Shoulder','Ctrl_RightArm' ,'Ctrl_PLACE'),
		('Anchor_Torso','Ctrl_PLACE'),
		('Anchor_Torso','Ctrl_PLACE'),
		('Ctrl_Hip' , 'Ctrl_Body' , 'Ctrl_PLACE' , 'Ctrl_ROOT'),
		('Ctrl_Hip' , 'Ctrl_Body' , 'Ctrl_PLACE' , 'Ctrl_ROOT'),
		('Ctrl_PLACE' , 'Ctrl_ROOT'),
		('Ctrl_PLACE' , 'Ctrl_ROOT'),
		('Ctrl_Neck','Ctrl_PLACE'),
		('Ctrl_LeftFoot','Ctrl_PLACE' , 'Ctrl_ROOT'),
		('Ctrl_RightFoot','Ctrl_PLACE' , 'Ctrl_ROOT')]
		defaultVal = [5,5,2,2,0,0,2,2,0,0,0,1,1]
		for i in range(len(sourceObj)):
			#DP.ar_dynParent(sourceObj[i],targets[i],defaultVal[i])
			DP.ar_dynParent(sourceObj[i],None,targets[i],[(target.split('_')[1]) for target in targets[i]],defaultVal[i])
			
		#Skin Joints 
		querysjCB = mc.checkBox('sjCB' , q = True , v = True)
		if querysjCB:
			SJ.ar_skinJoints()
		
		#Proxy Creation
		if mc.checkBox('proxyCB' , q = True , v = True):
			grpProxy = CP.ar_buildProxy()
			mc.parent(grpProxy , 'MODELS')
		
		#Set Defults Values to Custom Attributes
		ctrls=mc.ls('Ctrl_*',type='transform')
		SD.ar_setDefault(ctrls)
 	
 		#Set Expresion for Dag Menu
 		# exp = mc.expression(n = 'dagSource', s='source dagMenuProc2012.mel;' )
 		#exp = mc.expression(n = 'dagSource', s='if (getApplicationVersionAsFloat() == 2008)\n{\nsource dagMenuProc2008.mel;\n}\nif (getApplicationVersionAsFloat() == 2009)\n{\nsource dagMenuProc2009.mel;\n}' )
 		#exp = mc.expression(n = 'dagSource', s='source dagMenuProc2008.mel;' )
 		# mc.lockNode(exp, l = True)
 		
 		mc.select(cl = True)

#**************************************************END**************************************************#

ar_autoRig()
