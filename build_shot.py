import os
import subprocess
from PySide2 import QtWidgets, QtUiTools, QtCore
from xml.dom.minidom import parse
import xml.dom.minidom

hou.hscript("setenv PRJPATH = R:/filmServe")
hroot = hou.getenv("PRJPATH")

tab_id = int(hou.getenv('ENV_ID'))
if tab_id == 1:
    k = hou.ui.displayMessage("Shot Build tool not available for Asset File Build", buttons=('OK', 'Cancel'), default_choice=0, close_choice=1, title="Do manual build for Asset file !")   
else:
        cgPublishPath = hroot + '/' + hou.getenv('HSHOW') + '/VFX/sequences/' + hou.getenv('HSEQ') + '/' + hou.getenv('HSHOT') + '/CG/'
        animPublishPath = cgPublishPath + 'Animation/publish/'
        layPublishPath = cgPublishPath + 'Layout/publish/'
        matchPublishPath = cgPublishPath + 'MatchMove/publish/'
        #print hou.getenv("HSHOW").split('_')[2]
        

        #setting Frame range from machmove punlish xml   
        xmlPath = matchPublishPath + hou.getenv("HSHOW").split('_')[2] +'_' + hou.getenv("HSHOT") + '_trk.xml'
        xmlPath_anim = animPublishPath +hou.getenv("HSHOW").split('_')[2] +'_' + hou.getenv("HSHOT") + '_anim.xml'
        print xmlPath
        if os.path.isfile(xmlPath)==0 and os.path.isfile(xmlPath_anim)==0:
            perror = hou.ui.displayMessage("Shot is not publish", buttons=('OK', 'Cancel'), default_choice=0, close_choice=1, title="Not Publish!")
        else:
            if os.path.isfile(xmlPath)==0:
                xmlPath = xmlPath_anim
            DOMTree = xml.dom.minidom.parse(xmlPath)
            root = DOMTree.documentElement
            resolutionCam = root.getElementsByTagName("CommonRenderSetting")[0]
            rHeight = int(resolutionCam.getAttribute('height'))
            rWidth = int(resolutionCam.getAttribute('width'))
            imageplane = root.getElementsByTagName("imagePlane")
            print len(imageplane)
            if len(imageplane)==0:
                print("Image sequence not available.")
            else:
                
                imagePathRaw = imageplane[0].getAttribute('imageName')
                imagePathL = imagePathRaw.split('.')
                print imagePathL
                imagePath = imagePathL[0] + '.$F' + str(len(imagePathL[1])) + '.' + imagePathL[2]
                imagePathM = imagePathL[0] + '*.' + imagePathL[2]

        class buildScene(QtWidgets.QWidget):
                def __init__(self):
                        super(buildScene, self).__init__()
                        widgets = hou.qt.mainWindow().children()
                        for index in widgets:
                                        try:
                                                if index.windowTitle() == "REAPER - SHOT BUILD":
                                                        index.setParent(None)
                                                        index.setWindowFlags(QtCore.Qt.WA_DeleteOnClose)
                                                        index.close()
                                                        continue
                                        except Exception as e:
                                                pass
        
                        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
                        loader = QtUiTools.QUiLoader()
                        self.ui = loader.load('R:/Library/VHQ_Houdini_Tool/vLib/scripts/python/prjman/ui/shotBuild.ui')
                        self.setGeometry(550, 300, 881, 450)
                        self.setWindowTitle("REAPER - SHOT BUILD")
                        self.setStyleSheet(hou.qt.styleSheet())
                        self.setProperty("houdiniStyle", True)
        
        
                        self.animList = self.ui.findChild(QtWidgets.QListWidget, "anim")
                        self.layList = self.ui.findChild(QtWidgets.QListWidget, "layout")
                        self.matchList = self.ui.findChild(QtWidgets.QListWidget, "matchmove")
                        self.btnShotBuild = self.ui.findChild(QtWidgets.QPushButton, "shotBuild")
                        self.btnAnimExp = self.ui.findChild(QtWidgets.QPushButton, "e_anim")
                        self.btnLayExp = self.ui.findChild(QtWidgets.QPushButton, "e_lay")
                        self.btnMatchExp = self.ui.findChild(QtWidgets.QPushButton, "e_match")
                        self.btnPreLayout = self.ui.findChild(QtWidgets.QPushButton, "view_layout")
                        self.frameSet = self.ui.findChild(QtWidgets.QCheckBox, "frame_range")
        
        
                        self.mainLayout = QtWidgets.QVBoxLayout()
                        self.mainLayout.addWidget(self.ui)
                        self.setLayout(self.mainLayout)
        
        
        
                        #self.userList.itemClicked.connect(self.getElem)
                        #self.elemList.itemClicked.connect(self.getHip)
                        self.connect(self.btnShotBuild, QtCore.SIGNAL('clicked()'), self.shotBuild)
                        self.connect(self.btnAnimExp, QtCore.SIGNAL('clicked()'), self.openAnim)
                        self.connect(self.btnLayExp, QtCore.SIGNAL('clicked()'), self.openLay)
                        self.connect(self.btnMatchExp, QtCore.SIGNAL('clicked()'), self.openMatch)
                        self.connect(self.btnPreLayout, QtCore.SIGNAL('clicked()'), self.l_preview)
        
                        
        
        
                        for abcLay in os.listdir(layPublishPath):
                                if abcLay.endswith('.abc'):
                                        self.layList.addItem(abcLay)
                
                        for abcAnim in os.listdir(animPublishPath):
                                if abcAnim.endswith('.abc'):
                                        self.animList.addItem(abcAnim) 
                
                
                        for abcMatch in os.listdir(matchPublishPath):
                                if abcMatch.endswith('.abc'):
                                        self.matchList.addItem(abcMatch) 
                
                def openAnim(self):
                                pathAnim = os.path.normpath(animPublishPath)
                                subprocess.Popen('explorer' + ' ' + pathAnim)
            
                def openLay(self):
                                pathLay = os.path.normpath(layPublishPath)
                                subprocess.Popen('explorer' + ' ' + pathLay)        
                       
                def openMatch(self):
                                pathMatch = os.path.normpath(matchPublishPath)
                                subprocess.Popen('explorer' + ' ' + pathMatch) 
            
            
                def l_preview(self):
                        preview_path = matchPublishPath + hou.getenv("HSHOW").split('_')[2] +'_' + hou.getenv("HSHOT") + '_trk.mov'
                        preview_path_anim = animPublishPath +hou.getenv("HSHOW").split('_')[2] +'_' + hou.getenv("HSHOT") + '_anim.mov'
                        #print preview_path
                        if os.path.isfile(preview_path)==1:
                                os.system("start "+preview_path)
                        if os.path.isfile(preview_path_anim)==1: 
                                os.system("start "+preview_path_anim)
                                
                        else:
                                ip = hou.expandString('$HB/mplay')
                                subprocess.Popen([ip, imagePathM])
            
            
                
                
                def shotBuild(self):
        
        
                        assetNodeName = 'APKG_' + hou.getenv('HSHOT') + '_import'
                        assetNode = hou.node('/obj').createNode('subnet', assetNodeName)
                        assetNode.setUserData('nodeshape', 'tabbed_left')
                        assetNode.setColor(hou.Color((.98, .275, .275)))
                        asset_path = assetNode.path()
        
        
        
                        if len(self.layList.selectedItems()) > 0:
                                for abcLaySelected in self.layList.selectedItems():
                                        alembicPath = layPublishPath + '/' + abcLaySelected.text()
                                        #print alembicPath
                                        p = assetNode.createNode('alembicarchive', abcLaySelected.text() + '_Layout')
                                        p.parm('fileName').set(alembicPath)
                                        p.parm('buildSubnet').set(0)
                                        p.parm('buildSingleGeoNode').set(1)
                                        p.parm('viewportlod').set(2)
                                        p.parm('buildHierarchy').pressButton()
                                        p.moveToGoodPosition()
                
                        if len(self.matchList.selectedItems()) > 0:
                                for abcMatchSelected in self.matchList.selectedItems():
                                        alembicPath = matchPublishPath + '/' + abcMatchSelected.text()
                                        #print alembicPath
                                        p = assetNode.createNode('alembicarchive', abcMatchSelected.text() + '_Matchmove')
                                        p.parm('fileName').set(alembicPath)
                                        p.parm('buildSubnet').set(0)
                                        p.parm('buildSingleGeoNode').set(1)
                                        p.parm('viewportlod').set(2)
                                        p.parm('buildHierarchy').pressButton()
                                        p.moveToGoodPosition()
                
                        if len(self.animList.selectedItems()) > 0:
                                for abcAnimSelected in self.animList.selectedItems():
                                        alembicPath = animPublishPath + '/' + abcAnimSelected.text()
                                        #print alembicPath
                                        p = assetNode.createNode('alembicarchive', abcAnimSelected.text() + '_Animation')
                                        p.parm('fileName').set(alembicPath)
                                        p.parm('buildSubnet').set(0)
                                        p.parm('buildSingleGeoNode').set(1)
                                        p.parm('viewportlod').set(2)
                                        p.parm('buildHierarchy').pressButton()
                                        p.moveToGoodPosition()
        
                        assetNode.layoutChildren(horizontal_spacing=-1.0, vertical_spacing=-1.0)
        
                        #print rHeight, rWidth
                        for childCam in assetNode.allSubChildren():
                                if childCam.type().name() == 'cam':
                                        childCam.parm('resx').set(rWidth)
                                        childCam.parm('resy').set(rHeight)
                                        try:
                                            childCam.parm('vm_background').set(imagePath)
                                        except:
                                            pass
        
        
                        
                        if self.frameSet.isChecked() == True:
            

                                timeRange = root.getElementsByTagName("TimeRange")[0]
                                startFrame = float(timeRange.getAttribute('start'))
                                endFrame = float(timeRange.getAttribute('end'))

                                setGobalFrangeExpr = 'tset `(%d-1)/$FPS` `%d/$FPS`' % (startFrame, endFrame)

                                hou.hscript(setGobalFrangeExpr)
                                hou.playbar.setPlaybackRange(startFrame, endFrame)
                                hou.setFrame(startFrame)
        
                        #adding Build UI
                        parm_group = assetNode.parmTemplateGroup()
                        parm_group.hideFolder('Transform', True)
                        parm_group.hideFolder('Subnet', True)
                        parm_folder = hou.FolderParmTemplate('folder', 'Build Scene')
                        build_btn = hou.ButtonParmTemplate('build', 'Alembic Scene Build') 
                        build_btn.setTags({"script_callback": "import reaper.assetPkg; reload(reaper.assetPkg); reaper.assetPkg.build();", "script_callback_language": "python"})
                        parm_folder.addParmTemplate(build_btn)
                        parm_folder.addParmTemplate(hou.MenuParmTemplate("viewportLod", "Dispaly As", "01234", ( "Full Geometry", "Point Cloud", "Bounding Box", "Centroid","Hidden" ), 2))
                        parm_group.append(parm_folder)
                        assetNode.setParmTemplateGroup(parm_group)
                        #del imagePath
                        dialog.close()
        dialog = buildScene()
        dialog.show()
