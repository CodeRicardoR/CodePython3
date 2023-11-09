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
import time

def SendFileFTP(namefile, DataPath):

	os.chdir(DataPath)
	resultado = "Error"

	try:
		ftp = ftplib.FTP(host = host_ip, timeout = 30)
		ftp.login(user,password)
		ftp.cwd(pathserver)

		f = open(namefile,'rb')
		ftp_cmd = 'STOR ' + namefile
		resultado = ftp.storbinary(ftp_cmd,f)
		f.close()
		ftp.quit()
		
	except:
		f.close()
		ftp.quit()
	
	return resultado
		
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

FilePy = sys.argv[0]
DirWork = os.path.dirname(FilePy)
if DirWork == "":
	DirWork = os.getcwd()
FileLog = os.path.join(DirWork,"FileLogFTP.txt")
FileLast = os.path.join(DirWork,"LastSend.txt")

pathserver = sys.argv[1]
bufferfile = sys.argv[2]
file_server = sys.argv[3]

#Separando strings:
newpath = os.path.dirname(bufferfile)
newfile = os.path.basename(bufferfile)

inList = open(file_server, 'r').readlines()      
buffer_line = ""
conta = 0
for line in inList:
	pos_chr = line.rfind(' ')
	if conta == 0:
		host_ip = line[pos_chr + 1:len(line) - 1]
		conta = conta + 1
	elif conta == 1:
		user = line[pos_chr + 1:len(line) - 1]
		conta = conta + 1
	elif conta == 2:
		password = line[pos_chr + 1:len(line) - 1]
		conta = 3
		

#Determinando la hora y minutos (23:50)
hour_today = int(time.strftime("%H"))
minute_today = int(time.strftime("%M"))
print("Hora: %d:"%hour_today + "%d "%minute_today)

if hour_today == 23:
	if minute_today >= 30:
		#Guardando nombre del ultimo archivo enviado:
		if os.path.exists(FileLast):
			print("Existe: " + FileLast)
		else:
			print("Creando: " + FileLast)
			p = open(FileLast,"w")
			p.write(newfile)
			p.close()


if hour_today == 0:
	if minute_today >= 30:
		#enviamos el archvio del dias anterior
		if os.path.exists(FileLast):
			p = open(FileLast)
			lastsendfile = p.readline()
			p.close()
			#-----------------------------------------------------------------------
			if len(lastsendfile) == 12:
				letras = SendFileFTP(lastsendfile, newpath)
				if letras.find("Transfer complete") >= 0:
					print("Archivo enviado...BCK")
				else:
					print("No se logro completar el envio...BCK")
					Log = open(FileLog,'a')
					Log.write("---------------------------\n")
					Log.write("File past<" + lastsendfile + "> NO sent." + '\n')
					Log.close()
			else:
				print("Archivo LastSend.txt con error.")
				Log = open(FileLog,'a')
				Log.write("---------------------------\n")
				Log.write("File past:<" + lastsendfile + "> ERROR" + '\n')
				Log.close()

			os.remove(FileLast)
			#-----------------------------------------------------------------------
		else:
			print("No existe: ", FileLast)


letras = SendFileFTP(newfile, newpath)
if letras.find("Transfer complete") >= 0:
	print("Archivo enviado...2")
else:
	Log = open(FileLog,'a')
	Log.write("---------------------------\n")
	Log.write("File " + os.path.join(newpath, newfile) + " NO sent." + '\n')
	Log.close()
	print("No se logro completar el envio...2")
