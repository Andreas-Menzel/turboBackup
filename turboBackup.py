#!/usr/bin/env python3

# TODO
# argparse

import os
import shutil
import datetime
import platform
from pathlib import Path, PurePosixPath

def deleteBackups(backupDir, pattern, keep):
    directoryList= os.listdir(backupDir)
    if not directoryList:
        return
    
    patternFiltered=[]
    for i in directoryList:
        if i.endswith(pattern):
            patternFiltered.append(i)

    if len(patternFiltered) <= keep:
        return
    
    patternFiltered.sort()
    toDelete= patternFiltered[0:len(patternFiltered)-keep]

    for i in toDelete:
        shutil.rmtree(backupDir / Path(i))    


def doBackup(sourceDir, backupDir, name="", keep=0):
    datetimeString= (datetime.datetime.now()).strftime("%Y-%m-%d_%H-%M-%S")
    if name != "":
        name= "_" + name

    if not os.path.exists(backupDir):
        os.makedirs(backupDir)

    latestBackup= "placeholder"
    directoryList= os.listdir(backupDir)
    if directoryList:
        latestBackup= max(directoryList)

    if platform.system() == "Windows":
        sourceDirTmp= str(PurePosixPath(sourceDir))
        backupDirTmp= str(PurePosixPath(backupDir))
        sourceDirTmp= "/cygdrive/" + sourceDirTmp[0] + sourceDirTmp[3:]
        backupDirTmp= "/cygdrive/" + backupDirTmp[0] + backupDirTmp[3:]
        
        latestBackupTmp= backupDirTmp + "/" + latestBackup
         
        os.system(
            "rsync -a " +
            "--delete " +
            "--link-dest '" + latestBackupTmp + "' " +
            "'" + sourceDirTmp + "/' " +
            "'" + backupDirTmp + "/" + datetimeString + name + "'"
        )
    else:
        os.system(
            "rsync -a " +
            "--delete " +
            "--link-dest '" + str(backupDir) + "/" + latestBackup + "' " +
            "'" + str(sourceDir) + "/' " +
            "'" + str(backupDir) + "/" + datetimeString + name + "'"
        )

    if keep > 0:
        deleteBackups(backupDir, name, keep)

def pathResolveWrapper(sourceDir, backupDir, name="", keep=0):
    sourceDir= Path(sourceDir).absolute()
    backupDir= Path(backupDir).absolute()
    
    doBackup(sourceDir, backupDir, name=name, keep=keep)

def main():
    sourceDir= "testOrdner"
    backupDir= "backupOrdner"
    pathResolveWrapper(sourceDir, backupDir, name="test", keep=5)

if __name__ == "__main__":
    main()
