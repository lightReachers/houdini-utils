import os
import sys
import shutil
from PySide2 import QtWidgets, QtUiTools, QtCore, QtGui

hou.hscript("setenv PRJPATH = R:/filmServe")
hroot = hou.getenv("PRJPATH")
fileRoot = hou.getenv('JOB') + 'scenes/' 
#print fileRoot

def switch (user):
    return {
        'FX4' : 'Jeff',
        'fx5' : 'Vijay',
        'fx2' : 'Avinash',
        'FX6' : 'Himanshu',
        'fx1' : 'Trishit'
    }[user]


class openFile(QtWidgets.QWidget):
    def __init__(self):
        super(openFile, self).__init__()
        widgets = hou.qt.mainWindow().children()
        for index in widgets:
                try:
                    if index.windowTitle() == 'VHQ FX - Open File':
                        index.setParent(None)
                        index.setWindowFlags(QtCore.Qt.WA_DeleteOnClose)
                        index.close()
                        continue
                except Exception as e:
                    pass
        
        
        
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load('R:/Library/VHQ_Houdini_Tool/vLib/scripts/python/prjman/ui/vhq_open2.ui')
        self.setGeometry(550, 300, 1120, 600)
        self.setWindowTitle('VHQ FX - Open File')
        #self.setStyleSheet(hou.qt.styleSheet())
        #self.setProperty("houdiniStyle", True)
        
        
#        self.userList = self.ui.findChild(QtWidgets.QListWidget, "listUser")
#        self.elemList = self.ui.findChild(QtWidgets.QListWidget, "listElement")
#        self.fileList = self.ui.findChild(QtWidgets.QListWidget, "listFile")
        self.btnSetOpen = self.ui.findChild(QtWidgets.QPushButton, "btnOpen")
        self.tabs = self.ui.findChild(QtWidgets.QTabWidget, "tab_open") 
        self.hipFile = self.ui.findChild( QtWidgets.QTreeView, "tree_asset" )
        self.hipFileWork = self.ui.findChild( QtWidgets.QTreeView, "tree_work" )
        self.elemListAsset = self.ui.findChild( QtWidgets.QListWidget, "list_elemAsset" )
        self.userListWork = self.ui.findChild( QtWidgets.QListWidget, "user_work" )
        self.hipFile.clicked.connect( self.getAssetFile )
        self.hipFileWork.clicked.connect( self.getWorkFile )
        self.userListWork.itemClicked.connect(self.getWorkElem)
        
        self.btnSetOpen.hide()
        self.jobPath = hou.getenv('JOB')
        self.workUserPath = self.jobPath + "/scenes"
        #print self.workUserPath
        self.elemPath = os.path.abspath(os.path.join(self.jobPath, os.pardir))
        
        
        
        
        self.env_id = hou.getenv('ENV_ID')
        #print (self.env_id)
        if(self.env_id == "1" ):
            self.tabs.setTabEnabled(0, False)
            for dir in os.listdir(self.elemPath):
                self.elemListAsset.addItem(dir)
        else:
            self.tabs.setTabEnabled(1, False)
            for user in os.listdir(self.workUserPath):
                self.userListWork.addItem(user)
        
        
        
        
        
        
        
            
        self.currentItem = hou.getenv('HELEM')
        self.currentUserItem = hou.getenv('HUSER')
        self.currentelemIndex = self.elemListAsset.findItems(self.currentItem, QtCore.Qt.MatchExactly)
        self.currentUserIndex = self.userListWork.findItems(self.currentUserItem, QtCore.Qt.MatchExactly)
        if(len(self.currentelemIndex)>0):
            self.elemListAsset.setCurrentItem(self.currentelemIndex[0])
        if(len(self.currentUserIndex)>0):
            self.userListWork.setCurrentItem(self.currentUserIndex[0])    
            
        
        self.elemListAsset.itemClicked.connect(self.getAssetElem)
        self.connect(self.btnSetOpen, QtCore.SIGNAL('clicked()'), self.fileOpen)
        self.model = QtWidgets.QFileSystemModel()
        
        if(self.env_id == "1" ):
            fileRoot = hou.getenv('JOB') + 'scenes/'
            self.model.setRootPath(fileRoot)
            #self.tree = QtWidgets.QTreeView()
            self.hipFile.setModel(self.model)
            self.hipFile.setRootIndex(self.model.index(fileRoot))
            self.hipFile.setColumnWidth(0, 450)
 
            self.hipFile.setAnimated(False)
            self.hipFile.setIndentation(40)
            self.hipFile.setSortingEnabled(True)
        else:
            fileRoot = self.workUserPath + '/' + self.userListWork.currentItem().text()
            #print fileRoot
            self.model.setRootPath(fileRoot)
            #self.tree = QtWidgets.QTreeView()
            self.hipFileWork.setModel(self.model)
            self.hipFileWork.setRootIndex(self.model.index(fileRoot))
            self.hipFileWork.setColumnWidth(0, 450)
 
            self.hipFileWork.setAnimated(False)
            self.hipFileWork.setIndentation(40)
            self.hipFileWork.setSortingEnabled(True)
        
        
        
        
        
        
        
        
        
        
        
        
        
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.ui)
        self.setLayout(self.mainLayout)
        
        
    def getAssetElem(self):
        self.btnSetOpen.hide() 
        self.selectedAssetElem = self.elemListAsset.currentItem().text()
        self.filePath = self.elemPath + '/' + self.selectedAssetElem + '/scenes'
        if os.path.isdir(self.filePath) ==0:
            k = hou.ui.displayMessage("This element does not have any Hip file", buttons=('OK', 'Cancel'), default_choice=0, close_choice=1, title="Save a file in this element !")
            
        else:
            fileRoot = self.filePath
            self.model.setRootPath(fileRoot)
            self.hipFile.setRootIndex(self.model.index(fileRoot))
    
    def getWorkElem(self):
        self.btnSetOpen.hide() 
        self.selectedWorkUser = self.userListWork.currentItem().text()
        self.filePath = self.workUserPath + '/' + self.selectedWorkUser
        self.workElemCount = len(os.walk(self.filePath).next()[1])
        if self.workElemCount == 0:
            k = hou.ui.displayMessage("This User does not have any Elements", buttons=('OK', 'Cancel'), default_choice=0, close_choice=1, title="Create a Element for this user from set shot tool !")
            
        else:
            fileRoot = self.filePath
            self.model.setRootPath(fileRoot)
            self.hipFileWork.setRootIndex(self.model.index(fileRoot))
    
    def getWorkFile(self):
        self.btnSetOpen.show()
        self.currWorkItem = self.hipFileWork.currentIndex()
    # print item from first column
        #self.assetIndex = self.model.selectedIndexes()[0]
        self.hipfilePath = self.model.filePath(self.currWorkItem)
        #print self.hipfilePath
        return self.hipfilePath        
            
            
    def getAssetFile(self):
        self.btnSetOpen.show()
        self.currAssetItem = self.hipFile.currentIndex()
    # print item from first column
        #self.assetIndex = self.model.selectedIndexes()[0]
        self.hipfilePath = self.model.filePath(self.currAssetItem)
        #print self.hipfilePath
        return self.hipfilePath
        
        
    
        
        
    def fileOpen(self):
            
        
        
        #if switch(os.getenv('username')) == hou.getenv("HUSER"):
        hou.hipFile.load(self.hipfilePath, suppress_save_prompt=False, ignore_load_warnings=False)
         
        #else:
        
            #filename = self.hipfilePath
            #filename = filename[filename.rfind("/")+1:]
            
            #rev = filename[filename.rfind("_")+1:]
            
            #ver = filename[:filename.rfind("_")]
            #ver = ver[ver.rfind("_")+1:]
            
            #prefix = self.hipfilePath [:self.hipfilePath.rfind("_")]
            #prefix = prefix[:prefix.rfind("_")]
            
            #newpath = None
            
            #if (os.getenv('username') in filename):
            #    newpath = prefix + "_" + ver + "_" + rev
            #else:
            #    newpath = prefix + "_" + os.getenv('username') + "_" + ver + "_" + rev
            
                
            #if (self.hipfilePath != newpath):    
            #    shutil.copy2(self.hipfilePath, newpath)  
            
            #hou.hipFile.load(newpath, suppress_save_prompt=False, ignore_load_warnings=False)
            
        
        self.close()    
        
dia = openFile()
dia.show()         
