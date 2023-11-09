import serial
import threading
import time

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
	
	cmd = 'NNNNJROCMD' + ID_CMD + chr(13) + chr(10)
	ser.write(cmd.encode())
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

        #-----------------------------------
        self.ser2 = serial.Serial(port= PORT_SERIAL, baudrate=38400, stopbits=1, parity=serial.PARITY_NONE, bytesize=8, timeout = 3)
        self.ser2.reset_input_buffer()
        self.ser2.reset_output_buffer()

        print("Starting receive data...in 1 seconds")
        Second1 = int(time.strftime('%S'))
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
                for s in range(10):
                    InBUF = self.ser2.read(31)

                    RxData = ''
                    for l in InBUF:
                        RxData = RxData + '%c'%l
                    
                    count = 0
                    pos = RxData.find('JRO')
                    if (pos == -1) or (pos > 8):
                        count = 255
                        print("JRO No found")
                    else:
                        count = ord(RxData[pos + 7])
                        value1 = RxData[pos + 8  : pos + 12]
                        value2 = RxData[pos + 12 : pos + 16]
                        value3 = RxData[pos + 16 : pos + 20]
                        value4 = RxData[pos + 20 : pos + 24]
                        value5 = RxData[pos + 24 : pos + 28]

                        ValueX  = ord(value1[3])*(256**3) + ord(value1[2])*(256**2) + ord(value1[1])*256 + ord(value1[0])
                        ValueY  = ord(value2[3])*(256**3) + ord(value2[2])*(256**2) + ord(value2[1])*256 + ord(value2[0])
                        ValueZ  = ord(value3[3])*(256**3) + ord(value3[2])*(256**2) + ord(value3[1])*256 + ord(value3[0])
                        ValueTC = ord(value4[3])*(256**3) + ord(value4[2])*(256**2) + ord(value4[1])*256 + ord(value4[0])
                        ValueTS = ord(value5[3])*(256**3) + ord(value5[2])*(256**2) + ord(value5[1])*256 + ord(value5[0])
                        Max_pos = 2**31 - 1
                        if ValueX > Max_pos:
                            ValueX = ValueX - 2**32     
                        if ValueY > Max_pos:
                            ValueY = ValueY - 2**32       
                        if ValueZ > Max_pos:
                            ValueZ = ValueZ - 2**32
                        if ValueTC > Max_pos:
                            ValueTC = ValueTC - 2**32
                        if ValueTS > Max_pos:
                            ValueTS = ValueTS - 2**32
                        
                        ValX = ValX + ValueX
                        ValY = ValY + ValueY
                        ValZ = ValZ + ValueZ
                        ValTC = ValTC + ValueTC
                        ValTS = ValTS + ValueTS
                    
                
                DicDataSec['X'] = int(ValX/10.0)
                DicDataSec['Y'] = int(ValY/10.0)
                DicDataSec['Z'] = int(ValZ/10.0)*(-1)
                DicDataSec['TC'] = int(ValTC/10.0)*(-1)
                DicDataSec['TS'] = int(ValTS/10.0)*(-1)
                DataTime = time.strftime("%H%M%S%d%m%y")
                DataStream = True
            
            #Wait 1 second
            while(Second1 == int(time.strftime('%S'))):
                pass
            Second1 = int(time.strftime('%S'))
        
        #Rutina to stop digitizer:
        time.sleep(0.5)
        while(self.SendCMD2('5') != True):
            time.sleep(1.3)
            print('Stoping Digitizer')
        
        DataStream = False
        #-----------------------------------	
        print("Finish receive data.")
        self.ser2.close()
    
    def SendCMD2(self, ID_CMD):
        
        cmd = 'NNNNJROCMD' + ID_CMD + chr(13) + chr(10)
        self.ser2.write(cmd.encode())
        letras = self.ser2.read(13)
        ID = self.ConvertCMD2(letras)
        if ID_CMD != ID:
            print('ERROR: CMD = ' + ID)
            return False
        else:
            return True
    
    def ConvertCMD2(self, bytes):
        rx = ''
        
        for i in bytes:
            rx = rx + '%c'%i
        
        pos = rx.find('JRO')
        if (pos == -1) or (pos > 8):
            id_cmd = 'X'
        else:
            id_cmd = rx[pos + 6]
        
        return id_cmd

#---------------------------------------------------------------------------------

PORT_SERIAL = "/dev/ttyUSB0"

ser = serial.Serial(port=PORT_SERIAL, baudrate=38400, stopbits=1, parity=serial.PARITY_NONE, bytesize=8, timeout = 3)
ser.reset_input_buffer()
ser.reset_output_buffer()


DicDataSec = {'X':0.0, 'Y':0.0, 'Z':0.0, 'TC':0.0, 'TS':0.0}
DataTime = ''
EnaStream = False
DataStream = False
Cte = 2500.0/(2**31 - 1)


while(SendCMD('5') != True):
	time.sleep(0.7)
	print('Stoping Digitizer')



print('------------------------')
if(SendCMD('0')):
    print("Digitizer config OK...")
    if(SendCMD('3')):
        print("Digitizer init OK...")
        ser.close()
else:
    ser.close()
    quit()

time.sleep(1)
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
    print(DataTime," -> ", "%02d"%i, ' X: ', "%+013.7f"%(DicDataSec['X']*Cte), ' Y: ', "%+013.7f"%(DicDataSec['Y']*Cte), ' Z: ', "%+013.7f"%(DicDataSec['Z']*Cte), ' TC: ', "%+013.7f"%(DicDataSec['TC']*Cte), ' TS: ', "%+013.7f"%(DicDataSec['TS']*Cte))

EnaStream = False
while(DataStream):
	pass

print("*** FIN ***")
quit()
