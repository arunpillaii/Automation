import maya.cmds as mc
import ar_rigTools as tools
import sk_ctrlCurves as scc


def rig_eye(const_grp=None, parent_grp=None, ctrl_postion=1, chrScale=1, aim_object=None):

	#Eyes Rig
    eyeJnts = mc.ls('*Eye_CJ')
    cntrlEye = 'Ctrl_Eye'
    EyeCntrls = [cntrlEye]
    inst = scc.Ctrlcircle(cntrlEye ,(.55*chrScale) , (0,0,1))
    inst.circsquare()
    mc.setAttr((cntrlEye + '.sx') , .2)
    mc.makeIdentity(cntrlEye ,apply = True)
    eyeMainGrp = mc.group(cntrlEye , n = 'Grp_Eye')
    mc.delete(mc.parentConstraint(eyeJnts[0] , eyeMainGrp , st = 'x'))
    mc.setAttr(eyeMainGrp + '.tz' , (ctrl_postion*chrScale))
    
    if const_grp and mc.objExists(const_grp):
        mc.parentConstraint(const_grp , eyeMainGrp , mo = True)
    
    if const_grp and mc.objExists(parent_grp):
        mc.parent(eyeMainGrp , parent_grp)
    
    for jnt in eyeJnts:
        ctrlName = 'Ctrl_%s' % jnt.split('_')[0]
        circMain = mc.circle(name = ctrlName, c = (0,0,0), nr = (1,0,0), sw = 360, ch = 0 , r = .039)
        circ1 = mc.circle(name = ctrlName , c = (0,0,0), nr = (0,1,0), sw = 360, ch = 0 , r = .039)
        circ2 = mc.circle(name = ctrlName , c = (0,0,0), nr = (0,0,1), sw = 360, ch = 0 , r = .039)
        mc.parent(mc.listRelatives(circ1[0], c = 1 , s = 1)[0],mc.listRelatives(circ2[0], c = 1 , s = 1)[0],circMain[0],r = 1 , s = 1)
        eyeGrp = mc.group(ctrlName , n = ('Grp_%s' % jnt.split('_')[0]))
        mc.delete(circ1[0],circ2[0],mc.parentConstraint(jnt , eyeGrp))
        mc.setAttr(eyeGrp + '.tz' , (ctrl_postion*chrScale))
        mc.parent(eyeGrp , cntrlEye)
        mc.aimConstraint(ctrlName , jnt ,  mo  = 1 , w  = 1 , aim = (0,0,1) , u = (0,1,0) , wut = 'object' , wuo = aim_object)
        EyeCntrls.append(ctrlName)
    for cntrl in EyeCntrls:
        tools.lockhide(cntrl,('tx', 'ty', 'tz'))
    
    mc.sets(EyeCntrls , n = 'Eye_Sets' , t = 'gCharacterSet')
    return EyeCntrls