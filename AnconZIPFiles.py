#Compresion de archivos de segundos del 2022

import sys
import os
import zipfile
import glob

compresion = zipfile.ZIP_DEFLATED

def Comprimir(pathseg, pathzip):
    #Listando archivos a comprimir:
    os.chdir(pathseg)
    FilesSeg = glob.glob("*")

    #comprimiendo el archivo:
    for j in FilesSeg:
        os.chdir(pathzip)
        filezip = j[:-3] + "zip"
        zf = zipfile.ZipFile(filezip, mode = "w")
        
        os.chdir(pathseg)
        zf.write(j, compress_type = compresion)
        zf.close()


DataPath= "/media/usb/DataMagnet"



Month = sys.argv[1]
DataYea = sys.argv[2]

DataPathSec = os.path.join(DataPath, DataYea)
DataPathSec = os.path.join(DataPathSec, "DataSec")

DataPathZip = os.path.join(DataPath, DataYea)
DataPathZip = os.path.join(DataPathZip, "DataZip")
os.chdir(DataPathSec)

ListMonths = glob.glob(Month + "*")
ListMonths.sort()

ListPathMontsSec = []
ListPathMontsZip = []
for DayFile in ListMonths:
    ListPathMontsSec.append(os.path.join(DataPathSec,DayFile))
    ListPathMontsZip.append(os.path.join(DataPathZip,DayFile))

for DirZip in ListPathMontsZip:
    if not os.path.isdir(DirZip):
        os.makedirs(DirZip)

for c in range(len(ListPathMontsSec)):
    Comprimir(ListPathMontsSec[c], ListPathMontsZip[c])

print("***Finish***")






