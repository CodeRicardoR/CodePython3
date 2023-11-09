import serial
import threading
import time

Cte = 2500.0/(2**23 - 1)

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
		
		self.ser2 = serial.Serial(port=PORTCOM, baudrate=38400, stopbits=1, parity=serial.PARITY_NONE, bytesize=8, timeout = 3)
		self.ser2.reset_input_buffer()
		self.ser2.reset_output_buffer()
		#-----------------------------------
		if(self.SendCMD2('4')):
			print("Starting receive data...")

			while(EnaStream):
				#Read Header: TimeDate = X..X
				InBUF = self.ser2.read(23)

				RxData = ''
				for l in InBUF:
					RxData = RxData + '%c'%l
				TempDataTime = RxData[9:9+12]

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
				
				DicDataSec['X'] = int(ValX/5)
				DicDataSec['Y'] = int(ValY/5)
				DicDataSec['Z'] = int(ValZ/5)
				DicDataSec['TC'] = int(ValTC/5)
				DicDataSec['TS'] = int(ValTS/5)
				DataTime = TempDataTime
				DataStream = True


			#Rutina to stop digitizer:
			while(self.SendCMD2('5') != True):
				time.sleep(1.3)
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
PORTCOM = "/dev/ttyS0"
ser = serial.Serial(port=PORTCOM, baudrate=38400, stopbits=1, parity=serial.PARITY_NONE, bytesize=8, timeout = 3)
ser.reset_input_buffer()
ser.reset_output_buffer()

DicDataSec = {'X':0, 'Y':0, 'Z':0, 'TC':0, 'TS':0}
DataTime = ''
EnaStream = False
DataStream = False


time.sleep(1)    
if(SendCMD('0')):
	letras = ser.read(25)
	(ID, DATA) = ConvertDAT(letras)
	print(ID + ':' + ''.join(DATA))

time.sleep(1)    
if(SendCMD('8')):
	letras = ser.read(25)
	(ID, DATA) = ConvertDAT(letras)
	print(ID + ':' + ''.join(DATA))

time.sleep(1)    
if(SendCMD('1')):
	letras = ser.read(25)
	(ID, DATA) = ConvertDAT(letras)
	print(ID + ':' + ''.join(DATA))

time.sleep(1)    
if(SendCMD('2')):
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
print('Start Digitizer...')
EnaStream = True
threadRX = ReceiveThread()
threadRX.start()

while(not DataStream):
	pass


SecondNow = int("".join(DataTime[4:6]))
for i in range(61):
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
