#!/usr/bin/env python3

# TODO
# argparse

import os
import shutil
import datetime
import platform
from pathlib import Path, PureWindowsPath

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

    latestBackupDir= "placeholder"
    directoryList= os.listdir(backupDir)
    if directoryList:
        latestBackupDir= Path(max(directoryList))

    if platform.system() == "Windows":
        os.system(
            "rsync -a " +
            "--delete " +
            "--link-dest " + ".\\..\\" + str(latestBackupDir) + " " +
            ".\\" + str(sourceDir) + " " +
            ".\\" + str(backupDir) + "\\" + datetimeString + name
        )
    else:
        os.system(
            "rsync -a " +
            "--delete " +
            "--link-dest " + "./../" + str(latestBackupDir) + " " +
            "./" + str(sourceDir) + " " +
            "./" + str(backupDir) + "/" + datetimeString + name
        )

    if keep > 0:
        deleteBackups(backupDir, name, keep)

def pathResolveWrapper(sourceDir, backupDir, name="", keep=0):
    if platform.system() == "Windows":
        sourceDir= PureWindowsPath(sourceDir)
        backupDir= PureWindowsPath(backupDir)
    else:
        sourceDir= Path(sourceDir)
        backupDir= Path(backupDir)
    
    doBackup(sourceDir, backupDir, name=name, keep=keep)

def main():
    sourceDir= "testOrdner"
    backupDir= "backupOrdner"
    pathResolveWrapper(sourceDir, backupDir, name="test", keep=5)

if __name__ == "__main__":
    main()
