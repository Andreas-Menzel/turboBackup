#!/usr/bin/env python3

#from constants import *
import sys
import os
import datetime


def main():
    sourceDir= "testOrdner" + "/"
    backupDir= "backupOrdner"
    datetimeString= (datetime.datetime.now()).strftime("%Y-%m-%d_%H-%M-%S")

    if not os.path.exists(backupDir + "/" + datetimeString + "_new"):
        os.makedirs(backupDir + "/" + datetimeString + "_new")

    latestBackup= "placeholder"
    for i in os.listdir(path=backupDir):
        if(i.endswith("latest")):
                latestBackup= i

    os.system(
        "rsync -av " + 
        "--link-dest " + "..\\" + latestBackup + " " +
        sourceDir + " " +
        backupDir + "\\" + datetimeString + "_new"
    )

    if os.path.exists(backupDir + "/" + latestBackup):
        os.rename(
            (backupDir + "/" + latestBackup), 
            (backupDir + "/" + latestBackup[0:19])
        )

    os.rename(
        (backupDir + "/" + datetimeString + "_new"), 
        (backupDir + "/" + datetimeString + "_latest")
    )


if __name__ == "__main__":
    main()
