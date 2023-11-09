import sys
import os
import ftplib
import time

def SendFileFTP(namefile):
	try:
		ftp = ftplib.FTP(host = host_ip, timeout = 30)
    		ftp.login(user,password)
		ftp.cwd(pathserver)

		f=open(namefile,'rb')
		ftp_cmd = 'STOR ' + namefile
		resultado = ftp.storbinary(ftp_cmd,f)
		f.close()
		ftp.quit()
		return resultado
		
	except:
		f.close()
		ftp.quit()
		return resultado
#----------------------------------------------------------------------

pathserver = sys.argv[1]
bufferfile = sys.argv[2]
file_server = sys.argv[3]

#Separando strings:
pos_chr = bufferfile.rfind('/')
newpath = bufferfile[:pos_chr + 1]
newfile = bufferfile[pos_chr + 1:]


inList = open(file_server, 'rU').readlines()      
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
		
oldpath = os.getcwd()
os.chdir(newpath)


#Determinando la hora y minutos (23:50)
hour_today = int(time.strftime("%H"))
minute_today = int(time.strftime("%M"))
print "Hora: %d:"%hour_today + "%d "%minute_today

if hour_today == 23:
	if minute_today >= 30:
		#Guardando nombre del ultimo archivo enviado:
		if os.path.exists("LastSend.txt"):
			print "Archivo LastSend.txt existe"
		else:
			p=open("LastSend.txt","w")
			p.write(newfile)
			p.close()

if hour_today == 0:
	if minute_today >= 30:
		#enviamos el archvio del dias anterior
		if os.path.exists("LastSend.txt"):
			p=open("LastSend.txt")
			lastsendfile = p.readline()
			p.close()
			if len(lastsendfile) == 12:
				letras = SendFileFTP(lastsendfile)
				if letras.find("Transfer complete") >= 0:
					print "Archivo enviado...1"
					os.remove("LastSend.txt")
				else:
					print "No se logro completar el envio...1"
			else:
				print "Archivo LastSend.txt con error."
				os.remove("LastSend.txt")
		else:
			print "Archivo LastSend.txt no existe."


letras = SendFileFTP(newfile)
if letras.find("Transfer complete") >= 0:
	print "Archivo enviado...2"
else:
	print "No se logro completar el envio...2"

print "***** FIN *****"
quit()




