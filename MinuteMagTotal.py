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

DataD = []
DataH = []
DataZ = []

flag = False
for i in lines:
	a = i.split()
	if len(a) != 10:
		continue
	try:
		if not flag:
			d_ini = float(a[5])
			h_ini = float(a[6])
			z_ini = float(a[7])
		

		DataD.append((float(a[5]) - d_ini)*60.0)
		DataH.append(float(a[6]) - h_ini)
		DataZ.append(float(a[7]) - z_ini - 50)
		flag = True
	except:
		continue
	
time = []
conta = 0
for i in range(len(DataD)):
	time.append((conta + 1)/60.0)
	conta = conta + 1
	
try:
	f, ax = plt.subplots(figsize=(10,5))
	ax2 = ax.twinx()
	ax.plot(time,DataH,'b',label = 'Horizontal component (H)')
	ax.plot(time,DataZ,'g',label = 'Vertical component (Z)')
	ax2.plot(time,DataD,'r',label = 'Declination angle (D)')
	
	#ax.set_ylim(-100,150)
	#ax.set_xlim(0,24)
	ax.set_title(titulo)
	ax.set_ylabel('H & Z Magnetic Field Intensities (nT)')
	ax.set_xlabel('Time (UT)')
	
	majorLocator   = MultipleLocator(2)
	majorFormatter = FormatStrFormatter('%d')
	minorLocator   = MultipleLocator(1)
	
	ax.xaxis.set_major_locator(majorLocator)
	ax.xaxis.set_major_formatter(majorFormatter)
	ax.xaxis.set_minor_locator(minorLocator)
	ax.grid()
	
	#ax2.set_ylim(-20,5)
	#ax2.set_xlim(0,24)
	ax2.set_ylabel('Declination Angle (min)')
	
	ax.legend(shadow=False,loc='best',bbox_to_anchor=(0.370, 0.160),fontsize = 12)
	ax2.legend(shadow=False,loc='best',bbox_to_anchor=(0.700, 0.160),fontsize = 12)
	plt.show()
	plt.close()
	
except:
	pass
		
