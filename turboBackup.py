#!/usr/bin/env python3

# TODO
# argparse

import os
import shutil
import datetime
import platform

def deleteBackups(backupDir, pattern, keep):
    directoryList= os.listdir(backupDir)
    if(not directoryList):
        return
    
    patternFiltered=[]
    for i in directoryList:
        if(i.endswith(pattern)):
            patternFiltered.append(i)

    if(len(patternFiltered) <= keep):
        return
    
    patternFiltered.sort()
    toDelete= patternFiltered[0:len(patternFiltered)-keep]

    for i in toDelete:
        shutil.rmtree(backupDir + "/" + i)    


def doBackup(sourceDir, backupDir, name="", keep=0):
    datetimeString= (datetime.datetime.now()).strftime("%Y-%m-%d_%H-%M-%S")
    if(name != ""):
        name= "_" + name

    if not os.path.exists(backupDir):
        os.makedirs(backupDir)

    latestBackup= "placeholder"
    directoryList= os.listdir(backupDir)
    if(directoryList):
        latestBackup= max(directoryList)        

    if(platform.system() == "Windows"):
        os.system(
            "rsync -a " +
            "--delete " +
            "--link-dest " + ".\\..\\" + latestBackup + " " +
            ".\\" + sourceDir + " " +
            ".\\" + backupDir + "\\" + datetimeString + name
        )
    
    if((platform.system() == "Linux") or (platform.system() == "Darwin")):
        os.system(
            "rsync -av " +
            "--delete " +
            "--link-dest " + "./../" + latestBackup + " " +
            "./" + sourceDir + " " +
            "./" + backupDir + "/" + datetimeString + name
        )

    if(keep > 0):
        deleteBackups(backupDir, name, keep)

def main():
    sourceDir= "testOrdner"
    backupDir= "backupOrdner"
    doBackup(sourceDir, backupDir, name="test", keep=5)

if __name__ == "__main__":
    main()
