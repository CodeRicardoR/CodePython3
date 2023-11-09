#!/usr/bin/python3

######################################################################
#
# MagnetPlot.py
#
#	Created on: November 30, 2021
#	    Author: Ricardo V. Rojas Quispe
# 	    e-mail: net85.ricardo@gmail.com
#
#	Este script se encarga de comprimir a ZIP
#
######################################################################

import sys
import os
import zlib
import zipfile
import time

compresion = zipfile.ZIP_DEFLATED

# File OUT zip
datapath1 = sys.argv[1] 
# File IN to zip
datapath2 = sys.argv[2]

#Separando las rutas:
pathzip = os.path.dirname(datapath1)
filezip = os.path.basename(datapath1)

pathseg = os.path.dirname(datapath2)
fileseg = os.path.basename(datapath2)

FilePy = sys.argv[0]
DirWork = os.path.dirname(FilePy)
if DirWork == "":
	DirWork = os.getcwd()
FileLog = os.path.join(DirWork,"FileLogZIP.txt")


#comprimiendo el archivo:
os.chdir(pathzip)
zf = zipfile.ZipFile(filezip, mode = "w")

os.chdir(pathseg)
try:
	print("Agregando archivo con compresion estandar:", compresion)
	zf.write(fileseg,compress_type = compresion)

except:
	Log = open(FileLog,'a')
	Log.write('---------------------------------------\n')
	Log.write("Error al comprimir archivo, " + time.strftime("%Y-%m-%d %H:%M:%S") + '\n')
	Log.close()
	
finally:
	print("cerrando archivo")
	zf.close()
	