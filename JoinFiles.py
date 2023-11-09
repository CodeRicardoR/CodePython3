
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


def joinFiles(FileA, FileB):

    if not os.path.exists(FileA):
        f = open(FileA, 'w')
        f.close()
    
    if not os.path.exists(FileB):
        f = open(FileB, 'w')
        f.close()

    fa = open(FileA, 'r')
    linesA = fa.readlines()
    fa.close()

    fb = open(FileB, 'r')
    linesB = fb.readlines()
    fb.close()

    dayFileA = FileA[-9:-7]
    dayFileB = FileB[-9:-7]
    NewFileName = FileA[:-9] + dayFileA + "-" + dayFileB + FileA[-7:]

    fc = open(NewFileName, 'w')

    for line in linesA:
        fc.write(line)
    
    fc.write("---------------------------------------------------------------\n")

    for line in linesB:
        fc.write(line)
    
    fc.close()

    return NewFileName

def ReadFiles(DataLines):
    DataZ = [None]*1440*2
    
    flag = 0
    name_station = "none"
    conta_line = 0
    day_cero = 0
    for i in DataLines:
        a = i.split()
        if conta_line == 0:
            name_station = a[1]
            conta_line = conta_line + 1
        
        if len(a) != 10:
            continue
        
        try:
            if flag == 0:
                z_ini = float(a[7])
                day_cero = int(a[0])
            
            hora = int(a[3])
            minuto = int(a[4])
            number_day = int(a[0])

            time_data = hora*60 + minuto + 1440*(number_day - day_cero)
            DataZ[time_data] = float(a[7]) - z_ini
            flag = 1
        
        except:
            continue
    
    return(DataZ,name_station)

def Plotter(time_ini, time_end, canal1, canal2, canal3, canal4, title_figure, label_1, label_2, label_3, label_4, name_file):

    canal1 = canal1[60*time_ini: 60*time_end]
    canal2 = canal2[60*time_ini: 60*time_end]
    canal3 = canal3[60*time_ini: 60*time_end]
    canal4 = canal4[60*time_ini: 60*time_end]
    
    time = []
    conta = 0
    for i in range(len(canal1)):
        time.append((i+1)/60.0 + time_ini)
        conta = conta + 1
    
    majorLocator   = MultipleLocator(1)
    majorFormatter = FormatStrFormatter('%02d')
    minorLocator   = MultipleLocator(0.5)
    
    f, ax = plt.subplots(figsize=(15,7))
    #-------------------------------------------------------
    #	Grafica de canal 1
    ax.plot(time, canal1,'r',label = label_1)
    #------------------------------------------------------
    #	Grafica de canal 2
    ax.plot(time, canal2,'b',label = label_2)
    #------------------------------------------------------
    #	Grafica de canal 3
    ax.plot(time, canal3,'g',label = label_3)
    #------------------------------------------------------
    #	Grafica de canal 4
    ax.plot(time, canal4,'y',label = label_4)
    #------------------------------------------------------
    
    #ax.set_ylim(-200,300)
    ax.set_xlim(time_ini, time_end)
    
    ax.set_title(title_figure)
    ax.set_xlabel("Time (UT)")
    ax.set_ylabel("Magnetic Field Intensities (nT)")

    
    plt.grid()
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    
    #for the minor ticks, use no labels; default NullFormatter
    ax.xaxis.set_minor_locator(minorLocator)
    
    legend = ax.legend(shadow=False,bbox_to_anchor=(0.3, 0.9),fontsize = 12)
    name_file = "/home/ricardo/Downloads/" + name_file
    print(name_file)
    #plt.savefig(name_file, dpi=500, bbox_inches = "tight")
    plt.show()
    plt.close()

FileName1A = "DataMin/jic21jun.23m"
FileName1B = "DataMin/jic22jun.23m"

FileName2A = "DataMin/07m21jun.23m"
FileName2B = "DataMin/07m22jun.23m"

FileName3A = "DataMin/das21jun.23m"
FileName3B = "DataMin/das22jun.23m"

FileName4A = "DataMin/39k21jun.23m"
FileName4B = "DataMin/39k22jun.23m"


NewFile1 = joinFiles(FileName1A, FileName1B)
NewFile2 = joinFiles(FileName2A, FileName2B)
NewFile3 = joinFiles(FileName3A, FileName3B)
NewFile4 = joinFiles(FileName4A, FileName4B)

f = open(NewFile1, 'r')
lines1 = f.readlines()
f.close()

f = open(NewFile2, 'r')
lines2 = f.readlines()
f.close()

f = open(NewFile3, 'r')
lines3 = f.readlines()
f.close()

f = open(NewFile4, 'r')
lines4 = f.readlines()
f.close()

(DataZ1, NameStation1) = ReadFiles(lines1)
(DataZ2, NameStation2) = ReadFiles(lines2)
(DataZ3, NameStation3) = ReadFiles(lines3)
(DataZ4, NameStation4) = ReadFiles(lines4)


Plotter(22, 27, DataZ1, DataZ2, DataZ3, DataZ4, "Component Z", NameStation1, NameStation2, NameStation3, NameStation4, "NameFile.png")



