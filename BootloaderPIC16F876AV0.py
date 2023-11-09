import serial
from tkinter import filedialog
from tkinter import *

def TwoComplement_Cal(number):

    num = 0xFF&number
    bn = "{0:08b}".format(num)
    c_bn = ''
    for c in range(len(bn)):
        if bn[c] == '0':
            c_bn = c_bn + '1'
        else:
            c_bn = c_bn + '0'
    result = (int('0b' + c_bn,2) + 1)&0xFF

    return(result)

def SyncMCU():
    global ser

    ser.timeout = 0.5
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    flag_start = False
    #Wait for 50 seconds
    for i in range(100):
        char_tx = bytearray()
        char_tx.append(0x55)
        ser.write(char_tx)
        char_rx = ser.read(1)
        try:
            char_star = ord(char_rx)
        except:
            char_star = 0

        if char_star == ord('K'):
            flag_start = True
            break
        else:
            print('No Sycn.')

    return (flag_start)

def CheckSumFile(NameFile):

    FileHEX = open(NameFile,'r')
    lines = FileHEX.readlines()
    FileHEX.close()

    #Filter lines no data
    new_lines = lines[1:len(lines)-2]

    #Extract only data
    lines = []
    for line in new_lines:
        buf_line = line[1:len(line)-1]
        lines.append(buf_line)
    
    CheckSum = 0
    for i in lines:
        n_bytes = int('0x' + i[:2],16)
        upper_add = int('0x' + i[2:4],16)
        lower_add = int('0x' + i[4:6],16)
        address = int((256*upper_add + lower_add)/2)
        id_line = int(i[6:8],16)
        data_bytes = i[8:8 + 2*n_bytes]
        cc = int('0x' + i[8+2*n_bytes:8+2*n_bytes +2],16)
        #info_code = str(n_bytes) +',' + str(hex(address)) + ',' + str(hex(id_line)) + ',' + data_bytes + ',' + str(hex(cc))

        #Calculo de CheckSUM
        conta = 0
        bytes_code = []
        for j in range(int(len(data_bytes)/2)):
            j_byte = int(data_bytes[conta: conta + 2],16)
            conta = conta + 2
            bytes_code.append(j_byte)
        
        sum_bytes = 0
        for n in bytes_code:
            sum_bytes = sum_bytes + n
        
        Total_sum = n_bytes + upper_add + lower_add + id_line + sum_bytes
        val1 = TwoComplement_Cal(Total_sum)
        if val1 != cc:
            CheckSum = CheckSum + 1
    
    if CheckSum != 0:
        return False
    else:
        return True

def filterHexfile(NameFile):

    FileHEX = open(NameFile,'r')
    lines = FileHEX.readlines()
    FileHEX.close()

    StatusData = True
    DataLines1 = []
    DataLines2 = []
    for line in lines:
        buf_line = line[1:len(line)-1]
        DataLines1.append(buf_line)
        DataLines2.append(buf_line)

    #Filtrando solo lineas validas
    for p in range(len(DataLines1)):
        i = DataLines1[p]
        upper_add = int('0x' + i[2:4],16)
        lower_add = int('0x' + i[4:6],16)
        type_line = int('0x' + i[6:8],16)
        address = upper_add*256 + lower_add

        if type_line != 0:
            DataLines2.remove(i)
            print('Removing line ' + str(p) + ': ' + i)

        if address >= 0x4000:
            DataLines2.remove(i)
            print('Removing line ' + str(p) + ': ' + i)

        if (address >= 0x3E80) and (address < 0x4000):
            StatusData = False
            print('Excedio disponibilidad de Flash...')
            print('Imposible cargar firmware')

    return (DataLines2, StatusData)


def LoadFirmware(ListData, FileName):
    global ser

    ser.timeout = 5
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    f = open(FileName, 'w')
    
    carry = []
    LoadError = 0
    conta_lines = 0

    for p in range(len(ListData)):
        i = ListData[p]
        n_bytes = int('0x' + i[:2],16)
        upper_add = int('0x' + i[2:4],16)
        lower_add = int('0x' + i[4:6],16)
        data_bytes = i[8:8 + 2*n_bytes]

        #Limits address
        address_ini = int((256*upper_add + lower_add)/2)
        address_end = address_ini + int(n_bytes/2) - 1
        #------------------------------------------------------------------
        bytes_left = address_ini%4
        bytes_right = 3 - (address_end%4)
        len_address = bytes_left + int(n_bytes/2) + bytes_right
        #------------------------------------------------------------------
        bytes_data = []
        for k in range(int(n_bytes/2)):
            data_low = int('0x' + ''.join(data_bytes[4*k: 4*k + 2]),16)
            data_hig = int('0x' + ''.join(data_bytes[4*k + 2: 4*k + 4]),16)
            resul_dat = data_hig*256 + data_low
            bytes_data.append(resul_dat)
        #------------------------------------------------------------------
        #Default values: Instrutions and address
        temp_data = [0x3FFF]*len_address
        temp_address = []
        for d in range(len_address):
            temp_address.append(address_ini - bytes_left + d)
        #------------------------------------------------------------------
        # Carry Option
        try:
            for l in range(bytes_left):
                temp_data[l] = carry[l]
        except:
            pass
        #------------------------------------------------------------------
        # Data words
        for l in range(len(bytes_data)):
            temp_data[l + bytes_left] = bytes_data[l]
        #------------------------------------------------------------------
        #Maxima cantidad de words a programar: 8
        final_data = []
        carry = []
        carry_add = []
        if len(temp_data)<8:
            for count in range(4):
                final_data.append(temp_data[count])
            #Generando nuevo Carry
            for count in range(len(temp_data) - 4):
                carry.append(temp_data[count + 4])
                carry_add.append(temp_address[count + 4])
        else:
            for count in range(8):
                final_data.append(temp_data[count])
            #Generando nuevo Carry
            for count in range(len(temp_data) - 8):
                carry.append(temp_data[count + 8])
                carry_add.append(temp_address[count + 8])

        char_tx = bytearray()       #Char to start
        char_tx.append(ord('S'))                
        ser.write(char_tx)
        
        n_inst = len(final_data)            #Number of instrucctions
        t_bytes = int(n_inst*2 + n_inst/2)  #Totl bytes
        n_cycles = int(n_inst/4)            #Number of cycles

        char_tx = bytearray()
        char_tx.append(t_bytes)
        char_tx.append(n_cycles)
        ser.write(char_tx)
        f.write("%02X"%(char_tx[1]*8))

        DataPack = bytearray()
        first_add = temp_address[0]
        if conta_lines == 0:
            first_add = 0x1FF8
        upper_add = int((first_add&0xFF00)/256)
        lower_add = int(first_add&0x00FF)
        DataPack.append(upper_add)
        DataPack.append(lower_add)

        conta_add = 0
        for l in final_data:
            upper_dat = int((l&0xFF00)/256)
            lower_dat = int(l&0x00FF)
            DataPack.append(upper_dat)
            DataPack.append(lower_dat)
            conta_add = conta_add + 1
            if (conta_add%4 == 0) and (conta_add < len(final_data)):
                first_add = first_add + 4
                upper_add = int((first_add&0xFF00)/256)
                lower_add = int(first_add&0x00FF)
                DataPack.append(upper_add)
                DataPack.append(lower_add)
            
        conta_lines = conta_lines + 1
        ser.write(DataPack)
        byte_check = ser.read(1)

        #Write in file
        for i in DataPack:
            f.write("%02X"%i)
        f.write('\n')

        BX = byte_check.decode('utf-8')
        if BX != 'X':
            LoadError = LoadError + 1
    
    #Last carry data
    if len(carry)!= 0:
        temp_data = [0x3FFF]*4
        for count in range(len(carry)):
            temp_data[count] = carry[count]
        
        #Enviando datos a uC:
        char_tx = bytearray()       #Char to start
        char_tx.append(ord('S'))
        ser.write(char_tx)

        DataPack = bytearray()
        DataPack.append(10)         #Total bytes
        DataPack.append(1)          #number of cycles
        ser.write(DataPack)
        f.write("%02X"%8)

        DataPack = bytearray()
        first_add = carry_add[0]
        upper_add = int((first_add&0xFF00)/256)
        lower_add = int(first_add&0x00FF)
        DataPack.append(upper_add)
        DataPack.append(lower_add)
        for l in temp_data:
            upper_dat = int((l&0xFF00)/256)
            lower_dat = int(l&0x00FF)
            DataPack.append(upper_dat)
            DataPack.append(lower_dat)
        
        ser.write(DataPack)
        byte_check = ser.read(1)

        for i in DataPack:
            f.write("%02X"%i)
        f.write('\n')

        BX = byte_check.decode('utf-8')
        if BX != 'X':
            LoadError = LoadError + 1
    
    f.close()
    char_tx = bytearray()
    char_tx.append(ord('T'))                #Char to Finish
    ser.write(char_tx)

    byte_check = ser.read(1)
    BF = byte_check.decode('utf-8')
    if BF != 'F':
        LoadError = LoadError + 1
    
    return LoadError

ser = serial.Serial(port = '/dev/ttyS0', baudrate=38400, stopbits=1, parity=serial.PARITY_NONE, bytesize=8)
ser.reset_input_buffer()
ser.reset_output_buffer()

File_to_load = filedialog.askopenfilename(initialdir = '/home/ricardo/Documents',title = "Select a File",filetypes = (("Hex files","*.hex*"),("all files","*.*")))

Status_file = CheckSumFile(File_to_load)
if Status_file:
    print('CHECKSUM OK.')
    (DataHex, StatusHex) = filterHexfile(File_to_load)
    if StatusHex:
        Status_sync = SyncMCU()
        if Status_sync:
            print('SYNC OK.')
            Status_load = LoadFirmware(DataHex, "16FHEXfile.txt")
            if Status_load == 0:
                print("Firmware load OK")
            else:
                print("Error in load new firmware")
