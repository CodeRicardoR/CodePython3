import sys
import os
import ftplib
import glob
import time

host_ip = "lisn.igp.gob.pe"
user = "cesar"
password = "cev2001gobpe"
pathserver = "/home/cesar/isr/magnetometer/ancm/2022"

def SendFileFTP(Listfiles):
    os.chdir(Listfiles)
    Zipfiles = glob.glob("*")
    Zipfiles.sort()
    for n_file in Zipfiles:
        f = open(n_file,'rb')
        ftp_cmd = 'STOR ' + n_file
        ftp.storbinary(ftp_cmd,f)
        f.close()
        print(n_file)
    return



DataPath= "/media/usb/DataMagnet"

Month = sys.argv[1]
DataYea = sys.argv[2]

DataPathZip = os.path.join(DataPath, DataYea)
DataPathZip = os.path.join(DataPathZip, "DataZip")
os.chdir(DataPathZip)

ListMonths = glob.glob(Month + "*")
ListMonths.sort()

ListPathMontsZip = []
for DayFile in ListMonths:
    ListPathMontsZip.append(os.path.join(DataPathZip,DayFile))

ftp = ftplib.FTP(host = host_ip, timeout = 30)
ftp.login(user,password)
ftp.cwd(pathserver)

for Dir_files in ListPathMontsZip:
    print("Enviando " + Dir_files)
    SendFileFTP(Dir_files)
    time.sleep(1)

ftp.quit()

print("FINISH")
