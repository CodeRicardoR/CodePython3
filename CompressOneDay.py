import sys
import glob
import os
import time

DirWork = "/home/pi/MagnetProgram"
DataDirZip = "/media/usb/DataMagnet/2023/DataZip"
DataDirSec = "/media/usb/DataMagnet/2023/DataSec"

day = sys.argv[1]

Dirfiles = os.path.join(DataDirSec, day)
os.chdir(Dirfiles)

ListFiles = glob.glob('*.23s')
ListFiles.sort()

os.chdir(DirWork)

for i in ListFiles:
    cmd_line = "python3 " + os.path.join(DirWork, "CompressFile.py") + " " + os.path.join(DataDirZip, day) + "/" + i[:-3] + "zip " + os.path.join(DataDirSec, day) + "/" + i
    os.system(cmd_line)
    time.sleep(2)

print("****FINISH****")


