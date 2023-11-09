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
    ser.flushInput()
    ser.flushOutput()

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
            char_tx = bytearray()
            char_tx.append(ord('O'))
            ser.write(char_tx)
            break
        else:
            print('No Sycn.')

    return(flag_start)
    
def MenErased():
    global ser


    ser.timeout = 5

    flag_erased = False
    char_rx = ser.read(1)
    try: 
        char_erased = ord(char_rx)
    except:
        char_erased = 0
    
    if char_erased == ord('R'):
        flag_erased = True
    else:
        print('No erased')

    return (flag_erased)

def CheckSumFile(NameFile):

    FileHEX = open(NameFile,'r')
    lines = FileHEX.readlines()
    FileHEX.close()

    #Filter lines no data for PIC18F-XC8
    new_lines = lines[:len(lines)-6]

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
        address = int(256*upper_add + lower_add)     #FIRST ADDRES TO LINE
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
        print(str(hex(val1)) + '   ' + str(hex(cc)))
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

    #Filter lines no data for PIC18F-XC8
    new_lines = lines[:len(lines)-6]

    StatusData = True
    DataLines1 = []
    DataLines2 = []
    for line in new_lines:
        buf_line = line[1:len(line)-1]
        DataLines1.append(buf_line)
        DataLines2.append(buf_line)

    #Filtrando solo lineas validas
    for p in range(len(DataLines1)):
        i = DataLines1[p]
        upper_add = int('0x' + i[2:4],16)
        lower_add = int('0x' + i[4:6],16)
        type_line = int('0x' + i[6:8],16)
        address = int(upper_add*256 + lower_add)

        if type_line != 0:
            DataLines2.remove(i)
            print('Removing line ' + str(p) + ': ' + i)

        if address >= 0x7E00:
            StatusData = False
            print('Excedio disponibilidad de Flash...')
            print('Imposible cargar firmware')
            break
    
    #Modificando HEX file:
    CodeBoot = "20EF3FF0FFFFFFFF"   #8 bytes for goto boot
    #----------------------------
    MaskInstr0 = "087FC000FFFFFFFFFFFFFFFFCC"
    list_MaskInstr0 = []
    for i in MaskInstr0:
        list_MaskInstr0.append(i)
    #----------------------------
    CodeInstr0 = DataLines2[0]
    bytes_Instr0 = int('0x' + CodeInstr0[:2], 16)
    list_CodeInstr0 = []
    for i in CodeInstr0:
        list_CodeInstr0.append(i)
    
    list_GotoInstr0 = []
    if (bytes_Instr0 > 3) and (bytes_Instr0 < 8):
        for i in range(bytes_Instr0*2):
            list_GotoInstr0.append(list_CodeInstr0[8 + i])
            list_CodeInstr0[8 + i] = CodeBoot[i]
    elif (bytes_Instr0 >= 8):
        for i in range(8*2):
            list_GotoInstr0.append(list_CodeInstr0[8 + i])
            list_CodeInstr0[8 + i] = CodeBoot[i]
    else:
        print("No cumple longitud de vector de instruccion")
    
    DataLines2[0] = "".join(list_CodeInstr0)

    for i in range(len(list_GotoInstr0)):
        list_MaskInstr0[8 + i] = list_GotoInstr0[i]
    
    MaskInstr0 = "".join(list_MaskInstr0)
    #----------------------------
    DataLines2.append(MaskInstr0)
    #----------------------------

    return (DataLines2, StatusData)

def LoadFirmware(ListData, FileName):
    global ser

    ser.timeout = 5
    ser.flushInput()
    ser.flushOutput()

    carry = []
    LoadError = 0

    f = open(FileName, 'w')

    for p in range(len(ListData) - 1):
        i = ListData[p]
        n_bytes = int('0x' + i[:2], 16)
        upper_add = int('0x' + i[2:4], 16)
        lower_add = int('0x' + i[4:6], 16)
        data_bytes = i[8:8 + 2*n_bytes]

        #Limits address
        address_ini = int(256*upper_add + lower_add)
        address_end = address_ini + n_bytes - 1
        #------------------------------------------------------------------
        #Blocks in 8 bytes
        bytes_left = address_ini%8
        bytes_right = 7 - (address_end%8)
        len_address = bytes_left + n_bytes + bytes_right
        #------------------------------------------------------------------
        # bytes in line HEX 
        bytes_data = []
        for k in range(int(n_bytes)):
            value_byte = int('0x' + ''.join(data_bytes[2*k: 2*k + 2]), 16)
            bytes_data.append(value_byte)
        #------------------------------------------------------------------
        #Default values: Instrutions and address
        temp_data = [0xFF]*len_address
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
        #-----------------------------------------------------------------
        # Data bytes
        for l in range(len(bytes_data)):
            temp_data[l + bytes_left] = bytes_data[l]
        #------------------------------------------------------------------
        #Maxima cantidad de bytes a programar: 16
        final_data = []
        carry = []
        carry_add = []

        if len(temp_data) < 16:
            for count in range(8):
                final_data.append(temp_data[count])
            #Generando nuevo Carry
            for count in range(len(temp_data) - 8):
                carry.append(temp_data[count + 8])
                carry_add.append(temp_address[count + 8])

        else:
            for count in range(16):
                final_data.append(temp_data[count])
            #Generando nuevo Carry
            for count in range(len(temp_data) - 16):
                carry.append(temp_data[count + 16])
                carry_add.append(temp_address[count + 16])
        #------------------------------------------------------------------
        #Enviando datos a uC:
        char_tx = bytearray()       #Char to start
        char_tx.append(ord('S'))                
        ser.write(char_tx)

        #---------------------------------------------
        n_bytes = len(final_data)           #Number of bytes
        t_bytes = int(n_bytes + n_bytes/4)  #TotalBytes
        n_cycles = int(n_bytes/8)           #Number of cycles
        #---------------------------------------------
        char_tx = bytearray()
        char_tx.append(t_bytes)
        char_tx.append(n_cycles)
        ser.write(char_tx)
        f.write("%02X"%n_bytes)

        DataPack = bytearray()
        first_add = temp_address[0]
        upper_add = first_add & 0xFF00
        lower_add = first_add & 0x00FF
        upper_add = upper_add >> 8
        DataPack.append(upper_add)
        DataPack.append(lower_add)

        conta_add = 0
        for l in final_data:
            DataPack.append(l)
            conta_add = conta_add + 1
            if (conta_add % 8 == 0) and (conta_add < len(final_data)):
                first_add = first_add + 8               #in bytes
                upper_add = first_add & 0xFF00
                lower_add = first_add & 0x00FF
                upper_add = upper_add >> 8
                DataPack.append(upper_add)
                DataPack.append(lower_add)
 
        ser.write(DataPack)
        byte_check = ser.read(1)

        #Write in file
        for i in DataPack:
            f.write("%02X"%i)
        f.write('\n')

        BX = byte_check.decode('utf-8')
        if BX != 'X':
            LoadError = LoadError + 1
            print('X ERROR')
    
    #Last carry data
    if len(carry)!= 0:
        temp_data = [0xFF]*8
        for count in range(len(carry)):
            temp_data[count] = carry[count]
        
        #Enviando datos a uC:
        char_tx = bytearray()       #Char to start
        char_tx.append(ord('S'))
        ser.write(char_tx)

        DataPack = bytearray()
        DataPack.append(10)         # Total bytes
        DataPack.append(1)          # Number of cycles
        ser.write(DataPack)
        f.write("%02X"%8)

        DataPack = bytearray()
        first_add = carry_add[0]
        upper_add = first_add & 0xFF00
        lower_add = first_add & 0x00FF
        upper_add = upper_add >> 8
        DataPack.append(upper_add)
        DataPack.append(lower_add)
        for count in temp_data:
            DataPack.append(count)
        
        ser.write(DataPack)
        byte_check = ser.read(1)

        for i in DataPack:
            f.write("%02X"%i)
        f.write('\n')

        BX = byte_check.decode('utf-8')
        if BX != 'X':
            LoadError = LoadError + 1
            print('X ERROR')
    
    #last Goto Instruction
    i = ListData[-1]
    n_bytes = int('0x' + i[:2], 16)
    upper_add = int('0x' + i[2:4], 16)
    lower_add = int('0x' + i[4:6], 16)
    data_bytes = i[8:8 + 2*n_bytes]

    address_ini = int(256*upper_add + lower_add)
    temp_data = []
    for k in range(int(n_bytes)):
        value_byte = int('0x' + ''.join(data_bytes[2*k: 2*k + 2]), 16)
        temp_data.append(value_byte)
    
    #Enviando datos a uC:
    char_tx = bytearray()       #Char to start
    char_tx.append(ord('S'))
    ser.write(char_tx)

    DataPack = bytearray()
    DataPack.append(10)         # Total bytes
    DataPack.append(1)          # Number of cycles
    ser.write(DataPack)
    f.write("%02X"%8)

    DataPack = bytearray()
    first_add = address_ini
    upper_add = first_add & 0xFF00
    lower_add = first_add & 0x00FF
    upper_add = upper_add >> 8
    DataPack.append(upper_add)
    DataPack.append(lower_add)
    for count in temp_data:
        DataPack.append(count)
    
    ser.write(DataPack)
    byte_check = ser.read(1)
    
    for i in DataPack:
        f.write("%02X"%i)
    f.write('\n')
    
    BX = byte_check.decode('utf-8')
    if BX != 'X':
        LoadError = LoadError + 1
        print('X ERROR')

    
    char_tx = bytearray()
    char_tx.append(ord('T'))                #Char to Finish
    ser.write(char_tx)

    byte_check = ser.read(1)
    BF = byte_check.decode('utf-8')
    if BF != 'F':
        LoadError = LoadError + 1
    
    f.close()
    return LoadError


ser = serial.Serial(port = '/dev/ttyS0', baudrate=38400, stopbits=1, parity=serial.PARITY_NONE, bytesize=8)
ser.flushInput()
ser.flushOutput()

File_to_load = filedialog.askopenfilename(initialdir = '/home/ricardo',title = "Select a File",filetypes = (("Hex files","*.hex*"),("all files","*.*")))

Status_file = CheckSumFile(File_to_load)
if Status_file:
    print('CHECKSUM OK.')
    (DataHex, StatusHex) = filterHexfile(File_to_load)
    if StatusHex:
        print('HEX file OK')
        f = open("HEX_file5.txt",'w')
        for i in DataHex:
            f.write(i + '\n')
        f.close()
        Status_sync = SyncMCU()
        if Status_sync:
            print('SYNC OK.')
            Status_erase = MenErased()
            if Status_erase:
                print('FLASH Erased')
                Status_load = LoadFirmware(DataHex,"FileX5.txt")
                if Status_load == 0:
                    print("Firmware load OK")
                else:
                    print("Error in load new firmware")
else:
    print('CHECKSUM ERROR...')

ser.close()

print("***Finish***")
