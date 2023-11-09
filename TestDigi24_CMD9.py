import serial
import threading
import time

#--------------------------------------------------------------------
def ConvertCMD(letras):

    rx = ''
    for i in letras:
        rx = rx + '%c'%i

    pos = rx.find('JRO')
    if (pos == -1) or (pos > 8):
        id_cmd = 'X'
    else:
        id_cmd = rx[pos + 6]
    
    return id_cmd

def ConvertDAT(letras):

    datos = [0]*12
    rx = ''
    for i in letras:
        rx = rx + '%c'%i
    
    pos = rx.find('JRO')
    if (pos == -1) or (pos > 8):
        id_dat = 'X'
    else:
        id_dat = rx[pos + 6]
        for i in range(len(datos)):
            datos[i] = rx[pos + 7 + i]
    
    return (id_dat,datos)

def SendCMD(ID_CMD):
    global ser
    
    cmd = 'NNNNJROCMD' + ID_CMD + chr(13) + chr(10)

    cmd_tx = bytearray()
    for c in cmd:
        cmd_tx.append(ord(c))

    ser.write(cmd_tx)

    letras = ser.read(13)
    ID = ConvertCMD(letras)
    if ID_CMD != ID:
        print('ERROR: CMD = ' + ID)
        return False
    else:
        return True

class ReceiveThread (threading.Thread):
	
    def run(self):
        global DicDataSec
        global DataTime
        global DataStream

        self.ser2 = serial.Serial(port= PORT_SELECTED, baudrate=38400, stopbits=1, parity=serial.PARITY_NONE, bytesize=8, timeout = 3)
        self.ser2.flushInput()
        self.ser2.flushOutput()
        #-----------------------------------
        print("Starting receive data...in 1 seconds")
        Second1 = int(time.strftime('%S'))
        while(Second1 == int(time.strftime('%S'))):
                pass
        while(EnaStream):
            if(self.SendCMD2('9')):
                #Read Header: TimeDate = X..X
                InBUF = self.ser2.read(23)

                #Read Data
                ValX = 0
                ValY = 0
                ValZ = 0
                ValTC = 0
                ValTS = 0
                for s in range(5):
                    InBUF = self.ser2.read(24)
                    
                    RxData = ''
                    for l in InBUF:
                        RxData = RxData + '%c'%l
                    
                    pos = RxData.find('JRO')
                    if (pos == -1) or (pos > 8):
                        count = 255
                        print("JRO No found")
                    else:
                        count = ord(RxData[pos +  6])
                        ValueX  =  ord(RxData[pos +  7]) + ord(RxData[pos +  8])*256 + ord(RxData[pos +  9])*(256**2)
                        ValueY  =  ord(RxData[pos + 10]) + ord(RxData[pos + 11])*256 + ord(RxData[pos + 12])*(256**2)
                        ValueZ  =  ord(RxData[pos + 13]) + ord(RxData[pos + 14])*256 + ord(RxData[pos + 15])*(256**2)
                        ValueTC =  ord(RxData[pos + 16]) + ord(RxData[pos + 17])*256 + ord(RxData[pos + 18])*(256**2)
                        ValueTS =  ord(RxData[pos + 19]) + ord(RxData[pos + 20])*256 + ord(RxData[pos + 21])*(256**2)
                        Max_pos = 2**23 - 1

                        if ValueX > Max_pos:
                            ValueX = ValueX - 2**24
                        if ValueY > Max_pos:
                            ValueY = ValueY - 2**24
                        if ValueZ > Max_pos:
                            ValueZ = ValueZ - 2**24
                        if ValueTC > Max_pos:
                            ValueTC = ValueTC - 2**24
                        if ValueTS > Max_pos:
                            ValueTS = ValueTS - 2**24
                        
                        ValX = ValX + ValueX
                        ValY = ValY + ValueY
                        ValZ = ValZ + ValueZ
                        ValTC = ValTC + ValueTC
                        ValTS = ValTS + ValueTS
						
                DicDataSec['X'] = int(ValX/5.0)
                DicDataSec['Y'] = int(ValY/5.0)
                DicDataSec['Z'] = int(ValZ/5.0)
                DicDataSec['TC'] = int(ValTC/5.0)
                DicDataSec['TS'] = int(ValTS/5.0)
                DataTime = time.strftime("%H%M%S%d%m%y")
                DataStream = True

            #Wait 1 second
            while(Second1 == int(time.strftime('%S'))):
                pass
            Second1 = int(time.strftime('%S'))
        
        #Rutina to stop digitizer:
        while(self.SendCMD2('5') != True):
            time.sleep(0.7)
            print('Stoping Digitizer')
        DataStream = False
        #-----------------------------------	
        print("Finish receive data.")
        self.ser2.close()
    
    def SendCMD2(self, ID_CMD):
        
        cmd = 'NNNNJROCMD' + ID_CMD + chr(13) + chr(10)

        cmd_tx = bytearray()
        for c in cmd:
            cmd_tx.append(ord(c))

        self.ser2.write(cmd_tx)

        letras = self.ser2.read(13)
        ID = self.ConvertCMD2(letras)
        if ID_CMD != ID:
            print('ERROR: CMD = ' + ID)
            return False
        else:
            return True
    
    def ConvertCMD2(self, letras):
        
        rx = ''
        for i in letras:
            rx = rx + '%c'%i

        pos = rx.find('JRO')
        if (pos == -1) or (pos > 8):
            id_cmd = 'X'
        else:
            id_cmd = rx[pos + 6]
        
        return id_cmd

#---------------------------------------------------------------------------------
PORT_SELECTED = "/dev/ttyUSB2"
ser = serial.Serial(port=PORT_SELECTED, baudrate=38400, stopbits=1, parity=serial.PARITY_NONE, bytesize=8, timeout = 3)
ser.flushInput()
ser.flushInput()

DicDataSec = {'X':0, 'Y':0, 'Z':0, 'TC':0, 'TS':0}
DataTime = ''
EnaStream = False
DataStream = False
Cte = 2500.0/(2**23 - 1)

#Stoping Digitizer
stop = 0
conta = 0
while stop == 0:
	conta = conta + 1
	print('#: ', conta)
	if SendCMD('5'):
		stop = 1
		break
	else:
		time.sleep(0.3)

time.sleep(1)    
if(SendCMD('0')):
    letras = ser.read(25)
    (ID, DATA) = ConvertDAT(letras)
    print(ID + ':' + ''.join(DATA))

time.sleep(1)    
if(SendCMD('3')):
    letras = ser.read(25)
    (ID, DATA) = ConvertDAT(letras)
    RV_byte = ord(DATA[0])
    OffsetReg = ord(DATA[1])*(256**3) + ord(DATA[2])*(256**2) + ord(DATA[3])*256 + ord(DATA[4])
    GaintReg = ord(DATA[5])*(256**3) + ord(DATA[6])*(256**2) + ord(DATA[7])*256 + ord(DATA[8])

    str_RV = "{0:02x}".format(RV_byte)
    str_offset = "{0:08x}".format(OffsetReg)
    str_gain = "{0:08x}".format(GaintReg)

    print('RV:' + str_RV)
    print('Offset: ' + str_offset)
    print('Gain: ' + str_gain)

time.sleep(1)
if(SendCMD('6')):
	letras = ser.read(3)
	value = ''
	for i in letras:
		value = value + '%c'%i
	value_gnd = ord(value[0]) + ord(value[1])*256 + ord(value[2])*(256**2)
	if value_gnd > (2**23 - 1):
		value_gnd = value_gnd - 2**24

	value_gnd = value_gnd*Cte
	print('GND mv: ', '%+012.6f'%value_gnd)

ser.close()

time.sleep(1)
print('------------------------')
EnaStream = True
threadRX = ReceiveThread()
threadRX.start()

while(not DataStream):
	pass

SecondNow = int("".join(DataTime[4:6]))
for i in range(22):
    while(SecondNow == int("".join(DataTime[4:6]))):
        pass
    SecondNow = int("".join(DataTime[4:6]))
    dataX =  '%+012.6f'%(DicDataSec['X']*Cte)
    dataY =  '%+012.6f'%(DicDataSec['Y']*Cte)
    dataZ =  '%+012.6f'%(DicDataSec['Z']*Cte)
    dataTC =  '%+012.6f'%(DicDataSec['TC']*Cte)
    dataTS =  '%+012.6f'%(DicDataSec['TS']*Cte)
    print(DataTime," -> ", i, ' X: ' + dataX + ' Y: ' + dataY + ' Z: ' + dataZ + ' TC: ' + dataTC + ' TS: ' + dataTS)

EnaStream = False
while(DataStream):
	pass

print("*** FIN ***")
quit()