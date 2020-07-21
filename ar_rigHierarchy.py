                                            #--------------------------------------------------------------#
                                            # 	DESCRIPTION	: Python Module for Rig Hierarachy SetUp       #	 																		   
                                            # 	AUTHOR 			: Arun . S - arunpillaii@gmail.com             #                    												                       				                     
                                            # 	VERSION			: 1.00 , 03 June 2010			                     #
                                            #								: 2.00 , 21 June 2011													 #
                                            #   Copyright (C) 2011.  All rights reserved.									 #
                                            #--------------------------------------------------------------#

# imports!!
import maya.cmds as mc
import ar_rigTools as tools
import sk_ctrlCurves as scc
import datetime as dt

def ar_rigHierarchy(characterName,Details,charScale=1):
    grpGeo = 'GEO'
    #main groups
    mainGrp = mc.group(n=characterName , em=True)
    mc.addAttr(mainGrp , ln='DisplayType' , at='enum' , en='Normal:Template:Reference:',k=False)
    mc.setAttr(mainGrp + '.DisplayType',e=True,cb=True)
    mc.addAttr(mainGrp,ln='Textures',at='bool',k=False)
    mc.setAttr(mainGrp + '.Textures',1,e=True,cb=True)
    
    rigGrp = mc.group(n='RIG' , em=True , p=mainGrp)
    sysGrp = mc.group(n='Systems' , em=True , p=rigGrp)
    modelGrp = mc.group(n='MODELS' , em=True , p=mainGrp)
    
    mc.connectAttr(mainGrp + '.DisplayType', modelGrp+ '.overrideDisplayType')
    mc.connectAttr(mainGrp + '.Textures', modelGrp+ '.overrideTexturing') 
    mc.setAttr(modelGrp+ '.overrideEnabled',1,l=True)
    if mc.objExists(grpGeo):
        mc.parent(grpGeo , modelGrp)
    centerGrp = mc.group(n='CENTER' , em=True)
    for grp in [mainGrp,rigGrp,sysGrp,modelGrp]:
        tools.lockhide(grp,('v'))
    
    #Place and Root Controls
    place,root = 'Ctrl_PLACE' , 'Ctrl_ROOT'
    #ROOT
    inst = scc.Ctrlcircle(root,(1.3*charScale),[0,1,0])
    inst.doubleshape(1.03)
    mc.addAttr(root,ln="GeoVis",at='bool',k=False)
    mc.setAttr(root + '.GeoVis',1,e=True,cb=True)
    mc.addAttr(root,ln="ControlVis",at='bool',k=False)
    mc.setAttr(root + '.ControlVis',1,e=True,cb=True)
    mc.addAttr(root , ln='Display' , at='enum' , en='Proxy:Mid:High:',k=False)
    mc.setAttr(root + '.Display',e=True,cb=True)
    
    mc.connectAttr(root + '.GeoVis' ,modelGrp + '.v')
    mc.setAttr(modelGrp + '.v',l=True)
    mc.connectAttr(root + '.ControlVis' ,centerGrp + '.v')
    mc.setAttr(centerGrp + '.v',l=True)

    #PLACE
    inst = scc.Ctrlcircle(place,(1.1*charScale),[0,1,0])
    mc.setAttr(root + '.v' , k=False ,  l=True, cb=False)
    mc.setAttr(place + '.v' , k=False , l=True, cb=False)
    
    mc.parent(root,rigGrp)
    mc.parent(place ,root)
    mc.parent(centerGrp,place)
    
    #creating utility for global scale
    rootPlaceMD = mc.createNode('multiplyDivide' , n='RootPlace_MD')
    mc.setAttr(rootPlaceMD + '.operation' , 1)
    mc.connectAttr(root + '.scale' , rootPlaceMD + '.input1')
    mc.connectAttr(place + '.scale' , rootPlaceMD + '.input2')
    querypScaleMD = mc.ls('pScale*' , type='multiplyDivide')				# Connecting to global scale
    for each in querypScaleMD:
        mc.connectAttr((rootPlaceMD + '.outputX') , (each + '.input2X'))
        
    #Quick Selection sets
    mc.sets([place,root], t='gCharacterSet', name=('Main_Sets'))
    allSets = mc.ls('*_Sets')
    mc.sets(allSets , n='Select_Controls')

    #Adding to Systems and Main Group	
    if mc.objExists('Root_CJ'):
        mc.delete(mc.parentConstraint('Root_CJ',centerGrp))
        mc.addAttr(sysGrp , ln='Skeleton_CJ' , at='bool', k=True , h=False)
        mc.setAttr((sysGrp + '.Skeleton_CJ'), 0 , k=False , cb=True)
        mc.connectAttr((sysGrp + '.Skeleton_CJ') , ('Root_CJ.v'))

    querypSys = mc.ls('Sys_*' , assemblies=True)
    for sys in querypSys:
        mc.addAttr(sysGrp , ln=sys[4:] , at='bool', k=True , h=False)
        mc.setAttr((sysGrp + '.%s' % sys[4:]), 0 , k=False , cb=True)
        mc.connectAttr((sysGrp + '.%s' % sys[4:]), (sys + '.v'))
        mc.parent(sys , sysGrp)
    
    getGrp = mc.ls('Grp_*' , assemblies=True)
    mc.parent(getGrp ,centerGrp )
    
    #Assigning color to controls
    set_colors()
    
    #Adding Details
    mc.addAttr(mainGrp , ln='CharacterName' , dt='string')
    mc.setAttr((mainGrp + '.CharacterName') , Details[0] , type='string', l=True)
    mc.addAttr(mainGrp , ln='RigBy' , dt='string')
    mc.setAttr((mainGrp + '.RigBy') , Details[1],type='string', l=True)
    mc.addAttr(mainGrp , ln='RiggedOn' , dt='string')
    mc.setAttr((mainGrp + '.RiggedOn') , (dt.date.today()),type='string', l=True)
    
    #return
    return mainGrp


def set_colors():
    controls = mc.ls('Ctrl_*','*AnnotationShape' , typ=['nurbsCurve','annotationShape'])
    for cntrl in controls:
        try:
            if 'Left' in cntrl:
                mc.setAttr(cntrl + '.drawOverride.overrideColor',6)
            elif 'Right' in cntrl:
                mc.setAttr(cntrl + '.drawOverride.overrideColor',13)
            else:
                mc.setAttr(cntrl + '.drawOverride.overrideColor',22)
            mc.setAttr(cntrl + '.overrideEnabled', 1,l=True)
        except:
            continue


#**************************************************END**************************************************#
