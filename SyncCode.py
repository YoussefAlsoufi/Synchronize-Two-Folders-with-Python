import filecmp
import os
import shutil
import hashlib
import schedule,time

srcFolderPath =input("Enter Source Folder Path: ")
ReplicaFolderPath=input ("Enter Replica Folder Path: ")

info_log=[]
path = '/Users/Josef/Projects/SycnTwoFolderWithPython/'

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

def WriteToTxtFile ():
    comparison = filecmp.dircmp(srcFolderPath, ReplicaFolderPath)
    sourcefolderfiles = ','.join(comparison.left_only)
    replicaFolderFiles =','.join(comparison.right_only)
    
    common_files = ','.join(comparison.common)
    
    with open(path+ 'Report.txt','w' ) as Folder_report:
        Folder_report.write("Steps of synchronising the folders.\n\n")
        for line in info_log:
            Folder_report.write(line)
            Folder_report.write("\n\n")
        Folder_report.write("\n")
        Folder_report.write("="*25+"\n")
        Folder_report.write("Report To check Unmatched Folders/Files.\n\n")
        Folder_report.write("Common Files : \n" + common_files+ "\n")
        Folder_report.write("\n Source File contains : \n" + sourcefolderfiles + "\n")
        Folder_report.write("\n Replica Folder contains :\n" + replicaFolderFiles + "\n")
    
    
# This Check Fun will check the Content of the file after Copying/Creating to confirm that no changing after the process is done.
def CheckContent(srcFilePath,desFilePath,file, message):
    if (CalculateMd5(srcFilePath)!= CalculateMd5(desFilePath+'/'+file)):
        info_log.append("The Content of "+file+" has changed by someone'Hacker' during "+ message+ " the file, ReWrite the file in progress.")
        RewriteFile(srcFilePath, desFilePath, file, message)


def RemoveUnmatchedFiles(desPath, srcPath):           
    for folders, subFolders, items in os.walk(desPath):
        for item in items : 
            srcFilePathReplaced= folders.replace(desPath,srcPath)
            srcFilePath= srcFilePathReplaced+'/'+item
            desFilePath= folders+'/'+item
            if not (os.path.exists(srcFilePath)):
                os.remove(desFilePath)
                info_log.append(item +" has Removed from "+ folders)
            
def RemoveUnmatchedDirs(desPath, srcPath):    
    for folders,subFolders,items in os.walk(desPath):
        srcPathReplaced = folders.replace(desPath,srcPath)
        for folder in subFolders:
            try:
                if (os.path.exists(srcPathReplaced+'/'+folder)):
                    continue
                else:
                    shutil.rmtree(folders+'/'+folder)
                    info_log.append(folder +" has Removed from "+ folders)
            except FileNotFoundError as e:
                    info_log.append("An Error with removing "+ folders+" "+e)
                
        

            
# Copy the content of the first file in            
def SelectItems(srcPath,desPath):
    info_log.clear()  
    for dirs,subdirs,files in os.walk(srcPath):
        for subdir in subdirs :
            desSubfolderPathReplaced=dirs.replace(srcPath,desPath)
            try:
                os.mkdir(desSubfolderPathReplaced+'/'+subdir)
                info_log.append("The "+subdir+" has Created in "+desSubfolderPathReplaced)
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
    WriteToTxtFile()


def Starter():   
    try :
        if ((os.path.exists(srcFolderPath)) and (os.path.exists(ReplicaFolderPath))):
            SelectItems(srcFolderPath, ReplicaFolderPath)
            schedulerRun=schedule.every().day.at("02:55").do(SelectItems(srcFolderPath, ReplicaFolderPath))
            print("The synchronization process has been done successfully!")
            while True:
                schedulerRun.run_pending()
                time.sleep(1)
            
        else :
            print("Source Folder Path/ Replica Folder Path doesn't exist, please check them again!")

            
    except FileNotFoundError as e:
        print("These is an Error: ",e)

Starter()  

      
'''      
my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(60, 1, do_something, (my_scheduler,))
my_scheduler.run()
'''     










