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
        global EnaStream

        self.ser2 = serial.Serial(port="COM1", baudrate=38400, stopbits=1, parity=serial.PARITY_NONE, bytesize=8, timeout = 3)
        self.ser2.flushInput()
        self.ser2.flushOutput()

        #-----------------------------------
        print("Starting receive data...in 1 seconds")
        Second1 = int(time.strftime('%S'))
        while(Second1 == int(time.strftime('%S'))):
                pass
        
        Second1 = int(time.strftime('%S'))
        while(EnaStream):

            ValX = 0.0
            ValY = 0.0
            ValZ = 0.0
            ValTC = 0.0
            ValTS = 0.0
            ValAUX0 = 0.0
            ValAUX1 = 0.0
            ValAUX2 = 0.0
            Max_pos = 2**23 - 1.0

            if(self.SendCMD2('9')):
                #Read Header: "G-JRODATEXXXXXXXXXXXXAB"
                InBUF = self.ser2.read(23)

                #Read Data
                for s in range(5):
                    InBUF = self.ser2.read(33)
                    
                    RxData = ''
                    for l in InBUF:
                        RxData = RxData + '%c'%l
                    
                    pos = RxData.find('ADQ')
                    if (pos == -1) or (pos > 15):
                        count = 255
                        print("JRO No found")
                        EnaStream = False
                        break
                    else:
                        count = ord(RxData[pos + 3])
                        ValX  =   ValX +  ord(RxData[pos + 4]) +  ord(RxData[pos + 5])*256 +   ord(RxData[pos + 6])*(256**2)
                        ValY  =   ValY +  ord(RxData[pos + 7]) +  ord(RxData[pos + 8])*256 +   ord(RxData[pos + 9])*(256**2)
                        ValZ  =   ValZ +  ord(RxData[pos + 10]) + ord(RxData[pos + 11])*256 +  ord(RxData[pos + 12])*(256**2)
                        ValTC  =  ValTC + ord(RxData[pos + 13]) + ord(RxData[pos + 14])*256 +  ord(RxData[pos + 15])*(256**2)
                        ValTS  =  ValTS + ord(RxData[pos + 16]) + ord(RxData[pos + 17])*256 +  ord(RxData[pos + 18])*(256**2)
                        ValAUX0  =  ValAUX0 + ord(RxData[pos + 19]) + ord(RxData[pos + 20])*256 +  ord(RxData[pos + 21])*(256**2)
                        ValAUX1  =  ValAUX1 + ord(RxData[pos + 22]) + ord(RxData[pos + 23])*256 +  ord(RxData[pos + 24])*(256**2)
                        ValAUX2  =  ValAUX2 + ord(RxData[pos + 25]) + ord(RxData[pos + 26])*256 +  ord(RxData[pos + 27])*(256**2)
                
                ValX = ValX/5.0
                ValY = ValY/5.0
                ValZ = ValZ/5.0
                ValTC = ValTC/5.0
                ValTS = ValTS/5.0
                ValAUX0 = ValAUX0/5.0
                ValAUX1 = ValAUX1/5.0
                ValAUX2 = ValAUX2/5.0

                if ValX > Max_pos:
                    ValX = ValX - 2**24
                if ValY > Max_pos:
                    ValY = ValY - 2**24
                if ValZ > Max_pos:
                    ValZ = ValZ - 2**24
                if ValTC > Max_pos:
                    ValTC = ValTC - 2**24
                if ValTS > Max_pos:
                    ValTS = ValTS - 2**24
                if ValAUX0 > Max_pos:
                    ValAUX0 = ValAUX0 - 2**24
                if ValAUX1 > Max_pos:
                    ValAUX1 = ValAUX1 - 2**24
                if ValAUX2 > Max_pos:
                    ValAUX2 = ValAUX2 - 2**24
	
                DicDataSec['X'] = int(ValX - ValueGround)
                DicDataSec['Y'] = int(ValY - ValueGround)
                DicDataSec['Z'] = int(ValZ - ValueGround)
                DicDataSec['TC'] = int(ValTC - ValueGround)
                DicDataSec['TS'] = int(ValTS - ValueGround)
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
ser = serial.Serial(port="COM1", baudrate=38400, stopbits=1, parity=serial.PARITY_NONE, bytesize=8, timeout = 3)
ser.flushInput()
ser.flushInput()

DicDataSec = {'X':0, 'Y':0, 'Z':0, 'TC':0, 'TS':0}
DataTime = ''
EnaStream = False
DataStream = False
ValueGround = 0
Cte = 2500.0/(2**23 - 1)

time.sleep(1)    
if(SendCMD('0')):
    letras = ser.read(25)
    (ID, DATA) = ConvertDAT(letras)
    dat = ''.join(DATA)
    print('Test CMD0 ok')
    print(ID + ':' + dat)

time.sleep(1)    
if(SendCMD('3')):
    letras = ser.read(25)
    (ID, DATA) = ConvertDAT(letras)
    print('Test CMD3 ok')
    RV_byte = ord(DATA[0])
    OffsetReg = ord(DATA[1])*(256**3) + ord(DATA[2])*(256**2) + ord(DATA[3])*256 + ord(DATA[4])
    GaintReg = ord(DATA[5])*(256**3) + ord(DATA[6])*(256**2) + ord(DATA[7])*256 + ord(DATA[8])

    str_RV = "{0:02x}".format(RV_byte)
    str_offset = '0x' + "{0:08x}".format(OffsetReg)
    str_gain = '0x' +  "{0:08x}".format(GaintReg)
    print('RV:' + str_RV)
    print('Offset: ' + str_offset)
    print('Gain: ' + str_gain)

#Read Value Ground
time.sleep(1)
if (SendCMD('6')):
    letras = ser.read(3)
    val = ''
    for n in letras:
        val = val + '%c'%n
    ValueGround =   ord(val[0]) + ord(val[1])*256 + ord(val[2])*(256**2)

    print('Value GND: ' + str(ValueGround) + "   mV: " + '%+012.6f'%(ValueGround*Cte))

ser.close()

time.sleep(1)
print('------------------------')
EnaStream = True
threadRX = ReceiveThread()
threadRX.start()

while(not DataStream):
	pass

SecondNow = int("".join(DataTime[4:6]))
for i in range(30):
    while(SecondNow == int("".join(DataTime[4:6]))):
        pass
    SecondNow = int("".join(DataTime[4:6]))
    dataX =  '%+012.6f'%(DicDataSec['X']*Cte)
    dataY =  '%+012.6f'%(DicDataSec['Y']*Cte)
    dataZ =  '%+012.6f'%(DicDataSec['Z']*Cte)
    dataTC =  '%+012.6f'%(DicDataSec['TC']*Cte)
    dataTS =  '%+012.6f'%(DicDataSec['TS']*Cte)
    print(DataTime," -> ", '%02d'%i, ' X: ' + dataX + ' Y: ' + dataY + ' Z: ' + dataZ + ' TC: ' + dataTC + ' TS: ' + dataTS)

EnaStream = False
while(DataStream):
	pass

print("*** FIN ***")
