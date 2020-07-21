											#-----------------------------------------------------------#
											# 	DESCRIPTION	: Python Module for Creating Multiple       #
											#					Parents to the given Object				#	 																		   
											# 	AUTHOR 		: Arun . S - arunpillaii@gmail.com         	#                    												                       				                     
											# 	VERSION		: 1.00 , 03 March 2010		               	#
											#   Copyright (C) 2010.  All rights reserved.				#
											#-----------------------------------------------------------#
#imports!
import maya.cmds as mc
import maya.OpenMaya as om

def ar_dynParent(targetObj,optAttrObj,parentObjs,parentAttrNames,defaultVal,parMode=1,parType=3,offsetOnOff=1):
	upGrpTarget = mc.listRelatives(targetObj , p = True)#Get Parent grp	
	splitName = targetObj.split('_')
	try:
		getName=splitName[1]
	except IndexError:
		getName=splitName[0]
		pass
		
	if optAttrObj == None:optAttrObj=targetObj
	if parentAttrNames == None:parentAttrNames =[(name.split('_')[1]) for name in parentObjs]

	if parMode==1:
		mainGrpPB = mc.group(em = 1 , n = ('grp%s_PB' % getName))
		if upGrpTarget:mc.parent(mainGrpPB,upGrpTarget[0])
		mc.delete(mc.parentConstraint(targetObj , mainGrpPB))
		grpPB0 = mc.duplicate(mainGrpPB , n = ('grp%s_PB0' % getName))[0]
		grpPB1 = mc.duplicate(mainGrpPB , n = ('grp%s_PB1' % getName))[0]
		mc.parent(targetObj , mainGrpPB)
		arrayPB=[grpPB0,grpPB1]
		
		#Adding attributes for parent
		enumnames = [(target + ':') for target in parentAttrNames]
		mc.addAttr(optAttrObj , ln = 'ParentBlend' , at = 'double' , min = 0 , max = 1, k = True)
		mc.addAttr(optAttrObj , ln = 'Parent0' , at = 'enum' , en = (''.join(enumnames)), k = True)
		mc.setAttr((optAttrObj + '.Parent0') , defaultVal)
		mc.addAttr(optAttrObj , ln = 'Parent1' , at = 'enum' , en = (''.join(enumnames)), k = True)
		mc.setAttr((optAttrObj + '.Parent1') , defaultVal)
		
		parCon = mc.parentConstraint(grpPB0 , grpPB1 , mainGrpPB,mo=1)
		parConTgts = mc.parentConstraint(parCon[0] , q = True , wal = True)
		mc.connectAttr((optAttrObj + '.ParentBlend') , (parCon[0] + '.%s' % parConTgts[1]) )
		rev = mc.createNode('reverse' , n = ('grp%s_PB_rev' % getName))
		mc.connectAttr((parCon[0] + '.%s' % parConTgts[1]),(rev + '.inputX'))
		mc.connectAttr((rev + '.outputX') , (parCon[0] + '.%s' % parConTgts[0]))
		
		for n in range (2):
			for i in range (len(parentObjs)):	
				if parType == 1:
					targCon = mc.pointConstraint(parentObjs[i] , arrayPB[n] , mo = offsetOnOff)
					queryTarget = mc.pointConstraint(targCon[0] ,q = True , wal = True)
				elif parType == 2:
					targCon = mc.orientConstraint(parentObjs[i] , arrayPB[n] , mo = offsetOnOff)
					queryTarget = mc.orientConstraint(targCon[0] ,q = True , wal = True)
				elif parType == 3:
					targCon = mc.parentConstraint(parentObjs[i] , arrayPB[n] , mo = offsetOnOff)
					queryTarget = mc.parentConstraint(targCon[0] ,q = True , wal = True)
				
				conNode = mc.createNode('condition' , n = (getName + 'PB%d_Con%d' % (n , i)))
				mc.setAttr((conNode + '.colorIfFalse') , 0 , 0 ,0)
				mc.setAttr((conNode + '.colorIfTrue') ,1 , 1 , 1)
				mc.setAttr((conNode + '.secondTerm') , i)
				mc.connectAttr((optAttrObj + '.Parent%d' % n) , (conNode + '.firstTerm'))
				mc.connectAttr((conNode + '.outColor.outColorR') , (targCon[0] + '.%s' % queryTarget[i]))
		
	if parMode==2:	
		mainGrpPB = mc.group(em = 1 , n = ('grp%s_PB' % getName))
		if upGrpTarget:mc.parent(mainGrpPB,upGrpTarget[0])
		mc.delete(mc.parentConstraint(targetObj , mainGrpPB))
		mc.parent(targetObj , mainGrpPB)
		#Adding attributes for parent
		enumnames = [(target + ':') for target in parentAttrNames]
		mc.addAttr(optAttrObj , ln = 'Parent' , at = 'enum' , en = (''.join(enumnames)), k = True)
		mc.setAttr((optAttrObj + '.Parent') , defaultVal)
	
		for i in range (len(parentObjs)):	
			if parType == 1:
				targCon = mc.pointConstraint(parentObjs[i] , mainGrpPB , mo = offsetOnOff)
				queryTarget = mc.pointConstraint(targCon[0] ,q = True , wal = True)
			elif parType == 2:
				targCon = mc.orientConstraint(parentObjs[i] , mainGrpPB , mo = offsetOnOff)
				queryTarget = mc.orientConstraint(targCon[0] ,q = True , wal = True)
			elif parType == 3:
				targCon = mc.parentConstraint(parentObjs[i] , mainGrpPB , mo = offsetOnOff)
				queryTarget = mc.parentConstraint(targCon[0] ,q = True , wal = True)
				
			conNode = mc.createNode('condition' , n = (getName + 'Parent_Con%d' % i ))
			mc.setAttr((conNode + '.colorIfFalse') , 0 , 0 ,0)
			mc.setAttr((conNode + '.colorIfTrue') ,1 , 1 , 1)
			mc.setAttr((conNode + '.secondTerm') , i)
			mc.connectAttr((optAttrObj + '.Parent') , (conNode + '.firstTerm'))
			mc.connectAttr((conNode + '.outColor.outColorR') , (targCon[0] + '.%s' % queryTarget[i]))
			
def ar_dynParentWin(loadEvent = 0):
	# UI exists check
	if mc.window('dynParWin',exists = 1):
		mc.deleteUI('dynParWin',window = 1)
	if mc.windowPref('dynParWin',exists = 1)and loadEvent == 0:
		mc.windowPref('dynParWin',remove = True)
		
	# Main window and Menu Creation
	win = mc.window('dynParWin',t = "Dynamic Parenting Tool" ,menuBar  = 1 ,s = 1 ,wh = (520,525))
	mc.menu(label = "File")
	mc.menuItem(label = "Refresh",c = "ar_dynParent.ar_dynParentWin(1)")
	mc.menuItem(label = "Close",c = "mc.deleteUI('dynParWin',window = 1)")
	mc.menu(label = "Help")
	mc.menuItem(label = "Help.." ,c = "")
	mc.menuItem(label = "About!",c = "")
	
	mc.formLayout('dynParFoL')
	mc.textFieldButtonGrp('parConTFBG' , l='Target Control -->> ', tx='', bl='   << Get Control >>',
	cw3=[125,250,140],cat=[3,'both',15] , bc =lambda:loadTFBG('parConTFBG'))
	
	mc.checkBox('attrbCntrlCB' , label='Optional',v=0,onc='mc.textFieldButtonGrp("sepAttrcTFGB",e=1,en=1)',ofc='mc.textFieldButtonGrp("sepAttrcTFGB",e=1,en=0)')
	mc.textFieldButtonGrp('sepAttrcTFGB' , buttonLabel=' << Attr Control',cw2=[275,120],cat=[2,'both',15],en=0,	bc = lambda :loadTFBG('sepAttrcTFGB'))

	mc.radioButtonGrp('parModeRBG' , sl=1, label=' Parent Mode : ', labelArray2=['Multiple', 'Single'], numberOfRadioButtons=2 )
	mc.radioButtonGrp('parTypeRBG',sl=3, label=' Parent Type : ', labelArray3=['Translate', 'Rotate' , 'Both'], numberOfRadioButtons=3 )

	mc.checkBox('offsetCBG' , label='Offset - On/Off',v=1 )

	mc.text('parTXT', label='Parents', fn='boldLabelFont',w=50 )
	mc.text('attrTXT', label='AttributeName', fn='boldLabelFont',w=80 )

	mc.textScrollList('parentTSL',w=225,h=250,fn='fixedWidthFont',sc='mc.textScrollList("attrTSL",e=1,sii=mc.textScrollList("parentTSL",q=1,sii=1)[0])')
	mc.textScrollList('attrTSL',w=150,h=250,dcc=lambda:enterCustomName(mc.textScrollList("attrTSL",q=1,sii=1)[0]),fn='fixedWidthFont',sc='mc.textScrollList("parentTSL",e=1,sii=mc.textScrollList("attrTSL",q=1,sii=1)[0])')

	mc.button('addBTN',   l='Add Objects',w=80,c=lambda event:functionsTSL('addObj'))
	mc.button('removeBTN',l='Remove',w=80,c=lambda event:functionsTSL('remObj'))
	mc.button('insertBTN',l='Add New One',w=80,c=lambda event:functionsTSL('insertObj'))
	mc.button('clBTN',    l='Clear All',w=80,c=lambda event:functionsTSL('clearAll'))
	mc.button('upBTN',l='UP',w=80,c=lambda event:functionsTSL('goUpDn','up'))
	mc.button('dnBTN',l='DOWN',w=80,c=lambda event:functionsTSL('goUpDn','dn'))
	mc.button('crDynParBTN',l='Create Dynamic Parent',c=lambda event:parentBtn(),h=35,w= 400)

	mc.separator('sep1',st='out',w=520)
	mc.separator('sep2',st='out',w=520)
	mc.separator('sep3',st='out',w=520)

	mc.formLayout('dynParFoL' , edit = True , attachForm=[('parConTFBG', 'top', 5),
	('attrbCntrlCB', 'top', 38),('attrbCntrlCB', 'left', 20),
	('sepAttrcTFGB', 'top', 35),('sepAttrcTFGB', 'left', 100),
	('sep1', 'top', 60),
	('parModeRBG', 'top', 70),('parModeRBG', 'left', -10),
	('offsetCBG', 'top', 70),('offsetCBG', 'left', 375),
	('sep2', 'top', 90),
	('parTypeRBG', 'top', 100),
	('sep3', 'top', 120),
	('parTXT', 'top', 130),('parTXT', 'left', 105),('attrTXT', 'top', 130),('attrTXT', 'left', 380),
	('parentTSL', 'top', 150),('parentTSL', 'left', 15),
	('attrTSL', 'top', 150),('attrTSL', 'left', 343),

	('addBTN', 'top', 155),('addBTN', 'left', 250),
	('removeBTN', 'top', 195),('removeBTN', 'left', 250),
	('insertBTN', 'top', 240),('insertBTN', 'left', 250),
	('clBTN', 'top', 285),('clBTN', 'left', 250),
	('upBTN', 'top', 330),('upBTN', 'left', 250),
	('dnBTN', 'top', 370),('dnBTN', 'left', 250),
	('crDynParBTN', 'top', 420),('crDynParBTN', 'left', 55)])

	mc.showWindow('dynParWin')

def functionsTSL(switchMode , fun=None):
	sel=mc.ls(sl=1)
	if switchMode == 'addObj':
		if not sel:
			om.MGlobal.displayWarning('No Objects are selected...')
			return
		mc.textScrollList('parentTSL',e=True,ra=True,a=sel,sii=1)
		mc.textScrollList('attrTSL',e=True,ra=True,a=sel,sii=1)
	
	if switchMode == 'remObj':
		allObjs = mc.textScrollList('parentTSL',q=True,ai=True)
		if not allObjs:
			return
		if len(allObjs) ==1:
			mc.textScrollList('parentTSL',e=True,ra=True)
			mc.textScrollList('attrTSL',e=True,ra=True)
			return
		getObjint=mc.textScrollList('parentTSL',q=True,sii=True)
		selObj=getObjint
		if mc.textScrollList('parentTSL',q=True,ni=True)== getObjint[0]:selObj=getObjint[0]-1
		mc.textScrollList('parentTSL',e=True,rii=getObjint,sii=selObj)
		mc.textScrollList('attrTSL',e=True,rii=getObjint,sii=selObj)
		
	if switchMode == 'insertObj':
		if not sel:
			om.MGlobal.displayWarning('Select Objects to Add;...')
			return
		siObj=mc.textScrollList('parentTSL',q=True,sii=True)
		pos = siObj[len(siObj)-1]+1
		allObj=mc.textScrollList('parentTSL',q=True,ai=True)
		allAttrObj=mc.textScrollList('attrTSL',q=True,ai=True)
		for each in sel:
			if each in allObj:
				continue
			mc.textScrollList('parentTSL',e=True,ap=[pos,each])
			mc.textScrollList('attrTSL',e=True,ap=[pos,each])
			pos +=1
			allObj=mc.textScrollList('parentTSL',q=True,ai=True)
	
	if switchMode == 'clearAll':
		mc.textScrollList('parentTSL',e=True,ra=True)
		mc.textScrollList('attrTSL',e=True,ra=True)
	
	if switchMode == 'goUpDn':
		for each in ['parentTSL','attrTSL']:
			siObjIndex=mc.textScrollList(each,q=True,sii=True)
			allObj = mc.textScrollList(each,q=True,ai=True)
			newObjs = goUpDn(allObj,siObjIndex[0]-1,fun)
			mc.textScrollList(each,e=True,ra=True,a=newObjs[0],sii=newObjs[1])

def goUpDn(li,i,func):
			if func == 'up':
				if i == 0:
					return li,1
				return (li[:i-1] + [li[i]] + [li[i-1]] + li[i+1:]),i
			if func == 'dn':
				if i == len(li)-1:
					return li,i+1
				return li[:i] + [li[i+1]] + [li[i]] + li[i+2:],i+2
					
def loadTFBG(getTFBG):
	sel=mc.ls(sl=1)
	if not sel:
		om.MGlobal.displayWarning('Select a Object')
		return
	mc.textFieldButtonGrp(getTFBG,e=True,text=sel[0])
					
def enterCustomName(itmIndex):
	curItem=mc.textScrollList("attrTSL",q=1,si=1)[0]
	getRes = mc.promptDialog(t='Custom Name',	m='Enter Attribute Name:',tx=curItem,b=['OK', 'Cancel'],db='OK',cb='Cancel',	ds='Cancel')
	if getRes == 'OK':
		text = mc.promptDialog(q=True, t=True)
		if text:
			mc.textScrollList("attrTSL",e=1,rii=itmIndex)
			mc.textScrollList("attrTSL",e=1,ap=[itmIndex,text],sii=itmIndex)
		
def parentBtn():
	gettargetObj=mc.textFieldButtonGrp('parConTFBG',q=True,tx=True)
	if mc.checkBox('attrbCntrlCB' , q=True,v=True):
		getoptAttrObj=mc.textFieldButtonGrp('sepAttrcTFGB',q=True,tx=True)
	else:
		getoptAttrObj=None
	getparentObjs=mc.textScrollList('parentTSL',q=True,ai=True)
	getparentAttrNames=mc.textScrollList('attrTSL',q=True,ai=True)
	getparMode=mc.radioButtonGrp('parModeRBG' ,q=True,sl=1)
	getparType=mc.radioButtonGrp('parTypeRBG' ,q=True,sl=1)
	getOffset=mc.checkBox('offsetCBG' ,q=True,v=True )
	
	ar_dynParent(gettargetObj,getoptAttrObj,getparentObjs,getparentAttrNames,1,getparMode,getparType,getOffset)


	
