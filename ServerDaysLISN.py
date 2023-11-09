import sys
import os
import ftplib
import time

mes = {"jan":31, "feb":29, "mar":31, "apr":30, "may":31, "jun":30, "jul":31, "aug":31, "sep":30, "oct":31, "nov":30, "dec":31}

host_ip = "lisn.igp.gob.pe"
user = "cesar"
password = "cev2001gobpe"

var_mes = sys.argv[2]
path = "/home/cesar/isr/magnetometer/"

ftp = ftplib.FTP(host = host_ip, timeout = 30)
ftp.login(user,password)


path_files = path + sys.argv[1]
ftp.cwd(path_files)

files_server = ftp.nlst()

#Filtrando archivos de mes
data_files = []
for i in files_server:
	pos = i.find(var_mes)
	if (pos == -1) or (pos > 8):
		pass
	else:
		data_files.append(i)
conta = 0
for i in data_files:
	conta = conta + 1
	print ("%02d"%conta," , ",i,"=>",ftp.size(i))

year = int(var_mes[4:6])

mes["feb"] = 28
if (year % 4) == 0:
	mes["feb"] = 29

print ("Total de archivo: ", "%02d"%len(data_files) ,"/", mes[var_mes[:3]])

ftp.quit()
	
	
 


