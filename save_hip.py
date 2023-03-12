import os
import re
import shutil
from PySide2 import QtWidgets, QtUiTools, QtCore
import nodesearch
import json

hou.hscript("setenv PRJPATH = R:/filmServe")
root = hou.getenv('HIP')
hroot = hou.getenv("PRJPATH")
currFile = hou.hipFile.basename()
#print currFile

match = re.search('(.*)([\_])([v])([\d]+)(\_)([r])([\d]+)(\.hip)', currFile)





class vhqSave(QtWidgets.QWidget):
    if(hou.hipFile.basename()=="untitled.hip"):
        hou.ui.displayMessage("Your filename is Untitled.hip. Set $JOB with |Set Shot| shelf Tool and save your file.", buttons=('OK', 'Cancel'), default_choice=0, close_choice=1, title="Save your File")
    else:
        def __init__(self):
            super(vhqSave, self).__init__()
            widgets = hou.qt.mainWindow().children()
            if not os.path.isdir(root):
                raise ValueError("The given root is not valid: {0}".format(root))
            
            for index in widgets:
                try:
                    if index.windowTitle() == "VHQ Save AS":
                        index.setParent(None)
                        index.setWindowFlags(QtCore.Qt.WA_DeleteOnClose)
                        index.close()
                        continue
                except Exception as e:
                    pass
            self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
            loader = QtUiTools.QUiLoader()
        
            self.ui = loader.load('R:/Library/VHQ_Houdini_Tool/vLib/scripts/python/prjman/ui/vhq_save_new.ui')
        
            self.setGeometry(800, 300, 450, 180)
            #self.setStyleSheet(hou.qt.styleSheet())
            #self.setProperty("houdiniStyle", True)
        
            self.shotName = self.ui.findChild(QtWidgets.QLineEdit, "lineEdit")
            self.shotVer = self.ui.findChild(QtWidgets.QSpinBox, "spinBox")
            self.shotRev = self.ui.findChild(QtWidgets.QSpinBox, "spinBox_2")
            self.saveAs = self.ui.findChild(QtWidgets.QPushButton, "saveas")
        
            self.setWindowTitle('VHQ Save AS')
            self.job = hroot = hou.getenv("JOB")
            self.jobList = self.job.split('/')
        
        #self.saveAs.clicked.connect(self.saveAs)
            self.connect(self.saveAs, QtCore.SIGNAL('clicked()'), self.saveFile)
        
        #print self.jobList
            shot = match.group(1)
            rev = int(match.group(7))
            ver = int(match.group(4))
        #x = str(int(match.group(4))).rjust(len("000"), '0')
        #print x
        
        
            self.shotVer.setValue(ver)
            self.shotRev.setValue(rev)
            self.shotName.setText(shot)
        
            mainLayout = QtWidgets.QVBoxLayout()
            mainLayout.addWidget(self.ui)
            self.setLayout(mainLayout)
            
        def importData(self):
            geotype = nodesearch.NodeType("geo")
            objlvl = hou.node("/obj/")
            alembic_in_list = []
            bgeo_in_list = []
            vdb_in_list = []
            for geo in geotype.nodes(objlvl, recursive=True):
                    geolvl = hou.node(geo.path())
                    alembictype = nodesearch.NodeType("alembic")
                    filetype = nodesearch.NodeType("file")
                    vhqtype = nodesearch.NodeType("vhq_in_out")
                    
                    #print alembictype.nodes(geolvl)
                    for _alembic in alembictype.nodes(geolvl):
                            _fileNameABC = _alembic.parm('fileName').eval()
                            if _fileNameABC != 'default.abc': 
                                    alembic_in_list.append(_fileNameABC)
                                    #print _alembic.path() + ' --> ' + _fileNameABC +'\n \n'
                    for _file in filetype.nodes(geolvl):
                            _fileNode = hou.node(_file.path())
                            _fileAll = _fileNode.inputs()
                            if len(_fileAll) == 0:
                                    _filePath = _file.parm('file').eval()
                                    if _filePath != 'default.bgeo':
                                            _formatID = _filePath.split('.')[-2] + '.' + _filePath.split('.')[-1]
                                            _formatID2 = _filePath.split('.')[-1]
                                            if _formatID2 == 'bgeo' or _formatID2 == 'bgeosc' or _formatID2 == 'bgeogz':
                                                    bgeo_in_list.append(_filePath)
                                            if _formatID == "bgeo.sc" or _formatID == "bgeo.gz" or _formatID == "bgeo.bz2":
                                                    bgeo_in_list.append(_filePath)
            #                    print _formatID
                                            if _formatID2 == 'abc':
                                                    alembic_in_list.append(_filePath)
                                            if _formatID2 == 'vdb':
                                                    vdb_in_list.append(_filePath)
            #            print _file.path()
                    for _vhqinout in vhqtype.nodes(geolvl):
                            _vhqNode = hou.node(_vhqinout.path())
                            _vhqAll = _vhqNode.inputs()
                            if len(_vhqAll) == 0:
                                    _load_format = _vhqinout.parm('switch').eval()
                                    if _load_format == 1:
                                            _filenameBGEO = _vhqinout.parm('file_bgeo').eval()
                                            bgeo_in_list.append(_filenameBGEO)
                                    if _load_format == 2:
                                            _filenameVDB = _vhqinout.parm('file_vdb').eval()
                                            vdb_in_list.append(_filenameVDB)
            #                print _vhqinout.path()
                
    
            import_data = { 'alembic' : alembic_in_list, 'bgeo' : bgeo_in_list, 'vdb' : vdb_in_list}
    
    #        print import_data['vdb']
            _importJson = hou.getenv('JOB') + '/data/' + hou.getenv('HIPNAME') + '_geo_import.json'
            with open( _importJson, 'w') as import_json_file:
              json.dump(import_data, import_json_file,  indent=4)
          
        def saveFile(self):
                filepath = root + "/" + self.shotName.text() + "_v" + str(self.shotVer.value()).rjust(len("000"), '0') + "_r" + str(self.shotRev.value()).rjust(len("000"), '0') + match.group(8)
                if os.path.isfile(filepath):
                    overwrite =  hou.ui.displayMessage("Overwrite the a existing hip file?", buttons=('OK', 'Cancel'), default_choice=0, close_choice=1, title="Overwrite File!!")
                    #print overwrite
                    if overwrite == 0:
                        hou.hipFile.save(filepath)   
                else:
                    hou.hipFile.save(filepath)
                self.importData()
                copy = filepath
                copy = filepath[filepath.rfind(":"):]
                copy = "E" + copy
                     
                if not os.path.exists(copy[:copy.rfind("/")+1]):
                    os.makedirs(copy[:copy.rfind("/")+1])
            
                shutil.copy2(filepath, copy)   
                
                dialog.close()
        
        
            
dialog = vhqSave()
dialog.show() 
                        
