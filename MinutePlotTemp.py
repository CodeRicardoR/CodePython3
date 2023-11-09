#!/usr/bin/python3

######################################################################
#
# MagnetPlot.py
#
#	Created on: November 12, 2021
#	    Author: Ricardo V. Rojas Quispe
# 	    e-mail: net85.ricardo@gmail.com
#
#	Este script se encarga de graficar los datos de los archivos
#	de minutos 
#
######################################################################

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import sys

f = open(sys.argv[1],'r')
lines = f.readlines()
f.close()

titulo = lines[0]
titulo = titulo[:len(titulo) - 1]

DataTC = [None]*1440
DataTS = [None]*1440

for i in lines:
	a = i.split()
	if len(a) != 10:
		continue
	try:
		hora = int(a[3])
		minuto = int(a[4])
		time_data = hora*60 + minuto
		DataTC[time_data] = float(a[8])/10.0
		DataTS[time_data] = float(a[9])/10.0                
	except:
		continue

time = []
conta = 0
for i in range(len(DataTC)):
	time.append((conta + 1)/60.0)
	conta = conta + 1

try:
	f, ax = plt.subplots(figsize=(10,5))
	ax.plot(time,DataTC,'r',label = "Inside Control Unit")
	ax.plot(time,DataTS,'b',label = "Inside Sensor Unit")
	
	ax.set_xlim(0,24)
	ax.set_title(titulo)
	ax.set_ylabel("Temperature (Degrees Celsius)")
	ax.set_xlabel('Time (UT)')
	
	majorLocator   = MultipleLocator(2)
	majorFormatter = FormatStrFormatter('%d')
	minorLocator   = MultipleLocator(1)
	
	ax.xaxis.set_major_locator(majorLocator)
	ax.xaxis.set_major_formatter(majorFormatter)
	ax.xaxis.set_minor_locator(minorLocator)
	ax.grid()
	
	ax.legend(shadow=False,loc='best',bbox_to_anchor=(0.370, 0.160),fontsize = 12)
	plt.show()
	plt.close()

except:
	pass
	
