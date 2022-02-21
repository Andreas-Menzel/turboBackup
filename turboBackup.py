#!/usr/bin/env python3

import os
import datetime

def doBackup(sourceDir, backupDir):
    datetimeString= (datetime.datetime.now()).strftime("%Y-%m-%d_%H-%M-%S")

    if not os.path.exists(backupDir + "/" + datetimeString + "_new"):
        os.makedirs(backupDir + "/" + datetimeString)

    latestBackup= "placeholder"
    if os.path.exists(backupDir + "/" + "latestBackup"):
        latestBackup= "latestBackup"

    os.system(
        "rsync -av " + 
        "--link-dest " + "..\\" + latestBackup + " " +
        sourceDir + " " +
        backupDir + "\\" + datetimeString
    )

    os.system("rmdir " + backupDir + "\\" + "latestBackup")
    os.system("mklink /J " + backupDir + "\\" + "latestBackup " +
        backupDir + "\\" + datetimeString)

def main():
    sourceDir= "testOrdner" + "/"
    backupDir= "backupOrdner"
    doBackup(sourceDir, backupDir)

if __name__ == "__main__":
    main()
