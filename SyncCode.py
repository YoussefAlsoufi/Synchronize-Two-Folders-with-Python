import filecmp
import os
import shutil
import hashlib

info_log=[]
def RewriteFile(srcPath,desPath,file,message):
    try:
        shutil.copy(srcPath, desPath)
        info_log.append( message +" "+file+" is done successfully in "+desPath)
    except:
        info_log.append( message + file + " in "+desPath+ "didn't happend with an exception, please check again!")
        
def CalculateMd5(srcFilePath):
    hasher=hashlib.md5()
    with open (srcFilePath,'rb') as open_file:
        content = open_file.read()
        hasher.update(content) 
    return hasher.hexdigest()

# This Check Fun will check the Content of the file after Copying/Creating to confirm that no changing after the process is done.
def CheckContent(srcFilePath,desFilePath,file, message):
    if (CalculateMd5(srcFilePath)!= CalculateMd5(desFilePath+'/'+file)):
        info_log.append("The Content of "+file+" has been changing by someone'Hacker' during "+ message+ " the file, ReWrite the file in progress.")
        RewriteFile(srcFilePath, desFilePath, file, message)


def RemoveUnmatchedFiles(desPath, srcPath):           
    for folders, subFolders, items in os.walk(desPath):
        for item in items : 
            srcFilePathReplaced= folders.replace(desPath,srcPath)
            srcFilePath= srcFilePathReplaced+'/'+item
            desFilePath= folders+'/'+item
            if not (os.path.exists(srcFilePath)):
                os.remove(desFilePath)
                info_log.append(item +" Removed from "+ folders)
            
def RemoveUnmatchedDirs(desPath, srcPath):    
    for folders,subFolders,items in os.walk(desPath):
        srcPathReplaced = folders.replace(desPath,srcPath)
        for folder in subFolders:
            try:
                if (os.path.exists(srcPathReplaced+'/'+folder)):
                    continue
                else:
                    shutil.rmtree(folders+'/'+folder)
                    info_log.append(folder +" Removed from "+ folders)
            except FileNotFoundError as e:
                    info_log.append("An Error with removing "+ folders+" "+e)
                
            
    
#path = '/Users/Josef/Projects/SycnTwoFolderWithPython/'

            
# Copy the content of the first file in            
def SelectItems(srcPath,desPath):
    for dirs,subdirs,files in os.walk(srcPath):
        for subdir in subdirs :
            desSubfolderPathReplaced=dirs.replace(srcPath,desPath)
            try:
                os.mkdir(desSubfolderPathReplaced+'/'+subdir)
                info_log.append("The "+subdir+" is Created in "+desSubfolderPathReplaced)
            except :
                info_log.append("The Folder "+subdir+" is already in "+desSubfolderPathReplaced)
          
        for file in files :
            desFilePathReplaced= dirs.replace(srcPath,desPath)
            srcFilePath= dirs+'/'+file
            desFilePath= desFilePathReplaced+'/'+file
            if (os.path.exists(desFilePath)):
                if (CalculateMd5(srcFilePath)!= CalculateMd5(desFilePath)):
                    info_log.append("The Content of "+ file+" has changed in the SourceFolder so it's going to Copy the updates.")
                    RewriteFile(srcFilePath, desFilePathReplaced,file,"Copying")
                    CheckContent(srcFilePath, desFilePathReplaced, file, "Copying")
                    
                else:
                    info_log.append(file+" is already in "+ desFilePathReplaced +" with all contents")
                    CheckContent(srcFilePath, desFilePathReplaced, file, "Copying")
            else:
                RewriteFile(srcFilePath, desFilePathReplaced,file,"Creating")
                CheckContent(srcFilePath, desFilePathReplaced, file, "Creating")
                
    RemoveUnmatchedFiles(desPath,srcPath)
    RemoveUnmatchedDirs(desPath,srcPath)
                               
    
info_log.clear()  
SelectItems('/Users/Josef/Projects/SycnTwoFolderWithPython/SourceFolder', '/Users/Josef/Projects/SycnTwoFolderWithPython/ReplicaFolder')




# Compare the content of two folders :

comparison = filecmp.dircmp('/Users/Josef/Projects/SycnTwoFolderWithPython/SourceFolder', '/Users/Josef/Projects/SycnTwoFolderWithPython/ReplicaFolder')
comparisonFull=comparison.report_partial_closure()


with open('/Users/Josef/Desktop/folder_info.txt','w' ) as Folder_report:
    print("Report : ",comparisonFull,file=Folder_report)
'''
common_files = ','.join(comparison.common)

sourcefolderfiles = ','.join(comparisonFull.left_only)
replicaFolderFiles =','.join(comparisonFull.right_only)

with open(path+ 'folder_info.txt','w' ) as Folder_report:
    Folder_report.write("Common Files : \n" + common_files+ "\n")
    Folder_report.write("\n Source File contains : \n" + sourcefolderfiles + "\n")
    Folder_report.write("\n Replica Folder contains :\n" + replicaFolderFiles + "\n")

'''










