#import matplotlib
#matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import sys
import numpy
import os
import ftplib
import os.path
from datetime import date, timedelta
import time



def ReadFile(DataLines, offset):
	DataD = [None]*1440
	DataH = [None]*1440
	DataZ = [None]*1440

		
	flag = 0
	name_station = "none"
	conta_line = 0
	for i in DataLines:
		a = i.split()
		if conta_line == 0:
			name_station = a[1]
			conta_line = conta_line + 1

		if len(a) != 10:
			continue
		try:
			hora = int(a[3])
			minuto = int(a[4])
			time_data = hora*60 + minuto
			DataD[time_data] = float(a[5]) - offset[0]
			DataH[time_data] = float(a[6]) - offset[1]
			DataZ[time_data] = float(a[7]) - offset[2]
			flag = 1
			
		except:
			continue
	return(DataD, DataH, DataZ, name_station)

def ReadFileSec(DataLines, time_hour, offset):

	DicDataSecH = {}
	DicDataSecD = {}
	DicDataSecZ = {}

	conta_line = 0
	for line in DataLines:
		try:
			a = line.split()
			if conta_line == 0:
				name_station = a[1]
				conta_line = conta_line + 1

			minute = a[1]
			D = float(a[3])
			ListDataD = DicDataSecD.get(minute)
			if ListDataD == None:
				DicDataSecD.setdefault(minute, [])
			DicDataSecD[minute].append(D)

			H = float(a[4])
			ListDataH = DicDataSecH.get(minute)
			if ListDataH == None:
				DicDataSecH.setdefault(minute, [])
			DicDataSecH[minute].append(H)

			Z = float(a[5])
			ListDataZ = DicDataSecZ.get(minute)
			if ListDataZ == None:
				DicDataSecZ.setdefault(minute, [])
			DicDataSecZ[minute].append(Z)
		except:
			continue

	ListPromMinuteD = [None]*60
	ListPromMinuteH = [None]*60
	ListPromMinuteZ = [None]*60

	for minute in range(60):
		promD = 0
		for i in DicDataSecD['%02d'%minute]:
			promD = promD + i
		promD = promD/len(DicDataSecD['%02d'%minute])
		ListPromMinuteD[minute] = promD

		promH = 0
		for i in DicDataSecH['%02d'%minute]:
			promH = promH + i
		promH = promH/len(DicDataSecH['%02d'%minute])
		ListPromMinuteH[minute] = promH

		promZ = 0
		for i in DicDataSecZ['%02d'%minute]:
			promZ = promZ + i
		promZ = promZ/len(DicDataSecZ['%02d'%minute])
		ListPromMinuteZ[minute] = promZ

	hour_val = time_hour
	DataD = [None]*1440
	DataH = [None]*1440
	DataZ = [None]*1440

	for i in range(60):
		DataD[hour_val*60 + i] = ListPromMinuteD[i] - offset[0]
		DataH[hour_val*60 + i] = ListPromMinuteH[i] - offset[1]
		DataZ[hour_val*60 + i] = ListPromMinuteZ[i] - offset[2]

	return(DataD, DataH, DataZ, name_station)


def Plotter(canal1, canal2, title_figure, label_1, label_2, name_file, flag_ylabel):

	time = []
	conta = 0
	for i in range(len(canal1)):
		time.append((i+1)/60.0)
		conta = conta + 1


	majorLocator   = MultipleLocator(2)
	majorFormatter = FormatStrFormatter('%d')
	minorLocator   = MultipleLocator(1)


	f, ax = plt.subplots()
	#-------------------------------------------------------
	#	Grafica de canal1
	ax.plot(time,canal1,'b',label = label_1)
	#------------------------------------------------------
	#	Grafica de canal2
	ax.plot(time,canal2,'r',label = label_2)
	#------------------------------------------------------

	#ax.set_ylim(-200,300)
	ax.set_xlim(0,24)

	ax.set_title(title_figure)
	ax.set_xlabel("Time (UT)")
	if flag_ylabel == 0:
		ax.set_ylabel("Magnetic Field Intensities (nT)")
	else:
		ax.set_ylabel("Declination Angle (grades)")
	
	plt.grid()

	ax.xaxis.set_major_locator(majorLocator)
	ax.xaxis.set_major_formatter(majorFormatter)

	#for the minor ticks, use no labels; default NullFormatter
	ax.xaxis.set_minor_locator(minorLocator)

	legend = ax.legend(shadow=False,bbox_to_anchor=(0.3, 0.2),fontsize = 12)
	#plt.savefig(name_file,dpi=100)
	plt.show()


#------------------------------------------------------------------------
	
#	Determinacion de fecha de nombre de archivos:

file_refer  = sys.argv[1]
file_comp1  = sys.argv[2]
file_hour = int(sys.argv[3])


a = len(file_refer)

dia = file_refer[a-9:a-7]
mes = file_refer[a-7:a-4]
ano = file_refer[a-3:a-1]

file_image = "Image.png"

#	Lectura de archivos de datos:
if not os.path.exists(file_refer):
	f = open(file_refer, "w")
	f.close()

if not os.path.exists(file_comp1):
	f = open(file_comp1, "w")
	f.close()



f1 = open(file_refer, "r")
lines1 = f1.readlines()
f1.close()
	
f2 = open(file_comp1, "r")
lines2 = f2.readlines()
f2.close()


#	Generando listas de datos para offset:
DataD1, DataH1, DataZ1, Name1 = ReadFile(lines1, [0, 0, 0])
DataD2, DataH2, DataZ2, Name2 = ReadFileSec(lines2, file_hour, [0, 0, 0])

#	Generando listas de datos para graficos:
DataD1, DataH1, DataZ1, Name1 = ReadFile(lines1, [DataD1[60*file_hour], DataH1[60*file_hour], DataZ1[60*file_hour]])
DataD2, DataH2, DataZ2, Name2 = ReadFileSec(lines2, file_hour, [DataD2[60*file_hour], DataH2[60*file_hour], DataZ2[60*file_hour]])


#	Generando graficas de datos:
fecha_data = dia + "/" + mes + "/" + "20" + ano

Plotter(DataD1, DataD2, "Component D     " + fecha_data, Name1 + " Minute", Name2 + " Sencond", "CompD_" + file_image, 1)
Plotter(DataH1, DataH2, "Component H     " + fecha_data, Name1 + " Minute", Name2 + " Sencond", "CompH_" + file_image, 0)
Plotter(DataZ1, DataZ2, "Component Z     " + fecha_data, Name1 + " Minute", Name2 + " Sencond", "CompZ_" + file_image, 0)

print ("termino script")


