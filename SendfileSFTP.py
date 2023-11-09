import sys
import os
import paramiko
import time


def SendFileSFTP(namefile):

	resultado = "Error"
	try:
		transport = paramiko.Transport((host_ip,22))
		transport.connect(username = user, password = password)
		SFTP = paramiko.SFTPClient.from_transport(transport)
		SFTP.chdir(pathserver)
		resultado = SFTP.put(newfile, newfile)
		SFTP.close()
		transport.close()
		
	except:
		pass

	return resultado


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

FilePy = sys.argv[0]
DirWork = os.path.dirname(FilePy)
if DirWork == "":
	DirWork = os.getcwd()

FileLog = os.path.join(DirWork,"FileLogSFTP.txt")
FileLast = os.path.join(DirWork,"LastSend2.txt")

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
		

os.chdir(newpath)

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
	if minute_today >= 15:
		#enviamos el archvio del dias anterior
		if os.path.exists(FileLast):
			p = open(FileLast)
			lastsendfile = p.readline()
			p.close()
			#-----------------------------------------------------------------------
			if len(lastsendfile) == 12:
				letras = SendFileSFTP(lastsendfile)
				if letras.st_size >= 0:
					print("Archivo enviado...BCK")
					os.remove(FileLast)
				else:
					print("No se logro completar el envio...BCK")
					Log = open(FileLog,'a')
					Log.write("---------------------------\n")
					Log.write("File past<" + lastsendfile + "> NO sent." + '\n')
					Log.close()
			else:
				os.remove(FileLast)
				print("Archivo LastSend.txt con error.")
				Log = open(FileLog,'a')
				Log.write("---------------------------\n")
				Log.write("File past:<" + lastsendfile + "> ERROR" + '\n')
				Log.close()
			#-----------------------------------------------------------------------
		else:
			print("No existe: ", FileLast)


letras = SendFileSFTP(newfile)
if letras.st_size >= 0:
	print("Archivo enviado...2")
else:
	Log = open(FileLog,'a')
	Log.write("---------------------------\n")
	Log.write("File " + os.path.join(DirWork,newfile) + " NO sent." + '\n')
	Log.close()
	print("No se logro completar el envio...2")
