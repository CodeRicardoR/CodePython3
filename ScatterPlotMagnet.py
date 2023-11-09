#!/usr/bin/python3


import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import sys
import os


def ReaFile(NameFile):
    
    Data = {'X':[None]*1440, 'Y':[None]*1440, 'Z':[None]*1440, 'TC':[None]*1440, 'TS':[None]*1440}
    station = ""
    
    try:
        f = open(NameFile,'r')
        lines = f.readlines()
        f.close()
        titulo = lines[0]
        titulo_list = titulo.split(' ')
        station = titulo_list[1]
        
        for i in lines:
            a = i.split()
            if len(a) != 10:
                continue
            
            try:
                hora = int(a[3])
                minuto = int(a[4])
                time_data = hora*60 + minuto
                Data['X'][time_data] = float(a[5])
                Data['Y'][time_data] = float(a[6])
                Data['Z'][time_data] = float(a[7])
                Data['TC'][time_data] = float(a[8])
                Data['TS'][time_data] = float(a[9])

            
            except:
                continue
    except:
        print('No file')
    
    return (Data, station)

def ReaFile2(NameFile):
    
    Data = {'X':[None]*1440, 'Y':[None]*1440, 'Z':[None]*1440, 'TC':[None]*1440, 'TS':[None]*1440}
    station = ""
    
    try:
        f = open(NameFile,'r')
        lines = f.readlines()
        f.close()
        titulo = lines[0]
        titulo_list = titulo.split(' ')
        station = titulo_list[1]
        
        for i in lines:
            a = i.split()
            if len(a) != 13:
                continue
            
            try:
                hora = int(a[3])
                minuto = int(a[4])
                time_data = hora*60 + minuto
                Data['X'][time_data] = float(a[5])
                Data['Y'][time_data] = float(a[6])
                Data['Z'][time_data] = float(a[7])
                Data['TC'][time_data] = float(a[9])
                Data['TS'][time_data] = float(a[8])

            
            except:
                continue
    except:
        print('No file')
    
    return (Data, station)


datafile1 = sys.argv[1]
datafile2 = sys.argv[2]

filename1 = os.path.basename(datafile1)
titulo = filename1[:3].upper() +' -' + filename1[3:8] + filename1[9:11]

(Data1, titulo1) = ReaFile2(datafile1)
(Data2, titulo2) = ReaFile2(datafile2)


XMax = 0
XMin = 9999
for j in Data1['X']:
    if j != None:
        if j>XMax:
            XMax = j
        if j<XMin:
            XMin = j
X1 = range(int(XMin),int(XMax))

YMax = 0
YMin = 9999
for j in Data1['Y']:
    if j != None:
        if j>YMax:
            YMax = j
        if j<YMin:
            YMin = j
Y1 = range(int(YMin),int(YMax))

ZMax = 0
ZMin = 9999
for j in Data1['Z']:
    if j != None:
        if j>ZMax:
            ZMax = j
        if j<ZMin:
            ZMin = j
Z1 = range(int(ZMin),int(ZMax))

TCMax = 0
TCMin = 9999
for j in Data1['TC']:
    if j != None:
        if j>TCMax:
            TCMax = j
        if j<TCMin:
            TCMin = j
TC1 = range(int(TCMin),int(TCMax))

TSMax = 0
TSMin = 9999
for j in Data2['TS']:
    if j != None:
        if j>TSMax:
            TSMax = j
        if j<TSMin:
            TSMin = j

a = TSMin
TSA = [a]
for j in range(5000):
    if (a + j*0.02) < TSMax:
        TSA.append(a + j*0.02)
        
TSMax = 0
TSMin = 9999
for j in Data1['TS']:
    if j != None:
        if j>TSMax:
            TSMax = j
        if j<TSMin:
            TSMin = j

a = TSMin
TSB = [a]
for j in range(5000):
    if (a + j*0.02) < TSMax:
        TSB.append(a + j*0.02)

TS1 = []
for i in range(len(TSA)):
	TS1.append((TSA[i] + TSB[i])/2.0)

val = 0
conta = 0
for n in range(1440):
	if (Data1['TS'][n] != None) and (Data2['TS'][n] != None):
		val = val + abs(Data1['TS'][n] - Data2['TS'][n])
		conta = conta + 1
		
Dif = val/conta
print('erro: ', Dif)



#------   X
f, ax = plt.subplots(figsize=(5,5))
ax.set_title('Channel X - ' + titulo)
ax.plot(Data1['X'], Data2['X'],'r.',label='Data')
ax.plot(X1, X1,'k',label='y = x')
ax.legend(shadow=False,loc='best',bbox_to_anchor=(0.90, 0.30),fontsize = 12)
plt.savefig('/home/ricardo/Documents/Python3/MagnetTUMIMED/2022/Images/SC-X_' + titulo + '.png' ,bbox_inches="tight")
plt.show()

#------   Y
f, ax = plt.subplots(figsize=(5,5))
ax.set_title('Channel Y - ' + titulo)
ax.plot(Data1['Y'], Data2['Y'],'r.',label = 'Data')
ax.plot(Y1, Y1,'k',label='y = x')
ax.legend(shadow=False,loc='best',bbox_to_anchor=(0.90, 0.30),fontsize = 12)
plt.savefig('/home/ricardo/Documents/Python3/MagnetTUMIMED/2022/Images/SC-Y_' + titulo + '.png' ,bbox_inches="tight")
plt.show()

#------   Z
f, ax = plt.subplots(figsize=(5,5))
ax.set_title('Channel Z - ' + titulo)
ax.plot(Data1['Z'], Data2['Z'],'r.',label = 'Data')
ax.plot(Z1, Z1,'k',label='y = x')
ax.legend(shadow=False,loc='best',bbox_to_anchor=(0.90, 0.30),fontsize = 12)
plt.savefig('/home/ricardo/Documents/Python3/MagnetTUMIMED/2022/Images/SC-Z_' + titulo + '.png' ,bbox_inches="tight")
plt.show()


#------   TC
f, ax = plt.subplots(figsize=(5,5))
ax.set_title('Channel TC - ' + titulo)
ax.plot(Data1['TC'], Data2['TC'],'r.',label = 'Data')
ax.plot(TC1, TC1,'k',label='y = x')
ax.legend(shadow=False,loc='best',bbox_to_anchor=(0.90, 0.30),fontsize = 12)
plt.savefig('/home/ricardo/Documents/Python3/MagnetTUMIMED/2022/Images/SC-TC_' + titulo + '.png' ,bbox_inches="tight")
plt.show()

#------   TS
f, ax = plt.subplots(figsize=(10,10))
ax.set_title('Channel TS - ' + titulo)
ax.plot(Data1['TS'], Data2['TS'],'r.',label = 'Data')
ax.plot(TS1, TS1,'k',label='y = x')
ax.text(265,264.6,'Difference: ' + str(Dif) + 'mV',fontsize = 10)
ax.legend(shadow=False,loc='best',bbox_to_anchor=(0.90, 0.30),fontsize = 12)
plt.savefig('/home/ricardo/Documents/Python3/MagnetTUMIMED/2022/Images/SC-TS_' + titulo + '.png' ,bbox_inches="tight")
plt.show()


