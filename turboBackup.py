#!/usr/bin/env python3

# TODO
# OS compatability
# keep Variable -> keep certain amount of backups, delete the rest
# argparse
# --delete flag

import os
import datetime

def deleteBackups(pattern, keep):
    pass
    directoryList= os.listdir(backupDir)
    if(directoryList):
        directoryList.sort()

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

    
    os.system(
        "rsync -av " +
        "--link-dest " + ".\\..\\" + latestBackup + " " +
        ".\\" + sourceDir + " " +
        ".\\" + backupDir + "\\" + datetimeString + name
    )


    if(keep > 0):
        deleteBackups(name, keep)

def main():
    sourceDir= "testOrdner"
    backupDir= "backupOrdner"
    doBackup(sourceDir, backupDir, name="test")

if __name__ == "__main__":
    main()
