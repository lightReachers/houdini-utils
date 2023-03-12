import hou 
import os
from PySide2 import QtWidgets, QtUiTools, QtCore,QtGui

hou.hscript("setenv PRJPATH = R:/filmServe")
hroot = hou.getenv("PRJPATH")

class showSet(QtWidgets.QWidget):
    def __init__(self):
        super(showSet, self).__init__()
        widgets = hou.qt.mainWindow().children()
        
        for index in widgets:
            try:
                if index.windowTitle() == "VHQ FX - Set Shot":
                    index.setParent(None)
                    index.setWindowFlags(QtCore.Qt.WA_DeleteOnClose)
                    index.close()
                    continue
            except Exception as e:
                pass
        self.env_id = hou.getenv('ENV_ID')
        
        if not self.env_id:
            hou.hscript("setenv ENV_ID = 0")    
        
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load('R:/Library/VHQ_Houdini_Tool/vLib/scripts/python/prjman/ui/shot_env.ui')
        #self.setGeometry(800, 300, 755, 590)
        self.setWindowTitle('VHQ FX - Set Shot')
        #self.setStyleSheet(hou.qt.styleSheet())
        #self.setProperty("houdiniStyle", True)
        
#Fx ui linking        
        self.showBox = self.ui.findChild(QtWidgets.QComboBox, "showBox")
        self.jobPath = self.ui.findChild(QtWidgets.QLabel, "jobPath")
        self.seqBox = self.ui.findChild(QtWidgets.QComboBox, "seqBox")
        self.gaffer_seqBox = self.ui.findChild(QtWidgets.QComboBox, "lgt_seqBox")
        self.shotList = self.ui.findChild(QtWidgets.QListWidget, "shotList")
        self.gaffer_shotList = self.ui.findChild(QtWidgets.QListWidget, "lgt_shotList")
        self.listUser = self.ui.findChild(QtWidgets.QListWidget, "listUser")
        self.gaffer_listUser = self.ui.findChild(QtWidgets.QListWidget, "lgt_listUser")
        self.btnSet = self.ui.findChild(QtWidgets.QPushButton, "pushButton")
        
        self.lineEle = self.ui.findChild(QtWidgets.QLineEdit, "lineElement")
        self.gaffer_lineEle = self.ui.findChild(QtWidgets.QLineEdit, "lgt_lineElement")
        self.listEle = self.ui.findChild(QtWidgets.QListWidget, "listElement")
        self.gaffer_listEle = self.ui.findChild(QtWidgets.QListWidget, "lgt_listElement")
        self.tabAll = self.ui.findChild(QtWidgets.QTabWidget, "tab_all")
#Asset ui linking 
        self.asset_add = self.ui.findChild(QtWidgets.QLineEdit, "lineElem_asset")
        regex=QtCore.QRegExp("[\w]+")
        validator = QtGui.QRegExpValidator(regex)
        self.asset_add.setValidator(validator)
        self.listUser_asset = self.ui.findChild(QtWidgets.QListWidget, "listUser_asset")
        self.listFxElem_asset = self.ui.findChild(QtWidgets.QListWidget, "listWidget_asset")
        #self.imageX = self.ui.findChild(QtWidgets.QFrame, "frame")
        
        #self.imageX.setMinimumSize(755,587)
        #self.imageX.setStyleSheet("background-image: url(C:/Users/fx6/Desktop/ui/bg.png); background-attachment: fixed")
        
 #adding show to QComboBox show Dropdown
        self.btnSet.hide()
        #self.showBox.addItem('Select JOB')
        for dir in os.listdir(hroot):
            #if type(dir.split('_')[0]) is int:
            if dir[:1].isdigit() == True:
                self.showBox.addItem(dir)
        self.showBox.setCurrentText(hou.getenv('HSHOW'))    
        self.getSeq()    
        self.seqBox.setCurrentText(hou.getenv('HSEQ'))
        self.gaffer_seqBox.setCurrentText(hou.getenv('HSEQ'))
        self.getShot()
        self.getShotLgt()
        #self.shotList.setCurrentItem(hou.getenv('HSHOT'))
        self.lineEle.setReadOnly(True)
        self.lineEle.clear()
        self.listFxElem()
 #adding UI           
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.ui)
        self.setLayout(self.mainLayout)
 # Connecting event         
        self.showBox.activated[str].connect(self.getSeq) 
        self.showBox.activated[str].connect(self.listFxElem)
        self.seqBox.activated[str].connect(self.getShot)
        self.gaffer_seqBox.activated[str].connect(self.getShotLgt)
        self.shotList.itemClicked.connect(self.selectShot)
        self.gaffer_shotList.itemClicked.connect(self.selectShotLgt)
        self.listUser.itemClicked.connect(self.getUser)
        self.gaffer_listUser.itemClicked.connect(self.getUserLgt)
        self.connect(self.lineEle, QtCore.SIGNAL('returnPressed()'), self.addElement)
        self.connect(self.gaffer_lineEle, QtCore.SIGNAL('returnPressed()'), self.addElementLgt)
        self.connect(self.asset_add, QtCore.SIGNAL('returnPressed()'), self.addFxElement)
        self.listFxElem_asset.itemClicked.connect(self.selectFxElem)
        self.listUser_asset.itemClicked.connect(self.selectFxUser)
        self.listEle.itemClicked.connect(self.getElem)
        self.gaffer_listEle.itemClicked.connect(self.getElemLgt)
        self.connect(self.btnSet, QtCore.SIGNAL('clicked()'), self.setEnv)
        self.tabAll.currentChanged.connect(self.tabName)
        self.tabAll.currentChanged.connect(self.cStyle)
        
        self.tabAll.setCurrentIndex(int(hou.getenv('ENV_ID')))
        self.tab_id = (int(hou.getenv('ENV_ID')))
        
 ##ASSET SECTION  
    def listFxElem(self):
        self.btnSet.hide()
        self.jobPath.setText('Houdini project path')
        self.listUser_asset.clear()
        self.listFxElem_asset.clear()
        for fxele in os.listdir(self.assetRoot):
            self.listFxElem_asset.addItem(fxele)
            
        
        
        
        
    def tabName(self):
        self.btnSet.hide()
        self.listFxElem()
        self.getShot()
        self.tab_name = self.tabAll.currentIndex()
        if(self.tab_name==0):
            self.tab_id = 0;
        if(self.tab_name==1):
            self.tab_id = 1;
        if(self.tab_name==2):
            self.tab_id = 2;
        print self.tab_id    
        return self.tab_id
            
    def cStyle(self):    
        self.setStyleSheet(hou.qt.styleSheet())
        self.setProperty("houdiniStyle", True)    
    
    
    def addFxElement(self):
        self.btnSet.hide()
        self.listUser_asset.clear()
        self.newFxEle = self.asset_add.text() + '_FxSetup'
        #userPath = userHip  
        self.listFxElem_asset.clear()
        for ele in os.listdir(self.assetRoot):
            self.listFxElem_asset.addItem(ele)
        if self.newFxEle not in os.listdir(self.assetRoot):
            os.makedirs(self.assetRoot + self.newFxEle)    
            self.listFxElem_asset.addItem(self.newFxEle)
            print self.newFxEle + " asset fx element is added to your file"
            self.asset_add.clear()
        else:
            hou.ui.displayMessage("Fx asset element is already available. Please select from fx element list", buttons=('OK', 'Cancel'), default_choice=0, close_choice=1, title="Existing Fx asset element")
            self.asset_add.clear()        

    def selectFxElem(self):
        self.btnSet.hide()
        
        self.fxElem = self.listFxElem_asset.currentItem().text()
        self.assetJob = self.assetRoot + self.fxElem +'/'
        print self.assetJob
        self.listUser_asset.clear()
        self.a_userList = ["Trishit", "Avinash", "Shunmuga", "Jeff", "Vijay", "Himanshu", "Ghost"]
        for a_userItem in self.a_userList:
            self.listUser_asset.addItem(a_userItem)
        if len(os.listdir(self.assetJob)) == 0:
            prj_scene = ["abc", "ass", "audio", "cache", "comp", "desk", "flip", "geo", "hda", "ref", "render", "scenes", "scripts", "sim", "tex", "video", "cam"]
            for folder in prj_scene:
                os.makedirs(self.assetJob + "/" + folder)
        self.lineEle.setReadOnly(True)    
        self.btnSet.hide()
        #print "Now Project is directed to" + " " +self.job
        self.jobPath.setText(self.assetJob)
        return self.assetJob, self.fxElem 
        
    def selectFxUser(self):
        self.assetScene = self.assetJob + 'scenes/'
        self.selectedUser =  self.listUser_asset.currentItem().text()
        return  self.assetScene, self.selectedUser 
        
        
 #Creating function for $JOB, and for seq and shot directories
 
    def getSeq(self):
        self.lineEle.clear()
        self.listUser_asset.clear()
        self.lineEle.setReadOnly(True)
        self.btnSet.hide()
        self.item = self.showBox.currentText()
        print "Project Name :" + " " + self.item
        self.seqPath = hroot + '/' + self.item + '/VFX/sequences'
        self.assetRoot = hroot + '/' + self.item + '/VFX/assets/CGassets/Effects/'
        #self.job = self.seqPath + '/' + 'SC0001/VFX_0001_0001/CG/Effects/Work'
        self.seqBox.clear()
        self.shotList.clear()
        self.listUser.clear()
        self.listEle.clear()
        self.gaffer_seqBox.clear()
        hou.hscript("setenv HSHOW =" + self.item)
        #hou.hscript("setenv JOB =" + self.job)
        #self.jobPath.setText(self.job)
        
        for seq in os.listdir(self.seqPath):
            self.seqBox.addItem(seq)
            self.gaffer_seqBox.addItem(seq)
        
        return self.seqPath, self.assetRoot
        
        
        
          
        
        
        
    def getShot(self):
        #self.seqPath = self.getSeq()
        self.lineEle.clear()
        self.listUser.clear()
        self.seqItem = self.seqBox.currentText()
        self.shotPath = self.seqPath + '/' + self.seqItem
        self.btnSet.hide()
        
        self.lineEle.setReadOnly(True)
        self.shotList.clear()
        self.listEle.clear()
        print self.shotPath
        for shot in os.listdir(self.shotPath):
            self.shotList.addItem(shot)
            
        self.shotList.sortItems()
        
        return self.shotPath
        
    def getShotLgt(self):
        self.gaffer_listUser.clear()
        self.gaffer_lineEle.clear()
        self.lgt_seqItem = self.gaffer_seqBox.currentText()
        self.lgt_shotPath = self.seqPath + '/' + self.lgt_seqItem
        self.btnSet.hide()
        self.gaffer_shotList.clear()
        self.lineEle.setReadOnly(True)
        self.gaffer_lineEle.setReadOnly(True)
        self.gaffer_shotList.clear()
        self.gaffer_listEle.clear()
        for lgt_shot in os.listdir(self.lgt_shotPath):
            self.gaffer_shotList.addItem(lgt_shot)
        self.gaffer_shotList.sortItems()
        return self.lgt_shotPath, self.lgt_seqItem
        
    def selectShot(self):
        self.lineEle.clear()
        self.listEle.clear()
        self.shotItem = self.shotList.currentItem().text()
        #hou.hscript("setenv HSHOT =" + self.shotItem)
        self.job = self.shotPath + '/' + self.shotItem + '/CG/Efx/Work'
        #hou.hscript("setenv JOB =" + self.job)
        self.listUser.clear()
        self.userList = ["Trishit", "Avinash", "Shunmuga", "Jeff", "Vijay", "Himanshu", "Ghost"]
        for userItem in self.userList:
            self.listUser.addItem(userItem)
        if len(os.listdir(self.job)) == 0:
            prj_scene = ["abc", "ass", "audio", "cache", "comp", "desk", "flip", "geo", "hda", "ref", "render", "scenes", "scripts", "sim", "tex", "video", "cam", "data"]
            for folder in prj_scene:
                os.makedirs(self.job + "/" + folder)
        self.lineEle.setReadOnly(True)    
        self.btnSet.hide()
        print "Now Project is directed to" + " " +self.job
        self.jobPath.setText(self.job)
        return self.job
        
    def selectShotLgt(self):
        self.gaffer_lineEle.clear()
        self.gaffer_listEle.clear()
        self.lgt_shotItem = self.gaffer_shotList.currentItem().text()
        #hou.hscript("setenv HSHOT =" + self.shotItem)
        self.lgt_job = self.lgt_shotPath + '/' + self.lgt_shotItem + '/CG/Lighting/local/Light_FX'
        if not os.path.exists(self.lgt_job):
            os.makedirs(self.lgt_job)
        print self.lgt_job    
        #hou.hscript("setenv JOB =" + self.job)
        self.gaffer_listUser.clear()
        self.lgt_userList = ["Rusydi", "Leela", "Sajad", "Ghost"]
        for userItem in self.lgt_userList:
            self.gaffer_listUser.addItem(userItem)
        if len(os.listdir(self.lgt_job)) == 0:
            prj_scene = ["abc", "ass", "audio", "cache", "comp", "desk", "flip", "geo", "hda", "ref", "render", "scenes", "scripts", "sim", "tex", "video", "cam", "data"]
            for folder in prj_scene:
                os.makedirs(self.lgt_job + "/" + folder)
        self.gaffer_lineEle.setReadOnly(True)    
        self.btnSet.hide()
        print "Now Project is directed to" + " " +self.lgt_job
        self.jobPath.setText(self.lgt_job)
        return self.lgt_job, self.lgt_shotItem    
    
    def getUser(self):
        self.btnSet.hide()
        
        self.scenes = self.job + "/" + "scenes"
        self.User = self.listUser.currentItem().text()
        #hou.hscript("setenv HUSER =" + self.User)
        if self.User not in os.listdir(self.scenes):
            os.makedirs(self.scenes + "/" + self.User)
        self.userHip = self.scenes + "/" + self.User    
        self.listEle.clear()
        for ele in os.listdir(self.userHip):
            self.listEle.addItem(ele)
        self.lineEle.setReadOnly(False)
        return self.User, self.userHip
        
    def getUserLgt(self):
        self.btnSet.hide()
        
        self.lgt_scenes = self.lgt_job + "/" + "scenes"
        self.lgt_User = self.gaffer_listUser.currentItem().text()
        #hou.hscript("setenv HUSER =" + self.User)
        if self.lgt_User not in os.listdir(self.lgt_scenes):
            os.makedirs(self.lgt_scenes + "/" + self.lgt_User)
        self.lgt_userHip = self.lgt_scenes + "/" + self.lgt_User    
        self.gaffer_listEle.clear()
        for ele in os.listdir(self.lgt_userHip):
            self.gaffer_listEle.addItem(ele)
        self.gaffer_lineEle.setReadOnly(False)
        return self.lgt_User, self.lgt_userHip    
    
    def addElementLgt(self):
        self.btnSet.hide()
        self.lgt_newEle = self.gaffer_lineEle.text() + '_lgt'
        #userPath = userHip  
        self.gaffer_listEle.clear()
        for lgt_ele in os.listdir(self.lgt_userHip):
            self.gaffer_listEle.addItem(lgt_ele)
        if self.lgt_newEle not in os.listdir(self.lgt_userHip):
            os.makedirs(self.lgt_userHip + "/" + self.lgt_newEle)    
            self.gaffer_listEle.addItem(self.lgt_newEle)
            print self.lgt_newEle + "light element is added to your file"
            self.gaffer_lineEle.clear()
        else:
            hou.ui.displayMessage("Light Element is already available. Please select from element list", buttons=('OK', 'Cancel'), default_choice=0, close_choice=1, title="Existing light element")
            self.gaffer_lineEle.clear()    
        
        
    def addElement(self):
        self.btnSet.hide()
        self.newEle = self.lineEle.text()
        #userPath = userHip  
        self.listEle.clear()
        for ele in os.listdir(self.userHip):
            self.listEle.addItem(ele)
        if self.newEle not in os.listdir(self.userHip):
            os.makedirs(self.userHip + "/" + self.newEle)    
            self.listEle.addItem(self.newEle)
            print self.newEle + " element is added to your file"
            self.lineEle.clear()
        else:
            hou.ui.displayMessage("Element is already available. Please select from element list", buttons=('OK', 'Cancel'), default_choice=0, close_choice=1, title="Existing element")
            self.lineEle.clear()
        
    def getElem(self):
        self.element = self.listEle.currentItem().text()
        print  '-----' + self.element + '-----' + 'is  selected as your file element'
        #hou.hscript("setenv HELEM =" + self.element)
        return self.element
    
    def getElemLgt(self):
        self.lgt_element = self.gaffer_listEle.currentItem().text()
        print  '-----' + self.lgt_element + '-----' + 'is  selected as your file element'
        #hou.hscript("setenv HELEM =" + self.element)
        return self.lgt_element    
        
    
    def setEnv(self):
        self.value = self.tab_id
        hou.hscript("setenv ENV_ID =" + str(self.value))
        #self.tabName()
        if self.value == 0:
            #print "this is 0"
            hou.hscript("setenv HUSER =" + self.User)
            hou.hscript("setenv HELEM =" + self.element)
            self.shotItem = self.shotList.currentItem().text()
            hou.hscript("setenv HSHOT =" + self.shotItem)
            self.job = self.shotPath + '/' + self.shotItem + '/CG/Efx/Work'
            hou.hscript("setenv JOB =" + self.job)
            show = hou.getenv("HSHOW").split('_')[2]
            filename = show + '_' + hou.getenv('HSHOT') + '_' + hou.getenv('HELEM') + '_v001_r001'
            hou.hscript("setenv HIPNAME =" + filename)
            hou.hscript("setenv HSEQ =" + self.seqBox.currentText())
            self.btnSet.show()
            hou.hipFile.setName(hou.getenv("HIPNAME"))
            hou.hscript(
                "setenv HIP =" + hou.getenv('JOB') + "/scenes/" + hou.getenv('HUSER') + '/' + hou.getenv('HELEM'))
            hou.hscript("setenv HIPFILE =" + hou.getenv('HIP') + '/' + hou.getenv("HIPNAME") + '.hip')
            shotData = [hou.getenv('ENV_ID'), hou.getenv('HSHOW'), hou.getenv('HSEQ'), hou.getenv('HSHOT'),
                        hou.getenv('HUSER'), hou.getenv('HELEM'), hou.getenv('JOB')]
            userdir = os.getenv('HOME')
            setshotpath = userdir + "/houdini16.0/setshot1.txt"
            outF = open(setshotpath, 'w')
            if os.path.isfile(setshotpath):
                for line in shotData:
                    outF.write(line)
                    outF.write("\n")
                outF.close()
            self.close()
        if self.value == 1:
            #print "this is 1"
            if self.selectedUser not in os.listdir(self.assetScene):
                os.makedirs(self.assetScene + self.selectedUser)
            hou.hscript("setenv HUSER =" + self.selectedUser)
            hou.hscript("setenv JOB =" + self.assetJob)
            hou.hscript("setenv HELEM =" + self.fxElem)
            show = hou.getenv("HSHOW").split('_')[2]
            assetFilePath = self.assetScene + self.selectedUser + '/'
            assetFile = show + '_'  + hou.getenv('HELEM') + '_v001_r001'
            hou.hscript("setenv HIPNAME =" + assetFile)
            hou.hipFile.setName(hou.getenv("HIPNAME"))
            hou.hscript("setenv HIP =" + assetFilePath)
            hou.hscript("setenv HIPFILE =" + hou.getenv('HIP') + '/' + hou.getenv("HIPNAME") + '.hip')
            shotData = [hou.getenv('ENV_ID'), hou.getenv('HSHOW'), hou.getenv('HUSER'), hou.getenv('HELEM'), hou.getenv('JOB')]
            userdir = os.getenv('HOME')
            setshotpath = userdir + "/houdini16.0/setshot1.txt"
            outF = open(setshotpath, 'w')
            if os.path.isfile(setshotpath):
                for line in shotData:
                    outF.write(line)
                    outF.write("\n")
                outF.close()
            self.close()
            
        if self.value == 2:
            #print "this is 2"
            hou.hscript("setenv HUSER =" + self.lgt_User)
            hou.hscript("setenv HELEM =" + self.lgt_element)
            #self.shotItem = self.shotList.currentItem().text()
            hou.hscript("setenv HSHOT =" + self.lgt_shotItem)
            #self.job = self.shotPath + '/' + self.shotItem + '/CG/Efx/Work'
            hou.hscript("setenv JOB =" + self.lgt_job)
            show = hou.getenv("HSHOW").split('_')[2]
            filename = show + '_' + hou.getenv('HSHOT') + '_' + hou.getenv('HELEM') + '_v001_r001'
            hou.hscript("setenv HIPNAME =" + filename)
            hou.hscript("setenv HSEQ =" + self.lgt_seqItem)
            self.btnSet.show()
            hou.hipFile.setName(hou.getenv("HIPNAME"))
            hou.hscript("setenv HIP =" + hou.getenv('JOB') + "/scenes/" + hou.getenv('HUSER') + '/' + hou.getenv('HELEM'))
            hou.hscript("setenv HIPFILE =" + hou.getenv('HIP') + '/' + hou.getenv("HIPNAME") + '.hip')
            shotData = [hou.getenv('ENV_ID'), hou.getenv('HSHOW'), hou.getenv('HSEQ'), hou.getenv('HSHOT'),
                        hou.getenv('HUSER'), hou.getenv('HELEM'), hou.getenv('JOB')]
            userdir = os.getenv('HOME')
            setshotpath = userdir + "/houdini16.0/setshot1.txt"
            outF = open(setshotpath, 'w')
            if os.path.isfile(setshotpath):
                for line in shotData:
                    outF.write(line)
                    outF.write("\n")
                outF.close()   
  
            self.close()        
dialog = showSet()
dialog.show() 
                
        
        
      
            
        
 
