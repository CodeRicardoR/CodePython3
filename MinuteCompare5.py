import matplotlib
matplotlib.use('Agg')

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
	return(DataD, DataH, DataZ, name_station)


def Plotter(canal1, canal2, canal3, canal4, canal5, title_figure, label_1, label_2, label_3, label_4, label_5, name_file, flag_ylabel):

	time = []
	conta = 0
	for i in range(len(canal1)):
		time.append((i+1)/60.0)
		conta = conta + 1


	majorLocator   = MultipleLocator(2)
	majorFormatter = FormatStrFormatter('%d')
	minorLocator   = MultipleLocator(1)


	f, ax = plt.subplots(figsize=(15,7))
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
	#	Grafica de canal4
	ax.plot(time,canal4,'y',label = label_4)
	#------------------------------------------------------
	#	Grafica de canal5
	ax.plot(time,canal5,'c',label = label_5)
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

	legend = ax.legend(shadow=False,bbox_to_anchor=(0.3, 0.9),fontsize = 12)
	name_file = "/home/ricardo/Downloads/" + name_file
	print(name_file)
	plt.savefig(name_file, dpi=500, bbox_inches = "tight")
	plt.close()
	#plt.show()
	
def GenerarMagnetogramas(file_jica, file_test1, file_test2, file_test3, file_test4):

	a = len(file_jica)
	dia = file_jica[a-9:a-7]
	mes = file_jica[a-7:a-4]
	ano = file_jica[a-3:a-1]

	os.chdir("/home/ricardo/Documents/Python3")
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
		
	if not os.path.exists(file_test3):

		f=open(file_test3, 'w')
		f.close()
		
	if not os.path.exists(file_test4):

		f=open(file_test4, 'w')
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

	f4 = open(file_test3, 'r')
	lines4 = f4.readlines()
	f4.close()

	f5 = open(file_test4, 'r')
	lines5 = f5.readlines()
	f5.close()


	#	Generando listas de datos para determinacion de offset:
	DataD1,DataH1,DataZ1,Name1 = ReadFile(lines1, [0, 0, 0])
	DataD2,DataH2,DataZ2,Name2 = ReadFile(lines2, [0, 0, 0])
	DataD3,DataH3,DataZ3,Name3 = ReadFile(lines3, [0, 0, 0])
	DataD4,DataH4,DataZ4,Name4 = ReadFile(lines4, [0, 0, 0])
	DataD5,DataH5,DataZ5,Name5 = ReadFile(lines5, [0, 0, 0])
	
	#	Generar lista de datos a graficar
	DataD1x,DataH1x,DataZ1x,Name1 = ReadFile(lines1, [DataD1[60*11], DataH1[60*11] ,DataZ1[60*11]])
	DataD2x,DataH2x,DataZ2x,Name2 = ReadFile(lines2, [DataD2[60*11], DataH2[60*11] ,DataZ2[60*11]])
	DataD3x,DataH3x,DataZ3x,Name3 = ReadFile(lines3, [DataD3[60*11], DataH3[60*11] ,DataZ3[60*11]])
	DataD4x,DataH4x,DataZ4x,Name4 = ReadFile(lines4, [DataD4[60*11], DataH4[60*11] ,DataZ4[60*11]])
	DataD5x,DataH5x,DataZ5x,Name5 = ReadFile(lines5, [DataD5[60*11], DataH5[60*11] ,DataZ5[60*11]])

	#	Generando graficas de datos:
	fecha_data = dia + "/" + mes + "/" + "20" + ano
	fecha_data2 = dia + mes + ano + ".png"

	Plotter(DataD1x, DataD2x, DataD3x, DataD4x, DataD5x, "Component D     " + fecha_data, Name1, Name2, Name3, Name4, Name5, "CompD_" + fecha_data2, 1)
	Plotter(DataH1x, DataH2x, DataH3x, DataH4x, DataH5x, "Component H     " + fecha_data, Name1, Name2, Name3, Name4, Name5, "CompH_" + fecha_data2, 0)
	Plotter(DataZ1x, DataZ2x, DataZ3x, DataZ4x, DataZ5x, "Component Z     " + fecha_data, Name1, Name2, Name3, Name4, Name5, "CompZ_" + fecha_data2, 0)
	
	os.chdir("/home/ricardo/Downloads/")
	FinalFile = "Total_" + fecha_data2
	os.system("montage " + "CompD_" + fecha_data2 + " " + "CompH_" + fecha_data2 + " " + "CompZ_" + fecha_data2 + " -tile 1x3 -geometry +0+0 " + FinalFile)


#------------------------------------------------------------------------
month = "nov"
year = "23"
iagas = ["jic", "das", "39k", "roj", "tar"]

list_days = []
for i in range(5,6):
	name = "%02d"%i + month + "." + year + "m"
	list_days.append(name)

conta = 0
for day in list_days:
	file_jica  = "DataMin/jica/" + iagas[0] + day
	file_test1 = "DataMin/jica/" + iagas[1] + day
	file_test2 = "DataMin/jica/" + iagas[2] + day
	file_test3 = "DataMin/jica/" + iagas[3] + day
	file_test4 = "DataMin/jica/" + iagas[4] + day
	GenerarMagnetogramas(file_jica, file_test1, file_test2, file_test3, file_test4)
	#conta = conta + 1
	#if conta == 1:
	#	break






print ("termino script")


