#!/usr/bin/env python3

"""
MIT License

Copyright (c) 2022 Tizian Erlenberg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Project is on GitHub: https://github.com/tizianerlenberg/turboBackup/

import os
import shutil
import datetime
import platform
from pathlib import Path, PurePosixPath
import re

def deleteBackups(baseDirectory, listToDelete, dryRun=True):
	if dryRun:
		for i in listToDelete:
			print(f"shutil.rmtree({baseDirectory / Path(i)})")
	else:
		for i in listToDelete:
			shutil.rmtree(baseDirectory / Path(i))

#
def rename(directory, oldName, newName, dryRun=True):
	if dryRun:
		print(f"shutil.move({directory / oldName}, {directory / newName})")
	else:
		shutil.move(directory / oldName, directory / newName)

def createDir(directory, dryRun=True):
	if not os.path.exists(directory):
		if dryRun:
			print(f"os.makedirs({directory})")
		else:
			os.makedirs(directory)

def getUncompletedBackup(directoryList):
	filteredList= list(filter(lambda x: x.startswith(".tmp_"), directoryList))
	if filteredList:
		return filteredList[0]
	else:
		return ""

def doBackupAndCleanup(sourceDir, backupDir, name="backup", keep=0, additionalOptions="", dryRun=True):
	if not os.path.exists(sourceDir):
		raise Exception("Source Directory was not found")
	if keep <= 0:
		raise Exception("keep can not be below 0")
	if not re.search('^[A-Za-z0-9]+$', name):
		raise Exception("name can only contain A-Z, a-z and 0-9")

	createDir(backupDir, dryRun=dryRun)

	datetimeString= (datetime.datetime.now()).strftime("%Y-%m-%d_%H-%M-%S")
	directoryStringList= os.listdir(backupDir)
	filteredDirectoryStringList= []
	if directoryStringList:
		filteredDirectoryStringList= list(filter(lambda x: x.endswith(f"_{name}"), directoryStringList))
	relativeNewDir= Path(f".tmp_{datetimeString}_{name}")
	relativeLinkDestDir=Path()

	if directoryStringList:
		uncompletedBackup= getUncompletedBackup(directoryStringList)
		if uncompletedBackup:
			rename(backupDir, Path(uncompletedBackup), Path(relativeNewDir), dryRun=dryRun)
			directoryStringList.remove(uncompletedBackup)
		else:
			if (keep != 0) and (len(filteredDirectoryStringList) >= keep):
				filteredDirectoryStringList.sort()
				deleteBackups(backupDir, filteredDirectoryStringList[keep:], dryRun=dryRun)
				rename(backupDir, Path(filteredDirectoryStringList[0]), Path(relativeNewDir), dryRun=dryRun)
				directoryStringList.remove(filteredDirectoryStringList[0])
			else:
				createDir(backupDir / Path(relativeNewDir), dryRun=dryRun)

		if directoryStringList:
			relativeLinkDestDir= Path(max(directoryStringList))


	executeRsyncCommand(sourceDir, backupDir, relativeNewDir,
						relativeLinkDestDir=relativeLinkDestDir,
						additionalOptions=additionalOptions, dryRun=dryRun)

	rename(backupDir, relativeNewDir,
		   Path(str(relativeNewDir)[5:]), dryRun=dryRun)

def executeRsyncCommand(sourceDir, backupDir, relativeNewDir, relativeLinkDestDir=Path(), additionalOptions="", dryRun=True):
	if platform.system() == "Windows":
		sourceDir= generateRsyncWindowsPathString(sourceDir)
		backupDir= generateRsyncWindowsPathString(backupDir)
	else:
		sourceDir= str(sourceDir)
		backupDir= str(backupDir)

	relativeNewDir= str(relativeNewDir)

	commandToRun = "rsync -a --delete "

	if additionalOptions != "":
		commandToRun += f"{additionalOptions} "

	if relativeLinkDestDir == Path():
		commandToRun += (
			f"'{sourceDir}/' "
			f"'{backupDir}/{str(relativeNewDir)}'"
		)
	else:
		commandToRun += (
			f"--link-dest '{backupDir}/{str(relativeLinkDestDir)}' "
			f"'{sourceDir}/' "
			f"'{backupDir}/{str(relativeNewDir)}'"
		)

	if dryRun:
		print(f"os.system({commandToRun})")
	else:
		os.system(commandToRun)

def generateRsyncWindowsPathString(path):
	path= str(PurePosixPath(path))
	return "/cygdrive/" + path[0] + path[3:]

def pathResolveWrapper(sourceDir, backupDir, name="backup", keep=0, additionalOptions="", dryRun=True):
	sourceDir= Path(sourceDir).absolute()
	backupDir= Path(backupDir).absolute()
	doBackupAndCleanup(sourceDir, backupDir, name=name, keep=keep, additionalOptions=additionalOptions, dryRun=dryRun)

def main():
	import argparse

	parser = argparse.ArgumentParser(description=
		"""TurboBackup is a cross platform rsync Backup utility.
		It copys the content of a source directory to a destination directory.
		It will create a new subdirectory with a timestamp as the name
		with each execution. Every subdirectory is going to contain hardlinks
		to the instances of files in the previous subdirectorys,
		except if changes were made to the file, effectivley making the
		subdirectorys snapshots of the source directory.""")
	parser.add_argument("sourceDir", help = "path to source directory")
	parser.add_argument("backupDir", help = "path to backup directory")
	parser.add_argument('-n', '--name',
		help="name to append to the incremental backup subdirectories", default = "")
	parser.add_argument('-k', '--keep', type= int,
		help="if a number is provided, this scirpt will delete all backups with the specified name (0 does not delete any backups)", default= 0)
	parser.add_argument('-p', '--passthrough',
		help="USE WITH CAUTION! arguments will get passed through to rsync, use like this: -p='--log-file=FILE' option -a is already applied", default= "")
	parser.add_argument('-d', '--dryrun', action='store_true',
		help="this will print out what was about to be done, instead of actaully performing the operations")
	args = parser.parse_args()

	pathResolveWrapper(args.sourceDir, args.backupDir, name=args.name, keep=args.keep, additionalOptions=args.passthrough, dryRun=args.dryrun)

if __name__ == "__main__":
	main()
