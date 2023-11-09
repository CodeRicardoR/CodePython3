import serial
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

def ReadData_simple():

    ValX = 0.0
    ValY = 0.0
    ValZ = 0.0
    ValTC = 0.0
    ValTS = 0.0
    ValAUX0 = 0.0
    ValAUX1 = 0.0
    ValAUX2 = 0.0
    Max_pos = 2**23 - 1.0

    if SendCMD('9'):
        letras = ser.read(23)   #"G-JRODATEXXXXXXXXXXXXAB"

        #Read Data
        for s in range(5):
            InBUF = ser.read(33)

            RxData = ''
            for l in InBUF:
                RxData = RxData + '%c'%l
            
            pos = RxData.find('ADQ')
            if (pos == -1) or (pos > 15):
                count = 255
                print("JRO No found")
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

    return(ValX, ValY, ValZ, ValTC, ValTS, ValAUX0, ValAUX1, ValAUX2)

def ReadGND():

    ValGND = 0
    if SendCMD('6'):
        InBUF = ser.read(3)
        
        RxData = ''
        for l in InBUF:
            RxData = RxData + '%c'%l

        ValGND = ord(RxData[0]) +  ord(RxData[1])*256 +   ord(RxData[2])*(256**2)
    
    return ValGND
        


ser = serial.Serial(port="COM1", baudrate=38400, stopbits=1, parity=serial.PARITY_NONE, bytesize=8, timeout = 3)
ser.reset_input_buffer()
ser.reset_output_buffer()

#----------------------------------------------------
time.sleep(1)
if SendCMD('0'):
    letras = ser.read(25)
    (DAT_ID, DATA) = ConvertDAT(letras)
    dat = ''.join(DATA)
    print('Test CMD0 ok')
    print(DAT_ID + ':' + dat)


time.sleep(1)
if SendCMD('3'):
    letras = ser.read(25)
    (DAT_ID, DATA) = ConvertDAT(letras)
    print('Test CMD3 ok')
    RV_byte = ord(DATA[0])
    OffsetReg = ord(DATA[1])*(256**3) + ord(DATA[2])*(256**2) + ord(DATA[3])*256 + ord(DATA[4])
    GaintReg = ord(DATA[5])*(256**3) + ord(DATA[6])*(256**2) + ord(DATA[7])*256 + ord(DATA[8])

    str_RV = "{0:02x}".format(RV_byte)
    str_offset = "{0:08x}".format(OffsetReg)
    str_gain = "{0:08x}".format(GaintReg)
    print('RV:' + str_RV)
    print('Offset: ' + str_offset)
    print('Gain: ' + str_gain)


Cte = 2500.0/(2**23 - 1)

time.sleep(1)
ValueGND = ReadGND()
print("Value GND: " + '%+012.6f'%(ValueGND*Cte))

time.sleep(1)

Second1 = int(time.strftime('%S'))
while(Second1 == int(time.strftime('%S'))):
    pass

Second1 = int(time.strftime('%S'))
for n in range(10):
    (ValX, ValY, ValZ, ValTC, ValTS, ValAUX0, ValAUX1, ValAUX2) = ReadData_simple()
        
    ValueX = '%+012.6f'%(ValX*Cte)
    ValueY = '%+012.6f'%(ValY*Cte)
    ValueZ = '%+012.6f'%(ValZ*Cte)
    ValueTC = '%+012.6f'%(ValTC*Cte)
    ValueTS = '%+012.6f'%(ValTS*Cte)
    ValueAUX0 = '%+012.6f'%(ValAUX0*Cte)
    ValueAUX1 = '%+012.6f'%(ValAUX1*Cte)
    ValueAUX2 = '%+012.6f'%(ValAUX2*Cte)
    print('X: ' + ValueX + ' Y: ' + ValueY + ' Z: ' + ValueZ + ' TC: ' + ValueTC + ' TS: ' + ValueTS + ' AUX0: ' + ValueAUX0 + ' AUX1: ' + ValueAUX1 + ' AUX2: ' + ValueAUX2)

    #Wait 1 second
    while(Second1 == int(time.strftime('%S'))):
        pass
    Second1 = int(time.strftime('%S'))



ser.close()