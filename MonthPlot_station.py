import os
import glob
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import sys



DicMonths = {0:['Cero','cer',0],1:['January','jan',31],2:['February','feb',28],3:["March",'mar',31],4:["April",'apr',30],
5:["May",'may',31],6:["June",'jun',30],7:["July",'jul',31],8:["August",'aug',31],9:["September",'sep',30],
10:["October",'oct',31],11:["November",'nov',30],12:["December",'dec',31]}



def GetData(ListFiles, base, days):
	DataH = []
	
	for i in range(1440*days):
		DataH.append(None)

		
	for NameFile in ListFiles:
		print(NameFile)
		n_day = int(NameFile[3:5]) - 1
		f = open(NameFile, 'r')
		lines = f.readlines()
		f.close()
		
		flag = 0
		
		for i in lines:
			a = i.split()
			if len(a) != 10:
				continue
			
			try:
				if flag == 0:
					h_ini = float(a[6])
					flag = 1

				hora = int(a[3]) + 24*n_day
				minuto = int(a[4])
				time_data = hora*60 + minuto
				DataH[time_data] = float(a[6]) - h_ini

			except:
				continue
	
	return(DataH)
	
	


PathData = "/home/ricardo/Documents/Python3/DataMin"
Month = int(sys.argv[1])
DataYea = sys.argv[2]

Monthfile = DicMonths[Month][1]
days = DicMonths[Month][2]





l_base = {'jic':24500.0, 'are':22875.0}




#--------------------------------------------------
os.chdir(os.path.join(PathData, 'nazc'))
ListFiles = glob.glob("naz*" + Monthfile + "." + DataYea[-2:] + "m")
ListFiles.sort()
DataNazc = GetData(ListFiles, l_base['jic'], days)

os.chdir(os.path.join(PathData, 'areq'))
ListFiles = glob.glob("are*" + Monthfile + "." + DataYea[-2:] + "m")
ListFiles.sort()
DataAreq = GetData(ListFiles, l_base['are'], days)

os.chdir(os.path.join(PathData, 'jica'))
ListFiles = glob.glob("jic*" + Monthfile + "." + DataYea[-2:] + "m")
ListFiles.sort()
DataJica = GetData(ListFiles, l_base['are'], days)

			
time = []
conta = 0
for i in range(1440*days):
	time.append((conta + 1)/(60.0*24))
	conta = conta + 1


f, ax = plt.subplots(figsize=(50,4))

titulo = "Variacion de Componente H en " + DicMonths[Month][0] + " " + DataYea 
f.suptitle(titulo)


ax.plot(time, DataNazc, 'b', label = "Nazca")
ax.plot(time, DataAreq, 'r', label = "Arequipa")
ax.plot(time, DataJica, 'g', label = "Jicamarca")
#x.set_title('Jicamarca')



ax.set_xlim(0, days)
ax.set_xlabel("Days")
ax.set_ylabel("Amplitud")

majorLocator   = MultipleLocator(2)
majorFormatter = FormatStrFormatter('%d')
minorLocator   = MultipleLocator(1)

ax.xaxis.set_major_locator(majorLocator)
ax.xaxis.set_major_formatter(majorFormatter)
ax.xaxis.set_minor_locator(minorLocator)
ax.grid()

legend = ax.legend(shadow=False,bbox_to_anchor=(0.3, 0.2),fontsize = 12)



plt.show()
