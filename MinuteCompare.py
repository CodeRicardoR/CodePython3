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
	return(DataD,DataH,DataZ,name_station)


def Plotter(canal1,canal2,title_figure,label_1,label_2,name_file,flag_ylabel):

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
		ax.set_ylabel("Declination Angle (°)")
	
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

file_jica  = sys.argv[1]
file_emb04 = sys.argv[2]
hour = int(sys.argv[3])

a = len(file_jica)

dia = file_jica[a-9:a-7]
mes = file_jica[a-7:a-4]
ano = file_jica[a-3:a-1]

file_image = "Image.png"

print ("file image:",file_image)

#	Lectura de archivos de datos:
if not os.path.exists(file_jica):
	f=open(file_jica,"w")
	f.close()

if not os.path.exists(file_emb04):
	f=open(file_emb04,"w")
	f.close()



f1=open(file_jica,"r")
lines1 = f1.readlines()
f1.close()
	
f2=open(file_emb04,"r")
lines2 = f2.readlines()
f2.close()



#	Generando listas de datos:
DataD1,DataH1,DataZ1,Name1 = ReadFile(lines1, [0, 0, 0])
DataD2,DataH2,DataZ2,Name2 = ReadFile(lines2, [0, 0, 0])


pos = hour*60
DataD1,DataH1,DataZ1,Name1 = ReadFile(lines1, [DataD1[pos], DataH1[pos], DataZ1[pos]])
DataD2,DataH2,DataZ2,Name2 = ReadFile(lines2, [DataD2[pos], DataH2[pos], DataZ2[pos]])

#	Generando graficas de datos:
fecha_data = dia + "/" + mes + "/" + "20" + ano

Plotter(DataD1,DataD2,"Component D     " + fecha_data,Name1, Name2,"CompD_" + file_image,1)
Plotter(DataH1,DataH2,"Component H     " + fecha_data,Name1, Name2,"CompH_" + file_image,0)
Plotter(DataZ1,DataZ2,"Component Z     " + fecha_data,Name1, Name2,"CompZ_" + file_image,0)



print ("termino script")

#Huancayo
#-12.041327, -75.320494
#H = 24421.3
#D = -4.233
#Z = -654.0

#24 08 2023 05 00 +01.3434 -00115.8 -00031.8 -164.6360 +00120.1

e_D = -4.233 - 1.3434
e_H = 24421.3 + 115.8
a_z = -654.0 + -31.8

