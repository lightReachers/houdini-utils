import hou
import os
from xml.dom.minidom import parse
import xml.dom.minidom
import glob
hroot = hou.getenv("PRJPATH")
cgPublishPath = hroot + '/' + hou.getenv('HSHOW') + '/VFX/sequences/' + hou.getenv('HSEQ') + '/' + hou.getenv('HSHOT') + '/CG/'
animPublishPath = cgPublishPath + 'Animation/publish/'
layPublishPath = cgPublishPath + 'Layout/publish/'
matchPublishPath = cgPublishPath + 'Matchmove/publish/'
xml_list = glob.glob(matchPublishPath + '*xml')
xml_list_anim = glob.glob(animPublishPath + '*xml')
xml_list_lay = glob.glob(layPublishPath + '*xml')
if len(xml_list)==0:
    try:
        xmlPath = max(xml_list_anim, key=os.path.getctime)
    except:
        xmlPath = max(xml_list_lay, key=os.path.getctime)
if len(xml_list)>0:
    xmlPath = max(xml_list, key=os.path.getctime)


def build():
    currentNode = hou.node(hou.pwd().path());
    for kid in currentNode.children():
        kid.parm('viewportlod').set(currentNode.parm('viewportLod').eval());
        kid.parm('buildHierarchy').pressButton();

    #print xmlPath
    if os.path.exists(xmlPath) == 0:
        hou.ui.displayMessage("Current shot does not have published xml file.Enter camera resolution manually.",
                              buttons=('OK', "kill it"), default_choice=0, close_choice=1,
                              title="Not published!!")
    else:
        DOMTree = xml.dom.minidom.parse(xmlPath)
        root = DOMTree.documentElement
        resolutionCam = root.getElementsByTagName("CommonRenderSetting")[0]
        rHeight = int(resolutionCam.getAttribute('height'))
        rWidth = int(resolutionCam.getAttribute('width'))
        imageplane = root.getElementsByTagName("imagePlane")
        #print(len(imageplane))
        if len(imageplane) > 0:
            imagePathRaw = imageplane[0].getAttribute('imageName')
            imagePathL = imagePathRaw.split('.')
			
            try:
                imagePathM = imagePathL[0] + '*.' + imagePathL[2]
                imagePath = imagePathL[0] + '.$F' + str(len(imagePathL[1])) + '.' + imagePathL[2]
            except:
                frameNumber = imagePathL[0][imagePathL[0].rfind("_")+1:]
                fore = imagePathL[0][:imagePathL[0].rfind("_")]
				
                imagePath = fore + '_$F' + str(len(frameNumber)) + '.' + imagePathL[1]
                imagePathM = fore + '*.' + imagePathL[1]
				
            image = True
        else:
            print("Image sequence not available.")
            image = False
        for childCam in currentNode.allSubChildren():
            if childCam.type().name() == 'cam':
                childCam.parm('resx').set(rWidth)
                childCam.parm('resy').set(rHeight)
                if(image==True):
                    childCam.parm('vm_background').set(imagePath)
            if childCam.type().name() == 'alembic':

                name = childCam.parent().parent().name()
                name = name[:name.rfind(".")]

                assetName = 'OUT_' + childCam.parent().parent().name() # abc name

                parentNode = childCam.parent().path()


                unpack = hou.node(parentNode).createNode('unpack')
                unpack.setInput(0, childCam)
                unpack.parm('transfer_attributes').set('path')

                convert = hou.node(parentNode).createNode('convert')
                convert.setInput(0, unpack)

                bgeonull = hou.node(parentNode).createNode('null', 'OUT_' + name)
                bgeonull.setInput(0, convert)

                currentNode = bgeonull
                path = "/" + currentNode.name()

                while True:
                    if (currentNode.parent().type().name() == "obj"):
                        path = "/obj" + path
                        break
                    else:
                        currentNode = currentNode.parent()
                        path = "/" + currentNode.name() + path

                outpath = path[:path.rfind("/")]
                outname = bgeonull.name()[bgeonull.name().find("_") + 1:] + '.bgeo_' + hou.getenv("HUSER")
                newpath = hou.getenv('JOB')
                newpath = 'F' + newpath[newpath.rfind(":"):]

                vhqinout = hou.node(parentNode).createNode('vhq_in_out', outname)
                vhqinout.setInput(0, bgeonull)

                vhqinout.parm('folders1').set(1)
                vhqinout.parm('switch').set(1)
                vhqinout.parm('read').set(0)
                vhqinout.parm('trange').set(1)
                vhqinout.parm('fdrive').set(newpath + "/cache/$OS/`chs('vers')`/$OS.$F4.bgeo.sc")
                vhqinout.parm('rdrive').set("$JOB/cache/$OS/`chs('vers')`/$OS.$F4.bgeo.sc")
                vhqinout.parm('sopoutput_bgeo').set(newpath + "/cache/$OS/`chs('vers')`/$OS.$F4.bgeo.sc")

                outpos = hou.Vector2((0.0, 0.0))
                outpos[0] = bgeonull.position().x()
                outpos[1] = bgeonull.position().y() - 1.2

                bgeonull.setColor(hou.Color(0.1024, 0.30476, 0))

                vhqinout.setUserData("nodeshape", "circle")
                vhqinout.setColor(hou.Color(0.0, 0.0, 0.545098))

                vhqinout.setPosition(outpos)

                outnull = hou.node(parentNode).createNode('null', 'OUT_' + outname)
                outnull.setInput(0, vhqinout)

                # For render farm
                vhqinout_farm = hou.node("/out").createNode('geometry', outname, 0)
                vhqinout_farm.moveToGoodPosition()
                vhqinout_farm.parm('soppath').set(path)
                vhqinout_farm.parm('sopoutput').set('`chs("../..' + outpath + '/' + outname + '/sopoutput_bgeo")`')
                vhqinout_farm.parm('trange').set(vhqinout.parm('trange'))
                vhqinout_farm.parm('f1').set(vhqinout.parm('f1'))
                vhqinout_farm.parm('f2').set(vhqinout.parm('f2'))
                vhqinout_farm.parm('f3').set(vhqinout.parm('f3'))
                vhqinout_farm.parm('take').set(vhqinout.parm('take'))

                hou.node(parentNode).layoutChildren(horizontal_spacing=-1.0, vertical_spacing=-1.0)

                abcnull = hou.node(parentNode).createNode('null', assetName)
                abcnull.setInput(0, childCam)

                outpos = hou.Vector2((0.0, 0.0))
                outpos[0] = abcnull.position().x() + 4
                outpos[1] = abcnull.position().y() - 1.2

                abcnull.setPosition(outpos)
                abcnull.setDisplayFlag(1)
        
