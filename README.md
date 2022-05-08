# turboBackup

TurboBackup is a cross platform rsync Backup utility.
It copys the content of a source directory to a destination directory.
It will create a new subdirectory with a timestamp as the name
with each execution. Every subdirectory is going to contain hardlinks
to the instances of files in the previous subdirectorys,
except if changes were made to the file, effectivley making the
subdirectorys snapshots of the source directory.

## Install instructions:

Clone the repository. Execute turboBackup.py.
See --help flag for more info on the usage.

## Requirements:

rsync (added to path)
