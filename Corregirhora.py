import sys
import time
import datetime
import os



NameFile = sys.argv[1]      #Format name file: DDMMYYYY_XX.txt
DD = int(NameFile[0:2])
MM = int(NameFile[2:4])
YYYY = int(NameFile[4:8])

signo = sys.argv[2]     #Format: HHMM

ValueTime = sys.argv[3]     #Format: HHMM
hh = int(ValueTime[0:2])
mm = int(ValueTime[2:4])

NameFile = os.path.join("/home/magnet/MagnetProgram8CH/DataMin", NameFile)
f = open(NameFile,'r')
lines = f.readlines()
f.close()

h = open(NameFile + ".cor", 'w')
for i in lines:
    a = i.split()
    if len(a) != 10:
        continue
    try:
        hora = int(a[3])
        minuto = int(a[4])
        line_date = datetime.datetime(YYYY, MM, DD, hora, minuto, 0, 0)
        diff_date = datetime.timedelta(hours = hh, minutes = mm)
        if signo == "+":
            new_date = line_date + diff_date
        elif signo == "-":
            new_date = line_date - diff_date

        new_hora = new_date.strftime("%H")
        new_minuto = new_date.strftime("%M")
        a[3] = new_hora
        a[4] = new_minuto
        new_line = " " + a[0] + " " + a[1] + " " + a[2] + "  " + a[3] + " " + a[4] + "  " + a[5] + " " + a[6] + " " + a[7] + " " + a[8] + " " + a[9]
        h.write(new_line + "\n")

    except:
        continue
h.close()