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
import ftplib
import glob
import time


def SendFileFTP(n_file):
    f = open(n_file,'rb')
    ftp_cmd = 'STOR ' + n_file
    ftp.storbinary(ftp_cmd,f)
    f.close()
    return
		
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

Monthfile = sys.argv[1]
DataYea = sys.argv[2]


pathData = "/media/usb/DataMagnet/" + DataYea + "/DataMin"



host_ip = "lisn.igp.gob.pe"
user = "cesar"
password = "cev2001gobpe"

pathserver = "/home/cesar/isr/magnetometer/areq/" + DataYea

os.chdir(pathData)
ListDay = glob.glob("*" + Monthfile + "." + DataYea[-2:] + "m")
ListDay.sort()

ftp = ftplib.FTP(host = host_ip, timeout = 30)
ftp.login(user,password)
ftp.cwd(pathserver)

for minute in ListDay:
    print("Enviando " + minute)
    SendFileFTP(minute)
    time.sleep(0.3)

ftp.quit()
print("FINISH")
