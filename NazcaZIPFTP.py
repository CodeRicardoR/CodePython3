import sys
import os
import ftplib
import glob
import time


Month = sys.argv[1]
DataYea = sys.argv[2]

host_ip = "lisn.igp.gob.pe"
user = "cesar"
password = "cev2001gobpe"

pathserver = "/home/cesar/isr/magnetometer/piur/" + DataYea

def SendFileFTP(n_file):
    f = open(n_file,'rb')
    ftp_cmd = 'STOR ' + n_file
    ftp.storbinary(ftp_cmd,f)
    f.close()
    return

ftp = ftplib.FTP(host = host_ip, timeout = 30)
ftp.login(user,password)
ftp.cwd(pathserver)


#DataPath= "/media/usb/DataMagnet"
DataPath = "/home/magnet/MagnetProgram/DataZip"
os.chdir(DataPath)
Listday = glob.glob("*" + Month + DataYea)
Listday.sort()

for dir in Listday:
    newpath = os.path.join(DataPath, dir)
    os.chdir(newpath)

    ListFiles = glob.glob("*")
    ListFiles.sort()

    for Zip_FILE in ListFiles:
        print("Enviando " + Zip_FILE)
        SendFileFTP(Zip_FILE)
        time.sleep(0.3)


ftp.quit()

print("FINISH")
