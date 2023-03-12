import hou
import os
import shutil
import nodesearch
import json

def importData():
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

def main():
    if(hou.hipFile.basename()=="untitled.hip"):
        hou.ui.displayMessage("Your filename is Untitled.hip. Set $JOB with |Set Shot| shelf Tool and save your file.", buttons=('OK', 'Cancel'), default_choice=0, close_choice=1, title="Save your File")
    else:
        filename = hou.hipFile.basename()
        sfilename = filename.split('.')
        nameonly = sfilename[0]
        snameonly = nameonly.split('_')
        
    
        newName = nameonly[0:-9] +snameonly[-2] + "_r" + str(int(snameonly[-1][1:4]) + 1).rjust(len(snameonly[-1][1:4]), '0')
        
    
        newFileName = newName + '.hip'
        
        filePath = hou.hipFile.path()
        filedir = os.path.dirname(filePath)
        
        newFile = filedir +'/'+ newFileName
    
        if os.path.isfile(newFile):
            overwrite =  hou.ui.displayMessage("Overwrite the current hip file?", buttons=('OK', 'Cancel'), default_choice=0, close_choice=1, title="Overwrite File!!")
            print overwrite
            if overwrite == 0:
                hou.hipFile.save(newFile)   
        else:
            hou.hipFile.save(newFile) 
            
        copy = newFile
        copy = newFile[newFile.rfind(":"):]
        copy = "E" + copy
          
             
        if not os.path.exists(copy[:copy.rfind("/")+1]):
            os.makedirs(copy[:copy.rfind("/")+1])
            
        
        shutil.copy2(newFile, copy) 
        importData()
    
main()
