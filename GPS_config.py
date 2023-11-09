import serial
import sys

SERIAL_PORT = "/dev/ttyUSB0"
ser = serial.Serial(port = SERIAL_PORT, baudrate=4800, stopbits=1, parity=serial.PARITY_NONE, bytesize=8, timeout = 3)

final_string = chr(13) + chr(10)

cmd = sys.argv[1]

buffer_tx = cmd + final_string

bytesTX = bytearray()
for j in buffer_tx:
    bytesTX.append(ord(j))

ser.write(bytesTX)


ser.close()