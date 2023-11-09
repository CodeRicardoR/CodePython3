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



def ReadFile(DataLines, Flag_second):

	
	DataD = [None]*60*60
	DataH = [None]*60*60
	DataZ = [None]*60*60
	DataTC = [None]*60*60
	DataTS = [None]*60*60
	Constantes = DataLines[1].split(' ')
	Cte1 = float(Constantes[1])
	Cte2 = float(Constantes[3])
	
		
	name_station = "none"
	conta_line = 0
	for i in DataLines:
		a = i.split()
		if conta_line == 0:
			name_station = a[1]
			conta_line = conta_line + 1

		if len(a) != 11:
			continue
			
		if (Flag_second == 0):
			try:
				hora = int(a[0])
				minuto = int(a[1])
				segundo = int(a[2])
				time_data = segundo + minuto*60
				DataH[time_data] = int(a[3])*Cte1 + Cte2
				DataD[time_data] = int(a[4])*Cte1 + Cte2
				DataZ[time_data] = int(a[5])*Cte1 + Cte2
				DataTC[time_data] = int(a[6])*Cte1 + Cte2
				DataTS[time_data] = int(a[7])*Cte1 + Cte2
				
			except:
				continue
		else:
			try:
				hora = int(a[0])
				minuto = int(a[1])
				segundo = int(a[2])
				time_data = segundo + minuto*60
				DataH[time_data] = int(a[3])*Cte1 + Cte2
				DataD[time_data] = int(a[4])*Cte1 + Cte2
				DataZ[time_data] = int(a[5])*Cte1 + Cte2
				DataTC[time_data] = int(a[7])*Cte1 + Cte2
				DataTS[time_data] = int(a[6])*Cte1 + Cte2
				
			except:
				continue
			
	return(DataD,DataH,DataZ,DataTC,DataTS,name_station,hora)


def Plotter(canal1, canal2, title_figure, label_1, label_2, hora):

	time = []
	conta = 0
	for i in range(len(canal1)):
		time.append((i+1)/60.0)
		conta = conta + 1


	majorLocator   = MultipleLocator(10)
	majorFormatter = FormatStrFormatter('%d')
	minorLocator   = MultipleLocator(5)


	f, ax = plt.subplots()
	#-------------------------------------------------------
	#	Grafica de canal1
	ax.plot(time,canal1,'b',label = label_1)
	#------------------------------------------------------
	#	Grafica de canal2
	ax.plot(time,canal2,'r',label = label_2)
	#------------------------------------------------------

	#ax.set_ylim(-200,300)
	ax.set_xlim(0,60)

	ax.set_title(title_figure)
	ax.set_ylabel("Component in mv")
	ax.set_xlabel("Hour " + "%02d" %hora)

	
	plt.grid()

	ax.xaxis.set_major_locator(majorLocator)
	ax.xaxis.set_major_formatter(majorFormatter)

	#for the minor ticks, use no labels; default NullFormatter
	ax.xaxis.set_minor_locator(minorLocator)

	legend = ax.legend(shadow=False,bbox_to_anchor=(0.3, 0.2),fontsize = 12)
	plt.show()


def Scatter(canal1, canal2, title_figure):

	f, ax = plt.subplots()
	ax.scatter(canal1, canal2)
	ax.set_title(title_figure)
	ax.set_aspect('equal', 'box')
	ax.set_ylabel("Data 16bits")
	ax.set_xlabel("Data 24bits")
	
	plt.show()
	
#------------------------------------------------------------------------
	
#	Determinacion de fecha de nombre de archivos:

file_jica  = sys.argv[1]
file_test1 = sys.argv[2]


a = len(file_jica)

dia = file_jica[a-9:a-7]
mes = file_jica[a-7:a-4]
ano = file_jica[a-3:a-1]


#	Lectura de archivos de datos:
if not os.path.exists(file_jica):
	f=open(file_jica, 'w')
	f.close()

if not os.path.exists(file_test1):
	f=open(file_test1, 'w')
	f.close()



f1=open(file_jica, 'r')
lines1 = f1.readlines()
f1.close()
	
f2=open(file_test1, 'r')
lines2 = f2.readlines()
f2.close()


#	Generando listas de datos:
#Cte1 = .30517578125
#Cte2 = .00000000001
DataD1, DataH1, DataZ1, DataTC1, DataTS1, Name1, hora1 = ReadFile(lines1, 0)

#Cte1 = .00029802325940409414
#Cte2 = .00000000001
DataD2, DataH2, DataZ2, DataTC2, DataTS2, Name2, hora2 = ReadFile(lines2, 0)


#	Generando graficas de datos:
fecha_data = "28/10/2023"

Plotter(DataD1, DataD2, "Component D     " + fecha_data, Name1, Name2, hora1)
Scatter(DataD1, DataD2, "Scatter Plot D     " + fecha_data)

Plotter(DataH1, DataH2, "Component H     " + fecha_data, Name1, Name2, hora1)
Scatter(DataH1, DataH2, "Scatter Plot H     " + fecha_data)

Plotter(DataZ1, DataZ2, "Component Z     " + fecha_data, Name1, Name2, hora1)
Scatter(DataZ1, DataZ2, "Scatter Plot Z     " + fecha_data)

Plotter(DataTC1, DataTC2, "Component TC     " + fecha_data, Name1, Name2, hora1)
Scatter(DataTC1, DataTC2, "Scatter Plot TC     " + fecha_data)

Plotter(DataTS1, DataTS2, "Component TS     " + fecha_data, Name1, Name2, hora1)
Scatter(DataTS1, DataTS2, "Scatter Plot TS     " + fecha_data)


print ("termino script")


