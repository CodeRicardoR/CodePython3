#! /usr/bin/python2.6

import serial
import time
import subprocess
import sys
from MagnetLib import *


#--------------------------------------------------------------------
def ConvertCMD(bytes):

    rx = ''
    for i in bytes:
        rx = rx + '%c'%i

    pos = rx.find('JRO')
    if (pos == -1) or (pos > 8):
        id_cmd = 'X'
    else:
        id_cmd = rx[pos + 6]
    
    return id_cmd

def SendCMD(ID_CMD):
    global ser
    
    tx_string = bytearray()
    cmd = 'NNNNJROCMD'

    for i in cmd:
        tx_string.append(i)

    tx_string.append(ID_CMD)
    tx_string.append(chr(13))
    tx_string.append(chr(10))

    ser.write(tx_string)
    return
#---------------------------------------------------------------------------------

DicDataSec = {'X':0, 'Y':0, 'Z':0, 'T1':0, 'T2':0}
DicSumSec  = {'X':0, 'Y':0, 'Z':0, 'T1':0, 'T2':0}
DicPathServers = {1:'PathServer1', 2:'PathServer2'}
ContaSec = 0
ContaMin = 0

#Sync Date/Time LISN Server
string_CMD = "/home/magnet/UpdateTime &"
os.system(string_CMD)
print(string_CMD)


DirWork = "/home/magnet"
FileSetuplog = os.path.join(DirWork, 'Setuplog.cfg')
if not os.path.isfile(FileSetuplog):
    CreateFileSetuplog(FileSetuplog)

#read File Setuplog.cfg
DicParams = ReadFileSetup(FileSetuplog)

#Mount USB Device:
time.sleep(15)
StatusUSBData = False
usb = subprocess.Popen(['mount', DicParams['USB'], '/mnt/usb_flash/'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(stdout_value, stderr_value) = usb.communicate()
out_error = stderr_value.decode('utf-8')
print ('Error USB mount:',out_error)
if len(out_error) == 0:
    PathData = os.path.join('/mnt/usb_flash','DataMag')
    StatusUSBData = True
    time.sleep(15)

if StatusUSBData:
    print('Mounting USB device...wait 20 seconds')
    print('PathData: ', PathData)
    print('Dir Work', DirWork)
    os.chdir(DirWork)
else:
    print('Mount USB device failed!')
    sys.exit("***END***")

DataTime = time.strftime("%H%M%S%d%m%y")
#Update Date/time Files
YearFull = '20' + ''.join(DataTime[10:])
PathMin = os.path.join(PathData,YearFull)
PathMin = os.path.join(PathMin,'DataMin')
PathSec = os.path.join(PathData,YearFull)
PathSec = os.path.join(PathSec,'DataSec')
PathZip = os.path.join(PathData,YearFull)
PathZip = os.path.join(PathZip,'DataZip')
PathTem = os.path.join(PathData,YearFull)
PathTem = os.path.join(PathTem,'DataTem')

DicParams['PathM'] = PathMin
DicParams['PathS'] = PathSec
DicParams['PathZ'] = PathZip
DicParams['PathT'] = PathTem

#Update info in Setuplog.cfg
UpdateSetupFile(FileSetuplog, DicParams)

(DateFileMin, DateFileSec, DateFileZip, FormatDateMin, FormatDateSec, FormatDateUi, DataPathSEC, DataPathZIP, Numday) = FechaHora(DicParams,DataTime)
DataPathMinM = os.path.join(DicParams['PathM'], DateFileMin + 'm')
DataPathMinV = os.path.join(DicParams['PathM'], DateFileMin + 'v')

DataPathSec = os.path.join(DataPathSEC, DateFileSec)
DataPathZip = os.path.join(DataPathZIP, DateFileZip)
SecToZip = DataPathSec


CreateFileMinM({}, DicParams, FormatDateMin, DataPathMinM, Numday)
CreateFileMinV({}, DicParams, FormatDateMin, DataPathMinV, Numday)
CreateFileSec({}, DicParams, FormatDateSec, DataPathSec, Numday)

FileHistory = os.path.join(DirWork,'Historial.log')
CreateFilesHistory(DicParams, FormatDateUi, FileHistory)

DicPathServers[1] = DicParams['Server1'] + '/' + YearFull
DicPathServers[2] = DicParams['Server2'] + '/' + YearFull

FileFgx = os.path.join(DirWork,'Fgxfiles.txt')
CreateFgxfiles(DicPathServers, DataPathMinM, DataPathMinV, DataPathSec, DataPathZip, FormatDateUi, FileFgx)

#Test 1:
print('Path SEC: ', SecToZip)
print('Path ZIP: ', DataPathZip)

ser = serial.Serial(port= DicParams['Serial'], baudrate=38400, stopbits=1, parity=serial.PARITY_NONE, bytesize=8, timeout = 3)
ser.flushInput()
ser.flushOutput()

conta = 0
while conta < 60:
    SendCMD('5')
    time.sleep(1)
    SendCMD('0')
    rx_data = ser.read(13)
    ID_CMD0 = ConvertCMD(rx_data)
    if ID_CMD0 == '0':
        print('Stoped Digitizer!....1')
        conta = 0
        break
    else:
        time.sleep(1)
        ser.flushOutput()
        ser.flushInput()
        conta = conta + 1

if conta > 50:
    print("Digitizer failed!...")
    sys.exit("***END***")

print("Starting receive data...in 1 seconds")
ValueSec = int(time.strftime('%S'))
while(ValueSec == int(time.strftime('%S'))):
    pass

EnableADQ = True
while(EnableADQ):
    SendCMD('9')
    InBUF = ser.read(88)        
    RxData = ''
    for l in InBUF:
        RxData = RxData + '%c'%l

    pos = RxData.find('JRO')
    if (pos == -1) or (pos > 8):
        print("JRO No found")
    else:
        BufferX   = RxData[20 : 40]
        BufferY   = RxData[40 : 60]
        BufferZ   = RxData[60 : 80]
        BufferTC  = RxData[80 : 82]
        BufferTS  = RxData[82 : 84]
        BufferGND = RxData[84 : 86]

        ValueX = 0
        ValueY = 0
        ValueZ = 0
        for l in range(10):
            TempX = ord(BufferX[2*l + 1]) + 256*ord(BufferX[2*l])
            TempY = ord(BufferY[2*l + 1]) + 256*ord(BufferY[2*l])
            TempZ = ord(BufferZ[2*l + 1]) + 256*ord(BufferZ[2*l])
            ValueX = TempX + ValueX
            ValueY = TempY + ValueY
            ValueZ = TempZ + ValueZ

        ValueX   = int(ValueX/10)
        ValueY   = int(ValueY/10)
        ValueZ   = int(ValueZ/10)
        ValueTC  = ord(BufferTC[1]) + 256*ord(BufferTC[0])
        ValueTS  = ord(BufferTS[1]) + 256*ord(BufferTS[0])
        ValueGND = ord(BufferGND[1]) + 256*ord(BufferGND[0])

        Max_pos = 2**15 - 1
        if ValueX > Max_pos:
            ValueX = ValueX - 2**16
        if ValueY > Max_pos:
            ValueY = ValueY - 2**16
        if ValueZ > Max_pos:
            ValueZ = ValueZ - 2**16
        if ValueTC > Max_pos:
            ValueTC = ValueTC - 2**16
        if ValueTS > Max_pos:
            ValueTS = ValueTS - 2**16
						
        DicDataSec['X'] = ValueX
        DicDataSec['Y'] = ValueY
        DicDataSec['Z'] = ValueZ
        DicDataSec['T1'] = ValueTC
        DicDataSec['T2'] = ValueTS
        DataTime = time.strftime("%H%M%S%d%m%y")

        #---------------------------------------------------------------------
        # Write Data in files
        #Update Date/time Files
        YearFull = '20' + ''.join(DataTime[10:])
        PathMin = os.path.join(PathData,YearFull)
        PathMin = os.path.join(PathMin,'DataMin')
        PathSec = os.path.join(PathData,YearFull)
        PathSec = os.path.join(PathSec,'DataSec')
        PathZip = os.path.join(PathData,YearFull)
        PathZip = os.path.join(PathZip,'DataZip')
        PathTem = os.path.join(PathData,YearFull)
        PathTem = os.path.join(PathTem,'DataTem')

        DicParams['PathM'] = PathMin
        DicParams['PathS'] = PathSec
        DicParams['PathZ'] = PathZip
        DicParams['PathT'] = PathTem

        (DateFileMin, DateFileSec, DateFileZip, FormatDateMin, FormatDateSec, FormatDateUi, DataPathSEC, DataPathZIP, Numday) = FechaHora(DicParams, DataTime)
        DataPathMinM = os.path.join(DicParams['PathM'], DateFileMin + 'm')
        DataPathMinV = os.path.join(DicParams['PathM'], DateFileMin + 'v')
        DataPathSec = os.path.join(DataPathSEC, DateFileSec)

        NewDataPathZip = os.path.join(DataPathZIP, DateFileZip)
        NewSecToZip = DataPathSec

        ValueSec = int(''.join(DataTime[4:6]))
        ValueMin = int(''.join(DataTime[2:4]))
        
        CreateFileSec(DicDataSec, DicParams, FormatDateSec, DataPathSec, Numday)
        ContaSec = ContaSec + 1
        
        for key in DicDataSec:
            DicSumSec[key] = DicSumSec[key] + DicDataSec[key]
        
        #--------------------------------------------------------------------
        if ValueSec == 59:
            for key in DicSumSec:
                DicSumSec[key] = DicSumSec[key]/ContaSec
            
            CreateFileMinM(DicSumSec, DicParams, FormatDateMin, DataPathMinM, Numday)
            CreateFileMinV(DicSumSec, DicParams, FormatDateMin, DataPathMinV, Numday)
            ContaMin = ContaMin + 1
            print('Data in last minute: ' + str(ContaSec))
            #Reset to zero
            for key in DicSumSec:
                DicSumSec[key] = 0
            ContaSec = 0
        #--------------------------------------------------------------------
        if ValueMin == 0:
            if ValueSec == 20:
                #Test 2:
                #print('Path SEC: ', SecToZip)
                #print('Path ZIP: ', DataPathZip)

                #Compress SecFile
                string_CMD = 'python /home/magnet/CompressFile.py ' + DataPathZip +  ' ' + SecToZip + ' &'
                os.system(string_CMD)
            
            if ValueSec == 30:
                #Send ZipFile to server1
                string_CMD = 'python /home/magnet/SendfileFTP.py ' + DicPathServers[1] + ' ' + DataPathZip + ' /home/magnet/lisn_logon1.txt &'
                os.system(string_CMD)
                #print(string_CMD)

                #Send ZipFile to server2
                string_CMD = 'python /home/magnet/SendfileFTP.py ' + DicPathServers[2] + ' ' + DataPathZip + ' /home/magnet/lisn_logon2.txt &'
                os.system(string_CMD)
                #print(string_CMD)
                
                #Update FilesZip
                DataPathZip = NewDataPathZip
                SecToZip = NewSecToZip
                CreateFgxfiles(DicPathServers, DataPathMinM, DataPathMinV, DataPathSec, DataPathZip, FormatDateUi, FileFgx)
                ContaMin = 0
        #------------------------------------------------------------------
        if ContaMin == int(DicParams['Set']):
            if ValueSec == 15:
                ContaMin = 0
                #Send MinuteFile to server1
                string_CMD = 'python /home/magnet/SendfileFTP.py ' + DicPathServers[1] + ' ' + DataPathMinM + ' /home/magnet/lisn_logon1.txt &'
                os.system(string_CMD)
                #print(string_CMD)

                string_CMD = 'python /home/magnet/SendfileFTP.py ' + DicPathServers[1] + ' ' + DataPathMinV + ' /home/magnet/lisn_logon1.txt &'
                os.system(string_CMD)
                #print(string_CMD)
                
                #Send MinuteFile to server2
                string_CMD = 'python /home/magnet/SendfileFTP.py ' + DicPathServers[2] + ' ' + DataPathMinM + ' /home/magnet/lisn_logon2.txt &'
                os.system(string_CMD)
                #print(string_CMD)

                string_CMD = 'python /home/magnet/SendfileFTP.py ' + DicPathServers[2] + ' ' + DataPathMinV + ' /home/magnet/lisn_logon2.txt &'
                os.system(string_CMD)
                #print(string_CMD)
            
            #Update files and servers
            DicParams = ReadFileSetup(FileSetuplog)
            DicPathServers[1] = DicParams['Server1'] + '/' + YearFull
            DicPathServers[2] = DicParams['Server2'] + '/' + YearFull
        #---------------------------------------------------------------------
    #Wait 1 second
    while(ValueSec == int(time.strftime('%S'))):
        pass

#Rutina to stop digitizer:
flag_stop = True
while(flag_stop):
    SendCMD('5')
    time.sleep(1)
    SendCMD('0')
    rx_data = ser.read(13)
    ID = ConvertCMD(rx_data)
    if ID == '0':
        flag_stop = False
        print('Stoped Digitizer!...2')
    else:
        time.sleep(1)
        ser.flushInput()
        ser.flushOutput()

ser.close()
