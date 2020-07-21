import maya.cmds as mc
def addEyeAnnote():
	if mc.objExists('Ctrl_Eye'):
		gGrp='Grp_EyeAnn'
		if mc.objExists(gGrp):
			mc.delete(gGrp)
		for each in ['Left','Right']:
			if mc.objExists('Ctrl_%sEye' % each) and mc.objExists('%sEye_CJ' % each):
				stLoc=mc.spaceLocator(n='%sEyeSt_Loc' % each)
				mc.setAttr(mc.listRelatives(stLoc[0],s=1,c=1)[0]+'.v',0)
				edLoc=mc.spaceLocator(n='%sEyeEd_Loc' % each)
				mc.setAttr(mc.listRelatives(edLoc[0],s=1,c=1)[0]+'.v',0)
				annShape=mc.annotate(edLoc[0], tx='')
				mc.setAttr(annShape+'.template',1,l=1)
				ann=mc.listRelatives(annShape,p=1)[0]
				mc.parent(annShape,stLoc[0],r=1,s=1)
				mc.delete(ann)
				mc.pointConstraint('%sEye_CJ' % each,stLoc[0])
				mc.pointConstraint('Ctrl_%sEye' % each,edLoc[0])
				mainGrp=mc.group(n='Grp_%sEyeAnn' % each,em=1)
				mc.parent(stLoc[0],edLoc[0],mainGrp)
				if not mc.objExists(gGrp):
					mc.group(n=gGrp,em=1,p='Grp_Eye')
				mc.parent(mainGrp,gGrp)
			
		if not mc.listAttr('Ctrl_Eye.Annotation'):		
			mc.addAttr('Ctrl_Eye',ln='Annotation',at='bool')
			mc.setAttr('Ctrl_Eye.Annotation',e=1,cb=1)
	mc.connectAttr('Ctrl_Eye.Annotation',gGrp+'.v')	
