import pymel.core as pm

def createFK_heirarchy(start_jnt, limb_name=None):
    child_jnts = pm.ls(start_jnt,dag=1,type="joint")[:-1]
    limp_index = 1
    ctrl_grps = []
    for child_jnt in child_jnts:
        name = child_jnt.name().split("_")[0]
        if limb_name:
            name = "%s%s" % (limb_name, limp_index)
        
        ctrl = pm.circle(n="Ctrl_%s" % name,nr=(1,0,0),r=1,ch=0)
        sdkgrp = pm.group(ctrl,n="%s_sdk" % name)
        grp = pm.group(sdkgrp,n="Grp_%s" % name)
        pm.delete(pm.parentConstraint(child_jnt, grp))        
        pm.parentConstraint(ctrl, child_jnt)
        parent_jnt = child_jnt.getParent()
        if parent_jnt:
            pm.parentConstraint(parent_jnt, grp,mo=1)
        limp_index = limp_index+1
        ctrl_grps.append(grp)
    if ctrl_grps:
        main_grp_name = "Grp_%s" % limb_name
        pm.group(ctrl_grps, name=main_grp_name)

    return main_grp_name