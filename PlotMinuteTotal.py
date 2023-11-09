#!/usr/bin/python3

######################################################################
#
# MagnetPlot.py
#
#	Created on: November 30, 2021
#		Modified: March 14, 2023
#	    Author: Ricardo V. Rojas Quispe
# 	    e-mail: net85.ricardo@gmail.com
#
#	Este script se encarga de enviar por FTP
#		- Corregido path de LastSend.txt
#
######################################################################

import sys
import os
import glob



#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

Iaga = sys.argv[1]
Monthfile = sys.argv[2]
DataYea = sys.argv[3]


#pathData = "/home/ricardo/Documents/Python3/DataMin"
#DirData = os.path.join(pathData, Iaga)
DirData  = "/home/ricardo/Documents/Data/Data_Nazca2023/DataMagnet/2023/DataMin"
 



os.chdir(DirData)
ListDay = glob.glob(Iaga[:3] + "*" + Monthfile + "." + DataYea[-2:] + "m")
ListDay.sort()


for i in ListDay:
	print("File: " + i)
	os.system("python3 /home/ricardo/Documents/Python3/MinutePlotMag.py " + os.path.join(DirData, i))

print("***FINISH***")
