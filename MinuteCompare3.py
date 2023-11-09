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



def ReadFile(DataLines):
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
			if flag == 0:
				d_ini = float(a[5])
				h_ini = float(a[6])
				z_ini = float(a[7])

			hora = int(a[3])
			minuto = int(a[4])
			time_data = hora*60 + minuto
			DataD[time_data] = (float(a[5]) - d_ini)*60.0
			DataH[time_data] = float(a[6]) - h_ini
			DataZ[time_data] = float(a[7]) - z_ini
			flag = 1
			
		except:
			continue
	return(DataD,DataH,DataZ,name_station)


def Plotter(canal1, canal2, canal3, title_figure, label_1, label_2, label_3, name_file, flag_ylabel):

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
	ax.plot(time,canal1,'r',label = label_1)
	#------------------------------------------------------
	#	Grafica de canal2
	ax.plot(time,canal2,'b',label = label_2)
	#------------------------------------------------------
	#	Grafica de canal3
	ax.plot(time,canal3,'g',label = label_3)
	#------------------------------------------------------

	#ax.set_ylim(-200,300)
	ax.set_xlim(0,24)

	ax.set_title(title_figure)
	ax.set_xlabel("Time (UT)")
	if flag_ylabel == 0:
		ax.set_ylabel("Magnetic Field Intensities (nT)")
	else:
		ax.set_ylabel("Declination Angle (min)")
	
	plt.grid()

	ax.xaxis.set_major_locator(majorLocator)
	ax.xaxis.set_major_formatter(majorFormatter)

	#for the minor ticks, use no labels; default NullFormatter
	ax.xaxis.set_minor_locator(minorLocator)

	legend = ax.legend(shadow=False,bbox_to_anchor=(0.3, 0.2),fontsize = 12)
	#plt.savefig(name_file,dpi=100)
	plt.show()


#------------------------------------------------------------------------


file_jica  = sys.argv[1]
file_test1 = sys.argv[2]
file_test2 = sys.argv[3]


a = len(file_jica)

dia = file_jica[a-9:a-7]
mes = file_jica[a-7:a-4]
ano = file_jica[a-3:a-1]

file_image = "Image.png"

print ("file image:",file_image)

#	Lectura de archivos de datos:
if not os.path.exists(file_jica):
	f=open(file_jica, 'w')
	f.close()

if not os.path.exists(file_test1):
	f=open(file_test1, 'w')
	f.close()

if not os.path.exists(file_test2):
	f=open(file_test2, 'w')
	f.close()
	




f1 = open(file_jica, 'r')
lines1 = f1.readlines()
f1.close()
	
f2 = open(file_test1, 'r')
lines2 = f2.readlines()
f2.close()

f3 = open(file_test2, 'r')
lines3 = f3.readlines()
f3.close()




#	Generando listas de datos:
DataD1,DataH1,DataZ1,Name1 = ReadFile(lines1)
DataD2,DataH2,DataZ2,Name2 = ReadFile(lines2)
DataD3,DataH3,DataZ3,Name3 = ReadFile(lines3)

#	Generando graficas de datos:
fecha_data = dia + "/" + mes + "/" + "20" + ano

Plotter(DataD1, DataD2, DataD3, "Component D     " + fecha_data, Name1, Name2, Name3, "CompD_" + file_image, 1)
Plotter(DataH1, DataH2, DataH3, "Component H     " + fecha_data, Name1, Name2, Name3, "CompH_" + file_image, 0)
Plotter(DataZ1, DataZ2, DataZ3, "Component Z     " + fecha_data, Name1, Name2, Name3, "CompZ_" + file_image, 0)



print ("termino script")


